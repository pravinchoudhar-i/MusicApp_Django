from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import *
# Register your models here.

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]

class MasterLogAdmin(admin.ModelAdmin):
    model = MasterLog
    list_display = ('timeStamp', 'username','description','activity')

    def username(self,obj):
        return obj.user.username
    
admin.site.register(MasterLog, MasterLogAdmin)