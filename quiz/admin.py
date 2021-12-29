from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
# Register your models here.
from .models import Quiz, Category, Question, Progress, Result
from mcq.models import MCQQuestion, Answer
from django.utils.translation import ugettext_lazy as _
import datetime 
from django.utils import timezone
from django.contrib.admin.filters import DateFieldListFilter
import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib import auth
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


class AnswerInline(admin.TabularInline):
    model = Answer


class QuizAdminForm(forms.ModelForm):
    """
        below is from
        http://stackoverflow.com/questions/11657682/
        django-admin-interface-using-horizontal-filter-with-
        inline-manytomany-field
    """

    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(
            verbose_name=_("Questions"),
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial = \
                self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz


class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm

    list_display = ('title', 'category', )
    list_filter = ('category',)
    search_fields = ('description', 'category', )


class CategoryAdmin(admin.ModelAdmin):
    
    search_fields = ('category', )


class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'category', )
    list_filter = ('category',)
    fields = ('content', 'category',
              'figure', 'quiz', 'explanation', 'answer_order')

    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

    inlines = [AnswerInline]


class ProgressAdmin(admin.ModelAdmin):
    """
    to do:
            create a user section
    """
    search_fields = ('user', 'score', )



class ResultAdmin(admin.ModelAdmin):
    list_filter = (
        ('date_time', DateRangeFilter),
    )

admin.site.unregister(auth.models.Group)

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MCQQuestion, MCQuestionAdmin)
admin.site.register(Result, ResultAdmin)
