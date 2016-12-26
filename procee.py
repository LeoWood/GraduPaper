
with open('20161101-20161130.txt', 'r', encoding='utf-8') as f:
    weibos = f.readlines()
# with open('946-source.txt', 'w', encoding='utf-8') as f:
#     for line in lines:
#         line = line.strip()
#         if line != '':
#             f.write(line+'\n')

with open(r'F:\毕业论文\test\result\7.txt', 'r', encoding='utf-8') as f:
    results = f.readlines()
i = 0
for re in results:
    if re != '':
        nums = re.split(',')
        i += 1
        with open('F:\\毕业论文\\test\\result\\clasifacation-'+str(i)+'.txt', 'w', encoding='utf-8') as f:
            for num in nums:
                id = int(num)-1
                f.write(weibos[id].replace('/', '')+'\n')

# # 去重
# newlist = []
# with open(r'F:\毕业论文\test\数据\chong.txt', 'r', encoding='utf-8') as f:
#     list = f.readlines()

# for l in list:
#     l = l.strip()
#     if l not in newlist:
#         newlist.append(l)

# with open(r'F:\毕业论文\test\数据\quchong.txt', 'w', encoding='utf-8') as f:
#     for i in newlist:
#         f.write(i+'\n')
