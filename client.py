from multiprocessing import Value
from threading import Timer
from utils import States
import multiprocessing
import random
import socket
import time
import utils

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MSS = 12 # maximum segment size

sock = socket.socket(socket.AF_INET,    # Internet
                     socket.SOCK_DGRAM) # UDP

def send_udp(message):
  sock.sendto(message, (UDP_IP, UDP_PORT))

class Client:
  def __init__(self):
    self.client_state = States.CLOSED
    self.handshake()

  def handshake(self):
    if self.client_state == States.CLOSED:
      seq_num = utils.rand_int()
      syn_header = utils.Header(seq_num, 0, syn = 1, ack = 0)
      # for this case we send only header;
      # if you need to send data you will need to append it
      send_udp(syn_header.bits())
      self.update_state(States.SYN_SENT)
    else:
      pass

  def terminate(self):
    pass

  def update_state(self, new_state):
    if utils.DEBUG:
      print(self.client_state, '->', new_state)
    self.client_state = new_state

  def send_reliable_message(self, message):
    # send messages
    # we loop/wait until we receive all ack.
    pass

  # these two methods/function can be used receive messages from
  # server. the reason we need such mechanism is `recv` blocking
  # and we may never recieve a package from a server for multiple
  # reasons.
  # 1. our message is not delivered so server cannot send an ack.
  # 2. server responded with ack but it's not delivered due to
  # a network failure.
  # these functions provide a mechanism to receive messages for
  # 1 second, then the client can decide what to do, like retransmit
  # if not all packets are acked.
  # you are free to implement any mechanism you feel comfortable
  # especially, if you have a better idea ;)
  def receive_acks_sub_process(self, lst_rec_ack_shared):
    while True:
      recv_data, addr = sock.recvfrom(1024)
      header = utils.bits_to_header(recv_data)
      if header.ack_num > lst_rec_ack_shared.value:
        lst_rec_ack_shared.value = header.ack_num
  def receive_acks(self):
    # Start receive_acks_sub_process as a process
    lst_rec_ack_shared = Value('i', self.last_received_ack)
    p = multiprocessing.Process(target=self.receive_acks_sub_process, args=(lst_rec_ack_shared,))
    p.start()
    # Wait for 1 seconds or until process finishes
    p.join(1)
    # If process is still active, we kill it
    if p.is_alive():
      p.terminate()
      p.join()
    # here you can update your client's instance variables.
    self.last_received_ack = lst_rec_ack_shared.value

# we create a client, which establishes a connection
client = Client()
# we send a message
client.send_reliable_message("This message is to be received in pieces")
# we terminate the connection
client.terminate()
