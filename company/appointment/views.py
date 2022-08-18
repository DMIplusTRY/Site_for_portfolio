from django.shortcuts import render
from .models import Appointment
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from .models import Client
from .forms import ChangeUserInfoForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import CreateView
from .forms import RegisterUserForm
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from .utilities import signer


def index(request):
    appointment = Appointment.objects.all()
    return render(request, 'appointment/appointment.html', {'appointments': appointment})


class AppointmentLoginView(LoginView):
    template_name = 'appointment/login.html'


@login_required()
def profile(request):
    return render(request, 'appointment/profile.html')


class AppointmentLogoutView(LogoutView):
    template_name = 'appointment/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Client
    template_name = 'appointment/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('appointment:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ChangePasswordView(PasswordChangeView, SuccessMessageMixin, LoginRequiredMixin):
    template_name = 'appointment/change_password.html'
    success_url = reverse_lazy('appointment:profile')
    success_message = "Пороль изменен"


class RegisterUserView(CreateView):
    model = Client
    template_name = 'appointment/register_user.html'
    success_url = reverse_lazy('appointment:register_done')
    form_class = RegisterUserForm


class RegisterDoneView(TemplateView):
    template_name = 'appointment/register_done.html'

def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'appointment:bad_signature.html')
    user = get_object_or_404(Client, username=username)
    if user.is_activated:
        template = 'appointment:user_is_activated.html'
    else:
        template = 'appointment:activation_done.html'
        user.is_activated = True
        user.is_active = True
        user.save()
    return render(request, template)