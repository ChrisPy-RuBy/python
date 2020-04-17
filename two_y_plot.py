import numpy as np
import matplotlib.pyplot as plt


t = np.arange(0.01, 10.0, 0.01)
y1 = np.exp(t)
y2 = np.sin(2 * np.pi * t)

def doubleYSingleXPlot(x, y1, y2, xlabel, y1label, y2label):

    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(y1label, color=color)
    ax1.plot(t, y1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color= 'tab:blue'
    ax2.set_ylabel(y2label, color=color)
    ax2.plot(t, y2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()
    plt.show()


def doubleYPlotsSingleX(x, y1, y2):

    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.5, 0.8, 0.4],
                       xticklabels=[], ylim=(-1.2, 10000), xlim=(0, 1000))
    ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.4],
                       ylim=(-1.2, 1.2), xlim=(0, 1000))
    ax1.plot(y1)
    ax2.plot(y2)
    plt.show()
    print("done")


doubleYPlotsSingleX(t, y1, y2)


#doubleYSingleXPlot(t, y1, y2, 'x', 'a', 'b')
