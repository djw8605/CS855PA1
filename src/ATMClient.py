#!/usr/bin/python
"""
    
.. moduleauthor:: Derek Weitzel <dweitzel@cse.unl.edu>

The ATM Client can be used for example by issueing the command::

    $ python ATMClient.py <server> <port> <operation> <account> [<amount>]

server
    The server that the ATM client should connect to.
port
    Port that the client should use to connect to the ATM Server
operation
    One of:
    
    * inquiry - Check the status of an account
    * deposit - Deposit money into the account
    * withdraw - Withdraw money from an account
    
account
    This is the numeric account number.  Must be an integer
amount
    Amount of money to either deposit or withdraw

"""


import xmlrpclib
import sys
import time


def usage():
    print "usage: %s server port operation account [amount]" % sys.argv[0]


def main():
    """This is the main function
       
    """
    # First parse the arguments
    if len(sys.argv) < 4:
        print "Not enough arguments."
        usage() 
    
    remote_server = sys.argv[1]
    try:
        remote_port = int(sys.argv[2])
    except:
        print "Unable to convert port number to integer: %s" % sys.argv[2]
        sys.exit(1)
    operation = sys.argv[3]
    
    # setup the server
    server = xmlrpclib.ServerProxy("http://%s:%i" % (remote_server, remote_port), )
    
    try:
        customer_number = int(sys.argv[4])
    except:
        print "Unable to convert account number to number: %s" % sys.argv[4]
        sys.exit(1)
    

    
    # Inquiry operation
    if operation == "inquiry":
        
        try:
            account_number = int(sys.argv[5])
        except: 
            print "Unable to convert account number to number: %s" % sys.argv[5]
            sys.exit(1)
        
        while True:
            return_dict = server.inquiry(customer_number, account_number)
            if return_dict['status'] == 'WAIT':
                time.sleep(1)
                continue
            else:
                break
                
        if return_dict['status'] == 'OK':
            print "Current value of account %i is $%.2f" % (account_number, float(return_dict['result']))
        else:
            print "Error from ATM Server: %s" % return_dict['reason']
        
    elif operation == "deposit":
        
        try:
            account_number = int(sys.argv[5])
        except: 
            print "Unable to convert account number to number: %s" % sys.argv[5]
            sys.exit(1)
        
        try:
            account_modify = float(sys.argv[6])
        except:
            print "Unable to convert money to number: %s" % sys.argv[6]
            sys.exit(1)
            
        while True:
            return_dict = server.deposit(customer_number, account_number, account_modify)
            if return_dict['status'] == 'WAIT':
                time.sleep(1)
                continue
            else:
                break
                
        if return_dict['status'] == 'OK':
            print "Successful deposit of $%.2f to account %i" % (account_modify, account_number)
        else:
            print "Error from ATM Server: %s" % return_dict['reason']
        
    elif operation == "withdraw":
        
        try:
            account_number = int(sys.argv[5])
        except: 
            print "Unable to convert account number to number: %s" % sys.argv[5]
            sys.exit(1)
        
        try:
            account_modify = float(sys.argv[6])
        except:
            print "Unable to convert money to number: %s" % sys.argv[6]
            sys.exit(1)
        
        while True:
            
            return_dict = server.withdraw(customer_number, account_number, account_modify)
            if return_dict['status'] == 'WAIT':
                time.sleep(1)
                continue
            else:
                break
                
        if return_dict['status'] == 'OK':
            print "Successful withdraw of $%.2f to account %i" % (account_modify, account_number)
        else:
            print "Error from ATM Server: %s" % return_dict['reason']
    
    elif operation == "begin_transaction":
        # do nothing
        print "Customer %i starts their transaction" % customer_number
        
    elif operation == "end_transaction":
        
        while True:
            return_dict = server.commit_transaction(customer_number)
            if return_dict['status'] == 'WAIT':
                time.sleep(1)
                continue
            else:
                break
        
        print "Customer %i commits their transaction" % customer_number
        
    
    elif operation == "abort_transaction":
        
        while True:
            return_dict = server.abort_transaction(customer_number)
            if return_dict['status'] == 'WAIT':
                time.sleep(1)
                continue
            else:
                break
        print "Customer %i aborts their transaction" % customer_number
        
    
    else:
        print "Unknown operation: %s" % operation
        sys.exit(1)


if __name__ == "__main__":
    main()


