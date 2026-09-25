# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-09-25

### Fixed
- **Construction definition.** Construction is now ANZSIC 2006 subdivisions 30–32 (Division E). Earlier versions classed codes 3000–3999 as Construction, which also included Wholesale Trade (subdivisions 33–38) and Motor Vehicle and Parts Retailing (39); 707 of the 1,007 postings previously analysed as Construction came from those industries. They are now in Traditional. All results change accordingly; see the revised paper.
- Three repeated job identifiers are now removed before counting, as the paper describes.
- Newey–West (HAC) confidence intervals for the share-ratio trends are now computed (previously only the OLS slope was fitted).

### Changed
- One script, `analysis/reproduce_paper.py`, replaces the previous notebook and reproduces every figure, table and statistic in the paper, including the sensitivity analysis excluding March 2025, the month-of-year post-hoc checks and the ARIMA stability check.
- Growth indices use each sector's 2021 quarterly average as the base, because the Construction series had only four postings in Q1 2021.
- Supplementary materials are reorganised under descriptive names, indexed by paper section in `supplementary/README.md`, with a full ANZSIC `sector_mapping.csv` and consolidated `methods_notes.md`.

### Removed
- The exploratory notebook, citation metadata, contributor and migration guides, and setup script. The paper no longer cites supplementary items by table or appendix number.

## [1.1.0] - 2026-09-17

### Added
- Supplementary Tables S1–S3 (Analysis Parameters, Seasonality Summary, Forecast Metrics) tracked in repository.
- Supplementary Table S4 (`Table_S4_Bootstrap_CCF_STL_Remainders.csv`) containing bootstrap cross-correlation results on STL remainders (B = 1,500).
- Dedicated Step 3.4 & 4.6 analysis cell in Jupyter notebook reproducing Table 09 and Figures 14–15.

### Changed
- Updated bootstrap replication count to B = 1,500 across all inference cells.
- Reconciled cross-correlation lag-sign convention across all functions and docstrings (+lag indicates Construction leads comparator sector: corr(x_t, y_{t+L})), matching manuscript Figures 7–8 and Table S4.
- Updated `supplementary/Appendix_C_Bootstrap_Settings.md` with exact STL remainder confidence bands.
- De-anonymised `CITATION.cff` with full author list, ORCIDs, and accepted SASBE article metadata.

### Fixed
- Repaired sanitisation placeholder artefacts across notebook cells (date parsing in cell 9, Excel serial epoch in cells 3 and 11, ANZSIC code ranges in comments).

## [1.0.0] - 2025-10-13

### Added
- Initial release of reproducible research repository
- STL decomposition analysis for three sectors
- Moving-block bootstrap inference for month-of-year effects
- ETS forecasting with automatic model selection
- Cross-correlation analysis between sectors
- Comprehensive documentation (README, DATA.md, CONTRIBUTING.md)
- Jupyter notebook with full analysis pipeline
- Supplementary methodological appendices
- MIT License
- Citation file (CITATION.cff)
- Environment configuration (environment.yml, requirements.txt)
- Directory structure for organized outputs

### Documentation
- Detailed README with installation instructions
- Data specification guide
- Contributing guidelines
- Code of conduct (implicit in CONTRIBUTING.md)
- Methodological supplements

### Features
- Reproducible analysis with fixed random seeds
- Automatic generation of publication-ready tables and figures
- Data validation utilities
- Sample data generator for testing
- Comprehensive error handling and logging

---

## Version History

- **1.0.0** (2025-10-13): Initial public release
