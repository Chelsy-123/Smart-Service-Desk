from rest_framework.routers import DefaultRouter
from kb.views import FAQViewSet, KBDocumentViewSet, KBUploadView
from django.urls import path
router = DefaultRouter()
router.register(r'faqs', FAQViewSet, basename='faq')

router.register(r'documents', KBDocumentViewSet)

urlpatterns = [
    path("upload/", KBUploadView.as_view()),
] + router.urls
# api endpoints:
# /api/kb/faqs/
# /api/kb/documents/