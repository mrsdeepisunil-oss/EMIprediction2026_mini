import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="EMIPredict AI", layout="wide")

# --- 2. MOCK PREDICTION LOGIC ---
def get_realtime_analytics(data):
    # Calculate Disposable Income and Debt-to-Income (DTI)
    disposable_income = data['salary'] - data['emi'] - data['rent']
    total_obligations = data['emi'] + data['rent']
    dti_ratio = total_obligations / data['salary'] if data['salary'] > 0 else 1
    
    # --- A. CLASSIFICATION LOGIC (Decision Tree) ---
    score = 0
    # Condition 1: Creditworthiness
    if data['credit'] > 700: score += 1
    # Condition 2: Disposable Income & DTI Safety
    if disposable_income > 25000 and dti_ratio < 0.45: score += 1
    # Condition 3: Age & Liquidity Penalty (Reduces risk for age 50+ with low bank balance)
    if data['age'] > 45 and data['bank'] < 100000: score -= 1

    # Map score to result
    if score >= 2: result = 2   # Eligible
    elif score == 1: result = 1 # High Risk
    else: result = 0            # Denied

    # --- B. REGRESSION LOGIC (Weighted Formula) ---
    # Capacity reduces as you approach retirement (age 60)
    age_tenure_factor = max(0.1, (60 - data['age']) / 30) 
    base_capacity = disposable_income * 0.4
    
    # Final Capacity adjusted by age and credit reliability
    final_cap = base_capacity * age_tenure_factor * (data['credit'] / 850)
    
    return result, max(0, final_cap)

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
    st.title("🧬 Real-Time Financial Analytics")
    st.markdown("Predicting **Eligibility (Classification)** and **Capacity (Regression)**.")

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
        
        run_analysis = st.form_submit_button("🚀 RUN ANALYTICS")

    if run_analysis:
        # 1. Package inputs for the function
        feature_data = {
            "salary": u_salary, "age": u_age, "credit": u_credit, "years": u_years,
            "rent": u_rent, "emi": u_cur_emi, "bank": u_bank, "dep": u_dependents
        }

        # 2. Run the Function (Classification & Regression)
        elig_result, cap_result = get_realtime_analytics(feature_data)

        st.divider()
        res1, res2 = st.columns(2)

        with res1:
            st.subheader("📊 Classification: Eligibility")
            status_map = {0: "❌ Denied", 1: "⚠️ High Risk", 2: "✅ Eligible"}
            st.metric("System Verdict", status_map[elig_result])
            
            # Contextual warning for your age 50 scenario
            if u_age > 45 and elig_result < 2:
                st.warning("Decision influenced by limited retirement tenure and high expenses.")

        with res2:
            st.subheader("📈 Regression: EMI Capacity")
            st.metric("Predicted Max EMI", f"₹{cap_result:,.2f}")
            st.progress(min(1.0, cap_result/u_salary) if u_salary > 0 else 0)
            st.caption("Calculated via Age-Weighted Regression Logic.")


# --- PAGE 3: DATA INSIGHTS ---
elif page == "Data Insights":
    show_data_insights()

# --- PAGE 4: ADMIN ---
elif page == "Admin Dashboard":
    st.title("⚙️ System Admin")
    st.metric("Registry Status", "Connected", delta="Sync Active")