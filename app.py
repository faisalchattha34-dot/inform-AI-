import streamlit as st
import pandas as pd
import json
import uuid

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

# =====================================================
# LOGIN / REGISTER
# =====================================================

if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---------------- LOGIN ----------------

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

    # ---------------- REGISTER ----------------

    with tab2:

        st.subheader("Register")

        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Create Account"):

            result = create_user(
                username,
                email,
                password
            )

            if result:
                st.success(
                    "Account Created Successfully"
                )
            else:
                st.error(
                    "Email already exists"
                )

    st.stop()

# =====================================================
# DASHBOARD
# =====================================================

user = st.session_state.user

st.sidebar.success(
    f"Welcome {user['username']}"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.user = None

    st.rerun()

st.header("Dashboard")

form_name = st.text_input(
    "Form Name"
)

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.success(
        "Excel Loaded Successfully"
    )

    st.subheader(
        "Detected Columns"
    )

    st.dataframe(
        pd.DataFrame(
            {
                "Columns": df.columns
            }
        )
    )

    columns_data = []

    for col in df.columns:

        values = (
            df[col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        columns_data.append(
            {
                "name": col,
                "values": values[:20]
            }
        )

    if st.button("Save Form"):

        form_id = str(uuid.uuid4())

        save_form(
            form_id=form_id,
            user_id=user["id"],
            form_name=form_name,
            columns_json=json.dumps(
                columns_data
            )
        )

        st.success(
            f"Form Created Successfully: {form_id}"
        )

# =====================================================
# MY FORMS
# =====================================================

st.subheader("My Forms")

forms = get_user_forms(
    user["id"]
)

if forms:

    for form in forms:

        st.info(
            f"{form['form_name']} | ID: {form['id']}"
        )

else:

    st.warning(
        "No forms created yet."
    )
