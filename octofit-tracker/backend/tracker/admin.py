from django.contrib import admin
from tracker.models import Team, UserProfile, Activity, Leaderboard, Workout


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'team', 'total_workouts', 'total_calories_burned')
    search_fields = ('user__username', 'email')
    list_filter = ('team', 'created_at')
    ordering = ('-created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration', 'distance', 'calories', 'created_at')
    search_fields = ('user__username', 'activity_type')
    list_filter = ('activity_type', 'intensity', 'created_at')
    ordering = ('-created_at',)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'rank', 'total_points', 'total_activities', 'team')
    search_fields = ('user__username',)
    list_filter = ('team', 'rank')
    ordering = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'duration', 'calories_burned_estimate', 'created_at')
    search_fields = ('name',)
    list_filter = ('difficulty', 'created_at')
    ordering = ('-created_at',)
