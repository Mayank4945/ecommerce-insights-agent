# Quick Start Script for E-Commerce Insights Agent
# This script activates the virtual environment and runs the Streamlit app

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host " E-Commerce Insights Agent" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting application..." -ForegroundColor Green
Write-Host ""

# Activate virtual environment and run app
& .\venv\Scripts\Activate.ps1
streamlit run app.py
