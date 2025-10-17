import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("IARE Samvidha Attendance Percentage Checker")

# Inputs for login
username = st.text_input("Enter Registration Number / Username")
password = st.text_input("Enter Password", type="password")

if st.button("Fetch My Attendance %"):
    session = requests.Session()
    login_url = "https://samvidha.iare.ac.in/index"
    dashboard_url = "https://samvidha.iare.ac.in/home?action=stud_att_STD"

    # STEP 1: Simulate login (the actual form name/fields may require inspection)
    payload = {
        "username": username,    # Use the actual form field names from portal
        "password": password
    }
    # Sometimes the form field names are different; use browser inspector tools to identify correct names!
    login_resp = session.post(login_url, data=payload, allow_redirects=True)
    if login_resp.ok and "Sign out" in login_resp.text:
        # STEP 2: Fetch attendance page
        resp = session.get(dashboard_url)
        if resp.ok:
            soup = BeautifulSoup(resp.text, "html.parser")
            # Find all rows in the attendance table
            table = soup.find("table")
            rows = table.find_all("tr")[1:] if table else []   # Skipping header
            total_attended, total_conducted = 0, 0
            # Parse table for attended/conducted data
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 7:
                    try:
                        conducted = int(cols[5].get_text())
                        attended = int(cols[6].get_text())
                        total_attended += attended
                        total_conducted += conducted
                    except:
                        continue
            if total_conducted > 0:
                overall_percentage = (total_attended/total_conducted)*100
                st.success(f"Your overall attendance percentage is: {overall_percentage:.2f}%")
            else:
                st.error("Could not parse attendance data.")
        else:
            st.error("Could not fetch attendance page after login.")
    else:
        st.error("Login failed! Please check credentials.")
