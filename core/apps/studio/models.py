from django.db import models

from core.apps.common.models import User

class Problem(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class Challenge(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.problem.name

class SubmissionLangConfig(models.Model):
    id = models.AutoField()
    version = models.IntegerField()

    LANGUAGE_CHOICES = (
        ("PY", "Python"),
        ("JS", "JavaScript"),
        ("JAVA", "Java"),
        ("CPP", "C++"),
    )
    language = models.TextField(choices=LANGUAGE_CHOICES)
    function_signature = models.CharField(max_length=100)

    class Meta:
        unique_together = ("id", "version")
