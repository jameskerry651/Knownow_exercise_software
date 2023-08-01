def remove_spaces(input_file, output_file):
    # 读取txt文本文件
    with open(input_file, 'r',encoding='utf-8') as file:
        content = file.read()

    # 删除所有空格
    content_without_spaces = content.replace(' ', '')

    # 保存处理后的内容到新文件
    with open(output_file, 'w',encoding='utf-8') as file:
        file.write(content_without_spaces)

if __name__ == "__main__":
    input_file = "./questions/xuanze.txt"
    output_file = "output.txt"

    remove_spaces(input_file, output_file)
