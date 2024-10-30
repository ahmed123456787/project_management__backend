from django.contrib import admin
from django.urls import path,include
from core.views import SendInvitationEmail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # This enables login/logout views
    path('api/send-invitation/', SendInvitationEmail.as_view(), name='send_invitation'),
    path('',include("core.urls")),
]
