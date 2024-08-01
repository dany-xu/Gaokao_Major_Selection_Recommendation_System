

# 文件结构说明：

**主体：Major_Recommender_Systems**

**功能模块：**

每一个功能模块对应一个app，现有模块：

+ ormDesign：对应数据库模块
+ recommender:对应推荐系统模块

**如想要加入新的app，采用以下基本步骤：**

+ Major_Recommender_Systems\Major_Recommender_Systems\settings.py中添加`<app_name>.apps.<apps文件下的类名>`
+ 在app目录下创建`urls.py,`在urlpatterns中添加view.py中的函数
+ 在Major_Recommender_Systems\Major_Recommender_Systems\urls.py,仿造urlpatterns前面的例子添加。

**更改模型的基本步骤：**

+ 编辑 `models.py` 文件，改变模型。
+ 运行 `python manage.py makemigrations `为模型的改变生成迁移文件。
+ 运行 `python manage.py migrate` 来应用数据库迁移。

**static:静态文件存放**

**templates：html文件存放**

# 跳转逻辑说明

首页 http://127.0.0.1:8000/ 

地图http://127.0.0.1:8000/map_test/

薪资就业率http://127.0.0.1:8000/major_info/

学校信息http://127.0.0.1:8000/college_info/

性格测试http://127.0.0.1:8000/psychological_test/

推荐结果界面http://127.0.0.1:8000/recommender/

