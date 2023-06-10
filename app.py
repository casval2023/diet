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
height = st.number_input('Height (cm)', min_value=120, max_value=250, step=1)
weight = st.number_input('Weight (kg)', min_value=30, max_value=200, step=1)
body_fat = st.number_input('Body Fat (%)', min_value=2.0, max_value=50.0, step=1.0)
age = st.number_input('Age', min_value=10, max_value=120, step=1)
gender = st.selectbox('Gender', ['Male', 'Female'])

# タスクの設定
st.subheader('今日のタスク')
tasks = st.text_area('今日のタスクを入力してください')
st.write('例：１日1500kcal以内（基礎代謝量＋200～300kcal目安）、１日１万歩達成、動画講義１章分視聴、復習問題１章分チャレンジ、筋トレメニュー')
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
