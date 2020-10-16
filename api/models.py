from django.db import models


class Simulation(models.Model):
    created = models.DateTimeField(auto_now_add=True)

