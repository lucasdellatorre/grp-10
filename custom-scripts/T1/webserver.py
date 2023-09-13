from http.server import BaseHTTPRequestHandler,HTTPServer
from time import sleep
import sys
import os

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8000


class GetCpuLoad(object):
    '''
    classdocs
    '''

    def __init__(self, percentage=True, sleeptime = 1):
        '''
        @parent class: GetCpuLoad
        @date: 04.12.2014
        @author: plagtag
        @info: 
        @param:
        @return: CPU load in percentage
        '''
        self.percentage = percentage
        self.cpustat = '/proc/stat'
        self.sep = ' ' 
        self.sleeptime = sleeptime

    def getcputime(self):
        '''
        http://stackoverflow.com/questions/23367857/accurate-calculation-of-cpu-usage-given-in-percentage-in-linux
        read in cpu information from file
        The meanings of the columns are as follows, from left to right:
            0cpuid: number of cpu
            1user: normal processes executing in user mode
            2nice: niced processes executing in user mode
            3system: processes executing in kernel mode
            4idle: twiddling thumbs
            5iowait: waiting for I/O to complete
            6irq: servicing interrupts
            7softirq: servicing softirqs

        #the formulas from htop 
             user    nice   system  idle      iowait irq   softirq  steal  guest  guest_nice
        cpu  74608   2520   24433   1117073   6176   4054  0        0      0      0


        Idle=idle+iowait
        NonIdle=user+nice+system+irq+softirq+steal
        Total=Idle+NonIdle # first line of file for all cpus

        CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)
        '''
        cpu_infos = {} #collect here the information
        with open(self.cpustat,'r') as f_stat:
            lines = [line.split(self.sep) for content in f_stat.readlines() for line in content.split('\n') if line.startswith('cpu')]

            #compute for every cpu
            for cpu_line in lines:
                if '' in cpu_line: cpu_line.remove('')#remove empty elements
                cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]#type casting
                cpu_id,user,nice,system,idle,iowait,irq,softrig,steal,guest,guest_nice = cpu_line

                Idle=idle+iowait
                NonIdle=user+nice+system+irq+softrig+steal

                Total=Idle+NonIdle
                #update dictionionary
                cpu_infos.update({cpu_id:{'total':Total,'idle':Idle}})
            return cpu_infos

    def getcpuload(self):
        '''
        CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)

        '''
        start = self.getcputime()
        #wait a second
        sleep(self.sleeptime)
        stop = self.getcputime()

        cpu_load = {}

        for cpu in start:
            Total = stop[cpu]['total']
            PrevTotal = start[cpu]['total']

            Idle = stop[cpu]['idle']
            PrevIdle = start[cpu]['idle']
            CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)*100
            cpu_load.update({cpu: CPU_Percentage})
        return cpu_load

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""

        datahora = os.popen('date').read()
        uptime = os.popen('cat /proc/uptime').read()
        cpu_name = os.popen('grep "model name" /proc/cpuinfo').read()
        cpu_vel = os.popen('grep "cpu MHz" /proc/cpuinfo').read()
        cpu_capacity =  GetCpuLoad().getcpuload()
        ram = os.popen('grep -E "MemTotal|MemAvailable" /proc/meminfo').read()
        sys_version = os.popen('cat /proc/version').read()
        proc_list = os.popen("ps aux | awk '{print $1, $3}' | tail -n +2'").read().split("\n")


        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(f"<p>Data e Hora: {datahora}</p>".encode())
        s.wfile.write(f"<p>Uptime: {uptime}</p>".encode())
        s.wfile.write(f"<p>Modelo do processador e velocidade: {cpu_name} {cpu_vel} MHz</p>".encode())
        s.wfile.write(f"<p>Capacidade ocupada do processador: </p>".encode())
        for cpu in cpu_capacity:
            usage = cpu_capacity[cpu]
            s.wfile.write(f"<p> {cpu}: {usage} </p>".encode())
        s.wfile.write(f"<p>Quantidade de memória RAM total e usada : {ram}</p>".encode())
        s.wfile.write(f"<p>Versao do sistema: {sys_version}</p>".encode())
        s.wfile.write(f"<p>Lista de processos em execução (pid e comando): </p>".encode())
        for line in proc_list:
            s.wfile.write(f"<p> {line} </p>".encode())
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("</body></html>".encode())

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    # print("Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    httpd.serve_forever()
