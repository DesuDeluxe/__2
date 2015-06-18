 from django.contrib import User


from .models import Choice,Question


class ChoiceInline(user.TabularInline):
    model = Choice
    extra = 1


class QuestionUser(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_filter = ['pub_date']
    search_fields = ['question_text']
    list_display = ('question_text', 'pub_date', 'was_published_recently','by')



admin.site.register(Question, QuestionUser)
