import streamlit as st
import pandas as pd
import json
import uuid
from io import BytesIO

from database import *
from email_service import *

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="InformAI Forms",
    layout="wide"
)

init_db()

# -------------------------
# SESSION STATE
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------
# TITLE
# -------------------------

st.title("📄 InformAI Forms")
st.caption("Excel → Dynamic Form → Email → Responses")

# -------------------------
# LOGIN / REGISTER
# -------------------------

if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(
        [
            "Login",
            "Register"
        ]
    )

    with tab1:

        st.subheader("Login")

        login_email = st.text_input(
            "Email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            user = login_user(
                login_email,
                login_password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user = dict(user)

                st.success("Login Successful")
                st.rerun()

            else:
                st.error("Invalid Credentials")

    with tab2:

        st.subheader("Register")

        username = st.text_input(
            "Username"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Create Account"):

            try:

                create_user(
                    username,
                    email,
                    password
                )

                st.success(
                    "Account Created Successfully"
                )

            except Exception as e:
                st.error(str(e))

    st.stop()
