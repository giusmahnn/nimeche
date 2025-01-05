import random
from django.core.management.base import BaseCommand, CommandError
from voting.models import (
    Position,
    Candidate,
    Voter
)


class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **options):
        positions_list = [
            "President",
            "Vice President 1",
            "Vice President 2",
            "General Secretary",
            "Assistant General Secretary",
            "Financial Secretary",
            "Public Relations Officer 1",
            "Public Relations Officer 2",
            "Technical Secretary 1",
            "Technical Secretary 2",
            "Welfare Director 1",
            "Welfare Director 2",
            "Social Director 1",
            "Social Director 2",
        ]

        positions = []
        for position_name in positions_list:
            position = Position(
                name=position_name,
                description=f"This is the office of the {position_name}"
            )
            positions.append(position)
        Position.objects.bulk_create(positions)
        self.stdout.write(self.style.SUCCESS('Successfully created positions'))

        candidates_list = [
            "Emeka Nwosu",
            "Fatima Yusuf",
            "Chinedu Okafor",
            "Oluwaseun Adeola",
            "Ngozi Eze",
            "Ibrahim Mohammed",
            "Ifeoma Ndukwe",
            "Uchechi Ibe",
            "Chukwuemeka Onwukwe",
            "Zainab Ibrahim",
            "Kelechi Abara",
            "Blessing Okwuosa",
            "Olaniyi Ayodele",
            "Precious Adebayo",
            "Adaobi Nnamdi",
            "Tobi Amusa",
            "Chimezie Ezeh",
            "Nneka Ugochukwu",
            "Tolu Ajayi",
            "Amara Ikemefuna",
            "Seyi Shyllon",
            "Joy Ogbonna",
            "Nnamdi Madu",
            "Funke Soetan",
            "Ayo Alabi",
            "Kehinde Bakare",
            "Chidi Orji",
            "Temitope Fadeyi",
        ]
        all_positions = list(Position.objects.all())
        candidates = []
        for candidate_name in candidates_list:
            candidate = Candidate(
                name=candidate_name,
                introduction=f"My name is {candidate_name} and I am running for the position of {random.choice(all_positions)}.",
                position=random.choice(all_positions)
            )
            candidates.append(candidate)
        Candidate.objects.bulk_create(candidates)
        self.stdout.write(self.style.SUCCESS('Successfully created candidates'))

        voters = []
        for i in range(300):
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

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with initial data'))