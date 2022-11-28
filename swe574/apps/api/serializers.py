from rest_framework import serializers
from learning_space.models import LearningSpace


class LearningSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningSpace
        fields = '__all__'
