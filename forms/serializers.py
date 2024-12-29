from rest_framework import serializers
from .models import Form, Question, Answer
from rest_framework.exceptions import ValidationError


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ['id', 'title', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    form = FormSerializer()

    class Meta:
        model = Question
        fields = ['id', 'form', 'text', 'required', 'question_type', 'max_length', 'min_value', 'max_value',
                  'allow_decimal']

    def validate_max_length(self, value):  # field-level validation for max_length
        if value is not None:
            if value < 0:
                raise ValidationError('Max length cannot be negative.')

            question_type = self.initial_data.get('question_type')  # Get question type from input
            if question_type == 'short_text' and value > 200:
                raise ValidationError('Max length for short text question cannot exceed 200 characters.')
            if question_type == 'long_text' and value > 5000:
                raise ValidationError('Max length for long text question cannot exceed 5000 characters.')
        return value

    def validate(self, attrs):  # object-level validation
        question_type = attrs.get('question_type')
        min_value = attrs.get('min_value')
        max_value = attrs.get('max_value')

        # Validation for numeric range
        if question_type == 'number':
            if min_value is not None and max_value is not None and min_value > max_value:
                raise ValidationError({'min_value': 'Min value cannot be greater than max value.'})

        return attrs

    def create(self, validated_data):
        form_data = validated_data.pop('form')  # Extract nested form data
        form, created = Form.objects.get_or_create(**form_data)  # Get or create the form
        question = Question.objects.create(form=form, **validated_data)
        return question

    def update(self, instance, validated_data):
        form_data = validated_data.pop('form', None)
        if form_data:
            form, created = Form.objects.get_or_create(**form_data)
            instance.form = form
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text_answer', 'numeric_answer', 'email_answer']

    def validate(self, attrs):
        question = attrs.get('question')

        # Check if multiple answer types are provided
        provided_answers = [
            bool(attrs.get('text_answer')),
            bool(attrs.get('numeric_answer')),
            bool(attrs.get('email_answer'))
        ]

        if sum(provided_answers) > 1:
            raise ValidationError("Only one type of answer can be provided for a single question.")

        # Check for existing answer
        if Answer.objects.filter(question=question).exists():
            raise ValidationError("An answer already exists for this question.")

        # Validation for short_text and long_text questions
        if question.question_type in ['short_text', 'long_text']:
            text_answer = attrs.get('text_answer', '')
            if not text_answer:
                raise ValidationError({'text_answer': 'This field is required for text type questions.'})
            if len(text_answer) > question.max_length:
                raise ValidationError(
                    {'text_answer': f'Answer length cannot exceed {question.max_length} characters.'}
                )

        # Validation for number questions
        elif question.question_type == 'number':
            numeric_answer = attrs.get('numeric_answer')
            if numeric_answer is None:
                raise ValidationError({'numeric_answer': 'This field is required for numeric type questions.'})
            if question.min_value is not None and numeric_answer < question.min_value:
                raise ValidationError(
                    {'numeric_answer': f'Answer must be greater than or equal to {question.min_value}.'}
                )
            if question.max_value is not None and numeric_answer > question.max_value:
                raise ValidationError(
                    {'numeric_answer': f'Answer must be less than or equal to {question.max_value}.'}
                )

        # Validation for email questions
        elif question.question_type == 'email':
            email_answer = attrs.get('email_answer')
            if not email_answer:
                raise ValidationError({'email_answer': 'This field is required for email type questions.'})

        return attrs

# class AnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Answer
#         fields = ['id', 'question', 'text_answer', 'numeric_answer', 'email_answer']
#
#     def validate(self, attrs):
#         question = attrs.get('question')
#
#         provided_answers = [
#             bool(attrs.get('text_answer')),
#             bool(attrs.get('numeric_answer')),
#             bool(attrs.get('email_answer'))
#         ]
#
#         if sum(provided_answers) > 1:
#             raise ValidationError("Only one type of answer can be provided for a single question.")
#
#         if Answer.objects.filter(question=question).exists():
#             raise ValidationError("An answer already exists for this question.")
#
#         if question.question_type == 'short_text' or question.question_type == 'long_text':
#             text_answer = attrs.get('text_answer', '')
#             if not text_answer:
#                 raise ValidationError({'text_answer': 'This field is required for text type questions.'})
#             if len(text_answer) > question.max_length:
#                 raise ValidationError(
#                     {'text_answer': f'Answer length cannot exceed {question.max_length} characters.'}
#                 )
#
#         elif question.question_type == 'number':
#             numeric_answer = attrs.get('numeric_answer')
#             if numeric_answer is None:
#                 raise ValidationError({'numeric_answer': 'This field is required for numeric type questions.'})
#             if question.min_value is not None and numeric_answer < question.min_value:
#                 raise ValidationError(
#                     {'numeric_answer': f'Answer must be greater than or equal to {question.min_value}.'}
#                 )
#             if question.max_value is not None and numeric_answer > question.max_value:
#                 raise ValidationError(
#                     {'numeric_answer': f'Answer must be less than or equal to {question.max_value}.'}
#                 )
#
#         elif question.question_type == 'email':
#             email_answer = attrs.get('email_answer')
#             if not email_answer:
#                 raise ValidationError({'email_answer': 'This field is required for email type questions.'})
#
#         return attrs

