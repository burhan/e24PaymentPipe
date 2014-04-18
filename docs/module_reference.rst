================
Module Reference
================

If you haven't already done so, please read the :doc:`quickstart </usage>` for an overview of the payment process
and a quick example on usage of this module.


Main Methods / Public Interface
-------------------------------

.. py:class:: Gateway(resource, alias, [,currency=414, lang='ENG'])
   
   This is the main class that creates
   parses the terminal resource file
   and creates the gateway link in order
   to initiate the payment process.

   :param str resource: The full path name the the resource file provided by the
                        payment processor
   :param str alias: The alias for the terminal. See your payment processor for more
                     information
   :param int currency: The ISO 4217 numeric code for the currenty of the transaction.
                        See `ISO 4217 <http://en.wikipedia.org/wiki/ISO_4217>`_ for more.
   :param str lang: The language supported by the gateway. See your payment processor's
                    documentation for the languages supported. Defaults to 'ENG' for US English.


.. py:staticmethod:: sanitize(s) -> string
      
      Returns the string stripped of characters
      not allowed in the transaction id or the
      UDF (user defined fields)

      The following characters are stripped:

      ====== === ====
      Symbol Hex Name
      ====== === ====
      ~      x7E TILDE
      `      x60 LEFT SINGLE QUOTATION MARK, GRAVE ACCENT
      !      x21 EXCLAMATION POINT (bang)
      #      x23 NUMBER SIGN (pound sign)
      $      x24 DOLLAR SIGN
      %      x25 PERCENT SIGN
      ^      x5E CIRCUMFLEX ACCENT
      |      x7C VERTICAL LINE (pipe)
      \      x5C REVERSE SLANT (REVERSE SOLIDUS, backslash, backslant)
      :      x3A COLON
      '      x27 APOSTROPHE, RIGHT SINGLE QUOTATION MARK, ACUTE ACCENT (single quote)
      "      x22 QUOTATION MARK, DIAERESIS
      /      x2F SLANT (SOLIDUS, slash)
      ====== === ====

      :param str s: The string to be sanitized
      :return: Sanitized string, with characters not allowed removed
      :rtype: str
 
.. py:method:: get_payment_url() -> dict

      This function returns a two element dictionary
      with the `paymentID` and the `paymentURL` that
      is needed to redirect the user to the gateway.

      In order to call this method, the gateway needs
      to be correctly initialized and configured.

      :raises ValueError: if the object is not configured correctly
      :return: A dictionary of payment id and payment url from the gateway
      :rtype: dict

Properties
----------

Properties are used to set various gateway parameters, and to ensure that all
parameters are correctly sanitized.

All properties are accessed from instances of the gateway object.


+---------------+-------------------------------------------------------------------------+-------------------+
| Property Name | Description                                                             | Required/Optional |
+===============+=========================================================================+===================+
| udf           | Set or get the user defined fields (UDF).                               | Optional          |
|               | Please note the following restrictions:                                 |                   |
|               |                                                                         |                   |
|               | 1. You can only send data for a maximum of 5 fields.                    |                   |
|               | 2. If passing a dictionary, the keys must be named 'UDF[1..5]'          |                   |
|               | 3. When setting the field, if a tuple or list is passed,                |                   |
|               |    the keys are generated automatically.                                |                   |
|               | 4. All values are automatically processed by :py:meth:`sanitize`        |                   |
+---------------+-------------------------------------------------------------------------+-------------------+
| error_url     | The fully qualified URL to the error handler for the gateway.           | Required          |
|               | See the :doc:`quickstart </usage>` for more information                 |                   |
+---------------+-------------------------------------------------------------------------+-------------------+
| amount        | The amount for this transaction, this should be a floating              | Required          |
|               | point number. The default and the minimum is 1.0.                       |                   |
|               | Invalid values will raise a `TypeError`.                                |                   |
+---------------+-------------------------------------------------------------------------+-------------------+
| trackid       | The tracking id for this transaction. It must be a unique value.        | Optional          |
|               | Like the udf fields, it is also sanitized. A default value based        |                   |
|               | on the current timestamp is generated if not provided.                  |                   |
+---------------+-------------------------------------------------------------------------+-------------------+
| response_url  | The fully qualified URL for all affirmative responses from the          | Required          |
|               | gateway. See :doc:`quickstart </usage>`                                 |                   |
+---------------+-------------------------------------------------------------------------+-------------------+

