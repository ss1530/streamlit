from typing import Counter
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.utility_functions import pascal_to_space_pascal
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Path to your cleaned data
DATA_DIR = "data/cleaned/"


# Function to load a specific CSV file
def load_data(sheet_name):
    filename = f"{DATA_DIR}{''.join(sheet_name.split())}.csv"
    return pd.read_csv(filename)


# Function to plot time-series analysis grouped by decade
def plot_time_series(df, date_column, title):
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Group data by year
    df['Year'] = df[date_column].dt.year
    
    # Count number of products per year
    year_data = df.groupby('Year').size().reset_index(name='Count')
    
    # Group data by decade
    df['Decade'] = (df['Year'] // 10) * 10
    
    # Count number of products per decade
    decade_data = df.groupby('Decade').size().reset_index(name='Decade_Count')
    
    # Create a bar chart for the number of products per year
    bar_fig = px.bar(year_data, x='Year', y='Count', labels={'Year': 'Year', 'Count': 'Number of Products'})
    
    # Create a line plot for the number of products per decade
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(x=decade_data['Decade'], y=decade_data['Decade_Count'],
                                   mode='lines+markers', name='Decade Count', line=dict(color='blue')))
    
    # Set the same y-axis range for both plots
    y_max = max(year_data['Count'].max(), decade_data['Decade_Count'].max())
    bar_fig.update_yaxes(range=[0, y_max])
    line_fig.update_yaxes(range=[0, y_max])
    
    # Combine both plots
    bar_fig.update_traces(marker_color='rgba(50, 171, 96, 0.7)', marker_line_color='rgba(50, 171, 96, 1)', 
                          marker_line_width=1.5, opacity=0.7)
    bar_fig.add_trace(line_fig.data[0])
    
    # Set layout properties
    bar_fig.update_layout(title=title, xaxis_title='Year', yaxis_title='Number of Products', 
                          legend_title_text='Legend', barmode='overlay', bargap=0.05)
    
    return bar_fig


# Function to perform text analysis and plot word cloud as image
def plot_word_cloud(df, column):
    text = " ".join(df[column].dropna().values)
    wordcloud = WordCloud(width=800, height=400, colormap="viridis").generate(text)

    # Generate the word cloud image
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    # Display the word cloud image using Streamlit
    st.image(wordcloud.to_array(), use_column_width=True)


# Tab names
tabs = [
    "Current Authorised Products",
    "Suspended Products",
    "Expired Products",
    "Homeopathic Products",
]

# Tab selection
selected_sheet = st.selectbox("Product Inventory", tabs)
# Load the data for the selected tab
df = load_data(selected_sheet)

# Controlled Drug filter logic with unique key
# Controlled Drug filter logic with conditional display
if selected_sheet != "Expired Products":
    controlled_drug_options = ["2", "3", "4", "5", "N"]
    selected_drugs = st.multiselect(
        "Filter by Controlled Drug", 
        controlled_drug_options, 
        key=f"controlled_drug_{selected_sheet}"
    )

    if selected_drugs:
        df = df[df["ControlledDrug"].isin(selected_drugs)]
else:  # Explicitly disable/hide for Expired Products
    st.write("**Controlled Drug filter not applicable for expired products.")
        
# Filter based on ControlledDrug flag
controlled_drug_options = ["2", "3", "4", "5", "N"]
selected_drugs = st.multiselect("Filter by Controlled Drug", controlled_drug_options)

# Add a collapsible section for more filters
more_filters_expander = st.expander("More Filters", expanded=False)
with more_filters_expander:
    # Add a search bar to filter by target species
    search_species = st.text_input("Search by Target Species")

    # Filter DataFrame based on search input
    if search_species:
        df = df[df["TargetSpecies"].str.contains(search_species, case=False, na=False)]

    # Add a search bar to filter by Active Substances
    search_substances = st.text_input("Search by Active Substances")

    # Filter DataFrame based on search input
    if search_substances:
        df = df[
            df["ActiveSubstances"].str.contains(search_substances, case=False, na=False)
        ]

    # Add a search bar to filter by Therapeutic Group
    search_th_grp = st.text_input("Search by Therapeutic Group")

    # Filter DataFrame based on search input
    if search_th_grp:
        df = df[
            df["TherapeuticGroup"].str.contains(search_th_grp, case=False, na=False)
        ]

# Display time-series analysis
if "DateOfIssue" in df.columns:
    st.plotly_chart(plot_time_series(df, "DateOfIssue", "Trend Analysis Over Time"))

# Display word cloud for Active Substances
if "ActiveSubstances" in df.columns:
    st.write("Word Cloud for Active Substances")
    plot_word_cloud(df, "ActiveSubstances")


# Define number of rows and columns for each page
rows_per_page = 6
columns_per_page = 1

# Calculate total number of pages
total_pages = -(-len(df) // (rows_per_page * columns_per_page))  # Round up division

# Get the current page number from the URL query parameters, default to page 1
page_number = st.query_params.get("page_number", 1)
page_number = int(page_number)

# Calculate start and end index for the current page
start_index = (page_number - 1) * rows_per_page * columns_per_page
end_index = min(start_index + rows_per_page * columns_per_page, len(df))

# Subset the DataFrame for the current page
df_page = df.iloc[start_index:end_index]

# Reset page number when a different tab is selected
if st.session_state.get("selected_sheet") != selected_sheet:
    page_number = 1

# Save selected tab to session state
st.session_state.selected_sheet = selected_sheet

# Display the number of results available
st.write(f"{len(df)} results available")

# Display the information in a grid of cards
columns = st.columns(columns_per_page)

# Columns to display based on the selected tab
if selected_sheet == "Expired Products":
    columns_to_display = [
        "VMDProductNo",
        "MAHolder",
        "VMNo",
        "DateOfExpiration",
        "AuthorisationRoute",
        "Territory",
        "ActiveSubstances",
    ]
else:
    columns_to_display = [
        "VMDProductNo",
        "MAHolder",
        "VMNo",
        "ControlledDrug",
        "ActiveSubstances",
        "TargetSpecies",
        "DistributionCategory",
        "PharmaceuticalForm",
        "TherapeuticGroup",
    ]

# Pagination controls at the top of the page
st.write("")  # Add space for better appearance
st.write(f"Page {page_number} of {total_pages}")
previous_page, next_page = st.columns(2)
if page_number > 1:
    if previous_page.button("Previous"):
        page_number -= 1
if page_number < total_pages:
    if next_page.button("Next"):
        page_number += 1

# Set URL query parameters for pagination
st.query_params["page_number"] = page_number

# Loop over each column
for i, column in enumerate(columns):
    # Display cards in this column
    for j in range(rows_per_page):
        index = i * rows_per_page + j
        if index < len(df_page):
            # Display product name above the card
            with column:
                # Apply different styling to the product name
                st.markdown(
                    f'<h3 style="color: #CA9CE1; font-size: 1.5em;">{df_page["Name"].iloc[index]}</h3>',
                    unsafe_allow_html=True,
                )

                # Display product details in two columns
                col1, col2 = st.columns(2)
                product_info = (
                    df_page[columns_to_display[1:]].iloc[index].to_dict()
                )  # Exclude product name from body
                for key, value in product_info.items():
                    # Apply styling to keys
                    col1.markdown(
                        f'<span style="color: #F2BEFC;">{pascal_to_space_pascal(key)}:</span>',
                        unsafe_allow_html=True,
                    )
                    # Apply styling to values
                    col2.markdown(
                        f'<span style="font-family: Roboto, sans-serif;">{value}</span>',
                        unsafe_allow_html=True,
                    )

                # Close product details container
                st.markdown("</div>", unsafe_allow_html=True)

                # Add horizontal separator between products
                st.markdown('<hr style="margin: 20px 0;">', unsafe_allow_html=True)
