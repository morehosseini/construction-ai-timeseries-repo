# Contributing to Construction AI Time-Series Analysis

Thank you for your interest in contributing to this project! We welcome contributions from the research and development community.

## 🎯 Ways to Contribute

- **Bug Reports**: Found a bug? Open an issue with a clear description
- **Feature Requests**: Have an idea? Open an issue to discuss it
- **Code Contributions**: Submit a pull request with improvements
- **Documentation**: Help improve our docs, tutorials, or examples
- **Research Extensions**: Share alternative methods or analyses

## 🔄 Development Workflow

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/construction-ai-timeseries-repo.git
cd construction-ai-timeseries-repo
```

### 2. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b bugfix/issue-description
```

### 3. Set Up Environment

```bash
# Create and activate environment
conda env create -f environment.yml
conda activate construction-timeseries

# Or use venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Make Your Changes

- Write clear, documented code
- Add tests if applicable
- Update documentation
- Follow the code style (use `black` for Python)

### 5. Test Your Changes

```bash
# Format code
black .

# Run linting
flake8 .

# Test the notebook runs without errors
jupyter nbconvert --to notebook --execute notebooks/*.ipynb
```

### 6. Commit and Push

```bash
# Stage changes
git add .

# Commit with a descriptive message
git commit -m "Add: Brief description of your changes"

# Push to your fork
git push origin feature/your-feature-name
```

### 7. Submit a Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template with:
   - Description of changes
   - Related issue number (if applicable)
   - Testing performed
   - Any breaking changes

## 📝 Code Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use `black` for automatic formatting
- Add docstrings to functions and classes
- Keep functions focused and modular
- Use type hints where appropriate

Example:
```python
def calculate_seasonal_strength(
    series: pd.Series,
    seasonal_period: int = 12
) -> float:
    """
    Calculate seasonal strength using STL decomposition.
    
    Parameters
    ----------
    series : pd.Series
        Time series data with datetime index
    seasonal_period : int, default=12
        Number of observations per seasonal cycle
        
    Returns
    -------
    float
        Seasonal strength value between 0 and 1
    """
    # Implementation here
    pass
```

### Jupyter Notebooks

- Clear section headers using markdown
- One analysis step per cell (mostly)
- Include explanatory markdown cells
- Clear all outputs before committing
- Set random seeds for reproducibility

### Documentation

- Use clear, concise language
- Include code examples
- Add references to papers/methods
- Keep README updated with new features

## 🧪 Testing Guidelines

While this is primarily a research repository, please ensure:

- Code runs without errors
- Results are reproducible (check random seeds)
- Outputs match expected formats
- Documentation reflects code behavior

## 📋 Pull Request Checklist

Before submitting a PR, verify:

- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Notebook runs without errors
- [ ] Commits have clear messages
- [ ] PR description explains changes
- [ ] No merge conflicts with main branch

## 🐛 Reporting Bugs

When reporting bugs, include:

1. **Description**: Clear description of the bug
2. **Reproduction Steps**: Minimal code to reproduce
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: Python version, OS, package versions
6. **Screenshots**: If applicable

Example bug report:
```markdown
## Bug: STL decomposition fails with short time series

**Steps to reproduce:**
1. Load data with only 18 months
2. Run STL with seasonal_period=12
3. Error occurs: "Series too short for STL"

**Expected:** Graceful error message with minimum length requirement
**Actual:** Cryptic numpy error

**Environment:** Python 3.10, statsmodels 0.14.0, Ubuntu 22.04
```

## 💡 Feature Requests

When suggesting features:

1. **Use Case**: Explain why this feature is needed
2. **Proposed Solution**: How it could work
3. **Alternatives**: Other approaches considered
4. **Research Context**: Relevant papers or methods

## 🔬 Research Contributions

We especially welcome:

- **Alternative Methods**: SARIMA, Prophet, Neural forecasting, etc.
- **Statistical Tests**: Additional hypothesis tests or diagnostics
- **Visualization**: New plotting functions
- **Case Studies**: Applications to other domains
- **Benchmarking**: Comparative analyses

Please include:
- Methodology description
- References to papers/methods
- Example code or notebook
- Interpretation guidelines

## 📧 Questions?

- Open an issue for general questions
- Email Dr. M. Reza Hosseini (reza.hosseini@unimelb.edu.au) for collaboration inquiries
- Check existing issues and PRs first to avoid duplicates

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Acknowledgments

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- Academic papers (where appropriate)

Thank you for contributing to advancing research in construction AI and time-series analysis!
