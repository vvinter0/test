import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.title("Azure Web App")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state["data"] = df  # optional: store in session state

if "data" in st.session_state:
    df = st.session_state["data"]

    gb = GridOptionsBuilder.from_dataframe(df)

    # Enable filtering for all columns
    gb.configure_default_column(filter=True)

    gb.configure_grid_options(
        suppressColumnVirtualisation=True,
        suppressRowClickSelection=True,
        onFirstDataRendered="function(params){params.api.sizeColumnsToFit();}",
        onGridSizeChanged="function(params){params.api.sizeColumnsToFit();}"
    )

    gridOptions = gb.build()

    AgGrid(
        df,
        gridOptions=gridOptions,
        height=500,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=True,
        fit_columns_on_grid_load=True
    )
