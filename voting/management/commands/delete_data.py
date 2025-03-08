from django.core.management.base import BaseCommand  
from voting.models import Position, Candidate, Voter
from django.db import transaction 

class Command(BaseCommand):  
    help = 'Remove all data from Positions, Candidates, and Voters tables'  
    @transaction.atomic
    def handle(self, *args, **options):  
        
        # confirmed = input("Are you sure you want to delete all Positions, Candidates, and Voters? (yes/no): ")  
        # if confirmed.lower() != 'yes':  
        #     self.stdout.write(self.style.WARNING('Deletion canceled.'))  
        #     return  

        Position.objects.all().delete()  
        Candidate.objects.all().delete()  
        Voter.objects.all().delete()  
        # deleted_count, _ = Voter.objects.filter(matric_number__startswith="P/HND/23").delete()
        # deleted_count, _ = Voter.objects.filter(matric_number__startswith="P/ND/24").delete()
        # deleted_count, _ = Voter.objects.filter(matric_number__startswith="P/ND/22").delete()

        # print(f"Deleted {deleted_count} incorrect voters.")

        self.stdout.write(self.style.SUCCESS('Successfully deleted all data from Positions, Candidates, and Voters.'))