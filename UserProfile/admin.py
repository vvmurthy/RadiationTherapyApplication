# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
print(sys.path)

from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Hospital)

