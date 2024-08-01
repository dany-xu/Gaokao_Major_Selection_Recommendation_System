from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
# Create your views here.
def index(request):
    print(request.GET)
    return render(request,"test.html")

def map(request):
    return render(request,"maptest.html")
"""
def test(request):
    print(request.GET)
    result={"college":"清华大学","major":"计算机系"}
    #return render(request,"test.html",{"result":result})
    return JsonResponse(result)
"""
def college_info(request):
    college_info=pd.read_csv('Data/学校信息汇总.csv')
    return JsonResponse({"college_info":college_info.values.tolist()})   
def major_info(request):
    major_info=pd.read_csv('Data/专业信息汇总.csv',encoding='gbk')
    return JsonResponse({"major_info":major_info.values.tolist()})
def psychological_test(request):
    return render(request,"psychological_test.html")
