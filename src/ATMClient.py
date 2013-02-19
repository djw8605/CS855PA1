#!/usr/bin/python

import xmlrpclib
import sys


def usage():
    print "usage: %s server port operation account [amount]" % sys.argv[0]


def main():
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
        account_number = int(sys.argv[4])
    except:
        print "Unable to convert account number to number: %s" % sys.argv[4]
        sys.exit(1)
    
    
    if operation == "inquiry":
        account_value = server.inquiry(account_number)
        print "Current value of account %i is $%.2f" % (account_number, float(account_value))
        
    elif operation == "deposit":
        try:
            account_modify = float(sys.argv[5])
        except:
            print "Unable to convert money to number: %s" % sys.argv[5]
            sys.exit(1)
        server.deposit(account_number, account_modify)
        print "Successful deposit of $%.2f to account %i" % (account_modify, account_number)
        
    elif operation == "withdraw":
        try:
            account_modify = float(sys.argv[5])
        except:
            print "Unable to convert money to number: %s" % sys.argv[5]
            sys.exit(1)
        server.withdraw(account_number, account_modify)
        print "Successful withdraw of $%.2f to account %i" % (account_modify, account_number)
    
    else:
        print "Unidentified operation: %s" % operation
        sys.exit(1)


if __name__ == "__main__":
    main()


