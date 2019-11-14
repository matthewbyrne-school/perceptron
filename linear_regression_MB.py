# A level Computer Science Project 2019
# Author: Matthew Byrne
# Date: 7/10/19

# Imports

import matplotlib.pyplot as plt

x = [1,2,3,4,5,6,7,8,9,10,11,12]
z = [13,14,15,16,17,18,19,20,21,22,23,24]

# Equation Class, filled with useful procedures 
class Equation:
    def __init__(self, contents): 
        self.contents = contents
        self.equation = self.contents.replace(" ","").replace("y=","")
        
        if " x" in (" " + self.equation):
            self.equation = "1"+self.equation

        self.ac()
        self.x, self.y = self.evaluate()

    def ac(self):
        xPos = 0
        for i, I in enumerate(self.equation):
            if I.lower() == "x":
                xPos = i

        try:
            self.a = int(self.equation[:xPos]) if xPos > 0 else 1
        except ValueError:
            self.a = float(self.equation[:xPos]) if xPos > 0 else 1
        

        try:
            self.c = int(self.equation[xPos+2:])
        except ValueError:
            self.c = float(self.equation[xPos+2:])

    def __str__(self):
        return self.contents

    def __repr__(self):
        return self.contents

    def evaluate(self):
        x = []
        y = []

        for i in range(0,25):
            total = (self.a * i) + self.c
            x.append(i)
            y.append(total)

        return x,y

    def plot(self):
        plt.plot(self.x, self.y, color="black")
        
    def predict(self, x):
        yPrediction = []

        for i in x:
            total = (self.a * i) + self.c
            yPrediction.append(total)

        return yPrediction

# Global Subroutines
def findMean(data):
    total = 0
    tally = 0
    for i in data:
        total += i
        tally += 1

    mean = total / tally

    return mean

def sumVarTakeMean(data, mean): # Sum of variable - variable barred
    total = []

    for i in data:
        total.append(i - mean)

    return total

def sumVarTakeMeanSquared(data, mean): # Sum of (variable - variable barred) ** 2 
    total = 0

    for i in data:
        total += (i - mean) ** 2

    return total

def MultiplyArray(x, y):
    if type(x) is list and type(y) is list:
        total = 0
        for i, j in zip(x, y):
            total += i * j

        return total

    else:
        return x * y

def plot(x, y):
    plt.plot(x, y, color="red", dashes=[5, 5])

def FormEquation(x,y):
    xBar = findMean(x) # Mean of x
    sumXtakeXbar = sumVarTakeMean(x, xBar) # Sigma x - x barred
    sumXtakeXbarSquared = sumVarTakeMeanSquared(x, xBar) # Sigma (x - x barred) ** 2


    yBar = findMean(y) # Mean of y
    sumYtakeYbar = sumVarTakeMean(y, yBar) # Sigma y - y barred

    sigVarsTakeMean = MultiplyArray(sumXtakeXbar, sumYtakeYbar)

    m = sigVarsTakeMean / sumXtakeXbarSquared
    c = yBar - (m * xBar)


    return m, c, xBar, yBar

def Rsquare(y, yBar, yPred):
    predMinBar = []
    actMinBar = []

    for i, j in zip(yPred, y):
        totalPred = (i - yBar) ** 2
        totalAct = (j - yBar) ** 2
        predMinBar.append(totalPred)
        actMinBar.append(totalAct)

    sumPred = sum(predMinBar)
    sumAct = sum(actMinBar)

    rSquare = sumPred / sumAct

    return rSquare

def optimise(x, y, line_equ, yBar, m, c, r2):
    optimisedUp = False
    optimisedDown = False

    optimalUp = line_equ.contents
    optimalDown = line_equ.contents

    oldR2Up = r2
    oldR2Down = r2

    i = 0.1
    j = 0.1


    # Incrementing m and comparing the r^2 
    while not optimisedUp and i < 5:
        new_equation = Equation(f"y = {m+i}x + {c}")
        newPredictions = new_equation.predict(x)
        newR2Up = Rsquare(y, yBar, newPredictions)

        if (1 - newR2Up) < (1 -oldR2Up) and (1 - newR2Up) >= 0:
            optimalUp = new_equation.contents
            oldR2Up = newR2Up
            i += 0.1

        else:
            optimisedUp = True

    # Decrementing m and comparing the r^2 
    while not optimisedDown and j < 5:
        new_equation = Equation(f"y = {m-j}x + {c}")
        newPredictions = new_equation.predict(x)
        newR2Down = Rsquare(y, yBar, newPredictions)

        if (1 - newR2Down) < (1 - oldR2Down) and (1 - newR2Down) >= 0:
            optimalDown = new_equation.contents
            oldR2Down = newR2Down
            j += 0.1

        else:
            optimisedDown = True


    # Comparing the Incremented r^2 to the decremented r^2 to see which is closer to 1
    if (1 - newR2Down) < (1 - newR2Up):
        return Equation(optimalDown)

    elif (1 - newR2Down) > (1 - newR2Up):
        return Equation(optimalUp)

    else:
        return line_equ


if __name__ == "__main__":
    # Results
    
    y = [3,4,2,4,5,6,6,9,11,12,14,16]

    m, c, xBar, yBar = FormEquation(x, y)
    line_equ = Equation(f"y = {m}x + {c}")
    yPred = line_equ.predict(x)
    r2 = Rsquare(y, yBar, yPred)

    optimised_equation = optimise(x, y, line_equ, yBar, m, c, r2)

    predictions = optimised_equation.predict(x)
    r2 = Rsquare(y, yBar, predictions)

    plot(x, y)
    print(f"This line models the data with a {r2 * 100}% accuracy")
    plt.title(f"Sales Prediction Using Linear Regression\nAccuracy of approximately {round(r2 * 100)}%")
    optimised_equation.plot()
    plt.legend([optimised_equation], loc=2)
    plt.ylabel("Sales (£1000)")
    plt.xlabel("Time (Months)")

    plt.savefig("output.png")

    results = optimised_equation.y[12:]
    for i, I in enumerate(results):
        results[i] = round(I)

    plt.show()
