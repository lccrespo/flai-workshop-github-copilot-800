from rest_framework import serializers
from django.contrib.auth.models import User
from tracker.models import Team, UserProfile, Activity, Leaderboard, Workout


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'email', 'team', 'team_name', 'bio', 'profile_picture', 
                  'total_calories_burned', 'total_distance', 'total_workouts', 'created_at', 'updated_at')


class ActivitySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Activity
        fields = ('id', 'user', 'username', 'activity_type', 'duration', 'distance', 
                  'calories', 'intensity', 'notes', 'created_at', 'updated_at')


class LeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Leaderboard
        fields = ('id', 'user', 'username', 'rank', 'total_points', 'total_activities', 
                  'team', 'team_name', 'updated_at')


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'
