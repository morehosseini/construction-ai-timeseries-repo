#!/bin/bash
# Setup script for Construction AI Time-Series Analysis Repository

echo "================================================"
echo "Construction AI Time-Series Analysis - Setup"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Ask user for installation method
echo "Choose installation method:"
echo "1) pip (virtual environment)"
echo "2) conda (recommended)"
echo "3) pip (system-wide, not recommended)"
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "Setting up with pip and virtual environment..."
        
        # Create virtual environment
        python3 -m venv .venv
        
        # Activate virtual environment
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            source .venv/Scripts/activate
        else
            source .venv/bin/activate
        fi
        
        # Upgrade pip
        pip install --upgrade pip
        
        # Install requirements
        pip install -r requirements.txt
        
        echo ""
        echo "✅ Setup complete!"
        echo ""
        echo "To activate the environment in the future, run:"
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            echo "  source .venv/Scripts/activate"
        else
            echo "  source .venv/bin/activate"
        fi
        ;;
        
    2)
        echo ""
        echo "Setting up with conda..."
        
        # Check if conda is installed
        if ! command -v conda &> /dev/null; then
            echo "❌ Conda is not installed. Please install Anaconda or Miniconda first."
            echo "   Download from: https://docs.conda.io/en/latest/miniconda.html"
            exit 1
        fi
        
        # Create conda environment
        conda env create -f environment.yml
        
        echo ""
        echo "✅ Setup complete!"
        echo ""
        echo "To activate the environment, run:"
        echo "  conda activate construction-timeseries"
        ;;
        
    3)
        echo ""
        echo "⚠️  Installing system-wide (not recommended)..."
        read -p "Are you sure? This may affect other Python projects. [y/N]: " confirm
        
        if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
            pip install --user -r requirements.txt
            echo ""
            echo "✅ Setup complete!"
        else
            echo "Installation cancelled."
            exit 0
        fi
        ;;
        
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "================================================"
echo "Next steps:"
echo "================================================"
echo "1. Prepare your data following DATA.md specifications"
echo "2. Place data in the 'data/' directory"
echo "3. Run: jupyter notebook notebooks/AI_Job_Postings_Construction_TimeSeries.ipynb"
echo ""
echo "For questions, see README.md or open an issue on GitHub."
echo "================================================"
