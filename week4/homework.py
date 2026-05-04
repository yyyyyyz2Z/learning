from sqlalchemy import create_engine, String, Integer, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column

DB_URL = 'mysql+pymysql://root:123456@localhost/music'

engine = create_engine(DB_URL, echo=True)

class Base(DeclarativeBase):
    pass

class Singer(Base):
    __tablename__ = 'singers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(2), nullable=False)   
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    phone: Mapped[str] = mapped_column(String(11), nullable=False)
    debut_year: Mapped[int] = mapped_column(Integer, nullable=False)
    representative_song: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self):
        return f'<Singer {self.id}: {self.name}, {self.age}岁, {self.phone}>'


def task1():
    """题目1：单表CRUD + 手机号查重 + 扩展查询"""
    # 自动建表
    Base.metadata.create_all(engine)

    session = Session(engine)
    try:
        # ----- 4. 插入五名歌手（假设表此时为空）-----
        singers = [
            Singer(name='周杰伦', gender='男', age=45, phone='13800000001',
                   debut_year=2000, representative_song='七里香'),
            Singer(name='林俊杰', gender='男', age=43, phone='13800000002',
                   debut_year=2003, representative_song='江南'),
            Singer(name='邓紫棋', gender='女', age=32, phone='13800000003',
                   debut_year=2008, representative_song='光年之外'),
            Singer(name='刘若英', gender='女', age=53, phone='13800000004',
                   debut_year=1995, representative_song='后来'),
            Singer(name='李荣浩', gender='男', age=38, phone='13800000005',
                   debut_year=2010, representative_song='年少有为'),
        ]
        session.add_all(singers)
        session.commit()
        print("五名歌手插入成功")

        # ----- 5. 基础查询：年龄大于30岁的歌手 -----
        stmt = select(Singer).where(Singer.age > 30)
        result = session.execute(stmt).scalars().all()
        print("\n年龄大于30岁的歌手：")
        for singer in result:
            print(f"  姓名：{singer.name}，年龄：{singer.age}")

        # ----- 6. 按性别查询：所有女歌手 -----
        stmt = select(Singer).where(Singer.gender == '女')
        result = session.execute(stmt).scalars().all()
        print("\n女歌手：")
        for singer in result:
            print(f"  姓名：{singer.name}，代表作：{singer.representative_song}")

        # ----- 7. 排序查询：按出道年份升序 -----
        stmt = select(Singer).order_by(Singer.debut_year.asc())
        result = session.execute(stmt).scalars().all()
        print("\n按出道年份升序：")
        for singer in result:
            print(f"  姓名：{singer.name}，出道年份：{singer.debut_year}")

        # ----- 8. 更新操作：周杰伦年龄改为46 -----
        stmt = select(Singer).where(Singer.name == '周杰伦')
        zhou = session.execute(stmt).scalar_one()
        zhou.age = 46
        session.commit()
        print("\n周杰伦年龄已更新为46")

        # ----- 9. 更新代表作：邓紫棋改为《泡沫》-----
        stmt = select(Singer).where(Singer.name == '邓紫棋')
        deng = session.execute(stmt).scalar_one()
        deng.representative_song = '泡沫'
        session.commit()
        print("邓紫棋代表作已更新为《泡沫》")

        # ----- 10. 手机号查重：尝试插入刘德华（手机号已存在）-----
        phone_liu = '13800000001'   
        exists = session.execute(select(Singer).where(Singer.phone == phone_liu)).scalar_one_or_none()
        if exists:
            print(f"插入失败：手机号{phone_liu}已存在")
        else:
            liu = Singer(name='刘德华', gender='男', age=55, phone=phone_liu,
                         debut_year=1985, representative_song='忘情水')
            session.add(liu)
            session.commit()
            print("刘德华插入成功")

        # ----- 11. 插入陈奕迅（手机号不存在，应成功）-----
        phone_chen = '13800000006'
        exists = session.execute(select(Singer).where(Singer.phone == phone_chen)).scalar_one_or_none()
        if exists:
            print(f"插入失败：手机号{phone_chen}已存在")
        else:
            chen = Singer(name='陈奕迅', gender='男', age=50, phone=phone_chen,
                          debut_year=1996, representative_song='十年')
            session.add(chen)
            session.commit()
            print("陈奕迅插入成功")

        # ----- 12. 删除邓紫棋 -----
        stmt = select(Singer).where(Singer.name == '邓紫棋')
        deng = session.execute(stmt).scalar_one_or_none()
        if deng:
            session.delete(deng)
            session.commit()
            print("邓紫棋已被删除")

        # ----- 13. 再次查询所有歌手，验证结果 -----
        stmt = select(Singer)
        all_singers = session.execute(stmt).scalars().all()
        print("\n===== 当前所有歌手 =====")
        for s in all_singers:
            print(f"ID:{s.id} 姓名:{s.name} 年龄:{s.age} 手机号:{s.phone} 出道:{s.debut_year} 代表作:{s.representative_song}")
        print(f"共 {len(all_singers)} 人（预期：周杰伦、林俊杰、刘若英、李荣浩、陈奕迅）")

    except Exception as e:
        session.rollback()
        print("发生错误，已回滚:", e)
    finally:
        session.close()


def task2():
    """题目2：事务自动回滚（with session.begin()）"""
    session = Session(engine)
    try:
        session.query(Singer).filter(Singer.phone == '13800000006').delete()
        session.commit()
    except:
        pass
    finally:
        session.close()

    session = Session(engine)
    try:
        # 使用 with session.begin() 开启自动事务
        with session.begin():
            # 查询手机号是否存在
            exists = session.execute(select(Singer).where(Singer.phone == '13800000006')).scalar_one_or_none()
            if exists:
                print("手机号13800000006已存在，跳过插入（本应不存在）")
            else:
                # 插入王菲
                wangfei = Singer(name='王菲', gender='女', age=55, phone='13800000006',
                                 debut_year=1989, representative_song='天空')
                session.add(wangfei)
                print("王菲已添加到会话，尚未提交")
                # 故意抛出异常，触发回滚
                raise Exception("模拟出错，事务应回滚")
    except Exception as e:
        print("事务已回滚，原因:", e)

    result = session.execute(select(Singer).where(Singer.phone == '13800000006')).scalar_one_or_none()
    if result is None:
        print(" 验证通过：王菲没有被插入，事务回滚生效")
    else:
        print(" 验证失败：王菲被插入了", result)
    session.close()


if __name__ == '__main__':
    print("========== 题目1 开始 ==========")
    task1()
    print("\n========== 题目2 开始 ==========")
    task2()
