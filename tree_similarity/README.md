# tree_similarity

### Tree类

输入

+ json格式文件，该文件包含
  1. 若干个节点组成的列表
  2. 上述节点之间关系的列表

输出

+ `Nodes`  节点名称的集合
+ `Edges`  边（关系）的集合
+ `Level(Nodes)`  确定所有节点在树中的深度的方法，返回`int`
+ `Parents(Nodes)` 获取所有节点在树中的所有父节点列表，返回`list`
+ `Children(Nodes)` 获取所有节点在树中的所有子节点，返回`list`

### Node类

输入

+ 节点n
+ Tree类

输出

+ `Parents` 该节点的父节点列表

+ `Children` 该节点的子节点列表

+ `Position(node)` 获取该节点在树中的位置，分为`root`,`branch`,`leaf`。分别表示处于根部、中间和叶节点

+ `L(n)` 获取节点的L值，每个节点的L值等于其子节点L值的平均值加一

  ```python
  L(n) = 0
  L(n) += L(i) for i in Children 
  ```

### MultiTree类

输入

+ 两个不同的树，T1 T2
+ `α` 阻尼因子，阻尼因子保证了低层级的节点（靠近叶的节点）在计算相似度时能贡献出更多的权重

输出

+ `MultiTree`继承了`Tree`中的所有属性

+ `Delta(MultiTree,T1,T2)`为每一个词生成计算权重所用的参数δ，返回一个字典Δ，其计算逻辑为：
+ 对于multitree中的某个节点A，首先要确定该节点的层级n。
  + 再将A与T1和T2中n层级的所有节点组成节点对，其形式为`pairs=[(A,T1_n1),(A,T1_n2)...(A,T2_n1),(A,T2_n2)... ]`这样做是为了避免跨层级比较相似度，节省了计算的时间

  + 最后使用word2vec计算所有节点对的相似度，返回所有相似度大于0.6的节点对，这一步是为了的到所有与A相似的节点以及他们之间的相似度：
+ 节点A的δ为与其相似节点的相似度平均值，在字典Δ中添加一条索引`{A:δ}`

### MultiNode类

输入

+ 节点`n`
+ `MultiTree`类

输出

+ 继承了`Node`类的属性

+ `W(n)`计算该节点的权重，不同节点的计算方法不同：

1. 叶节点

$$
W_{leaf}\left(n\right)=\left\{\begin{array}{ll}
  1 & \text { if } n \in Nodes^{T_{1}}, n \in Nodes^{T_{2}} \\
  \Delta & \text { Otherwise }
  \end{array}\right.
$$

  $\Delta$— 节点n所对应的

2. 根节点

$$
W_{root}\left(n, \alpha\right)=\left(\frac{1}{\beta_{n}}\right)\left(\sum_{\forall n_{x} \in \operatorname{Children}\left(n\right)}W\left(n_{x}, \alpha\right)\right)
$$
  $\beta_{n}$— 子节点的个数

3. 中间节点

$$
\begin{array}{c}
W_{branch}\left(n, \alpha\right)=\left(1-\frac{1}{\alpha^{{L}\left(n\right)}}\right) W_{root}\left(n, \alpha\right) \\
+\left(\frac{1}{\alpha^{{L}\left(n\right)}}\right) W_{leaf}\left(n\right)
\end{array}
$$



### 结果

根节点的权重$W_{root}$即为两个树的相似度

### 伪代码

#### Sim(node,MultiTree,T1,T2)

```python

if node.position == "leaf":
   if node in T1 and node in T2:
       Weight = 0
   else:
       Weight = Δ[node]
            
if node.position = "root":
	Weight = sum(node.Children.Weight) / β 
    Similarity = W

if node.position = "branch":
	if node in T1 and node in T2:
		γ = 0
	else:
         γ = Δ[node]
	θ = sum(node.Children.W) / β 
	Weight = (1 - 1 / (α ** L(node))) * θ + (1 / (α ** L(node))) * γ
```

α — 阻尼系数，取e（2.71）

β — 子节点的个数

Similarity — 树的相似度

Δ — 由`Delta(MultiTree,T1,T2)`生成的参数字典

#### 



