class ElementSimilarity:
    def __init__(self):
        pass

    #this function find unique blocks and returns the len of unique blocks
    def find_unique_blocks(self, blocks_list):
        if len(blocks_list)==0:
            return 0

        unique_blocks=[]
        for block in blocks_list:
            new_list=self.exclude_from_blocks(block, blocks_list)#give a list of all blocks exculding the target block
            if self.is_unique(block, new_list):#if block does not have similarity with any other blocks
                unique_blocks.append(block)

        return len(unique_blocks)

    #this function is used to determine if a block is unique or not. The target block is compared against all other blocks so far
    # two aspects of blocks are importatnt for us. 1) its children and 2) its attributes. If we want to say two blocks are the sam
    def is_unique(self, block, element_list):
        for item in element_list:
            if self.is_similar(item, block):
                return False
        return True

    #for comparing if two elements are equal, we need to see if their children are similar or not.
    # Then we check if they have similar attributes.
    def is_similar(self, item, block):
        if not self.similar_children(item, block):#if they have different components, then they are not similar
            return False

        #if they have similar components, then we will check the attributes
        if self.attribs_are_equal(item.attrib, block.attrib):
            return True

        return False

    def find_children_types(self, item_children):
        dic={}#key is item type and value is its number of occurance
        for item in item_children:
             item_type=vars(item)['tag'].split("}")[1]
             if item_type in dic:
                 dic[item_type]=dic[item_type]+1
             else:
                 dic[item_type]=1

        return dic

    def similar_children(self, block, item):
        block_children=block._children
        item_children=item._children

        if len(block_children)==0 and len(item_children)==0:
            return True

        if len(block_children)==0 and len(item_children)!=0 or len(block_children)!=0 and len(item_children)==0:
            return False

        #when we arrive here, we have equal length of children
        for block_child in block_children:
            block_child_type=vars(block_child)['tag'].split("}")[1]
            for item_child in item_children:
                item_child_type=vars(item_child)['tag'].split("}")[1]
                if block_child_type==item_child_type:
                    if not self.equal_in_depth(block_child, item_child):#we want to see if two elements of same type are equal
                        return False
        return True


    def equal_in_depth(self, block_child, item_child):
        if not self.attribs_are_equal(block_child.attrib, item_child.attrib):
            return False

        if len(block_child._children)!=len(item_child._children):
            return False

        if self.similar_children(block_child, item_child):
            return True
        else:
            return False

    def attribs_are_equal(self, dic1, dic2):
        if len(dic1)!=len(dic2):
            return False
        for key,value in dic1.iteritems():
            if not key in dic2:
                return False

        return True

    def exclude_from_blocks(self, b, blocks):
        excluded_list=[]

        for item in blocks:
            if item!=b:
               excluded_list.append(item)

        return excluded_list









