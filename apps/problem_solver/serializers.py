from rest_framework import serializers
from .models import Problem, Answer, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        ref_name = "ProblemSolverTag"


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Answer
        fields = "__all__"


class ProblemSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Problem
        fields = "__all__"