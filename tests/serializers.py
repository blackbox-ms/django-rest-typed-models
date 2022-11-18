from rest_framework import serializers

from rest_typed_models.serializers import TypedModelSerializer

from tests.models import BlogBase, BlogOne, BlogTwo, BlogThree


class BlogBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogBase
        fields = ('name', 'slug')


class BlogOneSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogOne
        fields = ('name', 'slug', 'info')


class BlogTwoSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogTwo
        fields = ('name', 'slug')


class BlogThreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogThree
        fields = ('name', 'slug', 'info', 'about')


class BlogTypedModelSerializer(TypedModelSerializer):
    model_serializer_mapping = {
        BlogBase: BlogBaseSerializer,
        BlogOne: BlogOneSerializer,
        BlogTwo: BlogTwoSerializer,
        BlogThree: BlogThreeSerializer
    }
