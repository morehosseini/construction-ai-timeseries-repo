"""Reproduce every figure, table and reported statistic in the paper.

    python analysis/reproduce_paper.py --data data/all_industries_merged.xlsx --out outputs

Input: the Lightcast extract of AI-related job postings (one row per posting, with
`JobID`, `JobDate` and `ANZSIC CODE` columns). The extract is licensed and is not
distributed with this repository; see DATA.md.

Outputs (under --out):
    figures/Figure02..Figure15 (.png, 600 dpi)
    tables/*.csv                (the tables published in supplementary/)
    results.json                (every number quoted in the paper, full panel and
                                 50-month sensitivity panel)
"""
import argparse
import json
import os
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import kruskal, mannwhitneyu, norm, rankdata
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings("ignore")

# ----------------------------------------------------------------------------
# Parameters (Table of analysis parameters in supplementary/)
# ----------------------------------------------------------------------------
SECTORS = ["Construction", "Digital", "Traditional"]
PERIOD = 12            # monthly seasonality
BLOCK = 6              # moving-block length (months)
B = 1500               # bootstrap replications
SEED_MOY = 7           # month-of-year test
SEED_CCF = 123         # cross-correlation bands
MAX_LAG = 6            # CCF lags (months)
ETS_TEST = 8           # rolling one-step evaluation window (months)
HAC_LAGS = 2           # Newey-West lags: floor(4 (T/100)^(2/9)) for T = 17 quarters
PANEL_END = "2025-03-17"
COLOURS = {"Construction": "#1f4e79", "Digital": "#d9822b", "Traditional": "#3a7d44"}


# ----------------------------------------------------------------------------
# Sector mapping (ANZSIC 2006 class codes; see supplementary/sector_mapping.csv)
# ----------------------------------------------------------------------------
def subdivision(code):
    """Two-digit ANZSIC 2006 subdivision of a class code (codes 01xx-09xx arrive without the leading zero)."""
    return int(code) // 100


CONSTRUCTION_SUBDIVISIONS = {30, 31, 32}                       # Division E
DIGITAL_SUBDIVISIONS = {58, 59, 60, 62, 63, 69, 70, 72}        # parts of Divisions J, K, M, N


def sector(code):
    s = subdivision(code)
    if s in CONSTRUCTION_SUBDIVISIONS:
        return "Construction"
    if s in DIGITAL_SUBDIVISIONS:
        return "Digital"
    return "Traditional"


# ----------------------------------------------------------------------------
# Data preparation
# ----------------------------------------------------------------------------
def load(path):
    raw = pd.read_excel(path)
    info = {"rows_in_extract": int(len(raw))}
    raw = raw.dropna(subset=["JobDate", "ANZSIC CODE"])
    info["rows_missing_date_or_code"] = info["rows_in_extract"] - int(len(raw))
    raw = raw.sort_values("JobDate")
    dup = raw["JobID"].duplicated(keep="first")
    info["duplicate_job_ids_removed"] = int(dup.sum())
    raw = raw[~dup].copy()
    raw["Sector"] = raw["ANZSIC CODE"].apply(sector)
    raw["Month"] = raw["JobDate"].dt.to_period("M").dt.to_timestamp()
    info["postings_analysed"] = int(len(raw))
    info["first_date"], info["last_date"] = f"{raw.JobDate.min():%Y-%m-%d}", f"{raw.JobDate.max():%Y-%m-%d}"
    info["engineering_architecture_consultancy_postings_6921_6923"] = int(
        raw["ANZSIC CODE"].isin([6921, 6922, 6923]).sum())
    monthly = (raw.groupby(["Month", "Sector"]).size().unstack(fill_value=0)[SECTORS]
               .asfreq("MS").fillna(0).astype(float))
    return raw, monthly, info


def quarterly(m):
    q = m.groupby(m.index.to_period("Q")).sum()
    return q


# ----------------------------------------------------------------------------
# Methods
# ----------------------------------------------------------------------------
def stl_fit(y):
    return STL(y, period=PERIOD, robust=True).fit()


def seasonal_strength(res):
    """F_S = max(0, 1 - Var(R) / Var(S + R)) (Wang, Smith and Hyndman, 2006)."""
    return max(0.0, 1 - np.var(res.resid, ddof=1) / np.var(res.seasonal + res.resid, ddof=1))


def _mbb_indices(n, rng):
    starts = rng.integers(0, n, size=int(np.ceil(n / BLOCK)))
    return np.concatenate([np.arange(s, s + BLOCK) for s in starts])[:n] % n


def moy_test(detrended):
    """Kruskal-Wallis across calendar months; p-value from a circular moving-block bootstrap of the month labels."""
    rng = np.random.default_rng(SEED_MOY)
    x, mo = detrended.values, detrended.index.month.values
    months = np.unique(mo)
    h_obs = kruskal(*[x[mo == k] for k in months])[0]
    h_boot = np.empty(B)
    for b in range(B):
        mb = mo[_mbb_indices(len(x), rng)]
        h_boot[b] = kruskal(*[x[mb == k] for k in months])[0]
    return float(h_obs), float((np.sum(h_boot >= h_obs) + 1) / (B + 1))


def dunn_holm(detrended):
    """Smallest Holm-adjusted p across the 66 pairwise Dunn tests between calendar months."""
    x, mo = detrended.values, detrended.index.month.values
    r, n = rankdata(x), len(x)
    _, t = np.unique(x, return_counts=True)
    tie = np.sum(t ** 3 - t) / (12 * (n - 1))
    ps = []
    for i in range(1, 13):
        for j in range(i + 1, 13):
            se = np.sqrt((n * (n + 1) / 12 - tie) * (1 / (mo == i).sum() + 1 / (mo == j).sum()))
            ps.append(2 * (1 - norm.cdf(abs(r[mo == i].mean() - r[mo == j].mean()) / se)))
    ps = np.sort(ps)
    adj = np.maximum.accumulate(np.minimum(1, ps * (len(ps) - np.arange(len(ps)))))
    return float(adj[0])


def ccf(x, y):
    """corr(x_t, y_{t+L}); positive L means x (Construction) leads y (comparator)."""
    n = len(x)
    x, y = x - x.mean(), y - y.mean()
    s = np.sqrt((x ** 2).sum() * (y ** 2).sum())
    return {L: float((np.dot(x[:n - L], y[L:]) if L >= 0 else np.dot(x[-L:], y[:n + L])) / s)
            for L in range(-MAX_LAG, MAX_LAG + 1)}


def ccf_bootstrap(x, y):
    """Joint circular moving-block bootstrap of the (x, y) pairs; 95% percentile bands."""
    n, rng, obs = len(x), np.random.default_rng(SEED_CCF), ccf(x, y)
    pairs, boot = np.column_stack([x, y]), {L: np.empty(B) for L in obs}
    for b in range(B):
        starts = rng.integers(0, n, size=int(np.ceil(n / BLOCK)))
        idx = np.concatenate([(np.arange(BLOCK) + s) % n for s in starts])[:n]
        for L, v in ccf(pairs[idx, 0], pairs[idx, 1]).items():
            boot[L][b] = v
    rows = []
    for L in sorted(obs):
        lo, hi = np.percentile(boot[L], [2.5, 97.5])
        rows.append({"lag": L, "r": obs[L], "ci_lower": lo, "ci_upper": hi, "excludes_zero": not (lo <= 0 <= hi)})
    return pd.DataFrame(rows)


def ratio_trend(ratio):
    """OLS linear trend on the quarterly ratio with Newey-West (HAC) 95% confidence interval."""
    x = sm.add_constant(np.arange(len(ratio), dtype=float))
    res = sm.OLS(ratio.values, x).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_LAGS})
    lo, hi = res.conf_int()[1]
    return {"slope": float(res.params[1]), "ci_lower": float(lo), "ci_upper": float(hi),
            "p": float(res.pvalues[1]), "intercept": float(res.params[0])}


def ets_rolling(y):
    """Rolling one-step ETS (additive trend and seasonality) over the final ETS_TEST months."""
    preds, actual = [], []
    for t in range(ETS_TEST, 0, -1):
        fit = ExponentialSmoothing(y.iloc[:-t], trend="add", seasonal="add", seasonal_periods=PERIOD).fit(optimized=True)
        preds.append(float(fit.forecast(1).iloc[0]))
        actual.append(float(y.iloc[-t]))
    a, p = np.array(actual), np.array(preds)
    mae = float(np.mean(np.abs(a - p)))
    denom = float(np.mean(np.abs(y.values[PERIOD:] - y.values[:-PERIOD])))   # full-series seasonal naive
    smape = float(100 * np.mean(np.abs(a - p) / ((np.abs(a) + np.abs(p)) / 2)))
    return {"MAE": mae, "MASE": mae / denom, "sMAPE": smape, "pred": p.tolist(), "actual": a.tolist()}


def arima_check(y):
    """Small (S)ARIMA grid by AIC on the training span, then rolling one-step forecasts (stability check only)."""
    train = y.iloc[:-ETS_TEST]
    best = (None, None, np.inf)
    for p in (0, 1):
        for d in (0, 1):
            for q in (0, 1):
                for P in (0, 1):
                    for Q in (0, 1):
                        try:
                            r = SARIMAX(train, order=(p, d, q), seasonal_order=(P, 0, Q, PERIOD),
                                        enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
                            if r.aic < best[2]:
                                best = ((p, d, q), (P, 0, Q, PERIOD), r.aic)
                        except Exception:
                            pass
    preds = []
    for t in range(ETS_TEST, 0, -1):
        r = SARIMAX(y.iloc[:-t], order=best[0], seasonal_order=best[1],
                    enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
        preds.append(float(r.forecast(1).iloc[0]))
    obs_max = float(y.max())
    return {"order": str(best[0]), "seasonal_order": str(best[1]), "max_abs_forecast": float(np.max(np.abs(preds))),
            "observed_max": obs_max, "explosive": bool(np.max(np.abs(preds)) > 3 * obs_max)}


# ----------------------------------------------------------------------------
# One panel (full, or excluding the partial March 2025)
# ----------------------------------------------------------------------------
def analyse(m, with_arima=False):
    R = {"months": len(m), "span": f"{m.index.min():%Y-%m} to {m.index.max():%Y-%m}"}
    tot = m.sum()
    R["totals"] = {s: int(tot[s]) for s in SECTORS}
    R["share_pct"] = {s: float(100 * tot[s] / tot.sum()) for s in SECTORS}
    R["annual"] = {s: {int(k): int(v) for k, v in m[s].groupby(m.index.year).sum().items()} for s in SECTORS}
    R["zero_months"] = {s: [f"{d:%Y-%m}" for d in m.index[m[s] == 0]] for s in SECTORS}
    R["monthly_range"] = {s: [int(m[s].min()), int(m[s].max())] for s in SECTORS}

    q = quarterly(m)
    R["quarterly"] = {s: {str(k): int(v) for k, v in q[s].items()} for s in SECTORS}
    R["quarterly_range"] = {s: [int(q[s].min()), int(q[s].max())] for s in SECTORS}
    R["quarterly_range_complete_quarters"] = {s: [int(q[s].iloc[:-1].min()), int(q[s].iloc[:-1].max())] for s in SECTORS}
    R["quarterly_cv"] = {s: float(q[s].std(ddof=1) / q[s].mean()) for s in SECTORS}
    base = q[q.index.year == 2021].mean()
    gi = q / base * 100
    R["growth_index_base2021"] = {s: {str(k): float(v) for k, v in gi[s].items()} for s in SECTORS}

    R["stl"], R["moy"], rem, detr_c = {}, {}, {}, None
    for s in SECTORS:
        res = stl_fit(m[s])
        rem[s] = res.resid.values
        detr = res.observed - res.trend
        H, p = moy_test(detr)
        tr = res.trend
        R["stl"][s] = {"Fs": seasonal_strength(res),
                       "trend_first": float(tr.iloc[0]), "trend_last": float(tr.iloc[-1]),
                       "trend_max": float(tr.max()), "trend_max_at": f"{tr.idxmax():%Y-%m}",
                       "trend_min": float(tr.min()), "trend_min_at": f"{tr.idxmin():%Y-%m}",
                       "seasonal_range": [float(res.seasonal.min()), float(res.seasonal.max())],
                       "remainder_range": [float(res.resid.min()), float(res.resid.max())],
                       "remainder_max_at": f"{res.resid.idxmax():%Y-%m}"}
        R["moy"][s] = {"H": H, "p": p}
        if s == "Construction":
            detr_c = detr
    q2 = detr_c.index.month.isin([4, 5, 6])
    R["construction_posthoc"] = {
        "dunn_holm_min_p": dunn_holm(detr_c),
        "mannwhitney_AprJun_vs_rest_p": float(mannwhitneyu(detr_c[q2], detr_c[~q2], alternative="two-sided").pvalue),
        "detrended_month_means": {int(k): float(v) for k, v in detr_c.groupby(detr_c.index.month).mean().items()}}

    R["ccf"] = {c: ccf_bootstrap(rem["Construction"], rem[c]) for c in ("Digital", "Traditional")}
    R["ratios"] = {}
    for c in ("Digital", "Traditional"):
        r = q["Construction"] / q[c]
        R["ratios"][c] = {"series": {str(k): float(v) for k, v in r.items()}, "start": float(r.iloc[0]),
                          "end": float(r.iloc[-1]), "end_complete_quarter": float(r.iloc[-2]),
                          "min": float(r.min()), "max": float(r.max()), **ratio_trend(r)}
    R["ets"] = {s: ets_rolling(m[s]) for s in SECTORS}
    if with_arima:
        R["arima"] = {s: arima_check(m[s]) for s in SECTORS}
    R["_frames"] = {"m": m, "q": q, "gi": gi}
    return R


# ----------------------------------------------------------------------------
# Figures
# ----------------------------------------------------------------------------
def _style():
    plt.rcParams.update({"savefig.dpi": 600, "font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10,
                         "legend.fontsize": 9, "axes.spines.top": False, "axes.spines.right": False})


def _qx(idx):
    return idx.to_timestamp(how="start")


def _save(fig, out, name):
    fig.tight_layout()
    fig.savefig(os.path.join(out, name))
    plt.close(fig)


def figures(R, out):
    _style()
    m, q, gi = R["_frames"]["m"], R["_frames"]["q"], R["_frames"]["gi"]
    x = _qx(q.index)
    size = (7.0, 4.2)

    # Figure 2: quarterly postings (two panels: comparators and Construction)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=size, sharex=True, gridspec_kw={"height_ratios": [1.6, 1]})
    for s, ax in (("Digital", a1), ("Traditional", a1), ("Construction", a2)):
        ax.plot(x[:-1], q[s].iloc[:-1], color=COLOURS[s], marker="o", ms=3, label=s)
        ax.plot(x[-2:], q[s].iloc[-2:], color=COLOURS[s], ls=":", marker="o", ms=3, mfc="white")
    a1.set_ylabel("Postings per quarter"); a2.set_ylabel("Postings per quarter")
    a1.legend(loc="upper left", frameon=False); a2.legend(loc="upper left", frameon=False)
    a2.annotate("Q1 2025 partial\n(to 17 March)", (x[-1], q["Construction"].iloc[-1]), xytext=(-120, -8),
                textcoords="offset points", fontsize=8, arrowprops={"arrowstyle": "-", "lw": 0.6})
    _save(fig, out, "Figure02_quarterly_postings.png")

    # Figure 3: growth index (2021 average = 100)
    fig, ax = plt.subplots(figsize=size)
    for s in SECTORS:
        ax.plot(x[:-1], gi[s].iloc[:-1], color=COLOURS[s], marker="o", ms=3, label=s)
        ax.plot(x[-2:], gi[s].iloc[-2:], color=COLOURS[s], ls=":", marker="o", ms=3, mfc="white")
    ax.axhline(100, color="grey", lw=0.6)
    ax.set_ylabel("Index (2021 quarterly average = 100)")
    ax.legend(frameon=False, loc="upper left")
    ax.text(x[-1], ax.get_ylim()[1] * 0.97, "Q1 2025\npartial", fontsize=8, ha="right", va="top")
    _save(fig, out, "Figure03_growth_index.png")

    # Figures 4-6: STL decompositions
    for n, s in zip((4, 5, 6), SECTORS):
        res = stl_fit(m[s])
        fig, axes = plt.subplots(4, 1, figsize=(7.0, 4.67), sharex=True)
        for ax, comp, lab in zip(axes, (res.observed, res.trend, res.seasonal, res.resid),
                                 ("Observed", "Trend", "Seasonal", "Remainder")):
            if lab == "Remainder":
                ax.axhline(0, color="grey", lw=0.6)
                ax.plot(comp.index, comp.values, "o", ms=2.5, color=COLOURS[s])
            else:
                ax.plot(comp.index, comp.values, color=COLOURS[s], lw=1.2)
            ax.set_ylabel(lab, fontsize=8)
            ax.tick_params(labelsize=8)
        _save(fig, out, f"Figure0{n}_stl_{s.lower()}.png")

    # Figures 7-8: CCF on STL remainders (point estimates)
    for n, c in ((7, "Digital"), (8, "Traditional")):
        d = R["ccf"][c]
        fig, ax = plt.subplots(figsize=size)
        ax.vlines(d.lag, 0, d.r, color=COLOURS["Construction"])
        ax.plot(d.lag, d.r, "o", color=COLOURS["Construction"])
        ax.axhline(0, color="grey", lw=0.6)
        ax.set_xticks(d.lag); ax.set_xlabel("Lag (months; positive = Construction leads)"); ax.set_ylabel("Correlation")
        ax.set_ylim(-0.6, 0.8)
        _save(fig, out, f"Figure0{n}_ccf_construction_{c.lower()}.png")

    # Figures 9-10: ratios with linear trend
    for n, c in ((9, "Digital"), (10, "Traditional")):
        rr = R["ratios"][c]
        r = q["Construction"] / q[c]
        fig, ax = plt.subplots(figsize=size)
        ax.plot(x[:-1], r.iloc[:-1], color=COLOURS["Construction"], marker="o", ms=3, label=f"Construction/{c}")
        ax.plot(x[-2:], r.iloc[-2:], color=COLOURS["Construction"], ls=":", marker="o", ms=3, mfc="white")
        fit = rr["intercept"] + rr["slope"] * np.arange(len(r))
        ax.plot(x, fit, color="grey", ls="--", lw=1,
                label=f"Linear trend ({rr['slope']:+.5f} per quarter)")
        ax.set_ylabel("Ratio of quarterly postings"); ax.legend(frameon=False, loc="upper left")
        _save(fig, out, f"Figure{n:02d}_ratio_construction_{c.lower()}.png")

    # Figures 11-13: rolling one-step ETS forecasts
    for n, s in zip((11, 12, 13), SECTORS):
        e = R["ets"][s]
        tail = m[s].iloc[-24:]
        fig, ax = plt.subplots(figsize=size)
        ax.plot(tail.index, tail.values, color=COLOURS[s], label="Actual")
        ax.plot(m.index[-ETS_TEST:], e["pred"], "o--", color="black", ms=4, lw=1, label="ETS one-step forecast")
        ax.set_ylabel("Postings per month"); ax.legend(frameon=False, loc="best")
        ax.set_title(f"MAE {e['MAE']:.2f}; MASE {e['MASE']:.2f}; sMAPE {e['sMAPE']:.1f}%", fontsize=9, loc="right")
        _save(fig, out, f"Figure{n}_ets_{s.lower()}.png")

    # Figures 14-15: bootstrap CCF bands
    for n, c in ((14, "Digital"), (15, "Traditional")):
        d = R["ccf"][c]
        fig, ax = plt.subplots(figsize=size)
        ax.bar(d.lag, d.r, width=0.6, color=["#b03a2e" if z else "#95a5a6" for z in d.excludes_zero])
        ax.errorbar(d.lag, d.r, yerr=[d.r - d.ci_lower, d.ci_upper - d.r], fmt="none", ecolor="black", capsize=3, lw=0.8)
        ax.axhline(0, color="black", lw=0.6)
        ax.set_xticks(d.lag); ax.set_xlabel("Lag (months; positive = Construction leads)"); ax.set_ylabel("Correlation")
        ax.legend(handles=[Patch(color="#b03a2e", label="95% band excludes zero"),
                           Patch(color="#95a5a6", label="95% band includes zero")], frameon=False, loc="upper left")
        ax.set_ylim(-0.6, 0.8)
        _save(fig, out, f"Figure{n}_ccf_bootstrap_construction_{c.lower()}.png")


# ----------------------------------------------------------------------------
# Tables (published in supplementary/)
# ----------------------------------------------------------------------------
def tables(full, excl, info, out):
    T = {}
    T["analysis_parameters"] = pd.DataFrame([
        ("Data", f"Lightcast AI-related job postings, Australia and New Zealand, {info['first_date']} to {info['last_date']}"),
        ("Postings analysed", f"{info['postings_analysed']:,} (duplicate job identifiers removed: {info['duplicate_job_ids_removed']})"),
        ("Sector mapping", "ANZSIC 2006 subdivision of the employer's class code; see sector_mapping.csv"),
        ("Frequency and span", f"Monthly; {full['months']} observations per sector (March 2025 partial, to 17 March)"),
        ("Decomposition", "STL, additive, period = 12, robust = True"),
        ("Seasonal strength", "F_S = max(0, 1 - Var(R)/Var(S + R))"),
        ("Month-of-year test", f"Kruskal-Wallis on STL trend-removed values; circular moving-block bootstrap, block = {BLOCK}, B = {B}, seed = {SEED_MOY}"),
        ("Cross-correlation", f"STL remainders, lags +/-{MAX_LAG}; joint circular moving-block bootstrap, block = {BLOCK}, B = {B}, seed = {SEED_CCF}; 95% percentile bands"),
        ("Lag convention", "Positive lag = Construction leads the comparator: corr(Construction_t, comparator_t+L)"),
        ("Share ratios", f"Quarterly Construction/comparator ratios; OLS trend with Newey-West (HAC) 95% CI, {HAC_LAGS} lags"),
        ("Forecasting", f"ETS (additive trend and seasonality, period = 12); rolling one-step over final {ETS_TEST} months"),
        ("Accuracy metrics", "MAE; MASE (12-month seasonal-naive denominator from full series); sMAPE"),
        ("Sensitivity", "All analyses repeated on the 50-month panel ending February 2025"),
    ], columns=["Component", "Setting"])
    T["seasonality_summary"] = pd.DataFrame([{
        "Sector": s, "Months": full["months"], "STL_seasonal_strength": round(full["stl"][s]["Fs"], 3),
        "MoY_KW_H": round(full["moy"][s]["H"], 2), "MoY_bootstrap_p": round(full["moy"][s]["p"], 3)} for s in SECTORS])
    T["forecast_accuracy_ets"] = pd.DataFrame([{
        "Sector": s, "MAE": round(full["ets"][s]["MAE"], 2), "MASE": round(full["ets"][s]["MASE"], 2),
        "sMAPE_percent": round(full["ets"][s]["sMAPE"], 1)} for s in SECTORS])
    rows = []
    for c in ("Digital", "Traditional"):
        for _, r in full["ccf"][c].iterrows():
            rows.append({"Pair": f"Construction-{c}", "Lag": int(r.lag), "r": round(r.r, 4),
                         "CI_lower_95": round(r.ci_lower, 4), "CI_upper_95": round(r.ci_upper, 4),
                         "Band_excludes_zero": bool(r.excludes_zero)})
    T["ccf_bootstrap_stl_remainders"] = pd.DataFrame(rows)
    T["share_ratio_trends"] = pd.DataFrame([{
        "Ratio": f"Construction/{c}", "Panel": lab, "Start_Q1_2021": round(P["ratios"][c]["start"], 4),
        "End_Q1_2025_partial": round(P["ratios"][c]["end"], 4), "Q4_2024": round(P["ratios"][c]["end_complete_quarter"], 4),
        "Slope_per_quarter": round(P["ratios"][c]["slope"], 5), "HAC_CI_lower": round(P["ratios"][c]["ci_lower"], 5),
        "HAC_CI_upper": round(P["ratios"][c]["ci_upper"], 5), "HAC_p": round(P["ratios"][c]["p"], 4)}
        for c in ("Digital", "Traditional") for lab, P in (("51 months", full), ("50 months (excl. March 2025)", excl))])

    def pair(name, f, e, fmt="{:.3f}"):
        return {"Metric": name, "Full panel (51 months)": fmt.format(f), "Excluding March 2025 (50 months)": fmt.format(e)}

    sens = []
    for s in SECTORS:
        sens.append(pair(f"STL seasonal strength: {s}", full["stl"][s]["Fs"], excl["stl"][s]["Fs"]))
    for s in SECTORS:
        sens.append(pair(f"Month-of-year bootstrap p: {s}", full["moy"][s]["p"], excl["moy"][s]["p"]))
    for c in ("Digital", "Traditional"):
        for L in (-1, 0, 1):
            f = full["ccf"][c].set_index("lag").loc[L]; e = excl["ccf"][c].set_index("lag").loc[L]
            sens.append({"Metric": f"CCF Construction-{c}, lag {L:+d} [95% band]",
                         "Full panel (51 months)": f"{f.r:.3f} [{f.ci_lower:.2f}, {f.ci_upper:.2f}]",
                         "Excluding March 2025 (50 months)": f"{e.r:.3f} [{e.ci_lower:.2f}, {e.ci_upper:.2f}]"})
    for c in ("Digital", "Traditional"):
        sens.append(pair(f"Ratio Construction/{c}: slope per quarter", full["ratios"][c]["slope"], excl["ratios"][c]["slope"], "{:+.5f}"))
        sens.append(pair(f"Ratio Construction/{c}: final value", full["ratios"][c]["end"], excl["ratios"][c]["end"], "{:.4f}"))
    sens.append({"Metric": "Construction STL trend, first to last (postings per month)",
                 "Full panel (51 months)": f"{full['stl']['Construction']['trend_first']:.1f} to {full['stl']['Construction']['trend_last']:.1f}",
                 "Excluding March 2025 (50 months)": f"{excl['stl']['Construction']['trend_first']:.1f} to {excl['stl']['Construction']['trend_last']:.1f}"})
    for s in SECTORS:
        sens.append(pair(f"ETS one-step MASE: {s}", full["ets"][s]["MASE"], excl["ets"][s]["MASE"], "{:.2f}"))
    T["sensitivity_excluding_march_2025"] = pd.DataFrame(sens)

    os.makedirs(os.path.join(out, "tables"), exist_ok=True)
    for k, v in T.items():
        v.to_csv(os.path.join(out, "tables", f"{k}.csv"), index=False)


def _jsonable(R):
    out = {}
    for k, v in R.items():
        if k == "_frames":
            continue
        if k == "ccf":
            out[k] = {c: d.to_dict(orient="records") for c, d in v.items()}
        else:
            out[k] = v
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/all_industries_merged.xlsx")
    ap.add_argument("--out", default="outputs")
    a = ap.parse_args()
    os.makedirs(os.path.join(a.out, "figures"), exist_ok=True)
    raw, monthly, info = load(a.data)
    info["march_2025_counts"] = {s: int(monthly.loc["2025-03-01", s]) for s in SECTORS}
    full = analyse(monthly, with_arima=True)
    excl = analyse(monthly[monthly.index < "2025-03-01"])
    figures(full, os.path.join(a.out, "figures"))
    tables(full, excl, info, a.out)
    with open(os.path.join(a.out, "results.json"), "w") as f:
        json.dump({"data": info, "full": _jsonable(full), "excl_march_2025": _jsonable(excl)}, f, indent=1, default=float)
    print(f"Done. Outputs in {a.out}")


if __name__ == "__main__":
    main()
