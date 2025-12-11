import streamlit as st
from snowflake import connector
import pandas as pd

ctx = connector.connect(
    account='',
    #user='us336280@mmm.com',
    user =  "",
    password='',
    database='SFDB_DEV',
    warehouse='WH_XS',
    schema='DFASTDICTW01',
    role='FASTBALL_CUSTOM_ROLE',
    autocommit=True,
    client_session_keep_alive=True
    )
tab1,tab2=st.tabs(["Tab 1","Tab2"])
with tab1:
        
    query =  '''

    select RETAILER, COUNTRY, MMM_ID_NBR, SAP_ID, DIVISION from DFASTCDLV02.V02_RETAILER_CATALOG limit 1000;
    '''
    df = pd.read_sql(query, ctx)

    #reset button
    reset_bt = st.sidebar.button("Click to get Original Data")

    retaileroptions = df['RETAILER'].unique()
    Retailer_filter = st.sidebar.selectbox("Choose a Retailer)", retaileroptions)

    # Filter SAP IDs based on selected retailer
    sap_ids = df['SAP_ID'].loc[df['RETAILER'] == Retailer_filter]
    # Text input for SAP ID
    text_filter = st.sidebar.text_input("Enter SAP_ID")


    # Apply filters
    filtered_df = df
    if not reset_bt:
        if Retailer_filter:
            filtered_df = filtered_df[filtered_df['RETAILER'] == Retailer_filter]
        if text_filter:
            filtered_df = filtered_df[filtered_df['SAP_ID'].str.contains(text_filter, case=False)]


    st.write(filtered_df)
