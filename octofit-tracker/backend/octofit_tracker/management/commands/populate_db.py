import logging
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId
from django.conf import settings
from pymongo import MongoClient

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        logging.debug('Starting database population script.')

        # Connect to MongoDB and clear collections
        logging.debug('Connecting to MongoDB and clearing collections.')
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboards.delete_many({})
        db.workouts.delete_many({})

        # Create users
        logging.debug('Creating users.')
        users = [
            User(email='thundergod@mhigh.edu', name='Thor', age=30),
            User(email='metalgeek@mhigh.edu', name='Tony Stark', age=45),
            User(email='zerocool@mhigh.edu', name='Steve Rogers', age=100),
            User(email='crashoverride@mhigh.edu', name='Natasha Romanoff', age=35),
            User(email='sleeptoken@mhigh.edu', name='Bruce Banner', age=40),
        ]
        
        # Save users individually to ensure primary keys are assigned
        for user in users:
            user.save()

        # Create teams
        logging.debug('Creating teams.')
        team1 = Team(name='Blue Team')
        team2 = Team(name='Gold Team')
        team1.save()
        team2.save()
        team1.members.set([users[0], users[1]])  # Use set() to assign members
        team2.members.set([users[2], users[3], users[4]])

        # Create activities
        logging.debug('Creating activities.')
        activities = [
            Activity(user=users[0], activity_type='Cycling', duration=60),
            Activity(user=users[1], activity_type='Crossfit', duration=120),
            Activity(user=users[2], activity_type='Running', duration=90),
            Activity(user=users[3], activity_type='Strength', duration=30),
            Activity(user=users[4], activity_type='Swimming', duration=75),
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        logging.debug('Creating leaderboard entries.')
        leaderboard_entries = [
            Leaderboard(team=team1, score=200),
            Leaderboard(team=team2, score=300),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        logging.debug('Creating workouts.')
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event'),
            Workout(name='Crossfit', description='Training for a crossfit competition'),
            Workout(name='Running Training', description='Training for a marathon'),
            Workout(name='Strength Training', description='Training for strength'),
            Workout(name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        logging.debug('Database population script completed successfully.')
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
