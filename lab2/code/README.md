
now the folder structure here<br/>
├── first<br/>
│  ├── client.py<br/>
│  └── server.py<br/>
├── second<br/>
│  ├── client.py<br/>
│  └── server.py<br/>
├── third<br/>
│  ├── client.py<br/>
│  └── server.py<br/>
├── p1_transfer.py<br/>
├── p2_0_session.py<br/>
├── p2_1_encription.py<br/>
└── p3_ atm.py<br/>

The protocols are directly in this folder.<br/>
If you want to start the client and server code, you have to move them from their sub-folder into the code folder.<br/><br/>
The first one is in *p1_transfer.py*. It establishes a connection between two sockets and sends messages between them.<br/>

The second one is in *p2_0_session.py*. <br/>
The connection establishing part exchanges public keys.<br/>
After that the send and receive use those keys to encrypt and decrypt the messages.<br/>

The encryption happens with functions from *p2_1_encription.py* <br/>

For both layers described above the server and client first establish a connection then send messages and wait for a response.

The application layer is represented as an ATM in *p3_ atm.py*.<br/>

For this layer the server just starts the ATM with <br/>
`atm.start_atm()`

And the state is managed internally.

The client then can interact with the ATM:
`machine = atm.insert_card('87352')`

Next, this is what happens on the client side:

`Hi, please type PIN`<br/>
`>>7845`<br/>
`Hi, what would you like to do?`<br/>
`0. Eject card`<br/>
`1. Change PIN`<br/>
`2. Transfer money`<br/>
`3. Get cash`<br/>
`4. Check balance`<br/>
`>>4`<br/>
`Balance:`<br/>
`56.87`<br/>
`1. Back`<br/>
`>>`<br/>
`Hi, what would you like to do?`<br/>
`0. Eject card`<br/>
`1. Change PIN`<br/>
`2. Transfer money`<br/>
`3. Get cash`<br/>
`4. Check balance`<br/>
`>>3`<br/>
`Introduce sum to get:`<br/>
`>>23`<br/>
`Balance changed`<br/>
`1. Back`<br/>
`>>`<br/>
`Hi, what would you like to do?`<br/>
`0. Eject card`<br/>
`1. Change PIN`<br/>
`2. Transfer money`<br/>
`3. Get cash`<br/>
`4. Check balance`<br/>
`>>4`<br/>
`Balance:`<br/>
`33.87`<br/>
`1. Back`<br/>
`>>`<br/>
`Hi, what would you like to do?`<br/>
`0. Eject card`<br/>
`1. Change PIN`<br/>
`2. Transfer money`<br/>
`3. Get cash`<br/>
`4. Check balance`<br/>
`>>0`<br/>
`Here is your card`<br/>
`87352`<br/>

