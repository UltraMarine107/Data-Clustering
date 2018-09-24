import csv
import sys
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from matplotlib import pyplot
import numpy as np
from itertools import cycle, islice


def get_data():
    csv_file = open("CustomerList4.4.csv")
    reader = csv.reader(csv_file)

    data = []
    for row in reader:
        try:
            data.append([float(row[49]), float(row[50])])
        except ValueError:
            continue

    return data


def cluster_demo():
    data = get_data()
    gmm = BayesianGaussianMixture(n_components=5)
    gmm.fit(data)

    return [gmm.predict(data),]


def scatter_plot(cluster, row=1, col=1, objective="Original data"):
    pyplot.figure(figsize=(15, 8))

    for i in range(1, len(cluster) + 1):
        x = []
        y = []

        cluster_num = int(max(cluster[i - 1]) + 1)
        for couple in get_data():
            x.append(couple[0])
            y.append(couple[1])

        colors = np.array(list(islice(cycle(['red', 'orange', 'yellow', 'green',
                                             'cyan', 'blue', 'purple']),
                                      cluster_num)))

        pyplot.subplot(row, col, i)
        pyplot.scatter(x, y, color=colors[cluster[i - 1]])
        title = str(cluster_num) \
            + " clusters"

        if i == 1:
            title = objective + ", " + title
            pyplot.xlabel("Logged YTD")
            pyplot.ylabel("Logged Physical Lines")

        pyplot.title(title)

    pyplot.show()


def arrange_by_cluster(cluster):
    result = {}
    data = get_data()
    cluster_num = int(max(cluster) + 1)

    for i in range(cluster_num):
        result[i] = ([], [])
        for row in range(len(cluster)):
            if cluster[row] == i:
                result[i][0].append(data[row][0])
                result[i][1].append(data[row][1])

    return result


def naive_assess(arranged):
    x_variance = 0
    y_variance = 0

    for data in arranged.values():
        length = len(data[0])
        x_variance += length
        y_variance += length

    return x_variance, y_variance


def comparative_cluster(start, end):
    result = []
    data = get_data()

    for i in range(start, end + 1):
        gmm = GaussianMixture(n_components=i)
        gmm.fit(data)
        result.append(gmm.predict(data))

    return result


# ToDo result not stable, changes between each time of clustering
def comparative_assess(clusters, algorithms, plot=True):
    results = []

    for i in range(1, len(algorithms) + 1):
        x_variance = []
        y_variance = []

        for cluster_pattern in clusters:
            arranged = arrange_by_cluster(cluster_pattern)
            x, y = algorithms[i - 1](arranged)

            x_variance.append(x)
            y_variance.append(y)

        x_mean = np.mean(x_variance)
        y_mean = np.mean(y_variance)
        combine_variance = []
        min_var = sys.maxsize
        min_var_index = 0

        for j in range(len(x_variance)):
            var = x_variance[i] / x_mean + y_variance[i] / y_mean
            combine_variance.append(var)

            if var < min_var:
                min_var = var
                min_var_index = j

        results.append(min_var_index)

        ran = range(0, len(x_variance))

        if plot:
            pyplot.subplot(i, 2, i * 2 - 1)
            pyplot.plot(ran, x_variance)
            pyplot.title("Variance in logged YTD")
            pyplot.xlabel("Number of clusters")
            pyplot.ylabel("Variance")

            pyplot.subplot(i, 2, i * 2)
            pyplot.plot(ran, y_variance)
            pyplot.title("Variance in logged physical lines")
            pyplot.xlabel("Number of clusters")
            pyplot.ylabel("Variance")

    if plot:
        pyplot.show()

    return results


# def recluster_assess():
#     arrange_by_cluster()


cluster_demo()
# print(comparative_assess(comparative_cluster(5, 21), [naive_assess,]))
