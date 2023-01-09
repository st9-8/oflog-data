from django.contrib import admin

from core.models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code_module', 'code_presentation')


@admin.register(StudentInfo)
class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ('id_student', 'course', 'gender')


@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'date_registration', 'date_unregistration')


@admin.register(VLE)
class VLEAdmin(admin.ModelAdmin):
    list_display = ('id_site', 'course', 'activity')
    list_filter = ('activity',)


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id_assessment', 'course', 'assessment_type', 'date')
    list_filter = ('assessment_type',)


@admin.register(StudentAssessment)
class StudentAssessmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'assessment', 'date_submitted')


@admin.register(StudentVle)
class StudentVleAdmin(admin.ModelAdmin):
    list_display = ('material', 'course', 'student')
