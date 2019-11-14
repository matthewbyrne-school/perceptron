# main functions are sign(), dot(), 

# Imports
from math import e
import linear_regression_MB
import matplotlib.pyplot as plt

# Subroutines
def sign(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


def dotIndicator(x):
    return 1 if x else 0


def sigmoidFunc(v):
    return 1 / (1 + (e**(-v)))


def linRegression(x, y, lims=None):
    if not lims:
        lims = [j for j in range(1, 2*len(y))]

    if not x or x == []:
        x = [i for i in range(1, len(y))]

    if len(x) != len(y):
        raise Exception("\nInput Error: x and y are not equal in length\n")

    a, c, xBar, yBar = linear_regression_MB.FormEquation(x, y)

    return {"a":-a, "c":c, "x bar":xBar, "y bar":yBar}


def unpackDict(originalFunc):
    def wrapperFunc(dict, *args):
        return originalFunc(*args, **dict)
    return wrapperFunc()
    

def checkHigherDecBound(x, y, a, c):
    correct = True
    for i, j in enumerate(y):
        correct = correct and (j > a*x[i]+c)
        return correct


def checkLowerDecBound(x, y, a, c):
    correct = True
    for i, j in enumerate(y):
        correct = correct and (j < a*x[i]+c)
        return correct


def findDecisionPlane(a, biggestNegativeTuple, smallestPositiveTuple):
    '''
    The decision plane is an idea in computer science, ANNs specifically, that when using a perceptron as a linear
    classifier it is possible to draw the points on a graph and draw a line between them to separate the two classes.
    This line is the decision plane.
    '''
    n = biggestNegativeTuple
    p = smallestPositiveTuple

    c_negative = n[1] - (a * n[0])
    c_positive = p[1] - (a * p[0])

    posEqu = LinearEquation(a, c_positive)
    negEqu = LinearEquation(a, c_negative)

    resEqu = posEqu.average(negEqu)

    return resEqu.a, resEqu.c


def stepFunction(decisionPlaneM, decisionPlaneC, checkTuple): # linear classifier - if x > i then 1 else 0
    x, y = checkTuple
    a = decisionPlaneM
    c = decisionPlaneC

    return 1.0 if y >= (a*x + c) else 0.0


def graph(x, y, colour="black", Scatter=False): # matplotlib command
    if not Scatter:
        plt.plot(x, y, color=colour)
    
    else:
        plt.plot(x, y, color=colour, marker="o")


def showPlot(): # matplotlib command
    plt.savefig("output.png")
    plt.show()


def normalise(inputs): # normalising values
    total = 0

    for i in inputs:
        total += i ** 2

    total = total**0.5
    newX = []

    for i in inputs:
        newX.append(float(i/total))

    return inputs


def frange(x, y, jump): # float range - used to increment by a float value
  while x < y:
    yield x
    x += jump


# Equation Class
class LinearEquation:
    def __init__(self, a, c):
        self.a = a
        self.c = c

    def __add__(self, other):
        return LinearEquation(self.a+other.a, self.c+other.c)

    def average(self, other):
        return LinearEquation((self.a+other.a)/2, (self.c+other.c)/2)

    def gradIncrease(self, posBool, xInt, yInt):
        if posBool:
            self.a += 1
            self.c = yInt - (self.a * xInt)

    def graphEqu(self, lims):
        x = [i for i in range(lims[0], lims[1])]
        y = [(i*self.a + self.c) for i in range(lims[0], lims[1])]

        print(x, y)

        plt.plot(x, y, color="black")

# Main Node class
class Node():
    def __init__(self, decisionPlane, w=[1,1,1,1], b=0):
        self.a = decisionPlane.a
        self.c = decisionPlane.c
        self.weights = w
        self.bias = b

    def integrate(self, inputs):
        inputs = normalise(inputs)

        weighted_sum = sum(inputs[k] * self.weights[k] for k in range(0, len(inputs)))
        return weighted_sum + self.bias

    def checkTrained(self, data, falsePos=None):
        if type(data) is list:
            if not falsePos:
                output = True


                for i in data:
                    output = (self.output(i["x"]) == i["y"]) and output

                return output

            else:
                present = (self.weights in falsePos)
                for i in falsePos:
                    if self.weights in i:
                        present = True

                if present:
                    return False
                
                else:
                    output = True
                    for i in data:
                        output = (self.output(i["x"]) == i["y"]) and output
                    return output

        elif type(data) is dict:
            if not falsePos:
                output = True

                output = (self.output(data["x"]) == data["y"]) and output

                return output

            else:
                present = (self.weights in falsePos)
                for i in falsePos:
                    if self.weights in i:
                        present = True

                if present:
                    return False
                    
                else:
                    output = True
                    output = (self.output(data["x"]) == data["y"]) and output
                    return output


        else:
            return "else"



    def train(self, data, falsePos=None):
        for i in frange(-50, 51, 0.5):
            self.bias = i
            if self.checkTrained(data, falsePos):
                return None

        
        for a in range(-5, 6):
            for b in range(-5, 6):
                for c in range(-5, 6):
                    for d in range(-5, 6):
                        self.weights = [a, b, c, d]

                        for i in frange(-50, 51, 0.5):
                            self.bias = i

                            # print(f"\n{self.weights}\t{self.bias}\t\t\t{self.checkTrained(data, falsePos)}")

                            if self.checkTrained(data, falsePos):
                                return None


    def output(self, inputs):
        return stepFunction(self.a, self.c, (sum(inputs), self.integrate(inputs)))



            
