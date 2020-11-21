import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

from square import Square

class Pflanze:

    COLORS = [
        "#ef5350",
        "#AB47BC",
        "#5C6BC0",
        "#26C6DA",
        "#66BB6A",
        "#FFEE58",
        "#FFA726"
    ]

    def __init__(self):
        self.a = 1
        self.u = 4
        self.n = 0
        self.squrs = 1
        self.drawLimit = 8

        self.baseSquare = Square((1.5, 1.5), 1, Square.NONE, None)
        self.lastSquares = [self.baseSquare]

        self.animation = None
        self.ax = None
        self.fig = None

    def startGui(self):
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        plt.subplots_adjust(right=.6)

        ax.set_xlim([0, 4])
        ax.set_ylim([0, 4])

        ax.set_aspect("equal", adjustable="box")

        plt.grid(b=True, which='major', color='#666666', linestyle='--', alpha=.8)

        ax.plot(self.baseSquare.getXPoints(), self.baseSquare.getYPoints())
        # self.ax.add_patch(self.baseSquare.getRect())


        '''for i in range(6):
            self.step()'''

        # buttons and stuff
        axStepBtn = plt.axes([.625, .175, .2, .05])
        axResetBtn = plt.axes([.625, .1, .2, .05])

        btnStep = Button(axStepBtn, "nächster Schritt")
        btnReset = Button(axResetBtn, "Zurücksetzen")
        self.text = self.fig.text(.625, .7, "")
        self.drawText()

        btnStep.on_clicked(lambda event: self.step(ax))
        btnReset.on_clicked(lambda event: self.reset(ax))

        plt.show()
    
    def step(self, ax):

        if self.n < self.drawLimit:
            oldSquares = self.lastSquares.copy()
            self.lastSquares.clear()

            for oldSquare in oldSquares:

                newSquares = oldSquare.getChilds()
                for newSquare in newSquares:
                
                    self.lastSquares.append(newSquare)
                    ax.plot(newSquare.getXPoints(), newSquare.getYPoints())

        newSquaresCount = 4*3**self.n
        self.squrs += newSquaresCount
        self.n += 1
        squareSize = 1/3**self.n
        print(squareSize)
        self.a += squareSize**2 * newSquaresCount
        self.u += squareSize * 2 * newSquaresCount

        self.drawText()

        self.fig.canvas.draw()

    def reset(self, ax):
        self.a = 1
        self.u = 4
        self.n = 0
        self.squrs = 1

        self.lastSquares = [self.baseSquare]

        ax.clear()

        ax.grid(b=True, which='major', color='#666666', linestyle='--', alpha=.8)

        ax.set_xlim([0, 4])
        ax.set_ylim([0, 4])

        ax.set_aspect("equal", adjustable="box")

        ax.plot(self.baseSquare.getXPoints(), self.baseSquare.getYPoints())

        self.drawText()

        self.fig.canvas.draw()

    def drawText(self):
        if self.n < self.drawLimit:
            self.text.set_text("A = {:n}\nU = {:n}\nn = {:n}\nAnzahl an Quadraten:\n{:e}"
                               .format(self.a, self.u, self.n, self.squrs))
        else:
            self.text.set_text("A = {:n}\nU = {:n}\nn = {:n}\nAnzahl an Quadraten:\n{:e}"
                               "\n\nDie Quadrate werden nun\nnicht mehr gezeichnet!"
                               .format(self.a, self.u, self.n, self.squrs))

if __name__ == "__main__":
    qp = Pflanze()
    qp.startGui()