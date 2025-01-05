import random
from django.core.management.base import BaseCommand, CommandError
from voting.models import (
    Position,
    Candidate,
    Voter
)


class Command(BaseCommand):

    help = 'Populate the database with voter details'

    def handle(self, *args, **options):
        voters = []
        for i in range(100):
            program = random.choice(["F", "P"])
            level = random.choice(["ND", "HND"])
            year = random.choice(["21", "22", "23"])
            matric_number = f"{program}/{level}/{year}/34400{i}"
            ip_address = f"192.168.{random.randint(0, 255)}.{random.randint(1, 255)}"
            voter = Voter(
                matric_number=matric_number,
                ip_address=ip_address
            )
            voters.append(voter)
        Voter.objects.bulk_create(voters)
        self.stdout.write(self.style.SUCCESS('Successfully created voters'))
