import Basics
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from matplotlib import pyplot
import numpy


def gmm_result_demo():
    data = Basics.get_data()[20000:20200]
    result = []

    for i in range(4):
        gmm = GaussianMixture(n_components=5)
        gmm.fit(data)
        result.append(gmm.predict(data))

    Basics.scatter_plot(result, row=2, col=2)


def gmm_kmeans_score_demo():
    data = Basics.get_data()
    k_means_scores = []
    gmm_scores_0 = []
    gmm_scores_1 = []

    for i in range(2, 21):
        gmm = GaussianMixture(n_components=i)
        k_means = KMeans(n_clusters=i)

        gmm.fit(data)
        gmm_scores_0.append(gmm.score(data))

        gmm.fit(data)
        gmm_scores_1.append(gmm.score(data))

        k_means.fit(data)
        k_means_scores.append(k_means.score(data))

    pyplot.subplot(1, 3, 1)
    pyplot.plot(range(19), gmm_scores_0)
    pyplot.title("GMM Scores 2 to 20 Clusters 1")

    pyplot.subplot(1, 3, 2)
    pyplot.plot(range(19), gmm_scores_1)
    pyplot.title("GMM Scores 2 to 20 Clusters 2")

    pyplot.subplot(1, 3, 3)
    pyplot.plot(range(19), k_means_scores)
    pyplot.title("K Means Scores 2 to 20 Clusters")
    pyplot.show()


def elbow_test(data):
    scores = []

    for i in range(2, 21):
        gmm = GaussianMixture(n_components=i)
        gmm.fit(data)
        scores.append(gmm.score(data))

    max_slope = -20  # Todo change algorithm
    best_k = 0

    for j in range(1, 18):
        slope = 2 * scores[j] - scores[j + 1]

        if slope > max_slope:
            max_slope = slope
            best_k = j + 2

    return best_k


def recluster_assess(data):
    if len(data) < 20:
        return False

    dist = []

    for point in data:
        d = (point[0] ** 2 + point[1] ** 2) ** (1 / 2)
        dist.append(d)

    std = numpy.std(dist)

    if std > 0.25:
        return True

    return False


def cluster(data, prev="", arranged=list(), labels=list(), scores=list()):
    working = {}

    k = elbow_test(data)
    gmm = GaussianMixture(n_components=k)
    gmm.fit(data)
    raw = gmm.predict(data)
    score = gmm.score(data)

    for i in range(k):
        working[i] = []

    for i in range(len(data)):
        for j in range(k):
            if raw[i] == j:
                working[j].append(data[i])
                break

    for label, content in working.items():
        if recluster_assess(content):
            name = prev + str(label) + "."
            arranged, labels, scores = cluster(content, prev=name,
                                       arranged=arranged, labels=labels,
                                       scores=scores)

        else:
            arranged += content
            cluster_name = prev + str(label)
            name_list = [cluster_name] * len(content)
            labels += name_list
            variance = numpy.var(content)
            scores.append([cluster_name, score, variance])

    return arranged, labels, scores


def write_csv():
    file = open("Clustering_Pattern2.csv", "w")
    file2 = open("Score_Variance2.csv", "w")
    arranged, labels, scores = cluster(Basics.get_data())

    for i in range(len(arranged)):
        line = str(arranged[i][0]) + ", " + str(arranged[i][1]) + \
               ", " + str(labels[i]) + "\n"
        file.write(line)

    for i in range(len(scores)):
        line = str(scores[i][0]) + ", " + str(scores[i][1]) + \
               ", " + str(scores[i][2]) + "\n"
        file2.write(line)


write_csv()
