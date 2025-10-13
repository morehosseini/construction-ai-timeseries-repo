# Construction AI Job Postings — Time-Series Analysis

This repository provides a **reproducible, sanitized** version of the analysis accompanying the paper on AI job-posting dynamics in Construction vs Digital/Traditional sectors. Data are **not included**; the notebook and scripts are designed to run on your own monthly aggregates.

## What’s here
- `notebooks/AI_Job_Postings_Construction_TimeSeries.ipynb` — sanitized Colab/Python notebook (outputs cleared; paths anonymized; no secrets).
- `supplementary/` — CSV tables and short method appendices for the paper (Table S1–S3; Appendices C–F).
- `requirements.txt` — minimal Python dependencies.
- `DATA.md` — notes on expected input structure.
- `.gitignore` — excludes data, secrets, and checkpoints.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# open the notebook in Jupyter or Colab and set SOURCE_XLSX='path/to/your_data.xlsx'
```

## Reproducing key outputs
The notebook contains a helper cell that:
- computes STL seasonal-strength and Month-of-Year bootstrap p-values,
- produces ETS-only one-step forecast metrics (MAE/MASE/sMAPE),
- saves CSVs consistent with the paper’s tables.

## Data policy
Raw postings are not distributed here. Provide your own monthly tidy file with columns `date, sector, postings` or a wide pivot with sector columns. See `DATA.md`.

## Citation
If you use this repository, please cite the associated paper. See `CITATION.cff`.