import re

from django.http import HttpResponse
from django.urls import reverse


class LoginCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):

        urllist = [reverse('bUser :login'), reverse('bUser :book_index'), reverse('bUser :register')]

        if re.match('/', request.path) and request.path not in urllist:

            if request.session.get('username','') == '':
                url = reverse('bUser :login')
                return HttpResponse(f'<script>alert("请先登录"); location.href="{url}";</script>')

        response = self.get_response(request)
        return response