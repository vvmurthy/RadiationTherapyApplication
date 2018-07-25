# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
print(sys.path)

from django.contrib import admin
try:
	from models import UserProfile
except:
	from .models import UserProfile # Python 3 compatibility
# Register your models here.
admin.site.register(UserProfile)

