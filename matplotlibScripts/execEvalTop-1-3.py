import matplotlib.pyplot as plt
import sys, operator
import os
import time
import math
import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm
import argparse
import threading
import copy

from matplotlib.patches import Ellipse, Polygon
from numpy import nan

def some_Stuff():
    #Set pattern array
    patterns = ('-', '+', 'x', '\\', '*', 'o', 'O', '.')

    font = {'size'   : 18}

    plt.rc('font', **font)

    N = 3

    Types = 1
    ind = np.arange(N)  # the x locations for the groups
    width = 1.0/ (Types + 2)     # the width of the bars

def adjustFigAspect(fig,aspect=1):
    '''
    Adjust the subplot parameters so that the figure has the correct
    aspect ratio.
    '''
    xsize,ysize = fig.get_size_inches()
    minsize = min(xsize,ysize)
    xlim = .45*minsize/xsize
    ylim = .45*minsize/ysize
    if aspect < 1:
        xlim *= aspect
    else:
        ylim /= aspect
    fig.subplots_adjust(left=.5-xlim,
                        right=.5+xlim,
                        bottom=.5-ylim,
                        top=.5+ylim)

    #fig, ax = plt.subplots()


def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)


def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom', rotation='vertical')

if __name__ == "__main__":
    font = {'size'   : 14}
    plt.rc('font', **font)
     
    top3_F1 = [0.864, 0.729, 0.289, 0.047, 0.0006] 
    top1_F1 = [0.794, 0.621, 0.045, 0.04, 0.00002] 
    Types = 5
    barwidth = 1.0/(Types+2)
    
    r1 = np.arange(len(top3_F1))
    r2 = [x+barwidth for x in r1]
    fig, ax = plt.subplots()
    rects1 = ax.bar(r1, top3_F1, color='deepskyblue', width = barwidth, edgecolor='black', label='F1(Top-3)', hatch='*') 
    rects2 = ax.bar(r2, top1_F1, color='lightcoral', width = barwidth, edgecolor='black', label='F1(Top-1)', hatch='x') 

    ax.set_title('Query Execution - Top-3 vs. Top-1\n (Course Website)', fontsize=22)
    ax.set_xticks(r1+barwidth)
    ax.set_xticklabels(('Q-Learn', 'RNN-S', 'CF-SVD', 'CF-Cos', 'RNN-H'), fontsize=25)
    #ax.set_yscale('log')
    #plt.ylabel('log-scale',fontsize=20)
    plt.yticks(np.arange(0, 1.1, 0.2),fontsize=25)
    ax.tick_params(labelsize=16)
    ax.legend(bbox_to_anchor=(0.5,-0.05), loc='upper center', ncol=2, prop={'size':14})
    
    #autolabel(rects1, "center")
    #autolabel(rects2, "center")
    #autolabel(rects3, "center")
    fig.tight_layout()
    #plt.savefig('sustQualityCourse.eps')
    plt.show()
    

    '''
    #t1 = np.arange(0.0, 5.0, 0.1)
    #t2 = np.arange(0.0, 5.0, 0.02)
    fig = plt.figure()
    #adjustFigAspect(fig,aspect=1)
    #plt.subplots_adjust(top=0.88)
    some_Stuff()
    #plt.plot(cols[tokens[6]], cols[tokens[0]], 'r', linewidth=2, marker = 'x', label = 'QBC(2)')
    #plt.plot(cols[tokens[6]], cols[tokens[1]], 'g', linewidth = 2, marker = '+', label= 'Margin')
    #plt.plot(cols[tokens[6]], cols[tokens[0]], 'r--', linewidth = 2, label = 'createQBC(2)')
    #plt.plot(cols[tokens[6]], cols[tokens[1]], 'b--', linewidth = 2, label = 'createQBC(20)')
    plt.plot(cols[tokens[4]], cols[tokens[0]], 'r', linewidth = 4, marker = '^', markevery=50, markersize = 12, label= 'Trees(2)')
    plt.plot(cols[tokens[4]], cols[tokens[1]], 'b', linewidth = 4, marker = '*', markevery=50, markersize = 12, label= 'Trees(10)')
    plt.plot(cols[tokens[4]], cols[tokens[2]], 'g', linewidth = 4, marker = 'o', markevery=50, markersize = 12, label= 'Trees(20)')
    #plt.plot(cols[tokens[5]][0:len(cols[tokens[3]])], cols[tokens[3]], 'm', linewidth = 4, marker = 'v', markevery=50, markersize = 12, label= 'Rules(LFP/LFN)')
    
    plt.xticks(np.arange(0,2500,500))
    plt.xlabel('#Labeled Examples',fontsize=20)
    #plt.yticks(np.arange(0, 1.1, 0.1))
    plt.yscale('log')
    plt.ylabel('Depth',fontsize=20)
    plt.title("Depth of Tree-based Classifiers\nCora")
    plt.legend(loc = 'best') 
    #plt.plot([1,2,3,4],[5,6,7,8], 'ro')
    #plt.savefig('Cora-forestDepth.eps')
    plt.show()
    '''
