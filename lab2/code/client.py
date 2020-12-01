import p3_atm as atm

if __name__ == "__main__":
    machine = atm.insert_card('15643')

    while True:
        ans = atm.get_answ(machine)

        mess = input(ans) 
        atm.resp(machine, mess)

