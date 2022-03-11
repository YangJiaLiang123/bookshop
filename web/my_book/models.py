from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    telephone = models.CharField(max_length=11)
    email = models.EmailField(max_length=64)   # unique=True


class Address(models.Model):
    userinfo = models.ForeignKey(UserInfo, related_name='userinfo_address', on_delete=models.CASCADE)
    province = models.CharField(max_length=30)    # 省份
    city = models.CharField(max_length=30)        # 市区
    district = models.CharField(max_length=30)    # 县区
    detail = models.CharField(max_length=128)     # 详细地区
    get_name = models.CharField(max_length=128)
    get_phone = models.CharField(max_length=128)
    get_code = models.CharField(max_length=128)

    def getFullAddress(self):
        return self.province + ' ' + self.city + ' ' + self.district + ' ' + self.detail + '(' + self.get_name + '收)' + ' ' + self.get_phone

