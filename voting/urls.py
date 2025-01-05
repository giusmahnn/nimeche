from django.urls import path
from .views import (
    HomePage,
    test_template
)


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('test/', test_template, name='test'),
    # path('candidates/', CandidatesView.as_view(), name='candidates'),
    # path('candidates/<int:pk>/', CandidateDetailView.as_view(), name='candidate_detail'),
    # path('candidates/<int:pk>/vote/', vote, name='vote'),
    # path('results/', ResultsView.as_view(), name='results'),
    # path('admin/', admin.site.urls),
]
