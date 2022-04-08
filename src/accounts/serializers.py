from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile, ExecutorOffer
from ..projects.models import WorkerSlot


class UserDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class ExecutorOfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutorOffer
        exclude = ('profile', 'id')


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    remote = serializers.CharField(source='get_remote_value')
    sex = serializers.CharField(source='get_sex_value')
    executor_offer = ExecutorOfferDetailSerializer()

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


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['old_password', 'new_password']

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ExecutorOfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutorOffer
        exclude = ('profile', 'id')


class ExecutorOfferListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutorOffer
        fields = '__all__'


class WorkerSlotListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerSlot
        fields = '__all__'
