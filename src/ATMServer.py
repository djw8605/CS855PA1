#!/usr/bin/python
from SimpleXMLRPCServer import SimpleXMLRPCServer

class ATMServer:
    
    def __init__(self):
        
        # Initialized the starting account
        self.accounts = {100: 1000.0}
        
        
    def deposit(self, account, amount):
        self.accounts[int(account)] += float(amount)

        
    def withdraw(self, account, amount):
        self.accounts[int(account)] -= float(amount)

        
    def inquiry(self, account):
        if account in self.accounts:
            return self.accounts[account]
        else:
            return 0

        
        

def main():
    server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True, allow_none=True)
    server.register_introspection_functions()
    server.register_multicall_functions()
    server.register_instance(ATMServer())
    try:
        print 'Use Control-C to exit'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Exiting'





if __name__ == "__main__":
    main()



