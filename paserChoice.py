import re
import pandas as pd
import numpy as np
"""
从txt当中读取选择题的数据，然后正则匹配结果后保存到csv文件
保存形式：
question(string) | options(string) | answer(string) | isMultiChoice (int) | count(int)

options 有4-6个，用逗号隔开的字符串
answer 有4-6个大写字母，用逗号隔开
type 0表示单选，1表示多选
count 一共几个选项
"""

def extract_strings_from_text(file_path):
    result = []
    with open(file_path, 'r', encoding='utf-8') as file:
        current_string = ""
        for line in file:
            line = line.strip()  # 去除行首尾的空白字符（包括换行符）
            if line:  # 如果不是空行
                current_string += line  # 将当前行添加到当前字符串中
            else:  # 如果是空行，将当前字符串添加到结果列表，并清空当前字符串
                if current_string:
                    result.append(current_string)
                    current_string = ""
        # 添加最后一个字符串（如果文本没有以空行结尾）
        if current_string:
            result.append(current_string)
    return result


# 从txt文件读取数据
file_path = "./questions/output.txt"

# 题目 提取表达式(多行模式)
title_pattern = r"^[0-9]{1,3}[\.、].*"



# 从题目中提取答案和替换
answer_pattern = r"[（( ][A-G]{1,6}[ ）)]"

# 从选项中提取每一项, 
# !!!有部分小bug，建议修改文件本身



try:
    with open(file_path, 'r', encoding='utf-8') as file:
        questions_text = file.read()
except FileNotFoundError:
    print("文件未找到或路径错误。")
    exit()

# 正则表达式匹配题目和答案.
questions = []  # 所有题目
answers = []    # 所有答案
options = []    # 所有选项
type_ls = []    # 单选or 多选
count_ls = []   # 选项数量

# 匹配问题
problems = re.findall(title_pattern, questions_text,re.MULTILINE)
test_ls = []
for problem in problems:
    if len(problem)<5:
        print(f"该问题长度小于5： {problem}")
        continue
    qs = re.sub(answer_pattern,'( )', problem)  # 删除括号中的答案
    answer = re.findall(answer_pattern,problem.replace(" ", "")) # 提取括号中的答案
    print(answer)
    answer = re.sub(r'[^a-zA-Z]', '', answer[0])
    questions.append(qs)
    if len(answer)==0:
        print(f"该问题为提取到答案：{problem}")
    if len(answer)>1:
        tmp = []
        for i in answer:
            i = re.sub(r"[（）]",'',i)
            tmp.append(i)
        answers.append("".join(tmp))
    else:
        answers.append(re.sub(r"[（）]",'',answer[0]))

# 区分多选和单选题
for x in answers:
    if len(x)>1:
        type_ls.append(1)
    else:
        type_ls.append(0)

# --------------------------------匹配选项--------------------------------------------------------

# 整体选项 提取
options_pattern = r"A\..*[\n ]([B-G]\..*[ \n]){0,5}"

file_path = "./questions/options.txt"  # 替换为您要读取的txt文件路径

problemOptions = extract_strings_from_text(file_path)

print(f"选项的总数量：{len(problemOptions)}")

one_option_pattern = r"[A-Z]\.\s*([^A-Z]+)"
# 每一个problemOption都是一个4-6个选项组成的答案

sub_str_ls = ["B.", "C.", "D.", "E.", "F."]
for problemOpiton in problemOptions:
    option_ls = []
    front_position = 0
    for sub_str in sub_str_ls:
        back_position = problemOpiton.find(sub_str)
        if back_position==-1:
            option_ls.append(problemOpiton[front_position:])
            break
        option_ls.append(problemOpiton[front_position:back_position])
        front_position = back_position

    count_ls.append(len(option_ls))
    options.append(",".join(option_ls))

    
    

        


# count = 0
# for problemOption in problemOptions:
#     res = re.findall(one_option_pattern, problemOption) # 拿到所有的单个选项列表
#     count_ls.append(len(res))  # 选项数量
#     if len(res)<=3:
#         print(f"选项数量少于3：{problemOption}")
#         print(res)
#         count = count + 1
#     options.append(",".join(res))       # 组合成一个完整的选项
  
# print(f"有问题的选项{count}")



def remove_newlines_from_list(input_list):
    return [string.replace("\n", "") for string in input_list]

questions = remove_newlines_from_list(questions)
answers = remove_newlines_from_list(answers)
options = remove_newlines_from_list(options)


print(f"问题总数量：{len(questions)}")
print(f"答案总数量：{len(answers)}")
print(f"选项总数量：{len(options)}")
print(len(count_ls))
print(len(type_ls))
# 保存结果到csv
data = {
    "question": questions,
    "options": options,
    "answer": answers,
    "isMultiChoice": type_ls,
    "count": count_ls
}

df = pd.DataFrame(data)

df.to_csv("choice_data.csv",index=False,encoding="utf-8")
