class Transaction:
    def __init__(self,sender,receiver,amount):
        self.sender=Node(sender)
        self.receiver=Node(receiver)
        self.amount=amount
        
    
    def __str__(self):
        return self.sender.name+' '+self.receiver.name+' '+str(self.amount)
    
    
import hashlib
import time
class Block:
    def __init__(self, index, transactions,previous_hash,nonce,time_stamp):
        self.index=index
        self.transactions=transactions
        self.time_stamp = time_stamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hashlib.sha256(str.encode(str(self.transactions)+str(self.index)+str(self.previous_hash)+str(self.nonce)+str(self.time_stamp))).hexdigest()
        
    def hashBlock(self):
        return self.hash

    def __str__(self):
        a=''
        if type(self.transactions) != list:
            a+= str(['index = ' + str(self.index) +','
                      ' sender = ' + str(self.transactions.sender.name) +','
                      ' receiver = ' + str(self.transactions.receiver.name) +','
                      ' amount = '+ str(self.transactions.amount) +','
                      ' time stamp = ' + str(self.time_stamp) +','
                    ' hash = '+str(self.previous_hash) ])  +'\n' + ('-' *17) + '\n'
        else:
            a='[index = ' + str(self.index) + ' ,'
            for i in range(len(self.transactions)):
               a += str(' [sender = ' + str(self.transactions[i].sender.name) +' ,'
                    ' receiver = ' + str(self.transactions[i].receiver.name) +' ,'
                     ' amount = '+ str(self.transactions[i].amount) +' ] ,')
            a += ' time stamp = ' + str(self.time_stamp) +' ,' + ' hash = '+str(self.previous_hash) +' ]' + '\n' + ('-' *17) + '\n'
        return a
    
import pickle
class BlockChain:
    transactionpool=[]
##    alltransactions=[]
    allmoney={}
    def __init__(self):
        tr=Transaction(' ',' ',' ')
        bl=Block(0,tr,' ',0,time.asctime(time.localtime(time.time()))[11:19])
        self.chain=[bl]
        self.ls_node=[]
    
    def addTransaction(self,transaction):
        self.ls_node.append(transaction.sender)
        self.ls_node.append(transaction.receiver)
        self.transactionpool.append(transaction)
        try:
            self.allmoney[transaction.sender.name]-=(int(transaction.amount))
        except:
            self.allmoney[transaction.sender.name]=-(int(transaction.amount))
        print(self.allmoney)
            
        
    def data(self):
        return str(self.transactionpool)+str(len(self.chain))+str(self.chain[-1].hashBlock())
        
        
    def mine(self,name,nonce,time):
        ls=[]
        for i in range(len(self.transactionpool)):
            ls.append(int(self.transactionpool[i].amount))
        reward=sum(ls)//10
        block=Block(len(self.chain),self.transactionpool,self.chain[-1].hashBlock(),nonce,time)
        print(block.hashBlock())
        if block.hashBlock()[0:2]=='00':
            print('Valid Hash :)')
            transaction=Transaction(central_node.name,name,reward)
            self.chain.append(block)
            for i in range(len(self.transactionpool)):
                try:
                    self.allmoney[self.transactionpool[i].receiver.name]+=(int(self.transactionpool[i].amount))
                except:
                    self.allmoney[self.transactionpool[i].receiver.name
                                  ]=(int(self.transactionpool[i].amount))
                
            self.transactionpool=[transaction]
            
            
        
    def save(self,address):
        fileObject=open(address,'wb')
        pickle.dump(self.chain,fileObject)
        fileObject.close()
        
        
    def load(self,address):
        try:
            fileObject=open(address,'rb')
            self.chain=pickle.load(fileObject)
            return True
        except:
            print('Loading Failed!')
            return False
        
    def validationCheck(self):
        for i in range(len(self.chain)-1):
            if self.chain[i+1].previous_hash != self.chain[i].hashBlock():
                print('Invalid Block!!!')
                return False
        return True
    
    def __str__(self):
        a=' '
        for i in range(len(self.chain)):
           a += (str(self.chain[i]))
        return a        

class Node:
    def __init__(self,name):
        self.name=name
        
    def cal_balance(self):
        try:
            coin=BlockChain.allmoney[self.name]
        except:
            coin=0
        return str(coin)
        
    
    def __str__(self):
        return self.name

central_node=Node('central')

ser_block=BlockChain()


from flask import Flask,request
app=Flask(__name__)
@app.route('/new/transaction', methods=['POST'])
def transaction():
     sender=request.args['sender']
     receiver=request.args['receiver']
     amount=request.args['amount']
     transaction=Transaction(sender,receiver,amount)
     ser_block.addTransaction(transaction)
     return ('Transaction added :)')
    
    
@app.route('/validity' , methods=['GET'])
def valid():
    if ser_block.validationCheck():
        return ('Chain is valid :)')
    else:
        return ('Chain is invalid :(')
 

@app.route('/cal/balance', methods=['POST'])
def calculate():
    name=request.args['name']
    node=Node(name)
    a=node.cal_balance()
    return str(a)


@app.route('/show' , methods=['GET'])
def show():
    return str(ser_block)


@app.route('/save' , methods=['POST'])
def save():
    address=request.args['address']
    ser_block.save(address)
    return ('Block saved :)')

@app.route('/load' , methods=['POST'])
def load():
    address=request.args['address']
    ser_block.load(address)
    return ('Block loaded :)')

@app.route('/mine' , methods=['POST'])
def mine():
    nonce=request.args['nonce']
    time=request.args['time']
    name=request.args['name']
    ser_block.mine(name, nonce, time)
    return ('Block mined :)')

@app.route('/bl' , methods=['GET'])
def bl():
    return ser_block.data()

@app.route('/bye' , methods=['GET'])
def bye():
    return ('BYE :)')
app.run('',port=3000)