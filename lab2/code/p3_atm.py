import p2_0_session as ses

clients = [
    {
        'number': '15643',
        'password': '2615',
        'balance': 0.0,
        },
    {
        'number': '87352',
        'password': '7845',
        'balance': 56.87
        },
]

def get_acc(card, pin):
    for acc in clients:
        if acc['number'] == card and acc['password'] == pin:
            return acc
        else:
            return None

def update_acc(acc):
    # update acc in var
    for index in range(len(clients)):
        if clients[index]['number'] == acc['number']:
            clients[index] == acc
            break    

def update_balance(acc_nr, sum):
    for index in range(len(clients)):
        if clients[index]['number'] == acc_nr:
            clients[index]['number'] += sum

class Atm:
    def __init__(self, atm):
        self.atm = atm
        self.client_card = None
        self.client_acc = None
        

def start_atm():
    server = Atm(ses.start_sever("0.0.0.0", 1919))
    print('started atm')
    idle_atm(server)

def idle_atm(atm):
    print('idle atm')
    card = ses.recv(atm.atm)
    atm.client_card = card
    get_pin(atm)

def get_pin(atm):
    mess = 'Hi, please type PIN\n'
    ses.send(mess, atm.atm)
    for i in range(3):
        pin = ses.recv(atm.atm)
        acc = get_acc(atm.client_card, pin)
        if acc:
            atm.client_acc = acc
            # mess = 'LogIn successful'
            # ses.send(mess, atm.atm)
            break
    show_main(atm)

def show_main(atm):
    mess = 'Hi, what would you like to do?\n0. Eject card\n1. Change PIN\n2. Transfer money\n3. Get cash\n4. Check balance\n'
    ses.send(mess, atm.atm)
    resp = ses.recv(atm.atm)
    if resp == '0':
        eject_card(atm)
    elif resp == '1':
        change_pin(atm)
    elif resp == '2':
        tranfer_mony(atm)
    elif resp == '3':
        get_cash(atm)
    elif resp == '4':
        chek_balance(atm)

    # print (resp)
def eject_card(atm):
    mess = 'Here is your card\n' + atm.client_card + '\n'
    ses.send(mess, atm.atm)
    # idle_atm(atm)

def change_pin(atm):
    mess = 'Please enter old PIN'
    ses.send(mess, atm.atm)
    resp = ses.recv(atm.atm)
    if resp == atm.client_acc['password']:
        mess = 'Please enter new PIN'
        ses.send(mess, atm.atm)
        resp = ses.recv(atm.atm)
        atm.client_acc['password'] = resp
        update_acc(atm.client_acc)

def tranfer_mony(atm):
    pass

def get_cash(atm):
    pass

def chek_balance(atm):
    pass

def resp(client, mess):
    ses.send(mess, client)

def get_answ(client):
    mess = ses.recv(client)
    return mess

def insert_card(number):
    client = ses.connect_to("0.0.0.0", 1919)
    ses.send(number, client)  
    return client

# def 