from django.contrib import admin
from .models import teacher_subject, assignments_by_teacher, assignment_and_class, teacher_in_class

admin.site.register(assignments_by_teacher)
admin.site.register(assignment_and_class)
admin.site.register(teacher_in_class)
admin.site.register(teacher_subject)

# Register your models here.
