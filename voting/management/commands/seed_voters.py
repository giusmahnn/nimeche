import random
import csv
from django.core.management.base import BaseCommand
from voting.models import (
    Voter
)
from nimeche.settings.base import BASE_DIR



# class Command(BaseCommand):

#     help = 'Populate the database with voter details'

#     def handle(self, *args, **options):
#         voters = []
#         for i in range(100):
#             program = random.choice(["F", "P"])
#             level = random.choice(["ND", "HND"])
#             year = random.choice(["21", "22", "23"])
#             matric_number = f"{program}/{level}/{year}/34400{i}"
#             ip_address = f"192.168.{random.randint(0, 255)}.{random.randint(1, 255)}"
#             voter = Voter(
#                 matric_number=matric_number,
#                 ip_address=ip_address
#             )
#             voters.append(voter)
#         Voter.objects.bulk_create(voters)
#         self.stdout.write(self.style.SUCCESS('Successfully created voters'))



class Command(BaseCommand):
    help = "Copy voter details from a file"

    def handle(self, *args, **kwargs):
        file_path = BASE_DIR / "matric_numbers.csv"
        voters = []
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                print(reader.fieldnames)
                for row in reader:
                    voter = Voter(
                        matric_number=row['matric_number'],
                    )
                    voters.append(voter)
            Voter.objects.bulk_create(voters)
            self.stdout.write(self.style.SUCCESS('Successfully created voters'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
