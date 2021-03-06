#!/usr/bin/python
from SimpleXMLRPCServer import SimpleXMLRPCServer

class ATMServer:
    """
    The Main ATMServer that should be used to export.
    
    """
    
    def __init__(self):
        
        # Initialized the starting account
        self.accounts = {100: 1000.0}
        
        
    def deposit(self, account, amount):
        """Deposit money into the account.
        
        :param int account: Account number to deposit money into
        :param float amount: value to be added to the account
            
        :rtype: status dict, see: :ref:`Status Dictionary <status-dict>`
        
        This function will fail if the account does not exist.
        
        """
        if account not in self.accounts:
            return { 'status': 'ERROR', 'reason': "Account %s was not found" % account }
        
        self.accounts[int(account)] += float(amount)
        return { 'status': 'OK' }

        
    def withdraw(self, account, amount):
        """Withdraw money from the account
        
        :param int account: Account number to deposit money into
        :param float amount: value to be added to the account
            
        :rtype: status dict, see: :ref:`Status Dictionary <status-dict>`
            
        This function will fail if the account does not have sufficient funds to make the withdraw.
        
        """
        if account not in self.accounts:
            return { 'status': 'ERROR', 'reason': "Account %s was not found" % account }
        
        if  self.accounts[int(account)] >= float(amount):
            self.accounts[int(account)] -= float(amount)
            return { 'status': 'OK' }
        else:
            return { 'status': 'ERROR', 'reason': "Insufficient Funds"}

        
    def inquiry(self, account):
        """
        Inquire the account amount
        
        :param int account: Account number to deposit money into
            
        :rtype: status dict, see: :ref:`Status Dictionary <status-dict>`
        
        """
        if account in self.accounts:
            return { 'status': 'OK', 'result': self.accounts[account] }
        else:
            return { 'status': 'ERROR', 'reason': "Unknown account %s" % account }

        
        

def main():
    server = SimpleXMLRPCServer(('', 9000), logRequests=True, allow_none=True)
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



