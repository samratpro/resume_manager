from django.db import models
from django.contrib.auth.models import User
from resumemanager.models import Application


class Comment(models.Model):
    """Internal recruiter notes on candidates"""
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.application.reference_number}"


class ContactLog(models.Model):
    """Log of all contacts made with candidates"""
    CONTACT_TYPE_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('phone', 'Phone Call'),
        ('email', 'Email'),
        ('other', 'Other'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='contact_logs')
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES)
    message_sent = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    contacted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-contacted_at']

    def __str__(self):
        return f"{self.contact_type} - {self.application.reference_number} on {self.contacted_at}"


class StatusHistory(models.Model):
    """Track all status changes for candidates"""
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='status_history')
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = "Status histories"

    def __str__(self):
        return f"{self.application.reference_number}: {self.old_status} → {self.new_status}"
