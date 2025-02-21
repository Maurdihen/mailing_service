from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .tokens import email_verification_token
from django.conf import settings

from .models import User
from .forms import UserRegisterForm, UserProfileForm

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    
    def form_valid(self, form):
        # Добавим логирование для отладки
        user = form.get_user()
        print(f"Trying to login user: {user.username}, is_active: {user.is_active}")
        return super().form_valid(form)

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.')
        return redirect('home')
        
    def post(self, request):
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.')
        return redirect('home')

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Деактивируем пользователя до подтверждения email
        user.save()

        # Отправляем email для подтверждения
        current_site = get_current_site(self.request)
        subject = 'Активируйте ваш аккаунт'
        message = render_to_string('users/email/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': email_verification_token.make_token(user),
        })
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER or 'test@example.com',
            [user.email],
            fail_silently=False,
        )
        
        messages.success(
            self.request,
            'Пожалуйста, подтвердите свой email - проверьте свою почту.'
        )
        return super().form_valid(form)

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Профиль успешно обновлен!')
        return response 

class ActivateAccount(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Ваш аккаунт активирован. Теперь вы можете войти.')
            return redirect('login')
        else:
            messages.error(request, 'Ссылка для активации недействительна!')
            return redirect('home') 