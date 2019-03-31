from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0023_botusers_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botusers',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
