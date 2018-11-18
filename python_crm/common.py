# 公共返回对象
class Message(object):

    def __init__(self, code=200, msg='success', obj=None):
        self.code = code,
        self.msg = msg,
        self.obj = obj

    def result(self):
        result = {'code': self.code[0], 'msg': self.msg[0]}
        if self.obj:
            result['obj'] = self.obj[0]
        return result