'''
Get data for all analysis practice
MBT: March total bill, which represents the amount of service 
    that customers purchase
emp: Employee number, the size of customer companies 
'''


import csv
import codecs
from matplotlib import pyplot
import math


def get_data():
    # Read csv file
    csvFile = codecs.open('3.22MRR&EMP.csv', "r", encoding='latin-1',
                          errors='ignore')
    reader = csv.reader(csvFile)

    data = []  # put all data into the format of double list
    for row in reader:
        data.append(row)

    del data[0]  # delete title row
    return data


def get_log_MBT_emp(data):
    march_bill_total = []
    emp = []

    for row in data:
        march_bill_total.append(int(row[18]))
        emp.append(int(row[36]))

    log_march_bill_total = []
    log_emp = []

    for row in data:
        try:
            bill = math.log(int(row[18]))
            emp_number = math.log(int(row[36]))
            log_march_bill_total.append(bill)
            log_emp.append(emp_number)
        except ValueError:
            continue

    return log_march_bill_total, log_emp


def get_log_LT_3(data):
    ins1, ins2 = get_log_MBT_emp(data)

    # TODO index out of range, cause unknown. This should work?!
    for i in range(len(ins2)):
        if ins2[i] < 3:
            del ins2[i]
            del ins1[i]

    return ins1, ins2


def scatter_plot(list1, list2):
    pyplot.scatter(list1, list2)
    pyplot.show()


# ins1, ins2 = get_log_LT_3(get_data())
# scatter_plot(ins1, ins2)
