from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from tracker.models import Team, UserProfile, Activity, Leaderboard, Workout
from tracker.serializers import (
    TeamSerializer, UserProfileSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer, UserSerializer
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Register a new user"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data.get('email'),
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', '')
            )
            user.set_password(request.data.get('password'))
            user.save()
            
            # Create user profile
            UserProfile.objects.create(user=user, email=user.email)
            
            # Create leaderboard entry
            Leaderboard.objects.create(user=user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get all user profiles by team"""
        team_id = request.query_params.get('team_id')
        if team_id:
            profiles = UserProfile.objects.filter(team_id=team_id)
            serializer = self.get_serializer(profiles, many=True)
            return Response(serializer.data)
        return Response({'error': 'team_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get all activities for a specific user"""
        user_id = request.query_params.get('user_id')
        if user_id:
            activities = Activity.objects.filter(user_id=user_id)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'user_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get all activities of a specific type"""
        activity_type = request.query_params.get('type')
        if activity_type:
            activities = Activity.objects.filter(activity_type=activity_type)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'type parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def rankings(self, request):
        """Get global rankings"""
        leaderboards = Leaderboard.objects.all().order_by('-total_points')
        serializer = self.get_serializer(leaderboards, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get rankings by team"""
        team_id = request.query_params.get('team_id')
        if team_id:
            leaderboards = Leaderboard.objects.filter(team_id=team_id).order_by('-total_points')
            serializer = self.get_serializer(leaderboards, many=True)
            return Response(serializer.data)
        return Response({'error': 'team_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts by difficulty level"""
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            workouts = Workout.objects.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'difficulty parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        """Get personalized workout recommendations"""
        difficulty = request.query_params.get('difficulty', 'beginner')
        workouts = Workout.objects.filter(difficulty=difficulty)
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)
