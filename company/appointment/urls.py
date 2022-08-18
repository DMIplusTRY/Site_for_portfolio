from django.urls import path
from .views import index, AppointmentLoginView, profile, AppointmentLogoutView, \
    ChangeUserInfoView, ChangePasswordView, RegisterUserView, RegisterDoneView

app_name = 'appointment'
urlpatterns = [
    path('', index, name = 'index'),
    path('accounts/login/', AppointmentLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', AppointmentLogoutView.as_view(), name='logout'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/change_password/', ChangePasswordView.as_view(), name='password_change'),
    path('accounts/register/', RegisterUserView.as_view(), name="register"),
    path('accounts/register/done/', RegisterDoneView.as_view(), name="register_done"),
]
