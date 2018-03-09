import os
import shutil
import xml
import copy
from Variables import *
from ExtractFeatures import *
from EvaluateNaming import *
from FileComparison import *
import math
import numpy as np
import plotly.plotly as py
import matplotlib.pyplot as plt
import pylab
from matplotlib.dates import date2num
import datetime
import plotly.plotly as py
import re
import collections
from collections import OrderedDict

class DeviationOveTime:
    def __init__(self, answers_features, students_submissions_features, students_list_path, output_path):
        self.deviations=OrderedDict()#key is the name of the student and value is a dictionary of the deviation of its answer in comparision with the correct answer        self.deviation_dir_input=input_path
        self.students_list_path=students_list_path
        self.students_list=[]

        self.answers=answers_features
        self.student_submissions=students_submissions_features

        self.feature_values={}
        self.file_names=[]

        self.measure()

        # self.var=Variables()
        deviation_dir=os.path.join(output_path, 'deviation graph')
        if os.path.exists(deviation_dir):
            shutil.rmtree(deviation_dir)

        os.makedirs(deviation_dir)

        for key,value in self.deviations.iteritems():#key is the students name and value is the deviation over time
            self.draw_deviation(value, deviation_dir, key)


    def measure(self):
        #get apps names
        apps_names=[]
        apps_names=self.answers.keys()

        #read list of students
        if len(os.listdir(self.students_list_path))>1:
            print 'students list is not correct'
            return

        for file in os.listdir(self.students_list_path):
            with open(os.path.join(self.students_list_path, file), 'r') as st_file:
                for line in st_file:
                    self.students_list.append(line.strip())


        #initialize deviation dictionary
        for st in self.students_list:
            cur_dev=OrderedDict()
            for app in apps_names:
                cur_dev[app]=0.0

            self.deviations[st]=copy.deepcopy(cur_dev)


        for app, submissions in self.student_submissions.iteritems():
            to_compare={}
            to_compare[app]=self.answers[app]
            for st,extracted_features in submissions.iteritems():
                self.file_names=[]
                self.feature_values={}
                to_compare[st]=copy.deepcopy(extracted_features)
                self.compare(to_compare)

                deviation_value=self.meaure_deviation(self.feature_values)

                # cur_dev={}
                # cur_dev[app]=deviation_value
                self.deviations[st][app]=deviation_value

                #delete current student's deviation from answer and go to the next students
                del[to_compare[st]]

    def compare(self,dic):
        features=self.get_feature_set(dic)
        for item in features:
            values=[]
            for file_name in self.file_names:
                values.append(self.find_feature_value(item, file_name, dic))

            self.feature_values[item]=values

        return self.feature_values

    def get_feature_set(self, dic):
        f=set()
        for key_outer, value_outer in dic.iteritems():
            self.file_names.append(key_outer)
            for key_inner,value_inn in dic[key_outer].iteritems():
                if type(dic[key_outer][key_inner]) is not set:
                    f.add(key_inner)

        return f

    def find_feature_value(self, item, file_name, dic):
        if item in dic[file_name]:
            return dic[file_name][item]
        else:
            return 0



        # root_dir=self.var.deviation_measurement_input_files
        # all_dirs=[name for name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, name))]
        #
        # for cur_dir in all_dirs:
        #     files=[]
        #     file_characteristics_for_comparison={}
        #     cur_dir_path=root_dir+'\\'+cur_dir
        #     for file in os.listdir(cur_dir_path):
        #         file_address=os.path.join(cur_dir_path, file)
        #         files.append(file_address)
        #
        #
        #     for file in files:
        #         features=self.extract_features(file)
        #         file_name=self.get_file_name(file)
        #         file_characteristics_for_comparison[file_name]=copy.deepcopy(features)
        #
        #     comp=FileComparison()
        #     feature_values=comp.compare(file_characteristics_for_comparison)
        #
        #     cur_deviation=self.meaure_deviation(feature_values)
        #     self.deviation_changes[cur_dir]=cur_deviation
        #
        # ordered_deviation_changes=self.sort_dictionary()
        # self.draw_deviation(ordered_deviation_changes)

    def get_file_name(self, file_address):
        address_splitted=file_address.split("\\")
        return address_splitted[-1].split('.xml')[0]

    def meaure_deviation(self, feature_values):

        if len(feature_values)==0:
            return 0.0


        weight=1.0
        dic_len=len(feature_values)
        sum_deviation=0.0

        for key,value in feature_values.iteritems():
            if self.distinct_feature(value):
                weight=6.0
            else:
                weight=1.0

            sum_deviation+=weight *(math.fabs(feature_values[key][0]-feature_values[key][1]))

        return round(sum_deviation/dic_len,2)


    def draw_deviation(self, deviations, output_dir, st_name):
        values=self.get_values(deviations)
        N = len(self.get_label_set(deviations))

        ind = np.arange(N)  # the x locations for the groups
        width = 0.35      # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, values, width, color='r')
        # rects2 = ax.bar(ind + width, values2, width, color='b')

        # add some text for labels, title and axes ticks
        ax.set_ylabel('Deviation Measure')
        ax.set_title('Devation from Tutorial for Submitted Apps')
        ax.set_xticks(ind + width)
        ax.set_xticklabels(self.get_label_set(deviations), rotation='vertical')

        self.autolabel(ax, rects1)
        # self.autolabel(ax, rects2)
        plt.tight_layout()

        # plt.draw()
        # fig1=plt.figure()

        output_path=output_dir+'\\'+st_name

        plt.savefig(output_path+'.png')
        # plt.show()

    def get_label_set(self, dic):
        label_set=[]
        for key,value in dic.iteritems():
            # key= self.label_refinement(key)
            label_set.append(key)

        return label_set


    def get_values(self, feature_values):
        vals=[]
        for key,value in feature_values.iteritems():
            vals.append(feature_values[key])

        return vals

    def autolabel(self, ax, rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 2.5*height,
                   '%d' % int(height),
                   ha='center', va='center')

    def sort_dictionary(self):
        # ordered_devation_changes={}
        od = collections.OrderedDict(sorted(self.deviation_changes.items()))

        # for key,value in od.iteritems():
        #     ordered_devation_changes[key]=self.deviation_changes[key]

        return od

    def distinct_feature(self, values):
        if values[0]==0 and values[1]!=0:
            return True

        if values[1]==0 and values[0]!=0:
            return True

        return False
