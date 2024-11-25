"""Module for Django admin."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Courses, Labs, LabGroups, Report, SignUp

admin.site.register(User, UserAdmin)

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('name', 'labs_amount', 'is_visible')

@admin.register(Labs)
class LabsAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'max_students', 'is_visible')

@admin.register(LabGroups)
class LabGroupsAdmin(admin.ModelAdmin):
    list_display = ('formatted_date', 'lab', 'formatted_start_time', 'formatted_end_time', 'signed_up_students', 'assistant')

    def formatted_date(self, obj):
        return obj.date.strftime("%d-%m-%Y")
    formatted_date.short_description = "date"

    def formatted_start_time(self, obj):
        if obj.start_time:
            return obj.start_time.strftime("%H:%M")
        return
    formatted_start_time.short_description = "start time"

    def formatted_end_time(self, obj):
        if obj.end_time:
            return obj.end_time.strftime("%H:%M")
        return
    formatted_end_time.short_description = "end time"

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'lab_group', 'formatted_send_date', 'grade', 'formatted_grading_date', 'graded_by')

    def formatted_send_date(self, obj):
        if obj.send_date:
            return obj.send_date.strftime("%d-%m-%Y")
        return
    formatted_send_date.short_description = "send date"

    def formatted_grading_date(self, obj):
        if obj.grading_date:
            return obj.grading_date.strftime("%d-%m-%Y")
        return
    formatted_grading_date.short_description = "grading date"

@admin.register(SignUp)
class SignUpAdmin(admin.ModelAdmin):
    list_display = ('user', 'labgroups')
