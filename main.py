import streamlit as st
import requests
from bs4 import BeautifulSoup

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
            # ------- STEP 1: Login Form Data -------
            login_url = "https://samvidha.iare.ac.in/login"
            payload = {
                'username': username,
                'password': password,
                # Add other hidden CSRF/form fields if present in the HTML inspection!
            }
            login = session.post(login_url, data=payload, timeout=15)
            
            # ------- STEP 2: Access Attendance Page -------
            attendance_url = "https://samvidha.iare.ac.in/home?action=stud_att_STD"
            att_page = session.get(attendance_url, timeout=15)
            soup = BeautifulSoup(att_page.text, "html.parser")
            
            # ------- STEP 3: Parse Table -------
            table = soup.find('table')
            conducted, attended = 0, 0
            subjects = []
            for row in table.find_all("tr")[2:]:
                cols = row.find_all('td')
                if len(cols) > 6:
                    subject = cols[2].text.strip()
                    c = int(cols[5].text.strip())
                    a = int(cols[6].text.strip())
                    p = float(cols[7].text.strip())
                    conducted += c
                    attended += a
                    subjects.append({'Subject': subject, 'Conducted': c, 'Attended': a, 'Attendance %': p})

            overall = (attended / conducted) * 100 if conducted else 0

            st.success(f"Your overall attendance is **{overall:.2f}%**")
            st.subheader("Subject-wise Attendance")
            st.table(subjects)

        except Exception as e:
            st.error(f"Error: {str(e)} - You may need to adapt field names, handle captchas, or check if portal structure changed!")

else:
    st.info("Please enter your username and password to begin.")
