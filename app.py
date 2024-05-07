import streamlit as st

# APP
def main():
    st.set_page_config(page_title="ElabLite",)
    st.title("ElabLite")
    st.write(
        "Welcome to ElabLite like metadata generator! This tool helps you generate metadata for use in your elabFTW instance with easy templates.")

if __name__ == "__main__":
    main()