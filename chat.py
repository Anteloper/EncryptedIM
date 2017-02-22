import argparse
import socket
import sys
import select
import signal
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Hash import HMAC

def handler(signum,frame):
    sys.exit(0)

def chat(socket):
	global confkey
	global authkey
	#Client and server both generate a random IV. The first person to send a message also 
	#sends the IV that both parties will use.
	IV = Random.new().read( AES.block_size )
	IVAgreedUpon = False
	#This will be set once we agree upon an IV
	cipher = None
	authenticator = HMAC.new(authkey)
	
	readable = [socket, sys.stdin]
	while True:
		r, writeable, exceptionable = select.select(readable, [], [])
		if socket in r:
			data = socket.recv(1024)
			if not IVAgreedUpon:
				IVAgreedUpon = True
				IV = data
				cipher = AES.new(confkey, AES.MODE_CBC, IV)
			else:
				print authenticate(cipher.decrypt(data), authenticator)

		if sys.stdin in r:
			if not IVAgreedUpon:
				socket.send(IV)
				IVAgreedUpon = True
				cipher = AES.new(confkey, AES.MODE_CBC, IV)

			m = sys.stdin.readline()
			authenticator.update(pad(m))
			hash = authenticator.digest()
			ciphertext = cipher.encrypt(hash + pad(m))
			

			socket.send(ciphertext)

def authenticate(data, authenticator):
	MAC = data[:16]
	message = data[16:]
	authenticator.update(message)
	if authenticator.digest() == MAC:
		return unpad(message)
	else:
		print "Unauthenticated Message, program will exit now"
		sys.exit(0)



#Inspired by the pad function found here:
#https://gist.github.com/crmccreary/5610068
def pad(message):
	l = len(message)
	padding = (16 - l % 16) * chr(16 - l % 16) 
	return message+padding

def unpad(message):
	return message[0:-ord(message[-1])]

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-c", "--client", type=str)
group.add_argument("-s", "--server", action="store_true")
parser.add_argument("--confkey" , type=str)
parser.add_argument("--authkey", type=str)
args = parser.parse_args()
port = args.server
signal.signal(signal.SIGINT,handler)
confkey = SHA256.new(args.confkey).digest()
authkey = args.authkey

if args.client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((args.client, 9999))
	chat(sock)

elif args.server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(("", 9999))
	sock.listen(5)
	conn, addr = sock.accept()
	chat(conn)
					
				



