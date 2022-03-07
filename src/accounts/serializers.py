from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile, ExecutorOffer


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


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

    def update(self, instance, validated_data):
        user = instance.user

        for attr, value in validated_data.pop('user').items():
            setattr(user, attr, value)

        super(ProfileUpdateSerializer, self).update(instance, validated_data)
        instance.save()

        return instance


class ExecutorOfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutorOffer
        fields = '__all__'
        # exclude = ('profile',)
        extra_kwargs = {
            'profile': {
                'validators': [],
            },
        }

    def create(self, validated_data):
        offer, _ = ExecutorOffer.objects.update_or_create(
            profile=validated_data.get('profile'),
            defaults={'description': validated_data.get('description'),
                      'salary': validated_data.get('salary'),
                      'work_hours': validated_data.get('work_hours')})

        return offer
