import streamlit as st
from PIL import Image


@st.dialog("Capture or Upload photos")
def add_photos_dialog():
  st.write('Add Classroom photos to scan for attendence')

  if 'photo_tab' not in st.session_state:
    st.session_state.photo_tab = 'camera'

  t1, t2 = st.columns(2)

  with t1:
    type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
    if st.button('Camera', type=type_camera, width='stretch'):
      st.session_state.photo_tab = 'camera'
      st.rerun()

  with t2:
    type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
    if st.button('upload photos', type=type_upload, width='stretch'):
      st.session_state.photo_tab = 'upload'
      st.rerun()

  if st.session_state.photo_tab == 'camera':
    cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
    if cam_photo:
      try:
        st.session_state.attendence_images.append(Image.open(cam_photo))
        st.toast('Photo Captured')
        st.rerun()
      except Exception:
        st.error('Could not process that photo. Try again.')

  if st.session_state.photo_tab == 'upload':
    uploaded_files = st.file_uploader('Choose image files', type=['jpg', 'png', 'jpeg'], accept_multiple_files=True, key='dialog_upload')

    if uploaded_files:
      try:
        for f in uploaded_files:
          st.session_state.attendence_images.append(Image.open(f))
        st.toast('Photo Uploaded Successfully')
        st.rerun()
      except Exception:
        st.error('Could not process one or more images.')

  st.divider()
  if st.button('Done', type='primary', width='stretch'):
    st.rerun()
