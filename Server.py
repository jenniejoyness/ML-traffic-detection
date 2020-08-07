import socket
import get_tree
import ID3

tree = None
dict_att_by_index = None
file_name = "traffic.txt"


def send_to_client(message, c_socket):
    c_socket.send(message.encode("utf-8"))


def add_data(data, c_socket):
    #print(b'data:' +data)

    file = open(file_name, 'a+')
    data = data.split("\r\n")
    file.write(data[0] + '\n')



# get prediction
def is_busy(data, c_socket):

    tree, dict_att_by_index = get_tree.read_files()
    data = data.split("\r\n")[0].split("\t")
    ans = ID3.get_prediction(tree, data, dict_att_by_index) + "\r\n"
    send_to_client(ans, c_socket)


def illegal_request(data, client_addr):
    return 'blah'


switcher = {
    "1": add_data,
    "2": is_busy
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


def handle_client(c_socket):
    # continue handling client requests until they want to stop
    data = c_socket.recv(BUFFER_SIZE)
    if not data:
        c_socket.close()
        return
    #print(data)
    request_handler(data, c_socket)
    #print("handled request")
    c_socket.close()


if __name__ == "__main__":

    tree, dict_att_by_index = get_tree.read_files()

    TCP_IP = '0.0.0.0'
    TCP_PORT = 3001
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(10)
    # handling client requests
    while True:
        print("Server waiting...")
        c_socket, addr = s.accept()
        handle_client(c_socket)

