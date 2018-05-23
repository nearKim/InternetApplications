from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt

categories = ['economy', 'entertainment', 'health', 'politics', 'sports', 'technology', 'us']

data = load_files(container_path='text_all', categories=categories, shuffle=True,
                    encoding='utf-8', decode_error='replace')

#TODO - Data preprocessing and clustering
data_trans = TfidfTransformer().fit_transform(CountVectorizer(stop_words='english').fit_transform(data.data))
clst = KMeans(n_clusters=7, n_init=20)
a = clst.fit(data_trans)

print(metrics.v_measure_score(data.target, clst.labels_))

#cluster와 실제 category의 시각화
clusters = a.labels_.tolist()
labels = data.target
colors = {0: 'b', 1: 'g', 2: 'r', 3: 'c', 4: 'm', 5: 'y', 6: 'k'}

pca = PCA(n_components=2).fit_transform(data_trans.toarray())
xs, ys = pca[:, 0], pca[:, 1]
#df = pd.DataFrame(dict(x=xs, y=ys, label=clusters))
df = pd.DataFrame(dict(x=xs, y=ys, label=labels))
groups = df.groupby('label')

# set up plot
fig, ax = plt.subplots(figsize=(17, 9)) # set size
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

#iterate through groups to layer the plot
for idx, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=8, 
            color=colors[idx], mec='none')
    ax.set_aspect('auto')
    ax.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params(\
        axis= 'y',         # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelleft='off')
    
plt.show() #show the plot