import re
import jieba
import matplotlib.pyplot as plt
import numpy as np
#定义清洗函数，去除噪声url，结果写入新文档test1.txt
def delete_url():
    f=open('weibo.txt','r',encoding='UTF-8')
    s=f.read()
    results=re.compile(r'http://[a-zA-Z0-9.?/&=:]*',re.S)
    dd=results.sub("",s)
    f.close()
    d=open('test1.txt','w',encoding='UTF-8')
    d.write(dd)
    d.close()

#定义停用词表
def stopwordslist():
    stopwords=[line.strip() for line in open('stopwords_list.txt', encoding='UTF-8').readlines()]
    return stopwords
#定义分词函数
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

#将情绪词典加入Jieba的自定义词典，调用分词函数，得到的结果写入新文档test2.txt
def f1():
    with open("test1.txt","r",encoding='UTF-8') as f:
        d=open('test2.txt','w',encoding='UTF-8')
        jieba.load_userdict("anger.txt")
        jieba.load_userdict("disgust.txt")
        jieba.load_userdict("fear.txt")
        jieba.load_userdict("joy.txt")
        jieba.load_userdict("sadness.txt")
        for line in f:
            line_separate=separate(line)
            d.write(line_separate+"\n")
        d.close()
#利用闭包实现两个函数，返其情绪向量或情绪值
def f2(sign1,sign2):
    anger=[]
    disgust=[]
    fear=[]
    joy=[]
    sadness=[]
    with open("anger.txt","r",encoding='UTF-8') as f:
        for line in f:
            anger.append(line.strip('\n'))
    with open("disgust.txt","r",encoding='UTF-8') as f:
        for line in f:
            disgust.append(line.strip('\n'))
    with open("fear.txt","r",encoding='UTF-8') as f:
        for line in f:
            fear.append(line.strip('\n'))
    with open("joy.txt","r",encoding='UTF-8') as f:
        for line in f:
            joy.append(line.strip('\n'))
    with open("sadness.txt","r",encoding='UTF-8') as f:
        for line in f:
            sadness.append(line.strip('\n'))
    character_num=[]
    character_proportion=[]
#认为一条微博的情绪是混合的，即一共有n个情绪词，如果joy有n1个，则joy的比例是n1/n
    def f2_1():
        nonlocal anger,disgust,fear,joy,sadness,character_num,character_proportion,sign1,sign2
        with open('test2.txt','r',encoding='UTF-8') as f:
            d=open("test3.txt","w",encoding='UTF-8')
            for line in f.readlines():
                line_depart=jieba.lcut(line.strip())     
                n=0;n1=0;n2=0;n3=0;n4=0;n5=0
                for word in line_depart:
                    if word in anger:
                        n+=1
                        n1+=1
                    if word in disgust:
                        n+=1
                        n2+=1
                    if word in fear:
                        n+=1
                        n3+=1
                    if word in joy:
                        n+=1
                        n4+=1
                    if word in sadness:
                        n+=1
                        n5+=1
                if n==0:#无情绪的评论直接删除
                    continue
                else:
                    d.write(line)
                    list1=[]
                    list2=[]
                    list1.append(n1/n);list1.append(n2/n);list1.append(n3/n);list1.append(n4/n);list1.append(n5/n)
                    list2.append(n1);list2.append(n2);list2.append(n3);list2.append(n4);list2.append(n5)
                    character_proportion.append(list1)
                    character_num.append(list2)
            d.close()
        if sign2==1:
            print(character_proportion)
        return character_num
    if sign1:
        return f2_1
    else:       
#二是认为一条微博的情绪是唯一的
        def f2_2():
            character=['anger','disgust','fear','joy','sadness']
            character_num1=f2(1,0)()
            length=len(character_num1)
            for i in range(length):
                x=max(character_num1[i])
            for j in range(5):
                if character_num1[i][j]==x:#如果不同情绪的情绪词出现数目一样，同时显示
                    print(character[j],end=" ")
                    print("\n")
        return f2_2
#实现了小时模式和日模式，string是hour和day，num1到5代表情绪，sign表示是否画图
def f3(string,num,sign):
    character_num=f2(1,0)()
    with open('test3.txt','r',encoding='UTF-8') as f:
        if string=='hour':
            total=[0 for i in range(24)]
            emotion_num=[0 for i in range(24)]
            emotion_proportion=[0 for i in range(24)]
            reg=r"Oct\s\s\s\d\d\s\s\s\d\d"
            i=0
            for line in f.readlines():
                m=re.finditer(reg,line)
                for j in m:
                    x=int(j.group(0)[11:13])
                    emotion_num[x]+=character_num[i][num-1]
                    for k in range(5):
                        total[x-1]+=character_num[i][k]
                i+=1
            for p in range(24):
                emotion_proportion[p]+=emotion_num[p]/total[p]
            print(emotion_proportion)
            hour=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
            if sign:
                plt.plot(hour,emotion_proportion)
        elif string=='day':
            total=[0 for i in range(3)]
            emotion_num=[0 for i in range(3)]
            emotion_proportion=[0 for i in range(3)]
            reg=r"\w\w\w\s\s\sOct"
            i=0
            for line in f.readlines():
                m=re.finditer(reg,line)
                for j in m:
                    x=str(j.group(0)[0:3])
                    if x=='Fri':
                        y=0
                    elif x=='Sat':
                        y=1
                    else:
                        y=2
                    emotion_num[y]+=character_num[i][num-1]
                    for k in range(5):
                        total[y]+=character_num[i][k]
                i+=1
            for p in range(3):
                emotion_proportion[p]+=emotion_num[p]/total[p]
            print(emotion_proportion)
            day=np.array([5,6,7])
            if sign:
                plt.plot(day,emotion_proportion)
#情绪空间分布，取北京市中心经纬度做中心，distance表示半径，单位是千米，num1到5表示情绪
def f4(distance,num):
    center=[39.90555,116.424722]
    character_num=f2(1,0)()
    proportion=[]
    emotion_total=0;emotion=0;emotion_num=0
    with open('test3.txt','r',encoding='UTF-8') as f:
        reg1=r"\d+(\.\d+)+\s\s\s"
        reg2=r"\s\s\s\d+(\.\d+)+"
        k=0
        for line in f.readlines():
            m=re.finditer(reg1,line)
            n=re.finditer(reg2,line)
            for i in m:
                if float(i.group(0)[0:8])>30 and float(i.group(0)[0:8])<50:
                    x=float(i.group(0)[0:8])
            for j in n:
                y=float(j.group(0)[3:12])
            emotion_num+=character_num[k][num-1]
            x=pow((x-center[0])*111,2)
            y=pow((y-center[1])*85.276,2)
            z=pow(x+y,0.5)
            if z<=distance:
                for j in range(5):
                    emotion_total+=character_num[k][j]
                emotion+=character_num[k][num-1]
            k+=1
        proportion.append(emotion/emotion_num)#半径内此情绪占此情绪总体比例
        proportion.append(emotion/emotion_total)#半径内此情绪占半径内所有情绪总数比例
    print(proportion)
    

    
def main():
    #delete_url()
    #f1()
   # function=f2(1,1)()
    #f3('hour',1,1)
    f4(5,1)
    f4(5,2)
    f4(5,3)
    f4(5,4)
    f4(5,5)
    
    
if __name__ == '__main__':
    main()