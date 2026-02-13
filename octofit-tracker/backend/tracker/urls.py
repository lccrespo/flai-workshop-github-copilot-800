from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracker.views import (
    TeamViewSet, UserViewSet, UserProfileViewSet, ActivityViewSet,
    LeaderboardViewSet, WorkoutViewSet
)

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboards', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')

urlpatterns = [
    path('', include(router.urls)),
]
