from django.db import migrations

import register.managers


class Migration(migrations.Migration):

    dependencies = [
        ("admin", "0003_logentry_add_action_flag_choices"),
        ("authtoken", "0003_tokenproxy"),
        ("company", "0003_auto_20211022_1143"),
        ("register", "0002_auto_20211022_1143"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Client",
        ),
        migrations.CreateModel(
            name="Client",
            fields=[],
            options={
                "verbose_name": "Client",
                "verbose_name_plural": "Clients",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("register.user",),
            managers=[
                ("objects", register.managers.UserManager()),
            ],
        ),
    ]
