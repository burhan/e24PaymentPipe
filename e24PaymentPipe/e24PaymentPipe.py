# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import

import zipfile
import os
import datetime
import io

import xml.etree.cElementTree as et

import requests

from .utils import sanitize, xor
from .exceptions import ErrorUrlMissing
from .exceptions import ResponseUrlMissing
from .exceptions import AmountGreaterThanZero


class Gateway(object):
    """Class representing the pipe
       for the gateway. For historical
       reasons it retains the naming for
       the classes in the Java integration
       kit provided by ACI

       To initialize the class, you need two required arguments:

       :param str resource_file:  The **fully qualified** path to the resource file which you will get from
                             your payment processor.
       :param str alias: The alias for the terminal. See your payment provider for more information.

       Optional arguments (with reasonable defaults):

       :param int currency: The ISO currency numeric code for the transaction.
                       Defaults to 414 for Kuwaiti Dinars.
                       See `ISO 4217 <http://en.wikipedia.org/wiki/ISO_4217>_` for a list
                       of codes.
       :param str lang: The language supported by your payment processor. Defaults to 'ENG' for English.

    """

    def __init__(self, resource_file, alias, currency=414, lang='ENG'):
        self.resource_file = resource_file
        self.alias = alias + ".xml"
        self.node_titles = (('id', ''), ('password', ''), ('webaddress', ''), ('port', 443), ('context', ''),
                            ('passwordhash', ''), )
        self.gw = dict(self.node_titles)

        self._udf = {}
        self._amount = 1.0
        self._currency = currency

        self._action = 1  # 1 = Pay, other actions (such as refunds)
        # not yet implemented

        self._response_url = None
        self._error_url = None
        self._trackid = None
        self._lang = lang

    @property
    def udf(self):
        return self._udf

    @udf.setter
    def udf(self, value):
        """Sets the UDF dictionary, and filters out the restricted characters"""
        try:
            if len(list(value.keys())) > 5:
                raise ValueError('Only 5 user defined fields (UDF) are allowed')
            if not all(x[:3].upper() == 'UDF' and 0 < int(x[-1]) <= 5 for x in list(value.keys())):
                raise ValueError('Dictionary keys must be in the form of UDF1 through UDF5')
            self._udf.update({k.upper(): sanitize(str(v)) for k, v in list(value.items())})
        except AttributeError:
            # Passed value does not have a keys() method,
            # assume its not a dictionary
            self._udf.update({'UDF{}'.format(k + 1): sanitize(str(v)) for k, v in enumerate(value)})

    @property
    def error_url(self):
        return self._error_url

    @error_url.setter
    def error_url(self, value):
        self._error_url = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if not value:
            raise AmountGreaterThanZero
        value = float(value)
        if value < 1:
            raise AmountGreaterThanZero
        else:
            self._amount = value

    @property
    def trackid(self):
        return self._trackid

    @trackid.setter
    def trackid(self, value):
        self._trackid = sanitize(value)

    @property
    def response_url(self):
        return self._response_url

    @response_url.setter
    def response_url(self, value):
        self._response_url = value

    def _parse(self):
        out = io.BytesIO()

        with io.open(self.resource_file, mode='rb') as f:
            out.write(xor(bytearray(f.read())))

        try:
            temp = zipfile.ZipFile(out)
        except zipfile.BadZipfile:
            raise zipfile.BadZipfile

        if self.alias in temp.namelist():
            gw_info = xor(bytearray(temp.read(self.alias)))
        else:
            raise ValueError('Invalid alias {0} for resource file {1}, {2}'.format(self.alias,
                                                                              os.path.basename(self.resource_file),
                                                                              temp.namelist()))
        # PY 3
        try:
            xml = et.fromstring(gw_info)
        except TypeError:
            xml = et.fromstring(str(gw_info))

        for node in xml:
            if node.tag in self.gw:
                self.gw[node.tag] = node.text or ''

    def _connect(self, params, transaction_type=1):

        if int(self.gw['port']) == 443:
            scheme = 'https://{}'.format(self.gw['webaddress'])
        else:
            scheme = 'http://{}'.format(self.gw['webaddress'])

        context = self.gw['context'] if self.gw['context'][-1] == '/' else self.gw['context'] + '/'

        if transaction_type == 1:
            # Initialize a transaction
            url = '/{}servlet/PaymentInitHTTPServlet'.format(context)
        else:
            # Conduct payment
            url = '/{}servlet/PaymentTranHTTPServlet'.format(context)

        r = requests.post('{}{}'.format(scheme, url), data=params)
        r.raise_for_status()

        data = r.text

        result = data.split(':', 2)
        info = dict()
        info['paymentID'] = result[0] or None
        info['paymentURL'] = '{}:{}'.format(result[1], result[2]) or None
        return info

    def get_payment_url(self):
        """The main entry point to the class.
         This method is called once all parameters are set in order
         to initiate the pipe and return the payment id and gateway
         URL.

        """

        # Attempt to parse the resource file

        self._parse()

        # Configuration checks

        # if not self._amount:
        #     raise AmountMissing()
        if not self._error_url:
            raise ErrorUrlMissing()
        if not self._response_url:
            raise ResponseUrlMissing()
        if not self._trackid:
            # No tracking id provided, generate one
            # using the time stamp
            self._trackid = '{0.year}{0.month}{0.day}{0.hour}{0.minute}'.format(datetime.datetime.now())
        else:
            self._trackid = sanitize(self._trackid)

        params = dict()

        params.update(self.udf)

        params['id'] = self.gw['id']
        params['password'] = self.gw['password']
        params['amt'] = self._amount
        params['currencycode'] = self._currency
        params['action'] = self._action
        params['langid'] = self._lang
        params['errorURL'] = self._error_url
        params['responseURL'] = self._response_url
        params['trackid'] = self._trackid
        params['passwordhash'] = self.gw['passwordhash']

        return self._connect(params)
