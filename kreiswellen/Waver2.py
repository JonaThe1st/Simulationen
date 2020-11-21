#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
import time


class Waver:

    def __init__(self, l, a, c, d, e, y):
        self.l1 = 2*np.pi/l
        self.a1 = a
        self.l2 = 2*np.pi/l
        self.a2 = a
        self.c = c
        self.d = d
        self.e = e
        self.y = y
        self.trX = 0
        self.trY = 0
        self.running = 0

        self.bounds = 15
        self.meshgridLength = 50

        self.showTr = False
        self.axtrPlot = None
        self.trPlot = None
        self.trPlotX = np.linspace(9, 0, 50)
        self.trPlotY = []
        self.trPlotLine = None

        self.initGui()

    def initGui(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        fig.canvas.mpl_connect('close_event', self.onClose)

        self.timeText = fig.text(0.075, 0.775, "Zeit:")

        # display widgets
        axcolor = 'lightgoldenrodyellow'

        axl1 = plt.axes([0.075, 0.975, 0.35, 0.01], facecolor=axcolor)
        axa1 = plt.axes([0.075, 0.95, 0.35, 0.01], facecolor=axcolor)

        axl2 = plt.axes([.075, 0.925, 0.35, 0.01], facecolor=axcolor)
        axa2 = plt.axes([.075, 0.9, 0.35, 0.01], facecolor=axcolor)

        axc = plt.axes([0.525, 0.975, 0.35, 0.01], facecolor=axcolor)
        axe = plt.axes([.525, 0.95, 0.35, 0.01], facecolor=axcolor)
        axd = plt.axes([0.525, 0.925, 0.35, 0.01], facecolor=axcolor)
        axy = plt.axes([0.525, 0.9, 0.35, 0.01], facecolor=axcolor)
        axmeshgrid = plt.axes([0.525, 0.875, 0.35, 0.01], facecolor=axcolor)

        axtrx = plt.axes([0.15, 0.845, 0.8, 0.01], facecolor=axcolor)
        axtry = plt.axes([0.15, 0.82, 0.8, 0.01], facecolor=axcolor)

        startax = plt.axes([0.85, 0.175, 0.1, 0.03])
        stopax = plt.axes([0.85, 0.125, 0.1, 0.03])
        showtrax = plt.axes([0.85, 0.075, .1, .03])

        self.sl1 = Slider(axl1, 'lambda1', 1, 20, valinit=2*np.pi/self.l1, valstep=.5)
        self.sa1 = Slider(axa1, 'Amp1', 0.1, 5, valinit=self.a1, valstep=.1)
        self.sl2 = Slider(axl2, 'lambda2', 1, 20, valinit=2*np.pi/self.l2, valstep=.5)
        self.sa2 = Slider(axa2, 'Amp2', 0.1, 5, valinit=self.a2, valstep=.1)

        self.sc = Slider(axc, "c", .05, 1, valinit=self.c, valstep=.05)
        self.sd = Slider(axd, "dphi1", 0, 2., valinit=self.d, valstep=.1)
        self.se = Slider(axe, "e", 1, 20, valinit=self.e, valstep=.5)
        self.sy = Slider(axy, "y", 0, 10, valinit=self.y, valstep=.5)
        self.smg = Slider(axmeshgrid, "Teilchen/Reihe", 30, 100, valinit=50, valstep=5)

        strx = Slider(axtrx, "Testträgerteilchen X", -10, 10, valinit=0, valstep=.02)
        stry = Slider(axtry, "Testträgerteilchen Y", -10, 10, valinit=0, valstep=.02)

        strx.on_changed(self.setTrX)
        stry.on_changed(self.setTrY)

        btnStart = Button(startax, '(Re)start', color=axcolor, hovercolor='0.975')
        btnStop = Button(stopax, 'stop', color=axcolor, hovercolor='0.975')
        btnShowTr = Button(showtrax, "zeige trägerteilchen", color=axcolor, hovercolor='0.975')

        btnStart.on_clicked(lambda event: self.start(ax))
        btnStop.on_clicked(self.stop)
        btnShowTr.on_clicked(self.toggleTr)

        self.tr, = ax.plot([self.trX, self.trX], [self.trY, self.trY], zs=[-self.bounds, self.bounds], c="green")
        print(id(ax))

        self.axtrPlot = plt.axes([0.02, 0.05, 0.2, 0.2])
        self.trPlot, = plt.plot(9, 0, "o")

        plt.get_current_fig_manager().window.showMaximized()
        # wm = plt.get_current_fig_manager()
        # wm.window.state('zoomed')

        plt.show()

    def onClose(self, event):
        plt.close("all")
        self.running += 1
        del self

    def stop(self, event):
        self.running += 1
        print(self.running)

    """def generate(self, x1, x2, y, t):
        sqrY = y**2
        h1 = self.l1 * np.sqrt(x1**2+sqrY) - self.c*t
        h2 = self.l2 * np.sqrt(x2**2+sqrY) - self.c*t
        return np.where(h1 > 0, 0, self.a1 * np.sin(h1-self.d)) + np.where(h2 > 0, 0, self.a2 * np.sin(h2))"""

    def generate_performant(self, h1, h2, t):
        cxt = self.c*t
        return np.where(h1 > cxt, 0, self.a1 * np.sin(h1-cxt-self.d)) + np.where(h2 > cxt, 0, self.a2 * np.sin(h2-cxt))

    def generate_old(self, x, y, t):
        sqrY = (y+self.y)**2
        h1 = self.l1 * np.sqrt((x-self.e)**2+sqrY) - self.c*t
        h2 = self.l2 * np.sqrt((x+self.e)**2+sqrY) - self.c*t
        return np.where(h1 > 0, 0, self.a1 * np.sin(h1-self.d)) + np.where(h2 > 0, 0, self.a2 * np.sin(h2))

    def start(self, ax):

        self.running+=1
        print(self.running)
        id = self.running

        plt.pause(.1)
        ax.clear()
        self.tr, = ax.plot([self.trX, self.trX], [self.trY, self.trY], zs=[-self.bounds, self.bounds], c="green")
        ax.set_zlim(-self.bounds, self.bounds)
        t = 0
        wframe = None
        oszs = None
        tr = None

        # read values from sliders:
        self.l1 = 2*np.pi/self.sl1.val
        self.a1 = self.sa1.val
        self.l2 = 2*np.pi/self.sl2.val
        self.a2 = self.sa2.val
        self.c = self.sc.val
        self.d = self.sd.val/2*self.sl1.val
        self.e = self.se.val/2
        self.y = self.sy.val
        mgLength = int(self.smg.val)
        print(self.e)

        self.axtrPlot.axis([0, 10, (-self.a1-self.a2)*1.1, (self.a1+self.a2)*1.1])

        # Make the X, Y meshgrid.
        xs = np.linspace(-self.bounds, self.bounds, mgLength)
        ys = np.linspace(-self.bounds, self.bounds, mgLength)
        X, Y = np.meshgrid(xs, ys)

        x1 = X-self.e
        x2 = X+self.e
        y = Y + self.y

        h1 = self.l1 * np.sqrt(x1**2+y**2)
        h2 = self.l2 * np.sqrt(x2**2+y**2)

        oszx = np.array([-self.e, self.e])
        oszy = np.array([-self.y, -self.y])

        ax.plot([0-self.e, 0-self.e], [-self.y, -self.y], zs=[-self.bounds, self.bounds], c="red", zorder=1)
        ax.plot([0+self.e, 0+self.e], [-self.y, -self.y], zs=[-self.bounds, self.bounds], c="red", zorder=1)

        tstart = time.time()
        # Begin plotting.
        while self.running == id:
            # If a line collection is already remove it before drawing.
            if wframe:
                ax.collections.remove(wframe)
            if oszs:
                ax.collections.remove(oszs)
            if tr:
                ax.collections.remove(tr)
                tr = None

            if self.showTr:
                z = self.generate_old(self.trX, self.trY, t)
                tr = ax.scatter(self.trX, self.trY, zs=z+7, zorder=2, c="yellow", s=500, alpha=1)
                self.drawLine(z, t)

            Z = self.generate_performant(h1, h2, t)
            wframe = ax.plot_surface(X, Y, Z, color="blue", cstride=1, rstride=1,  zorder=-1)

            z = self.generate_old(oszx, oszy, t)+7
            oszs = ax.scatter(oszx, oszy, zs=z, zorder=2, c="green", s=500, alpha=1)

            self.timeText.set_text("Zeit: " + str(t))
            t += 1

            plt.pause(.1)

        print('Average FPS: %f' % (t/(time.time() - tstart)))


    def setTrX(self, x):
        self.trX = x
        self.redrawTr()


    def setTrY(self, y):
        self.trY = y
        self.redrawTr()

    def redrawTr(self):
        ax = self.tr.axes
        ax.lines.remove(self.tr)
        self.tr, = ax.plot([self.trX, self.trX], [self.trY, self.trY], zs=[-self.bounds, self.bounds], c="green")

    def toggleTr(self, event):
        self.showTr = not self.showTr

    def drawLine(self, z, t):
        while len(self.axtrPlot.lines) > 0:
            for line in self.axtrPlot.lines:
                line.remove()

        self.trPlot, = self.axtrPlot.plot(9, z, "bo")

        if len(self.trPlotY) == 50:
            self.trPlotY.pop(49)

        self.trPlotY.insert(0, z)
        if len(self.trPlotY) < self.trPlotX.size:
            x = self.trPlotX[0:len(self.trPlotY)]
            self.trPlotLine = self.axtrPlot.plot(x, self.trPlotY, c="green")
        else:
            self.trPlotLine = self.axtrPlot.plot(self.trPlotX, self.trPlotY, c="green")


if __name__ == "__main__":
    w = Waver(6, 1, .2, 0, 5, 0)
