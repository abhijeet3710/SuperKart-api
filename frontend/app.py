import os
import streamlit as st
import requests

st.set_page_config(page_title="Superkart Sales Prediction", layout="centered")

# Read backend base URL from environment variable or default to local/Codespaces port 7860
DEFAULT_BACKEND = "http://127.0.0.1:7860"
BACKEND_ROOT_URL = os.getenv("BACKEND_URL", DEFAULT_BACKEND).rstrip("/")
PREDICT_ENDPOINT = f"{BACKEND_ROOT_URL}/v1/predict"

st.title("Superkart Sales Prediction")
st.caption(f"Connected to Flask Backend: `{PREDICT_ENDPOINT}`")

# Form inputs
col1, col2 = st.columns(2)

with col1:
    Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
    Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, value=0.027)
    Product_MRP = st.number_input("Product MRP", min_value=0.0, value=150.0)
    Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])

with col2:
    Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
    Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
    Product_Id_char = st.selectbox("Product Id Character", ["DR", "FD", "NC"])
    Store_Age_Years = st.number_input("Store Age (Years)", min_value=0.0, value=10.0)
    Product_Type_Category = st.selectbox("Product Type Category", ["Beverages", "Snacks", "Food", "Non-Consumable"])

payload = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}

st.divider()

if st.button("Predict Sales", type="primary"):
    with st.spinner("Communicating with Flask Backend..."):
        try:
            response = requests.post(PREDICT_ENDPOINT, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                sales = result.get("predicted_sales")
                st.success(f"**Predicted Total Sales:** ${sales:,.2f}")
            else:
                st.error(f"Flask Backend Error ({response.status_code}): {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to Flask API at `{PREDICT_ENDPOINT}`: {e}")
