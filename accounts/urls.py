from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),

    # Forgot password flow
    path("password-reset/", views.StudyPlannerPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", views.StudyPlannerPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.StudyPlannerPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.StudyPlannerPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
