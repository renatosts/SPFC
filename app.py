import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def define_color(val):
    if val < 0:
        color = 'red'
    elif val > 0:
        color = 'green'
    else:
        color = 'gray'
    return 'color: %s' % color

def set_color_patrim(val):
    return 'color: %s' % 'olive'

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    #text = link.split('=')[1]
    if link == '':
        return link
    text = 'Vídeo'
    return f'<a target="_blank" href="{link}">{text}</a>'

@st.cache_data
def getFile(f):
    return pd.read_csv(f, sep=';', thousands='.', decimal=',')

st.set_page_config(
    layout='wide',
    initial_sidebar_state='collapsed',
    page_icon='app.jpg',
    page_title='SPFC')


f = 'https://raw.githubusercontent.com/renatosts/SPFC/main/SPFC.csv'
#f = 'SPFC.csv'

df = getFile(f)

df['data'] = pd.to_datetime(df['Data'], dayfirst=True)

df = df.sort_values('data', ascending=False)

df.Vídeo = df.Vídeo.fillna('').apply(make_clickable)

df.index = df.index + 1

df = df[['Data', 'Dia', 'Estádio', 'Tricolor', 'Pl1', 'Pl2', 'Adversário', 'Campeonato', 'Setor', 'Vídeo']]

camp = df['Campeonato'].drop_duplicates().sort_values()

advers = df['Adversário'].drop_duplicates().sort_values()

col1, col2, col3 = st.columns(3)
with col1:
    filt_advers = st.multiselect('Adversários', advers)
with col2:
    filt_camp = st.multiselect('Campeonatos', camp)

if filt_advers != []:
    df = df[df['Adversário'].isin(filt_advers)]

if filt_camp != []:
    df = df[df['Campeonato'].isin(filt_camp)]

df = df.to_html(escape=False)


st.write(df, unsafe_allow_html=True)
