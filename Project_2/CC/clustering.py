from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn import metrics
from sklearn.cluster import KMeans

categories = ['economy', 'entertainment', 'health', 'politics', 'sports', 'technology', 'us']

data = load_files(container_path='text_all', categories=categories, shuffle=True,
                    encoding='utf-8', decode_error='replace')

# TODO - Data preprocessing and clustering
data_trans = TfidfTransformer().fit_transform(CountVectorizer().fit_transform(data.data))
clst = KMeans(n_clusters=7)
clst.fit(data_trans)

print(metrics.v_measure_score(data.target, clst.labels_))