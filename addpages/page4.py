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
  genre_ = st.selectbox('장르를 선택하세요',('family','performance' ,'horror','etc','documentary','drama','melodrama','musical','mystery','crime','historical','western','adult','thriller','animated','action','adventure','war','comedy','fantasy'))
  genre_ = genre_
  #puid= 'adiv****'
  puid = st.text_input('', key=1)
                    
  #punick= '푸른불'
  punick = st.text_input('',key=2)

  puid=puid[0:4]+'****'

  def full_data_learning(genre_):
    col = 'item rating user'
    reader = Reader(line_format=col, sep=',', rating_scale=(0,10))
    
    total = []
    number = 1
    while True :
        try :
            datas = pd.read_csv(f'db/4p/{genre_}_review_noh_{str(number}.csv', header=None, index_col=False)
            total.append(datas)
        except :
            break
        number += 1
    tod = pd.concat(total, ignore_index=True)
    
    #data_folds = DatasetAutoFolds(ratings_file=f'db/4p/{genre_}_review_noh_1.csv', reader=reader)
    
    
    #trainset = data_folds.build_full_trainset()
    trainset = tod
    algo = SVD(n_epochs=5, n_factors=500, random_state=0)
    algo.fit(trainset)
    return algo
    

  algo = full_data_learning(genre_)
  
  def mvCd_of_unshow(genre_,puid,punick):
    total = []
    number = 1
    while True :
        try :
            datas = pd.read_csv(f'db/4p/{genre_}_review_noh_{str(number)}.csv', 
            names=['code','score','raw_user', 'userCd','user_id', 'user_nick', 'movie', 'genre','review'])
            total.append(datas)
        except :
            break
        number += 1
    data = pd.concat(total, ignore_index=True)
    #data = pd.read_csv(f'db/4p/{genre_}_review_noh_1.csv', names=['code','score','raw_user', 'userCd','user_id', 'user_nick', 'movie', 'genre','review'])
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
  
  '''
  genre_='fantasy'
  puid= 'adiv****'
  punick= '푸른불'
  
  
  puid=puid[0:4]+'****' # 아이디아스키값처리
  algo = full_data_learning(genre_) # 장르의 리뷰학습
  unshow_mvCd_array = mvCd_of_unshow(genre_,puid,punick) # 사용자가 보지 않은 영화선정
  user_mvrating_est_list = prediction(algo,puid,unshow_mvCd_array) # 예측평점구하기
  user_movie_recomendation_df = get_recomendationmovie(user_mvrating_est_list) #추천영화목록구하기
  #장르별 추천영화 순위순으로 표출
  user_movie_recomendation_df_ = user_movie_recomendation_df.set_index('rank')
  user_movie_recomendation_df_.sort_index()
  st.dataframe(user_movie_recomendation_df_)
  '''
  
  
  
  
  
 
