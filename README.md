#EncryptedIM
An encrypted IM program that uses AES in CBC mode with MAC's using SHA-256.

###Setup and run:

####Example run:
```
pip install pycrypto 

python chat.py -s --confkey SECRETKEY1 --authkey SECRETKEY2
python chat.py -c localhost --confkey SECRETKEY1 --authkey SECRETKEY2
```

Takes Three Command Line Arguments<br />

#####[-s] or [-c IPADDRESS\]  <br />
where -s is the server that is started first, and -c is the client that is started after the server. IPADDRESS can be the address of the server or its network name<br />
#####[--confkey SOMEKEY\] <br />
where SOMEKEY is the agreed upon confidentiality key<br />
#####[--authkey SOMEKEY\]
where SOMEKEY is the agreed upon authenticity key <br /><br />


###Methodology
Once a connection between the sockets is made, the first party to send a message automatically first sends a randomly generated IV in the clear. <br />
Both the client and the server initialize an AES cipher using the IV that was just sent in the clear.<br />
The first message encrypted message comes directly on the heels of the IV <br />


Each ciphertext consists of of MAC and a message.<br /> The MAC is constructed with SHA-256 and the authenticity key. 
The  MAC is the beginning of the message.<br /> After the 16 byte MAC, the message itself begins which is padded to be a multiple of 16 as well. <br />If an unauthenticated message is received, the program displays the occurence and exits. 
