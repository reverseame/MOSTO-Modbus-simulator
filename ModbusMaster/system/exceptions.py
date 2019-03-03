
class MasterError(Exception):

    def __init__(self, msg="Internal Error"):
        Exception.__init__(self)
        self.message = msg


class SendingDataError(MasterError):

    def __init__(self):
        MasterError.__init__(self, "No data to send")
