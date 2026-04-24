# week2 project note 
### 感谢DeepSeek老师
### 思路：把"数据"和"操作"分开，这样修改某一部分时不影响其他部分。
___
### book类
1. 用类封装对象的好处:<br>数据和方法绑定在一起，以后想加功能，直接在类里加方法就好。<br>
2. 
```python
def to_dict(self) -> Dict:
```
```python
def from_dict(cls, data: Dict) -> 'Book':
```
- JSON 只能存基本类型（字符串、数字、列表、字典），不能直接存对象
- 保存时：对象 → 字典 → JSON
- 读取时：JSON → 字典 → 对象
___
### BookManager 类
1. 初始化 init<br>
- data_file 有默认值，但也可以传入其他路径
- 初始化时自动调用 load_books()，这样程序一启动就有数据
2. 加载数据 load_books<br>
- 三种异常处理
3. 添加图书 add_book<br>
- 每步都要 while True 循环:用户输入错了不能直接退出，要让他重新输
- isbn_exists 要单独写一个方法? 一个方法多处调用，避免代码重复
4. 查看所有图书 view_all_books<br>
- 为什么用.copy()?复制一份再排序，不影响原数据
```python
key=lambda b: b.title
```
- 按 title 属性来排序<br>
5. 查询图书 search_book<br>
- 按 ISBN 查询：精确匹配，必须完全一样
- 按书名查询：模糊匹配，用 in 判断关键词是否在书名中
- .lower()：转小写再比较，这样不管用户输入大小写都能搜到
6. 修改数量 update_quantity<br>
- 撤销逻辑：先记下旧值，保存失败就恢复，保证内存和文件一致
7. 批量导入 batch_import<br>
- 逻辑：逐条读取文件数据，检查重复、检查格式，最终统计成功和跳过数量
___
### main函数 菜单交互
- 为什么用 while True？程序要反复显示菜单，每次操作完回到主界面。只有选 0 才 break 退出
