# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 16:50:38 2021

@author: admin
"""

import jieba
import wordcloud
#读入所有文档并分词
def f1():
    with open('jd_comments.txt','r',encoding='UTF-8') as f:
        for line in f.readlines():
            print(jieba.lcut(line,cut_all=True))

#过滤停用词
def stopwordslist():
    stopwords=[line.strip() for line in open('stopwords_list.txt', encoding='UTF-8').readlines()]
    return stopwords
def separate(sentence):
    sentence_depart=jieba.lcut(sentence.strip())
    stopwords=stopwordslist()
    output=''
    for i in sentence_depart:
        if i in stopwords:
            continue
        else:
            if i !='\t':
                output +=i
                output +=" "
    return output
def f2():
    outputs=open("out.txt",'w',encoding='UTF-8')
    with open('jd_comments.txt','r',encoding='UTF-8') as f:
        for line in f:
            line_separate=separate(line)
            outputs.write(line_separate+'\n')
    outputs.close()

def produce_items():
    #统计词频
    with open('out.txt','r',encoding='UTF-8') as f:
        words=jieba.lcut(f.read())
        counts={}
        for word in words:
            if len(word)==1:
                continue
            else:
                counts[word]=counts.get(word,0)+1
        items=list(counts.items())
        items.sort(key=lambda x: x[1],reverse=True)
        return items
def f3(x):
    items=produce_items()
    characters=[]
    for i in range(20):
        word, count = items[i]
        if(x==1):            
            print("{}--{}".format(word, count))
        #根据词频进行特征词筛选，如只保留高频词，删除低频词，并得到特征词组成的特征集
        characters.append(word)
    return characters
   
def f4(x):
    #利用特征集为每一条评论生成向量表示，可以是0，1表示（one-hot)也可以是出现次数的表示
    characters=f3(0)
    with open('out.txt','r',encoding='UTF-8') as f:
        character_num=[[0 for i in range(20)] for i in range(1002)]
        num=0
        for line in f.readlines():
            line_depart=jieba.lcut(line.strip())
            for word in line_depart:
                for i in range(20):
                    if word==characters[i]:
                        character_num[num][i]+=1
                        i+=1
            num+=1
        if x==1:
            print(character_num)
        return character_num

def f5():
    distance=[[0 for i in range(1002)] for i in range(1002)]
    character_num=f4(0)
    for i in range(1002):
        for j in range(1002):
            x=0
            for k in range(20):
                x+=(character_num[i][k]-character_num[j][k])**2
            x=x**0.5
            distance[i][j]+=x
    print(distance)
        
def f6():
    #找到所有评论的“重心”
    character_num=f4(0)
    center=[0 for i in range(20)]
    for i in range(20):
        for j in range(1002):
            center[i]+=character_num[j][i]
        center[i]=center[i]/1002
    print(center)

def f7():
    #词云图
    items=produce_items()
    w = wordcloud.WordCloud(font_path='./fonts/simhei.ttf')
    character=[]
    for i in range(20):
        word, count = items[i]
        for j in range(count):
            character.append(word)
    w.generate(str(character))
    w.to_file('output1.png')


def main():
    #f1()
    #f2()
    characters=f3(1)
    print(characters)
    #character_num=f4(1)
    #f5()
    #f6()
    #f7()
    
if __name__ == '__main__':
    main()