# Data notes

The repository does **not** include raw postings. Provide monthly aggregates in one of two formats:

## Tidy format
Columns: `date, sector, postings`
- `date`: month in ISO format (e.g., 2022-03-01 or 2022-03)
- `sector`: one of `Construction`, `Digital`, `Traditional`
- `postings`: integer count per month/sector

## Wide pivot format
Index: monthly `date`
Columns: `Construction`, `Digital`, `Traditional`
Values: counts per month

Update the notebook variable `SOURCE_XLSX='path/to/your_data.xlsx'` or load your CSV accordingly.