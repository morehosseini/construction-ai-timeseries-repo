# Appendix C. Bootstrap settings and inference notes (methods supplement)

Primary test: Month-of-year (12 categories) Kruskal–Wallis on STL trend-removed monthly series.

Bootstrap design: Moving-block bootstrap (MBB) to respect short-run dependence.
- Block length: 6 months (primary).
- Replications: 1,500.
- Random seed: 7.
- Label permutation: month labels resampled via MBB indices; test statistic recomputed per draw.

Rationale: The MBB preserves local autocorrelation typical of monthly posting counts, yielding more conservative p-values than i.i.d. resampling. We prioritise month-of-year inference; quarter-based tests are omitted in the main text to avoid mixing scales.

Sensitivity (optional to report):
- Analysts may replicate the MoY test with block lengths 3 and 9 months to confirm qualitative stability of conclusions.
- When sample sizes are short, differences across block lengths should be interpreted descriptively rather than as formal multiple-model evidence.

Reporting: Main-text p-values (Table 1) correspond to block length 6 and B = 1,500. Cross-correlations are computed on STL remainders, with 95% percentile bands from a circular moving-block bootstrap (block = 6 months, B = 1,500, seed = 123). The bands exclude zero at lag 0 for Construction–Digital, and at lags 0 and +1 for Construction–Traditional. All other lags include zero.