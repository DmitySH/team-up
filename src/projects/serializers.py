from rest_framework import serializers

from src.projects.models import Project


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
