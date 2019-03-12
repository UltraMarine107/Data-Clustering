'''
Implement K means clustering with my own code
'''

import Data
import random
import math
import sys
from matplotlib import pyplot

'''
A field where the initial nodes are generated
Actually this class is unnecessary, we can do it in a simpler way
So no need to look carefully here
'''
class Field:
    def __init__(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    @staticmethod
    def build(ins1, ins2):
        up = max(ins1)
        down = min(ins1)
        left = min(ins2)
        right = max(ins2)
        return Field(round((2*up + down)/3), round((up + 2*down)/3),
                     round((2*left + right)/3), round((left + 2*right)/3))


'''
The central node of each group, each data point is assigned to one node.
It has a 2-dimensional coordinate that changes during our clustering process.
For more info, Google the algorithm of K Means Clustering.
'''
class Node:
    # Initial location of node is randomly generated
    def __init__(self, field):
        self.y = random.randrange(field.down, field.up)
        self.x = random.randrange(field.left, field.right)
        self.children_x = []
        self.children_y = []

    # Calculate the distance from data point to node
    def distance(self, py, px):
        return math.sqrt((self.y - py) ** 2 + (self.x - px) ** 2)

    # Move the node to the average location of all its "children"
    def move(self):
        mean_y = 0
        for y in self.children_y:
            mean_y += y
        mean_y = mean_y / len(self.children_y)

        mean_x = 0
        for x in self.children_x:
            mean_x += x
        mean_x = mean_x / len(self.children_x)

        if self.x == mean_x and self.y == mean_y:
            return False

        self.x = mean_x
        self.y = mean_y
        return True


'''
This is where clustering happens
ins1:   A list of y coordinate of data points
ins2:   A list of x coordinate of data points
k:      The number of groups to cluster into
field:  The area where nodes are initiates
return: A list of Nodes, with all data points assigned into one of them
'''
def cluster(ins1, ins2, k, field=None):
    if field is None:
        field = Field.build(ins1, ins2)

    # Initialize nodes
    nodes = []
    for i in range(k):
        node = Node(field)
        nodes.append(node)

    # Repeat, until the groups are consolidated
    while True:
        # Step1: assign data points to nodes
        for i in range(len(ins1)):
            nearest = nodes[0]
            distance = sys.maxsize

            for node in nodes:
                new_distance = node.distance(ins1[i], ins2[i])
                if node.distance(ins1[i], ins2[i]) < distance:
                    distance = new_distance
                    nearest = node

            nearest.children_y.append(ins1[i])
            nearest.children_x.append(ins2[i])

        # Step2: move nodes to the average location of data points
        one_moved = False
        for node in nodes:
            this_moved = node.move()
            one_moved = one_moved or this_moved

        if not one_moved:  # Check if all nodes remain the same
                return nodes

        for node in nodes:
            node.children_y = []
            node.children_x = []


'''
Generate scatter plot
'''
def scatter(ins1, ins2, k):
    main_nodes = cluster(ins1, ins2, k)

    colors = ["red", "green", "blue", "yellow", "orange", "cyan"]
    for i in range(k):
        print("Cluster " + str(i) + " has " +
              str(len(main_nodes[i].children_x)) + " data points.")
        pyplot.scatter(main_nodes[i].children_y,
                       main_nodes[i].children_x, color=colors[i])

    pyplot.title("Yu's K Means")
    pyplot.show()


# Main function
log_MBT, log_emp = Data.get_log_MBT_emp(Data.get_data())
scatter(log_MBT, log_emp, 2)  # 2 is number of groups to cluster
