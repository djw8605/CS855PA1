#!/usr/bin/python


import xmlrpclib


server = xmlrpclib.ServerProxy('http://localhost:9000')

print server.inquiry(100)
