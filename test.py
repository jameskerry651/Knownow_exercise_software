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

if __name__ == "__main__":
    file_path = "options.txt"  # 替换为您要读取的txt文件路径

    string_list = extract_strings_from_text(file_path)

    # 输出提取的字符串列表
    print(string_list)
    print(len(string_list))
