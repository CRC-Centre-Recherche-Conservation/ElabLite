import streamlit as st

from utils.menu import menu

# APP
st.set_page_config(page_title="ElabLite", )
st.title("ElabLite")
st.write(
    "Welcome to ElabLite like metadata generator! This tool helps you generate metadata for use in your elabFTW instance with easy templates.")

# init step metadata
if "step_metadata" not in st.session_state:
    st.session_state["step_metadata"] = "step_metadata_base"

#SIDEBAR
menu()
