import pandas as pd

# 读取Excel文件
data = pd.read_excel('热搜数据.xlsx')

# 生成唯一的平台+榜单组合
unique_combinations = set()
for index, row in data.iterrows():
    platform = row['platform']
    list_name = row['slist'] if pd.notna(row['slist']) else ''
    unique_combinations.add((platform, list_name))

# 将组合排序
sorted_combinations = sorted(unique_combinations)

# 将组合存储到txt文件中
with open('Directory.txt', 'w', encoding='utf-8') as f:
    for platform, list_name in sorted_combinations:
        f.write(f"{platform},{list_name}\n")

print("目录已保存到Directory.txt文件中")
