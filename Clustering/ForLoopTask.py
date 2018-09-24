import csv
import numpy
import math


def get_data():
    # Read csv file
    csvFile = open('Customer_List_3_18_YTD&PL_Clusters_YTDSubscribed.csv',
                   "r", encoding="latin-1")
    reader = csv.reader(csvFile)

    data = []  # put all data into the format of double list
    for row in reader:
        data.append(row)

    del data[0]  # delete title row
    return data


def divide_by_cluster(log=False):
    data = get_data()
    clustered_data = {}

    for row in data:
        cluster_id = row[43]
        try:
            bill = int(row[17].replace(',', ''))
        except ValueError:
            continue

        if log is True:
            bill = math.log(bill)

        if cluster_id in clustered_data.keys():
            clustered_data[cluster_id][0].append(row[0])
            clustered_data[cluster_id][1].append(bill)
        else:
            clustered_data[cluster_id] = [[row[0],], [bill,]]

    return clustered_data


def find_outliers(src):
    outliers = []
    clustered_data = src

    for key, value in clustered_data.items():
        custid_list = value[0]
        march_bill_list = value[1]

        std = numpy.std(march_bill_list)
        mean = numpy.mean(march_bill_list)

        for i in range(len(march_bill_list)):
            if abs(march_bill_list[i] - mean) > 3 * std:
                id_bill_cluster = [custid_list[i], march_bill_list[i], key]
                outliers.append(id_bill_cluster)

    # print(outliers[0:20])
    return outliers


def write_csv(filename, src):
    file = open(filename, 'w')

    for row in src:
        file.write(row[0])
        file.write(', ')
        file.write(str(row[1]))
        file.write(', ')
        file.write(row[2])
        file.write('\n')


# write_csv("LoggedOutliers.csv", find_outliers(divide_by_cluster(log=True)))
