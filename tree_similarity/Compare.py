from gensim.models import Word2Vec
import gensim

print("Loading the w2v model...")
embedding_path = "source/cn.skipgram.bin"
# model = gensim.models.KeyedVectors.load_word2vec_format(embedding_path, binary=True, unicode_errors='ignore')
model = Word2Vec.load("Model/FEA.model")

print("Finished")


def syn(node, node_list):  # 使用word2vec比较一个元组中两个词的相似度

	pairs = []
	i = 0
	result = 0
	for item in node_list:
		pairs.append((item, node))
	for pair in pairs:
		try:
			sim = model.wv.similarity(pair[0], pair[1])
			if 0.5 < sim < 0.99:
				result += sim
				i += 1
			else:
				continue
		except KeyError:
			continue
	if i == 0:
		return result
	else:
		return result / i


if __name__ == '__main__':
	q = model.wv.similarity("有限元", "有限元分析")
	print(q)
