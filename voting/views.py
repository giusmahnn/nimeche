from django.shortcuts import get_object_or_404, render
from django.views import View

from voting.models import Candidate, Position


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