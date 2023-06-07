import streamlit as st
import csv
from datetime import datetime
import os
from module import login, save_profile, show_profile, profile, save_weight, show_weight, weight, save_meal, show_meal, meal, save_bmi, calculate_bmi, show_bmi, bmi, save_steps, show_steps, steps, show_exercise, save_exercise, exercise, save_journal, show_journal, reflection, logout, main
import pandas as pd
import boto3
from io import StringIO
import io

#ログイン情報
id_pwd = {'test': 'test'}

if __name__ == '__main__':
    main()
