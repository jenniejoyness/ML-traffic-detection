"""
Calculate the prediction of a given test line.
Build a tree based on the train data and when
receiving a test line, follow the tree to get
the prediction.
"""

import copy
import operator
import math
import Edge
import Node

'''
returns the entropy of the data
'''


def get_entropy(list_of_rows):
    pos = 0
    neg = 0
    # sum all the "yes" and the "no" in the data - the pos and the neg
    for row in list_of_rows:
        if row[-1] == "crowded":
            pos += 1
        else:
            neg += 1
    x = pos / (pos + neg)
    y = neg / (pos + neg)
    # if all the classifications are the same the entropy is 0
    if x == 0 or y == 0:
        entropy = 0
    # calculate the entropy
    else:
        entropy = (-x) * math.log(x, 2) - y * math.log(y, 2)
    return entropy


'''
 returns a dictionary of attributes and their index in the line
'''


def get_dict_att_by_index(attributes):
    dict_att_by_index = {}
    i = 0
    # go over all the attributes
    for att in attributes:
        dict_att_by_index[att] = i
        i += 1
    return dict_att_by_index


'''
return dict_of_att which is a dictionary of attributes and their possible values
'''


def get_dict_of_att(attributes, dict_att_by_index, training_values):
    dict_of_att = {}
    # go over all the attributes
    for att in attributes:
        # initial their values list with empty list
        dict_of_att[att] = []
        # go over the lines and check for a value - if already saw that
        for line in training_values:
            value = line[dict_att_by_index[att]]
            # add value to the list of an attribute
            if value not in dict_of_att[att]:
                dict_of_att[att].append(value)
            dict_of_att[att].sort()
    return dict_of_att


'''
 return dict_of_values which is a dictionary of values of an attribute
 and a list of the lines that includes that value
'''


def get_dict_of_values(training_values, dict_of_att, att, index):
    dict_for_att = {}
    # go over all the values of an attribute
    for value in dict_of_att[att]:
        dict_for_att[value] = []
        # go over the all the lines and add to the list lines that include the value
        for line in training_values:
            if line[index] == value:
                dict_for_att[value].append(line)
    return dict_for_att


'''
return dict_of_dict which is a dictionary of all the attributes, while the value is dictionary
of value and the lines that include this value
'''


def get_dict_of_dict(attributes, dict_att_by_index, training_values):
    dict_of_att = get_dict_of_att(attributes, dict_att_by_index, training_values)
    dict_of_dict = {}
    for att in attributes:
        dict_of_dict[att] = get_dict_of_values(training_values, dict_of_att, att, dict_att_by_index[att])
    return dict_of_dict


'''
return the average information entropy of an attribute
'''


def get_avg_info_entropy(dict_of_dict, att):
    avg_info_entropy = 0
    # rows_len_of_att is the length of the list of lines of current data table
    rows_len_of_att = 0
    # go over all the values of an attribute
    for value_of_att in dict_of_dict[att]:
        # list_of_one_value is a list of lines that includes the value_of_att
        list_of_one_value = dict_of_dict[att][value_of_att]
        rows_len_of_att += len(list_of_one_value)
        avg_info_entropy += (len(list_of_one_value) * get_entropy(list_of_one_value))
    avg_info_entropy = avg_info_entropy * (1 / rows_len_of_att)
    return avg_info_entropy


'''
 check the majority of the classification
'''


def majority_classification(lines):
    yes, no = 0, 0
    # go over all the lines
    for line in lines:
        if line[-1] == "crowded":
            yes += 1
        else:
            no += 1
    if yes >= no:
        return "crowded"
    else:
        return "not-crowded"


'''
check if all the data classification is the same
'''


def check_all_same(lines):
    yes, no = 0, 0
    # go over all the lines
    for line in lines:
        if line[-1] == "crowded":
            yes += 1
        else:
            no += 1
    # if there is no "yes" - return "no"
    if yes == 0:
        return "not-crowded"
    # if there is no "no" - return "yes"
    elif no == 0:
        return "crowded"
    # and else return "not same"
    else:
        return "not same"


'''
 returns the Edge of a value
'''


def get_edge(values, value):
    # go over all the values of an attribute
    for edge in values:
        if edge.value_name == value:
            return edge


'''
 returns the prediction of a test line according to the tree received by DTL in a recursive function
'''


def get_prediction(tree, test_line, dict_att_by_index):
    # if got to a leaf - return its classification
    if tree.values is None:
        return tree.att_name
    # get the next node of the tree according to the values of the test line
    next_node = get_edge(tree.values, test_line[dict_att_by_index[tree.att_name]]).next
    return get_prediction(next_node, test_line, dict_att_by_index)


'''
write all the nodes of the tree to a file in a recursive function
'''


def write_node(file, node, is_root, tab_num):
    # if the node is a leaf - write its classification
    if node.values is None:
        file.write(":" + node.att_name + "\n")
        return
    elif not is_root:
        file.write("\n")
        tab_num += 1
    for value in node.values:
        if not is_root:
            file.write(tab_num * "\t" + "|")
        file.write(node.att_name + "=" + value.value_name)
        write_node(file, value.next, False, tab_num)


'''
write to file the tree of the data
'''


def write_to_file(root):
    f = open("tree.txt", "w")
    write_node(f, root, True, 0)
    f.close()


'''
return the attribute with the highest gain
'''


def choose_att_by_max_gain(gain_dict):
    return max(gain_dict.items(), key=operator.itemgetter(1))[0]


'''
 the function calculate the entropy of all the attributes and their gain
  and returns the attribute with the highest gain
'''


def ID3(lines, attributes, dict_att_by_index):
    # calculate the entropy of all the lines - S_entropy
    s_entropy = get_entropy(lines)
    dict_of_dict = get_dict_of_dict(attributes, dict_att_by_index, lines)
    gain_dict = {}
    for att in attributes:
        gain_dict[att] = s_entropy - get_avg_info_entropy(dict_of_dict, att)
    return choose_att_by_max_gain(gain_dict)


'''
the function build the tree
'''


def DTL(data_lines, attributes, dict_att_by_index, dict_of_att, default_classification="crowded"):
    # if there is no data - return a node with default classification
    if not data_lines:
        return Node.Node(default_classification)
    # check if all the classifications remain are the same
    same = check_all_same(data_lines)
    # if they are the same return a node with this classification
    if same != "not same":
        return Node.Node(same)
    # if there are no more attributes return a node with the majority classification of the remaining data
    if not attributes:
        return Node.Node(majority_classification(data_lines))
    # call ID3 to get the best attribute - by calculating the gain of each attribute
    best_att = ID3(data_lines, attributes, dict_att_by_index)
    values = []
    # create the edges of the node - best attribute
    for value in dict_of_att[best_att]:
        values.append(Edge.Edge(value))
    # create the root
    tree = Node.Node(best_att, values)
    dict_of_dict = get_dict_of_dict(attributes, dict_att_by_index, data_lines)
    # create deep copy of the attributes list
    temp_attributes = copy.deepcopy(attributes)
    temp_attributes.remove(best_att)
    # go over all the values of the best attribute
    for value in dict_of_att[best_att]:
        # if the value does not exist in the data create a leaf node
        if value not in dict_of_dict[best_att]:
            edge = get_edge(values, value)
            edge.next = Node.Node(majority_classification(data_lines))
            continue
        data_lines_value = dict_of_dict[best_att][value]
        # call the DTL again to get the sub tree
        sub_tree = DTL(data_lines_value, temp_attributes, dict_att_by_index, dict_of_att,
                       majority_classification(data_lines))
        edge = get_edge(values, value)
        edge.next = sub_tree
    return tree


'''
the function run the decision tree class - ID3
'''


def run_ID3(training_values, attributes, dict_att_by_index):
    dict_of_att = get_dict_of_att(attributes, dict_att_by_index, training_values)
    # call the DTL function to receive the tree
    tree = DTL(training_values, attributes, dict_att_by_index, dict_of_att)
    # write_to_file(tree)
    return tree
