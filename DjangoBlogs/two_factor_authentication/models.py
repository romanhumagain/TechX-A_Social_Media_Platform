from django.db import models
from django.contrib.auth.models import User

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
