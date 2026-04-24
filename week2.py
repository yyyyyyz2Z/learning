"""
图书管理系统（简易版）
支持添加、查看、查询、修改、删除图书，数据持久化到JSON文件
"""

import json
import os
from typing import List, Dict, Optional


class Book:
    """图书类，封装图书信息"""
    
    def __init__(self, isbn: str, title: str, author: str, quantity: int):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.quantity = quantity
    
    def to_dict(self) -> Dict:
        """转换为字典，便于JSON序列化"""
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'quantity': self.quantity
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Book':
        """从字典创建Book对象"""
        return cls(
            isbn=data['isbn'],
            title=data['title'],
            author=data['author'],
            quantity=data['quantity']
        )
    
    def __str__(self) -> str:
        return f"ISBN: {self.isbn} | 书名: 《{self.title}》 | 作者: {self.author} | 数量: {self.quantity}"


class BookManager:
    """图书管理器，处理所有图书操作"""
    
    def __init__(self, data_file: str = "books.json"):
        self.data_file = data_file
        self.books: List[Book] = []
        self.load_books()
    
    def load_books(self) -> None:
        """从JSON文件加载图书信息"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(item) for item in data]
                print(f"✓ 成功加载 {len(self.books)} 本图书信息")
            else:
                print("ℹ 数据文件不存在，将创建新文件")
                self.books = []
        except json.JSONDecodeError:
            print("✗ 数据文件格式错误，将使用空数据")
            self.books = []
        except Exception as e:
            print(f"✗ 加载数据失败: {e}")
            self.books = []
    
    def save_books(self) -> bool:
        """保存图书信息到JSON文件"""
        try:
            data = [book.to_dict() for book in self.books]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"✗ 保存失败: {e}")
            return False
    
    def is_isbn_exists(self, isbn: str) -> bool:
        """检查ISBN是否已存在"""
        return any(book.isbn == isbn for book in self.books)
    
    def add_book(self) -> None:
        """添加图书"""
        print("\n--- 添加图书 ---")
        
        # 输入ISBN并验证
        while True:
            isbn = input("请输入图书编号(ISBN): ").strip()
            if not isbn:
                print("✗ ISBN不能为空，请重新输入")
                continue
            if self.is_isbn_exists(isbn):
                print(f"✗ ISBN '{isbn}' 已存在，请使用其他编号")
                continue
            break
        
        # 输入书名
        while True:
            title = input("请输入书名: ").strip()
            if not title:
                print("✗ 书名不能为空，请重新输入")
                continue
            break
        
        # 输入作者
        while True:
            author = input("请输入作者: ").strip()
            if not author:
                print("✗ 作者不能为空，请重新输入")
                continue
            break
        
        # 输入数量
        while True:
            try:
                quantity = int(input("请输入数量: ").strip())
                if quantity < 0:
                    print("✗ 数量不能为负数，请重新输入")
                    continue
                break
            except ValueError:
                print("✗ 请输入有效的整数")
        
        # 创建并添加图书
        new_book = Book(isbn, title, author, quantity)
        self.books.append(new_book)
        
        if self.save_books():
            print(f"✓ 图书《{title}》添加成功！")
        else:
            print("⚠ 图书已添加但保存失败")
    
    def view_all_books(self, sort_by: Optional[str] = None) -> None:
        """查看所有图书，支持排序"""
        if not self.books:
            print("\n📚 暂无图书信息")
            return
        
        print(f"\n--- 图书列表（共 {len(self.books)} 本） ---")
        
        # 排序处理
        books_to_display = self.books.copy()
        if sort_by == 'title':
            books_to_display.sort(key=lambda b: b.title)
            print("【按书名排序】")
        elif sort_by == 'author':
            books_to_display.sort(key=lambda b: b.author)
            print("【按作者排序】")
        
        # 显示图书
        for i, book in enumerate(books_to_display, 1):
            print(f"{i}. {book}")
    
    def search_book(self) -> None:
        """查询图书（按ISBN或书名）"""
        print("\n--- 查询图书 ---")
        print("1. 按ISBN查询")
        print("2. 按书名查询")
        
        try:
            choice = int(input("请选择查询方式(1-2): ").strip())
        except ValueError:
            print("✗ 输入无效")
            return
        
        if choice == 1:
            isbn = input("请输入ISBN: ").strip()
            found = [book for book in self.books if book.isbn == isbn]
        elif choice == 2:
            title = input("请输入书名关键词: ").strip()
            found = [book for book in self.books if title.lower() in book.title.lower()]
        else:
            print("✗ 无效选择")
            return
        
        if found:
            print(f"\n✓ 找到 {len(found)} 本图书:")
            for book in found:
                print(f"  {book}")
        else:
            print("✗ 未找到相关图书")
    
    def update_quantity(self) -> None:
        """修改图书数量"""
        print("\n--- 修改图书数量 ---")
        isbn = input("请输入要修改的图书ISBN: ").strip()
        
        for book in self.books:
            if book.isbn == isbn:
                print(f"当前信息: {book}")
                while True:
                    try:
                        new_quantity = int(input("请输入新的数量: ").strip())
                        if new_quantity < 0:
                            print("✗ 数量不能为负数")
                            continue
                        old_quantity = book.quantity
                        book.quantity = new_quantity
                        if self.save_books():
                            print(f"✓ 数量已从 {old_quantity} 修改为 {new_quantity}")
                        else:
                            book.quantity = old_quantity
                            print("✗ 保存失败，修改已撤销")
                        return
                    except ValueError:
                        print("✗ 请输入有效的整数")
        
        print(f"✗ 未找到ISBN为 '{isbn}' 的图书")
    
    def delete_book(self) -> None:
        """删除图书"""
        print("\n--- 删除图书 ---")
        isbn = input("请输入要删除的图书ISBN: ").strip()
        
        for i, book in enumerate(self.books):
            if book.isbn == isbn:
                print(f"确认删除: {book}")
                confirm = input("确认删除？(y/n): ").strip().lower()
                if confirm == 'y':
                    deleted_book = self.books.pop(i)
                    if self.save_books():
                        print(f"✓ 图书《{deleted_book.title}》已删除")
                    else:
                        self.books.insert(i, deleted_book)
                        print("✗ 保存失败，删除已撤销")
                else:
                    print("操作已取消")
                return
        
        print(f"✗ 未找到ISBN为 '{isbn}' 的图书")
    
    def batch_import(self) -> None:
        """批量导入图书（从JSON文件）"""
        print("\n--- 批量导入 ---")
        file_path = input("请输入导入文件路径(默认: import_books.json): ").strip()
        
        if not file_path:
            file_path = "import_books.json"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            imported_count = 0
            skipped_count = 0
            
            for item in data:
                try:
                    book = Book.from_dict(item)
                    if not self.is_isbn_exists(book.isbn):
                        self.books.append(book)
                        imported_count += 1
                    else:
                        skipped_count += 1
                except (KeyError, ValueError) as e:
                    print(f"⚠ 跳过无效数据: {item} - {e}")
            
            if self.save_books():
                print(f"✓ 导入完成: 成功 {imported_count} 本, 跳过(重复) {skipped_count} 本")
            else:
                print("✗ 保存失败")
                
        except FileNotFoundError:
            print(f"✗ 文件 '{file_path}' 不存在")
        except json.JSONDecodeError:
            print("✗ 文件格式错误，请确保是有效的JSON格式")
        except Exception as e:
            print(f"✗ 导入失败: {e}")


def show_menu() -> None:
    """显示主菜单"""
    print("\n" + "=" * 50)
    print("           图书管理系统（简易版）")
    print("=" * 50)
    print("1. 添加图书")
    print("2. 查看所有图书")
    print("3. 查询图书")
    print("4. 修改图书数量")
    print("5. 删除图书")
    print("6. 按书名排序查看")
    print("7. 按作者排序查看")
    print("8. 批量导入图书")
    print("0. 退出系统")
    print("-" * 50)


def main() -> None:
    """主程序"""
    manager = BookManager()
    
    while True:
        show_menu()
        
        try:
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                manager.add_book()
            elif choice == '2':
                manager.view_all_books()
            elif choice == '3':
                manager.search_book()
            elif choice == '4':
                manager.update_quantity()
            elif choice == '5':
                manager.delete_book()
            elif choice == '6':
                manager.view_all_books(sort_by='title')
            elif choice == '7':
                manager.view_all_books(sort_by='author')
            elif choice == '8':
                manager.batch_import()
            elif choice == '0':
                print("\n感谢使用图书管理系统，再见！")
                break
            else:
                print("✗ 无效选择，请输入0-8之间的数字")
                
        except KeyboardInterrupt:
            print("\n\n系统已中断")
            break
        except Exception as e:
            print(f"✗ 发生未知错误: {e}")


if __name__ == "__main__":
    main()