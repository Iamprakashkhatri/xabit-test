import os

from django.core.management.base import BaseCommand

# from django.contrib.auth.models import User
from user.models import User



class Command(BaseCommand):
    help = 'Populate the database with some default values'


    def add_arguments(self, parser):
        pass


    def handle(self, *args, **options):
        file_path = os.path.dirname(os.path.abspath(__file__))

        # Create the first super user
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(username="xabit",
                                                    password='admin',
                                                    # email="admin@xabit.com",
                                                    first_name="Admin",
                                                    last_name="admin"
                                                )

# class Command(BaseCommand):
#     help = 'Displays current time'

#     def handle(self, *args, **kwargs):
#         time = timezone.now().strftime('%X')
#         self.stdout.write("It's now %s" % time)