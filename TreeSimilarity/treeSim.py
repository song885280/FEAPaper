import math

import pandas
from tqdm import tqdm

import Compare
import jsonParser


class Tree:

    def __init__(self, tree_data: object) -> object:
        """

        :param tree_data: 树的结构，json形式
        """
        self.nodes = tree_data["NODES"]
        self.relations = tree_data["RELATIONS"]
        self.AllNodes = {}  # 存放节点和它对应的标签
        self.Edges = {}  # 存放边和它对应的值
        self.all_Relations = []
        self.Levels = {}  # 存放每个等级的所有节点

        for j in range(0, len(self.relations)):  # 存储所有关系
            self.all_Relations.append(self.relations[j])

        for i in range(0, len(self.nodes)):  # 命名，分配等级
            level = []
            for j in range(0, len(self.nodes[i])):
                node_name = self.nodes[i][j]
                level.append(node_name)
                try:
                    self.AllNodes[node_name] = {"Level": i}
                except TypeError:
                    print(tree_data)

            self.Levels[i] = level

        for i in range(0, len(self.relations)):
            edge_name = "E" + str(i)
            Relation = self.relations[i]
            self.Edges[edge_name] = Relation

        for node_name in self.AllNodes.keys():  # 获取每个节点父节点和子节点的集合
            parent = []
            children = []

            for j in range(0, len(self.relations)):

                pair = self.relations[j]
                if node_name in pair:

                    if pair.index(node_name) == 0:
                        parent.append(pair[1])
                    else:
                        children.append(pair[0])
            self.AllNodes[node_name]["Parents"] = parent
            self.AllNodes[node_name]["Children"] = children


class Node:

    def __init__(self, Tree, node_name):

        self.Parents = Tree.AllNodes[node_name]["Parents"]
        self.Children = Tree.AllNodes[node_name]["Children"]

        self.Concept = node_name
        self.Position = None
        self.L = 0

        num = 0
        if self.Parents and self.Children:
            self.Position = "branch"
            for child in self.Children:  # 用递归的方式给定参数L
                num += Node(Tree, child).L
            self.L = num / len(self.Children) + 1

        else:
            if not self.Parents:
                self.Position = "root"
                for child in self.Children:
                    num += Node(Tree, child).L
                self.L = num / len(self.Children) + 1

            else:

                self.Position = "leaf"


class MultiTree(Tree):

    def __init__(self, Tree_1: object, Tree_2: object, alpha: int, Method, PSO, Plist) -> object:
        """

        :param Tree_1: 树1
        :param Tree_2: 树2
        :param alpha: 阻尼因子
        """
        self.alpha = alpha  # 阻尼因子
        self.Tree_1 = Tree_1
        self.Tree_2 = Tree_2
        self.Method = Method
        self.PSO = PSO
        self.Plist = Plist
        self.simPairs = []
        Nodes = merge(self.Tree_1.nodes, self.Tree_2.nodes)
        Relations = merge_relations(self.Tree_1.all_Relations, self.Tree_2.all_Relations)

        self.AllNodes = Tree({"NODES": Nodes, "RELATIONS": Relations}).AllNodes
        self.Weight_dict = {}
        # print("Initialize the weight dict...")

        for node in self.AllNodes.keys():
            if Method == "1":
                level = self.AllNodes[node]["Level"]
                word_list = self.Tree_1.Levels[level] + self.Tree_2.Levels[level]
                self.Weight_dict[node] = Compare.syn(node, word_list)[0]
                simPairs = Compare.syn(node, word_list)[1]
                if simPairs != 0:
                    self.simPairs += Compare.syn(node, word_list)[1]
            else:
                self.Weight_dict[node] = 0

        # print("节点权重")
        # for nodes in self.Weight_dict:
        #     print(nodes, self.Weight_dict[nodes])


class MultiNode(Node, MultiTree):

    def __init__(self, MultiTree, node_name):
        alpha = MultiTree.alpha
        Method = MultiTree.Method
        PSO = MultiTree.PSO
        Plist = MultiTree.Plist
        node = Node(MultiTree, node_name)
        self.Position = node.Position
        self.Weight = 0
        self.Concept = node_name
        self.nodes_1 = MultiTree.Tree_1.AllNodes.keys()  # 所有节点的列表
        self.nodes_2 = MultiTree.Tree_2.AllNodes.keys()

        if self.Position == "leaf":
            if node.Concept in self.nodes_1 and node.Concept in self.nodes_2:
                self.Weight = 1
            else:
                if Method == "1":
                    self.Weight = MultiTree.Weight_dict[node.Concept]
                else:
                    self.Weight = 0  # 不使用word2vec

        if self.Position == "root":
            beta = len(node.Children)
            Sum = 0
            if PSO == "False":
                for Item in node.Children:
                    Sum += MultiNode(MultiTree, Item).Weight  # 不考虑传播率
            else:
                count = 0
                for Item in node.Children:
                    Sum += Plist[0] * MultiNode(MultiTree, Item).Weight  # 考虑传播率
                    count += 1
            self.Weight = Sum / beta

        if self.Position == "branch":
            if node.Concept in self.nodes_1 and node.Concept in self.nodes_2:
                delta = 1
            else:
                if Method == "1":
                    delta = MultiTree.Weight_dict[node.Concept]
                else:
                    delta = 0  # 不使用word2vec
            beta = len(node.Children)
            Sum = 0
            for Item in node.Children:
                Sum += MultiNode(MultiTree, Item).Weight
            row = Sum / beta

            self.Weight = (1 - 1 / (alpha ** node.L)) * row + (1 / (alpha ** node.L)) * delta


def merge(a, b):
    c = []
    for i in range(0, len(a)):
        d = []
        for item in a[i]:
            if item not in b[i]:
                d.append(item)
        c.append(d + b[i])
    return c


def merge_relations(a, b):
    """
    合并不同FEA案例树中的关系
    :param a: TreeA中的关系
    :param b: TreeB中的关系
    :return: 去重之后关系的集合
    """
    c = []
    for item in a:
        if item not in b:
            c.append(item)
    return b + c


def bulid_tree(tree_name):
    tree_data = jsonParser.Converter(tree_name)
    return Tree(tree_data)


def get_vectors(nodes: list) -> object:
    """
    使用word2vec获取每一个词的词向量
    :param nodes:
    """


# print(nodes)


if __name__ == '__main__':

    Tree_1 = bulid_tree("src/ALL/LNG低温卧式储罐_强度分析.json")
    Tree_2 = bulid_tree("src/ALL/大型氧化反应器_模态分析.json")

    multi = MultiTree(Tree_1, Tree_2, math.e, Method="0", PSO="False", Plist=[1.2, 1, 1, 1, 1])
    simPairs = multi.simPairs
    Data = []
    Similarity = 0
    for item in multi.AllNodes.keys():
        node = MultiNode(multi, item)
        Name = item
        Weight = node.Weight
        Position = node.Position
        if Position == "root":
            Similarity = Weight
        Data.append([Name, Weight, Position])
    simPairs_2 = []
    for item in simPairs:
        if item and [item[1], item[0]] not in simPairs_2:
            simPairs_2.append(item)

    table = pandas.DataFrame(Data, columns=["None", "Weight", "Position"])
    print(table)
    print(simPairs_2)
    print("Similarity : {0:.3f}".format(Similarity))
