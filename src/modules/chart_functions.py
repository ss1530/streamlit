import plotly.express as px
import pandas as pd
import streamlit as st

def create_mpc_bar_chart(dataframe, title):
    """
    Creates a bar chart of SAVSNET_MPC counts with hover effects and improved visualization features.

    Args:
        dataframe (pandas.DataFrame): The DataFrame containing the data.
        title (str): The title for the chart.
    """
    # Check if 'SAVSNET MPC' column exists in the dataframe
    if "SAVSNET MPC" not in dataframe.columns:
        raise ValueError("The dataframe does not contain the 'SAVSNET MPC' column.")

    mpc_counts = dataframe["SAVSNET MPC"].value_counts()

    # Get the index of the maximum count
    max_mpc = mpc_counts.idxmax()
    max_count = mpc_counts.max()

    fig = px.bar(
        mpc_counts,
        x=mpc_counts.index,
        y=mpc_counts.values,
        title=title,
        labels={"x": "SAVSNET_MPC", "y": "Count"},
        color=mpc_counts.index,  # Assign colors based on the index
        color_discrete_sequence=px.colors.qualitative.Pastel,  # Choose a color palette
    )
    fig.update_layout(
        font=dict(
            size=16, family="Courier New, monospace"
        ),  # Adjust the overall font size and family
        title_font_size=24,  # Increase the title font size
        height=600,  # Set the height of the figure
        legend=dict(
            title_font_size=16,  # Set font size for the legend title
            font_size=14,  # Set font size for the legend items
        ),
    )
    # Adjust axes label sizes separately if needed
    fig.update_xaxes(tickfont=dict(size=14))
    fig.update_yaxes(tickfont=dict(size=14))

    # Print the significant values in red and bold below the plot
    st.markdown(f"<p style='color:red; font-weight:bold;'>Most frequent SAVSNET MPC: {max_mpc}, Count: {max_count}</p>", unsafe_allow_html=True)
    
    return fig
    
def plot_consultation_heatmap(
    df, date_column="Consult_date", title="Consultation Frequency by Day and Time"
):
    """
    Generates a heatmap showing the frequency of consultations by day of the week and time of day.

    Args:
        df (pandas.DataFrame): The DataFrame containing the consultation data.
        date_column (str): The name of the column containing the consultation date.
        title (str): The title for the heatmap.

    Returns:
        plotly.graph_objects.Figure: The heatmap plot.
    """
    # Ensure 'Consult_date' is a datetime type and extract day and hour
    if date_column not in df.columns:
        raise KeyError(f"Column '{date_column}' not found in DataFrame.")

    df[date_column] = pd.to_datetime(df[date_column])
    df["Day"] = df[date_column].dt.day_name()
    df["Hour"] = df[date_column].dt.hour

    # Filter hours between 8 AM and 8 PM
    df_filtered = df[(df["Hour"] >= 8) & (df["Hour"] <= 20)]

    # Convert hour to AM/PM format and sort by day of the week
    df_filtered["Hour"] = df_filtered["Hour"].apply(
        lambda x: (
            "12 PM"
            if x == 12
            else "12 AM" if x == 0 else f"{x % 12} {'AM' if x < 12 else 'PM'}"
        )
    )
    df_filtered["Hour"] = pd.Categorical(
        df_filtered["Hour"],
        categories=[
            "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
            "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", 
            "7 PM", "8 PM"
        ],
        ordered=True,
    )
    df_filtered["Day"] = pd.Categorical(
        df_filtered["Day"],
        categories=[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
        ordered=True,
    )
    df_filtered = df_filtered.sort_values(by=["Day", "Hour"])

    # Group by day and hour to count consultations
    heatmap_data = (
        df_filtered.groupby(["Day", "Hour"]).size().reset_index(name="Counts")
    )

    # Get the index of the maximum count
    max_count_index = heatmap_data["Counts"].idxmax()
    max_count_day = heatmap_data.loc[max_count_index, "Day"]
    max_count_hour = heatmap_data.loc[max_count_index, "Hour"]

    # Generate the heatmap
    fig = px.imshow(
        heatmap_data.pivot(index="Day", columns="Hour", values="Counts").fillna(0),
        labels=dict(x="Hour of Day", y="Day of Week", color="Consultation Count"),
        aspect="auto",
        title=title,
        color_continuous_scale="Rainbow",  # Change color scale to rainbow
    )
    fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Day of Week")

    # Print the significant values in red and bold below the plot
    st.markdown(f"<p style='color:red; font-weight:bold;'>Highest patient count observed at {max_count_hour} on {max_count_day}</p>", unsafe_allow_html=True)

    return fig


def plot_consultation_frequency(df, title="Consultation Frequency Over Time"):
    """
    Generates a time-series plot showing the frequency of consultations over time.

    Args:
        df (pandas.DataFrame): The DataFrame containing the consultation data.
        title (str): The title for the chart.

    Returns:
        plotly.graph_objects.Figure: The time-series plot.
    """
    # Create a copy of the DataFrame to avoid modifying the original DataFrame
    df_copy = df.copy()

    # Ensure 'Consult_date' is a datetime type
    df_copy["Consult_date"] = pd.to_datetime(df_copy["Consult_date"])
    df_copy.set_index("Consult_date", inplace=True)

    # Resample and count consultations per quarter
    quarterly_counts = df_copy.resample("QE").size().reset_index(name="Counts")

    # Get the index of the maximum count
    max_count_index = quarterly_counts["Counts"].idxmax()
    max_count_date = quarterly_counts.loc[max_count_index, "Consult_date"]

    # Generate the plot
    fig = px.line(quarterly_counts, x="Consult_date", y="Counts", title=title)
    fig.update_layout(xaxis_title="Date", yaxis_title="Number of Consultations")

    # Print the significant values in red and bold below the plot
    st.markdown(f"<p style='color:red; font-weight:bold;'>Highest consultation count observed on {max_count_date}</p>", unsafe_allow_html=True)

    return fig