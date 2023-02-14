from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


# 强制登录
class LoginMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)
        self.user_session = None

    def process_request(self, request):
        # 排除不需要验证的 url
        if request.path_info in ['/login/']:
            return

        # 读取是否存在用户session信息
        self.user_session = request.session.get('account_cookie')
        if self.user_session:
            return
        return redirect('/login/')
