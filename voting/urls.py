from django.urls import path
from .views import (
	HomePage,
	DetailPage,
	VotesView,
	MatricNumber
)


urlpatterns = [
	path('', HomePage.as_view(), name='home'),
	path("detail/<slug:slug>/", DetailPage.as_view(), name='vote-detail'),
	path("votes/<int:candidate_id>/", VotesView.as_view(), name='votes'),
	path("matric-number/", MatricNumber.as_view(), name='matric_number'),
]
