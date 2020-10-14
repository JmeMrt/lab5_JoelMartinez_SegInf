import socket
import sys
import pyDes

class emisor:
    def contacto_A(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the port
        server_address = ('localhost', 10000)
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
    
    def respuesta_B(self,tex):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 1000)
        print('>>> connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)
        
        try:
            # Send data
            a=tex
            message = bytes(a, "ascii")
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

class bob:
    def __init__(self,b):
        self.b=b
        self.g=None
        self.p=None
        self.A=None

    def datos(self,s):
        self.g=s[0]
        self.p=s[1]
        self.A=s[2]

    def B(self):
        B=(self.g**self.b)%self.p
        return(B)

    def k(self):
        k=(self.A**self.b)%self.p
        return k

uno=emisor()
dat=uno.contacto_A()[2:-9]
dat=dat.split(",")

b=20
s=[int(dat[0]),int(dat[1]),int(dat[2])]

dos=bob(b)
dos.datos(s)
B=dos.B()
k=dos.k()
print('B='+str(B))
print('k='+str(k))

B2=str(B)
uno.respuesta_B(B2)

tt=open('mensajedeentrada.txt','r')
tex=tt.read()
print('_______________________________________________')
print()
print('texto original>>> '+tex)
print()

print('Encriptacion DES')
print()

data = bytes(tex, "ascii")

k = pyDes.des(b"DESCRYPT", pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
d = k.encrypt(data)
print ("Cifrado: %r" % d)

cif=open("mensajeseguro.txt","wb")
wri=d
cif.write(wri)
cif.close()

print()
print('Encriptacion 3DES')
print()

clabe = b'unodostrescuatrosincosei'
k = pyDes.triple_des(clabe, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

encry = k.encrypt(data)

print("Cifrado: = %r" % encry)
print()

cif2=open("mensaje_seguro.txt","wb")
wra=encry
cif2.write(wra)
cif2.close()
