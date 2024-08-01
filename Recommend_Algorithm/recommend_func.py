# 专业学校推荐
alldf = pd.read_csv('alldata1.0.csv',encoding='gbk',index_col=0)
alldf['c2']=alldf['c2'].fillna('')

def rec(cate,score,prov,c_rank,majors,m_rank,risk):
    '''
    输入为：文理科，高考分数，期望省份，地域重要性，期望专业（多选），专业重要性，风险性
    输出为：该推荐大学+专业的省市位置，大学名，专业名，预计所需最低排名，推荐指数
    '''
    
    # 筛选文理科
    df = alldf[alldf['categoryID_id'] == cate]     
    
    # 河南2021一分一档对照表
    rec_rank = rankings21[rankings21['categoryID_id'] == cate]     
    if score>=rec_rank.describe()['score']['max']:
        ranking=rec_rank.describe()['rank']['min']
    else:
        ranking = rec_rank[rec_rank['score'] == score]['rank'].values[0]
    print(ranking)
    
    df_pass=pd.DataFrame()
    
    for major in majors:
        # 筛选专业
        if major[1]==None:#输入 c1 None
            df_temp = df[df['c1'].str.contains(major[0])]
            df_pass = pd.concat([df_pass,df_temp],axis=0 ,ignore_index=True)
        else:#输入c1 c2
            df_temp = df[df['c2'].str.contains(major[1])]
            df_temp1 = df[(df['c1'].str.contains(major[0])) & (df['c2']=='')]
            df_pass = pd.concat([df_pass,df_temp,df_temp1],axis=0 ,ignore_index=True)
        
    df=df_pass.drop_duplicates()
    
    # 统计综合得分
    for provID in df['provinceLoc']:
        if provID == prov:
            df.loc[df['provinceLoc'] == prov,'sum_score'] = (df['cityScore']*(1 + c_rank/10) + df['majorScore']*m_rank) / (c_rank + m_rank)
        else:
            df.loc[df['provinceLoc'] != prov,'sum_score'] = (df['cityScore']*1 + df['majorScore']*m_rank) / (c_rank + m_rank)
            
    
    # 学校代码转换学校名称
    for dfs in df['collegeID_id']:
        df.loc[df['collegeID_id'] == dfs,'college'] = colleges21[colleges21[0] == dfs][1].values[0]
    df = df.sort_values(['preRanking'],ascending=True)

    # 报考排名范围：0.9ranking-1.5ranking
    if risk == 1:     # 输出所有符合条件的推荐方案
        df_temp1 = df[df['preRanking'] >= ranking*0.9]
        df_temp2 = df_temp1[df_temp1['preRanking'] < ranking*1.0]
        df_temp3 = df[df['preRanking'] >= ranking*1.0][0:6]
        df = pd.concat([df_temp2,df_temp3],axis=0 ,ignore_index=True)
        df = df[0:12]
        if df.empty:
            df = df[df['preRanking'] >= ranking*1.0][0:6]
    elif risk ==2:     # 输出报考风险相对大的推荐方案
#         df = df[df['preRanking'] < ranking*1.0]    
        df = df[df['preRanking'] >= ranking*0.9]
        df = df[0:6]
    else:     # 输出报考稳妥的推荐方案 
#         df = df[df['preRanking'] < ranking*1.5]    
        df = df[df['preRanking'] >= ranking*1.0]
        df = df[0:6]
    
    max_score=df.describe()['sum_score']['max']
    df['sum_score']=df['sum_score']/max_score*100
        
    df = df.sort_values(['sum_score'],ascending=False)
    df = df.loc[:,('provinceLoc','cityLoc','college','majorName','preRanking','sum_score')]
    
    return df
   

#示例调用
rec(1,672,'北京市',1,[['文学',None]],1,1)
rec(2,660,'江苏省',1,[['理学',None],['工学','计算机类'],['工学','电子信息类']],1,1)