from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.db.models import F, Sum
from voting.models import Candidate, Position, Voter


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
			if voter.voted_positions.filter(id=candidate.position.id).exists():
				messages.info(request, "You have already voted for this position.")
				return redirect(reverse('vote-detail', kwargs={'position_id': candidate.position.id}))
		else:
			# Check if the voter has already voted for this position using session data
			voted_positions = request.session.get("voted_positions", [])
			if candidate.position.id in voted_positions:
				messages.info(request, "You have already voted for this position.")
				return redirect(reverse('vote-detail', kwargs={'position_id': candidate.position.id}))

		# Record the vote
		candidate.votes = F('votes') + 1
		candidate.save()

		if settings.ENABLE_MATRIC_NUMBER_VALIDATION:
			# Mark this position as voted in the voter model
			voter.voted_positions.add(candidate.position)
		else:
			# Update session data
			voted_positions.append(candidate.position.id)
			request.session["voted_positions"] = voted_positions

		messages.success(request, "Your vote has been recorded.")
		return redirect(reverse('vote-detail', kwargs={'position_id': candidate.position.id}))


class MatricNumber(View):
	"""
	Handles the matric number validation process for voters.
	"""
	def get(self, request):
		return render(request, "voting/matric-number.html")
	
	def post(self, request):
		matric_number = request.POST.get('matric_number').upper()
		position_id = request.session.get("position_id")
		if settings.ENABLE_MATRIC_NUMBER_VALIDATION:
			# Validation enabled
			try:
				voter = Voter.objects.get(matric_number=matric_number)
				request.session["voter"] = {
                    "matric_number": voter.matric_number
                }
			except Voter.DoesNotExist:
				messages.error(request, "Invalid matric number.")
				return redirect(reverse("matric_number"))
			
			return redirect(reverse("vote-detail", kwargs={'position_id': position_id}))
		else:
			# Validation disabled
			request.session["voter"] = {
				"matric_number": matric_number
			}
		if position_id:
			return redirect(reverse("vote-detail", kwargs={'position_id': position_id}))
		else:
			return redirect(reverse("home"))



class AdminDashboardView(LoginRequiredMixin, View):
	login_url = reverse_lazy("admin-login")
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


	def get_winners(self):
		winners = []
		positions = Position.objects.prefetch_related("candidate_set")
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



class LoginView(View):
	
	def get(self, request):
		return render(request, "voting/admin-login.html")

	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			return redirect("admin-dashboard")
		else:
			messages.error(request, "Invalid username or password.")
			return redirect("admin-login")


class LogoutView(View):
	def get(self, request):
		request.session.flush()
		return redirect("admin-login")