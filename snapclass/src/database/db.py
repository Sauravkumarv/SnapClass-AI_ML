from src.database.config import supabase

import bcrypt


def hash_pass(pwd):
  return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()

def check_pass(pwd,hashed):
  return bcrypt.checkpw(pwd.encode(),hashed.encode())


def check_teacher_exists(username):
  # check for unique username return false when username has already taken
  response=supabase.table("teachers").select("username").eq("username",username).execute()
  return len(response.data)>0


def create_teacher(username,password,name):

  data={"username":username,"password":hash_pass(password),"name":name}
  response=supabase.table("teachers").insert(data).execute()
  return response.data


def teacher_login(username,password):
  response=supabase.table("teachers").select("*").eq("username",username).execute()

  if response.data:
    teacher=response.data[0]
    if check_pass(password,teacher['password']):
      return teacher
  return None

def get_all_students():
  response=supabase.table('students').select("*").execute()
  return response.data

def create_student(new_name,face_embedding=None,voice_embedding=None):
  data={"name":new_name,"face_embedding":face_embedding,"voice_embedding":voice_embedding}
  response=supabase.table('students').insert(data).execute()
  return response.data

def create_subject(subject_code,name,teacher_id,section):
  data={"subject_code":subject_code,"name":name,"teacher_id":teacher_id,"section":section}
  response=supabase.table("subjects").insert(data).execute()
  return response.data

def get_teacher_subjects(teacher_id):
  response=supabase.table("subjects").select("*,subject_students(count),attendence_logs(timestamp)").eq("teacher_id",teacher_id).execute()
  subjects=response.data

  for sub in subjects:
    sub["total_students"]=sub.get("subject_students",[{}])[0].get('count',0) if sub.get('subject_students')else 0
    attendence=sub.get('attendence_logs',[])
    unique_session=len(set(log['timestamp'] for log in attendence))
    sub['total_classes']=unique_session


    sub.pop('subject_student',None)
    sub.pop('attendence_logs',None)
  return subjects


def enroll_student_to_subject(studet_id,subject_id):
  data={'student_id':studet_id,"subject_id":subject_id}
  response=supabase.table('subject_students').insert(data).execute()
  return response.data


def unenroll_student_to_subject(studet_id,subject_id):
  response=supabase.table('subject_students').delete().eq('student_id',studet_id).eq('subject_id',subject_id).execute()
  return response.data

def get_student_subject(studet_id):
  response=supabase.table('subject_students').select('*,subjects(*)').eq('student_id',studet_id).execute()
  return response.data

def get_student_attendence(studet_id):
  response=supabase.table('attendence_logs').select('*,subjects(*)').eq('student_id',studet_id).execute()
  return response.data


def create_attendence(logs):
  response=supabase.table('attendence_logs').insert(logs).execute()
  return response.data


def get_attendence_for_teacher(teacher_id):
  response=supabase.table('attendence_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id',teacher_id).execute()
  return response.data