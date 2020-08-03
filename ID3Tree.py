import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.tree.export import export_text

classification_name = "play"

dataset = pd.read_csv("tennisNew.csv")
print(dataset.shape)
print(dataset.head())
X = dataset.drop(classification_name, axis=1)
y = dataset[classification_name]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

tree.export_graphviz(classifier)

y_pred = classifier.predict(X_test)

tree_rules = export_text(classifier, feature_names=list(X_train))
print(tree_rules)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

