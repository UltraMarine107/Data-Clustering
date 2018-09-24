'''
Practice Gaussian Mixture Model clustering
'''


import Data
from sklearn.mixture import GaussianMixture
from sklearn.cluster import MiniBatchKMeans
from matplotlib import pyplot
import numpy as np
from itertools import cycle, islice


def gaussian(ins1, ins2, k=2):
    X = []

    for i in range(len(ins1)):
        data_point = [ins1[i], ins2[i]]
        X.append(data_point)

    gmm = GaussianMixture(n_components=k, covariance_type='full')
    gmm.fit(X)
    pred = gmm.predict(X)

    colors = np.array(list(islice(cycle(['#377eb8', '#ff7f00', '#4daf4a',
                                         '#f781bf', '#a65628', '#984ea3',
                                         '#999999', '#e41a1c', '#dede00']),
                                  int(max(pred) + 1))))

    pyplot.scatter(ins1, ins2, color=colors[pred])
    pyplot.title("Gaussian Mixture")
    pyplot.show()

    kmeans = MiniBatchKMeans(n_clusters=k)
    kmeans.fit(X)
    pred = kmeans.predict(X)

    pyplot.scatter(ins1, ins2, color=colors[pred])
    pyplot.title("K Means by sklearn")
    pyplot.show()


log_MBT, log_emp = Data.get_log_MBT_emp(Data.get_data())
gaussian(log_MBT, log_emp)
