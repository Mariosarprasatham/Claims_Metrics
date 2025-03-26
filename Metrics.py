import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl

# Streamlit App
st.title('Claim Processing Dashboard')

# File Upload
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        # Filters
        level_options = ['All Levels', 'Level 1', 'Level 2', 'Level 3']
        selected_level = st.selectbox('Select Level', level_options)

        employee_options = ['All Employees']
        if selected_level == 'Level 1':
            employee_options.extend(df['Level 1 Owner'].dropna().unique())
        elif selected_level == 'Level 2':
            employee_options.extend(df['Level 2 Owner'].dropna().unique())
        elif selected_level == 'Level 3':
            employee_options.extend(df['Level 3 Owner'].dropna().unique())
        else:
            employee_options.extend(df['Level 1 Owner'].dropna().unique())
            employee_options.extend(df['Level 2 Owner'].dropna().unique())
            employee_options.extend(df['Level 3 Owner'].dropna().unique())

        selected_employee = st.selectbox('Select Employee', employee_options)

        # Filter Data
        filtered_df = df.copy()

        if selected_level != 'All Levels':
            if selected_level == 'Level 1':
                filtered_df = filtered_df.rename(columns={'Level 1 Owner': 'Owner', 'Level 1 Process Time': 'Process Time'})
                filtered_df = filtered_df[['Claim ID', 'Owner', 'Process Time', 'Claim Status', 'Invoice Amount']]
            elif selected_level == 'Level 2':
                filtered_df = filtered_df.rename(columns={'Level 2 Owner': 'Owner', 'Level 2 Process Time': 'Process Time'})
                filtered_df = filtered_df[['Claim ID', 'Owner', 'Process Time', 'Claim Status', 'Invoice Amount']]
            elif selected_level == 'Level 3':
                filtered_df = filtered_df.rename(columns={'Level 3 Owner': 'Owner', 'Level 3 Process Time': 'Process Time'})
                filtered_df = filtered_df[['Claim ID', 'Owner', 'Process Time', 'Claim Status', 'Invoice Amount']]

            if selected_employee != 'All Employees':
                filtered_df = filtered_df[filtered_df['Owner'] == selected_employee]
        else:
            if selected_employee != 'All Employees':
                filtered_df_level1 = df.rename(columns={'Level 1 Owner': 'Owner', 'Level 1 Process Time': 'Process Time'})[['Claim ID', 'Owner', 'Process Time', 'Claim Status', 'Invoice Amount']]
                filtered_df_level2 = df.rename(columns={'Level 2 Owner': 'Owner', 'Level 2 Process Time': 'Process Time'})[['Claim ID', 'Owner', 'Process Time', 'Claim Status', 'Invoice Amount']]
                filtered_df_level3 = df.rename(columns={'Level 3 Owner': 'Owner', 'Level 3 Process Time': 'Process Time'})[['Claim ID', 'Owner', 'Process Time', 'Claim Status', 'Invoice Amount']]

                filtered_df = pd.concat([filtered_df_level1, filtered_df_level2, filtered_df_level3], ignore_index=True)
                filtered_df = filtered_df[filtered_df['Owner'] == selected_employee]

        # Metrics
        st.subheader('Metrics')

        if selected_level == 'All Levels':
            level_times = {}
            for level in [1, 2, 3]:
                level_col = f'Level {level} Process Time'
                if level_col in df.columns:
                    level_times[f'Level {level}'] = df[level_col].mean()
            for level, avg_time in level_times.items():
                st.metric(f'Avg. {level} Process Time', f'{avg_time:.2f} mins')
        else:
            if 'Process Time' in filtered_df.columns:
                avg_level_time = filtered_df['Process Time'].mean()
                st.metric(f'Avg. {selected_level} Process Time', f'{avg_level_time:.2f} mins')

        invoice_by_status = filtered_df.groupby('Claim Status')['Invoice Amount'].sum()
        st.subheader('Invoice Amount by Claim Status')
        st.write(invoice_by_status)

        st.subheader('Claim Status Breakdown')
        fig_pie = px.pie(filtered_df, names='Claim Status', title='Claim Status Distribution')
        st.plotly_chart(fig_pie)

        # Employee Metrics
        if selected_employee != 'All Employees':
            st.subheader(f'Employee Metrics: {selected_employee}')
            claims_processed = len(filtered_df)
            st.metric('Number of Claims Processed', claims_processed)
            if 'Process Time' in filtered_df.columns:
                avg_employee_time = filtered_df['Process Time'].mean()
                st.metric('Avg. Claim Processing Time', f'{avg_employee_time:.2f} mins')

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload an Excel file.")
