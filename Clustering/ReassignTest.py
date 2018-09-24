import ForLoopTask
import numpy


def naive_reassign():
    data = ForLoopTask.divide_by_cluster(log=True)
    outliers = ForLoopTask.find_outliers(data)

    for outlier in outliers:
        val = outlier[1]
        name = outlier[0]
        previous_cluster = outlier[2]
        current_cluster = ""
        current_mean = numpy.mean(data[outlier[2]][1])

        for key, value in data.items():
            val_list = value[1]
            mean = numpy.mean(val_list)

            if abs(current_mean - val) > abs(mean - val):
                current_mean = mean
                current_cluster = key

        if current_cluster != "":
            data[previous_cluster][1].remove(val)
            data[previous_cluster][0].remove(name)
            data[current_cluster][1].append(val)
            data[current_cluster][0].append(val)

    return data


outliers_after_reassign = ForLoopTask.find_outliers(naive_reassign())
ForLoopTask.write_csv("LoggedOutliersAfterReassign.csv", outliers_after_reassign)
