import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.markdown(
    """
    <style>
        /* Page background */
        .main, .stApp {
            background-color: #F4F6F8;
        }

        /* Headings */
        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #1C3F66;
        }

        /* Buttons */
        .stButton>button {
            background-color: #3FB8AF;
            color: white;
            border-radius: 6px;
            border: none;
        }

        /* File uploader label */
        .stFileUploader label {
            color: #2F5C8F;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Azure Web App")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = df.head(100)
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
    st.subheader("Charts")

    all_cols = df.columns.tolist()

    x_col = st.selectbox("Select X‑axis column", all_cols)
    y_cols = st.multiselect("Select Y‑axis column(s)", all_cols)

    chart_type = st.radio("Chart type", ["Bar", "Line"])

    if x_col and y_cols:
        chart_data = df[[x_col] + y_cols]

        if chart_type == "Bar":
            st.bar_chart(chart_data, x=x_col)
        else:
            st.line_chart(chart_data, x=x_col)

else:
    st.info("Upload a CSV file to begin.")
