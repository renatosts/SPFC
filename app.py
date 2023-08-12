import streamlit as st
import pandas as pd


def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    if link == '':
        return link
    text = 'Vídeo'
    return f'<a target="_blank" href="{link}">{text}</a>'


@st.cache_data
def getFile(f):
    return pd.read_csv(f, sep=';', encoding='Latin1', thousands='.', decimal=',')

st.set_page_config(
    layout='wide',
    initial_sidebar_state='collapsed',
    page_icon='app.jpg',
    page_title='SPFC')


st.header('SÃO PAULO FUTEBOL CLUBE')

f = 'https://raw.githubusercontent.com/renatosts/SPFC/main/CSV/SPFC.csv'
#f = r'.\CSV\SPFC.csv'

df = getFile(f)

df['data'] = pd.to_datetime(df['Data'], dayfirst=True)

df = df.sort_values('data', ascending=False)

df['Dia'] = df['Dia'].str.capitalize()

df['VDE'] = 'E'
df.loc[df.Pl1 > df.Pl2, 'VDE'] = 'V'
df.loc[df.Pl1 < df.Pl2, 'VDE'] = 'D'

camp = df['Campeonato'].drop_duplicates().sort_values()

advers = df['Adversário'].drop_duplicates().sort_values()

vde = ['Vitória', 'Empate', 'Derrota']

col1, col2, col3, col4 = st.columns([2, 2, 1.5, 1])
with col1:
    filt_advers = st.multiselect('Adversários', advers)
with col2:
    filt_camp = st.multiselect('Campeonatos', camp)
with col3:
    filt_vde = st.multiselect('Resultados', vde)

if filt_advers != []:
    df = df[df['Adversário'].isin(filt_advers)]

if filt_camp != []:
    df = df[df['Campeonato'].isin(filt_camp)]

if filt_vde != []:
    df = df[df['VDE'].isin([x[:1] for x in filt_vde])]

df.Vídeo = df.Vídeo.fillna('').apply(make_clickable)

df.index = df.index + 1

df['Placar'] = df.Pl1.astype(str) + ' x ' + df.Pl2.astype(str)

if len(df) > 0:
    for col in ['Tricolor', 'Placar', 'Adversário']:
        df[col] = df.apply(lambda row: 
            f'<span style="font-weight:bold; color:darkgreen">{row[col]}</span>' if row.VDE == 'V' 
            else f'<span style="font-weight:bold; color:darkred">{row[col]}</span>' if row.VDE == 'D' 
            else f'<span style="font-weight:bold; color:goldenrod">{row[col]}</span>', axis=1)

df = df[['Data', 'Dia', 'Estádio', 'Tricolor', 'Placar', 'Adversário', 'Campeonato', 'Setor', 'Vídeo']]

df = df.to_html(escape=False)

st.write(df, unsafe_allow_html=True)
