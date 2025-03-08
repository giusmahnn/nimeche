import csv
import random
from django.core.management.base import BaseCommand
import requests
from voting.models import Candidate, Position
from faker import Faker  # type: ignore
from django.core.files.base import ContentFile

from nimeche.settings.base import BASE_DIR


# class Command(BaseCommand):
#     help = 'Create a new candidate'

#     def handle(self, *args, **options):
#         fake=Faker()
#         candidates_list = [
#             "Emeka Nwosu",
#             "Fatima Yusuf",
#             "Chinedu Okafor",
#             "Oluwaseun Adeola",
#             "Ngozi Eze",
#             "Ibrahim Mohammed",
#             "Ifeoma Ndukwe",
#             "Uchechi Ibe",
#             "Chukwuemeka Onwukwe",
#             "Zainab Ibrahim",
#             "Kelechi Abara",
#             "Blessing Okwuosa",
#             "Olaniyi Ayodele",
#             "Precious Adebayo",
#             "Adaobi Nnamdi",
#             "Tobi Amusa",
#             "Chimezie Ezeh",
#             "Nneka Ugochukwu",
#             "Tolu Ajayi",
#             "Amara Ikemefuna",
#             "Seyi Shyllon",
#             "Joy Ogbonna",
#             "Nnamdi Madu",
#             "Funke Soetan",
#             "Ayo Alabi",
#             "Kehinde Bakare",
#             "Chidi Orji",
#             "Temitope Fadeyi",
#         ]
#         # position_names = list(Position.objects.values_list('name', flat=True)) # Get a list of position names
#         all_positions = list(Position.objects.all())
#         candidates = []
#         for candidate_name in candidates_list:
#             position = random.choice(all_positions)
#             candidate = Candidate(
#                 name=candidate_name,
#                 introduction=f"My name is {candidate_name} and I am running for the position of {position.name}.",
#                 position=position,
#                 image=fake.image_url()
#             )
#             candidates.append(candidate)
#         Candidate.objects.bulk_create(candidates)
#         self.stdout.write(self.style.SUCCESS('Successfully created candidates'))


def convert_google_drive_url(url):
    if "drive.google.com" in url:
        file_id = url.split("id=")[-1]
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    return url

class Command(BaseCommand):
    help = 'Seed the database with candidates from a CSV file'

    def handle(self, *args, **kwargs):
        file_path = BASE_DIR / 'candidates.csv'  # Update this path to the actual location of your CSV file

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                position_name = row['position']
                position, created = Position.objects.get_or_create(name=position_name)

                image_url = convert_google_drive_url(row['image'])
                image_name = f"{row['name'].replace(' ', '_')}.jpg"  # Create a filename from the name column

                candidate = Candidate(
                    name=row['name'],
                    introduction=row['introduction'],
                    position=position
                )

                # Download the image and save it locally
                if image_url:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        candidate.image.save(image_name, ContentFile(response.content), save=False)

                candidate.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with candidates'))