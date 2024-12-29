from django.db import models
from django.core.exceptions import ValidationError


class Form(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Ensure title length is within the limit
        if len(self.title) > 100:
            raise ValidationError({'title': 'Title cannot exceed 100 characters.'})

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = (
        ('short_text', 'Short Text'),
        ('long_text', 'Long Text'),
        ('email', 'Email'),
        ('number', 'Number'),
    )

    form = models.ForeignKey(Form, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    required = models.BooleanField(default=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    max_length = models.PositiveIntegerField(null=True, blank=True)
    min_value = models.IntegerField(null=True, blank=True)
    max_value = models.IntegerField(null=True, blank=True)
    allow_decimal = models.BooleanField(default=False)

    def clean(self):
        if self.question_type == 'short_text' and self.max_length > 200:
            raise ValidationError('Max length for short text question cannot exceed 200 characters.')

        if self.question_type == 'long_text' and self.max_length > 5000:
            raise ValidationError('Max length for long text question cannot exceed 5000 characters.')

        if self.question_type == 'number' and (self.min_value is not None and self.max_value is not None):
            if self.min_value > self.max_value:
                raise ValidationError('Min value cannot be greater than max value.')

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text_answer = models.CharField(max_length=5000, blank=True)
    numeric_answer = models.FloatField(null=True, blank=True)
    email_answer = models.EmailField(null=True, blank=True)

    def clean(self):
        provided_answers = [
            bool(self.text_answer),
            bool(self.numeric_answer),
            bool(self.email_answer)
        ]

        if sum(provided_answers) > 1:
            raise ValidationError("Only one type of answer can be provided for a single question.")

        if self.question.question_type == 'short_text' or self.question.question_type == 'long_text':
            if self.text_answer and len(self.text_answer) > self.question.max_length:
                raise ValidationError(
                    {'text_answer': f'Answer cannot exceed {self.question.max_length} characters.'}
                )

        elif self.question.question_type == 'number':
            if self.numeric_answer is not None:
                if self.question.min_value is not None and self.numeric_answer < self.question.min_value:
                    raise ValidationError(
                        {'numeric_answer': f'Answer must be greater than or equal to {self.question.min_value}.'}
                    )
                if self.question.max_value is not None and self.numeric_answer > self.question.max_value:
                    raise ValidationError(
                        {'numeric_answer': f'Answer must be less than or equal to {self.question.max_value}.'}
                    )

        elif self.question.question_type == 'email':
            if not self.email_answer:
                raise ValidationError({'email_answer': 'Email answer is required for email type questions.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Answer to: {self.question.text}"
