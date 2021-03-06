from quiz import views as quiz_views
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register('question', quiz_views.QuestionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('question/by_subject/<int:id>', quiz_views.ByQuestion.as_view(), name='by-question'),
    path('subjects', quiz_views.SubjectViews.as_view(), name='subjects'),
    path('papers', quiz_views.PaperViews.as_view(), name='papers'),
    path('subject/by_paper/<int:paper_id>', quiz_views.SubjectByPaper.as_view(), name='subject-by-papers'),
    path('login', quiz_views.LoginView.as_view(), name='login'),
    path('logout', quiz_views.LogoutView.as_view(), name='logout'),
    path('signup', quiz_views.CreateUserView.as_view(), name='signup'),
    path('test/<int:test_id>', quiz_views.QuizView.as_view(), name='view-test'),
    path('time', quiz_views.TimeView.as_view(), name='time'),
    path('result', quiz_views.QuizResultView.as_view(), name='quiz-result'),
]

# Url's configuration for static, media, and router url's
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
