from http.server import BaseHTTPRequestHandler,HTTPServer
import os

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8000


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
        proc_capacity = os.popen('awk "/^cpu / {idle=$5; total=0; for (i=2; i<=NF; i++) total+=$i} END {print 100 - (idle / total * 100)}" /proc/stat')
        ram = os.popen('grep -E "MemTotal|MemAvailable" /proc/meminfo').read()
        sys_version = os.popen('cat /proc/version').read()
        proc_list = os.popen("ps aux | awk '{print $2, $11}'").read()


        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(f"<p>Data e Hora: {datahora}</p>".encode())
        s.wfile.write(f"<p>Uptime: {uptime}</p>".encode())
        s.wfile.write(f"<p>Modelo do processador e velocidade: {cpu_name} {cpu_vel} MHz</p>".encode())
        s.wfile.write(f"<p>Capacidade ocupada do processador: {proc_capacity}</p>".encode())
        s.wfile.write(f"<p>Quantidade de memória RAM total e usada : {ram}</p>".encode())
        s.wfile.write(f"<p>Versao do sistema: {sys_version}</p>".encode())
        s.wfile.write(f"<p>Lista de processos em execução (pid e nome): {proc_list}</p>".encode())
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("</body></html>".encode())

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    # print("Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    httpd.serve_forever()
