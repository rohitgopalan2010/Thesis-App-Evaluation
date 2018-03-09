from ExtractFeatures import *
from MeaningFullName import *


class EvaluateNaming:
    def __init__(self):
        pass

    def evaluate(self, extracted_features):
         return self.evelauting_namings(extracted_features)

    def evelauting_namings(self, extracted_features):

        degree_of_meaningfulness=0.0
        mn=MeaningFullName()
        naming=self.find_namings(extracted_features)
        degree_of_meaningfulness=mn.how_meaningfull(naming)

        return degree_of_meaningfulness

    def find_namings(self, extracted_features):
        naming=set()

        for key,value in extracted_features.iteritems():
            if 'name' in key or 'text' in key:
                if type(extracted_features[key]) is set:
                    for item in extracted_features[key]:
                        naming.add(item)

        return naming

