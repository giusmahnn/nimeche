from django.shortcuts import get_object_or_404, render
from django.views import View

from voting.models import Candidate, Position


class HomePage(View):
	def get(self, request):
		position = Position.objects.all()
		context = {
            "positions": position,
            }
		return render(request, "voting/home.html", context)
	

class DetailPage(View):
	def get(self, request, position_id):
		position = get_object_or_404(Position, id=position_id)
		candidates = Candidate.objects.filter(position=position)
		context = {
			"position": position, 
			"candidates": candidates
			}
		return render(request, "voting/vote-detail.html", context)