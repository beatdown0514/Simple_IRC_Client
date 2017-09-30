#!/usr/local/bin/python3.6

import socket
import yaml
import threading

class simple_irc_client():
    IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def _send_data(self, command):
        self.IRC.send((command + '\n').encode())
    
    def __init__(self, server='', port=6667, nickname='', username='', 
                 channel='', realname='', hostname=''):
        self.server = server
        self.port = port
        self.nickname = nickname
        self.username = username
        self.channel = channel
        self.realname = realname
        self.hostname = hostname
    
    def config_from_yaml(self, config):
        with open(config, 'r') as conf_file:
            conf = yaml.load(conf_file)
        self.server = conf['server']
        self.port = conf['port']
        self.nickname = conf['nickname']
        self.username = conf['username']
        self.channel = conf['channel']
        self.realname = conf['realname']
        self.hostname = conf['hostname']
    
    def _irc_conn(self):
        self.IRC.connect((self.server, self.port))
    
    def _join(self):
        self._send_data("JOIN %s" % self.channel)
    
    def notice(self, message):
        message = message.encode("iso2022_jp").decode()
        self._send_data("NOTICE %s :" % self.channel + message)
    
    def say(self, message):
        message = message.encode("iso2022_jp").decode()
        self._send_data("PRIVMSG %s :" % self.channel + message)
    
    def _login(self):
        self.send_data("USER %s %s %s %s" % (self.username, self.hostname, 
                                             self.server, self.realname))
        self.send_data("NICK " + self.nickname)
     
    def _wait_message(self):
        while True:
            buffer = self.IRC.recv(1024)
            try:
                msg = buffer.decode()
            except:
                pass
            split_msg = msg.split(':')
            if split_msg[0] == "PING ":
                self.send_data("PONG %s" % split_msg[1])
    
    def start(self):
        if not self.server or not self.nickname or not self.channel\
          or not self.realname or not self.hostname:
            print('error!!')
            print('invalid parameter(s). check server or nickname or channel or realname or hostname')
        else:
            thread = threading.Thread(target=self._wait_message)
            self._irc_conn()
            self._login()
            self._join()
            thread.start()
        
    def quit(self, message='byebye'):
        self._send_data("QUIT %s" % (message))


