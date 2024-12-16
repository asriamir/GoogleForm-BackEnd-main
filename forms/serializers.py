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


# class QuestionSerializer(serializers.ModelSerializer):
#     form = FormSerializer()
#
# class Meta: model = Question fields = ['id', 'form', 'text', 'required', 'question_type', 'max_length',
# 'min_value', 'max_value', 'allow_decimal']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text_answer', 'numeric_answer', 'email_answer']
