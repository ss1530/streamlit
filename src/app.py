import streamlit as st

# Page Configuration already set in your provided code
st.set_page_config(page_title="Home Page", page_icon="⚕️")
# Main title
st.title("Welcome to the Veterinary Management System")

# Introduction text
st.write(
    """
## About This Application

Welcome to the Veterinary Management System, designed to streamline the management of animal healthcare data. 
This application provides tools to:
- **Monitor** patient consultations.
- **Track** health records across different species.
- **Analyze** treatment outcomes.
- **Search and Filter** data to find relevant consultation histories and trends.

Whether you're a veterinarian, a clinic staff member, or an administrator, this system is tailored to help you 
manage your operations more effectively.
"""
)

# Video or additional graphics (optional)
# st.video('path_to_intro_video.mp4')

# How to use the system
st.write(
    """
## How to Use This System

1. **Navigate** through the sidebar to access different sections of the application.
2. **Dashboards** provide visual summaries of the data.
3. **Search features** allow detailed exploration of the consultation history and records.
4. **Data Upload** sections for entering new records securely and efficiently.

Feel free to explore the various features designed to assist you in managing your veterinary practice.
"""
)

# Contact or support section
st.write(
    """
## Need Help?

For support, please contact us:
- Email: [support@veterinarysystem.com](mailto:support@veterinarysystem.com)
- Phone: +1 234 567 8900
- Visit our [Help Center](https://www.veterinarysystemhelp.com)
"""
)

# Use this section for any additional information or links
st.info(
    "This system is developed with the aim of enhancing veterinary care services and operational efficiency. Thank you for choosing us!"
)
