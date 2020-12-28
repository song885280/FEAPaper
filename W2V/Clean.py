import re
import os


def dealPapers(Path):
	base_path = Path
	files = os.listdir(base_path)
	all_papers = open("Data/论文聚合.txt", "w", encoding="utf-8")
	for path in files:
		full_path = os.path.join(base_path, path)
		with open(full_path, encoding="utf-8") as fp:
			data = fp.read()
			all_papers.write(data)


def readPaperData(paperName):
	"""
	:param paperName: 论文名
	:return: 将论文和压力容器杂志的摘要汇总
	"""
	file = open('Data/《压力容器》摘要汇总.txt', 'a+', encoding='utf-8')
	copy = open('Data/分行语料.txt', 'a+', encoding="utf-8")

	for line in file:
		copy.write(line)

	with open(paperName, encoding="utf-8") as paper:
		content = paper.read()
		article = re.sub('[a-zA-Z0-9’!"#$%&\'()*+./（）《》￥’‘-‘ ]+', '', content)
		for item in article.split("，"):
			if "。" in item:
				for sentence in item.split("。"):
					copy.write(sentence + "\n")
			else:
				copy.write(item + "\n")

	file.close()
	copy.close()


if __name__ == '__main__':
	dealPapers("Data/Paper")
	readPaperData("Data/论文聚合.txt")
