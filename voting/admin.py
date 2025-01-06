from django.contrib import admin
from .models import Position, Candidate, Voter

# Register your models here.


from django.contrib import admin
from .models import Position, Candidate, Voter

# Register your models here.


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'votes')
    search_fields = ('name', 'position__name')
    list_filter = ('position',)


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('matric_number', 'ip_address')
    search_fields = ('matric_number',)
    list_filter = ('matric_number',)