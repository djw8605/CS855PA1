
Server Documentation
====================
   
.. _status-dict:
    
Status Dictionary
-----------------
    
All public functions return a status ``dict`` with the following elements:
    status (str)
        Either ``OK`` or ``ERROR`` indicating success or failure, respectibly
    reason (str)
        If status is ``ERROR``, then reason is the error string describing the issue.
    result (str)
        If the function requires sending back information, it will be stored in the result
    
Operation
---------

This is the main ATMServer that should be executed.
    
It can be executed with the command::
    
   $ python ATMServer.py
    
By default, it will run on port 9000 of the local server, and will listen to traffic from all sources (insecure!)


ATMServer Technical Document
----------------------------

.. automodule:: ATMServer
   :synopsis: An ATM RPC Server
   :members: ATMServer


