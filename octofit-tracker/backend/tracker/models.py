from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    """Team model for grouping users"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extended user profile with fitness data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    bio = models.TextField(blank=True)
    profile_picture = models.URLField(blank=True)
    total_calories_burned = models.FloatField(default=0.0)
    total_distance = models.FloatField(default=0.0)
    total_workouts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.user.username


class Activity(models.Model):
    """User activity model"""
    ACTIVITY_TYPES = (
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('gym', 'Gym'),
        ('yoga', 'Yoga'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration = models.IntegerField()  # in minutes
    distance = models.FloatField()  # in kilometers
    calories = models.FloatField()
    intensity = models.CharField(max_length=20, choices=(('low', 'Low'), ('medium', 'Medium'), ('high', 'High')))
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.created_at}"


class Leaderboard(models.Model):
    """Leaderboard model for tracking rankings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard')
    rank = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='leaderboards')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboards'
        ordering = ['-total_points']

    def __str__(self):
        return f"{self.user.username} - Rank: {self.rank}"


class Workout(models.Model):
    """Workout plan model"""
    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration = models.IntegerField()  # in minutes
    exercises = models.JSONField(default=list)  # list of exercises
    target_muscle_groups = models.JSONField(default=list)  # list of target muscles
    calories_burned_estimate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name
