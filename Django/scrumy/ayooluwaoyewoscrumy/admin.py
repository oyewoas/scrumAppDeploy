from django.contrib import admin

# Register your models here.
from .models import ScrumyGoals
from .models import ScrumyHistory
from .models import GoalStatus


admin.site.register(ScrumyGoals)
admin.site.register(ScrumyHistory)
admin.site.register(GoalStatus)