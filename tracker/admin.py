from django.contrib import admin
from .models import Abitudine, LogAbitudine

@admin.register(Abitudine)
class AbitudineAdmin(admin.ModelAdmin):
    list_display = ('nome', 'proprietario', 'created_at')
    search_fields = ('nome',)

@admin.register(LogAbitudine)
class LogAbitudineAdmin(admin.ModelAdmin):
    list_display = ('abitudine', 'data', 'completata')
    list_filter = ('completata', 'data')