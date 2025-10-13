# Migration Guide: Updating Your Repository

This guide helps you update your existing repository with the improved structure and documentation.

## 📋 What's New in the Improved Version?

### Documentation Improvements
✅ **Comprehensive README** with badges, table of contents, and detailed instructions  
✅ **Enhanced DATA.md** with validation scripts and sample data generator  
✅ **CONTRIBUTING.md** for community guidelines  
✅ **CHANGELOG.md** for tracking versions  
✅ **CITATION.cff** with proper metadata  

### Project Structure
✅ **Organized directories** (data/, outputs/, supplementary/, notebooks/)  
✅ **Output subdirectories** (figures/, tables/, diagnostics/)  
✅ **.gitkeep files** to maintain directory structure  

### Configuration Files
✅ **environment.yml** for conda users  
✅ **Enhanced requirements.txt** with version specifications  
✅ **Comprehensive .gitignore**  
✅ **setup.sh script** for easy installation  

### Visual Improvements
✅ **Badges** (License, Python version, Code style)  
✅ **Emoji sections** for better readability  
✅ **Code examples** throughout documentation  

## 🔄 Migration Options

### Option 1: Fresh Start (Recommended)

If you want to completely restructure:

```bash
# 1. Backup your current repository
cd /path/to/current/repo
git add .
git commit -m "Backup before migration"
git tag v0.9-old

# 2. Download/clone the improved version
cd /path/to/
git clone https://github.com/morehosseini/construction-ai-timeseries-repo-improved.git new-repo
cd new-repo

# 3. Copy your notebook if you made changes
cp /path/to/old/repo/notebook.ipynb notebooks/

# 4. Copy your supplementary materials
cp -r /path/to/old/repo/supplementary/* supplementary/

# 5. Review and customize
# - Update CITATION.cff with your ORCID and paper details
# - Review README.md for any specific changes
# - Update contact information

# 6. Push to your repository
git remote set-url origin https://github.com/yourusername/yourrepo.git
git push -u origin main
```

### Option 2: Incremental Update

If you want to keep your git history:

```bash
cd /path/to/your/repo

# 1. Create a new branch
git checkout -b improved-structure

# 2. Copy new files one by one
# Download files from improved version and add them

# 3. Reorganize structure
mkdir -p notebooks data outputs/{figures,tables,diagnostics} supplementary
mv your_notebook.ipynb notebooks/
# ... move other files

# 4. Update documentation
# Replace README.md, add new MD files

# 5. Test the new structure
jupyter notebook notebooks/your_notebook.ipynb

# 6. Commit and merge
git add .
git commit -m "Restructure repository with improved documentation"
git checkout main
git merge improved-structure
git push
```

## 📝 Checklist for Migration

### Essential Updates
- [ ] Replace README.md with comprehensive version
- [ ] Add CONTRIBUTING.md
- [ ] Add or update CITATION.cff with your details
- [ ] Update .gitignore
- [ ] Add environment.yml
- [ ] Update requirements.txt with versions
- [ ] Create organized directory structure
- [ ] Add .gitkeep files for empty directories

### Documentation Updates
- [ ] Update DATA.md with detailed specifications
- [ ] Add CHANGELOG.md
- [ ] Review and update supplementary materials
- [ ] Add code examples in documentation

### Configuration
- [ ] Add setup.sh script
- [ ] Update contact information in all files
- [ ] Add ORCID to CITATION.cff
- [ ] Update repository URLs

### Optional Enhancements
- [ ] Add badges to README
- [ ] Create GitHub Actions for CI/CD
- [ ] Add issue templates
- [ ] Create pull request template
- [ ] Add code of conduct
- [ ] Setup GitHub Pages for documentation

## 🔍 Key Files to Update

### 1. CITATION.cff
```yaml
# Update these fields:
authors:
  - family-names: Hosseini
    given-names: M. Reza
    orcid: "https://orcid.org/YOUR-ORCID-HERE"  # ← Add your ORCID
    
# When paper is published, update:
preferred-citation:
  doi: "10.xxxx/xxxxx"  # ← Add DOI
  journal: "Journal Name"  # ← Add journal
  volume: "XX"
  year: 2025
```

### 2. README.md
```markdown
# Update contact section with your links
- 🔗 GitHub: [@yourusername](https://github.com/yourusername)
- 🌐 Website: [yourunipage.edu](https://yourunipage.edu)
- 📊 ResearchGate: [Your Profile](https://researchgate.net/profile/yourprofile)
```

### 3. Environment Files
Check that all package versions work with your code:
```bash
# Test environment
conda env create -f environment.yml
conda activate construction-timeseries
python -c "import pandas, numpy, scipy, statsmodels, matplotlib"
```

## 🧪 Testing After Migration

### 1. Environment Setup
```bash
# Test conda setup
conda env create -f environment.yml
conda activate construction-timeseries

# Or test pip setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Directory Structure
```bash
# Verify structure
tree -L 2
# Should show organized directories
```

### 3. Notebook Execution
```bash
# Test notebook runs
cd notebooks
jupyter nbconvert --to notebook --execute *.ipynb
```

### 4. Documentation
```bash
# Check all markdown files render properly
# View on GitHub or use a markdown preview tool
```

## 🚀 Publishing the Updated Repository

### Update GitHub Repository

```bash
# Make sure all changes are committed
git add .
git commit -m "Major update: Restructure repository with comprehensive documentation"

# Tag the new version
git tag -a v1.0.0 -m "Version 1.0.0 - Improved structure and documentation"

# Push everything
git push origin main
git push --tags
```

### Update Repository Settings

On GitHub:
1. **Description**: Add concise description
2. **Topics**: Add relevant tags
   - `time-series-analysis`
   - `construction-industry`
   - `artificial-intelligence`
   - `reproducible-research`
   - `job-market-analysis`
   - `python`
   - `jupyter-notebook`
   
3. **About section**: Add website and key info
4. **README badges**: Verify they display correctly
5. **Social preview**: Upload a preview image

### Create GitHub Release

1. Go to Releases → Create a new release
2. Tag: `v1.0.0`
3. Title: `Version 1.0.0 - Major Update`
4. Description:
   ```markdown
   ## 🎉 Major Repository Restructuring
   
   This release includes:
   - ✅ Comprehensive documentation
   - ✅ Organized directory structure
   - ✅ Enhanced installation process
   - ✅ Publication-ready repository
   
   See [CHANGELOG.md](CHANGELOG.md) for details.
   ```

## 📊 Before/After Comparison

### Old Structure
```
repo/
├── README.md (minimal)
├── requirements.txt (basic)
├── notebook.ipynb (nested folders)
└── supplementary/ (nested)
```

### New Structure
```
repo/
├── README.md (comprehensive)
├── CONTRIBUTING.md
├── CITATION.cff
├── CHANGELOG.md
├── DATA.md
├── LICENSE
├── .gitignore (detailed)
├── setup.sh
├── requirements.txt (versioned)
├── environment.yml
├── notebooks/
│   └── AI_Job_Postings_Construction_TimeSeries.ipynb
├── data/ (with .gitkeep)
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── diagnostics/
└── supplementary/
    ├── Appendix_C_Bootstrap_Settings.md
    ├── Appendix_D_ARIMA_Diagnostics_Exclusion.md
    ├── Appendix_E_Data_Cleaning_and_Aggregation.md
    ├── Appendix_F_Code_and_Reproducibility.md
    └── README_Supplement.txt
```

## 💡 Tips

1. **Take it step by step**: Don't try to change everything at once
2. **Keep backups**: Use git tags before major changes
3. **Test frequently**: Make sure nothing breaks
4. **Ask for help**: Open an issue if you need assistance
5. **Customize**: Adapt the structure to your specific needs

## 🐛 Common Issues

### Issue: Import errors after migration
**Solution**: Verify all paths in notebook are updated for new structure

### Issue: Git ignoring output files
**Solution**: Check .gitignore - outputs are ignored by default (optional)

### Issue: Setup script doesn't run
**Solution**: Make it executable: `chmod +x setup.sh`

## 📧 Need Help?

If you encounter issues during migration:
- Open an issue on GitHub
- Email: reza.hosseini@unimelb.edu.au
- Check the FAQ in README.md

---

**Good luck with your migration!** 🚀
