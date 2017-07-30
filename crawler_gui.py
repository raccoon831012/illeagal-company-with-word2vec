import jieba
import logging
import requests
import json
import re
import os
from tkinter import *
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
ChineseFont1 = FontProperties(fname = 'C:\\Windows\\Fonts\\kaiu.ttf')

def main():
    root = Tk()

    root.title("New Application")
    root.geometry("640x640+0+0")

    heading = Label(root, text="WELCOME 104", font=("arial", 40, "bold"), fg="steelblue").pack()

    label1 = Label(root, text="Enter company", font=("arial", 20, "bold"), fg="black").place(x=10, y=200)

    name = StringVar()
    entrybox = Entry(root, textvariable = name, width=25, bg="lightgreen").place(x=280, y=200)

    def do_it():
        print("input company: " + name.get())
        searchCompanies(name.get())
    work = Button(root, text="Company", width=30, height=5, bg="lightblue", command=do_it).place(x=250, y=300)

    root.mainloop()

	
	
def searchCompanies(inputCompany):

    
	url = 'https://www.qollie.com/graphql'
	# name = input('請輸入公司全名：')
	companyName = []
	companyName.append(inputCompany)
	pattern = re.compile(r'\w+')

	for x in range(0,len(companyName)):
		string = str(companyName[x])
		match = re.search(pattern, string)
		companyName[x]=match.group()

		payloads = {
			"query":"\n  \nfragment commonFields on Company {\n  _id\n  authentication\n  name\n  category\n  website\n  introduction\n  sourcesLinks\n  createdAt\n  comments\n  enableNotify\n  authApplication {\n    _id\n    updatedAt\n  }\n  jobs {\n    _id\n    jobTitle\n  }\n  announcement\n  tags\n  logo\n  businessAddress {\n    kind\n    county\n    district\n    detail\n  }\n  address\n  website\n  facebook\n  instagram\n  linkedin\n  email\n  taxId\n}\n\n  query search(\n    $kind: String\n    $keyword: String\n    $page: Int\n    $limit: Int\n  ) {\n    searchCompanies(query: {\n      kind: $kind\n      keyword: $keyword\n      limit: $limit\n      page: $page\n    }) {\n      ... commonFields\n    }\n  }\n  ",
			"variables":{"kind":"company","keyword":str(companyName[x]),"page":1,"limit":10}
		}

		res = requests.post(url,  data = json.dumps(payloads), headers= {'Content-Type': 'application/json'})
		parse = json.loads(res.text)
        # print (parse)
        # print (json.dumps(parse, indent=4, sort_keys=True, ensure_ascii=False))

		for company in parse['data']['searchCompanies']:
			companyId = str(company['_id'])
			print(companyId)

			print(str(companyName[x]))

			newpath = r'/' + str(companyName[x])
			if not os.path.exists(newpath):
				os.makedirs(newpath)

			searchComments(str(companyName[x]), companyId)

def searchComments(company, companyId):
    
	url = 'https://www.qollie.com/graphql'
# 5860c66430162b7e4c17de29
	payloads = {
		"query":"\n\nfragment commonFields on Comment {\n  _id\n  status\n  checked\n  kind\n  content\n  anonymous\n  likes\n  dislikes\n  judge\n  createdAt\n  category\n  pros\n  cons\n  shareType\n  isSysDelete\n  replies {\n    _id\n  }\n  author {\n    _id\n    nickname\n    picture\n    showComments\n    showAvatar\n  }\n  companyResponse {\n    content\n    createdAt\n    editHistories\n  }\n}\n\n\nfragment jobCommentFields on JobComment {\n  job {\n    _id\n    jobTitle\n    company {\n      _id\n      name\n      jobs {\n        _id\n        jobTitle\n      }\n      logo\n    }\n    sourcesLinks\n  }\n}\n\n\nfragment companyCommentFields on CompanyComment{\n  company {\n    _id\n    name\n    taxId\n    introduction\n    website\n    sourcesLinks\n    logo\n    jobs {\n      _id\n      jobTitle\n    }\n  }\n}\n\n\nquery search(\n  $kind: String\n  $companyId: ID\n  $jobId: ID\n  $keyword: String\n  $page: Int\n  $limit: Int\n) {\n  searchComments(query: {\n    kind: $kind\n    companyId: $companyId\n    jobId: $jobId\n    keyword: $keyword\n    page: $page\n    limit: $limit\n  }) {\n    ... commonFields\n    ... jobCommentFields\n    ... companyCommentFields\n  }\n}\n\n",
		"variables":{"companyId":companyId,"page":1,"limit":10}
	}

	res = requests.post(url,  data = json.dumps(payloads), headers= {'Content-Type': 'application/json'})
	parse = json.loads(res.text)
	# print (json.dumps(parse, indent=4, sort_keys=True, ensure_ascii=False))
	pointer = 0
	
	import pandas as pd
	xls_file = pd.ExcelFile("dictionary.xlsx")
	df = xls_file.parse('工作表1')
	predic = []
	list=[]
	sum = 0;
	for index, comment in enumerate(parse['data']['searchComments']):
		pointer = index
		logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        # jieba custom setting.
		jieba.set_dictionary('jieba_dict/dict.txt.big')

        # load stopwords set
		stopwordset = set()
		with open('jieba_dict/stopwords.txt','r',encoding='utf-8') as sw:
			for line in sw:
				stopwordset.add(line.strip('\n'))


		seg_list = jieba.cut(str(comment['pros']) + str(comment['cons']) + str(comment['content']), cut_all=False)
		var2 = 0
		sum1 = 0
		cal1 = 0
		result1 = 0
		print("analyze: ")
		for word in seg_list:
			for num2 in range(var2,len(df.index)):
				if word == df['word'][var2]:
					sum1 = sum1 + df['weight'][var2]
					cal1 = cal1 +1
				var2 = var2 + 1
			var2 = 0
		if cal1 != 0:
			result1 = 100*sum1/cal1-90
			sum = sum + result1
		predic.append(result1)
		print(result1)
	
	print(predic)
	objects_y = [0, 10, 20, 30, 40, 50 , 60, 70, 80, 90, 100]
	x_pos = range(len(objects_y))
	n = len(predic)
	x = range(n)
	width = 0.5
	plt.bar(x, predic,width, color="blue")
	#print ('average sum = ')
	#print(sum/n)
	
	plt.yticks(x_pos, objects_y)
	plt.ylabel('prediction(%)')
	plt.xlabel('comment')
	plt.title(company+",ave ="+str(sum/n*10)[:5]+"%",fontproperties = ChineseFont1,fontsize=15)
	plt.savefig(company+'.png')
	plt.show()

plt.show()


if __name__ == '__main__':
    main()
	
    



