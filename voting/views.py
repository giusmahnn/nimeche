from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from ipware import get_client_ip
from django.views import View
from django.contrib import messages
from django.middleware.csrf import get_token
from django.conf import settings
from django.db.models import F
from accounts.models import VotingStatus
from voting.models import (
    Candidate, 
    Position, 
    Voter)
import os

def my_view(request):
    ip, is_routable = get_client_ip(request)
    print(f"Client IP: {ip}, Routable: {is_routable}")
    return JsonResponse({"ip": ip, "is_routable": is_routable})

	
class HomePage(View):
	"""
	HomePage view for displaying the home page of the voting application.

	Methods:
		get(request):
			Handles GET requests to the home page.
			Retrieves all Position objects along with their related Candidate objects.
			Renders the 'voting/home.html' template with the retrieved positions.

	Attributes:
		None
	"""
	def get(self, request):
		position = Position.objects.all().prefetch_related('candidate_set')
		context = {
			"positions": position,
			}
		return render(request, "voting/home.html", context)
	

class DetailPage(View):
	"""
	View to handle the detail page for voting.

	Methods
	-------
	get(request, slug):
		Handles GET requests to display the voting detail page.
		If voting is allowed and the voter is not in session, redirects to matric number page.
		If voting is allowed and the voter is in session, displays the voting detail page with candidates.
		If voting is not allowed, redirects to the home page with an error message.

	Parameters
	----------
	request : HttpRequest
		The HTTP request object.
	slug : str
		The slug of the position to be voted on.
	"""
	def get(self, request, slug):
		voting_status = VotingStatus.objects.first()
		# voting_status = os.getenv("VOTING_STATUS")
		if voting_status:
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
		else:
			messages.error(request, "Voting has ended")
			return redirect(reverse('home'))


class VotesView(View):
	"""
	View to handle voting actions.

	Methods
	-------
	get(request, candidate_id)
		Handles GET requests to record a vote for a candidate.

	Parameters
	----------
	request : HttpRequest
		The HTTP request object.
	candidate_id : int
		The ID of the candidate being voted for.

	Returns
	-------
	HttpResponse
		Redirects to the appropriate page based on the voting status and validation checks.

	Behavior
	--------
	- Checks if voting is allowed based on the voting status.
	- Validates voter information based on session data and settings.
	- Records the vote if all validations pass.
	- Updates the voter's voting status in the database or session.
	- Provides appropriate messages to the user based on the outcome.
	"""
	def get(self, request, candidate_id):
		voting_status = VotingStatus.objects.first()
		# Controls voting status
		if voting_status.can_vote:
			candidate = get_object_or_404(Candidate, id=candidate_id)
			voter_data = request.session.get("voter")

			if not voter_data:
				messages.error(request, "You need to log in to vote.")
				return redirect(reverse('home'))

			matric_number = voter_data.get("matric_number")
			# ip_address = voter_data.get("ip_address")
			# Controls matric number validation T/F
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
		else:
			messages.error(request, "Voting has ended")
			return redirect(reverse('home'))


class MatricNumber(View):
	"""
	MatricNumber View handles the GET and POST requests for matric number validation.
	Methods:
		get(request):
			Renders the matric-number.html template.
		post(request):
			Processes the matric number submitted via POST request.
			- Converts the matric number to uppercase.
			- Retrieves the position slug from the session.
			- If matric number validation is enabled in settings:
				- Attempts to find a Voter with the given matric number.
				- If found, stores the matric number in the session and redirects to the vote-detail page.
				- If not found, displays an error message and redirects to the matric_number page.
			- If matric number validation is disabled:
				- Stores the matric number in the session.
			- Redirects to the vote-detail page if position slug is available, otherwise redirects to the home page.
	"""
	def get(self, request):
		csrf_token = get_token(request)
		print(f"CSRF Token: {csrf_token}")
		return render(request, "voting/matric-number.html")
	
	def post(self, request):
		matric_number = request.POST.get('matric_number').upper()
		ip_address, is_routable = get_client_ip(request)
		position_slug = request.session.get("position_slug")
		if settings.ENABLE_MATRIC_NUMBER_VALIDATION:
			# Matric number validation is enabled
			try:
				voter = Voter.objects.get(matric_number=matric_number)
				request.session["voter"] = {
                    "matric_number": voter.matric_number,
					"ip_address": ip_address
                }
			except Voter.DoesNotExist:
				messages.error(request, "Invalid matric number.")
				return redirect(reverse("matric_number"))
			
			return redirect(reverse("vote-detail", kwargs={'slug': position_slug}))
		else:
			# Matric number validation is disabled
			request.session["voter"] = {
				"matric_number": matric_number,
				"ip_address": ip_address,
			}
		if position_slug:
			return redirect(reverse("vote-detail", kwargs={'slug': position_slug}))
		else:
			return redirect(reverse("home"))