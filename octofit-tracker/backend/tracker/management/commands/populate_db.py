from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Team, UserProfile, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        self.stdout.write('Deleting existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='The mighty superheroes team with extraordinary powers'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='The justice seekers dedicated to protecting the world'
        )

        # Create superheroes
        self.stdout.write('Creating superheroes...')
        superheroes = [
            {
                'username': 'ironman',
                'email': 'ironman@marvel.com',
                'first_name': 'Tony',
                'last_name': 'Stark',
                'team': team_marvel,
                'bio': 'Genius billionaire philanthropist'
            },
            {
                'username': 'captainamerica',
                'email': 'captainamerica@marvel.com',
                'first_name': 'Steve',
                'last_name': 'Rogers',
                'team': team_marvel,
                'bio': 'The first Avenger'
            },
            {
                'username': 'thor',
                'email': 'thor@marvel.com',
                'first_name': 'Thor',
                'last_name': 'Odinson',
                'team': team_marvel,
                'bio': 'God of Thunder'
            },
            {
                'username': 'blackwidow',
                'email': 'blackwidow@marvel.com',
                'first_name': 'Natasha',
                'last_name': 'Romanoff',
                'team': team_marvel,
                'bio': 'Master spy and assassin'
            },
            {
                'username': 'hawkeye',
                'email': 'hawkeye@marvel.com',
                'first_name': 'Clint',
                'last_name': 'Barton',
                'team': team_marvel,
                'bio': 'Perfect archer and marksman'
            },
            {
                'username': 'batman',
                'email': 'batman@dc.com',
                'first_name': 'Bruce',
                'last_name': 'Wayne',
                'team': team_dc,
                'bio': 'The Dark Knight of Gotham'
            },
            {
                'username': 'superman',
                'email': 'superman@dc.com',
                'first_name': 'Clark',
                'last_name': 'Kent',
                'team': team_dc,
                'bio': 'Man of Steel'
            },
            {
                'username': 'wonderwoman',
                'email': 'wonderwoman@dc.com',
                'first_name': 'Diana',
                'last_name': 'Prince',
                'team': team_dc,
                'bio': 'Amazon warrior princess'
            },
            {
                'username': 'flash',
                'email': 'flash@dc.com',
                'first_name': 'Barry',
                'last_name': 'Allen',
                'team': team_dc,
                'bio': 'The fastest man alive'
            },
            {
                'username': 'aquaman',
                'email': 'aquaman@dc.com',
                'first_name': 'Arthur',
                'last_name': 'Curry',
                'team': team_dc,
                'bio': 'King of the Seas'
            },
        ]

        users = []
        for hero in superheroes:
            user = User.objects.create_user(
                username=hero['username'],
                email=hero['email'],
                first_name=hero['first_name'],
                last_name=hero['last_name'],
                password='superhero123'
            )
            users.append(user)

            # Create user profile
            UserProfile.objects.create(
                user=user,
                email=hero['email'],
                team=hero['team'],
                bio=hero['bio'],
                total_calories_burned=random.randint(5000, 20000),
                total_distance=random.randint(50, 500),
                total_workouts=random.randint(10, 100)
            )

            # Create leaderboard entry
            Leaderboard.objects.create(
                user=user,
                rank=0,
                total_points=random.randint(1000, 10000),
                total_activities=random.randint(10, 100),
                team=hero['team']
            )

        # Create activities for each user
        self.stdout.write('Creating activities...')
        activity_types = ['running', 'cycling', 'swimming', 'walking', 'gym', 'yoga']
        intensities = ['low', 'medium', 'high']

        for user in users:
            for _ in range(random.randint(5, 15)):
                Activity.objects.create(
                    user=user,
                    activity_type=random.choice(activity_types),
                    duration=random.randint(20, 120),
                    distance=round(random.uniform(1, 20), 2),
                    calories=random.randint(100, 800),
                    intensity=random.choice(intensities),
                    notes='Great workout session!'
                )

        # Create sample workouts
        self.stdout.write('Creating workouts...')
        workouts_data = [
            {
                'name': 'Superhero Strength Training',
                'description': 'Build incredible strength like superheroes',
                'difficulty': 'advanced',
                'duration': 90,
                'exercises': ['Bench Press', 'Squats', 'Deadlifts', 'Pull-ups'],
                'target_muscle_groups': ['Chest', 'Legs', 'Back', 'Arms'],
                'calories_burned_estimate': 600
            },
            {
                'name': 'Marvel Cardio Challenge',
                'description': 'Fast-paced cardio workout for endurance',
                'difficulty': 'intermediate',
                'duration': 60,
                'exercises': ['Running', 'Jump Rope', 'Burpees', 'Mountain Climbers'],
                'target_muscle_groups': ['Cardio', 'Core', 'Legs'],
                'calories_burned_estimate': 500
            },
            {
                'name': 'DC Justice League Yoga',
                'description': 'Flexible and peaceful yoga for balance',
                'difficulty': 'beginner',
                'duration': 45,
                'exercises': ['Sun Salutation', 'Warrior Pose', 'Tree Pose', 'Savasana'],
                'target_muscle_groups': ['Full Body', 'Flexibility', 'Mind'],
                'calories_burned_estimate': 200
            },
            {
                'name': 'Quick Morning Stretch',
                'description': 'Begin your day with energizing stretches',
                'difficulty': 'beginner',
                'duration': 20,
                'exercises': ['Neck Stretches', 'Shoulder Rolls', 'Hamstring Stretch', 'Chest Stretch'],
                'target_muscle_groups': ['Full Body'],
                'calories_burned_estimate': 50
            },
            {
                'name': 'Intense Crossfit Session',
                'description': 'High-intensity interval training for athletes',
                'difficulty': 'advanced',
                'duration': 60,
                'exercises': ['Kettlebell Swings', 'Box Jumps', 'Wall Balls', 'Rowing Machine'],
                'target_muscle_groups': ['Full Body', 'Cardio'],
                'calories_burned_estimate': 700
            },
        ]

        for workout_data in workouts_data:
            Workout.objects.create(**workout_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data!'))
        self.stdout.write(f'Created {len(users)} superheroes across 2 teams')
        self.stdout.write(f'Created {Team.objects.count()} teams')
        self.stdout.write(f'Created {Activity.objects.count()} activities')
        self.stdout.write(f'Created {Workout.objects.count()} workouts')
