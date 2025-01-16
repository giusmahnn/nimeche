from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.db.models import F
from voting.models import Candidate, Position, Voter


class HomePage(View):
	def get(self, request):
		position = Position.objects.all().prefetch_related('candidate_set')
		context = {
			"positions": position,
			}
		return render(request, "voting/home.html", context)
	

class DetailPage(View):
	def get(self, request, slug):
		if not request.session.get("voter"):
			# query_params = urlencode({"position": position_id})
			# url = f"{reverse('matric_number')}?{query_params}"
			# return redirect(url)
			request.session["position_slug"] = slug
			return redirect(reverse("matric_number"))
		position = get_object_or_404(
			Position.objects.prefetch_related('candidate_set'),
			slug=slug
			)
		candidates = position.candidate_set.all()
		context = {
			"position": position, 
			"candidates": candidates
			}
		return render(request, "voting/vote-detail.html", context)


class VotesView(View):
	def get(self, request, candidate_id):
		candidate = get_object_or_404(Candidate, id=candidate_id)
		voter_data = request.session.get("voter")

		if not voter_data:
			messages.error(request, "You need to log in to vote.")
			return redirect(reverse('home'))

		matric_number = voter_data.get("matric_number")
		# ip_address = voter_data.get("ip_address")

		if settings.ENABLE_MATRIC_NUMBER_VALIDATION:
			voter = Voter.objects.filter(matric_number=matric_number).first()
			if not voter:
				messages.error(request, "Invalid voter information.")
				return redirect(reverse('home'))
			# Check if the voter has already voted for this position
			if voter.voted_position.filter(id=candidate.position.id).exists():
				messages.info(request, "You have already voted for this position.")
				return redirect(reverse('vote-detail', kwargs={'slug': candidate.position.slug}))
		else:
			# Check if the voter has already voted for this position using session data
			voted_positions = request.session.get("voted_positions", [])
			if candidate.position.id in voted_positions:
				messages.info(request, "You have already voted for this position.")
				return redirect(reverse('vote-detail', kwargs={'slug': candidate.position.slug}))

		# Record the vote
		candidate.votes = F('votes') + 1
		candidate.save()

		if settings.ENABLE_MATRIC_NUMBER_VALIDATION:
			# Mark this position as voted in the voter model
			voter.voted_position.add(candidate.position)
		else:
			# Update session data
			voted_positions.append(candidate.position.id)
			request.session["voted_positions"] = voted_positions

		messages.success(request, "Your vote has been recorded.")
		return redirect(reverse('vote-detail', kwargs={'slug': candidate.position.slug}))


class MatricNumber(View):
	"""
	Handles the matric number validation process for voters.
	"""
	def get(self, request):
		return render(request, "voting/matric-number.html")
	
	def post(self, request):
		matric_number = request.POST.get('matric_number').upper()
		position_slug = request.session.get("position_slug")
		if settings.ENABLE_MATRIC_NUMBER_VALIDATION:
			# Matric number validation is enabled
			try:
				voter = Voter.objects.get(matric_number=matric_number)
				request.session["voter"] = {
                    "matric_number": voter.matric_number
                }
			except Voter.DoesNotExist:
				messages.error(request, "Invalid matric number.")
				return redirect(reverse("matric_number"))
			
			return redirect(reverse("vote-detail", kwargs={'slug': position_slug}))
		else:
			# Matric number validation is disabled
			request.session["voter"] = {
				"matric_number": matric_number
			}
		if position_slug:
			return redirect(reverse("vote-detail", kwargs={'slug': position_slug}))
		else:
			return redirect(reverse("home"))