import streamlit as st
import pandas as pd
from modules.table_functions import prepare_and_display_consult_data
from modules.utility_functions import to_pascal_case, get_abbreviations_dict

# Set page configuration
st.set_page_config(page_title="Consultation History", layout="wide")

# Load abbreviations dictionary from JSON
abbreviations = get_abbreviations_dict("data/raw/commonly_used_terms.json")

# Prepare unique consultation types
consult_types_path = "data/cleaned/"
all_consult_types = pd.concat(
    [
        pd.read_csv(f"{consult_types_path}cats_consultations.csv")["SAVSNET MPC"],
        pd.read_csv(f"{consult_types_path}dogs_consultations.csv")["SAVSNET MPC"],
        pd.read_csv(f"{consult_types_path}other_species_consultations.csv")[
            "SAVSNET MPC"
        ],
    ]
).unique()
all_consult_types = pd.Series(all_consult_types).map(to_pascal_case).unique()

# Page title
st.title("Consultation History")

# Define tab selection based on user interaction
tab_selection = st.selectbox("Select Species", ["Cats", "Dogs", "Other Species"])

# Determine file path based on selection
selected_file_path = (
    f"{consult_types_path}{tab_selection.lower().replace(' ', '_')}_consultations.csv"
)

# Load data only for the selected species
df = pd.read_csv(selected_file_path)

# Apply consultation type filter
selected_types = st.multiselect(
    "Filter by Consultation Type:",
    options=all_consult_types,
    default=all_consult_types,
    key=f"{tab_selection}_consult_type",
)

# Filter data by selected types
filtered_data = df[df["SAVSNET MPC"].map(to_pascal_case).isin(selected_types)]

# Pagination setup
items_per_page = 10  # Set the number of items you want per page
max_pages = len(filtered_data) // items_per_page + (
    1 if len(filtered_data) % items_per_page > 0 else 0
)
current_page = st.slider("Select Page", 1, max_pages, 1)  # Slider for page selection
start_index = (
    current_page - 1
) * items_per_page  # Calculate the starting index of the current page
end_index = (
    start_index + items_per_page
)  # Calculate the ending index of the current page
page_data = filtered_data.iloc[
    start_index:end_index
]  # Slice the DataFrame for the current page

# Display the consultation data for the current page
prepare_and_display_consult_data(page_data, abbreviations=abbreviations)
