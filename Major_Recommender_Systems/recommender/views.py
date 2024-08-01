from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
#from ormDesign.models import *
from django.http import HttpResponse
from django.http import JsonResponse
import pandas as pd
import os
import sqlite3 as db

category={
	"文科":1,
	"理科":2,
	"综合":3
}
def predict(request):  # 预测函数，向前端发送json格式预测结果
    # 参数赋值
    args_dict={'cate':2, 'score':660, 'prov':'江苏', 'majors':["经济学","财经学类"],
                 'c_rank':1, 'm_rank':1, 'risk':1}
    
    args_list = ['cate', 'score', 'prov', 'majors',
                 'c_rank', 'm_rank', 'risk']  # 推荐系统接受的参数名称
    args_dict = {}  # 推荐系统接受的参数字典
    print(request.GET)
    for _ in range(len(request.GET)-len(args_list)):
        args_list.insert(4,'c_rank')
    print(args_list)
    for arg, (key,value) in zip(args_list, request.GET.items()):
        tb=request.GET.getlist(key,[])
        if "Majors" in key:
            args_dict.setdefault("majors",[]).append(tb)
        else:
            if arg =='cate':
                args_dict[arg]=category[tb[0]]
            else:
                args_dict[arg]= tb[0] if len(tb)==1 else tb
    print(args_dict)
    result = rec(**args_dict)  # 进行预测
    recommend_list = ['provinceLoc', 'cityLoc', 'college',
                      'majorName', 'preRanking', 'sum_score']  # 预测返回参数列表
    recommend_result = result.values.tolist()
    #print(recommend_result)
    return JsonResponse({"recommend_result": recommend_result})
#测试用例1
def predict1(request):  # 预测函数，向前端返回json
    # 参数赋值
    args_dict={'cate':1, 'score':660, 'prov':'江苏', 'majors':[['理学',None],['工学','计算机类'],['工学','电子信息类']],
                 'c_rank':1, 'm_rank':1, 'risk':1}
    result = rec(**args_dict)  # 进行预测
    recommend_list = ['provinceLoc', 'cityLoc', 'college',
                      'majorName', 'preRanking', 'sum_score']  # 预测返回参数列表
    recommend_result = result.values.tolist()
    #print(recommend_result)
    return JsonResponse({"recommend_result": recommend_result})
#测试用例2
def predict2(request):  # 预测函数，向前端返回json
    # 参数赋值
    args_dict={'cate':2, 'score':640, 'prov':'江苏', 'majors':["经济学","财经学类"],
                 'c_rank':1, 'm_rank':1, 'risk':1}
    result = rec(**args_dict)  # 进行预测
    recommend_list = ['provinceLoc', 'cityLoc', 'college',
                      'majorName', 'preRanking', 'sum_score']  # 预测返回参数列表
    recommend_result = result.values.tolist()
    #print(recommend_result)
    return JsonResponse({"recommend_result": recommend_result})

projectName = 'Major_Recommender_Systems'


def readDataBase(exeCMD):
    fdir = os.path.dirname(os.getcwd())  # 获取父目录
    sql_file = os.path.join(fdir, projectName, 'gaokao_database.sqlite3')
    #print('sql_file:', sql_file)
    try:
        conn = db.connect(sql_file)  # 返回数据库API链接
        c = conn.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
        cursor = c.execute(exeCMD)  # 该例程执行一个 SQL 语句
        rows = cursor.fetchall()  # 该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，则返回一个空的列表。
        return rows  # 输出查询结果
    except Exception as e:
        print(e)
        print('查询数据失败')
    finally:
        conn.close()  # 关闭数据库


def readMajors(request):
    exeCMD1 = 'select provinceName, COUNT(1) from Majors left join Provinces on Majors.provinceID_id = Provinces.provinceID group by provinceID_id order by COUNT(1) DESC'
    rows1 = readDataBase(exeCMD1)
    exeCMD2 = 'select provinceName, COUNT(1) from Rankings left join Provinces on Rankings.provinceID_id = Provinces.provinceID group by provinceID_id order by COUNT(1) DESC'
    rows2 = readDataBase(exeCMD2)
    tempdict = {}
    for r1 in rows1:
        for r2 in rows2:
            if r1[0] == r2[0]:
                tempdict[r1[0]] = f'专业录取数据{r1[1]}条，排名数据{r2[1]}条'

    exeCMD3 = 'select collegeName, COUNT(1) from Majors left join Colleges on Majors.collegeID_id = Colleges.collegeID group by collegeID_id order by COUNT(1) DESC'
    rows3 = readDataBase(exeCMD3)
    cdict = {}
    for r3 in rows3:
        cdict[r3[0]] = f'专业录取数据{r3[1]}条'
    return render(request, 'dataStatistics.html', {'Majors': tempdict, 'Colleges': cdict})


def getTable(tableName):
    fdir = os.path.dirname(os.getcwd())  # 获取父目录
    sql_file = os.path.join(fdir, projectName, 'gaokao_database.sqlite3')
    print('sql_file:', sql_file)
    line = 'select * from ' + tableName
    conn = db.connect(sql_file)
    c = conn.cursor()
    cursor = c.execute(line)  # 对数据库执行读取全表的操作
    alld = cursor.fetchall()
    cursor.close()
    conn.close()
    return alld

# 获取表的列名、列名结构


def get_cols(form):
    fdir = os.path.dirname(os.getcwd())  # 获取父目录
    sql_file = os.path.join(fdir, projectName, 'gaokao_database.sqlite3')
    print('sql_file:', sql_file)
    conn = db.connect(sql_file)  # 返回数据库API链接
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format(form))
    col_name = [tuple[0] for tuple in c.description]

    c.execute("PRAGMA table_info({})".format(form))
    col_structure = c.fetchall()
    return col_name, col_structure


# 获取表的内容（DF结构）
def db_to_df(form):
    fdir = os.path.dirname(os.getcwd())  # 获取父目录
    sql_file = os.path.join(fdir, projectName, 'gaokao_database.sqlite3')
    #print('sql_file:', sql_file)
    conn = db.connect(sql_file)  # 返回数据库API链接
    c = conn.cursor()
    sql = "SELECT * FROM {}".format(form)
    values = c.execute(sql)
    f_df = pd.DataFrame(data=values)
    return f_df


'''负责模型的同学直接复制一下代码进行数据读取即可，最终形式为dataframe类型的csv_data
a = getTable('total2020')
#print(a)
#print(type(a))

csv_data = pd.DataFrame(a, columns=['id', 'majorName', 'year', 'minScore', 'categoryID_id', 'collegeID_id', 'c1', 'c2',
                                    'college_loc', 'provinceLoc', 'cityLoc', 'adcode', 'cityScore', 'c2code', 'majorScore', 'preRanking'])
print(csv_data)
print(type(csv_data))
'''


def rec(cate, score, prov, majors, c_rank, m_rank, risk):
    """[专业推荐功能实现]

    Args:
        cate ([str]): [文理科]
        score ([int]): [高考分数]
        prov ([str]): [期望省份]
        majors ([list]): [期望专业（多选）]
        c_rank ([int]): [地域重要性]
        m_rank ([int]): [专业重要性]
        risk ([int]): [风险性]
    """
    score = int(score)
    c_rank = int(c_rank)
    m_rank = int(m_rank)
    risk = int(risk)

    table = readDataBase("SELECT name FROM sqlite_master WHERE type='table'")
    # print(table)
    cates = table[0][0]     # 获取类名
    mmajors = table[3][0]     # 获取专业表名
    colleges = table[6][0]     # 获取学校名
    province = table[4][0]
    rankings = table[4][0]
    fir = table[3][0]

    # 河南一分一档表
    rankings21 = db_to_df(rankings)
    rankings21.columns = get_cols(rankings)[0]
    rankings21 = rankings21[rankings21['year'] == 2021]
    rankings21 = rankings21[rankings21['provinceID_id'] == 1]

    colleges21 = db_to_df(colleges)
    # 专业学校推荐
    alldf = pd.DataFrame(getTable('total2020'), columns=['id', 'majorName', 'year', 'minScore', 'categoryID_id', 'collegeID_id', 'c1', 'c2',
                                                         'college_loc', 'provinceLoc', 'cityLoc', 'adcode', 'cityScore', 'c2code', 'majorScore', 'preRanking'])

    alldf['c2'] = alldf['c2'].fillna('')
    # 筛选文理科
    df = alldf[alldf['categoryID_id'] == cate]

    # 河南2021一分一档对照表
    rec_rank = rankings21[rankings21['categoryID_id'] == cate]
    if score >= rec_rank.describe()['score']['max']:
        ranking = rec_rank.describe()['rank']['min']
    else:
        ranking = rec_rank[rec_rank['score'] == score]['rank'].values[0]
    print(ranking)

    df_pass = pd.DataFrame()

    for major in majors:
        # 筛选专业
        if major[1] == None:  # 输入 c1 None
            df_temp = df[df['c1'].str.contains(major[0])]
            df_pass = pd.concat([df_pass, df_temp], axis=0, ignore_index=True)
        else:  # 输入c1 c2
            df_temp = df[df['c2'].str.contains(major[1])]
            df_temp1 = df[(df['c1'].str.contains(major[0])) & (df['c2'] == '')]
            df_pass = pd.concat([df_pass, df_temp, df_temp1],
                                axis=0, ignore_index=True)

    df = df_pass.drop_duplicates()

    # 统计综合得分
    for provID in df['provinceLoc']:
        if provID == prov:
            df.loc[df['provinceLoc'] == prov, 'sum_score'] = (
                df['cityScore']*(1 + c_rank/10) + df['majorScore']*m_rank) / (c_rank + m_rank)
        else:
            df.loc[df['provinceLoc'] != prov, 'sum_score'] = (
                df['cityScore']*1 + df['majorScore']*m_rank) / (c_rank + m_rank)
    # 学校代码转换学校名称
    for dfs in df['collegeID_id']:
        df.loc[df['collegeID_id'] == dfs,
               'college'] = colleges21[colleges21[0] == dfs][1].values[0]
    df = df.sort_values(['preRanking'], ascending=True)

    # 报考排名范围：0.9ranking-1.5ranking
    if risk == 1:     # 输出所有符合条件的推荐方案
        df_temp1 = df[df['preRanking'] >= ranking*0.9]
        df_temp2 = df_temp1[df_temp1['preRanking'] < ranking*1.0]
        df_temp3 = df[df['preRanking'] >= ranking*1.0][0:6]
        df = pd.concat([df_temp2, df_temp3], axis=0, ignore_index=True)
        df = df[0:12]
        if df.empty:
            df = df[df['preRanking'] >= ranking*1.0][0:6]
    elif risk == 2:     # 输出报考风险相对大的推荐方案
        #         df = df[df['preRanking'] < ranking*1.0]
        df = df[df['preRanking'] >= ranking*0.9]
        df = df[0:6]
    else:     # 输出报考稳妥的推荐方案
        #         df = df[df['preRanking'] < ranking*1.5]
        df = df[df['preRanking'] >= ranking*1.0]
        df = df[0:6]

    max_score = df.describe()['sum_score']['max']
    df['sum_score'] = df['sum_score']/max_score*100

    df = df.sort_values(['sum_score'], ascending=False)
    df = df.loc[:, ('provinceLoc', 'cityLoc', 'college',
                    'majorName', 'preRanking', 'sum_score')]

    return df


# 示例调用
# rec(1,672,'北京市',1,[['文学',None]],1,1)
# rec(2,660,'江苏省',1,[['理学',None],['工学','计算机类'],['工学','电子信息类']],1,1)
