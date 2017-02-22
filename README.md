#EncryptedIM
Takes three command line arguments
	1. [-s] or [-c IPADDRESS]
	2. [--confkey SOMEKEY]
	3. [--authkey SOMEKEY]


Once a connection between the sockets is made, 
the first party to send a message automatically first sends a randomly generated IV in the clear. 
The cipher is the officially created on both the client and server side, 
using the IV that was just sent in the clear. 
The first message comes directly on the heels of the IV but is encrypted using the IV in CBC mode using AES. 


Each ciphertext consists of first a MAC, 
constructed using SHA-256 and the authenticity key. 
The  MAC is the beginning of the message. After the first 16 bytes, the message itself begins which is padded to be a multiple of 16 as well. If an authenticated message is received, the program displays the occurence and exits. 
