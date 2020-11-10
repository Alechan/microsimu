from django.contrib.auth import get_user_model
from django.core.management import CommandError, BaseCommand


class Command(BaseCommand):
    help = 'Crate a superuser, and allow password to be provided'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def add_arguments(self, parser):
        parser.add_argument(
            '--username', dest='username', default=None,
            help='Specifies the user name for the user.', required=True
        )
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the user.', required=True
        )

    def handle(self, *args, **options):
        password = options.get('password')
        username = options.get('username')

        user = self.UserModel(username=username)
        user.set_password(password)
        user.save()
