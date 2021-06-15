import requests
import hashlib
import time
def mining(transactionpool,index,previous_hash):
    nonce=0
    full_string=(str(transactionpool)+str(index)+str(previous_hash))
    Time=time.asctime(time.localtime(time.time()))[11:19]
    while hashlib.sha256(str.encode(full_string+str(nonce)+str(Time))).hexdigest()[0:2] != '00':
        Time=time.asctime(time.localtime(time.time()))[11:19]
        nonce += 1
    return nonce , Time
    
def TUI():
    a='1'
    while a != '8':
        if a=='1' or a=='2' or a=='3' or a=='4' or a=='5' or a=='6' or a=='7':
            print()
            print('What do you want to do?\n')
            print('1.Add new transaction\n')
            print('2.Check the validity of the chain\n')
            print('3.Show the current chain\n')
            print('4.Save the chain\n')
            print('5.Load the chain\n')
            print('6.Calculate balance\n')
            print('7.Mine\n')
            print('8.Quit\n')
            a=input('Enter number: ')
            print()
        else:
            print('You entered wrong number :(')
            print()
            print('What do you want to do?\n')
            print('1.Add new transaction\n')
            print('2.Check the validity of the chain\n')
            print('3.Show the current chain\n')
            print('4.Save the chain\n')
            print('5.Load the chain\n')
            print('6.Calculate balance\n')
            print('7.Mine\n')
            print('8.Quit\n')
            a=input('Enter number: ')
            print()
        
        if a=='1':
            sender=input('Enter the name of sender: ')
            print()
            receiver=input('Enter the name of receiver: ')
            print()
            amount=input('Enter the amount of money: ')
            print()
            res=requests.post('http://127.0.0.1:3000/new/transaction',params={'sender':sender,'receiver':receiver,'amount':amount})
            print(res.text)
            
        if a=='2':
            res=requests.get('http://127.0.0.1:3000/validity')
            print(res.text)
            
        if a=='3':
            res=requests.get('http://127.0.0.1:3000/show')
            print(res.text)
            
        if a=='4':
            address=input('Enter the address: ')
            print()
            res=requests.post('http://127.0.0.1:3000/save',params={'address':address})
            print(res.text)
            
        if a=='5':
            address=input('Enter the address: ')
            print()
            res=requests.post('http://127.0.0.1:3000/load',params={'address':address})
            print(res.text)
            
        if a=='6':
            name=input('Enter name: ')
            print()
            res=requests.post('http://127.0.0.1:3000/cal/balance',params={'name':name})
            print(res.text)
        
        if a=='7':
            res=requests.get('http://127.0.0.1:3000/bl')
            resp=(res.text)
            for i in range(len(resp)):
                if resp[i]==']':
                    transactionpool=resp[0:i+1]
                    index=resp[i+1]
                    previous_hash=resp[i+2:]
                    break
            nonce=mining(transactionpool,index,previous_hash)[0]
            time=mining(transactionpool,index,previous_hash)[1]
            name=input('Enter your name: ')
            print()
            res=requests.post('http://127.0.0.1:3000/mine',params={'name':name , 'nonce':nonce , 'time':time})
            print(res.text)
            
            
        if a=='8':
            res=requests.get('http://127.0.0.1:3000/bye')
            print(res.text)
            
TUI()