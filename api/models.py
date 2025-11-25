from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Member(models.Model):
    """Custom user model for chat members"""
    username = models.CharField(max_length=50, unique=True, db_index=True)
    display_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Properties required for DRF compatibility
    is_authenticated = True
    is_anonymous = False
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
    
    def set_password(self, raw_password):
        """Hash and set password"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verify password"""
        return check_password(raw_password, self.password)
    
    def has_perm(self, perm, obj=None):
        """Check if user has permission"""
        return True
    
    def has_module_perms(self, app_label):
        """Check if user has module permissions"""
        return True


class AuthToken(models.Model):
    """Authentication token for members"""
    key = models.CharField(max_length=40, primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='auth_tokens')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Token for {self.member.username}"


class Message(models.Model):
    """Chat message model"""
    text = models.TextField(max_length=2000)
    author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.username}: {self.text[:50]}"
