from rest_framework import serializers

from files.models import FileHolder, UrlHolder


class FileHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileHolder
        fields = ['password', 'file']


class UrlHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlHolder
        fields = ['password', 'url']
