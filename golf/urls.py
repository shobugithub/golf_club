from django.urls import path
# from golf.views import LogoutView, register, sending_email, verify_email_complete, verify_email_confirm, verify_email_done
from golf.views import index_page, event_listing, event_detail, LoginPage, RegisterView, LogoutPage, sending_email, verify_email_done, verify_email_confirm, verify_email_complete

app_name = 'golf_club'

urlpatterns = [
    path('', index_page, name='index'),
    path('event-listing/', event_listing, name='event_listing'),
    path('event-detail/<int:pk>/', event_detail, name='event_detail'),

    #auth
    # path('login/', user_login, name='login'),
    # path('register/', register, name='register'),
    # path('logout/', user_logout, name='logout'),

        # authentication's url
    path('login-page/', LoginPage.as_view(), name='login'),
    path('logout-page/', LogoutPage.as_view(), name='logout'),
    path('register-page/', RegisterView, name='register'),
    # sending email url
    path('sending-email-url/', sending_email, name='sending_email'),

    # verify email

    path('verify-email-done/', verify_email_done, name='verify_email_done'),
    path('verify-email/complete/', verify_email_complete, name='verify_email_complete'),
    path('verify-email-confirm/<uidb64>/<token>/', verify_email_confirm, name='verify_email_confirm'),
]