from django.core.management.base import BaseCommand
from voting.models import Position



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