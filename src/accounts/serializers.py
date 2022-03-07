from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    remote = serializers.CharField(source='get_remote_value')
    sex = serializers.CharField(source='get_sex_value')
    belbin = serializers.SlugRelatedField(slug_field='role', many=True,
                                          read_only=True)
    mbti = serializers.SlugRelatedField(slug_field='role', many=True,
                                        read_only=True)
    lsq = serializers.SlugRelatedField(slug_field='role', many=True,
                                       read_only=True)
    specialization = serializers.SlugRelatedField(slug_field='name',
                                                  many=True,
                                                  read_only=True)

    class Meta:
        model = Profile
        exclude = ('is_male',)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    photo = serializers.CharField()
    cv = serializers.CharField()

    class Meta:
        model = Profile
        fields = (
            'remote', 'is_male', 'specialization', 'patronymic', 'city',
            'age', 'description', 'user', 'photo', 'cv'
        )

    def update(self, instance, validated_data):
        user = instance.user

        for attr, value in validated_data.pop('user').items():
            setattr(user, attr, value)

        super(ProfileUpdateSerializer, self).update(instance, validated_data)
        instance.save()

        return instance
