from gensim.models import Word2Vec

model_file_name = "Data/FEA.model"
word2vec_model = Word2Vec.load(model_file_name)


def similarwords(word):
	req_count = 10
	print(word)
	for key in word2vec_model.wv.similar_by_word(word, topn=100):

		req_count -= 1
		print(key[0], key[1])
		if req_count == 0:
			break;


def pair(test_pair):
	for [i, j] in test_pair:
		print([i, j])
		print(word2vec_model.wv.similarity(i, j))


test_pair = [["有限元分析", "有限元"],
             ["弹性系数", "弹性模量"],
             ["腐蚀裕量", "腐蚀裕度"],
             ["蒸汽", '水蒸气'],
             ["弹性模量", "弹性系数"],
             ["开孔接管", "开口接管"],
             ["工况", "作业条件"],
             ["工况", "工况条件"],
             ["有限元", "有限元分析"],
             ["应力分类", "应力分析"]]

similarwords("筒体")
