@echo off
echo ===================================================
echo Starting AI-Powered Stock Analysis Dashboard
echo ===================================================
echo Verifying Python environment...
python -m pip install -r requirements.txt
echo.
echo Launching Streamlit Dashboard...
python -m streamlit run app.py
pause
