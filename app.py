import streamlit as st
from add_pages import pages
from pages import pages1 as p1
from pages import pages2 as p2
from pages import pages3 as p3
from pages import pages4 as p4
from pages import pages5 as p5








app=pages()

st.title('Movie Project')

app.add_page('메인 페이지',p1.app)
app.add_page('영화 정보')
app.add_page('영화인 정보',p3.app)
app.add_page('영화추천')
app.add_page('가상 캐스팅')


