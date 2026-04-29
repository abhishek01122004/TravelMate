from django.db import models
from django.utils.text import slugify


class Destination(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    description = models.TextField()
    best_time = models.CharField(max_length=100)
    cover_image = models.ImageField(
        upload_to="destinations/covers/",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base = slugify(self.name) or "destination"
        slug = base
        counter = 1
        qs = Destination.objects.all()
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        while qs.filter(slug=slug).exists():
            slug = f"{base}-{counter}"
            counter += 1
        return slug

    def __str__(self):
        return self.name


class Attraction(models.Model):
    PRIORITY_CHOICES = [
        (1, "1 - Low"),
        (2, "2"),
        (3, "3 - Medium"),
        (4, "4"),
        (5, "5 - High"),
    ]

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="attractions",
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    estimated_time = models.FloatField(default=1.0)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)
    approx_cost = models.IntegerField(default=0)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.destination.name})"
