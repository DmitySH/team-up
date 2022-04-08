from rest_framework import serializers

from src.projects.models import Project, WorkerSlot


class ProjectDetailSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(slug_field='id', many=True,
                                        read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ('owner', 'verified', 'id',)


class WorkerSlotUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = WorkerSlot
        exclude = ('project', 'profile')


class DeleteWorkerSlotSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)

    class Meta:
        model = WorkerSlot
        fields = ['id']


class ProjectListSerializer(serializers.ModelSerializer):
    required_belbin = serializers.SlugRelatedField(
        slug_field='role',
        many=True,
        read_only=True
    )
    required_specialization = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        read_only=True)
    online = serializers.CharField(source='get_remote_value')

    class Meta:
        model = Project
        fields = '__all__'
