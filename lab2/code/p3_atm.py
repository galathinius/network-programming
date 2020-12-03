import p2_0_session as ses

clients = [
    {
        'number': '15643',
        'password': '2615',
        'balance': '0.0',
        },
    {
        'number': '87352',
        'password': '7845',
        'balance': '56.87'
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
            clients[index] = acc
            break    

def update_balance(acc_nr, mony):
    for index in range(len(clients)):
        if clients[index]['number'] == acc_nr:
            initial = clients[index]['balance']
            initial = float(initial)
            # mony = float(mony)
            initial += mony
            clients[index]['balance'] = str(initial)
            return True
    
    return False

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

def get_back(atm):
    ses.recv(atm.atm)
    show_main(atm)
    
def eject_card(atm):
    mess = 'Here is your card\n' + atm.client_card + '\n'
    ses.send(mess, atm.atm)
    # idle_atm(atm)

def change_pin(atm):
    mess = 'Please enter old PIN\n'
    ses.send(mess, atm.atm)
    resp = ses.recv(atm.atm)
    if resp == atm.client_acc['password']:
        mess = 'Please enter new PIN\n'
        ses.send(mess, atm.atm)
        resp = ses.recv(atm.atm)
        atm.client_acc['password'] = resp
        update_acc(atm.client_acc)
        mess = 'PIN changed\n1. Back\n'
        ses.send(mess, atm.atm)
        get_back(atm)

def tranfer_mony(atm):
    mess = 'Introduce account to transfer:\n'
    ses.send(mess, atm.atm)
    add_acc = ses.recv(atm.atm)
    mess = 'Introduce amount of money to transfer:\n'
    ses.send(mess, atm.atm)
    mony = ses.recv(atm.atm)

    update_balance(add_acc, float(mony))
    update_balance(atm.client_card, - float(mony))
    mess = 'Transfer done\n1. Back\n'
    ses.send(mess, atm.atm)
    get_back(atm)
    pass

def get_cash(atm):
    mess = 'Introduce sum to get:\n'
    ses.send(mess, atm.atm)
    resp = ses.recv(atm.atm)
    update_balance(atm.client_card, - float(resp))
    mess = 'Balance changed\n1. Back\n'
    ses.send(mess, atm.atm)
    get_back(atm)
    pass

def chek_balance(atm):
    mess = 'Balance:\n' + atm.client_acc['balance']
    mess += '\n1. Back\n'
    ses.send(mess, atm.atm)
    get_back(atm)

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