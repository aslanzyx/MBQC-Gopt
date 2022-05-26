class BaseException(Exception):
    def __init__(self, msg):
        super(BaseException, self).__init__(msg)


class OutputException(Exception):
    def __init__(self, msg):
        super(OutputException, self).__init__(msg)
