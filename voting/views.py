from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.conf import settings
from urllib.parse import urlencode
from django.db.models import F, Sum
from voting.models import Candidate, Position, Voter
from voting.serializers import VoterSerializer
from voting.utils import get_winners


class HomePage(View):
	def get(self, request):
		position = Position.objects.all().prefetch_related('candidate_set')
		context = {
			"positions": position,
			}
		return render(request, "voting/home.html", context)
	

class DetailPage(View):
	def get(self, request, position_id):
		if not request.session.get("voter"):
			# query_params = urlencode({"position": position_id})
			# url = f"{reverse('matric_number')}?{query_params}"
			# return redirect(url)
			request.session["position_id"] = position_id
			return redirect(reverse("matric_number"))
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
			# ip_address = voter_data.get("ip_address")

			voter = Voter.objects.filter(matric_number=matric_number).first()
			if voter:
				voted_positions = request.session.get("voted_positions", [])
				if candidate.position.id in voted_positions:
					messages.info(request, "You have already voted for this position.")
					return redirect(reverse('vote-detail', kwargs={'position_id': candidate.position.id}))

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
		

class MatricNumber(View):
	"""
	Handles the matric number validation process for voters.
	"""
	def get(self, request):
		return render(request, "voting/matric-number.html")
	
	def post(self, request):
		if settings.ENABLE_MATRIC_NUMBER_VALIDATION:
			matric_number = request.POST.get('matric_number').upper()
			position_id = request.session.get("position_id")
			try:
				voter = Voter.objects.get(matric_number=matric_number)
			except Voter.DoesNotExist:
				messages.error(request, "Invalid matric number.")
				return redirect(reverse("matric_number"))
		request.session["voter"] = {
			"matric_number": voter.matric_number}
		return redirect(reverse("vote-detail", kwargs={'position_id': position_id}))




class AdminDashboardView(View):
	def get(self, request):
		registered_voters = Voter.objects.count()
		positions = Position.objects.count()
		candidates = Candidate.objects.count()
		total_votes = Candidate.objects.aggregate(total_votes=Sum('votes'))['total_votes']
		winner = self.get_winners()

		context = {
			"registered_voters": registered_voters,
			"positions": positions,
			"candidates": candidates,
			"total_votes": total_votes,
			"winner": winner
		}
		return render(request, "voting/admin-dashboard.html", context)


	def get_winners(request):
		winners = []
		positions = Position.objects.prefetch_related("candidte_set")
		for position in positions:
			winner = position.candidate_set.order_by("-votes").first()
			if winner:
				winners.append({
					"position_name": position.name,
					"winner_name": winner.name,
					"winner_votes": winner.votes,
					"total_votes": position.candidate_set.aggregate(total_votes=Sum('votes'))['total_votes'] or 0,
				})
		return winners
	
    