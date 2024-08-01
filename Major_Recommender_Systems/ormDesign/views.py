
# Create your views here.
import random

from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
import sqlite3 as db
from . import models
projectName = 'rec2021'






def readDB(exeCMD):
    '''数据库查询标准函数'''
    pdir = os.path.dirname(os.getcwd())  # 获取父目录
    sql_file = os.path.join(pdir, projectName, 'db.sqlite3')  # 获取数据库文件路径
    print(sql_file)
    try:
        # 该 API 打开一个到SQLite数据库文件的链接，如果成功打开，则返回一个连接对象
        conn = db.connect(sql_file)
        c = conn.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
        cursor = c.execute(exeCMD)  # 该例程执行一个 SQL 语句
        rows = cursor.fetchall()  # 该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，返回空列表。
        return rows  # 输出查询结果
    except Exception as e:
        print(e)
        print('查询数据失败')
    finally:
        conn.close()  # 关闭数据库


def readMajors(request):
    exeCMD1 = 'select provinceName, COUNT(1) from Majors left join Provinces on Majors.provinceID_id = Provinces.provinceID group by provinceID_id order by COUNT(1) DESC'
    rows1 = readDB(exeCMD1)
    exeCMD2 = 'select provinceName, COUNT(1) from Rankings left join Provinces on Rankings.provinceID_id = Provinces.provinceID group by provinceID_id order by COUNT(1) DESC'
    rows2 = readDB(exeCMD2)
    tempdict = {}
    for r1 in rows1:
        for r2 in rows2:
            if r1[0] == r2[0]:
                tempdict[r1[0]] = f'专业录取数据{r1[1]}条，排名数据{r2[1]}条'

    exeCMD3 = 'select collegeName, COUNT(1) from Majors left join Colleges on Majors.collegeID_id = Colleges.collegeID group by collegeID_id order by COUNT(1) DESC'
    rows3 = readDB(exeCMD3)
    cdict = {}
    for r3 in rows3:
        cdict[r3[0]] = f'专业录取数据{r3[1]}条'
    return render(request, 'dataStatistics.html', {'Majors': tempdict, 'Colleges': cdict})


def recResuts(request):
    # 测试数据，需要从数据库读取相关数据，以返回推荐结果
    request.encoding = 'utf-8'
    province = request.GET.get("select_province", '')
    category = request.GET.get("select_category", '')
    score = request.GET.get("score", '')
    university_id = str(random.randint(1, 100))
    message = f'测试数据: 你在{province}{category}的省排名为{score}，可以上全国第{university_id}的学校了，恭喜你！'
    return HttpResponse(message)


def recResutsPost(request):
    # 测试数据，需要从数据库读取相关数据，以返回推荐结果
    request.encoding = 'utf-8'
    province = request.POST.get("select_province", '')
    category = request.POST.get("select_category", '')
    score = request.POST.get("score", '')
    university_id = str(random.randint(1, 100))
    message = f'测试数据: 你在{province}{category}的省排名为{score}，可以上全国第{university_id}的学校了，恭喜你！'
    return HttpResponse(message)
def getProvinces(request):
    df = pd.read_csv('./Data/province.csv')
    num = df.shape[0]
    for i in range(num):
        c1 = models.Provinces(provinceID=df.at[i,"provinceID"],
                           provinceName=df.at[i,"provinceName"]
                           )
        c1.save()
    return HttpResponse("Provinces in!")
def getColleges(request):
    df = pd.read_csv('./Data/college.csv', encoding='gbk')
    num = df.shape[0]
    for i in range(num):
        c1 = models.Colleges(collegeID=df.at[i, 'collegeID'],
                           collegeName=df.at[i, 'collegeName'],
                           provinceID=models.Provinces.objects.get(provinceID=df.at[i, 'provinceID']),
                           project985=df.at[i, 'project985'],
                           project211=df.at[i, 'project211'],
                           top=df.at[i,"top"]
                           )
        c1.save()
    return HttpResponse("Colleges in!")
def getCategory(request):
    c1 = models.Category(categoryID=1, categoryname="文科")
    c1.save()
    c1 = models.Category(categoryID=2, categoryname="理科")
    c1.save()
    c1 = models.Category(categoryID=3, categoryname="综合")
    c1.save()
    return HttpResponse("Category in!")


def getMajors(request):
    df = pd.read_csv('./Data/major.csv', encoding='gbk')
    num = df.shape[0]
    for i in range(num):
        c1 = models.Majors(majorName=df.at[i, 'majorName'],
                           year=df.at[i, 'year'],
                           id=i,
                           categoryID=models.Category.objects.get(categoryID=df.at[i, 'categoryID']),
                           minScore=df.at[i, 'minScore'],
                           collegeID=models.Colleges.objects.get(collegeID=df.at[i, 'collegeID']),
                           provinceID=models.Provinces.objects.get(provinceID=df.at[i, 'provinceID']))
        c1.save()
    return HttpResponse("Majors in!")


def getAreas(request):
    df = pd.read_csv('./Data/colleges地域(精确到市).csv', encoding='gbk')
    num = df.shape[0]
    for i in range(num):
        c1 = models.Areas(collegeID=models.Colleges.objects.get(collegeID=df.at[i, 'collegeID']),
                           collegeName=df.at[i, 'collegeName'],
                           cityName=df.at[i, 'city'])
        c1.save()
    return HttpResponse("Areas in!")


def getRankings(request):
    df = pd.read_csv('./Data/ranking.csv', encoding='gbk')
    num = df.shape[0]
    for i in range(num):
        c1 = models.Rankings(
            provinceID=models.Provinces.objects.get(provinceID=df.at[i, 'provinceID']),
            categoryID=models.Category.objects.get(categoryID=df.at[i, 'categoryID']),
            
            year=df.at[i, 'year'],
            score=df.at[i, "score"],
            rank=df.at[i, "rank"]
        )
        c1.save()
        print(df.at[i, 'categoryID'])
    return HttpResponse("Rankings in!")
