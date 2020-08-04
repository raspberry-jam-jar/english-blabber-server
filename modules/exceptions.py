class GraphQLError(Exception):
    default_message = 'A server error occurred'
    default_code = 'error'

    def __init__(self, message=None, code=None, **data):
        if message is None:
            message = self.default_message

        if code is None:
            code = self.default_code

        self.code = code
        self.error_data = data

        super().__init__(message)


class PermissionDenied(GraphQLError):
    default_message = 'You do not have permission to perform this action'
    default_code = 'permissionDenied'
