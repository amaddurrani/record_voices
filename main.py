from turtle import shape
import streamlit as st
import pandas as pd
from streamlit_card import card
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_option_menu import option_menu
import gspread_dataframe as gd
import os
from record import record,save_record,read_audio
import numpy as np
import glob
from upload_audios import upload_file
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]
df= pd.read_csv('voices_unavailable.csv')
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css('style.css')
st.image(image='HeaderBanner.jpg')

def functionality():
    card(title=df[0], text=' ', image="https://images.pexels.com/photos/2341290/pexels-photo-2341290.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")

with st.sidebar:
    choose = option_menu(" ", ["Record voice","Data recorded / Upload"],
                         icons=['mic','check' ],
                          default_index=0)
if choose=='Record voice':
    df=df['word']
    st.markdown('<p class="urdu-font"; style=text-align:right; >صوت ریکارڈ کیجیے</p>', unsafe_allow_html=True)
    if "counter" not in st.session_state:
        st.session_state["counter"] = 0
        st.session_state["rec"]=None
    
    with st.form("My form",clear_on_submit=True):
        functionality()
        submitted = st.form_submit_button("ریکارڈ کیجیے")
        if submitted:
            record_state= st.text('recording...')
            duration=3
            fs=48000
            myrecording = record(duration, fs)
            st.session_state["rec"] =myrecording
            path_myrecording = f"./temp/sample.wav"
            save_record(path_myrecording, myrecording, fs)
            st.audio(read_audio(path_myrecording))
            st.write("آواز دوبارہ ریکارڈ کرنے کے لیے' ریکارڈ کیجیے' کا بٹن دبایں۔")
            st.session_state["counter"] = 1
    if st.button("صوت سیو کیجیے"):
        if st.session_state["counter"] ==0:
            st.warning('voice not recorded yet first record it please')
        else:
            df=pd.read_csv('voices_unavailable.csv')
            word=df['word'][0]
            df=df.drop(df.loc[df['word']==word].index.values)
            final= pd.read_csv('final.csv')
            
            try:
                list_of_files = glob.glob('recorded_voices/*.wav') # * means all if need specific format then *.csv
                latest_file = max(list_of_files, key=os.path.getctime)
                file_name=str(int(latest_file.split('/')[1].split('.wav')[0])+1)
            except:
                file_name='0'
            path_myrecording = f"./recorded_voices/"+file_name+".wav"
            save_record(path_myrecording, st.session_state["rec"], 48000)
            os.remove('./temp/sample.wav')
            final=final.append({'word':word,'voice':path_myrecording},ignore_index=True)
            final.to_csv('final.csv',index=False)
            st.write('File Saved')
            st.session_state["counter"] = 0
            st.session_state["rec"]=None
            df.to_csv('voices_unavailable.csv',index=False)
            st.experimental_rerun()
if choose=='Data recorded / Upload':
    #show recorded voices
    #credentials = ServiceAccountCredentials.from_json_keyfile_name("words-correction-a710f731b5e8.json", scope)
    credentials = ServiceAccountCredentials.from_json_keyfile_name("voices-367409-3c9e0403a16a.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("recorded voices").sheet1
    final= pd.read_csv('final.csv')
    st.write(final)
    upload= st.button('Upload File')
    if upload:
        for i in final['voice']:
            upload_file(i)
        existing=gd.get_as_dataframe(sheet)
        updated= existing.append(final)
        gd.set_with_dataframe(sheet,updated)
        final.drop(final.index, inplace=True)
        final.to_csv('final.csv',index=False)
        st.write('Data Uploaded Successfully')
        st.write(sheet)