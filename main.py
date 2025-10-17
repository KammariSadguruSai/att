import streamlit as st
import requests
import re

st.set_page_config(page_title="IARE Attendance Calculator", page_icon="📋")
st.title("IARE Attendance Percentage Calculator")
st.write("Enter your IARE credentials to fetch and calculate your attendance.")

with st.form("login_form"):
    username = st.text_input("IARE Username")
    password = st.text_input("IARE Password", type="password")
    submitted = st.form_submit_button("Calculate Attendance")

if submitted and username and password:
    with requests.Session() as session:
        try:
            login_url = "https://samvidha.iare.ac.in/login"
            attendance_url = "https://samvidha.iare.ac.in/home?action=stud_att_STD"
            payload = {
                'username': username,
                'password': password,
            }
            session.post(login_url, data=payload, timeout=15)
            att_page = session.get(attendance_url, timeout=15)
            content = att_page.text

            # Extract attendance lines using regex
            lines = re.findall(r"\| \d+ \| [^\n]+\|", content)
            subjects = []
            conducted = attended = 0

            for line in lines:
                # Split by '|', strip spaces
                parts = [p.strip() for p in line.split('|')]
                # S.No | Code | Name | Type | Category | Conducted | Attended | % | Status
                subject = parts[3]
                c = int(parts[6])
                a = int(parts[7])
                p = float(parts[8])
                conducted += c
                attended += a
                subjects.append({'Subject': subject, 'Conducted': c, 'Attended': a, 'Attendance %': p})

            overall = (attended / conducted) * 100 if conducted else 0
            st.success(f"Your overall attendance is **{overall:.2f}%**")
            st.subheader("Subject-wise Attendance")
            st.table(subjects)

        except Exception as e:
            st.error(
                "Error: Could not parse attendance. "
                "This portal may use dynamic JS or captcha, or require Selenium. "
                "If scraping fails, run Selenium code locally instead. "
                f"Details: {str(e)}"
            )

else:
    st.info("Please enter your username and password to begin.")
