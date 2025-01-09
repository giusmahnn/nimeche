from django.urls import path
from .views import (
	HomePage,
	DetailPage,
	VotesView,
	ValidateVoter,
	MatricNumber,
)


urlpatterns = [
	path('', HomePage.as_view(), name='home'),
	path("detail/<int:position_id>/", DetailPage.as_view(), name='vote-detail'),
	path("votes/<int:candidate_id>/", VotesView.as_view(), name='votes'),
	path("register/", ValidateVoter.as_view(), name='validate'),
	path("matric-number/", MatricNumber.as_view(), name='matric_number'),
]
