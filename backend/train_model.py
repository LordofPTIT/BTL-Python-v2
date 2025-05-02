from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import json

# Giả sử có tập dữ liệu phishing_dataset.csv
# Tải từ https://archive.ics.uci.edu/ml/datasets/phishing+websites
data = pd.read_csv('phishing_dataset.csv')
X = data.drop('label', axis=1)
y = data['label']

# Huấn luyện mô hình
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X, y)


def serialize_tree(tree):
    tree_ = tree.tree_

    def recurse(node):
        if tree_.feature[node] != -2:
            return {
                "feature": int(tree_.feature[node]),
                "threshold": float(tree_.threshold[node]),
                "left": recurse(tree_.children_left[node]),
                "right": recurse(tree_.children_right[node])
            }
        else:
            return {"value": tree_.value[node].tolist()}

    return recurse(0)


forest = [serialize_tree(est) for est in clf.estimators_]

with open('model.json', 'w') as f:
    json.dump(forest, f)