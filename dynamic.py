import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Data Analysis")

st.title("Dynamic Data Analysis")
st.write("Upload a CSV or Excel File for Analysis")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File Uploaded Successfully!")

    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    num_cols = list(df.select_dtypes(include="number").columns)
    date_cols = list(df.select_dtypes(include="datetime").columns)
    other_cols = [c for c in df.columns if c not in num_cols and c not in date_cols]
    cat_cols = [c for c in other_cols]

    st.header("Dataset")
    st.write("Showing all", df.shape[0], "Scroll inside the box to see more.")
    st.dataframe(df, height=400)

    st.divider()
    st.header("Basic Details")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing values", int(df.isnull().sum().sum()))
    c4.metric("Duplicate rows", int(df.duplicated().sum()))

    st.subheader("Missing values per column")
    st.dataframe(df.isnull().sum().to_frame("Missing"))

    st.subheader("Column types")
    st.dataframe(df.dtypes.astype(str).to_frame("Type"))

    st.divider()
    st.header("Statistics")
    if num_cols:
        st.subheader("One column")
        stat_col = st.selectbox("Select a number column", num_cols)
        values = df[stat_col].dropna().to_numpy()

        s1, s2, s3 = st.columns(3)
        s1.metric("Mean", round(float(np.mean(values)), 2))
        s2.metric("Median", round(float(np.median(values)), 2))
        s3.metric("Mode", round(float(df[stat_col].mode().iloc[0]), 2))

        s4, s5, s6 = st.columns(3)
        s4.metric("Std Dev", round(float(np.std(values)), 2))
        s5.metric("Min", round(float(np.min(values)), 2))
        s6.metric("Max", round(float(np.max(values)), 2))

        st.subheader("All number columns")
        summary = pd.DataFrame({
            "Mean": df[num_cols].mean(),
            "Median": df[num_cols].median(),
            "Mode": df[num_cols].mode().iloc[0],
            "Std Dev": df[num_cols].std(),
            "Min": df[num_cols].min(),
            "Max": df[num_cols].max(),
        }).round(2)
        st.dataframe(summary)
    else:
        st.warning("No number columns in this file.")
        
    st.divider()
    st.header("Chart Builder")
    chart_type = st.selectbox("Select chart type", ["Bar", "Line", "Area", "Scatter", "Map"])

    if chart_type in ["Bar", "Line", "Area"]:
        x_options = date_cols + cat_cols

        if len(x_options) == 0 or len(num_cols) == 0:
            st.warning("This file needs at least one category or date column and one number column.")
        else:
            x_col = st.selectbox("X axis", x_options)
            y_col = st.selectbox("Y axis", num_cols)

            if x_col in date_cols:
                key = df[x_col].dt.year
            else:
                key = df[x_col]

            result = df.groupby(key)[y_col].mean().round(2)

            if chart_type == "Bar":
                st.bar_chart(result)
            elif chart_type == "Line":
                st.line_chart(result)
            else:
                st.area_chart(result)

    elif chart_type == "Scatter":
        if len(num_cols) < 2:
            st.warning("Scatter chart needs at least 2 number columns.")
        else:
            x_col = st.selectbox("X axis", num_cols)
            y_col = st.selectbox("Y axis", num_cols, index=1)

            if x_col == y_col:
                st.warning("Please select two different columns.")
            else:
                st.scatter_chart(df[[x_col, y_col]].dropna().head(2000), x=x_col, y=y_col)

    else:
        if "lat" in df.columns and "lon" in df.columns:
            st.map(df[["lat", "lon"]].dropna())
        else:
            st.warning("A map needs columns named lat and lon. This file has none.")     