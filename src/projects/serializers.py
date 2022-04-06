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

    def create(self, validated_data):
        profile = self.context['request'].user.profile
        project, _ = Project.objects.update_or_create(
            owner=profile,
            defaults={'description': validated_data.get('description'),
                      'title': validated_data.get('title'),
                      'vacant': validated_data.get('vacant'),
                      'owner': profile,
                      'city': validated_data.get('city') or '',
                      'online': validated_data.get('online'),
                      }
        )

        project.required_specialization.set(validated_data.get(
            'required_specialization'))
        project.required_belbin.set(validated_data.get('required_belbin'))

        return project


class WorkerSlotUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = WorkerSlot
        exclude = ('project', 'profile')

    def create(self, validated_data):
        profile = self.context['request'].user.profile

        slot, _ = WorkerSlot.objects.update_or_create(
            project=profile.project(),
            id=validated_data.get('id'),

            defaults={'description': validated_data.get('description'),
                      'salary': validated_data.get('salary'),
                      'work_hours': validated_data.get('work_hours') or 40,
                      }
        )

        slot.specialization.set(validated_data.get(
            'specialization'))
        slot.role.set(validated_data.get('role'))

        return slot


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


class InviteSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    slot_id = serializers.IntegerField()
    username = serializers.SlugField()
