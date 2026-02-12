@echo off
echo ================================================
echo Python Environment Setup
echo ================================================
echo.
echo This will create a virtual environment and install packages.
echo Make sure you have Python 3.11 or 3.12 installed!
echo.
pause

echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing packages...
pip install pandas numpy opencv-python scikit-learn streamlit jupyter matplotlib seaborn

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo To use the environment:
echo 1. Run: venv\Scripts\activate
echo 2. Then: python src\train_model_sklearn.py
echo.
pause
