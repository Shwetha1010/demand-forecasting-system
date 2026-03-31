# Demand Forecasting and Decision Intelligence System

## Overview

This project presents an end-to-end machine learning system for forecasting retail demand and generating actionable business recommendations. It simulates a real-world decision support system by integrating predictive modeling with an interactive user interface and a deployed API.

The system predicts future sales based on historical patterns and provides guidance on inventory and promotional strategies.

---

## Live Application

Frontend: https://demand-forecasting-system-1.onrender.com/  
Backend API: https://demand-forecasting-system-vm05.onrender.com/docs  

---

## Key Features

- Multi-step time series demand forecasting  
- Feature engineering using lag variables and rolling statistics  
- Machine learning model built using LightGBM  
- REST API using FastAPI for real-time predictions  
- Interactive dashboard built with Streamlit  
- Scenario-based analysis (High, Moderate, Low, Festival, Custom)  
- Business decision recommendations based on predicted demand  
- Cloud deployment using Render  

---

## System Architecture

User Interface (Streamlit)  
→ FastAPI Backend  
→ Machine Learning Model (LightGBM)  
→ Prediction Output  
→ Business Recommendation  

---

## Project Structure
demand_forecasting_system/
│
├── api/ # FastAPI backend
├── dashboard/ # Streamlit frontend
├── src/ # Data processing and modeling logic
├── models/ # Trained model artifacts
├── data/ # Dataset files
├── requirements.txt # Dependencies
└── README.md

---

## Model Details

- Model: LightGBM Regressor  
- Target: Sales  
- Key Features:
  - Sales lag features (previous day, previous week)
  - Rolling mean of sales
  - Store and promotional attributes  
- Forecasting approach: Recursive multi-step prediction for 7-day horizon  

---

## Output

- Next-day sales prediction  
- Weekly demand trend  
- Decision recommendation:
  - Increase stock  
  - Maintain stock  
  - Run promotions  

---

## Limitations

- Based on historical dataset (not real-time data)  
- Recursive forecasting may introduce cumulative error  
- Limited external factors (e.g., weather, pricing, events)  

---

## Future Enhancements

- Integration with real-time data sources  
- Inclusion of external variables (weather, holidays, pricing)  
- Model explainability using SHAP  
- Advanced forecasting models (Prophet, deep learning architectures)  

---

## Technologies Used

- Python  
- Pandas, NumPy  
- Scikit-learn  
- LightGBM  
- FastAPI  
- Streamlit  
- Plotly  
- Render (Deployment)  

