from django.core.management.base import BaseCommand  
from voting.models import Position, Candidate, Voter

class Command(BaseCommand):  
    help = 'Remove all data from Positions, Candidates, and Voters tables'  

    def handle(self, *args, **options):  
        
        # confirmed = input("Are you sure you want to delete all Positions, Candidates, and Voters? (yes/no): ")  
        # if confirmed.lower() != 'yes':  
        #     self.stdout.write(self.style.WARNING('Deletion canceled.'))  
        #     return  

        Position.objects.all().delete()  
        Candidate.objects.all().delete()  
        Voter.objects.all().delete()  

        self.stdout.write(self.style.SUCCESS('Successfully deleted all data from Positions, Candidates, and Voters.'))