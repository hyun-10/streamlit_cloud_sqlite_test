import streamlit as st
import sqlite3



def app():
  connect = sqlite3.connect('box.db', isolation_level=None)
  cursor = connect.cursor();
  
  #cursor.execute('select 영화명 from box')
  #for i in cursor:
      #st.write(i)
  
  
  #input="select 영화명, img_url from box ORDER BY 개봉일 DESC where 영화명 NOT IN(' " " ')"
  #input="select 영화명, 순위, 개봉일, 누적관객수, img_url from box where 영화인,순위,개봉일,누적관객수 NOT IN('"') ORDER BY 영화명 DESC"
  
  
  
  #input = 'SELECT 영화명,개봉일,img_url FROM box WHERE 개봉일 IN (%-%) ORDER BY 영화명 DESC'
  
  #input = 'SELECT 영화명,개봉일,img_url FROM box WHERE NOT 개봉일 IS null ORDER BY 영화명 DESC'
  
  
  
  
  
  
  #input = 'SELECT 영화명,개봉일,img_url FROM box WHERE NOT 개봉일 IS null GROUP BY 영화명 ORDER BY 개봉일 DESC '
  
  input = 'SELECT 영화명,개봉일,img_url FROM box WHERE NOT 영화명 IS " GROUP BY 영화명 ORDER BY 개봉일 DESC '
  cursor.execute(input)
  for i in cursor:
     j=i[:5]
      st.write(j)
  
  
  
  
  #st.write(input)
  
  #quary_string = f"select 영화명, 개봉일, 순위, 누적관객수fantasy,peopleNm from box where movieNm in ('{영화제목}')"

  
  #cursor.execute(quary_string)
  #for test in cursor:
      #st.write(test)
      


      #st.image(img_url,width=300,)
