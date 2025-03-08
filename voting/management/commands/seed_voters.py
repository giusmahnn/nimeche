import random
import csv
from django.core.management.base import BaseCommand
from voting.models import (
    Voter
)
from nimeche.settings.base import BASE_DIR



class Command(BaseCommand):
    help = 'Populate the database with voter details and save to CSV'

    def handle(self, *args, **options):
        voters = []
        csv_file = "votershnd1.csv"
        
        sequences = [
            
            ("P", "HD", "24", 60)
        ]
        
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["matric_number"])
            
            for program, level, year, count in sequences:
                for i in range(1, count + 1):
                    # Format matric number based on length
                    if i < 10:
                        matric_number = f"{program}/{level}/{year}/344000{i}"
                    elif i < 100:
                        matric_number = f"{program}/{level}/{year}/34400{i}"
                    else:
                        matric_number = f"{program}/{level}/{year}/3440{i}"
                    
                    # Skip if matric_number already exists
                    if Voter.objects.filter(matric_number=matric_number).exists():
                        continue
                    
                    voter = Voter(
                        matric_number=matric_number
                    )
                    voters.append(voter)
                    writer.writerow([matric_number])
        
        Voter.objects.bulk_create(voters)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(voters)} new voters and saved to {csv_file}'))




# class Command(BaseCommand):
#     help = "Copy voter details from a file"

#     def handle(self, *args, **kwargs):
#         file_path = BASE_DIR / "matric_numbers.csv"
#         voters = []
#         try:
#             with open(file_path, 'r') as file:
#                 reader = csv.DictReader(file)
#                 print(reader.fieldnames)
#                 for row in reader:
#                     voter = Voter(
#                         matric_number=row['matric_number'],
#                     )
#                     voters.append(voter)
#             Voter.objects.bulk_create(voters)
#             self.stdout.write(self.style.SUCCESS('Successfully created voters'))
#         except FileNotFoundError:
#             self.stdout.write(self.style.ERROR('File not found'))
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(e))
