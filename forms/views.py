from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Form, Question, Answer
from .serializers import FormSerializer, QuestionSerializer, AnswerSerializer


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        form = self.get_object()
        questions = form.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
