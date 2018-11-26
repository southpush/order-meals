# -*- coding: utf-8 -*-
class APIException(BaseException):
    def __init__(self, error_id, message, code=500):
        super(BaseException, self).__init__()
        self.raw_message = message
        self.error_id = error_id
        self.code = code
        self.message = message

    def to_dict(self):
        result = {
            "id": self.error_id,
            "code": self.code,
            "message": self.message
        }
        return result


errors = {
    "PersonalUserNotExist": {
        "message": "this personal not exist",
        "status": 404
    }
}
