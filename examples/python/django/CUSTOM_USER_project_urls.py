from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns += [
    path('reset', PasswordResetView.as_view(template_name='account/password_reset.html'), name='password_reset',),
    path('reset-enviado', PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done',),
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html' ), name='password_reset_confirm',),
    path('reset-concluido', PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html' ), name='password_reset_complete',),
]
