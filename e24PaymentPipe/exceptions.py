__author__ = 'burhan'


class ErrorUrlMissing(Exception):
    pass


class ResponseUrlMissing(Exception):
    pass


class AmountGreaterThanZero(Exception):
    pass


class GatewayError(Exception):
    pass
