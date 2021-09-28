#!/usr/bin/env python
# coding: utf-8

# In[2]:


#필요한 모듈 선언
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


#read_csv 를 통하여 dataframe 형태로 읽기
corona_all=pd.read_csv("./data/서울시 코로나19 확진자 현황.csv")


# In[4]:


corona_all.head()   # 상위 5개의 데이터 출력


# In[16]:


#dataframe 정보를 요약하려 출력
corona_all.info()


# In[7]:


corona_del_col = corona_all.drop(columns = ['국적','환자정보','조치사항'])


# In[8]:


corona_del_col.info() #정제 처리된 dataframe 정보를 출력합니다.


# In[9]:


corona_del_col['확진일']


# In[10]:


#확진일 데이터를 month, day 데이터로 나누기
month = []
day = []
for data in corona_del_col['확진일']:
    #split 함수를 사용해서 월, 일 나누어 list 저장
    month.append(data.split('.')[0])
    day.append(data.split('.')[1])


# In[11]:


corona_del_col['month'] = month
corona_del_col['day'] = day

corona_del_col['day'].astype('int64')
corona_del_col['month'].astype('int64')


# In[12]:


# 그래프에서 x 축의 순서를 정리하기 위해서 order list를 생성합니다.
order = []
for i in range(1,11):
    order.append(str(i))
    
order


# In[13]:


#그래프의 사이즈를 조절
plt.figure(figsize=(10,5))

#seaborn의 countplot 함수를 사용하여 출력
sns.set(style ="darkgrid")
ax=sns.countplot(x="month", data=corona_del_col, palette="Set3", order = order)


# In[14]:


#series의 plot 함수를 사용한 출력 방법
corona_del_col['month'].value_counts().plot(kind='bar')


# In[15]:


corona_del_col['month'].value_counts()


# In[16]:


#8월 확진자 수 출력
# x축의 순서를 정리하기 위해서 order list를 생성
order2 = []
for i in range(1,32):
    order2.append(str(i))
order2


# In[17]:


#seaborn의 countplot 함수를 사용하여 출력
plt.figure(figsize=(20,10))
sns.set(style="darkgrid")
ax = sns.countplot(x="day", data = corona_del_col[corona_del_col['month'] == '8'],palette="Paired", order = order2)


# In[18]:


#8월의 확진자 수
corona_del_col[corona_del_col['month'] == '8']['day'].count()/31


# In[56]:


#지역별 확진자 수 출력
corona_del_col['지역']


# In[36]:


import matplotlib.font_manager as fm

font_dirs = ['/usr/share/fonts/truetype/nanum', ]
font_files = fm.findSystemFonts(fontpaths=font_dirs)

for font_file in font_files:
    fm.fontManager.addfont(font_file)


# In[41]:


# replace 함수를 사용하여 해당 데이터를 변경합니다.
# 이상치가 처리된 데이터이기에 새로운 Dataframe으로 저장합니다.
corona_out_region = corona_del_col.replace({'종랑구':'중랑구', '한국':'기타'})


# In[42]:


#8월달 지역별 확진자수 출력 
#논리연산을 이용한 조건을 다음과 같이 사용하면 해당 조건에 맞는 데이터를 출력할 수 있습니다.
corona_out_region[corona_del_col['month'] == '8']


# In[45]:


# 그래프를 출력합니다.
plt.figure(figsize=(20,10))
sns.set(font="Malgun gothic", 
        rc={"axes.unicode_minus":False},
        style='darkgrid')
ax = sns.countplot(x="지역", data=corona_out_region[corona_del_col['month'] == '8'], palette="Set2")


# 서울 지역에서 확진자를 지도에 출력

# In[57]:


# 지도 출력을 위한 라이브러리 folium을 import 합니다.
import folium

# Map 함수를 사용하여 지도를 출력합니다.
#osm (open stream map)  , location [위도,경도], 초기 화면 크기 설정)
map_osm = folium.Map(location=[37.529622, 126.984307], zoom_start=11)

map_osm


# In[59]:


# CRS에 저장합니다.
CRS=pd.read_csv("./data/서울시 행정구역 시군구 정보 (좌표계_ WGS1984).csv")
CRS


# In[60]:


CRS[CRS['시군구명_한글']=='중구']


# In[61]:


# corona_out_region의 지역에는 'oo구' 이외로 `타시도`, `기타`에 해당되는 데이터가 존재 합니다.
# 위 데이터에 해당되는 위도, 경도를 찾을 수 없기에 삭제하여 corona_seoul로 저장합니다.
corona_seoul = corona_out_region.drop(corona_out_region[corona_out_region['지역'] == '타시도'].index)
corona_seoul = corona_seoul.drop(corona_out_region[corona_out_region['지역'] == '기타'].index)

# 서울 중심지 중구를 가운데 좌표로 잡아 지도를 출력합니다.
map_osm = folium.Map(location=[37.557945, 126.99419], zoom_start=11)

# 지역 정보를 set 함수를 사용하여 25개 고유의 지역을 뽑아냅니다.
for region in set(corona_seoul['지역']):

    # 해당 지역의 데이터 개수를 count에 저장합니다.
    count = len(corona_seoul[corona_seoul['지역'] == region])
    # 해당 지역의 데이터를 CRS에서 뽑아냅니다.
    CRS_region = CRS[CRS['시군구명_한글'] == region]

    # CircleMarker를 사용하여 지역마다 원형마커를 생성합니다
    #folium 에서 marker 사용. 위도 컬럼, 경도 컬럼을 가져옴
    # 원형 마커의 크기 (범위 반경) count 값에 따라 달라지도록
    #팝업 -> region, count, 단위
    marker = folium.CircleMarker([CRS_region['위도'], CRS_region['경도']], # 위치
                                  radius=count/10 + 10,                 # 범위
                                  color='#3186cc',            # 선 색상
                                  fill_color='#3186cc',       # 면 색상
                                  popup=' '.join((region, str(count), '명'))) # 팝업 설정
    
    # 생성한 원형마커를 지도에 추가합니다.
    marker.add_to(map_osm)

map_osm


# In[ ]:




