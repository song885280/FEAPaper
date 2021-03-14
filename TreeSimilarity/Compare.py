from gensim.models import Word2Vec
import gensim

print("Loading the w2v model...")
embedding_path = "source/cn.skipgram.bin"
# model = gensim.models.KeyedVectors.load_word2vec_format(embedding_path, binary=True, unicode_errors='ignore')
model = Word2Vec.load("Model/FEA.model")



def syn(node, node_list):  # 使用word2vec比较一个元组中两个词的相似度
	simPairs = []
	pairs = []
	i = 0
	result = 0
	for item in node_list:
		pairs.append((item, node))
	for pair in pairs:
		try:
			sim = model.wv.similarity(pair[0], pair[1])
			if 0.5 < sim < 0.99:

				simPairs.append([pair[1], pair[0]])
				result += sim
				i += 1
			else:
				continue
		except KeyError:
			continue
	if i == 0:
		return result, 0
	else:
		return result / i, simPairs


if __name__ == '__main__':
	q = model.wv.similarity("有限元", "有限元分析")
	print(q)
