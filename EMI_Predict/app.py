# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px

# # --- 1. CONFIGURATION ---
# st.set_page_config(page_title="EMIPredict AI", layout="wide")

# # --- 2. MOCK ENGINE (Replaces MLflow) ---
# def simulate_prediction(salary, credit_score, current_emi):
#     """
#     Simulates the AI models so you can develop the UI without a backend.
#     """
#     # Simple logic to determine 'Eligibility'
#     if credit_score > 700 and (current_emi < (salary * 0.4)):
#         elig_pred = 2 # Eligible
#     elif credit_score > 600:
#         elig_pred = 1 # High Risk
#     else:
#         elig_pred = 0 # Denied
        
#     # Simple logic for Max Capacity (30% of disposable income)
#     max_capacity = (salary - current_emi) * 0.35
#     return elig_pred, max_capacity

# # --- 3. UI COMPONENTS ---
# def show_data_insights():
#     st.title("📊 Data Insights")
#     try:
#         # Assuming you have this file locally
#         df = pd.read_csv("emi_prediction_dataset.csv")
#         st.subheader("Financial Distributions")
#         fig = px.histogram(df, x="credit_score", color="emi_eligibility", barmode="overlay")
#         st.plotly_chart(fig, use_container_width=True)
#     except:
#         st.warning("Upload 'emi_prediction_dataset.csv' to see real charts. Showing demo chart instead.")
#         st.bar_chart(np.random.randn(10, 2))

# # --- 4. SIDEBAR NAVIGATION ---
# st.sidebar.title("🚀 EMIPredict AI")
# st.sidebar.success("Mode: UI Development (Local)")
# page = st.sidebar.radio("Go to", ["Home", "Predictions", "Data Insights"])

# # --- PAGE 1: HOME ---
# if page == "Home":
#     st.title("🏦 Loan Eligibility System")
#     st.info("Welcome to the prediction interface. Go to 'Predictions' to test the calculator.")

# # --- PAGE 2: PREDICTIONS ---
# elif page == "Predictions":
#     st.title("🧬 EMI Eligibility Engine")
    
#     with st.form("feature_intelligence_form"):
#         c1, c2 = st.columns(2)
#         with c1:
#             st.subheader("👤 Profile")
#             u_salary = st.number_input("Monthly Net Income (₹)", value=85000)
#             u_credit = st.slider("Credit Score", 300, 850, 720)
#         with c2:
#             st.subheader("💳 Obligations")
#             u_cur_emi = st.number_input("Existing Monthly EMIs (₹)", value=5000)
#             u_rent = st.number_input("Monthly Rent (₹)", value=15000)
        
#         run_analysis = st.form_submit_button("🚀 CALCULATE ELIGIBILITY")

#     if run_analysis:
#         # Use our simulation function instead of MLflow
#         elig_pred, max_capacity = simulate_prediction(u_salary, u_credit, u_cur_emi)

#         st.divider()
#         res1, res2 = st.columns(2)

#         with res1:
#             status_map = {0: "❌ Denied", 1: "⚠️ High Risk", 2: "✅ Eligible"}
#             st.metric("Eligibility Status", status_map[elig_pred])
#             if elig_pred == 2:
#                 st.success("Strong likelihood of approval.")
#             elif elig_pred == 1:
#                 st.warning("Profile is on the edge.")
#             else:
#                 st.error("Does not meet thresholds.")

#         with res2:
#             st.metric("Max EMI Capacity", f"₹{max_capacity:,.2f}")
#             st.progress(0.65) # Visual placeholder
#             st.caption("AI-Predicted Monthly Capacity")

# # --- PAGE 3: DATA INSIGHTS ---
# elif page == "Data Insights":
#     show_data_insights()

# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px

# # --- 1. CONFIGURATION ---
# st.set_page_config(page_title="EMIPredict AI", layout="wide")

# # --- 2. MOCK PREDICTION LOGIC (For UI Testing) ---
# def get_mock_prediction(data):
#     # This simulates the model behavior
#     score = 0
#     if data['credit_score'] > 700: score += 1
#     if data['monthly_salary'] > 50000: score += 1
    
#     eligibility = 2 if score == 2 else 1 if score == 1 else 0
#     max_emi = (data['monthly_salary'] - data['current_emi_amount']) * 0.4
#     return eligibility, max_emi

# # --- 3. SIDEBAR NAVIGATION ---
# st.sidebar.title("🚀 EMIPredict AI")
# st.sidebar.info("Model Registry: Connected") # Keeping the label for UI look
# page = st.sidebar.radio("Go to", ["Home", "Predictions", "Data Insights", "Admin Dashboard"])

# # --- PAGE 1: HOME ---
# if page == "Home":
#     st.title("🏦 Loan Eligibility & EMI Prediction System")
#     st.write("Welcome! Navigate to the Predictions page to test the eligibility engine.")

# # --- PAGE 2: PREDICTIONS ---
# elif page == "Predictions":
#     st.title("🧬 EMI Eligibility ")
#     st.markdown("This engine calculates your **Eligibility Status** and **Affordability Limit** based on your unique features.")

#     with st.form("feature_intelligence_form"):
#         # Section 1: Profile & Obligations
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("👤 Profile & Income")
#             u_salary = st.number_input("Monthly Net Income (₹)", value=85000)
#             u_age = st.number_input("Current Age", 18, 70, 30)
#             u_credit = st.slider("Credit Score", 300, 850, 720)
#             u_years = st.number_input("Employment Years", value=5.0)

#         with col2:
#             st.subheader("💳 Obligations & Assets")
#             u_rent = st.number_input("Monthly Rent/Home Exp (₹)", value=15000)
#             u_cur_emi = st.number_input("Existing Monthly EMIs (₹)", value=5000)
#             u_bank = st.number_input("Liquid Bank Balance (₹)", value=250000)
#             u_dependents = st.number_input("Number of Dependents", 0, 10, 2)

#         st.divider()
        
#         # Section 2: Test Scenario (Matches your first screenshot)
#         st.subheader("🎯 Test Scenario")
#         sc1, sc2 = st.columns(2)
#         u_req_amt = sc1.number_input("Loan Amount to Test (₹)", value=500000)
#         u_tenure = sc2.number_input("Desired Tenure (Months)", value=48)
        
#         run_analysis = st.form_submit_button("🚀 CALCULATE ELIGIBILITY")

#     if run_analysis:
#         # Prepare the emi2026 dataframe
#         feature_data = {
#             "age": u_age,
#             "monthly_salary": u_salary,
#             "years_of_employment": u_years,
#             "current_emi_amount": u_cur_emi,
#             "credit_score": u_credit,
#             "bank_balance": u_bank,
#             "requested_emi": u_req_amt / u_tenure
#         }
        
#         # UI Results
#         elig, cap = get_mock_prediction(feature_data)
        
#         st.divider()
#         res1, res2 = st.columns(2)
#         with res1:
#             status_map = {0: "❌ Denied", 1: "⚠️ High Risk", 2: "✅ Eligible"}
#             st.metric("Eligibility Status", status_map[elig])
#         with res2:
#             st.metric("Max EMI Capacity", f"₹{cap:,.2f}")

# # --- PAGE 3: DATA INSIGHTS ---
# elif page == "Data Insights":
#     st.title("📊 Data Insights & Model Governance")
#     tab1, tab2 = st.tabs(["📈 Business Analytics", "⚙️ MLflow Tracking"])
    
#     with tab1:
#         st.subheader("Financial Distributions")
#         # Placeholder for the histogram in your screenshot
#         chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
#         st.line_chart(chart_data)

# # --- PAGE 4: ADMIN ---
# elif page == "Admin Dashboard":
#     st.title("⚙️ System Admin")
#     st.metric("Registry Status", "Connected", delta="Sync Active")


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

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🚀 EMIPredict AI")
st.sidebar.info("Model Registry: Connected")
page = st.sidebar.radio("Go to", ["Home", "Predictions", "Data Insights", "Admin Dashboard"])

# --- PAGE 1: HOME ---
if page == "Home":
    st.title("🏦 Loan Eligibility & EMI Prediction System")
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
    st.title("📊 Data Insights & Model Governance")
    st.info("Visualizing trends from the emi_prediction_dataset.")
    # Placeholder chart
    st.bar_chart(np.random.randn(10, 2))

# --- PAGE 4: ADMIN ---
elif page == "Admin Dashboard":
    st.title("⚙️ System Admin")
    st.metric("Registry Status", "Connected", delta="Sync Active")