import streamlit as st
from surprise import SVD
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise.dataset import DatasetAutoFolds
from surprise import Reader
import pandas as pd
import numpy as np
import sqlite3

def app():
  #genre_='fantasy'
  genre_ = st.selectbox('장르를 선택하세요',('action','adult','adventure','animation','comedy','crime','documentary','drama','etc','family','fantasy','fear','history','melo','musical','mystery','thriller','war','western'))
  genre_ = genre_

  puid = st.text_input('adiv****', key=1)
                    

  punick = st.text_input('푸른불',key=2)
  if punick:
    puid=puid[0:4]+'****'

    def full_data_learning(genre_):
      col = 'item rating user'
      reader = Reader(line_format=col, sep=',', rating_scale=(0,10))
 
      count = 0
      while True :
          try :
              data_folds = DatasetAutoFolds(ratings_file=f'db/4p/{genre_}_review_noh_{str(count)}.csv', reader=reader)
              trainset = data_folds.build_full_trainset()
              algo = SVD(n_epochs=5, n_factors=500, random_state=0)
              algo.fit(trainset)
              break
          except :
              count += 1
      return algo

    algo = full_data_learning(genre_)
  
    def mvCd_of_unshow(genre_,puid,punick):
      data = pd.read_csv(f'db/4p/{genre_}_review_noh_1.csv', names=['code','score','raw_user', 'userCd','user_id', 'user_nick', 'movie', 'genre','review'])
      str_expr = '(user_id == @puid) and (user_nick == @punick)'
      total = data.code.unique()
      query = data.query(str_expr)['code'].unique()
      indexes = [np.where(total==i)[0][0] for i in query]
      df_q =np.delete(total,indexes)
      return df_q
  
    unshow_mvCd_array = mvCd_of_unshow(genre_,puid,punick)
  
    def prediction(algo,uid, uia):
      pred = [algo.predict(uid=str(uid), iid=str(isbn)) for isbn in uia]
      ests = lambda x : x.est
      pred.sort(key=ests, reverse=True)
      top10_pred = pred[:10]
      isbn_est_list = [(pr.iid, pr.est) for pr in top10_pred]
      return isbn_est_list
  
    user_mvrating_est_list = prediction(algo,puid,unshow_mvCd_array)
  
    def get_recomendationmovie(prediction):
      movies = pd.read_table('db/4p/movie_info.csv', sep=',', encoding='utf-8', engine='python')
      mvCd_list = []
      for i in prediction :
        mvCd_list.append(i[0])
      str_expr='영화코드 in @mvCd_list'
      df_q = movies.query(str_expr)
    #추천순위로 정렬하기
      df_q['rank']=0
      rank=1
      for i in prediction:      
        index = df_q.index[df_q['영화코드'] == i[0]]
        df_q.loc[index,'rank']=rank
        rank=rank+1
      return df_q
  
    user_movie_recomendation_df = get_recomendationmovie(user_mvrating_est_list)

    user_movie_recomendation_df = user_movie_recomendation_df.set_index('rank')
    st.dataframe(user_movie_recomendation_df.sort_index())
    st.dataframe(ursr_movie_recomendataion_df.iloc[[1]]
  

  
