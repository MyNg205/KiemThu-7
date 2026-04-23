from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hotel", "0003_userprofile_profile_completed"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="booking_group",
            field=models.CharField(blank=True, db_index=True, max_length=32),
        ),
        migrations.AddField(
            model_name="booking",
            name="guest_count",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="booking",
            name="special_request",
            field=models.TextField(blank=True),
        ),
    ]
