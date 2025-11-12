@echo off
REM Quick Start Script for E-Commerce Insights Agent
REM This script activates the virtual environment and runs the Streamlit app

echo.
echo ====================================
echo  E-Commerce Insights Agent
echo ====================================
echo.
echo Starting application...
echo.

REM Activate virtual environment and run app
call venv\Scripts\activate.bat
streamlit run app.py

pause
