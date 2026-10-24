#!/bin/bash
echo "==================================================="
echo "Starting AI-Powered Stock Analysis Dashboard"
echo "==================================================="
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
