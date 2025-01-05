from django.contrib import admin
from .models import Position, Candidate, Voter

# Register your models here.


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'votes')


class VoterAdmin(admin.ModelAdmin):
    list_display = ('matric_number', 'ip_address')



admin.site.register(Position, PositionAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Voter, VoterAdmin)