#EncryptedIM

Takes Three Command Line Arguments<br /><br />

####[-s] or [-c IPADDRESS\]  <br />
where -s is the server that is started first, and -c is the client that is started after the server. IPADDRESS can be the address of the server or its network name<br />
####[--confkey SOMEKEY\] <br />
where SOMEKEY is the agreed upon confidentiality key<br />
####[--authkey SOMEKEY\]
where SOMEKEY is the agreed upon authenticity key <br /><br />

###Example setup and run:
```
pip install pycrypto 

python chat.py -s --confkey SECRETKEY1 --authkey SECRETKEY2
python chat.py -c localhost --confkey SECRETKEY1 --authkey SECRETKEY2
```

Once a connection between the sockets is made, 
the first party to send a message automatically first sends a randomly generated IV in the clear. 
The cipher is the officially created on both the client and server side, 
using the IV that was just sent in the clear. 
The first message comes directly on the heels of the IV but is encrypted using the IV in CBC mode using AES. 


Each ciphertext consists of first a MAC, 
constructed using SHA-256 and the authenticity key. 
The  MAC is the beginning of the message. After the first 16 bytes, the message itself begins which is padded to be a multiple of 16 as well. If an authenticated message is received, the program displays the occurence and exits. 
