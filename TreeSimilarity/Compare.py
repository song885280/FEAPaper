from gensim.models import Word2Vec
import gensim

print("Loading the w2v model...")
embedding_path = "source/cn.skipgram.bin"
# model = gensim.models.KeyedVectors.load_word2vec_format(embedding_path, binary=True, unicode_errors='ignore')
model = Word2Vec.load("Model/FEA.model")


def syn(node, node_list):
    """
	语义相似度
    :param node: 节点
    :param node_list: 相同深度节点
    :return: 最高的相似度
    """
    simPairs = []
    pairs = []
    i = 0
    result = []
    for item in node_list:
        pairs.append((item, node))
    for pair in pairs:
        try:
            sim = model.wv.similarity(pair[0], pair[1])
            if 0.5 < sim < 0.99:

                simPairs.append([pair[1], pair[0]])
                result.append(sim)
                i += 1
            else:
                continue
        except KeyError:
            continue
    if i == 0:
        return 0, 0
    else:
        return max(result), simPairs


if __name__ == '__main__':
    sim= model.wv.similarity("屈服极限", "屈服强度")
    print(sim)
