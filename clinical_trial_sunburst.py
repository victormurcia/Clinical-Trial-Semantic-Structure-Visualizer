import streamlit as st
import pandas as pd
import plotly.express as px

import os
print("Current Directory:", os.getcwd())
print("Files in Directory:", os.listdir('.'))

# Load the data
expanded_df = pd.read_parquet("full_test_sunburst.parquet.gzip")
criteria_df = pd.read_parquet("ct_criteria.parquet.gzip")

st.set_page_config(layout="wide")

# Streamlit app starts here
st.title('Clinical Trial Medical Concept Visualization')

# App description
st.markdown("""
This app visualizes the medical concepts associated with clinical trials based on the selected trial ID (NCTID). 

The entities were extracted using a LLM. **NOTE: This is a very early version of the LLM and as such the performance in terms of extraction accuracy is not great at times. The aim is more to show how such hierarchical information can be presented.** 

Select a trial to explore the hierarchical structure of entities, codes, and categories related to that trial in a detailed sunburst chart.
""")

# Dropdown to select NCTID
nctid_selected = st.selectbox('Select or Enter NCTID', expanded_df['NCTID'].unique())

# Filter dataframe based on selected NCTID
df_filtered = expanded_df[expanded_df['NCTID'] == nctid_selected]

col1, col2 = st.columns((1,3))  # Adjust the ratio as needed for your layout

# Column 1 for trial details
with col1:
    st.subheader("Trial Details")
    if nctid_selected:
        trial_details = criteria_df[criteria_df['nct_id'] == nctid_selected]
        if not trial_details.empty:
            st.markdown("**Brief Title:**")
            st.write(trial_details['brief_title'].values[0])
            st.markdown("**Eligibility Criteria:**")
            st.write(trial_details['criteria'].values[0])  # Assuming single match for NCTID
        else:
            st.write("No details available for the selected NCTID.")

# Generate and display sunburst plot for the selected NCTID
if not df_filtered.empty:
    # Column 2 for the sunburst chart
        with col2:
            st.subheader("Sunburst Chart")
            fig = px.sunburst(df_filtered, path=['NCTID', 'ENTITY', 'STY', 'SAB', 'CODE', 'STR'], 
                            title="Clinical Trial Medical Concept Structure",
                            width=600, height=600,
                            color_discrete_sequence=px.colors.qualitative.Antique)
            
            # Customize layout
            fig.update_layout(margin=dict(t=50, l=0, r=0, b=50),
                            paper_bgcolor="black",
                            title_text=f"Clinical Trial {nctid_selected} Medical Concept Structure",
                            title_font=dict(size=25),
                            title_x=0.27,
                            font=dict(family="Arial, sans-serif", size=14, color="RebeccaPurple"))
            
            st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data available for the selected NCTID.")
