# Methods notes

These notes give the settings behind each analysis in the paper and the reasons for them. Every setting is implemented in `analysis/reproduce_paper.py` and listed in `analysis_parameters.csv`.

## 1. Data preparation (paper Section 3.1)

1. Read the Lightcast extract (45,259 AI-related postings, 1 January 2021 to 17 March 2025). No record lacks a date or an ANZSIC code.
2. Remove repeated job identifiers, keeping the earliest record. Three postings are removed, all repeats on 1 January 2025 of advertisements first posted on 31 December 2024. This is in addition to the cross-board deduplication Lightcast applies at source. 45,256 postings remain.
3. Assign each posting to Construction, Digital or Traditional from the ANZSIC 2006 subdivision of the employer's class code (`sector_mapping.csv`). Every posting carries a valid class code, so none is excluded.
4. Count postings per calendar month and sector. All 51 months are present for every sector. Construction has one month with no postings (April 2021); this is a genuine zero and is kept as such. No value is interpolated, imputed or smoothed.
5. March 2025 is a partial month (to 17 March, about 55% of the month). It is kept unadjusted as the 51st observation, and every analysis is repeated without it (Section 7 below).

Quarterly series are the sums of the monthly counts. Q1 2025 is therefore partial and is marked as such in all quarterly figures.

## 2. Sector definitions and their limits (paper Sections 3.1 and 5.3)

- **Construction**: subdivisions 30–32 (Division E). The series captures AI hiring by construction firms, not the wider construction supply chain. It has 300 postings from fewer than 40 employers, and a handful of large contractors account for more than half of them.
- **Digital**: subdivisions 58–60, 62–63, 69–70 and 72. By postings, 58% come from professional, scientific and technical services including computer system design (69–70), 26% from finance and insurance (62–63), 9% from administrative services (72) and 7% from telecommunications, internet and data-processing and information services (58–60). The group represents data- and knowledge-intensive services generally. It includes engineering design and consulting firms (class 6923, 936 postings), so AI roles in construction-related design consultancies count as Digital.
- **Traditional**: all other subdivisions. The group is residual and heterogeneous. It includes wholesale and retail trade, manufacturing, mining, utilities, health, education, public administration and some digitally intensive industries such as software publishing (class 5420, 977 postings).

Versions of this repository before 2.0.0 classed codes 3000–3999 as Construction, which also took in Wholesale Trade (33–38) and Motor Vehicle and Parts Retailing (39). Those subdivisions are now in Traditional.

## 3. Decomposition and seasonality (paper Sections 3.2–3.3 and 4.2)

- **Decomposition**: additive STL, period = 12, robust fitting (statsmodels defaults for the seasonal and trend smoothers).
- **Seasonal strength**: F_S = max(0, 1 − Var(R)/Var(S + R)), where S is the seasonal and R the remainder component (sample variances). F_S is the share of detrended variation attributable to the seasonal component and ranges from 0 to 1. It is descriptive.
- **Month-of-year (MoY) test**: Kruskal–Wallis statistic H across the 12 calendar months, computed on STL trend-removed values (observed − trend). The p-value comes from a circular moving-block bootstrap of the month labels: blocks of 6 months, B = 1,500, seed = 7. It equals the proportion of bootstrap statistics at least as large as the observed H, with the +1 correction. Resampling in blocks preserves short-run dependence, so the p-values are more conservative than under an independence assumption.
- With about four observations per calendar month, the test has limited power. A non-significant result, as for Construction, indicates that no seasonality is detectable, not that none exists. Month-specific contrasts are not tested. The April–June comparison reported for Construction (Mann–Whitney U) is exploratory.

## 4. Cross-sector timing (paper Sections 3.4, 4.3 and 4.6)

- **Series**: STL remainders (detrended and seasonally adjusted), which removes common trend and seasonality before correlating.
- **Correlation**: Pearson correlation of Construction at time t with the comparator at t + L, for L = −6 to +6 months. A positive L means Construction leads.
- **Bands**: joint circular moving-block bootstrap of the paired remainders, with blocks of 6 months, B = 1,500 and seed = 123; 95% percentile bands.
- **Multiplicity**: 26 bands are examined (13 lags × 2 pairs). About one band would be expected to exclude zero by chance at the 95% level, so a single exclusion is interpreted cautiously.

## 5. Share-ratio trends (paper Sections 3.5 and 4.4)

- **Ratios**: quarterly Construction/Digital and Construction/Traditional posting ratios (17 quarters; Q1 2025 is partial).
- **Trend**: OLS of the ratio on a linear quarter index. A positive slope means convergence (Construction's share rising).
- **Inference**: Newey–West (HAC) standard errors with 2 lags, using the rule of thumb floor(4(T/100)^(2/9)) for T = 17. The reported intervals are 95% confidence intervals.

## 6. Forecasting (paper Sections 3.6 and 4.5)

- **Model**: ETS with additive trend and additive seasonality (period = 12), refitted at each step.
- **Design**: rolling one-step forecasts over the final 8 months of each series.
- **Metrics**: MAE; MASE, scaled by the mean absolute 12-month seasonal-naïve error over the full series (values below 1 mean ETS beats the seasonal-naïve benchmark); and sMAPE.
- **ARIMA**: a small seasonal ARIMA grid was also fitted, with p, d, q, P, Q ∈ {0, 1}, D = 0, selected by AIC on the training span. For the Digital series the selected model, ARIMA(1,1,1)(1,0,1)12, produced explosive one-step forecasts, orders of magnitude beyond the observed range. For a like-for-like comparison across sectors, ARIMA results are therefore not reported, and ETS is used for all three sectors. The script records the ARIMA check in `results.json`.

## 7. Sensitivity to the partial final month (paper Section 4.7)

Every analysis above is repeated on the 50-month panel ending February 2025 (`sensitivity_excluding_march_2025.csv`, and the `excl_march_2025` block of `results.json`). In the reduced panel:
- The seasonality, share-ratio and forecasting conclusions are unchanged.
- Which of the lag-0 and lag +1 cross-correlation bands exclude zero changes.
- No band at a negative lag excludes zero in either panel.

## 8. Software

The results were produced with Python 3.9, pandas 2.3, NumPy 2.0, SciPy 1.13, statsmodels 0.14.6 and Matplotlib 3.9. Bootstrap results depend on the random seeds listed above. Other package versions may change the third decimal place.
