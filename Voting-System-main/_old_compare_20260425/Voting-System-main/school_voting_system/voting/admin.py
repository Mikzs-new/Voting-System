from django.contrib import admin

from .models import *

admin.site.register(Election)
admin.site.register(SchoolYearElection)
admin.site.register(YearLevelValidItem)
admin.site.register(CoursesValidItem)
