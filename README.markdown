e24PaymentPipe Python Class
===========================

  This project contains a pure Python implementation
  of the ACI Worldwide Payment Gateway that is used
  by many payment gateway providers.

  Usually, the implementation kit comes with a few
  reference implementations of the payment gateway, but they
  are only available as a Java class, or a .dll library.

  So this python class was created for those of us that do
  not use Java or ASP.NET/.dlls for their development.

  The library has successfully been used in production.

  *UPDATE - 2011-12-28*

     A __*major*__ update and overhaul has been done, and a new
     branch production has been created.
  
  Quick Start
  -----------

  ```python
    from e24PaymentPipe import e24PaymentPipe as gw
    g = gw('/some/path/to/somefile.cgn','somealias')
    try:
      g.parse()
    except zipfile.BadZipfile:
    except AliasNotFound:
      pass

    # Before you try a transaction,
    # you have to set the error and response URLs

    g.ERROR_URL = 'https://www.example.com/error.html'
    g.RESPONSE_URL = 'https://www.example.com/response.jsp'

    trackid = 12343
    try:
       r = g.transaction(trackid,amount)
    except e:
       print e

    print('Payment ID: %s' % r[0])
    print('Payment URL: %s' % r[1])
  ```

  For more detailed docs, see the inline documentation provided in the class
