import django.db.models.deletion
from django.db import migrations, models


def delete_bookings_without_trip(apps, schema_editor):
    Booking = apps.get_model("hotels", "Booking")
    Booking.objects.filter(trip__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0002_booking_trip"),
        ("planner", "0003_trip_user"),
    ]

    operations = [
        migrations.RunPython(delete_bookings_without_trip, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="booking",
            name="trip",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings",
                to="planner.trip",
            ),
        ),
    ]
