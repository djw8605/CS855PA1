

Derek's ATM Server Design Document
==================================

This document will discuss the ATM RPC design.

How it Works
------------

The ATM is designed using the python `XMLRPC library <http://docs.python.org/2/library/simplexmlrpcserver.html>`.  T

In my design, the :class:`ATMClient` directly connects to the server.  In this case, the :class:`ATMClient` must know the Server's address.  Full documentation of the Client's operation is documented on the :ref:`client-docs`.

The Server exports an instance of the :class:`ATMServer` object.  This is done with the code::

   from SimpleXMLRPCServer import SimpleXMLRPCServer
   
   server = SimpleXMLRPCServer(('', 9000), logRequests=True, allow_none=True)
   server.register_introspection_functions()
   server.register_multicall_functions()
   server.register_instance(ATMServer())
   try:
       print 'Use Control-C to exit'
       server.serve_forever()
   except KeyboardInterrupt:
       print 'Exiting'
   

Design Trade-offs
-----------------

he XML-RPC library provided by Python greatly simplifies the RPC aspect of the communication.  This is because the Python XMLRPC:

* Does not require interface definition
* Does not require a registrer
* Performs simple XML HTTP requests in order to perform RPC.

Because of these advantages over more complex RPC systems, such as Java's RMI, it is much simplier to create a RPC server in Python.

Improvements and Extensions
---------------------------







