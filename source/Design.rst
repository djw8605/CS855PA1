

Derek's ATM Server Design Document
==================================

This document will discuss the ATM RPC design.

How it Works
------------

The ATM is designed using the python `XMLRPC library <http://docs.python.org/2/library/simplexmlrpcserver.html>`.

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
   
Each public function (funciton not starting with an underscore) in the :class:`ATMServer` is then available to be called.  Additionally, state is kept between calls since it's all one instance.

The :class:`ATMServer` starts with only 1 account.  Since there is only 1 account, responses are only give for 1 account.  All requests for other accounts will cause an error.

The RPC functions all return a special data structure, a :ref:`Status Dictionary <status-dict>`, which will return the status of the request, as well as a failure reason or a request response.  This is transferred with a dictionary, which is then serialized by the underlying XML RPC library.

Design Trade-offs
-----------------

he XML-RPC library provided by Python greatly simplifies the RPC aspect of the communication.  This is because the Python XMLRPC:

* Does not require interface definition
* Does not require a registrer
* Performs simple XML HTTP requests in order to perform RPC.

Because of these advantages over more complex RPC systems, such as Java's RMI, it is much simplier to create a RPC server in Python.

Since the requests are all done over HTTP, it is very easy and well known how to secure the communication (HTTPS) and how to load balance requests (Linux Virtual Server).

Improvements and Extensions
---------------------------

The design of the :class:`ATMServer` is very simple.  It could be improved by:

* Secure Account Storage - Since we are running on Amazon EC2, this could easily be done with on of many database systems available on EC2 such as Dynamo and RDS.
* Load Balanced Servers - Many more clients can be handled with load balanced HTTP requests.
* Authenticated Requests - It is well known how to handle authorize HTTP requests, digest or SSL Certs.






