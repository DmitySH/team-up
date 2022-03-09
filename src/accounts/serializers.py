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
        exclude = ('is_male', 'id')


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

        user.save()
        super(ProfileUpdateSerializer, self).update(instance, validated_data)
        instance.save()

        return instance


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

    def create(self, validated_data):
        profile = self.context['request'].user.profile
        offer, _ = ExecutorOffer.objects.update_or_create(
            profile=profile,
            defaults={'description': validated_data.get('description'),
                      'salary': validated_data.get('salary'),
                      'work_hours': validated_data.get('work_hours') or 40,
                      'profile': profile}
        )

        return offer


class ExecutorOfferListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutorOffer
        fields = '__all__'
