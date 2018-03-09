import os

import matplotlib.pyplot as plt
import pylab
from matplotlib.dates import date2num
import datetime
import plotly.plotly as py
import numpy as np
import re
from Variables import*
import matplotlib.patches as mpatches

class DrawChart:

    def __init__(self, output):
        self.output_path=output
        pass

    def draw(self, feature_values, file_names):

        values1=self.get_values(feature_values, 0)
        values2=self.get_values(feature_values, 1)
        N = len(self.get_label_set(feature_values))

        ind = np.arange(N)  # the x locations for the groups
        width = 0.35      # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, values1, width, color='r')
        rects2 = ax.bar(ind + width, values2, width, color='b')

        # add some text for labels, title and axes ticks
        ax.set_ylabel('Feature Comparison')
        ax.set_title('Feature Comparison of Two Submitted Codes')
        ax.set_xticks(ind + width)
        #ax.set_yticks(0,1,1.0)
        ax.set_xticklabels(self.get_label_set(feature_values), rotation='vertical')

        ax.legend((rects1[0], rects2[0]), (file_names[0], file_names[1]))

        self.autolabel(ax, rects1)
        self.autolabel(ax, rects2)
        plt.tight_layout()

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)


        plt.savefig(self.output_path+'\\'+file_names[1]+', '+file_names[0]+'.png')
        plt.close(fig)

    def draw_variables(self, feature_values_variables, file_names):

        values3=self.get_values_variables(feature_values_variables)
        M = len(self.get_label_set_variables(feature_values_variables))

        ind = np.arange(M)  # the x locations for the groups
        width = 0.35      # the width of the bars

        fig, ax = plt.subplots()
        rects3 = ax.bar(ind, values3, width, color='r')

        # add some text for labels, title and axes ticks
        ax.set_ylabel('Total Progress')
        ax.set_title('Features')
        ax.set_xticks(ind)
        ax.set_xticklabels(self.get_label_set_variables(feature_values_variables), rotation='vertical')
        ax.set_ylim(0,1)
        red_patch = mpatches.Patch(color='red', label='Attribute Value')
        plt.legend(handles=[red_patch])
        self.autolabel_variables(ax, rects3)
        plt.tight_layout()
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)


        plt.savefig(self.output_path+'\\'+file_names[1]+',., '+file_names[0]+'.png')
        plt.close(fig)

    def get_label_set(self, feature_values):
        label_set=[]
        for key,value in feature_values.iteritems():
            # key= self.label_refinement(key)
            label_set.append(key)

        return self.label_refinement(label_set)


    def get_values(self, feature_values, index):
        vals=[]
        for key,value in feature_values.iteritems():
            vals.append(feature_values[key][index])

        return vals

    def autolabel(self, ax, rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.4*height,
                   '%d' % int(height),
                   ha='center', va='center')

    def label_refinement(self, key_list):

        for i in range(len(key_list)):
            refined_item=self.refine(key_list[i])
            key_list[i]=refined_item

        return key_list

    def refine(self, key):
        if key=='COMPONENT_SELECTOR field':
            key='COMPONENT_SELECTOR'.lower()

        if 'procedures' in key:
            key=key.replace('procedures', 'proc').lower()

        if 'lexical' in key:
            key=key.replace('lexical', '').lower()

        if '_' in key:
            key=key.replace('_', ' ').lower()

        key = re.sub("([a-z])([A-Z])","\g<1> \g<2>", key)


        return key.title()

    def get_label_set_variables(self, feature_values):
        label_set=[]
        for key,value in feature_values.iteritems():
            # key= self.label_refinement(key)
            label_set.append(key)

        return self.label_refinement(label_set)


    def get_values_variables(self, feature_values):
        vals=[]
        for key,value in feature_values.iteritems():
            vals.append(value)

        return vals

    def autolabel_variables(self, ax, rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.4*height,
                   '%d' % int(height),
                   ha='center', va='center')

    def label_refinement_variables(self, key_list):

        for i in range(len(key_list)):
            refined_item=self.refine(key_list[i])
            key_list[i]=refined_item

        return key_list

    def refine_variables(self, key):
        if key=='COMPONENT_SELECTOR field':
            key='COMPONENT_SELECTOR'.lower()

        if 'procedures' in key:
            key=key.replace('procedures', 'proc').lower()

        if 'lexical' in key:
            key=key.replace('lexical', '').lower()

        if '_' in key:
            key=key.replace('_', ' ').lower()

        key = re.sub("([a-z])([A-Z])","\g<1> \g<2>", key)


        return key.title()

