from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from kb.models import FAQ, KBDocument
from kb.serializers import FAQSerializer, KBDocumentSerializer
from common.permissions import IsAdminOrSuperUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rag.ingest import ingest_documents
from rest_framework import status
import os
from django.conf import settings

class FAQViewSet(viewsets.ModelViewSet):
    serializer_class = FAQSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return FAQ.objects.all()
        return FAQ.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [permissions.AllowAny()]


class KBDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KBDocument.objects.filter(is_active=True)
    serializer_class = KBDocumentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]


class KBUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    def post(self, request):
        title = request.data.get("title")
        content = request.data.get("content")
        category = request.data.get("category")
        priority = request.data.get("priority")

        if not title or not content or not category or not priority:
            return Response(
                {"error": "Title, content, category and priority are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        docs_dir = os.path.join(settings.BASE_DIR, "rag", "rag_docs")
        os.makedirs(docs_dir, exist_ok=True)

        filename = f"{title.replace(' ', '_')}.md"
        filepath = os.path.join(docs_dir, filename)

        # 🔥 WRITE SAME FORMAT AS EXISTING .md FILES
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(
                f"TITLE: {title}\n\n"
                f"CATEGORY: {category}\n"
                f"PRIORITY: {priority}\n\n"
                f"CONTENT:\n{content}"
            )

        return Response(
            {"message": "KB document uploaded successfully"},
            status=status.HTTP_201_CREATED
        )

# API BEHAVIOR (VERY IMPORTANT)
# Public (No Login)
# GET /api/kb/faqs/
# GET /api/kb/faqs/{id}/
# ✔ Only active FAQs
# ✔ Read-only
# ---------------------------------------------
# Admin (Logged In)
# POST   /api/kb/faqs/
# PUT    /api/kb/faqs/{id}/
# DELETE /api/kb/faqs/{id}/

# ✔ Full control
# ✔ Protected by IsAdmin