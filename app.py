import streamlit as st
import pandas as pd
import boto3
import datetime

# AWSのS3の設定
s3 = boto3.client('s3', 
                  region_name="ap-northeast-1",
                  aws_access_key_id='AKIAV27ZCYO3NIGWWEEZ',
                  aws_secret_access_key='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')

bucket_name = 'skkeng'

def write_to_s3(df, filename):
    csv_buffer = df.to_csv(index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket_name, filename).put(Body=csv_buffer)

# StreamlitのUIの設定
st.title('Health & Fitness Tracker')

# ユーザー情報の入力
st.subheader('User Information')
height = st.number_input('Height (cm)', min_value=100.0, max_value=250.0)
weight = st.number_input('Weight (kg)', min_value=30.0, max_value=200.0)
body_fat = st.number_input('Body Fat (%)', min_value=5.0, max_value=50.0)
age = st.number_input('Age', min_value=10, max_value=100)
gender = st.selectbox('Gender', ['Male', 'Female'])

# タスクの設定
st.subheader('Today\'s Tasks')
tasks = ['Consume less than 1500 kcal',
         'Walk 10,000 steps',
         'Watch 1 chapter of video lecture',
         'Challenge 1 chapter of review questions',
         'Workout']
task_status = [st.checkbox(task) for task in tasks]

# 入力データの保存
if st.button('Submit'):
    data = {'Height': height, 'Weight': weight, 'Body Fat': body_fat,
            'Age': age, 'Gender': gender, 
            'Tasks': tasks, 'Task Status': task_status,
            'Date': datetime.date.today()}
    df = pd.DataFrame(data, index=[0])
    
    # データをS3に保存
    write_to_s3(df, f'data_{datetime.date.today()}.csv')

    st.success('Data submitted successfully.')
