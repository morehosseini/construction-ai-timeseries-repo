# Appendix F. Code and reproducibility

Design principles: Transparent, conservative analysis with parameter documentation in Table S1.

Key components to reproduce main results:
- STL decomposition: additive, period = 12, robust = True.
- Month-of-year test: Kruskal–Wallis on STL trend-removed series with moving-block bootstrap (block = 6, B = 1,500, seed = 7).
- Timing: CCFs on detrended, seasonally adjusted series; interpretation via bootstrap confidence bands.
- Forecasting: ETS (additive trend/seasonality, period = 12); unstable ARIMA excluded.
- Metrics: MAE, MASE (denominator from full series seasonal-naïve), sMAPE.

Availability: Data may be proprietary or licensed. To facilitate verification without redistribution, parameter tables (Table S1) and derived result tables (Table S2–S3) are provided. Where permissible, analysts can rerun the helper cell in the project notebook to regenerate seasonality and forecast summaries from local monthly data.