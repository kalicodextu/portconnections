# -*- coding: utf-8 -*-
import pexpect

class NginxStatus(object):

    def __init__(self, port):
        self.port = str(port)
        self.status = None
        self.nginx_status = dict()
        self.netstatInfo = list()
        self.established = 0
        self.syn_send = 0
        self.syn_recv = 0
        self.fin_wait1 = 0
        self.fin_wait2 = 0
        self.time_wait = 0
        self.close = 0
        self.close_wait = 0
        self.last_ack = 0
        self.listen = 0
        self.closing = 0
        self.unknown = 0

    def getAllStatus(self):
        shell_cmd = 'netstat -atn | grep -P ":' + self.port + ' "' 
        child = pexpect.spawn('/bin/bash', ['-c', shell_cmd])
        while True:
            index = child.expect(['tcp', pexpect.EOF])
            if index == 0:
                if child.before:
                    self.netstatInfo.append(child.before)
            else:
                if child.before:
                    self.netstatInfo.append(child.before)
                    
                break
        for statusinfo in self.netstatInfo:
            recv_q, send_q, local_addr, foreign_addr, state = statusinfo.split()[:5]
            if local_addr.split(':')[1] == self.port:
                if state == 'ESTABLISHED':
                    self.established += 1
                elif state == 'SYN_SENT':
                    self.syn_send += 1
                elif state == 'SYN_RECV':
                    self.syn_recv += 1
                elif state == 'FIN_WAIT1':
                    self.fin_wait1 += 1
                elif state == 'FIN_WAIT2':
                    self.fin_wait2 += 1
                elif state == 'TIME_WAIT':
                    self.time_wait += 1
                elif state == 'CLOSE':
                    self.close += 1
                elif state == 'CLOSE_WAIT':
                    self.close_wait += 1
                elif state == 'LAST_ACK':
                    self.last_ack += 1
                elif state == 'LISTEN':
                    self.listen += 1
                elif state == 'CLOSING':
                    self.closing += 1
                elif state == 'UNKNOW':
                    self.unknown += 1
                else:
                    pass
        self.nginx_status['ESTABLISHED'] = self.established
        self.nginx_status['SYN_SENT'] = self.syn_send
        self.nginx_status['SYN_RECV'] = self.syn_recv
        self.nginx_status['FIN_WAIT1'] = self.fin_wait1
        self.nginx_status['FIN_WAIT2'] = self.fin_wait2
        self.nginx_status['TIME_WAIT'] = self.time_wait
        self.nginx_status['CLOSE'] = self.close
        self.nginx_status['CLOSE_WAIT'] = self.close_wait
        self.nginx_status['LAST_ACK'] = self.last_ack
        self.nginx_status['LISTEN'] = self.listen
        self.nginx_status['CLOSING'] = self.closing
        self.nginx_status['UNKNOW'] = self.unknown
        

if __name__ == '__main__':
    Search = NginxStatus(5858)
    Search.getAllStatus()
    print Search.nginx_status
