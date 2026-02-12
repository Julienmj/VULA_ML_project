@echo off
echo ================================================
echo Crop Disease Detection - Training Script
echo ================================================
echo.
echo This will train the model using 3,000 sample images.
echo Training will take approximately 5-10 minutes.
echo.
echo Using Random Forest (scikit-learn) model
echo.
pause
echo.
echo Starting training...
python src\train_model_sklearn.py
echo.
echo ================================================
echo Training Complete!
echo ================================================
echo.
echo To run the web interface, execute: run_ui.bat
echo Or manually run: streamlit run ui\app.py
echo.
pause
