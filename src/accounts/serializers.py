from django.contrib.auth.models import User
from drf_base64.fields import Base64FileField, Base64ImageField
from rest_framework import serializers

from .models import Profile, ExecutorOffer, Specialization
from ..projects.models import WorkerSlot


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializes user model.
    """

    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ExecutorOfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializes executor's offer model.
    """

    class Meta:
        model = ExecutorOffer
        exclude = ('profile', 'id')


class ProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializes profile model.
    """

    user = UserDetailSerializer()
    remote = serializers.CharField(source='remote_value')
    sex = serializers.CharField(source='sex_value')
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
    project = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = Profile
        exclude = ('is_male',)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializes data to update profile model.
    """
    cv = Base64FileField(required=False)
    photo = Base64ImageField(required=False)
    user = UserDetailSerializer()

    class Meta:
        model = Profile
        fields = (
            'remote', 'is_male', 'specialization', 'patronymic', 'city',
            'age', 'description', 'user', 'photo', 'cv'
        )


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializes changed password.
    """

    class Meta:
        model = User
        fields = ['old_password', 'new_password']

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ExecutorOfferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializes executor offer model.
    """

    class Meta:
        model = ExecutorOffer
        exclude = ('profile', 'id')


class ExecutorOfferListSerializer(serializers.ModelSerializer):
    """
    Serializes list of all executor offers.
    """

    profile = serializers.CharField(source='profile.user.username')

    class Meta:
        model = ExecutorOffer
        fields = '__all__'


class WorkerSlotListSerializer(serializers.ModelSerializer):
    """
    Serializes list of all worker slots.
    """

    class Meta:
        model = WorkerSlot
        fields = '__all__'


class SpecializationListSerializer(serializers.ModelSerializer):
    """
    Serializes list of all specializations.
    """

    class Meta:
        model = Specialization
        fields = '__all__'
