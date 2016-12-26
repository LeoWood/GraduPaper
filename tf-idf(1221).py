# -*- coding: utf-8 -*-

import math


def GetLines(path):
    lines = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines()
            if line != '':
                line = line.strip()
                lines.append(line)
    return lines


def GetWords(lines, stoplist):
    l_list = []
    for line in lines:
        word_list = line.split('/')
        w_list = []
        for word in word_list:
            if word not in ['', ' ']:
                if word not in stoplist:
                    w_list.append(word)
        l_list.append(w_list[:-1])
    return l_list


def Idf(word, l_list):
    count = 0
    for l in l_list:
        if word in l:
            count += 1
    idf = math.log(len(l_list)/(1+count))
    return idf


def TfIdf():
    lines = GetLines('20161101-20161130.txt')
    stoplist = GetLines('stopword1.txt')
    i = 0
    l_list = GetWords(lines, stoplist)
    for l in l_list:
        i += 1
        tf_list = []
        for w in l:
            tf = l.count(w)/len(l)
            idf = Idf(w, l_list)
            tf_idf = round(tf*idf, 6)
            tf_list.append(w+'\t'+str(tf_idf))
        with open('F:\\毕业论文\\test\\test201611(new)\\'+str(i)+'.txt', 'w', encoding='utf-8') as f:
            for new in tf_list:
                f.write(new+'\n')
        print(str(i)+' done.')


def main():
    TfIdf()


if __name__ == '__main__':
    main()
