from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    # Add any additional fields you need
    # Example: profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # I think we may have to add the profile_picture field later because the computer I am using as of December 3, 2023 is not enough to do it

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        # Add this to avoid clashes with auth.User model
        swappable = 'AUTH_USER_MODEL'

# Add related names to avoid clashes with auth.User model
CustomUser._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'