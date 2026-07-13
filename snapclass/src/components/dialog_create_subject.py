import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
  st.write("Enter the detalis of subject")
  sub_id = st.text_input("Subject code", placeholder='CS101')
  sub_name = st.text_input("Subject name", placeholder='Introduction to computer science')
  sub_section = st.text_input("Section", placeholder='A')

  if st.button("Create subject Now", type='primary', width='stretch'):
    if sub_id and sub_name and sub_section:
      try:
        create_subject(sub_id, sub_name, teacher_id, sub_section)
        st.toast("Subject Created Successfully!")
        st.rerun()
      except Exception as e:
        st.error(f"Error: {str(e)}")
    else:
      st.warning("Plaese fill all the fields")
