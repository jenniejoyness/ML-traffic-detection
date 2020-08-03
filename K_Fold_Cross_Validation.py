import ID3
import KNN
import Naive_Bayes


def cross_validation(training_values, k):
    # divide_data = [training_values[i:i + k] for i in range(0, len(training_values), k)]
    #
    # for i in range(k):
    #     divide_data[i] = []
    # for line in training_values:
    #     [lst[i:i + n] for i in range(0, len(lst), n)]
    divide_data = [training_values[i::k] for i in range(k)]
    return divide_data


# receive a list of lines of data as one string and return list of list of
# strings of each line
def get_values(lines):
    values = []
    for line in lines[1:]:
        # split one line to list of values
        values_one_row = line.split('\t')
        values_one_row[-1] = values_one_row[-1][:-1]
        values.append(values_one_row)
    return values


def get_dict_att_by_index(attributes):
    dict_att_by_index = {}
    i = 0
    for att in attributes:
        dict_att_by_index[att] = i
        i += 1
    return dict_att_by_index


def write_accuracy(avg_acc_id3, avg_acc_knn, avg_acc_nb):
    f = open("accuracy.txt", "w")
    f.write(str("%.2f" % avg_acc_id3) + "\t" + str("%.2f" % avg_acc_knn) + "\t" + str("%.2f" % avg_acc_nb))
    f.close()


def get_test_and_training(divide_data, index):
    test = divide_data[index]
    train = []
    for i in range(len(divide_data)):
        if i != index:
            train.extend(divide_data[i])
    return test, train


def read_file():
    lines = []
    file_name = "dataset.txt"
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line)
    attributes = lines[0].split('\t')[:-1]
    dict_att_by_index = get_dict_att_by_index(attributes)
    training_values = get_values(lines)
    tree = ID3.run_ID3(training_values, attributes, dict_att_by_index)

    k = 5
    divide_data = cross_validation(training_values, k)
    avg_acc_id3, avg_acc_knn, avg_acc_nb = 0, 0, 0
    for i in range(k):
        acc_id3, acc_knn, acc_nb = 0, 0, 0
        test, train = get_test_and_training(divide_data, i)
        tree = ID3.run_ID3(train, attributes, dict_att_by_index)
        for test_line in test:
            if ID3.get_prediction(tree, test_line[:-1], dict_att_by_index) == test_line[-1]:
                acc_id3 += 1
            if KNN.run_KNN(test_line[:-1], train) == test_line[-1]:
                acc_knn += 1
            if Naive_Bayes.run_NB(test_line[:-1], train, attributes) == test_line[-1]:
                acc_nb += 1
        avg_acc_id3 += (acc_id3 / len(test))
        avg_acc_knn += (acc_knn / len(test))
        avg_acc_nb += (acc_nb / len(test))
        print("ID3: " + str(acc_id3 / len(test)) + " | KNN: " + str(acc_knn / len(test)) + " | NB: " + str(acc_nb / len(test)))
    print("ID3: " + str(avg_acc_id3 / k) + " | KNN: " + str(avg_acc_knn / k) + " | NB: " + str(avg_acc_nb / k))
    write_accuracy((avg_acc_id3 / k), (avg_acc_knn / k), (avg_acc_nb / k))


if __name__ == "__main__":
    read_file()
