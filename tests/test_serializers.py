from django.core.exceptions import ImproperlyConfigured

import pytest

from rest_typed_models.serializers import TypedModelSerializer

from tests.models import BlogBase, BlogOne, BlogTwo
from tests.serializers import BlogTypedModelSerializer

pytestmark = pytest.mark.django_db


class TestTypedModelSerializer:

    def test_model_serializer_mapping_is_none(self):
        class EmptyTypedModelSerializer(TypedModelSerializer):
            pass

        with pytest.raises(ImproperlyConfigured) as excinfo:
            EmptyTypedModelSerializer()

        assert str(excinfo.value) == (
            '`EmptyTypedModelSerializer` is missing a '
            '`EmptyTypedModelSerializer.model_serializer_mapping` attribute'
        )

    def test_resource_type_field_name_is_not_string(self, mocker):
        class NotStringTypedModelSerializer(TypedModelSerializer):
            model_serializer_mapping = mocker.MagicMock
            resource_type_field_name = 1

        with pytest.raises(ImproperlyConfigured) as excinfo:
            NotStringTypedModelSerializer()

        assert str(excinfo.value) == (
            '`NotStringTypedModelSerializer.resource_type_field_name` must '
            'be a string'
        )

    def test_each_serializer_has_context(self, mocker):
        context = mocker.MagicMock()
        serializer = BlogTypedModelSerializer(context=context)
        for inner_serializer in serializer.model_serializer_mapping.values():
            assert inner_serializer.context == context

    def test_serialize(self):
        instance = BlogOne.objects.create(name='blog', slug='blog', info='info')
        serializer = BlogTypedModelSerializer(instance)
        assert serializer.data == {
            'name': 'blog',
            'slug': 'blog',
            'info': 'info',
            'type': "tests.blogone",
        }

    def test_deserialize(self):
        data = {
            'name': 'blog',
            'slug': 'blog',
            'info': 'info',
            'type': 'tests.blogone',
        }
        serializers = BlogTypedModelSerializer(data=data)
        assert serializers.is_valid()
        assert serializers.data == data

    def test_deserialize_with_invalid_resourcetype(self):
        data = {
            'name': 'blog',
            'resourcetype': 'Invalid',
        }
        serializers = BlogTypedModelSerializer(data=data)
        assert not serializers.is_valid()

    def test_create(self):
        data = [
            {
                'name': 'b',
                'slug': 'b',
                'info': 'info',
                'type': 'tests.blogone',
            },
            {
                'name': 'c',
                'slug': 'c',
                'type': 'tests.blogtwo',
            },
        ]
        serializer = BlogTypedModelSerializer(data=data, many=True)
        assert serializer.is_valid()

        instances = serializer.save()
        assert len(instances) == 2
        assert [item.name for item in instances] == ['b', 'c']

        assert BlogBase.objects.count() == 2
        assert BlogTwo.objects.count() == 1
        assert BlogOne.objects.count() == 1

        assert serializer.data == data

    def test_update(self):
        instance = BlogOne.objects.create(name='blog', slug='blog', info='info')
        data = {
            'name': 'new-blog',
            'slug': 'blog',
            'type': 'tests.blogone',
        }

        serializer = BlogTypedModelSerializer(instance, data=data)
        assert serializer.is_valid()

        serializer.save()
        assert instance.name == 'new-blog'
        assert instance.slug == 'blog'

    def test_partial_update(self):
        instance = BlogOne.objects.create(name='blog', slug='blog', info='info')
        data = {
            'name': 'new-blog',
            'type': 'tests.blogone',
        }

        serializer = BlogTypedModelSerializer(
            instance, data=data, partial=True
        )
        assert serializer.is_valid()

        serializer.save()
        assert instance.name == 'new-blog'
        assert instance.slug == 'blog'

    def test_partial_update_without_resourcetype(self):
        instance = BlogOne.objects.create(name='blog', slug='blog', info='info')
        data = {'name': 'new-blog'}

        serializer = BlogTypedModelSerializer(
            instance, data=data, partial=True
        )
        assert serializer.is_valid()

        serializer.save()
        assert instance.name == 'new-blog'
        assert instance.slug == 'blog'

    def test_object_validators_are_applied(self):
        data = {
            'name': 'test-blog',
            'slug': 'test-blog-slug',
            'about': 'test-blog-about',
            'type': 'tests.blogthree',
        }
        serializer = BlogTypedModelSerializer(data=data)
        assert serializer.is_valid()
        serializer.save()


