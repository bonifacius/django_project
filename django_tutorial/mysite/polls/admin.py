from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    # Можно выбрать сколько вариантов ответов добавить к вопросу
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    # Добавляем инфу о вопросе(вопрос, дата публикации, был ли опубликован недавно)
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # Фильтр по дате публикации в адмике справа
    list_filter = ['pub_date']
    # Добавим возможность поиска по записи
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)