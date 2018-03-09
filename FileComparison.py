import os
from math import *

from Variables import *

class FileComparison:
    def __init__(self, path):
        # self.var=Variables()
        self.output_path=path
        self.file_names=[]
        self.feature_values={}
        self.feature_values_variables={}
        self.feature_values_variables['app_completion']=""
        self.feature_values_variables['creativeness'] = ""
        self.feature_values_variables['understanding']=""
        self.z=0.0
        self.y=0.0
        self.dict_file1 = open("C:/Users/rohit/Desktop/app1variables.txt", "r")
        self.dict_file2 = open("C:/Users/rohit/Desktop/app2variables.txt", "r")
        self.dict_file3 = open("C:/Users/rohit/Desktop/app3variables.txt", "r")
        self.dict_file4 = open("C:/Users/rohit/Desktop/app4variables.txt", "r")
        self.dict_file5 = open("C:/Users/rohit/Desktop/app5variables.txt", "r")
        self.dict_file6 = open("C:/Users/rohit/Desktop/app6variables.txt", "r")

        pass

    def compare(self,dic):
        features=self.get_feature_set(dic)
        for item in features:
            values=[]
            for file_name in self.file_names:
                values.append(self.find_feature_value(item, file_name, dic))

            self.feature_values[item]=values

        self.find_distinguisable_features(dic)
        return self.feature_values

    def jaccard_similarity(self,x, y):

        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality / float(union_cardinality)

    def compare_variables(self,dic):
        features_variables = self.get_feature_set_variable(dic)
        feature_set = {}  # key is file name and value is key set
        for key_outer, value_outer in dic.iteritems():
            feature_set[key_outer] = dic[key_outer].keys()

        file_names = feature_set.keys()

        first_not_in_second = []
        for f in feature_set[file_names[0]]:
            if not f in feature_set[file_names[1]]:
                first_not_in_second.append(f)

        second_not_in_first = []
        for f in feature_set[file_names[1]]:
            if not f in feature_set[file_names[0]]:
                second_not_in_first.append(f)

        sim=round(self.jaccard_similarity(feature_set[file_names[0]],feature_set[file_names[1]]),2)

        folder_name = '\\' + file_names[0] + ' , ' + file_names[1]

        # new_path = self.output_path+folder_name
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)


        if "app1" in self.output_path:
            if sim>(0.6):
                self.feature_values_variables['app_completion'] = sim
                if len(second_not_in_first) != 0:
                    self.feature_values_variables['creativeness'] = 1.0
                else:
                    self.feature_values_variables['creativeness'] = 0.0
            else:
                self.feature_values_variables['app_completion'] = sim
        if "app2" in self.output_path:
            if (sim>(0.85) or sim==(0.85)):
                self.feature_values_variables['app_completion'] = sim
                if len(second_not_in_first) != 0:
                    self.feature_values_variables['creativeness'] = 1.0
                else:
                    self.feature_values_variables['creativeness'] = 0.0
            else:
                self.feature_values_variables['app_completion'] = sim
        if "app3" in self.output_path:
            if sim>(0.85):
                self.feature_values_variables['app_completion'] = sim
                if len(second_not_in_first) != 0:
                    self.feature_values_variables['creativeness'] = 1.0
                else:
                    self.feature_values_variables['creativeness'] = 0.0
            else:
                self.feature_values_variables['app_completion'] = sim
        if "app4" in self.output_path:
            if sim>(0.7):
                self.feature_values_variables['app_completion'] = sim
                if len(second_not_in_first) != 0:
                    self.feature_values_variables['creativeness'] = 1.0
                else:
                    self.feature_values_variables['creativeness'] = 0.0
            else:
                self.feature_values_variables['app_completion'] = sim
        if "app5" in self.output_path:
            if sim>(0.75):
                self.feature_values_variables['app_completion'] = sim
                if len(second_not_in_first) != 0:
                    self.feature_values_variables['creativeness'] = 1.0
                else:
                    self.feature_values_variables['creativeness'] = 0.0
            else:
                self.feature_values_variables['app_completion'] = sim
        if "app6" in self.output_path:
            if sim>(0.75):
                self.feature_values_variables['app_completion'] = sim
                if len(second_not_in_first) != 0:
                    self.feature_values_variables['creativeness'] = 1.0
                else:
                    self.feature_values_variables['creativeness'] = 0.0
            else:
                self.feature_values_variables['app_completion'] = sim

        return self.feature_values_variables


    def get_feature_set(self, dic):
        f=set()
        for key_outer, value_outer in dic.iteritems():
            self.file_names.append(key_outer)
            for key_inner,value_inn in dic[key_outer].iteritems():
                if type(dic[key_outer][key_inner]) is not set:
                    f.add(key_inner)
        return f

    def get_feature_set_variable(self,dic):
        g=[]
        h=[]
        for key_outer,value_outer in dic.iteritems():
            if "Answer" in key_outer:
                if "field_text" in value_outer.keys():
                    g.append(list(value_outer['field_text']))
            else:
                if "field_text" in value_outer.keys():
                    h.append(list(value_outer['field_text']))
        lines1 = self.dict_file1.read().split('\n')
        lines2 = self.dict_file2.read().split('\n')
        lines3 = self.dict_file3.read().split('\n')
        lines4 = self.dict_file4.read().split('\n')
        lines5 = self.dict_file5.read().split('\n')
        lines6 = self.dict_file6.read().split('\n')
        if "app1" in self.output_path:
            if(len(h)!=0):
                for i in range(len(h)):
                    for j in range(len(h[i])):
                        #print(h[i][j])
                        for k in lines1:
                            #print(lines[k])
                            if str(h[i][j])==str(k):
                                #print(str(h[i][j])+" "+str(k))
                                self.y=self.y+1
                #print(round(self.y/len(h[0]),2))
                self.feature_values_variables['understanding'] =(round(self.y/len(h[0]),2))
        if "app2" in self.output_path:
            if(len(h)!=0):
                for i in range(len(h)):
                    for j in range(len(h[i])):
                        #print(h[i][j])
                        for k in lines2:
                            #print(lines[k])
                            if str(h[i][j])==str(k):
                                #print(str(h[i][j])+" "+str(k))
                                self.y=self.y+1
                #print(round(self.y/len(h[0]),2))
                self.feature_values_variables['understanding'] =(round(self.y/len(h[0]),2))
        if "app3" in self.output_path:
            if(len(h)!=0):
                for i in range(len(h)):
                    for j in range(len(h[i])):
                        #print(h[i][j])
                        for k in lines3:
                            #print(lines[k])
                            if str(h[i][j])==str(k):
                                #print(str(h[i][j])+" "+str(k))
                                self.y=self.y+1
                #print(round(self.y/len(h[0]),2))
                self.feature_values_variables['understanding'] =(round(self.y/len(h[0]),2))
        if "app4" in self.output_path:
            if(len(h)!=0):
                for i in range(len(h)):
                    for j in range(len(h[i])):
                        #print(h[i][j])
                        for k in lines4:
                            #print(lines[k])
                            if str(h[i][j])==str(k):
                                #print(str(h[i][j])+" "+str(k))
                                self.y=self.y+1
                #print(round(self.y/len(h[0]),2))
                self.feature_values_variables['understanding'] =(round(self.y/len(h[0]),2))
        if "app5" in self.output_path:
            if(len(h)!=0):
                for i in range(len(h)):
                    for j in range(len(h[i])):
                        #print(h[i][j])
                        for k in lines5:
                            #print(lines[k])
                            if str(h[i][j])==str(k):
                                #print(str(h[i][j])+" "+str(k))
                                self.y=self.y+1
                #print(round(self.y/len(h[0]),2))
                self.feature_values_variables['understanding'] =(round(self.y/len(h[0]),2))
        if "app6" in self.output_path:
            if(len(h)!=0):
                for i in range(len(h)):
                    for j in range(len(h[i])):
                        #print(h[i][j])
                        for k in lines6:
                            #print(lines[k])
                            if str(h[i][j])==str(k):
                                #print(str(h[i][j])+" "+str(k))
                                self.y=self.y+1
                #print(round(self.y/len(h[0]),2))
                self.feature_values_variables['understanding'] =(round(self.y/len(h[0]),2))




        print('hello')
        '''if ((len(h[0]))>len(g[0])):
            z=round(abs(float(((float(len(h[0])))-(float(len(g[0]))))/(float(len(h[0]))))),2)
        elif ((len(g[0]))>len(h[0])):
            z=round(abs(float(((float(len(g[0])))-(float(len(h[0]))))/(float(len(g[0]))))),2)
        self.feature_values_variables['understanding']=z'''


    def find_feature_value(self, item, file_name, dic):
        if item in dic[file_name]:
            return dic[file_name][item]
        else:
            return 0


    #in this function we want to extract features which are present in the first file and the feature in teh second file but not in teh first file
    def find_distinguisable_features(self, dic):
        feature_set={}#key is file name and value is key set
        for key_outer,value_outer in dic.iteritems():
            feature_set[key_outer]=dic[key_outer].keys()

        file_names=feature_set.keys()

        from_first_not_in_second=[]
        for f in feature_set[file_names[0]]:
                if not f in feature_set[file_names[1]]:
                    from_first_not_in_second.append(f)

        from_second_not_in_first=[]
        for f in feature_set[file_names[1]]:
                if not f in feature_set[file_names[0]]:
                    from_second_not_in_first.append(f)

        folder_name='\\'+file_names[0]+' , '+file_names[1]

        # new_path = self.output_path+folder_name
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        file=open(self.output_path+folder_name+'.txt', 'w')

        file.write('Features from '+file_names[0]+' which is not in '+ file_names[1]+ ' are: \n')
        for item in from_first_not_in_second:
            file.write(item+'\t')

        file.write('\n')
        file.write('Features from '+file_names[1]+' which is not in '+ file_names[0]+ ' are: \n')
        for item in from_second_not_in_first:
            file.write(item+'\t')










