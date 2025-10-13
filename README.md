# Construction AI Job Postings: Time-Series Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Reproducible research repository** for analyzing AI-related job posting dynamics across Construction, Digital, and Traditional sectors using advanced time-series methods.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Data Requirements](#data-requirements)
- [Methodology](#methodology)
- [Results & Outputs](#results--outputs)
- [Citation](#citation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🔍 Overview

This repository provides a complete, reproducible analysis pipeline for studying temporal patterns in AI-related job postings across three industry sectors. The analysis employs state-of-the-art time-series techniques including:

- **STL Decomposition** (Seasonal-Trend decomposition using Loess)
- **Exponential Smoothing (ETS)** for forecasting
- **ARIMA Modeling** with diagnostic testing
- **Moving-Block Bootstrap** for robust inference
- **Cross-Correlation Function (CCF)** analysis
- **Seasonal Strength** quantification

**Note:** This repository contains code and methodology only. Raw data are not included due to privacy/licensing restrictions. Users should provide their own monthly aggregate data following the format specified in [DATA.md](DATA.md).

## ✨ Features

- 📊 **Comprehensive Analysis Pipeline**: End-to-end workflow from data loading to publication-ready visualizations
- 🔄 **Reproducible Research**: All random seeds fixed; bootstrap parameters documented
- 📈 **Advanced Time-Series Methods**: STL, ETS, ARIMA with full diagnostics
- 🧪 **Robust Statistical Testing**: Moving-block bootstrap preserving temporal dependence
- 📑 **Publication-Ready Outputs**: Automated generation of tables and figures
- 🐍 **Clean Code**: Well-documented, modular Jupyter notebook
- 📚 **Supplementary Materials**: Detailed methodological appendices included

## 📁 Repository Structure

```
construction-ai-timeseries-repo/
│
├── notebooks/
│   └── AI_Job_Postings_Construction_TimeSeries.ipynb  # Main analysis notebook
│
├── supplementary/
│   ├── Appendix_C_Bootstrap_Settings.md                # Bootstrap methodology
│   ├── Appendix_D_ARIMA_Diagnostics_Exclusion.md       # Model selection criteria
│   ├── Appendix_E_Data_Cleaning_and_Aggregation.md     # Preprocessing details
│   ├── Appendix_F_Code_and_Reproducibility.md          # Reproducibility notes
│   └── README_Supplement.txt                            # Supplementary overview
│
├── data/                                               # (gitignored) Place your data here
│   └── .gitkeep
│
├── outputs/                                            # Generated results
│   ├── figures/                                        # Plots and visualizations
│   ├── tables/                                         # CSV outputs for paper
│   └── diagnostics/                                    # Model diagnostic plots
│
├── requirements.txt                                    # Python dependencies
├── environment.yml                                     # Conda environment file
├── DATA.md                                             # Data format specification
├── CITATION.cff                                        # Citation metadata
├── LICENSE                                             # MIT License
├── .gitignore                                          # Git ignore rules
├── CONTRIBUTING.md                                     # Contribution guidelines
└── README.md                                           # This file
```

## 🔧 Installation

### Option 1: pip (recommended for simple setups)

```bash
# Clone the repository
git clone https://github.com/morehosseini/construction-ai-timeseries-repo.git
cd construction-ai-timeseries-repo

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Conda (recommended for reproducibility)

```bash
# Clone the repository
git clone https://github.com/morehosseini/construction-ai-timeseries-repo.git
cd construction-ai-timeseries-repo

# Create conda environment
conda env create -f environment.yml
conda activate construction-timeseries

# Verify installation
python -c "import pandas, numpy, scipy, statsmodels, matplotlib; print('All packages imported successfully')"
```

### Option 3: Google Colab

1. Open the notebook directly in Google Colab: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/morehosseini/construction-ai-timeseries-repo/blob/main/notebooks/AI_Job_Postings_Construction_TimeSeries.ipynb)
2. Run the first cell to install dependencies
3. Upload your data file when prompted

## 🚀 Quick Start

1. **Prepare your data** following the format specified in [DATA.md](DATA.md)

2. **Launch Jupyter**:
   ```bash
   jupyter notebook notebooks/AI_Job_Postings_Construction_TimeSeries.ipynb
   ```

3. **Configure data path** in the first code cell:
   ```python
   SOURCE_XLSX = 'data/your_data.xlsx'  # Update this path
   ```

4. **Run all cells** to:
   - Load and validate data
   - Perform STL decomposition
   - Calculate seasonal strength metrics
   - Run bootstrap hypothesis tests
   - Generate ETS forecasts
   - Create publication-ready figures and tables

5. **Check outputs** in the `outputs/` directory

## 📊 Data Requirements

This analysis requires monthly aggregate data in one of two formats:

### Format 1: Tidy (Long) Format
```
date,sector,postings
2020-01-01,Construction,145
2020-01-01,Digital,892
2020-01-01,Traditional,456
2020-02-01,Construction,152
...
```

### Format 2: Wide (Pivot) Format
```
date,Construction,Digital,Traditional
2020-01-01,145,892,456
2020-02-01,152,901,468
...
```

**Requirements:**
- Date column: ISO format (YYYY-MM-DD or YYYY-MM)
- Sectors: Exactly three sectors named `Construction`, `Digital`, `Traditional`
- Postings: Non-negative integer counts
- Minimum 24 months of data recommended for reliable STL decomposition

See [DATA.md](DATA.md) for detailed specifications.

## 🔬 Methodology

### Time-Series Decomposition
- **STL** (Seasonal-Trend decomposition using Loess) with robust fitting
- Seasonal period: 12 months
- Trend window: 25 months (flexible)
- Seasonal strength: $1 - \frac{\text{Var}(\text{remainder})}{\text{Var}(\text{detrended})}$

### Statistical Testing
- **Month-of-Year Effect**: Kruskal-Wallis test on detrended series
- **Bootstrap Inference**: Moving-block bootstrap (block length = 6 months, B = 1,500)
- **Random Seed**: 7 (for reproducibility)

### Forecasting
- **Model**: Exponential Smoothing (ETS) with automatic model selection
- **Evaluation**: One-step-ahead forecasts
- **Metrics**: MAE, MASE, sMAPE

### Cross-Sector Analysis
- Cross-correlation function (CCF) with bootstrap confidence bands
- Lead-lag relationship assessment (±12 month window)

For detailed methodology, see supplementary appendices in `supplementary/`.

## 📈 Results & Outputs

The notebook automatically generates:

### Tables (CSV format in `outputs/tables/`)
- `Table_S1_Descriptive_Statistics.csv`: Monthly counts and summary stats
- `Table_S2_Seasonal_Strength.csv`: STL-derived seasonal metrics per sector
- `Table_S3_Forecast_Performance.csv`: ETS forecast accuracy (MAE/MASE/sMAPE)

### Figures (PNG/PDF in `outputs/figures/`)
- `Fig1_Time_Series_Overview.png`: Raw monthly counts by sector
- `Fig2_STL_Decomposition.png`: Trend, seasonal, and remainder components
- `Fig3_Seasonal_Patterns.png`: Month-of-year aggregated patterns
- `Fig4_CCF_Analysis.png`: Cross-correlation between sectors
- `Fig5_Forecast_Validation.png`: One-step-ahead predictions vs. actuals

### Diagnostics (in `outputs/diagnostics/`)
- `Bootstrap_P_Values.txt`: MoY test results
- `ETS_Model_Selection.txt`: Chosen ETS model per sector
- `Residual_Diagnostics.png`: ACF/PACF of forecast residuals

## 📚 Citation

If you use this repository or methodology in your research, please cite:

```bibtex
@misc{hosseini2025construction,
  title={Construction AI Job Postings: Time-Series Analysis},
  author={Hosseini, M. Reza},
  year={2025},
  publisher={GitHub},
  url={https://github.com/morehosseini/construction-ai-timeseries-repo},
  note={Reproducible research repository}
}
```

**Associated Paper**: [Citation details will be added upon publication]

For BibTeX and other citation formats, see [CITATION.cff](CITATION.cff).

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas for contribution:**
- Additional time-series models (SARIMA, Prophet, Neural Forecasting)
- Enhanced visualization options
- Alternative bootstrap schemes
- Extended documentation and tutorials
- Bug fixes and performance improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Contact

**Dr. M. Reza Hosseini**  
Senior Lecturer in Construction Technology  
Faculty of Architecture, Building and Planning  
The University of Melbourne

- 📧 Email: reza.hosseini@unimelb.edu.au
- 📱 Phone: +61 404 724 858
- 🔗 GitHub: [@morehosseini](https://github.com/morehosseini)

For questions about the methodology, data requirements, or collaboration opportunities, please open an issue or contact directly.

---

**Keywords**: Construction Industry, Artificial Intelligence, Job Market Analysis, Time Series, STL Decomposition, Forecasting, Labor Market Trends, Digital Transformation

**Last Updated**: October 2025
