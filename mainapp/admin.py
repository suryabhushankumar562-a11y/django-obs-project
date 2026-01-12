from django.contrib import admin
from .models import Enquiry, LoginInfo, UserInfo, Book

# Register your models here.
admin.site.register(Enquiry)
admin.site.register(LoginInfo)
admin.site.register(UserInfo)
