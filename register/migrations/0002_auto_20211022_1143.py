import django.db.models.deletion
from django.db import migrations, models

import register.managers
import register.validators


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="register.user",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("register.user",),
            managers=[
                ("objects", register.managers.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name="user",
            name="cpf",
            field=models.CharField(
                blank=True,
                max_length=14,
                null=True,
                unique=True,
                validators=[register.validators.validate_CPF],
                verbose_name="CPF",
            ),
        ),
    ]
