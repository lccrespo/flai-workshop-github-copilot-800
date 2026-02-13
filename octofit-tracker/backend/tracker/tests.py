from django.test import TestCase
from django.contrib.auth.models import User
from tracker.models import Team, UserProfile, Activity, Leaderboard, Workout
from rest_framework.test import APITestCase
from rest_framework import status


class TeamModelTest(TestCase):
    """Test Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Team Marvel',
            description='Marvel superheroes team'
        )
    
    def test_team_creation(self):
        """Test team can be created"""
        self.assertEqual(self.team.name, 'Team Marvel')
        self.assertIsNotNone(self.team.created_at)
    
    def test_team_string_representation(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Team Marvel')


class UserProfileModelTest(TestCase):
    """Test UserProfile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='ironman',
            email='ironman@marvel.com',
            password='testpass123'
        )
        self.team = Team.objects.create(name='Team Marvel')
        self.profile = UserProfile.objects.create(
            user=self.user,
            email=self.user.email,
            team=self.team,
            bio='Genius billionaire philanthropist'
        )
    
    def test_profile_creation(self):
        """Test user profile can be created"""
        self.assertEqual(self.profile.email, 'ironman@marvel.com')
        self.assertEqual(self.profile.team.name, 'Team Marvel')
    
    def test_profile_string_representation(self):
        """Test profile string representation"""
        self.assertEqual(str(self.profile), 'ironman')


class ActivityModelTest(TestCase):
    """Test Activity model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='ironman',
            email='ironman@marvel.com'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30,
            distance=5.0,
            calories=300,
            intensity='high'
        )
    
    def test_activity_creation(self):
        """Test activity can be created"""
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.calories, 300)
    
    def test_activity_string_representation(self):
        """Test activity string representation"""
        self.assertIn('ironman', str(self.activity))
        self.assertIn('running', str(self.activity))


class LeaderboardModelTest(TestCase):
    """Test Leaderboard model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='ironman',
            email='ironman@marvel.com'
        )
        self.team = Team.objects.create(name='Team Marvel')
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            rank=1,
            total_points=10000,
            total_activities=50,
            team=self.team
        )
    
    def test_leaderboard_creation(self):
        """Test leaderboard entry can be created"""
        self.assertEqual(self.leaderboard.rank, 1)
        self.assertEqual(self.leaderboard.total_points, 10000)
    
    def test_leaderboard_string_representation(self):
        """Test leaderboard string representation"""
        self.assertIn('ironman', str(self.leaderboard))
        self.assertIn('Rank: 1', str(self.leaderboard))


class WorkoutModelTest(TestCase):
    """Test Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Superhero Strength Training',
            description='Build incredible strength',
            difficulty='advanced',
            duration=90,
            exercises=['Bench Press', 'Squats', 'Deadlifts'],
            target_muscle_groups=['Chest', 'Legs', 'Back'],
            calories_burned_estimate=600
        )
    
    def test_workout_creation(self):
        """Test workout can be created"""
        self.assertEqual(self.workout.name, 'Superhero Strength Training')
        self.assertEqual(self.workout.difficulty, 'advanced')
    
    def test_workout_string_representation(self):
        """Test workout string representation"""
        self.assertEqual(str(self.workout), 'Superhero Strength Training')


class TeamAPITest(APITestCase):
    """Test Team API endpoints"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Team Marvel',
            description='Marvel superheroes'
        )
    
    def test_get_teams(self):
        """Test getting all teams"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_create_team(self):
        """Test creating a new team"""
        data = {
            'name': 'Team DC',
            'description': 'DC superheroes'
        }
        response = self.client.post('/api/teams/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserAPITest(APITestCase):
    """Test User API endpoints"""
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        data = {
            'username': 'batman',
            'email': 'batman@dc.com',
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'password': 'darknight2024'
        }
        response = self.client.post('/api/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ActivityAPITest(APITestCase):
    """Test Activity API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='ironman',
            email='ironman@marvel.com'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30,
            distance=5.0,
            calories=300,
            intensity='high'
        )
    
    def test_get_activities(self):
        """Test getting all activities"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_activities_by_user(self):
        """Test getting activities by user"""
        response = self.client.get(f'/api/activities/by_user/?user_id={self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    """Test Leaderboard API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='ironman',
            email='ironman@marvel.com'
        )
        self.team = Team.objects.create(name='Team Marvel')
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            rank=1,
            total_points=10000,
            total_activities=50,
            team=self.team
        )
    
    def test_get_rankings(self):
        """Test getting global rankings"""
        response = self.client.get('/api/leaderboards/rankings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    """Test Workout API endpoints"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Superhero Strength Training',
            description='Build strength',
            difficulty='advanced',
            duration=90,
            exercises=['Bench Press', 'Squats'],
            target_muscle_groups=['Chest', 'Legs'],
            calories_burned_estimate=600
        )
    
    def test_get_workouts(self):
        """Test getting all workouts"""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_workouts_by_difficulty(self):
        """Test getting workouts by difficulty"""
        response = self.client.get('/api/workouts/by_difficulty/?difficulty=advanced')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
