from django.db import models
from django.contrib.auth.models import User

class TwoFactorToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='two_factor_token')
    totp_key = models.CharField(max_length=50, blank=True, null=True) 
    last_verified_otp = models.IntegerField(blank=True, null=True)  
    is_verified = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def generate_otp(self):
        pass
    
    def verify_otp(self, otp):
        pass
