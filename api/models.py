from django.db import models
from django.contrib.gis.db import models as gis_models


from django.contrib.gis.db import models

class Trail(models.Model):
    object_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=8000, null=True, blank=True)
    county = models.CharField(max_length=130, null=True, blank=True)
    activity = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    website = models.URLField(max_length=8000, null=True, blank=True)
    length_km = models.FloatField(null=True, blank=True)
    difficulty = models.CharField(max_length=1000, null=True, blank=True)
    trail_type = models.CharField(max_length=1000, null=True, blank=True)
    ascent_metres = models.CharField(max_length=1000, null=True, blank=True)
    start_point = models.CharField(max_length=1000, null=True, blank=True)
    finish_point = models.CharField(max_length=1000, null=True, blank=True)
    nearest_town_start = models.CharField(max_length=1000, null=True, blank=True)
    nearest_town_finish = models.CharField(max_length=1000, null=True, blank=True)
    public_transport = models.CharField(max_length=1000, null=True, blank=True)
    dogs_allowed = models.CharField(max_length=256, null=True, blank=True)
    management_organisation = models.CharField(max_length=1000, null=True, blank=True)
    location = models.PointField(geography=True, null=True, blank=True)
    route = models.LineStringField(geography=True)

    def __str__(self):
        return self.name or f"Trail {self.object_id}"


class TrailSegment(models.Model):
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, related_name='segments')
    segment_index = models.IntegerField()
    start_time_offset = models.DurationField()
    start_distance_km = models.FloatField()
    end_distance_km = models.FloatField()
    segment_point = models.PointField(geography=True)
    segment_line = models.LineStringField(geography=True)

    def __str__(self):
        return f"{self.trail} - Segment {self.segment_index}"


class WeatherAlert(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MODERATE', 'Moderate'),
        ('SEVERE', 'Severe'),
        ('EXTREME', 'Extreme')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    location = models.PointField(geography=True)
    radius_km = models.FloatField()  # Affected radius in kilometers
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class UserWeatherAlert(models.Model):
    CONDITION_CHOICES = [
        ('SUNNY', 'Sunny (Low cloudiness)'),
        ('RAINY', 'Rainy (Precipitation)'),
        ('WINDY', 'Windy (High wind speed)'),
        ('HOT', 'Hot temperature'),
        ('COLD', 'Cold temperature')
    ]
    
    COMPARISON_CHOICES = [
        ('GT', 'Greater than'),
        ('LT', 'Less than'),
        ('EQ', 'Equal to')
    ]
    
    name = models.CharField(max_length=100)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    threshold = models.FloatField(help_text="Threshold value for the condition")
    comparison = models.CharField(max_length=2, choices=COMPARISON_CHOICES, default='GT')
    active = models.BooleanField(default=True)
    location = models.PointField(geography=True, null=True, blank=True)
    
    def __str__(self):
        comparison_display = {
            'GT': 'greater than',
            'LT': 'less than',
            'EQ': 'equal to'
        }
        return f"{self.name}: Alert when {self.get_condition_display()} is {comparison_display[self.comparison]} {self.threshold}"