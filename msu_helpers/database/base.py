#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.query import QuerySet


class SerializableModel(models.Model):

    _serializer = None

    class Meta:
        abstract = True

    @property
    def serialized(self) -> dict:
        return self.serializer.data

    @property
    def serializer(self):
        if self._serializer is None:
            self._serializer = self._get_serializer(self)
        return self._serializer

    @classmethod
    def _get_serializer(cls, data):
        from . import serializers
        serializer = serializers.get(cls.__name__)
        if isinstance(data, cls):
            return serializer(data)
        elif isinstance(data, dict):
            return serializer(data=data)
        else:
            raise TypeError(f'"data" should be dict or {cls.__name__}')

    @classmethod
    def deserialize(cls, data: dict):
        pk: int = data.get('id', 0)
        entry: cls = cls() if (pk <= 0 or not cls.exists(pk)) else cls.objects.get(pk=pk)
        attr_list: list = [attr for attr in dir(entry) if attr[0] != '_' and attr != 'id']

        for attr in attr_list:
            try:
                entry.__setattr__(
                    attr,
                    data.get(
                        attr,
                        entry.__getattribute__(attr)
                    )
                )
            except (TypeError, AttributeError):
                continue
            except Exception as e:
                print(f'An error occurred, during {cls.__name__} deserialization. {e}')

        return entry

    @classmethod
    def serialize_multiple(cls, data: QuerySet) -> dict:
        if not isinstance(data, QuerySet):
            raise TypeError(f'Invalid data type "{data.__class__.__name__}". '
                            f'It should be a {QuerySet.__name__} of {cls.__name__}s.')

        from . import serializers
        serializer_class = serializers.get(cls.__name__)
        serializer = serializer_class(data=data, many=True)

        if serializer.is_valid():
            return serializer.data

        raise ValueError(f'Invalid {cls.__name__} {QuerySet.__name__}. {serializer.errors}')

    @classmethod
    def exists(cls, pk: int):
        if pk is None or pk <= 0:
            raise ValueError('Invalid primary key')

        return cls.objects.filter(pk=pk).exists()
