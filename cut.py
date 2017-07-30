import jieba

input = open('badsource.txt','r',encoding = 'UTF-8')
seg_list = jieba.cut(input.read(), cut_all=False)
#print("Default Mode: " + " ".join(seg_list))  # 精确模式


f = open('output.txt', 'w', encoding = 'UTF-8')
f.write(" ".join(seg_list))
f.close()
input.close