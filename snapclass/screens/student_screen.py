import streamlit as st
from ui.base_layout import style_base_dashboard, style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_login
from PIL import Image
import numpy as np
import time

from src.pipelines.face_pipeline import predict_attendence,get_face_embeddings,train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students,create_student,get_student_subject,get_student_attendence,unenroll_student_to_subject
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
  student_data=st.session_state.student_data
  student_id=student_data['student_id']
  c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')

  with c1:
    header_dashboard()
  with c2:
    if st.button("Logout",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
      st.session_state['is_logged_in']=False
      del st.session_state.student_data
      st.rerun()
  st.space()

  c1,c2=st.columns(2)
  with c1:
    st.header('Your Enrolled Subjects')
  with c2:
    if st.button('Enroll in subject', type='primary',width='stretch'):
      enroll_dialog()
  

  st.divider()


  with st.spinner('Loading your enrolled subjects...'):
    subjects=get_student_subject(student_id)
    logs=get_student_attendence(student_id)
  
  stats_map={}

  for log in logs:
    sub = log['subjects']
    sid = sub['subject_id'] if isinstance(sub, dict) else sub

    if sid not in stats_map:
        stats_map[sid] = {
            "total": 0,
            "attendence": 0
        }
    stats_map[sid]['total'] += 1
    stats_map[sid]['attendence'] += 1


  cols=st.columns(2)
  for i,sub_node in enumerate(subjects):
    sub=sub_node['subjects']
    sid=sub['subject_id']


    stats=stats_map.get(sid,{"total":0,  "attendence":0})
    def uneroll_button():
      if st.button("Unenroll from this course",type='tertiary',width='stretch',icon=':material/delete_forever:'):
        unenroll_student_to_subject(student_id,sid)

    with cols[i%2]:
          subject_card(
            name=sub['name'],
            code=sub['subject_code'],
            section=sub['section'],
            stats=[
              ('📝','Total',stats['total']),
              ('✅','Attended',stats['attendence'])
            ],
            footer_callback=uneroll_button
          )
  
  footer_login()

  
  




def student_screen():
  style_base_dashboard()
  style_base_layout()

  if "student_data" in st.session_state:
    student_dashboard()
    return
  c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')

  with c1:
    header_dashboard()
  with c2:
    if st.button("Go Back to home",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
      st.session_state['login_type']=None
      st.rerun()

  st.header("Login using FaceID",text_alignment='center')
  st.space()
  st.space()
  show_registration=False

  photo_source=st.camera_input("Position your face in the center")
  if photo_source:
    img=np.array(Image.open(photo_source))

    with st.spinner("AI is scanning.."):
      detected,all_ids,num_faces=predict_attendence(img)

      if num_faces==0:
        st.warning('Face not Found!')
      elif num_faces>1:
        st.warning('Multiple faces found')

      else:
        if detected:
          student_id=list(detected.keys())[0]
          all_students=get_all_students()
          student=next((s for s in all_students if s['student_id']==student_id),None)

          if student:
            st.session_state.is_logged_in=True
            st.session_state.user_role='student'
            st.session_state.student_data=student
            st.toast(f"Welcome Back {student['name']}")
            time.sleep(1)
            st.rerun()

        else:
          st.info('Face not recognized You might be a new student!')
          show_registration=True

  if show_registration:
    with st.container(border=True):
      st.header('Register new profile')
      new_name=st.text_input("Enter you name", placeholder="E.g. Saurav Verma")

      st.subheader("Optional: Voice Enrollment")
      st.info("Enroll you for voice only attendence")


      audio_data=None

      try:
        audio_data=st.audio_input('Record a short phrase like I am present, My name is akash.')
      except Exception:
        st.error('Audio data failed')

      
      if st.button('Create Account', type='primary'):
        if new_name:
          with st.spinner('Creating Profile...'):
            img=np.array(Image.open(photo_source))
            encodings=get_face_embeddings(img)
            if encodings:
              face_emb=encodings[0].tolist()

              voice_emb=None 
              if audio_data:
                voice_emb=get_voice_embedding(audio_data.read())

              response_data=create_student(new_name,face_embedding=face_emb,voice_embedding=voice_emb)

              if response_data:
                train_classifier()
                st.session_state.is_logged_in=True
                st.session_state.user_role='student'
                st.session_state.student_data=response_data[0]
                st.toast(f"Profile crated ! Hi {new_name}!")
                time.sleep(1)
                st.rerun()
            else:
              st.error("Could'nt capture your facial features for registration")
        else:
          st.warning("Plaese enter yourname!")





   


  footer_login()