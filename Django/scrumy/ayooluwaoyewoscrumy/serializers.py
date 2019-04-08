from rest_framework import serializers
from .models import User, ScrumyGoals, ScrumyUser

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username']

class ScrumGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrumyGoals
        fields = ('visible', 'goal_id', 'goal_name', 'goal_status')

class ScrumUserSerializer(serializers.ModelSerializer):
    scrumygoals_set = ScrumGoalSerializer(many=True)
    class Meta:
        model = ScrumyUser
        fields = ('id', 'nickname', 'scrumygoals_set')
    
    




