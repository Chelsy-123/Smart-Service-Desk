from rest_framework import serializers
from kb.models import FAQ, KBDocument, KBChunk


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            'id',
            'question',
            'answer',
            'category',
            'is_active',
            'created_at'
        ]
        read_only_fields = ['created_at']


class KBDocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = KBDocument
        fields = [
            'id',
            'title',
            'source_type',
            'uploaded_by',
            'is_active',
            'created_at'
        ]
        read_only_fields = ['uploaded_by', 'created_at']


class KBChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = KBChunk
        fields = ['id', 'document', 'chunk_text']
