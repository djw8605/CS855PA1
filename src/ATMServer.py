#!/usr/bin/python
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
    



class Account:
    """
    A lockable account in the ATM
    
    """
    def __init__(self, id, amount):
        self.id = id
        self.amount = float(amount)
        self.tmp_amount = self.amount
        self.locked = False
        self.locked_customer = -1
        self._lock = threading.Lock()

        
        self.lock_queue = []
        
    def lock(self, customer):
        
        self._lock.acquire()
        if customer == self.locked_customer:
            self._lock.release()
            return True
        
        if self.locked == False:
            # Check the queue
            if len(self.lock_queue):
                print self.lock_queue
                if customer == self.lock_queue[0]:
                    # Your the next in the queue, so return
                    self.lock_queue.pop(0)
                    self.locked_customer = customer
                    self.locked = True
                    self._lock.release()
                    return True
                else:
                    # Your not the next in the queue
                    if customer in self.lock_queue:
                        self._lock.release()
                        return False
                    else:
                        self.lock_queue.append(customer)
                        self._lock.release()
                        return False
            else:
                # If queue is empty, then you got the lock
                self.locked = True
                self.locked_customer = customer
                self._lock.release()
                return True
        else:
            # If the lock is already taken, put yourself on the queue
            # Put the thread in a queue
            if customer not in self.lock_queue:
                self.lock_queue.append(customer)
            self._lock.release()
            return False
            
    def unlock(self, customer):
        self._lock.acquire()
        if self.locked == True:
            self.locked = False
        self._lock.release()
    
    def deposit(self, amount):
        self.tmp_amount += float(amount)
        
    def withdraw(self, amount):
        self.tmp_amount -= float(amount)
        
    def inquiry(self):
        return float(self.tmp_amount)
        
    def commit(self):
        self.amount = self.tmp_amount 
        
    def abort(self):
        self.tmp_amount = self.amount
        
        
        
    

class ATMServer:
    """
    The Main ATMServer that should be used to export.
    
    """
    
    def __init__(self):
        
        # Initialized the starting account
        self.accounts = {100: Account(100, 1000.0),
                         200: Account(100, 1000.0)}
                         
        self.customer = {}
        
        
    def _initialize_customer(self, customer):
        if customer not in self.customer:
            self.customer[int(customer)] = []
        
        
    def deposit(self, customer, account, amount):
        """Deposit money into the account.
        
        :param int customer: Customer number
        :param int account: Account number to deposit money into
        :param float amount: value to be added to the account
            
        :rtype: status dict, see: :ref:`Status Dictionary <status-dict>`
        
        This function will fail if the account does not exist.
        
        """
        
        self._initialize_customer(customer)
        if account not in self.accounts:
            return { 'status': 'ERROR', 'reason': "Account %s was not found" % account }
            
        if not self.accounts[int(account)].lock(customer):
            return { 'status': 'WAIT' }
        else:
            if int(account) not in self.customer[int(customer)]:
                self.customer[int(customer)].append(account)
        
        self.accounts[int(account)].deposit(float(amount))
        return { 'status': 'OK' }

        
    def withdraw(self, customer, account, amount):
        """Withdraw money from the account
        
        :param int customer: Customer number
        :param int account: Account number to deposit money into
        :param float amount: value to be added to the account
            
        :rtype: status dict, see: :ref:`Status Dictionary <status-dict>`
            
        This function will fail if the account does not have sufficient funds to make the withdraw.
        
        """
        self._initialize_customer(customer)
        if account not in self.accounts:
            return { 'status': 'ERROR', 'reason': "Account %s was not found" % account }
            
        if not self.accounts[int(account)].lock(customer):
            return { 'status': 'WAIT' }
        else:
            if int(account) not in self.customer[int(customer)]:
                self.customer[int(customer)].append(account)
        
        if  self.accounts[int(account)].inquiry() >= float(amount):
            self.accounts[int(account)].withdraw(float(amount))
            return { 'status': 'OK' }
        else:
            return { 'status': 'ERROR', 'reason': "Insufficient Funds"}

        
    def inquiry(self, customer, account):
        """
        Inquire the account amount
        
        :param int customer: Customer number
        :param int account: Account number to deposit money into
            
        :rtype: status dict, see: :ref:`Status Dictionary <status-dict>`
        
        """
        self._initialize_customer(customer)
        if account in self.accounts:
            
            if not self.accounts[int(account)].lock(customer):
                return { 'status': 'WAIT' }
            else:
                if int(account) not in self.customer[int(customer)]:
                    self.customer[int(customer)].append(account)
                
                return { 'status': 'OK', 'result': self.accounts[account].inquiry() }
        else:
            return { 'status': 'ERROR', 'reason': "Unknown account %s" % account }
            

    def commit_transaction(self, customer):
        """
        Commit a transaction for the customer
        
        :param int customer: Customer number
            
        :rtype: status dict, see: :ref:`Status Dictionary <status-dict>`
        
        """
        self._initialize_customer(customer)
        for account in self.customer[int(customer)]:
            self.accounts[int(account)].commit()
            self.accounts[int(account)].unlock(customer)
            self.customer[int(customer)].remove(account)
        
        return { 'status': 'OK' }
            
            
    def abort_transaction(self, customer):
        """
        Abort a transaction for the customer
        
        :param int customer: Customer number
            
        :rtype: status dict, see: :ref:`Status Dictionary <status-dict>`
        
        """
        self._initialize_customer(customer)
        for account in self.customer[int(customer)]:
            self.accounts[int(account)].abort()
            self.accounts[int(account)].unlock(customer)
            self.customer[int(customer)].remove(account)
    
        return { 'status': 'OK' }
    
        

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



