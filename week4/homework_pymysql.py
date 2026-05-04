import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'music',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor   
}

def task_pymysql():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            #如果已存在先删除
            cursor.execute("DELETE FROM singers WHERE phone = '13800000099'")
            insert_sql = """
                INSERT INTO singers (name, gender, age, phone, debut_year, representative_song)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, ('测试歌手', '保密', 20, '13800000099', 2020, '测试歌曲'))
            conn.commit()
            print("测试歌手插入成功")

            # 3. 定义恶意输入
            malicious_input = "测试歌手 OR '1' = '1'"

            # 4. 错误方式：使用 f-string 拼接 SQL（存在注入风险）
            print("\n===== 错误方式（f-string拼接）=====")
            unsafe_sql = f"SELECT * FROM singers WHERE name = '{malicious_input}'"
            print(f"执行的SQL: {unsafe_sql}")
            cursor.execute(unsafe_sql)
            unsafe_result = cursor.fetchall()
            print(f"查询结果数: {len(unsafe_result)}")
            for row in unsafe_result:
                print(row)

            # 5. 正确方式：使用 %s 占位符 + 参数元组（安全）
            print("\n===== 正确方式（参数化查询）=====")
            safe_sql = "SELECT * FROM singers WHERE name = %s"
            print(f"执行的SQL: {safe_sql}，参数: ('{malicious_input}',)")
            cursor.execute(safe_sql, (malicious_input,))
            safe_result = cursor.fetchall()
            print(f"查询结果数: {len(safe_result)}")
            for row in safe_result:
                print(row)

            # 6. 注释说明
            print("\n" + "="*60)
            print("【为什么参数化能防注入？】")
            print("参数化查询将SQL语句结构与数据内容分离。")
            print("数据库驱动会对参数中的特殊字符（如单引号、分号、OR等）进行转义或当成纯数据处理，")
            print("而不会将其解释为SQL指令的一部分。")
            print("因此，即使参数中包含 ' OR '1'='1'，它也只会被当作普通字符串值去匹配字段，")
            print("而不会改变原有SQL的查询逻辑，从而避免了数据泄漏或恶意操作。")
            print("="*60)

    except Exception as e:
        print("发生错误:", e)
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    task_pymysql()
