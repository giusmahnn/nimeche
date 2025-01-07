import random
from django.core.management.base import BaseCommand
from voting.models import Candidate, Position
from faker import Faker 


class Command(BaseCommand):
    help = 'Create a new candidate'

    def handle(self, *args, **options):
        fake=Faker()
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
        # position_names = list(Position.objects.values_list('name', flat=True)) # Get a list of position names
        all_positions = list(Position.objects.all())
        candidates = []
        for candidate_name in candidates_list:
            position = random.choice(all_positions)
            candidate = Candidate(
                name=candidate_name,
                introduction=f"My name is {candidate_name} and I am running for the position of {position.name}.",
                position=position,
                image=fake.image_url()
            )
            candidates.append(candidate)
        Candidate.objects.bulk_create(candidates)
        self.stdout.write(self.style.SUCCESS('Successfully created candidates'))