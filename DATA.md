# Data Specification

This repository **does not include raw data** due to privacy and licensing restrictions. Users must provide their own monthly aggregated job posting data in one of the formats specified below.

## 📊 Data Formats

### Format 1: Tidy (Long) Format ✅ Recommended

**File**: CSV or Excel with columns: `date`, `sector`, `postings`

**Example**:
```csv
date,sector,postings
2020-01-01,Construction,145
2020-01-01,Digital,892
2020-01-01,Traditional,456
2020-02-01,Construction,152
2020-02-01,Digital,905
2020-02-01,Traditional,462
2020-03-01,Construction,160
2020-03-01,Digital,920
2020-03-01,Traditional,455
```

**Column Specifications**:
- `date`: ISO 8601 format (YYYY-MM-DD or YYYY-MM)
  - Must be the first day of each month or just YYYY-MM
  - No missing months in the time series
  - Consistent frequency (monthly)
  
- `sector`: Categorical variable (string)
  - Exactly three sectors required: `Construction`, `Digital`, `Traditional`
  - Case-sensitive (use exact spelling)
  - No missing or null values
  
- `postings`: Non-negative integer
  - Count of AI-related job postings for that month/sector
  - Must be ≥ 0 (zero counts are valid)
  - No missing values

### Format 2: Wide (Pivot) Format

**File**: CSV or Excel with date index and sector columns

**Example**:
```csv
date,Construction,Digital,Traditional
2020-01-01,145,892,456
2020-02-01,152,905,462
2020-03-01,160,920,455
2020-04-01,158,935,450
```

**Column Specifications**:
- `date`: Same requirements as Format 1
- `Construction`, `Digital`, `Traditional`: Sector-specific posting counts (integers ≥ 0)

## ⚠️ Data Requirements

### Minimum Requirements
- **Time span**: At least 24 months of data (recommended: 36+ months)
  - Required for robust STL decomposition (needs ≥2 seasonal cycles)
  - Longer series improve bootstrap inference and forecasting
  
- **Completeness**: No missing months
  - Months with zero postings should be included as 0, not omitted
  - All sectors must have the same date range
  
- **Consistency**: Same aggregation level across sectors
  - All counts should represent the same geographic scope
  - Same job posting source/platform

### Recommended Data Characteristics
- **36-60 months**: Optimal for seasonal pattern detection
- **Recent data**: Include most recent months for relevant trends
- **Quality control**: Remove duplicates, verify counts are reasonable

## 🔧 Data Preparation

### If You Have Raw Job Postings

If you have individual job posting records (not aggregated), you'll need to:

1. **Filter for AI-related keywords** (examples):
   - "artificial intelligence", "machine learning", "deep learning"
   - "AI", "ML", "neural network", "computer vision", "NLP"
   - "data science", "predictive analytics"

2. **Classify by sector**:
   - **Construction**: Job postings from construction firms, contractors, builders
   - **Digital**: Job postings from tech companies, software firms, digital agencies
   - **Traditional**: Job postings from other established industries (manufacturing, retail, finance, etc.)

3. **Aggregate to monthly level**:
   ```python
   # Example using pandas
   import pandas as pd
   
   # Assuming 'df' has columns: posting_date, sector, other_fields
   monthly_counts = df.groupby([
       pd.Grouper(key='posting_date', freq='MS'),  # Month start
       'sector'
   ]).size().reset_index(name='postings')
   
   # Rename for consistency
   monthly_counts.rename(columns={'posting_date': 'date'}, inplace=True)
   ```

4. **Ensure complete time series** (fill missing months with zeros):
   ```python
   # Create complete date range
   date_range = pd.date_range(
       start=monthly_counts['date'].min(),
       end=monthly_counts['date'].max(),
       freq='MS'
   )
   sectors = ['Construction', 'Digital', 'Traditional']
   
   # Create complete index
   complete_index = pd.MultiIndex.from_product(
       [date_range, sectors],
       names=['date', 'sector']
   )
   
   # Reindex and fill missing with 0
   complete_data = (
       monthly_counts
       .set_index(['date', 'sector'])
       .reindex(complete_index, fill_value=0)
       .reset_index()
   )
   ```

5. **Save in required format**:
   ```python
   complete_data.to_excel('data/job_postings_monthly.xlsx', index=False)
   # or
   complete_data.to_csv('data/job_postings_monthly.csv', index=False)
   ```

## 📁 Where to Place Your Data

```
construction-ai-timeseries-repo/
├── data/                           # Create this folder
│   ├── job_postings_monthly.xlsx   # Your data file
│   ├── data_dictionary.txt         # Optional: Document your data
│   └── .gitkeep                    # Keeps folder in git
```

The `data/` folder is gitignored, so your data files won't be tracked or pushed to GitHub.

## 🔒 Data Privacy

If you're using proprietary or sensitive data:

1. **Never commit data files** to Git (they're gitignored by default)
2. **Anonymize if necessary**: Remove company names, specific locations
3. **Aggregate appropriately**: Monthly aggregates are less sensitive than individual postings
4. **Check licensing**: Ensure you have rights to use the data for research
5. **Consider synthetic data**: For code testing, generate fake data with similar statistical properties

## 📝 Sample Data for Testing

We provide a sample data generator in the notebook. To create synthetic data for testing:

```python
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate 48 months of synthetic data
dates = pd.date_range('2020-01-01', periods=48, freq='MS')
sectors = ['Construction', 'Digital', 'Traditional']

data = []
for date in dates:
    # Simple seasonal pattern + trend + noise
    month = date.month
    time_idx = (date.year - 2020) * 12 + date.month
    
    for sector in sectors:
        if sector == 'Construction':
            base = 100 + time_idx * 2  # Slow growth
            seasonal = 20 * np.sin(2 * np.pi * month / 12)
        elif sector == 'Digital':
            base = 800 + time_idx * 5  # Fast growth
            seasonal = 50 * np.sin(2 * np.pi * month / 12)
        else:  # Traditional
            base = 400 + time_idx * 1  # Minimal growth
            seasonal = 30 * np.sin(2 * np.pi * month / 12)
        
        noise = np.random.normal(0, 10)
        postings = max(0, int(base + seasonal + noise))
        
        data.append({
            'date': date,
            'sector': sector,
            'postings': postings
        })

# Create DataFrame
sample_data = pd.DataFrame(data)

# Save
sample_data.to_csv('data/sample_data.csv', index=False)
print("Sample data created!")
```

## 🔍 Data Validation

Before running the analysis, validate your data:

```python
import pandas as pd

# Load data
df = pd.read_excel('data/your_data.xlsx')  # or read_csv

# Check structure
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")

# Check for required columns
required_cols = ['date', 'sector', 'postings']
missing_cols = set(required_cols) - set(df.columns)
if missing_cols:
    print(f"\n❌ Missing required columns: {missing_cols}")
else:
    print("\n✅ All required columns present")

# Check sectors
unique_sectors = df['sector'].unique()
expected_sectors = {'Construction', 'Digital', 'Traditional'}
if set(unique_sectors) == expected_sectors:
    print(f"✅ All three sectors present: {unique_sectors}")
else:
    print(f"❌ Sector mismatch. Expected: {expected_sectors}, Got: {set(unique_sectors)}")

# Check for missing values
missing_vals = df.isnull().sum()
if missing_vals.sum() > 0:
    print(f"\n❌ Missing values:\n{missing_vals[missing_vals > 0]}")
else:
    print("\n✅ No missing values")

# Check date range
df['date'] = pd.to_datetime(df['date'])
print(f"\n📅 Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Number of months: {df['date'].nunique()}")

# Check for negative counts
if (df['postings'] < 0).any():
    print("\n❌ Negative posting counts found!")
else:
    print("✅ All posting counts are non-negative")
```

## 📧 Questions?

If you have questions about data formatting or preparation:
- Open an issue on GitHub
- Email: reza.hosseini@unimelb.edu.au
- See example data in the notebook
