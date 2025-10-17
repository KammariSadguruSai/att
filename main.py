import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="IARE Attendance Calculator", page_icon="📋")
st.title("IARE Attendance Percentage Calculator")
st.write("Enter your IARE credentials to fetch and calculate your attendance.")

with st.form("login_form"):
    username = st.text_input("IARE Username")
    password = st.text_input("IARE Password", type="password")
    submitted = st.form_submit_button("Calculate Attendance")

if submitted and username and password:
    options = Options()
    options.add_argument("--headless")  # no browser popup
    driver = webdriver.Chrome(options=options)

    driver.get("https://samvidha.iare.ac.in/home?action=stud_att_STD")
    time.sleep(2)
    # Find and fill username, password (update/select correct IDs/names below)
    driver.find_element(By.ID, 'username_inputID').send_keys(username)
    driver.find_element(By.ID, 'password_inputID').send_keys(password)
    driver.find_element(By.ID, 'loginButtonID').click()  # Change to actual login button ID
    time.sleep(4)

    # Parse attendance table
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all('tr')[2:]  # Find the attendance rows
    conducted, attended = 0, 0
    subjects = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 6:
            subject = cols[2].text.strip()
            c = int(cols[5].text.strip())
            a = int(cols[6].text.strip())
            p = float(cols[7].text.strip())
            conducted += c
            attended += a
            subjects.append({'name': subject, 'conducted': c, 'attended': a, 'percent': p})
    driver.quit()

    overall = (attended / conducted) * 100 if conducted else 0
    st.success(f"Your exact overall attendance is **{overall:.2f}%**")
    st.subheader("Subject-wise Attendance")
    st.table(subjects)
else:
    st.info("Please enter your username and password to begin.")
