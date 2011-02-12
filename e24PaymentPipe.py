# encoding: UTF-8
"""
 
 This is a pure python implementation of the e24PaymentPipe class
 usually provided with ACI payment gateway modules.

 The default samples provided with the gateway are only in Java,
 ASP and ColdFusion so this class was created to provide an
 implmentation in pure Python.

 @author Burhan Khalid <burhan.khalid@gmail.com>
 @version 1.0
 
 This code is provided with no license restrictions.
 You may use it, derive from it, modify it at your own peril.
 The author is not responsible should the use of this code
 lead to strange anomilies in the time space continuum.


"""

import cStringIO as StringIO
import itertools
import zipfile
import httplib, urllib
import logging
import logging.handlers
import datetime

from xml.dom.minidom import parseString

class e24PaymentPipe():
    """

      This is the main class that defines the payment pipe. For historical
      reasons, the name of this class matches that of the Java class.

      However, this can easily be changed in any future revisions.

      The class provides the following methods and properties.

      Properties
      ==========

      _buffer = Stores the internal buffer length used when reading resource
      files
      _nodes = list of nodes to be read from the XML file
      _gw = a dictionary that is used to store properties of the gateway
      _action = the default action of the gateway. Currently the only supported
      action is to pay, which is 1

      Sample use:

      from e24PaymentPipe import e24PaymentPipe as gateway
      import datetime
      gw = gateway(resource='somefile.cgn',alias='somealias')
      try:
        gw.parse()
      except e:
        print e
      
      now = datetime.datetime.now()
      trackid = "%d%d%d%d%d" % (now.year,now.month,now.day,now.hour,now.minute)

      try:
        r = gw.transaction(errorurl='http://www.google.com/',
                           responseurl='http://www.google.com/',
                           trackid=trackid,
                           amount=2)
      except e:
        print e

      print('Payment ID: %s' % r[0])
      print('Gateway URL: %s' % r[1])


    """

    def __init__(self, resource=None, alias=None):

        self._buffer = 2320 # Buffer for reading lines from the resource file
        self._nodes = ('id','password','webaddress','port','context')
        self._gw = {} # Stores the various elements to create the gateway
        self._action = 1 # For payment

        self.resource_file = resource
        self.alias = alias

    def _xor(self,  s=None):

        key = ""
        key = itertools.cycle(key)
        return ''.join(chr(ord(x)^ord(y)) for (x,y) in itertools.izip(s,key))


    def parse(self):
        """
          
          Method to parse the resource file for the terminal alias
          provided, and populate the gw array with the terminal information.

          Parameters
          ==========
             None

          Exceptions
          ==========

             zipfile.BadZipfile - in case resource file cannot be read
             "Alias %s not found in %s" - if alias terminal not found in
             resource file

        """

        out = StringIO.StringIO() # Temporary "file" to hold the zipped content
        with open(self.resource_file,'rb') as f:
            out.write(self._xor(f.read(self._buffer)))

        try:
            temp = zipfile.ZipFile(out)
        except zipfile.BadZipfile:
            raise zipfile.BadZipfile

        if self.alias+".xml" in temp.namelist():
            t = temp.open(self.alias+".xml")
            s = self._xor(''.join(f for f in t.read(self._buffer)))
        else:
            raise Exception("Alias %s not found in %s."
                    %(self.alias,self.resource_file))

        d = parseString(s) # Populate the DOM from the XML file

        for node in self._nodes:
            self._gw[node]=d.getElementsByTagName(node)[0].childNodes[0].nodeValue


    def connect(self,params={}):
        """

          Performs the connection to the gateway to retrieve the
          paymentid and gateway URL for submission of the payment request

          Parameters
          ==========

            params - a dictionary of various parameters required to submit to
            the payment gateway for a successfull request.

          Exceptions
          ==========

            httplib.HTTPException
            httplib.NotConnected
            Invalid Response - invalid response recieved from the gateway

          Returns
          =======

            Two member list, as a result of the gateway transaction

        """

        params = urllib.urlencode(params)

        try:
            if self._gw['port'] == httplib.HTTPS_PORT:
                conn = httplib.HTTPSConnection(self._gw['webaddress'],httplib.HTTPS_PORT)
            else:
                conn = httplib.HTTPConnection(self._gw['webaddress'],httplib.HTTP_PORT)
        except httplib.HTTPException:
            raise Exception(httplib.HTTPException,'Cannot open a connection to %s on port %s. Error was %s' %
                    (self._gw['webaddress'],self._gw['port'],httplib.HTTPException))

        try:
            conn.connect()
        except httplib.NotConnected:
            raise Exception(httplib.NotConnected)

        if self._gw['context'][-1] != '/':
            context = self._gw['context']+'/'
        else:
            context = self._gw['context']

        context = '/'+context+'servlet/PaymentInitHTTPServlet'
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        
        try:
            conn.request("POST",context,params,headers)
        except httplib.HTTPException:
            raise httplib.HTTPException

        result = conn.getresponse()
        data = result.read()
        
        try:
            return data.split(':',1)
        except KeyError:
            raise Exception("Invalid Response")


    def transaction(self, amount=1.000, lang='ENG', currency=414, udf={},
            errorurl=None, responseurl=None, trackid=None):

        """

           Main method to initiate a transaction request for the gateway.

           Parameters
           ==========

             amount - float, minimum 1, default 1.000

             lang - code of the language to be used, defaults to 'ENG'

             currency - ISO currency code, defaults to 414 for Kuwaiti Dinars

             udf - a dictionary object containing UDF fields for the
             transaction. See your gateway documentation on UDF fields. Format
             is:

                udf['udf1'] = 'some text'
                udf['udf2'] = 'some text

             errorurl = a fully qualified URL to the error page on the
             merchant's server.
             
             responseurl = a fully qualified URL of the response page on
             merchant's server.

             trackid = a unique tracking id. Can be in any format, but must be
             unique for each transaction request.

             Returns
             =======

             Two member list containing the payment id, and the gateway URL

             Exceptions
             ==========

             In case of an error, an exception is thrown with the text of the
             error message.

        """

        # Setup transaction parameters
       
        params = {}
        params['id'] = self._gw['id']
        params['password'] = self._gw['password']
        params['action'] = self._action

        params['amt'] = amount
        params['currencycode'] = currency
        params['langid'] = lang
        params['errorURL'] = errorurl
        params['responseURL'] = responseurl
        params['trackid'] = trackid

        for k,v in udf:
            params[k.lower()] = v

        try:
            r = self.connect(params)
        except KeyError:
            return False
         
        if r[0][1:6] == 'ERROR':
            raise Exception(r[1])
        
        return r
