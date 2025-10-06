from django.urls import path
from .webhooks import webhook_view

urlpatterns = [
    path("webhook/", webhook_view, name="stripe-webhook"),
]
