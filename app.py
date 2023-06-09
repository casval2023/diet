import streamlit as st
import pandas as pd
import boto3
import datetime
from io import StringIO
import matplotlib.pyplot as plt

# AWSのクレデンシャルを設定（AWS Management Consoleで確認できます）
AWS_ACCESS_KEY_ID = 'AKIAV27ZCYO3NIGWWEEZ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_BUCKET = 'skkeng'
AWS_S3_REGION_NAME = 'ap-northeast-1' # 例：'us-west-2'

s3 = boto3.client('s3', 
                  region_name=AWS_S3_REGION_NAME,
                  aws_access_key_id=AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
  
def load_data():
    # S3からCSVを読み込み、DataFrameに変換
    obj = s3.get_object(Bucket=AWS_S3_BUCKET, Key='df.csv')
    df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
    return df

def save_data(df):
    # DataFrameをCSVに変換し、S3に保存
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3.put_object(Bucket=AWS_S3_BUCKET, Key='df.csv', Body=csv_buffer.getvalue())

#df = load_data()
#list_df = df.values.tolist()
#st.write(list_df)
my_ID = 'test'
my_PASS = 'test'
date = datetime.datetime.utcnow().date().strftime("%Y/%m/%d")
#st.write(df)

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
#st.write('例：１日1500kcal以内（基礎代謝量＋200～300kcal目安）、１日１万歩達成、動画講義１章分視聴、復習問題１章分チャレンジ、筋トレメニュー')
#task_status = [st.checkbox(task) for task in tasks]

# データの作成
data = {
    '日付': ['2023-06-01', '2023-06-02', '2023-06-03', '2023-06-04', '2023-06-05'],
    '体重': [68, 69, 70, 71, 70]
}

# DataFrameへの変換と日付の型変換
df = pd.DataFrame(data)
df['日付'] = pd.to_datetime(df['日付'])
#st.write(f'{my_ID}さんの体重変化推移')
st.write('<p style="font-family:体重変化推移; color:purple; font-size: 36px;">体重変化推移</p>',  unsafe_allow_html=True)

# グラフの作成
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(df['日付'], df['体重'])
#ax.set_title('Weight changes')
ax.set_xlabel('Date')
ax.set_ylabel('Weight')
ax.grid(True)

# Streamlitにグラフを表示
st.pyplot(fig)

# 入力データの保存
if st.button('データ保存'):
    new_row = {'ID': my_ID,'PASS': my_PASS,'日付': date,'身長': height,'体重': weight,'体脂肪率': body_fat, '年齢': age,'性別': gender,'タスク': tasks,'感想': '良い'}
    #st.write(new_row)
    df = df.append(new_row, ignore_index=True)
    
    # データをS3に保存
    save_data(df)
    st.write(df)
    st.success('データ保存完了.')

