# Appendix E. Data provenance, cleaning, and aggregation (summary)

Provenance: Monthly job-posting counts for Construction, Digital, and Traditional sectors compiled over 51 months. Extraction date, taxonomy version, and filter definitions should be recorded in the project repository or data log.

Cleaning & preparation (summary):
1. Parse timestamps and aggregate to month start (MS).
2. Map industry/occupation codes to sector groupings (Construction; Digital; Traditional).
3. Filter and de-duplicate postings by unique job identifier where available.
4. Create monthly counts per sector; flag partial months where applicable.
5. Inspect for extreme outliers and missing months; apply minimal interpolation for isolated gaps.

Aggregation choices: National-level aggregation is used in the main analysis. Regional breakdowns are not reported and remain a candidate for future work.

Outputs: Tidy monthly series used for STL decomposition, MoY tests, CCFs, and rolling one-step forecasts.