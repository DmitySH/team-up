from rest_framework import serializers

from src.tests.models import BelbinTest, MBTITest, LSQTest


class BelbinTestListSerializer(serializers.ModelSerializer):
    """
    Serializes list of all belin test roles.
    """

    class Meta:
        model = BelbinTest
        fields = '__all__'


class MBTITestListSerializer(serializers.ModelSerializer):
    """
    Serializes list of all mbti test roles.
    """

    class Meta:
        model = MBTITest
        fields = '__all__'


class LSQTestListSerializer(serializers.ModelSerializer):
    """
    Serializes list of all lsq test roles.
    """

    class Meta:
        model = LSQTest
        fields = '__all__'
