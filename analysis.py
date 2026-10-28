import streamlit as st
import pandas as pd
import numpy as np

st.title("Healthcare Data Analysis")
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)

    uploaded_df["Date of Admission"] = pd.to_datetime(uploaded_df["Date of Admission"])
    uploaded_df["Discharge Date"] = pd.to_datetime(uploaded_df["Discharge Date"])
    uploaded_df["Stay Days"] = (uploaded_df["Discharge Date"] - uploaded_df["Date of Admission"]).dt.days

    st.header("Data Preview")
    st.dataframe(uploaded_df.head(10))

    st.divider()
    st.header("Basic Details")
    #c1, c2, c3, c4 = st.columns(4)
    st.metric("Rows", uploaded_df.shape[0])
    st.metric("Columns", uploaded_df.shape[1])
    st.metric("Missing values", int(uploaded_df.isnull().sum().sum()))
    st.metric("Duplicate rows", int(uploaded_df.duplicated().sum()))

    st.divider()
    st.header("Statistics")
    stat_col = st.selectbox("Select a column", ["Age", "Billing Amount", "Stay Days"])
    values = uploaded_df[stat_col].to_numpy()

    s1, s2, s3, s4, s5 = st.columns(5)
    s1.metric("Mean", round(float(np.mean(values)), 2))
    s2.metric("Median", round(float(np.median(values)), 2))
    s3.metric("Std Dev", round(float(np.std(values)), 2))
    s4.metric("Min", round(float(np.min(values)), 2))
    s5.metric("Max", round(float(np.max(values)), 2))

    st.divider()
    st.header("Group Analysis")

    st.subheader("Average billing amount by medical condition")
    billing_by_condition = uploaded_df.groupby("Medical Condition")["Billing Amount"].mean().round(2)
    st.bar_chart(billing_by_condition)

    st.subheader("Average age by medical condition")
    age_by_condition = uploaded_df.groupby("Medical Condition")["Age"].mean().round(1)
    st.bar_chart(age_by_condition)

    st.divider()
    st.header("Patient Count")
    count_by = st.selectbox(
        "Count patients by",
        ["Medical Condition", "Admission Type", "Test Results", "Gender"],
    )
    st.bar_chart(uploaded_df[count_by].value_counts())

    st.divider()
    st.header("Admissions Per Year")
    per_year = uploaded_df.groupby(uploaded_df["Date of Admission"].dt.year).size()
    st.line_chart(per_year)

    st.divider()
    st.header("Age vs Billing Amount")
    sample_df = uploaded_df.sample(2000)
    st.scatter_chart(sample_df, x="Age", y="Billing Amount")

else:
    st.info("Please upload a CSV file to begin.")