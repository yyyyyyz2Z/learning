# 后端第四次培训作业

## 一、总体说明

本次作业分为三个部分：
- 题目1 & 题目2：使用 SQLAlchemy 操作 MySQL 数据库，完成单表 CRUD、手机号查重、事务自动回滚等。
- 题目3：使用 PyMySQL 演示 SQL 注入攻击及参数化查询的防御方法。
---

## 二、homework.py 注释详解

### 2.1 数据库连接与模型定义
```python
DB_URL = 'mysql+pymysql://root:123456@localhost/music'
engine = create_engine(DB_URL, echo=True)
```
- 使用 SQLAlchemy 的 create_engine 创建数据库引擎，echo=True 会在控制台打印所有生成的 SQL 语句
- 连接字符串格式：mysql+pymysql://用户名:密码@主机/数据库名
- 模型字段类型与 SQL 类型对应（String、Integer）
- nullable=False 表示该字段不能为 NULL

### 2.2 task1() – 题目1

#### 自动建表
```python
Base.metadata.create_all(engine)
```
- 检查数据库中是否存在 singers 表，若不存在则根据模型定义创建

#### 插入五名歌手
```python
session.add_all(singers)
session.commit()
```
- 使用 add_all 批量添加对象，最后提交事务

#### 基础查询（年龄 > 30）
```python
stmt = select(Singer).where(Singer.age > 30)
result = session.execute(stmt).scalars().all()
```
- 使用 select() 构建查询，session.execute() 执行，scalars().all() 获取对象列表

#### 按性别查询、排序查询
```python
# 女歌手
stmt = select(Singer).where(Singer.gender == '女')
# 按出道年份升序
stmt = select(Singer).order_by(Singer.debut_year.asc())
```
- order_by() 可接受 .asc() 或 .desc() 控制排序方向

#### 更新操作
```python
zhou = session.execute(select(Singer).where(Singer.name == '周杰伦')).scalar_one()
zhou.age = 46
session.commit()
```
- 先查询出对象，修改属性后提交，SQLAlchemy 会自动生成 UPDATE 语句

#### 手机号查重逻辑
```python
exists = session.execute(select(Singer).where(Singer.phone == phone_liu)).scalar_one_or_none()
if exists:
    print("插入失败...")
else:
    session.add(new_singer)
    session.commit()
```
- scalar_one_or_none() 返回一个结果或 None，用于判断是否存在

#### 删除操作
```python
session.delete(deng)
session.commit()
```
- 直接删除对象

### 2.3 task2() – 题目2 事务自动回滚
```python
with session.begin():
    # 插入王菲
    # 故意抛异常
    raise Exception("模拟出错")
```
- with session.begin(): 会在代码块结束时自动提交，如果块内抛出异常则自动回滚
- 这是 SQLAlchemy 推荐的简便事务管理方式，无需显式调用 commit() 或 rollback()
- 故意抛出异常，验证回滚效果，最后查询确认王菲没有被插入

---

## 三、homework_pymysql.py 注释详解

### 3.1 连接配置与光标类型
```python
DB_CONFIG = {
    ...
    'cursorclass': pymysql.cursors.DictCursor
}
```
- 使用字典游标：查询结果以字典形式返回，键为列名，值为字段值。

### 3.2 插入测试歌手
```python
cursor.execute(insert_sql, ('测试歌手', '保密', 20, '13800000099', 2020, '测试歌曲'))
```
- PyMySQL 的参数化写法：SQL 中使用 %s 作为占位符，第二个参数传入元组。

### 3.3 SQL 注入演示

#### 恶意输入
```python
malicious_input = "测试歌手 OR '1' = '1'"
```
- 目的是让拼接后的 SQL 变成 ... WHERE name = '测试歌手 OR '1'='1'，但实际上由于单引号闭合，会变成：
  ... WHERE name = '测试歌手' OR '1'='1'，从而返回所有记录。

#### 错误方式（f-string 拼接）
```python
unsafe_sql = f"SELECT * FROM singers WHERE name = '{malicious_input}'"
cursor.execute(unsafe_sql)
```
- 直接将恶意字符串嵌入 SQL，破坏了原有语义，导致查询所有歌手（数据泄漏）

#### 正确方式（参数化查询）
```python
safe_sql = "SELECT * FROM singers WHERE name = %s"
cursor.execute(safe_sql, (malicious_input,))
```
- 数据库驱动会对参数进行转义或特殊处理，将其视为纯文本值，不会改变 SQL 结构。
- 因此即使输入包含 OR '1'='1'，它也只会当作普通字符串去匹配 name 字段，不会返回额外记录。

### 3.4 为什么参数化能防注入？

- SQL 语句结构与数据内容完全分离。
- 数据库驱动会对参数中的特殊字符（如单引号、分号、注释符等）进行转义，或者使用二进制协议传递，使数据库无法将用户输入解析为 SQL 指令。
