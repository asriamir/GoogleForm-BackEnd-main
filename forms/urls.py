from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormViewSet, QuestionViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r'forms', FormViewSet, basename='form')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet, basename='answer')

urlpatterns = [
    path('', include(router.urls)),  # Include all routes from the router
]


