
from ElementSimilarity import *
class ExtractFeatures:

    def __init__(self):
        self.extracted_features={}
        self.block_types=set()#defined as set to remove duplicates
        self.method_names=set()
        self.es=ElementSimilarity()
        self.blocks=[]
        # print 'Extract Features constructor class'

    def extract(self, root):

        for child in root._children:
            element_type=vars(child)['tag'].split("}")[1]
            if element_type=='block':#check if element is a block and it is not information.
                self.blocks.append(child)
                
        # self.extracted_features['num_blocks']=len(self.blocks)
        self.extracted_features['num_blocks']=0
        self.extracted_features['num_unique_blocks']=self.es.find_unique_blocks(self.blocks)

        for block in self.blocks:
            self.extract_block_features(block)
            #self.extracted_features['variable_name'] = self.extracted_features['field_text']


    def find_block_type(self, block):
        return block.__getattribute__('attrib')['type']

    def extract_block_features(self, element):
        element_type=vars(element)['tag'].split("}")[1]

        if element_type=='block':
            block_type=self.find_block_type(element)
            if block_type=='text':
                self.update_feature(self.find_block_type(element)+' block')#we save block types
            else:
                self.update_feature(block_type)#we save block types

            self.extracted_features['num_blocks']=self.extracted_features['num_blocks']+1

        if element_type=='mutation' and 'component_type' in element.attrib:
            self.update_feature(element.attrib['component_type'])
            if element.attrib['component_type']=='Player' and 'instance_name' in element.attrib:
                if 'instance_name' in self.extracted_features:
                    self.extracted_features['instance_name'].add(element.attrib['instance_name'])
                else:
                    instance_name_set=set()
                    instance_name_set.add(element.attrib['instance_name'])
                    self.extracted_features['instance_name']=instance_name_set

            if element.attrib['component_type']=='Clock':
                self.update_feature('Clock')

        if element_type=='mutation' and 'elseif' in element.attrib:
            self.update_feature('elseif')

        if element_type=='mutation' and 'event_name' in element.attrib:
            self.update_feature('when block')

        if element_type=='mutation' and 'method_name' in element.attrib:
            if 'method_name' in self.extracted_features:
                self.method_names.add(element.attrib['method_name'])
                self.extracted_features['method_name']=self.method_names
            else:
                self.method_names.add(element.attrib['method_name'])
                self.extracted_features['method_names']=self.method_names

        if element_type=='mutation' and 'name' in element.attrib:
            self.add_set_to_features(element, 'mutation_name', element.attrib['name'])

        if element_type=='statement':
            self.update_feature('statement')

        if element_type=='statement' and element.attrib['name']:
            self.add_set_to_features(element, 'statement_name', element.attrib['name'])

        if element_type=='field':
            if 'name' in element.attrib:
                if  element.attrib['name']=='TEXT':
                    self.update_feature('Text field')#we save block types
                else:
                    self.update_feature(element.attrib['name']+ ' field')#we save block types

            if 'field_text' in self.extracted_features:
                if element.text!='None':
                    names=set()
                    names=self.extracted_features['field_text']
                    value=element.text
                    names.add(value)
                    self.extracted_features['field_text']=set(names)
            else:
                    names=set()
                    names.add(element.text)
                    self.extracted_features['field_text']=names

        if len(element._children)==0:
            return

        for child in element._children:
            self.extract_block_features(child)


    def update_feature(self, block_type):
        if block_type in self.extracted_features:
            self.extracted_features[block_type]=self.extracted_features[block_type]+1
        else:
            self.extracted_features[block_type]=1

    def add_set_to_features(self, element, key_name, set_member):
        if key_name in self.extracted_features:
                if element.attrib['name'].strip()!='None' and element.attrib['name'].strip()!='':
                    names=set()
                    names=self.extracted_features[key_name]
                    value=element.attrib['name']
                    names.add(value)
                    self.extracted_features[key_name]=names
        else:
                names=set()
                names.add(element.attrib['name'])
                self.extracted_features[key_name]=names





