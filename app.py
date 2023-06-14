import streamlit as st
import pandas as pd
import boto3
import datetime

# S3
def connect_s3_skkeng():
    s3 = boto3.resource('s3',
                           region_name="ap-northeast-1",
                           aws_access_key_id='AKIAV27ZCYO3NIGWWEEZ',
                           aws_secret_access_key='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'
                       )
    return s3,s3.Bucket('skkeng')
  
def load_data(s3):
    src_obj = s3.Object('skkeng','diet/data.txt')
    body_in = src_obj.get()['Body'].read().decode("utf-8")
    buffer_in = io.StringIO(body_in)
    df_fn = pd.read_csv(buffer_in,header = None, index_col=0,lineterminator='\n')
    df_fn.reset_index(inplace= True)
    return df_fn

def save_data(s3):
    s3.Bucket('skkeng').upload_file(Filename='data.txt', Key='data.txt')
  


# StreamlitのUIの設定
st.title('ダイエット記録アプリ')

# ユーザー情報の入力
st.subheader('ユーザー情報')
height = st.number_input('身長(cm)', min_value=120, max_value=250, step=1)
weight = st.number_input('体重(kg)', min_value=30, max_value=200, step=1)
body_fat = st.number_input('体脂肪率(%)', min_value=2.0, max_value=50.0, step=1.0)
age = st.number_input('年齢', min_value=10, max_value=120, step=1)
gender = st.selectbox('性別', ['男性', '女性'])

# タスクの設定
st.subheader('今日のタスク')
tasks = st.text_area('今日のタスクを入力してください')
st.write('例：１日1500kcal以内（基礎代謝量＋200～300kcal目安）、１日１万歩達成、動画講義１章分視聴、復習問題１章分チャレンジ、筋トレメニュー')
#task_status = [st.checkbox(task) for task in tasks]

# 入力データの保存
if st.button('データ保存'):
    data = {'Height': height, 'Weight': weight, 'Body Fat': body_fat,
            'Age': age, 'Gender': gender, 
            'Tasks': tasks, 'Date': datetime.date.today()}
    # 'Task Status': task_status,
    df = pd.DataFrame(data, index=[0])
    
    # データをS3に保存
    write_to_s3(df, f'data_{datetime.date.today()}.csv')

    st.success('データ保存完了.')
