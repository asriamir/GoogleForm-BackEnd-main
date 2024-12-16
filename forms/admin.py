from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Form, Question, Answer


class FormAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

    def clean_title(self, obj):
        if len(obj.title) > 100:
            raise ValidationError('Title cannot exceed 100 characters')
        return obj.title


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'form', 'question_type', 'required', 'max_length', 'min_value', 'max_value', 'allow_decimal')
    search_fields = ('text', 'form__title')
    list_filter = ('form', 'question_type', 'required')

    # Custom validation for Question model
    def clean(self, obj):
        if obj.question_type == 'short_text' and obj.max_length > 200:
            raise ValidationError('Max length for short text question cannot exceed 200 characters.')

        if obj.question_type == 'long_text' and obj.max_length > 5000:
            raise ValidationError('Max length for long text question cannot exceed 5000 characters.')

        if obj.question_type == 'number' and obj.min_value and obj.max_value:
            if obj.min_value > obj.max_value:
                raise ValidationError('Min value cannot be greater than max value.')

        return obj


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text_answer', 'numeric_answer', 'email_answer')
    search_fields = ('question__text', 'text_answer', 'numeric_answer', 'email_answer')
    list_filter = ('question',)

    # validation for Answer model (if needed)
    def clean(self, obj):
        # For numeric_answer, ensure it's within the valid range for the question
        if obj.question.question_type == 'number':
            if obj.numeric_answer < obj.question.min_value or obj.numeric_answer > obj.question.max_value:
                raise ValidationError(f"Answer must be between {obj.question.min_value} and {obj.question.max_value}")
        return obj


admin.site.register(Form, FormAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
