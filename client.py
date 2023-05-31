import socket
import json

# CLIENT CODE
# Get local machine name (client)
SERVER_HOST = socket.gethostname()
SERVER_PORT = 9999
FORMAT = "utf-8"
MSG_SIZE = 1024

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connection to server on local machine
    s.connect((SERVER_HOST, SERVER_PORT))

    # init random id
    id = 456
    # create 5 request (single thread)
    for _ in range(5):

        # 1.Send data to server
        data_to_send = {"request_topic": "velocity", "id": id}
        s.send(json.dumps(data_to_send).encode(FORMAT))

        # 2. Receive from server
        msg = s.recv(MSG_SIZE)
        ros_data = json.loads(msg.decode(FORMAT))

        # 3. log the received data
        print(f"Received ROS data: {ros_data}, curr_host={SERVER_HOST}")
        id +=1

    # Close the socket
    s.close()

if __name__ == "__main__":
    main()