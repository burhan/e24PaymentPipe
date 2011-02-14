# encoding: utf-8
"""

 This modules defines custom exceptions that
 are used for the e24PaymentPipe class

 @author Burhan Khalid <burhan.khalid@gmail.com>
 @version 1.0

 This code is provided with no license restrictions.
 You may use it, derive from it, modify it at your own peril.
 The author is not responsible should the use of this code
 lead to strange anomilies in the time space continuum.


"""
__author__ = 'Burhan Khalid <burhan.khalid@gmail.com>'

class AliasNotFound(Exception): pass
class InvalidResponse(Exception): pass
class GatewayError(Exception): pass
  