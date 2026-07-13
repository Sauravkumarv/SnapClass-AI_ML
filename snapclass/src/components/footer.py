import streamlit as st


def footer_home():
   
    st.markdown(
        f"""
        <div style="margin-top: 2rem; display: flex; justify-content: center; items-align: center;">
        <p style="font-weight: bold; color: white;">
                Created with ❤️ Saurav
        </p>

        
        </div>
        """,
        unsafe_allow_html=True,
    )

def footer_login():
    

    st.markdown(
        f"""
        <div style="margin-top: 2rem; display: flex; justify-content: center; items-align: center;">
        <p style="font-weight: bold; color: black;">
                Created with ❤️ Saurav
        </p>

        
        </div>
        """,
        unsafe_allow_html=True,
    )