import re
import pandas as pd
import numpy as np

# 从txt文件读取数据
file_path = 'questions\panduan.txt'  # 替换为你的文件路径

# 题目 提取表达式
title_pattern = r"[0-9]{1,3}[\.．、][ a-zA-Z\u4e00-\u9fa5].*?[: 。）) °]\n"

# 从题目中提取答案和替换
answer_pattern = r"[×√]"

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        questions_text = file.read()
except FileNotFoundError:
    print("文件未找到或路径错误。")
    exit()

questions = []  # 所有题目
isCorrect = []  # 0表示错误，1表示正确

matches = re.findall(title_pattern, questions_text)

for x in matches:
    res = re.findall(answer_pattern,x)
    print(res)
    if res[0] == '√':
        isCorrect.append(1)
    else:
        isCorrect.append(0)

    questions.append(re.sub(answer_pattern,' ',x))
    
print(len(isCorrect))
print(len(questions))

# 写入csv
data = {
    "question": questions, 
    "answer": isCorrect, 
}
