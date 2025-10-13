# Appendix D. ARIMA diagnostics and exclusion rationale (Digital)

Automatic ARIMA selection for the Digital series produced numerically unstable behaviour (explosive forecasts and non-invertible roots). To avoid misleading cross-model comparisons, ARIMA results for Digital were excluded from the main accuracy table and figures; stable ETS results were retained.

Observed symptoms of instability:
- Explosive forecast magnitudes far beyond observed scale.
- Residual autocorrelation inconsistent with whiteness.
- Root diagnostics indicating stationarity/invertibility violations (details available on request).

Policy for exclusion: Models that violated basic stability checks or produced implausible forecast scales were moved to the supplement and not used in headline comparisons. This aligns with the conservative design principle for sparse series.