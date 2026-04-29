from django.db import migrations, models
from django.utils.text import slugify


def fill_destination_slugs(apps, schema_editor):
    Destination = apps.get_model("destinations", "Destination")
    for d in Destination.objects.all():
        base = slugify(d.name) or "destination"
        slug = base
        n = 1
        while Destination.objects.filter(slug=slug).exclude(pk=d.pk).exists():
            slug = f"{base}-{n}"
            n += 1
        d.slug = slug
        d.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("destinations", "0006_rename_ticket_price_attraction_approx_cost"),
    ]

    operations = [
        migrations.AddField(
            model_name="destination",
            name="slug",
            field=models.SlugField(blank=True, max_length=220, null=True),
        ),
        migrations.AddField(
            model_name="destination",
            name="cover_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="destinations/covers/"
            ),
        ),
        migrations.RunPython(fill_destination_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="destination",
            name="slug",
            field=models.SlugField(db_index=True, max_length=220, unique=True),
        ),
    ]
