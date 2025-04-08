from djongo import models

class User(models.Model):
    _id = models.ObjectIdField(primary_key=True)  # Use ObjectIdField for MongoDB compatibility
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()

    def __str__(self):
        return self.name

class Team(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    members = models.ManyToManyField('User')  # Changed from ArrayField to ManyToManyField

    def __str__(self):
        return self.name

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.activity_type}"

class Leaderboard(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.team.name} - {self.score}"

class Workout(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
