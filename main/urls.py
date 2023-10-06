from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView

from . import views
from .views import HomePage, RegistrationView, LoginView, TemplateBuilderView, ProfileView, ReportView

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('tempBuild/', TemplateBuilderView.as_view(), name='tempBuild'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('report/<int:temp_id>/', ReportView.as_view(), name='report'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico'))
]
