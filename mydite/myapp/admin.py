from django.contrib import admin
from .models import User,Commod,Detail,Orders,Cat
# Register your models here.

admin.site.register(User)
admin.site.register(Commod)
admin.site.register(Detail)
admin.site.register(Orders)

admin.site.register(Cat)