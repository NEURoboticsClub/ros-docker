#!/usr/bin/env python2
import rospy
import socket
import json
from std_msgs.msg import String


# global variable
client_socket = None
data_buffer = {} # ROStopic: data
TOPIC = "cpu_topic"

# Callback function when publisher publishe something on this topic
def callback(data):
    global client_socket
    # 1. This function gets called every time a message is published on the 'test_topic' topic
    # rospy.loginfo("CPU_SUB: %s", data.data)

    # 2. save lastest data on this topic
    data_buffer[TOPIC] = data.data



if __name__ == "__main__":
    print("Server Node is running...")

    # 1. init node
    rospy.init_node('cpusub_node')
    rospy.Subscriber(TOPIC, String, callback)

    # 2. init server socket to listen to client request
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostname()
    PORT = 9999
    SERVER_SOCKET.bind((HOST, PORT))
    SERVER_SOCKET.listen(5)

    
    while not rospy.is_shutdown():
        # 3. connect with new client (MC)
        client_socket, addr = SERVER_SOCKET.accept()
        print("Got a connection from {}, curr_host={}".format(str(addr), HOST))

        # 4.keep sending messages from CPU to MC
        while True:  
            # convert dict to json string
            json_data = json.dumps({"data": data_buffer[TOPIC]}) +"\n"
            print("sending-->", json_data)
            client_socket.send(json_data)
            
    # Close the connection
    client_socket.close()
