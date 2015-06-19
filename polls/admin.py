from django.contrib import admin



from .models import Choice,Route


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class RouteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['route_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_filter = ['pub_date']
    search_fields = ['route_text']
    list_display = ('route_text', 'pub_date', 'was_published_recently','by')
    inlines = [ChoiceInline]




admin.site.register(Route, RouteAdmin)
