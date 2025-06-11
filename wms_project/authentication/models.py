from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# We're using Django's built-in User model for authentication
# This file can be extended with additional user profile information if needed

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name=_("User"))
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True, null=True)
    address = models.TextField(_("Address"), blank=True, null=True)
    position = models.CharField(_("Position"), max_length=100, blank=True, null=True)
    profile_image = models.ImageField(_("Profile Image"), upload_to='profiles/', blank=True, null=True)

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return f"{self.user.username}'s Profile"