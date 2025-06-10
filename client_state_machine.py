"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
import subprocess
import random

class ClientSM():
    def __init__(self, s):
        # super().__init__()
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        # isa
        self.game = None

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself. Please try again\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n'
                        self.out_msg += "Enter \"intogame\" for the game at any time!\n"
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n'
                    self.out_msg += "Enter \"intogame\" for the game at any time!\n"
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
                if my_msg == 'intogame':
                    self.out_msg += '\nwait a min for game\n'
                    subprocess.Popen(["python", "color.py"])
                self.out_msg += "\n"+my_msg+"\n"

            if len(peer_msg) > 0:    
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "\n(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                else:
                    if peer_msg == "intogame":
                        self.out_msg +="The other user is in the game.\n How about starting your game as well?"
                    self.out_msg += "\n"+peer_msg["from"] + peer_msg["message"]+"\n"
                
        # isa added this part
        # elif self.state == S_GAME:
        #     if self.game:
        #         game_result = self.game.proc(my_msg)
        #         self.out_msg += game_result

        #         if self.game.is_game_over():
        #             self.state = S_LOGGEDIN
        #             self.game = None
        #             self.out_msg += "\nGame over. Score: " + self.game.get_score() + "\n"

        #     else:
        #         self.out_msg += "Need to start game!\n"
        #         self.state = S_LOGGEDIN

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
