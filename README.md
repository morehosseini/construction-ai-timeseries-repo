# Construction AI Job Postings: Time-Series Analysis

Code and supplementary materials for the article *Beyond the Laggard Myth: Time-Series Analysis of AI Job Market Dynamics in Construction* (Smart and Sustainable Built Environment).

The study compares monthly AI-related job postings in Construction with two comparator groups, Digital and Traditional industries, in Australia and New Zealand from January 2021 to 17 March 2025. It uses STL decomposition, month-of-year seasonality tests with moving-block bootstrap p-values, cross-correlations on STL remainders with bootstrap confidence bands, share-ratio trends with Newey–West confidence intervals, and rolling one-step ETS forecasts. Every analysis is repeated without the partial final month (March 2025).

## Reproducing the paper

One script regenerates every figure, table and statistic reported in the paper:

```bash
pip install -r requirements.txt
python analysis/reproduce_paper.py --data data/all_industries_merged.xlsx --out outputs
```

Outputs:

| Path | Contents |
|---|---|
| `outputs/figures/` | Figures 2–15 (600 dpi PNG). Figure 1 is a conceptual diagram. |
| `outputs/tables/` | The tables published in `supplementary/` |
| `outputs/results.json` | Every number quoted in the paper, for the full 51-month panel and the 50-month sensitivity panel |

A full run takes about two minutes on a laptop. The bootstrap seeds are fixed, so results are identical between runs with the same package versions.

## Data

The input is a licensed Lightcast extract of AI-related job postings and is not included in this repository. [DATA.md](DATA.md) describes the required columns and how to obtain equivalent data.

## Sector definitions

Each posting is assigned by the ANZSIC 2006 class code of the advertising employer, as coded by Lightcast.

| Group | ANZSIC 2006 subdivisions |
|---|---|
| Construction | 30–32 (Division E: building construction; heavy and civil engineering construction; construction services) |
| Digital | 58–60 (telecommunications, internet and data processing, information services), 62–63 (finance; insurance and superannuation funds), 69–70 (professional, scientific and technical services, including computer system design), 72 (administrative services) |
| Traditional | All other subdivisions |

The complete map is in [`supplementary/sector_mapping.csv`](supplementary/sector_mapping.csv). The paper (Section 5.3) discusses the breadth of the Digital grouping.

## Repository layout

```
analysis/reproduce_paper.py   Complete analysis pipeline
supplementary/                Supplementary tables and methods notes cited in the paper
data/                         Place the licensed extract here (not tracked)
outputs/                      Generated figures, tables and results (not tracked)
```

[`supplementary/README.md`](supplementary/README.md) lists each supplementary file against the section of the paper it supports.

## Version note

Version 2.0.0 corrects the Construction definition to ANZSIC subdivisions 30–32. Versions before 2.0.0 used class codes 3000–3999, which also included Wholesale Trade (subdivisions 33–38) and Motor Vehicle and Parts Retailing (39). See [CHANGELOG.md](CHANGELOG.md).

## Licence

Code and supplementary materials are released under the MIT Licence ([LICENSE](LICENSE)). The Lightcast data are subject to Lightcast's own licence terms.

## Citation

Please cite the associated article: *Beyond the Laggard Myth: Time-Series Analysis of AI Job Market Dynamics in Construction*, Smart and Sustainable Built Environment, 2026. The DOI will be added on publication.
