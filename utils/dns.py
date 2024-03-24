from dnslib.server import BaseResolver
from dnslib import DNSRecord, RR, A
import socket

class SimpleResolver(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        qname = request.q.qname
        qtype = request.q.qtype
        if qname.matchGlob("ECOONE.com.") and qtype == QTYPE.A:
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(socket.gethostbyname(socket.gethostname()))))
        return reply

if __name__ == "__main__":
    resolver = SimpleResolver()
    # Configurar el servidor DNS para UDP
  
    # Configurar el servidor DNS para TCP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((socket.gethostbyname(socket.gethostname()), 12345))
    tcp_socket.listen(5)
    print(socket.gethostname())


    print("DNS Server listening on port 12345...")

    try:
        while True:
            # Manejar solicitudes UDP

            tcp_conn, tcp_addr = tcp_socket.accept()
            tcp_data = tcp_conn.recv(1024)
            print(tcp_data)
            dns_request = DNSRecord.parse(tcp_data)
            dns_response = resolver.resolve(dns_request, None)
            tcp_conn.sendall(dns_response.pack())
            tcp_conn.close()

    except KeyboardInterrupt:
        pass
    finally:
        tcp_socket.close()
