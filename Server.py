"""
This class runs the server.
Server handles clients requests to add new information to ID3 tree or gets the prediction if the shuttle is crowded
or not.
"""

import socket
import get_tree
import ID3

tree = None
dict_att_by_index = None
file_name = "traffic.txt"

'''
Send message to client with c_socket parameter.
'''


def send_to_client(message, c_socket):
    c_socket.send(message.encode("utf-8"))


'''
Adding new data to the training file.
Then updating the tree with the new data.
'''


def add_data(data, c_socket):
    file = open(file_name, 'a+')
    data = data.split("\r\n")
    file.write(data[0] + '\n')
    # update tree
    global tree, dict_att_by_index
    tree, dict_att_by_index = get_tree.read_files()


'''
Return the prediction to the client by calling the get_prediction function in ID3 class.
'''


def return_prediction(data, c_socket):
    # need to send data as list to get_prediction function
    data = data.split("\r\n")[0].split("\t")
    ans = ID3.get_prediction(tree, data, dict_att_by_index) + "\r\n"
    send_to_client(ans, c_socket)


'''
Client's input was illegal.
'''


def illegal_request(data, client_addr):
    print("Illegal request sent to server")


switcher = {
    "1": add_data,
    "2": return_prediction
}

'''
Send to the correct function to handle the client's request.
Request with the number 1 - is to add data to the tree.
Request with the number 2 - is to get prediction for new data.
'''


def request_handler(client_request, c_socket):
    client_request = client_request.decode("utf-8")
    client_request = client_request.split(",")
    func = switcher.get(client_request[0], illegal_request)
    func(client_request[1], c_socket)


'''
Server reads data from socket and handles accordingly.
'''


def handle_client(c_socket):
    data = c_socket.recv(BUFFER_SIZE)
    if not data:
        c_socket.close()
        return
    request_handler(data, c_socket)
    c_socket.close()


'''
The main function trains the ID3 tree model and opens server to handle clients requests.
'''
if __name__ == "__main__":

    # get the tree that has been built with data in the training file
    tree, dict_att_by_index = get_tree.read_files()

    TCP_IP = '0.0.0.0'
    TCP_PORT = 3001
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(10)
    # handling client requests
    while True:
        print("Server waiting for new clients request...")
        c_socket, addr = s.accept()
        handle_client(c_socket)
