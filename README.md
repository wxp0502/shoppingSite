# 电子商务网站

- 功能介绍：
  - 游客：
    - 浏览商品
  - 用户：
    -  注册、登录、注销
    - 浏览商品、可添加至购物车
    - 购物车功能（增加、移除商品）
    - 购买商品（发送邮箱确认收货）
    - 查看完成订单
  - 管理员：
    - 所有用户功能
    - 商品目录的管理（增加、删除、修改）
    - 查看销售报表（所有商品的销量以及销售额）
    - 查看用户日志（订单历史、购物车列表）
- 开发环境：
  - python 3.9.7
  - PostgreSQL 12
- 所用框架：
  - 前端：bootstrap4.0
  - 后端：django4.0
- 结构说明：
  - users：实现用户登录、注册、注销功能
  - mall：实现商务网站功能
  - shoppingSite：项目配置文件
  - media：商品照片存放
  - manage.py：管理程序（接受命令并执行，诸如使用数据库和运行服务器等任务）
- 使用说明：
  - clone 项目之后
  - pip install -r requirements.txt
  - python manage.py runserver
- 作者：
  - 学号：201930343469
  - 姓名：温晓平
