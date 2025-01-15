from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.db.models import Sum
from voting.models import Candidate, Position, Voter

# Create your views here.

class LoginView(View):
	
	def get(self, request):
		return render(request, "accounts/admin-login.html")

	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user:
			auth_login(request, user)
			return redirect("admin-dashboard", username=user.username)
		else:
			messages.error(request, "Invalid username or password.")
			return redirect("admin-login")



class AdminDashboardView(LoginRequiredMixin, View):
	login_url = reverse_lazy("admin-login")
	def get(self, request, username):
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
		return render(request, "accounts/dashboard.html", context)


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



class LogoutView(View):
	def get(self, request):
		request.session.flush()
		return redirect("admin-login")