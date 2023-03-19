from django.core.management.base import BaseCommand, CommandError
import app_users.management.commands.builder


class Command(BaseCommand):
    help = "creates fake data"

    def add_arguments(self, parser):
        parser.add_argument(
            "total", type=int, help="Indicates the number of users to be created"
        )

    def handle(self, *args, **kwargs):
        num_user = kwargs["total"]
        app_users.management.commands.builder.run(num_user)
