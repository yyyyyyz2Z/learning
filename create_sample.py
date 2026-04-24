import json

sample_books = [
    {
        "isbn": "978-7-111-70444-3",
        "title": "Python编程从入门到实践",
        "author": "Eric Matthes",
        "quantity": 5
    },
    {
        "isbn": "978-7-121-35577-4",
        "title": "利用Python进行数据分析",
        "author": "Wes McKinney",
        "quantity": 2
    }
]

with open('import_books.json', 'w', encoding='utf-8') as f:
    json.dump(sample_books, f, ensure_ascii=False, indent=2)

print("✓ 示例文件已生成: import_books.json")
