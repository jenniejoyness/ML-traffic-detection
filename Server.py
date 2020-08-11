import socket
import get_tree
import ID3

tree = None
dict_att_by_index = None
file_name = "traffic.txt"

'''
 send message to client with c_socket parameter
'''
def send_to_client(message, c_socket):
    c_socket.send(message.encode("utf-8"))


'''
adding new data to the training file 
'''
def add_data(data, c_socket):
    file = open(file_name, 'a+')
    data = data.split("\r\n")
    file.write(data[0] + '\n')




'''
 return the prediction to the client by calling the  get_prediction function in ID3 class
 before returning prediction updating the tree with all the new that has been added
'''
def return_prediction(data, c_socket):
    tree, dict_att_by_index = get_tree.read_files()
    # need to send data as list to get_prediction function
    data = data.split("\r\n")[0].split("\t")
    ans = ID3.get_prediction(tree, data, dict_att_by_index) + "\r\n"
    send_to_client(ans, c_socket)

'''
clients input was illegal
'''
def illegal_request(data, client_addr):
    print("Illegal request sent to server")


switcher = {
    "1": add_data,
    "2": return_prediction
}

'''
send to the correct handler.
if an illegal request is made (not 1 or 2) will ignore.
'''


def request_handler(client_request, c_socket):

    client_request = client_request.decode("utf-8")
    client_request = client_request.split(",")
    func = switcher.get(client_request[0], illegal_request)
    func(client_request[1], c_socket)


'''
 server reads request from socket and handles accordingly
 request with number 1 - is to add data to the tree
 request with number 2 - get prediction for new data
'''
def handle_client(c_socket):
    data = c_socket.recv(BUFFER_SIZE)
    if not data:
        c_socket.close()
        return
    request_handler(data, c_socket)
    c_socket.close()


'''
 the main function trains the ID3 tree model and
 opens server to handle clients requests
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

