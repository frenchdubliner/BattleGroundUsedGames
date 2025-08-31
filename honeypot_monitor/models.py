from django.db import models
from django.utils import timezone

# Create your models here.

class HoneypotAttempt(models.Model):
    """Model to store honeypot access attempts"""
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    username = models.CharField(max_length=150, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    is_login_attempt = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Honeypot Attempt'
        verbose_name_plural = 'Honeypot Attempts'
    
    def __str__(self):
        action = 'Login attempt' if self.is_login_attempt else 'Page access'
        return f"{action} from {self.ip_address} at {self.timestamp}"
    
    @property
    def short_user_agent(self):
        """Return shortened user agent for display"""
        if len(self.user_agent) > 50:
            return self.user_agent[:50] + '...'
        return self.user_agent
