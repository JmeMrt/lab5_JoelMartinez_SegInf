import socket
import sys
import pyDes

class receptor:
    def contacto_B(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the port
        server_address = ('localhost', 1000)
        print('*** starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)
        
        # Listen for incoming connections
        sock.listen(1)
        
        while True:
            # Wait for a connection
            print('*** waiting for a connection')
            connection, client_address = sock.accept()
            try:
                print('*** connection from', client_address)
        
                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    textA='received {!r}'.format(data)
                    texB='{!r}'.format(data)
                    print('*** '+textA)
                    if data:
                        print('*** sending data back to the client')
                        connection.sendall(data)
                        return texB
                    else:
                        print('*** no data from', client_address,)
                        break
        
            finally:
                # Clean up the connection
                connection.close()
    
    def respuesta_A(self,tex):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 10000)
        print('>>> connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)
        
        try:
            # Send data
            a=tex
            message=bytes(a, "ascii")
            #message = b'sd'
            print('>>> sending {!r}'.format(message))
            sock.sendall(message)
        
            # Look for the response
            amount_received = 0
            amount_expected = len(message)
        
            while amount_received < amount_expected:
                data = sock.recv(16)
                amount_received += len(data)
                print('>>> received {!r}'.format(data))
        
        finally:
            print('>>> closing socket')
            sock.close()

class alice:
    def __init__(self,g,p,a):
        self.g=g
        self.p=p
        self.a=a

    def A(self):
        A=(self.g**self.a)%self.p
        return A

    def k(self,B):
        k=(B**self.a)%self.p
        return k



a=70
g=50
p=73

#B=55
uno=alice(g,p,a)
A=uno.A()
#k=uno.k(B)
print('A='+str(A))
#print('k='+str(k))

bhu=str(g)+','+str(p)+','+str(A)+',(g;p;A)'
print(bhu)

dos=receptor()
dos.respuesta_A(bhu)

dat=dos.contacto_B()[2:-1]
B=int(dat)
print('_______________________________________________')
print("B'="+str(B))

k=uno.k(B)
print('k='+str(k))

txt=open("mensajeseguro.txt", "rb")
xet=txt.read()

k = pyDes.des(b"DESCRYPT", pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
print()
print('Encriptacion DES')
print()
des=str(k.decrypt(xet))[2:-1]
print ("Descifrado: %r" % des)

abb=open("mensaje_seguro.txt", "rb")
abc=abb.read()
clabe = b'unodostrescuatrosincosei'
k = pyDes.triple_des(clabe, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
ddd= k.decrypt(abc)
print()
print('Encriptacion 3DES')
print()
print(ddd)

