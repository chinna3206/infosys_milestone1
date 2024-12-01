import streamlit as st

# Title
st.title("Claim your Free API Key")

# Description
st.write(
    "Claim your free key for the Alpha Vantage Stock API with lifetime access. "
    "We highly recommend that you use a legitimate email address - this is the primary way "
    "we will contact you for feature announcements or troubleshooting (e.g., if you lose your API key). "
    "By acquiring and using an Alpha Vantage API key, you agree to our Terms of Service and Privacy Policy."
)

# Form to collect user details
with st.form("api_key_form"):
    user_type = st.selectbox(
        "Which of the following best describes you?", 
        ["Investor", "Developer", "Researcher", "Other"]
    )
    organization = st.text_input("Organization (e.g., company, university, etc.)")
    email = st.text_input("Email")

    # Submit button
    submitted = st.form_submit_button("Get Free API Key")

    if submitted:
        if not email or "@" not in email:
            st.error("Please enter a valid email address.")
        else:
            st.success(f"API key request submitted successfully for {email}!")

# Sidebar (optional)
st.sidebar.title("Alpha Vantage Support")
st.sidebar.write("Claim your API key")
st.sidebar.write("Support")
