import pandas as pd 
import numpy as np 
import streamlit as st
import time
import plotly.express as px

#Saftey Check

def safety_check(upload_file, df):
    issues = []
    raw = upload_file.getvalue()
    name = upload_file.name.lower()

    # 1. Does the content match the file extension?
    if name.endswith(".csv"):
        if b"\x00" in raw[:4096]:
            issues.append("Named .csv but contains binary data")
    elif name.endswith(".xlsx"):
        if not raw.startswith(b"PK"):
            issues.append("Named .xlsx but isn't a real Excel file")
    elif name.endswith(".xls"):
        if not raw.startswith(b"\xd0\xcf\x11\xe0"):
            issues.append("Named .xls but isn't a real Excel file")

    # 2. Formula injection
    flagged = 0
    for col in df.columns:
        s = df[col].dropna().astype(str)
        flagged += int(s.str.match(r"^\s*(=|@|[+\-]\s*[A-Za-z(])").sum())
    if flagged:
        issues.append(f"{flagged} cells start with =, +, - or @ and could run as formulas in Excel")

    return issues

#Page title and intro section: 1
st.set_page_config(page_title="CSV Explorer", layout="wide")
with st.container(border=True):
    st.title("CSV Explorer")
    st.caption("Upload any Excel file (CSV, XLSX, OR XLS) to preview, display stats and display visualisation")

st.divider()

#Upload file section: 2
with st.container(border=True):
    upload_file = st.file_uploader("Choose a CSV file or Excel file", type=["csv", "xlsx", "xls"])

if upload_file is None:
    st.info("Upload a CSV or Excel file to get started")
    st.stop()

#Preview + Stats section: 3
if upload_file is not None:
    if upload_file.name.endswith(".csv"):
        df = pd.read_csv(upload_file)
    else:
        df = pd.read_excel(upload_file)

    st.divider()

    issues = safety_check(upload_file, df)

with st.container(border=True):
    st.subheader("File Safety Check")
    if issues:
        for issue in issues:
            st.warning(issue)
    else:
        st.success("No issues found")
    st.caption("Basic check only, not a full antivirus scan.")

    st.header("Data Preview")
    st.dataframe(df, use_container_width=True)

    start_time = time.time()
    _ = df.memory_usage(deep=True)
    load_duration = time.time() - start_time

st.divider()


with st.container(border=True):
    st.header("Dataset Overview & Memory")
    stat1, stat2, stat3, stat4, stat5, stat6 = st.columns(6)
    with stat1:
        st.metric("Rows", f"{df.shape[0]:,}")
    with stat2:
        st.metric("Columns", df.shape[1])
    with stat3:
        st.metric("Missing Values", f"{df.isna().sum().sum():,}")
    with stat4:
        mem_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
        st.metric("Memory usage", f"{mem_mb:.2f} MB")
    with stat5:
        dup_rows = df.duplicated().sum()
        st.metric("Duplicate Rows", f"{dup_rows:,}")
    with stat6:
        st.metric("Memory Scan Time ", f"{load_duration:.3f} sec")

st.divider()

with st.container(border=True):
    st.title("Visualisation")
    st.caption("Pick a chart type and columns to explore your dataset. Not every column combination will work with every chart, so if a chart looks wrong or fails, try a different selection.")

ctrl1, ctrl2, ctrl3 = st.columns(3)

with ctrl1:
    chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Pie", "Histogram", "Map view (requires latitude/longitude)"])

try:
    if chart_type == "Histogram":
        with ctrl2:
            x_col = st.selectbox("Column", df.columns)
        fig = px.histogram(df, x=x_col)

    elif chart_type == "Pie":
        with ctrl2:
            names_col = st.selectbox("Category column", df.columns)
        with ctrl3:
            values_col = st.selectbox("Value column", df.columns)
        fig = px.pie(df, names=names_col, values=values_col)

    elif chart_type == "Map view (requires latitude/longitude)":
        with ctrl2:
            lat_col = st.selectbox("Latitude column", df.columns)
        with ctrl3:
            lon_col = st.selectbox("Longitude column", df.columns)
        fig = px.scatter_map(df, lat=lat_col, lon=lon_col, zoom=3, height=500)
        fig.update_layout(map_style="open-street-map")

    else:  # Bar, Line, Scatter
        with ctrl2:
            x_col = st.selectbox("X-axis column", df.columns)
        with ctrl3:
            y_col = st.selectbox("Y-axis column", df.columns)

        if chart_type == "Bar":
            fig = px.bar(df, x=x_col, y=y_col)
        elif chart_type == "Line":
            fig = px.line(df, x=x_col, y=y_col)
        else:
            fig = px.scatter(df, x=x_col, y=y_col)

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Couldn't build this chart with those columns. Try a different combination. ({e})")