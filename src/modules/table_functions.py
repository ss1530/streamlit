import pandas as pd
import streamlit as st
from .utility_functions import to_pascal_case, annotate_abbreviations


def create_mpc_counts_table(dataframe):
    """
    Calculates SAVSNET MPC counts and generates a styled table with a loading spinner.

    Args:
        dataframe (pandas.DataFrame): The DataFrame containing consultation data.

    Returns:
        pandas.Styler: A styled table showing the count of each SAVSNET MPC type.
    """
    with st.spinner("Fetching data and preparing table..."):
        if "SAVSNET MPC" not in dataframe.columns:
            raise ValueError("The dataframe does not contain the 'SAVSNET MPC' column.")

        # Using value_counts to count occurrences of each type in 'SAVSNET MPC'
        mpc_counts = dataframe["SAVSNET MPC"].value_counts().reset_index()
        mpc_counts.columns = [
            "Consultation Type",
            "Count",
        ]  # Renaming columns for clarity

        # Sort by 'Count' in descending order for better data presentation
        mpc_counts.sort_values("Count", ascending=False, inplace=True)

        # Style the DataFrame
        styled_table = mpc_counts.style.set_properties(
            **{"text-align": "center"}
        ).set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [("font-size", "14pt"), ("text-align", "center")],
                },
                {
                    "selector": "td",
                    "props": [("font-size", "14pt"), ("text-align", "center")],
                },
            ]
        )

    return styled_table


def prepare_and_display_consult_data(df, filter_types=None, abbreviations=None):
    with st.spinner("Processing consultation data..."):
        required_columns = [
            "SAVSNET_consult_id",
            "Narrative",
            "SAVSNET MPC",
            "Consult_date",
        ]
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Missing one or more required columns in the DataFrame")

        df_display = df[required_columns].copy()
        df_display.rename(
            columns={
                "SAVSNET_consult_id": "Patient Consultation ID",
                "Narrative": "Consultation Notes",
                "SAVSNET MPC": "Consultation Type",
                "Consult_date": "Consultation Date",
            },
            inplace=True,
        )

        df_display["Consultation Type"] = df_display["Consultation Type"].apply(to_pascal_case)
        df_display["Consultation Date"] = pd.to_datetime(df_display["Consultation Date"]).dt.strftime("%Y-%m-%d %H:%M:%S")

        if filter_types:
            df_display = df_display[df_display["Consultation Type"].isin(filter_types)]

        if abbreviations:
            df_display["Consultation Notes"] = df_display["Consultation Notes"].apply(
                lambda x: annotate_abbreviations(x, abbreviations)
            )

        # Display each entry as a card
        for _, row in df_display.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.subheader(f"Consultation ID: {row['Patient Consultation ID']}")
                    st.write(f"**Type:** {row['Consultation Type']}")
                    st.write(f"**Date:** {row['Consultation Date']}")
                with col2:
                    # Apply inline styles for justification and line spacing
                    st.markdown(f"<div style='text-align: justify; line-height: 1.6;'><strong>Notes:</strong> {row['Consultation Notes']}</div>", unsafe_allow_html=True)
                st.markdown("---")  # Optional line separator

        return None  # This function does not return anything as it directly renders in Streamlit
