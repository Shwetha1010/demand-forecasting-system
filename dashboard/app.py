import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "https://demand-forecasting-system-vm05.onrender.com/predict"
st.set_page_config(page_title="Demand Intelligence System", layout="wide")

# ------------------- HEADER -------------------
st.title("📊 Demand Forecasting & Decision Intelligence System")

# ------------------- SCENARIO -------------------
scenario = st.selectbox(
    "Select Scenario",
    ["Custom", "High Demand", "Moderate Demand", "Low Demand", "Festival"]
)

# ------------------- DEFAULT VALUES -------------------
store = 1
promo = 1
dayofweek = 3
sales_lag_1 = 5000
sales_lag_7 = 5200
rolling_mean = 5100

year = 2015
month = 7
day = 15
week = 29
stateholiday = 0
schoolholiday = 0
storetype = 1
assortment = 1
competition = 500
promo_interval = 2

# ------------------- SCENARIO LOGIC -------------------
if scenario == "High Demand":
    sales_lag_1, sales_lag_7, rolling_mean = 9000, 8500, 8800
    promo = 1

elif scenario == "Low Demand":
    sales_lag_1, sales_lag_7, rolling_mean = 2000, 1800, 1900
    promo = 0

elif scenario == "Festival":
    sales_lag_1, sales_lag_7, rolling_mean = 9500, 9000, 9200
    promo = 1
    stateholiday = 1

elif scenario == "Moderate Demand":
    sales_lag_1, sales_lag_7, rolling_mean = 5000, 4800, 4900

# ------------------- ✅ CUSTOM INPUT UI (FIXED) -------------------
if scenario == "Custom":
    st.subheader("⚙️ Customize Inputs")

    col1, col2 = st.columns(2)

    with col1:
        store = st.number_input("Store ID", value=1)
        promo = st.selectbox("Promo Running", [0, 1])
        dayofweek = st.slider("Day of Week (0=Mon)", 0, 6, 3)

    with col2:
        sales_lag_1 = st.number_input("Yesterday Sales", value=5000)
        sales_lag_7 = st.number_input("Last Week Sales", value=5200)
        rolling_mean = st.number_input("7-Day Average Sales", value=5100)

# ------------------- PREDICTION -------------------
if st.button("🚀 Run Prediction"):

    input_data = {
        "Store": store,
        "Promo": promo,
        "DayOfWeek": dayofweek,
        "Sales_lag_1": sales_lag_1,
        "Sales_lag_7": sales_lag_7,
        "Rolling_mean_7": rolling_mean,
        "Year": year,
        "Month": month,
        "Day": day,
        "WeekOfYear": week,
        "StateHoliday": stateholiday,
        "SchoolHoliday": schoolholiday,
        "StoreType": storetype,
        "Assortment": assortment,
        "CompetitionDistance": competition,
        "PromoInterval": promo_interval
    }

    try:
        res = requests.post(API_URL, json=input_data)
        result = res.json()
    except:
        st.error("⚠️ API not running")
        st.stop()

    predicted = result["next_day_prediction"]
    predictions = result["predictions"]

    # ------------------- KPI -------------------
    col1, col2 = st.columns(2)
    col1.metric("📈 Next Day Sales", f"{predicted:.0f}")
    col2.metric("💡 Recommendation", result["recommendation"])

    # ------------------- BUSINESS MESSAGE -------------------
    if predicted > 8000:
        st.success("🔥 High demand → Increase stock")
    elif predicted < 3000:
        st.error("⚠️ Low demand → Run promotions")
    else:
        st.info("📊 Stable demand → Maintain stock")

    # ------------------- LINE CHART -------------------
    st.subheader("📈 Weekly Sales Forecast")

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    all_sales = [
        sales_lag_7,
        sales_lag_1,
        predicted
    ] + predictions[1:5]

    df_chart = pd.DataFrame({
        "Day": days,
        "Sales": all_sales
    })

    fig1 = px.line(
        df_chart,
        x="Day",
        y="Sales",
        markers=True,
        title="Weekly Sales Trend"
    )

    fig1.update_traces(
        text=[round(x) for x in all_sales],
        textposition="top center"
    )

    fig1.update_layout(template="plotly_dark")

    st.plotly_chart(fig1, use_container_width=True)

    # ------------------- BAR CHART -------------------
    st.subheader("📊 Sales Comparison")

    compare_df = pd.DataFrame({
        "Type": ["Yesterday", "Last Week", "Predicted"],
        "Sales": [sales_lag_1, sales_lag_7, predicted]
    })

    fig2 = px.bar(
        compare_df,
        x="Type",
        y="Sales",
        text="Sales",
        title="Sales Comparison View"
    )

    fig2.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig2.update_layout(template="plotly_dark")

    st.plotly_chart(fig2, use_container_width=True)

    # ------------------- INSIGHT -------------------
    best_day = df_chart.loc[df_chart["Sales"].idxmax()]
    st.success(f"🔥 Peak demand expected on {best_day['Day']}")