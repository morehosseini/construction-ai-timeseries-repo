# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Neural forecasting methods (LSTM, Transformer)
- Interactive dashboard using Streamlit or Plotly Dash
- Automated report generation
- Additional bootstrap schemes
- Docker containerization
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
