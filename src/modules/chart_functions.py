import plotly.express as px

def create_mpc_bar_chart(dataframe, title):
    """
    Creates a bar chart of SAVSNET_MPC counts with hover effects and improved visualization features.

    Args:
        dataframe (pandas.DataFrame): The DataFrame containing the data.
        title (str): The title for the chart.
    """
    # Check if 'SAVSNET MPC' column exists in the dataframe
    if 'SAVSNET MPC' not in dataframe.columns:
        raise ValueError("The dataframe does not contain the 'SAVSNET MPC' column.")

    mpc_counts = dataframe['SAVSNET MPC'].value_counts()

    fig = px.bar(
        mpc_counts, 
        x=mpc_counts.index, 
        y=mpc_counts.values, 
        title=title,
        labels={"x": "SAVSNET_MPC", "y": "Count"},
        color=mpc_counts.index,  # Assign colors based on the index
        color_discrete_sequence=px.colors.qualitative.Pastel  # Choose a color palette
    )
    fig.update_layout(
        font=dict(size=16, family="Courier New, monospace"),  # Adjust the overall font size and family
        title_font_size=24,  # Increase the title font size
        height=600,  # Set the height of the figure
        legend=dict(
            title_font_size=16,  # Set font size for the legend title
            font_size=14,  # Set font size for the legend items
        )
    )
    # Adjust axes label sizes separately if needed
    fig.update_xaxes(tickfont=dict(size=14))
    fig.update_yaxes(tickfont=dict(size=14))

    return fig
