import time
import functools
import hashlib
import json # json is a decoder and encoder
from collections import OrderedDict
import pickle # we can use pickle to convert our python data to binary data

Mining_reward = 10

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100    # any value because this is the genesis block
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Elon Musk'
participants = {owner}

def hash_block(block): # Using json function to transform everything into a String
    return hashlib.sha256(json.dumps(block, sort_keys = True).encode()).hexdigest() 
# hexdigest is to convert the result in a string
 
def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    print(guess_hash)
    return guess_hash[0:2] == '69'


def proof_of_work():
    last_hash = hash_block(blockchain[-1])
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
        time.sleep(0.005)
    return proof


''' 
json.dumps() - This method allows you to convert a python object into a serialized JSON object.
json.dump() - This method allows you to convert a python object into JSON and additionally allows you to store the information into a file (text file)
json.loads() - Deserializes a JSON object to a standard python object.
json.load() - Deserializes a JSON file object into a standard python object.
'''


def save_data():
    with open('Blockchain_data.txt', mode = 'w') as f: # we changed the mode to wb because using pickle we put 'Write Binary'
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(open_transactions))
        
        # to use pickle we have to create a dictionary that contains all the information we want to pickle

        # save_data = {
        #     'chain' : blockchain,
        #     'ot' : open_transactions
        # }
        # f.write(pickle.dumps(save_data))


def load_data():
    with open('blockchain_data.txt', mode = 'r') as f: 
        # file_content = pickle.loads(f.read()) # Pickle requires much less code than json. But because pickle uses binary, we can not edit the file for example to check the security of our chain, if we try to manipulate one transaction for example.
        file_content = f.readlines() 
        
        global blockchain, open_transactions
        # blockchain = file_content['chain']
        # open_transactions = file_content['ot']
        blockchain = json.loads(file_content[0][:-1]) # [-1] to exclude de \n character
        updated_blockchain = []
        for block in blockchain: 
            updated_block = {
                'previous_hash': block['previous_hash'],
                'index': block['index'],
                'proof': block['proof'],
                'transactions': [OrderedDict(
                [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]
            }
            updated_blockchain.append(updated_block)
        blockchain = updated_blockchain
        open_transactions = json.loads(file_content[1])
        updated_transactions = []
        for tx in open_transactions:
            updated_transaction = [OrderedDict(
                [('sender', tx['sender']),('recipient', tx['recipient']), ('amount', tx['amount'])])]
            updated_transactions.append(updated_transaction)
        open_transactions = updated_transactions


load_data() 


def get_balance(participant):    # We are just interested on the transactions that this participant was related.

    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain] # Calling the amount
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant] # Same logic as above but verifying just in the open_transactions and not in all the blocks
    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    print('Transcations sent: {}'.format(tx_sender))
    print('Transactions received: {}'.format(tx_recipient)) 

    return amount_received - amount_sent 
   
def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain [-1] # There is no need to use else: cause if the first statement won't be attended, the second return will be executed, they can't be executed together anyways


def verify_balance_for_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount'] # We could have written if, else as well. But using return it will return True or False anyways and the code looks cleaner.


def add_transaction(recipient, sender = owner, amount = 1.0):
    #transaction = {
     #  'sender': sender, 
     #  'recipient': recipient, 
     #  'amount': amount
     #  }
    transaction = OrderedDict([('sender', sender),('recipient', recipient),('amount', amount)])
    if verify_balance_for_transaction(transaction): # Here is where the code judge if the transactions will be added to the block (valid) or rejected (invalid)
        open_transactions.append(transaction) # Using append because its a list?
        participants.add(sender)              # Using add because its a set?
        participants.add(recipient)           # Using add because its a set?
        save_data()
        return True
    return False


def mine_block():
    hashed_block = hash_block(blockchain[-1])
    # print(hashed_block)
    proof = proof_of_work()
    mining_reward = OrderedDict([('sender', 'Mining reward'),('recipient', owner,),('amount', Mining_reward)])
    copied_open_transactions = open_transactions[:]
    copied_open_transactions.append(mining_reward)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_open_transactions,
        'proof' : proof
        }
    blockchain.append(block)
    return True


def get_transaction_value():
    sleep()
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Enter the amount sent: '))
    if tx_amount >= 0:
        return tx_recipient, tx_amount
    else:
        print('You can not send a negative value.')
        return tx_recipient==0, tx_amount==0


def get_user_choice():
    sleep()
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    index_block = 0
    for block in blockchain:
        sleep()
        print('Outputting block {}:\n'.format(index_block))
        sleep()
        print('{}\n'.format(block))
        index_block +=1
        sleep()
    else:
        sleep()
        print('-' * 100 +'\n')
        


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue 
        # in this case 'previous_hash' its a key in our dictionary
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):     # we used [:-1] because to reward comes after the validation of the block. So we are excluding the last value of the range
            print('Proof of Work is invalid! ')
            return False
    return True


def verify_transaction():
   all([verify_balance_for_transaction(tx) for tx in open_transactions])
    # 1) [tx for tx in open_transactions] -- to go to all transactions
    # 2) all([verify_balance_for_transaction(tx) for tx in open_transactions]) -- to verify if all are valid

def sleep():
    time.sleep(0.05)
     
waiting_for_input = True


while waiting_for_input:
    sleep()
    print('Choose one of the options:')
    sleep()
    print('1) Insert a new transaction to the blockchain:')
    sleep()
    print('2) Mine a new block:')
    sleep()
    print('3) Output the blockchain blocks:')
    sleep()
    print('4) Output all the participants: ')
    sleep()
    print('5) Check transaction validity')
    sleep()
    print('h) Hack/manipulate the blockchain:')
    sleep()
    print('q) Quit!')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data # It will take the first element of the tuple (tx_data) and store on the recipient variable, and do the same for amount
        if add_transaction(recipient, amount= amount):
            sleep()
            print('Transaction added')
        else:
            sleep()
            print('TRANSACTION FAILED, the sender does not have enough coins.\n')
        sleep()
        print('Open transcations: {}'.format(open_transactions))
    elif user_choice == '2':
        if mine_block() == True:
            open_transactions=[]
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print('Outputting the participants: ' + str(participants))
    elif user_choice == '5':
        if not verify_transaction():
            print('All transactions are valid')
        else: 
            print('Trere are invalid transactions')
    elif user_choice == 'h':
        if len(blockchain) > 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Chris', 'recipient': 'Marcos', 'amount' : 100}]
                }
    elif user_choice == 'q':
        waiting_for_input = False  
    else:
        print('Invalid input, please pick a value from the list')
    if not verify_chain(): # this means the same as if verify_chain is not True.
        print_blockchain_elements()
        print('SOS-' * 35 + 'SOS')
        print('The blockchain was hacked.')
        break
    #print("Elon Musk's Balance: " + str(get_balance('Elon Musk')) + ' Dogecoin(s)\n')
    sleep()
    print('{}\'s balance: {:.2f} {}'.format(owner, get_balance(owner),'Dogecoin(s)'))

else:
    sleep()
    print('User left')

sleep()
print('Done!')