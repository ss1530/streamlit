import streamlit as st
import pandas as pd
from modules import chart_functions as cf
from modules import table_functions as tf

# Data Loading (adjust paths if needed)
df_cats = pd.read_csv("data/cleaned/cats_consultations.csv")
df_dogs = pd.read_csv("data/cleaned/dogs_consultations.csv")
df_other = pd.read_csv("data/cleaned/other_species_consultations.csv")

st.set_page_config(layout="wide")

# Inject custom CSS to improve tab readability
st.markdown(
    """
<style>
.css-1lcbmhc {
    padding: 1rem 1rem;  /* Adjust padding around the tab texts */
}
.css-1lcbmhc e1tzin5v3 {
    font-size: 16px;  /* Increase the font size */
    font-weight: bold;  /* Make the font bold */
}
.stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:2rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.title("Veterinary Management Dashboard")

# Main Tabs for Species
cats_tab, dogs_tab, other_tab = st.tabs(["Cats", "Dogs", "Other Species"])

with cats_tab:
        # Add filters for Year and Consultation Type
    df_cats['Consult_date'] = pd.to_datetime(df_cats['Consult_date'])
    unique_years = df_cats['Consult_date'].dt.year.unique().tolist()
    selected_year = st.selectbox('Select Year', options=unique_years, index=unique_years.index(2018))

    consultation_types = df_cats['SAVSNET MPC'].unique().tolist()
    selected_consultation_types = st.multiselect('Select Consultation Types', options=consultation_types, default=['vaccination'])

    # Filter the dataframe based on the selected filters
    filtered_df_cats = df_cats[(df_cats['Consult_date'].dt.year == selected_year) & (df_cats['SAVSNET MPC'].isin(selected_consultation_types))]

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.title("Filtered Consultation Counts")
        cats_table = tf.create_mpc_counts_table(filtered_df_cats)
        st.table(cats_table)

    with row1_col2:
        st.title("Filtered Consultation Distribution")
        cat_chart = cf.create_mpc_bar_chart(filtered_df_cats, f"Cats: Consultation Types in {selected_year}")
        st.plotly_chart(cat_chart, use_container_width=True)
        
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.title("Consultation Frequency Over Time")
        time_series_fig = cf.plot_consultation_frequency(filtered_df_cats, "Consultation Frequency Over Time")
        st.plotly_chart(time_series_fig, use_container_width=True)

    with row2_col2:
        st.title("Consultation Heatmap")
        heatmap_fig_cats = cf.plot_consultation_heatmap(filtered_df_cats,"Consult_date", "Consultation Frequency by Day and Time")
        st.plotly_chart(heatmap_fig_cats, use_container_width=True)

with dogs_tab:
    
    # Add filters for Year and Consultation Type
    df_dogs['Consult_date'] = pd.to_datetime(df_dogs['Consult_date'])
    unique_years = df_dogs['Consult_date'].dt.year.unique().tolist()
    selected_year = st.selectbox('Select Year', options=unique_years, index=unique_years.index(2018))

    consultation_types = df_dogs['SAVSNET MPC'].unique().tolist()
    selected_consultation_types = st.multiselect('Select Consultation Types', options=consultation_types, default=['vaccination'])

    # Filter the dataframe based on the selected filters
    filtered_df_dogs = df_dogs[(df_dogs['Consult_date'].dt.year == selected_year) & (df_dogs['SAVSNET MPC'].isin(selected_consultation_types))]

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.title("Filtered Consultation Counts")
        dogs_table = tf.create_mpc_counts_table(filtered_df_dogs)
        st.table(dogs_table)

    with row1_col2:
        st.title("Filtered Consultation Distribution")
        dog_chart = cf.create_mpc_bar_chart(filtered_df_dogs, f"Dogs: Consultation Types in {selected_year}")
        st.plotly_chart(dog_chart, use_container_width=True)
        
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.title("Consultation Frequency Over Time")
        time_series_fig = cf.plot_consultation_frequency(filtered_df_dogs, "Consultation Frequency Over Time")
        st.plotly_chart(time_series_fig, use_container_width=True)

    with row2_col2:
        st.title("Consultation Heatmap")
        heatmap_fig_dogs = cf.plot_consultation_heatmap(filtered_df_dogs,"Consult_date", "Consultation Frequency by Day and Time")
        st.plotly_chart(heatmap_fig_dogs, use_container_width=True)

with other_tab:
    
    # Add filters for Year and Consultation Type
    df_other['Consult_date'] = pd.to_datetime(df_other['Consult_date'])
    unique_years = df_other['Consult_date'].dt.year.unique().tolist()
    selected_year = st.selectbox('Select Year', options=unique_years, index=unique_years.index(2018))

    consultation_types = df_other['SAVSNET MPC'].unique().tolist()
    selected_consultation_types = st.multiselect('Select Consultation Types', options=consultation_types, default=['vaccination'])

    # Filter the dataframe based on the selected filters
    filtered_df_other = df_other[(df_other['Consult_date'].dt.year == selected_year) & (df_other['SAVSNET MPC'].isin(selected_consultation_types))]

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.title("Filtered Consultation Counts")
        other_table = tf.create_mpc_counts_table(filtered_df_other)
        st.table(other_table)

    with row1_col2:
        st.title("Filtered Consultation Distribution")
        other_chart = cf.create_mpc_bar_chart(filtered_df_other, f"Other Species: Consultation Types in {selected_year}")
        st.plotly_chart(other_chart, use_container_width=True)
        
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.title("Consultation Frequency Over Time")
        time_series_fig = cf.plot_consultation_frequency(filtered_df_other, "Consultation Frequency Over Time")
        st.plotly_chart(time_series_fig, use_container_width=True)

    with row2_col2:
        st.title("Consultation Heatmap")
        heatmap_fig_others = cf.plot_consultation_heatmap(filtered_df_other,"Consult_date", "Consultation Frequency by Day and Time")
        st.plotly_chart(heatmap_fig_others, use_container_width=True)
