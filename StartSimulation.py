import copy
import os
import shutil
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree
from stat import S_IWRITE

from ExtractFeatures import *
from MeaningFullName import *
from EvaluateNaming import *
from FileComparison import *
from DrawChart import *
from Variables import *
from FileArrangement import *
from ElementSimilarity import *
from DeviationOverTime import *
from BuildGUI import *
from collections import OrderedDict


class StartSimulation:

    def __init__(self):
        self.var=Variables()
        self.file_characteristics_for_comparison=OrderedDict()
        bg=BuildGUI()

        #get GUI values
        file_paths_dic=bg.field_values
        self.var.answers=file_paths_dic['Answers']
        if not os.path.exists(self.var.answers):
            print "Error: "+self.var.answers +" file does not appear to exist."
            return

        self.var.submissions=file_paths_dic['All submissions']
        if not os.path.exists(self.var.submissions):
            print "Error: "+self.var.submissions +" file does not appear to exist."
            return

        self.var.students_list=file_paths_dic['Students list']
        if not os.path.exists(self.var.students_list):
            print "Error: "+self.var.students_list +" file does not appear to exist."
            return

        self.var.output=file_paths_dic['Output']
        path=''
        for item in self.var.output.strip().split('\\')[0:-1]:
            path+=item+'\\'

        if not os.path.exists(path):
            print "Error: "+path +" file does not appear to exist."
            return


        self.answers=OrderedDict()#key is app name and value is the list of features
        self.extract_answers_features()

        self.students_submissions_features=OrderedDict()#first key is app name, second key is student name, value is the list of features
        self.extract_students_submissions_features()

        def del_rw(action, name, exc):
            os.chmod(name, os.stat.S_IWRITE)
            os.remove(name)
        #creae output directory and if exists remove it
        if os.path.exists(self.var.output):
            shutil.rmtree(self.var.output, onerror=del_rw)

        os.makedirs(self.var.output)
        app_comparison_path=os.path.join(self.var.output, 'comparison')
        os.makedirs(app_comparison_path)


        for app, submissions in self.students_submissions_features.iteritems():#for each app in all submitted apps
            #retrive answers features
            self.file_characteristics_for_comparison['Answer']=copy.deepcopy(self.answers[app])

            cur_app_path=os.path.join(app_comparison_path, app)
            os.makedirs(cur_app_path)

            for st_name, st_features in submissions.iteritems():#for each students submissions
                if len(st_features)==0:
                    print st_name+' \'s submissions does not have any features'
                    continue

                self.file_characteristics_for_comparison[st_name]=copy.deepcopy(st_features)

                dest_path=cur_app_path+'\\'+self.file_characteristics_for_comparison.keys()[0]+' , '+self.file_characteristics_for_comparison.keys()[1]
                comp=FileComparison(dest_path)
                feature_values=comp.compare(self.file_characteristics_for_comparison)
                feature_values_variables=comp.compare_variables(self.file_characteristics_for_comparison)

                dc=DrawChart(dest_path)
                # print self.file_characteristics_for_comparison.keys()
                dc.draw(feature_values, self.file_characteristics_for_comparison.keys())

                dc.draw_variables(feature_values_variables, self.file_characteristics_for_comparison.keys())

                del[self.file_characteristics_for_comparison[st_name]]


        dt=DeviationOveTime(self.answers, self.students_submissions_features, self.var.students_list, self.var.output)

    def get_file_name(self, file_address):
        address_splitted=file_address.split("\\")
        return address_splitted[-2]

    def extract_features(self, file_address):
        tree = xml.etree.ElementTree.parse(file_address)
        tree=tree.getroot()

        ef=ExtractFeatures()
        ef.extract(tree)

        en=EvaluateNaming()
        ef.extracted_features['variable_meaning']=en.evaluate(ef.extracted_features)*10.00

        return ef.extracted_features


    def get_xml_file(self, base_dir):
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".xml"):
                    file_address=os.path.join(root, file)
                    break

        return file_address

    def extract_answers_features(self):
        app_paths=OrderedDict()#key is app name and value is app_path
        for app in os.listdir(self.var.answers):
            app_paths[app]=os.path.join(self.var.answers, app)

        for key,value in app_paths.iteritems():
            FileArrangement(value)
            app_xml_path=self.get_xml_file(value)
            features={}
            features=self.extract_features(app_xml_path)
            #features_variables_answers=list(features['field_text'])
            self.answers[key]=copy.deepcopy(features)

    def extract_students_submissions_features(self):

        for app in os.listdir(self.var.submissions):#for each app in all submitted apps
            print app
            cur_app_submission_features=[]
            cur_app_path=os.path.join(self.var.submissions, app)

            st_features={}#key is student name and value is set of extracted features
            for student_sub in os.listdir(cur_app_path):#for each students submissions
                student_name=student_sub.split('_')[0]
                cur_submission_path=os.path.join(cur_app_path, student_sub)

                #convert the .bky to .xml file
                if not FileArrangement(cur_submission_path):
                    print student_name+' \' submissions does not have .bky file'
                    continue

                #get the xml file
                app_xml_path=self.get_xml_file(cur_submission_path)

                features=self.extract_features(app_xml_path)
                #feature_variable_submission=list(features['field_text'])
                st_features[student_name]=copy.deepcopy(features)

            self.students_submissions_features[app]=copy.deepcopy(st_features)
















