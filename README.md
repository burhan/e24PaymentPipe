e24PaymentPipe
==============

> **Notice of Incompatibility** (2019-March)
>
> `KNET`, the payment network in Kuwait has upgraded their paymenent gateway provider. This kit does not work with the new terminal configuration; an updated kit is under development and you can follow the progress [here](https://github.com/burhan/pyipay).


![image](https://badge.fury.io/py/e24PaymentPipe.png%0A%20:target:%20http://badge.fury.io/py/e24PaymentPipe)

![image](https://travis-ci.org/burhan/e24PaymentPipe.png?branch=master%0A%20%20%20%20%20:target:%20https://travis-ci.org/burhan/e24PaymentPipe)

![image](https://img.shields.io/pypi/pyversions/e24PaymentPipe.svg)

![image](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg)

This package provides a Python implementation for ACI's e24PaymentPipe Merchant Gateway

> **Note**
>
> For legacy reasons, the name of the module is kept the same as the one from ACI's toolkit. This does not conform to PEP-8 guidelines.

-   Free software: BSD license
-   Documentation: <http://e24PaymentPipe.rtfd.org>.

Features
--------

-   Written in Python from scratch (not an existing port)
-   Supports both newer and legacy terminal resource (.cgn) file formats
-   Reasonably well documented
-   Proven code - running in production since 2011
-   Compatible with Python 3.4, Python 2.7

Todo
----

-   Add support for credit card payments, including refunds.
-   Create comprehensive test suite

