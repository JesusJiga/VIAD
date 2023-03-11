import socket

path_streamlit = "Web/src/"
path_localhost = ""

def get_path():

    if socket.gethostbyname(socket.gethostname()) == "172.27.0.2" or socket.gethostbyname(socket.gethostname()) == "172.19.0.2":
        path = path_localhost
    else:
        path = path_streamlit
    
    return path