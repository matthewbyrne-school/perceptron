# Imports
from useful_functions import *
from math import floor, ceil
import json
import winsound



def openJsonFile(filename):
    with open("data.json", "r") as f:
        data = f.read()
    return json.loads(data)

# Main Subroutine
def main():
    filename = "data.json"

    training_data = openJsonFile(filename)

    negative_values = {"x":[], "y":[]}
    positive_values = {"x":[], "y":[]}

    for dic in training_data:
        if dic["y"] == 0.00:
            negative_values["x"].append(sum(dic["x"]))
            negative_values["y"].append(dic["y"])

        elif dic["y"] == 1.00:
            positive_values["x"].append(sum(dic["x"]))
            positive_values["y"].append(dic["y"])

    loPos = min(positive_values["x"])
    hiNeg = max(negative_values["x"])


    lims = [floor(min([min(positive_values["x"]), min(negative_values["x"])])), ceil(max([max(positive_values["x"]), max(negative_values["x"])]))+5]

    posBoundary = linRegression(positive_values["x"], positive_values["y"], lims) # getting the positive regression line
    posBoundary = LinearEquation(posBoundary["a"], posBoundary["c"])

    negBoundary = linRegression(negative_values["x"], negative_values["y"], lims) # getting the negative regression line
    negBoundary = LinearEquation(negBoundary["a"], negBoundary["c"])

    decBoundary = posBoundary.average(negBoundary)                                # averaging the regression lines to create a plane

    node1 = Node(decBoundary)
    print(node1.checkTrained(training_data))


    # Training
    node1.train(training_data)
    print(node1.checkTrained(training_data))

    trained = node1.checkTrained(training_data)

    examples = [                    # data with which to test the node
        [1, 9, 9, 9],
        [1, 1, 1, 1],
        [1, 4, 6, 8],
        [1, 2, 3, 17]
    ]


    # # Testing
    # node1.weights = [0,1,0,0]
    # node1.bias = -4.5
    # print(node1.checkTrained(training_data))

    if trained:

        for i in examples:
            print(f"\n{i} --> {node1.output(i)}")
        
        print(f"\n\nWeights:\n\t{node1.weights}\n\nBias:\n\t{node1.bias}\n\n")
        winsound.PlaySound("beep", winsound.SND_FILENAME)
        


# Main bit
if __name__ == "__main__":
    main()