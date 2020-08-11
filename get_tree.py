"""
Reads the file_name file and splits into rows of data
the class finds all the attributes in the file and their values
"""

import ID3

file_name = "traffic.txt"

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
receive a list of lines of data as one string and return list of list of
 strings of each line
'''
def get_values(lines):
    values = []
    for line in lines:
        # split one line to list of values
        values_one_row = line.split('\t')
        values_one_row[-1] = values_one_row[-1][:-1]
        values.append(values_one_row)
    return values


'''
write all the conclusions to a file
'''
def write_to_file(root, acc_id3, acc_knn, acc_nb):
    f = open("output.txt", "w")
    ID3.write_node(f, root, True, 0)
    f.write("\n")
    f.write(str("%.2f" % acc_id3) + "\t" + str("%.2f" % acc_knn) + "\t" + str("%.2f" % acc_nb))
    f.close()

'''
create the train data and the test data
 returns the ID3 tree
'''
def read_files():
    train_file_name = file_name
    lines_train = []
    # read the data from the file
    with open(train_file_name, 'r') as file:
        for line in file:
            lines_train.append(line)

    # gets the attributes names
    attributes = lines_train[0].split('\t')[:-1]
    dict_att_by_index = get_dict_att_by_index(attributes)
    training_values = get_values(lines_train[1:])
    # test_values = get_values(lines_test[1:])
    # gets the tree from the ID3 to get the classifications
    tree = ID3.run_ID3(training_values, attributes, dict_att_by_index)
    #ID3.write_to_file(tree)
    return tree, dict_att_by_index


if __name__ == "__main__":
    read_files()
