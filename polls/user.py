 from django.contrib import User


from .models import Choice,Question


class ChoiceInline(user.TabularInline):
    model = Choice
    extra = 1


class QuestionUser(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['route_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_filter = ['pub_date']
    search_fields = ['route_text']
    list_display = ('route_text', 'pub_date', 'was_published_recently','by')



admin.site.register(Question, QuestionUser)
