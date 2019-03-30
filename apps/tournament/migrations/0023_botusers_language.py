from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0022_add_motion_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='botusers',
            name='language',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='tournament.Language'
            ),
        ),
    ]
