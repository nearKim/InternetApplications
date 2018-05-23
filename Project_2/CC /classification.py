from sklearn.datasets import load_files
from sklearn.pipeline import Pipeline
from sklearn import metrics
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC


categories = ['economy', 'entertainment', 'health', 'politics', 'sports', 'technology', 'us']

train_data = load_files(container_path='text/train', categories=categories, shuffle=True,
                        encoding='utf-8', decode_error='replace')


# TODO - 2-1-1. Build pipeline for Naive Bayes Classifier
clf_nb = Pipeline([('vect', CountVectorizer(ngram_range=(1,2))),
                  ('tfidf', TfidfTransformer()),
                   ('clf', BernoulliNB(alpha=0.05))])
clf_nb.fit(train_data.data, train_data.target)

# TODO - 2-1-2. Build pipeline for SVM Classifier
clf_svm = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', SVC(kernel = 'linear', decision_function_shape='ovr'))])
clf_svm.fit(train_data.data, train_data.target)


test_data = load_files(container_path='text/test', categories=categories, shuffle=True,
                        encoding='utf-8', decode_error='replace')
docs_test = test_data.data
predicted = clf_nb.predict(docs_test)
#predicted = clf_svm.predict(docs_test)

# 분류가 잘못된 기사 제목 print
for i in range(len(predicted)):
    if predicted[i] != test_data.target[i] :
        print(test_data.filenames[i])
print(test_data.target)
print(predicted)
print("accuracy : %d / %d" % (np.sum(predicted==test_data.target), len(test_data.target)))
print(metrics.classification_report(test_data.target, predicted, target_names=test_data.target_names))
print(metrics.confusion_matrix(test_data.target, predicted))

with open('model_nb.pkl', 'wb') as f1:
    pickle.dump(clf_nb, f1)

with open('model_svm.pkl', 'wb') as f2:
    pickle.dump(clf_svm, f2)