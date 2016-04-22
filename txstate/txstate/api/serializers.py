#!/usr/bin/env python
from rest_framework import serializers
from .models import Droplet
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):

    droplets = DropletSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'droplets')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)


class DropletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Droplet
        fields = ('drop_id', 'owner', 'latitude', 'longitude', 'data')
