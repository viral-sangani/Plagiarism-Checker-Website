from django.contrib import admin
from .models import Profile, assignment_by_student, assignment_submitted, assignment_save


admin.site.register(Profile)
admin.site.register(assignment_by_student)
admin.site.register(assignment_submitted)
admin.site.register(assignment_save)