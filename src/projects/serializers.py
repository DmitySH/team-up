from rest_framework import serializers

from src.projects.models import Project, WorkerSlot


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializes project model.
    """

    team = serializers.SlugRelatedField(slug_field='id', many=True,
                                        read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectUpdateSerializer(serializers.ModelSerializer):
    """
    Serializes fields to update in project model.
    """

    title = serializers.CharField()

    class Meta:
        model = Project
        exclude = ('owner', 'verified', 'id',)


class WorkerSlotUpdateSerializer(serializers.ModelSerializer):
    """
    Serializes fields to update in worker slot.
    """

    id = serializers.IntegerField(required=False)

    class Meta:
        model = WorkerSlot
        exclude = ('project', 'profile')


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializes list of all projects.
    """

    required_belbin = serializers.SlugRelatedField(
        slug_field='role',
        many=True,
        read_only=True
    )
    required_specialization = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        read_only=True)

    online = serializers.CharField(source='remote_value')
    owner = serializers.CharField(source='owner.user.username')

    class Meta:
        model = Project
        fields = '__all__'
