from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter()
def kong_upper(val):
    return val.upper()

@register.simple_tag()
def jia(a, b):

    res = int(a) + int(b)
    return res

@register.simple_tag()
def pagess(num,request):

    p = int(request.GET.get("page_num",1))

    start = p-5
    end = p+4
    if start <= 0:
        start = 1
        end=10
    if end > num:
        end = num
        start = num-10
    if num <= 10:
        start = 1
        end = num

    s = ''
    for i in range(start, end+1):

        s += f'<a href="?page_num={i}">{i}</a>'

    return format_html(s)

