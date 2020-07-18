class WechatyError(Exception):
    """ Wechaty error """

    def __init__(self, message, code=None, params=None):
        super().__init__(message, code, params)

        self.message = message
        self.code = code
        self.params = params

    def __str__(self):
        return repr(self)


class WechatyAccessoryBindingError(WechatyError):
    pass


class WechatyStatusError(AttributeError, WechatyError):
    pass


class WechatyConfigurationError(AttributeError, WechatyError):
    pass


class WechatyOperationError(WechatyError):
    pass


class WechatyPluginError(WechatyError):
    pass


class WechatyPayloadError(ValueError, WechatyError):
    pass
