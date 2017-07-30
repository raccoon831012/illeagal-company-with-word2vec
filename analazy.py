#-*- coding:utf-8 -*-

import xlrd
#打開xlsx文件
ad_wb = xlrd.open_workbook("dictionary.xlsx")
#獲取第一張表的名稱
row_data = ad_wb.sheets()[0]
print ("表單數量：", ad_wb.nsheets)
print ("表單名稱：", ad_wb.sheet_names())
#獲取第一個目標表單
sheet_0 = ad_wb.sheet_by_index(0)
print (u"表單 %s 共 %d 行 %d 列" % (sheet_0.name, sheet_0.nrows, sheet_0.ncols))

#直接輸出日期
date_value = xlrd.xldate_as_tuple(sheet_0.cell_value(2,2),ad_wb.datemode)
date1 = xlrd.xldate.xldate_as_datetime(sheet_0.cell_value(2, 2), ad_wb.datemode)
print (date_value)#元組
print (date1)#日期
# 遍歷所有表單，由於數據量大 ，這裡只取前10條
for s in ad_wb.sheets():
	for r in range(0, 10):
# 輸出指定行
		print (s.row(r))

