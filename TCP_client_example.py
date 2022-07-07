import socket
import json
import sys
import struct

DEFAULT_PACKET_SIZE_INFOS = {
    "nbr_bytes": 2,
    "type": '@H',
}

def dict_to_packet(dict_obj, packet_size_infos=DEFAULT_PACKET_SIZE_INFOS):
    """
    Convert dict to packet
    :type dict_obj: dict
    :param packet_size_infos:
    :return: packet
    """
    json_obj = json.dumps(dict_obj)

    if sys.version_info[0] == 3:
        json_obj = json_obj.encode()
    packet = "" if sys.version_info[0] == 2 else b""
    packet += struct.pack(packet_size_infos["type"], len(json_obj))
    packet += json_obj
    return packet


HOST = '169.254.200.200' #change this to your own robot's IP
PORT = 40001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print ('Connexion vers ' + HOST + ':' + str(PORT) + ' reussie.')

message = {'param_list': ['AUTO'], 'command': 'CALIBRATE'} # example message, you can put your own. Note that the Ned will not calibrate if it is already calibrated
packet_msg = dict_to_packet(message)
n = client.send(packet_msg)

print ('Reception...')
donnees = client.recv(1024)
print ('Recu :', donnees)

message = {'param_list': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'command': 'MOVE_JOINTS'}
packet_msg = dict_to_packet(message)
n = client.send(packet_msg)

print ('Reception...')
donnees = client.recv(1024)
print ('Recu :', donnees)

print ('Deconnexion.')
client.close()




