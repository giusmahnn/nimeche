from django.db import IntegrityError, transaction
from rest_framework import serializers  
from .models import Voter  

class VoterSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Voter  
        fields = [  
            "matric_number",  
            "ip_address"  
        ]  
        read_only_fields = ['ip_address']

    def create(self, validated_data):
        matric_number = validated_data.get("matric_number")
        request = self.context.get('request')
        ip_address = request.META.get('REMOTE_ADDR') if request else None

        try:
            with transaction.atomic():
                voter, created = Voter.objects.get_or_create(
                    matric_number=matric_number,
                    defaults={'ip_address': ip_address}
                )
        except IntegrityError:
            # In case of race condition, fetch the voter again
            voter = Voter.objects.get(matric_number=matric_number)
            created = False

        if created or voter.ip_address == ip_address:
            self.context['request'].session["voter"] = {
                "matric_number": matric_number,
                "ip_address": ip_address
            }
            return voter
        else:
            raise serializers.ValidationError("IP address does not match.")