class Wrapper:
    def __init__(self, data):
        """
          A Base class to be used for representing success or error response

          Arguments:
              :param data: data to be set as response
          """
        self.data = data


class ErrorWrapper(Wrapper):
    def __init__(self, error_message):
        """ Error Wrapper extends Wrapper class to populate fields related to error

               Arguments:
                     :param error_message: Error Message to be set
           """
        self.error = error_message
        self.success = False
        super().__init__(None)


class SuccessWrapper(Wrapper):
    def __init__(self, data):
        """ Success Wrapper extends Wrapper class to populate fields related to error

               Arguments:
                     :param data: data to be set for success response
           """
        self.success = True
        super().__init__(data)
