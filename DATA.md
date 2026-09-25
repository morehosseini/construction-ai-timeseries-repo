# Data

The analysis uses a licensed extract of AI-related job postings from Lightcast (Labour Insight, Australia and New Zealand). Lightcast's licence does not allow the extract to be redistributed, so it is not part of this repository. Researchers with Lightcast access can obtain equivalent data, as described below.

## Extract used in the paper

| Item | Value |
|---|---|
| Source | Lightcast job postings, Australia and New Zealand |
| Period | 1 January 2021 to 17 March 2025 (March 2025 is a partial month) |
| Selection | Postings flagged as AI-related by Lightcast's skills taxonomy (at least one requested skill in the artificial-intelligence branch), with Lightcast's false-positive exclusions and cross-board deduplication applied |
| Records | 45,259 postings; 45,256 after removing three repeated job identifiers |

## File expected by the script

`analysis/reproduce_paper.py` reads one Excel file (default `data/all_industries_merged.xlsx`) with one row per posting. Only three columns are used:

| Column | Type | Use |
|---|---|---|
| `JobID` | text | Unique posting identifier; repeated identifiers are dropped (earliest kept) |
| `JobDate` | date | Advertisement date; aggregated to calendar months |
| `ANZSIC CODE` | integer | ANZSIC 2006 class code of the advertising employer, as coded by Lightcast. Classes 0100–0999 may appear without the leading zero (for example `142` for class 0142). |

Other columns in the extract (employer, title, location, ANZSCO and Lightcast occupation codes, advertisement text) are not used.

## Sector assignment

Postings are grouped by the two-digit ANZSIC 2006 subdivision of the class code. [`supplementary/sector_mapping.csv`](supplementary/sector_mapping.csv) lists every subdivision and its group:

- Construction: 30–32
- Digital: 58–60, 62–63, 69–70, 72
- Traditional: all others

Sector membership therefore depends on the industry code that Lightcast assigns to each employer. The construction series is small (300 postings over 51 months), so the coding of even a few employers can change it noticeably.

## Folder layout

```
data/
└── all_industries_merged.xlsx   # licensed extract (not tracked by git)
```

The `data/` folder is excluded by `.gitignore`.
