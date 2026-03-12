from django.db import models

# ==================================================
# KNOWLEDGE BASE MODELS
# ==================================================

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


# -----------------------------
# KB DOCUMENT
# -----------------------------
class KBDocument(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('PDF', 'PDF'),
        ('DOC', 'Document'),
        ('TXT', 'Text'),
        ('URL', 'URL'),
    ]

    title = models.CharField(max_length=255)
    source_type = models.CharField(max_length=10, choices=SOURCE_TYPE_CHOICES)

    uploaded_by = models.ForeignKey(
        "users.Admin",
        on_delete=models.SET_NULL,
        null=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# -----------------------------
# KB CHUNKS (RAG)
# -----------------------------
class KBChunk(models.Model):
    document = models.ForeignKey(
        KBDocument,
        on_delete=models.CASCADE,
        related_name='chunks'
    )

    chunk_text = models.TextField()

    # pgvector or external vector DB reference
    embedding = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chunk for {self.document.title}"
