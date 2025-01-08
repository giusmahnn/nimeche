from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages

from voting.models import Candidate, Position, Voter
from voting.serializers import VoterSerializer


class HomePage(View):
	def get(self, request):
		position = Position.objects.all().prefetch_related('candidate_set')
		context = {
            "positions": position,
            }
		return render(request, "voting/home.html", context)
	

class DetailPage(View):
	def get(self, request, position_id):
		position = get_object_or_404(
			Position.objects.prefetch_related('candidate_set'),
			id=position_id
			)
		candidates = position.candidate_set.all()
		context = {
			"position": position, 
			"candidates": candidates
			}
		return render(request, "voting/vote-detail.html", context)

class ValidateVoter(APIView):
	def post(self, request):
		serializers = VoterSerializer(data=request.data, context={'request': request})
		if serializers.is_valid():
			serializers.save()
			return Response(serializers.data, status=status.HTTP_201_CREATED)
		return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



class VotesView(View):
    def get(self, request, candidate_id):
        candidate = get_object_or_404(Candidate, id=candidate_id)
        voter_data = request.session.get("voter")
        if not voter_data:
            messages.error(request, "You need to log in to vote.")
            return redirect(reverse('home'))

        if voter_data:
            matric_number = voter_data.get("matric_number")
            ip_address = voter_data.get("ip_address")

            voter = Voter.objects.filter(matric_number=matric_number, ip_address=ip_address).first()
            if voter:
                voted_positions = request.session.get("voted_positions", [])
                if candidate.position.id in voted_positions:
                    messages.info(request, "You have already voted for this position.")
                    return redirect(reverse('vote-detail', kwargs={'position_id': candidate.position.id}))

                from django.db.models import F
                candidate.votes = F('votes') + 1
                candidate.save()

                voted_positions.append(candidate.position.id)
                request.session["voted_positions"] = voted_positions

                messages.success(request, "Your vote has been recorded.")
                return redirect(reverse('vote-detail', kwargs={'position_id': candidate.position.id}))
            else:
                messages.error(request, "Invalid voter information.")
                return redirect(reverse('home'))
        else:
            messages.error(request, "You need to log in to vote.")
            return redirect(reverse('home'))