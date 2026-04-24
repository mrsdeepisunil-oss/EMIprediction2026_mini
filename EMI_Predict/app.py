import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="EMIPredict AI", layout="wide")

# --- 2. MOCK PREDICTION LOGIC ---
def get_mock_prediction(data):
    score = 0
    if data['credit_score'] > 700: score += 1
    if data['monthly_salary'] > 50000: score += 1
    
    eligibility = 2 if score == 2 else 1 if score == 1 else 0
    # Logic: Capacity is 40% of Disposable Income
    max_emi = (data['monthly_salary'] - data['current_emi_amount'] - data['rent']) * 0.4
    return eligibility, max_emi

def show_data_insights():
    st.title("📊 Data Insights")
    st.markdown("Explore the trends and underlying data used for our eligibility predictions.")
    
    try:
        # 1. THE CORRECT RAW URL
        csv_url = "https://raw.githubusercontent.com/mrsdeepisunil-oss/EMIprediction2026_mini/main/EMI_Predict/emi_prediction_dataset.csv"
        
        # 2. LOAD DATA ONCE (using q2024 as requested)
        q2024 = pd.read_csv(csv_url, on_bad_lines='skip')
        df = q2024 
        
        tab1, tab2 = st.tabs(["📈 Business Analytics", "📋 Dataset Overview"])

        with tab1:
            st.subheader("Financial Distributions")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Records", len(df))

            # 3. FIXED: parentheses after .mean()
            avg_score = int(df['credit_score'].mean()) 
            m2.metric("Avg Credit Score", avg_score)

            # 4. FIXED: parentheses after .mean()
            eligible_rate = (df['emi_eligibility'] == 2).mean()
            m3.metric("Eligible Rate", f"{eligible_rate:.1%}")
            
            col_left, col_right = st.columns(2)
            with col_left:
                st.write("**Credit Score Impact**")
                fig = px.histogram(
                    df, x="credit_score", color="emi_eligibility", 
                    barmode="overlay", color_discrete_sequence=px.colors.qualitative.Set1
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_right:
                st.write("**Income vs. Predicted Capacity**")
                fig2 = px.scatter(
                    df, x="monthly_salary", y="max_monthly_emi", 
                    color="emi_eligibility", opacity=0.5
                )
                st.plotly_chart(fig2, use_container_width=True)

        with tab2:
            st.subheader("Raw Data Preview")
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Dataset as CSV",
                data=csv,
                file_name='emi_data_export.csv',
                mime='text/csv',
            )

    except Exception as e:
        st.error(f"Error loading insights: {e}")

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🚀 EMIPredict AI")
st.sidebar.info("Model Registry: Connected")
page = st.sidebar.radio("Go to", ["Home", "Predictions", "Data Insights", "Admin Dashboard"])

# --- PAGE 1: HOME ---
if page == "Home":
    st.title("🏦 EMI Prediction System")
    st.write("Welcome! Navigate to the Predictions page to assess financial profile eligibility.")

# --- PAGE 2: PREDICTIONS ---
elif page == "Predictions":
    st.title("🧬 EMI Eligibility")
    st.markdown("Assess **Eligibility Status** and **Affordability Limit** based on profile features.")

    with st.form("feature_intelligence_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Profile & Income")
            u_salary = st.number_input("Monthly Net Income (₹)", value=85000)
            u_age = st.number_input("Current Age", 18, 70, 30)
            u_credit = st.slider("Credit Score", 300, 850, 720)
            u_years = st.number_input("Employment Years", value=5.0)

        with col2:
            st.subheader("💳 Obligations & Assets")
            u_rent = st.number_input("Monthly Rent/Home Exp (₹)", value=15000)
            u_cur_emi = st.number_input("Existing Monthly EMIs (₹)", value=5000)
            u_bank = st.number_input("Liquid Bank Balance (₹)", value=250000)
            u_dependents = st.number_input("Number of Dependents", 0, 10, 2)

        # The "Test Scenario" section has been removed from here
        
        run_analysis = st.form_submit_button("🚀 CALCULATE ELIGIBILITY")

    if run_analysis:
        # Data dictionary for calculation
        feature_data = {
            "age": u_age,
            "monthly_salary": u_salary,
            "years_of_employment": u_years,
            "current_emi_amount": u_cur_emi,
            "credit_score": u_credit,
            "bank_balance": u_bank,
            "rent": u_rent
        }
        
        # UI Results
        elig, cap = get_mock_prediction(feature_data)
        
        st.divider()
        res1, res2 = st.columns(2)
        with res1:
            status_map = {0: "❌ Denied", 1: "⚠️ High Risk", 2: "✅ Eligible"}
            st.metric("Eligibility Status", status_map[elig])
            
        with res2:
            # Setting a floor of 0 for capacity
            display_cap = max(0, cap)
            st.metric("Max EMI Capacity", f"₹{display_cap:,.2f}")
            st.info("This is the maximum monthly EMI the system predicts you can afford.")

# --- PAGE 3: DATA INSIGHTS ---
elif page == "Data Insights":
    show_data_insights()

# --- PAGE 4: ADMIN ---
elif page == "Admin Dashboard":
    st.title("⚙️ System Admin")
    st.metric("Registry Status", "Connected", delta="Sync Active")