from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta

class TwoFactorToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='two_factor')
    totp_key = models.CharField(max_length=50, blank=True, null=True)  
    last_verified_otp = models.IntegerField(blank=True, null=True)  
    is_verified = models.BooleanField(default=False)   
    date_2fa_enabled = models.DateTimeField(blank=True, null=True)  
    failed_attempts = models.IntegerField(default=0)  
    backup_codes = models.TextField(blank=True, null=True)  
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    date_2fa_disabled = models.DateTimeField(blank=True, null=True)  
    
    def generate_otp(self):
        pass
    
    def verify_otp(self, otp):
        pass
    
    def generate_backup_codes(self):
        pass

    def validate_backup_code(self, code):
        pass


class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_verifications')
    otp = models.CharField(max_length=8)  # Assuming 6-digit OTP
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=10))
    
    def is_valid(self):
        return timezone.now() < self.expires_at

    def verify(self, provided_otp):
        if self.is_valid() and self.otp == provided_otp:
            self.is_verified = True
            self.save()
            return True
        return False
