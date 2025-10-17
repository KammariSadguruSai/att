import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("IARE Attendance Percentage Calculator")

with st.form("login"):
    st.write("This demo does not do real login, you must provide raw attendance page HTML copy-paste (see below).")
    html = st.text_area("Paste your attendance HTML here")
    submitted = st.form_submit_button("Calculate Attendance")

if submitted and html:
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")[3:]  # Skips top 3 header rows
    subjects = []
    conducted = attended = 0
    for row in rows:
        cols = [x.get_text(strip=True) for x in row.find_all("td")]
        if len(cols) >= 9 and cols[0].isdigit():
            subject = cols[2]
            c = int(cols[5])
            a = int(cols[6])
            conducted += c
            attended += a
            subjects.append({'Subject': subject, 'Conducted': c, 'Attended': a, 'Attendance %': cols[7]})
    overall = (attended / conducted) * 100 if conducted else 0
    st.success(f"Your overall attendance is **{overall:.2f}%**")
    st.subheader("Subject-wise Attendance")
    st.table(subjects)
