import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider


class Main:

    def __init__(self):
        self.sMax = 1
        self.k = 4
        self.y = np.linspace(2*np.pi, -2*np.pi, 500)

        self.ax = None
        self.fig = None

    def initGui(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        plt.subplots_adjust(top=.8)


        self.ax.set_ylim([-2*np.pi, 2*np.pi])
        plt.plot(self.a(self.sMax, self.y, self.k), self.y)

        axk = plt.axes([.15, .95, .7, .02])
        self.sk = Slider(axk, "Spaltzahl", valmin=2, valmax=100, valstep=1)

        axsMax = plt.axes([.15, .9, .7, .02])
        self.ssMax = Slider(axsMax, "Amplitude", valmin=1, valmax=100, valstep=1)

        self.sk.on_changed(self.redraw)
        self.ssMax.on_changed(self.redraw)

        plt.show()

    def redraw(self, event):
        self.sMax = int(self.ssMax.val)
        self.k = int(self.sk.val)

        self.ax.clear()
        self.ax.set_ylim([-2*np.pi, 2*np.pi])
        self.ax.plot(self.a(self.sMax, self.y, self.k), self.y)

        self.fig.canvas.draw()

    def a(self, sMax, phi, k):
        x = 1
        y = 0
        for i in range(1, k):
            x += np.cos(i*phi)
            y += np.sin(i*phi)
        return sMax * np.sqrt(x**2 + y**2)


if __name__ == "__main__":
    m = Main()
    m.initGui()
    #plt.plot(y, a(1, y, 10))
    #plt.show()
