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

    def save_model(self, request, obj, form, change):
        # Validation: Ensure only one type of answer is provided
        provided_answers = [
            bool(obj.text_answer),
            bool(obj.numeric_answer),
            bool(obj.email_answer)
        ]

        if sum(provided_answers) > 1:
            self.message_user(request, "Error: Only one type of answer can be provided for a single question.", level="error")
            return

        # Validation: Ensure numeric answer is within range for number type questions
        if obj.question.question_type == 'number':
            if obj.numeric_answer is not None:
                if obj.question.min_value is not None and obj.numeric_answer < obj.question.min_value:
                    self.message_user(
                        request,
                        f"Error: Numeric answer must be greater than or equal to {obj.question.min_value}.",
                        level="error"
                    )
                    return

                if obj.question.max_value is not None and obj.numeric_answer > obj.question.max_value:
                    self.message_user(
                        request,
                        f"Error: Numeric answer must be less than or equal to {obj.question.max_value}.",
                        level="error"
                    )
                    return

        # Validation: Ensure email answer is provided for email type questions
        if obj.question.question_type == 'email' and not obj.email_answer:
            self.message_user(request, "Error: An email answer is required for email type questions.", level="error")
            return

        # Validation: Ensure text answer length is within max_length for short_text and long_text questions
        if obj.question.question_type in ['short_text', 'long_text']:
            if obj.text_answer and len(obj.text_answer) > obj.question.max_length:
                self.message_user(
                    request,
                    f"Error: Text answer cannot exceed {obj.question.max_length} characters.",
                    level="error"
                )
                return

        # Prevent duplicate answers for the same question
        if not change and Answer.objects.filter(question=obj.question).exists():
            self.message_user(request, "Error: An answer already exists for this question.", level="error")
            return

        # Save the object if all validations pass
        super().save_model(request, obj, form, change)


admin.site.register(Form, FormAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
