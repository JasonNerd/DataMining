from sklearn import tree
import numpy as np

def int_to_ordinal(int):
    if 11 <= (int % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(int % 10, 4)]
    return str(int) + suffix
  
def get_column_name(clf, index):
    if hasattr(clf, 'feature_names_in_'):
        return clf.feature_names_in_[index]
    else:
        return int_to_ordinal(index + 1)

def explain_tree(clf):
    n_nodes = clf.tree_.node_count
    children_left = clf.tree_.children_left
    children_right = clf.tree_.children_right
    feature = clf.tree_.feature
    threshold = clf.tree_.threshold
    impurity = clf.tree_.impurity

    node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
    is_leaves = np.zeros(shape=n_nodes, dtype=bool)
    stack = [(0, 0)]  # start with the root node id (0) and its depth (0)
    while len(stack) > 0:
        # `pop` ensures each node is only visited once
        node_id, depth = stack.pop()
        node_depth[node_id] = depth

        # If the left and right child of a node is not the same we have a split
        # node
        is_split_node = children_left[node_id] != children_right[node_id]
        # If a split node, append left and right children and depth to `stack`
        # so we can loop through them
        if is_split_node:
            stack.append((children_left[node_id], depth + 1))
            stack.append((children_right[node_id], depth + 1))
        else:
            is_leaves[node_id] = True
    
    out_tree = []
    for i in range(n_nodes):
        out_node = ""
        if is_leaves[i]:
            out_node = "{space}node={node} is a leaf node. All but {accuracy}% of samples at this point are impure.".format(
                space=node_depth[i] * "\t", node=i, accuracy=(round(impurity[i] * 100, 2))
            )
        else:
            out_node = """{space}node={node} is a split node:
            go to node {left} if {feature} <= {threshold}
            else to node {right}.""".format(
                space=node_depth[i] * "\t",
                node=i,
                left=children_left[i],
                feature=get_column_name(clf, feature[i]) + " column",
                threshold=round(threshold[i], 2),
                right=children_right[i],
            )
            
        out_tree.append(out_node)
    
    return out_tree
        

if __name__ == '__main__':
    from sklearn.datasets import load_iris
    from sklearn.tree import DecisionTreeClassifier
    
    iris = load_iris()
    X = iris.data
    y = iris.target

    clf = DecisionTreeClassifier(max_leaf_nodes=3, random_state=0)
    clf.fit(X, y)
    
    for line in explain_tree(clf):
        print(line)