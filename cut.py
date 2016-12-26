# -*- coding: utf-8 -*-
import jieba


# ReadFiles
def ReadTxt(path):
    file_in = open(path, 'r', encoding='utf-8')
    con = []
    for line in file_in.readlines():
        line = line.strip()
        con.append(line)
    file_in.close()
    return con


# write to txt
def WriteToFile(path, text):
    file_out = open(path, 'w', encoding='utf-8')
    file_out.write(text)
    file_out.close()


# 切词
def word_cut(lines):
    l_list = []
    for line in lines:
        line = '/'.join(jieba.cut(line))
        l_list.append(line)
    return l_list


def main():
    path = r'F:\毕业论文\test\tf-idf\20161101-20161130.txt'
    text = ReadTxt(path)
    l_list = word_cut(text)
    file_out = open(path, 'w', encoding='utf-8')
    for line in l_list:
        file_out.write(line+'\n')
    file_out.close()
    print('done')


if __name__ == '__main__':
    main()
