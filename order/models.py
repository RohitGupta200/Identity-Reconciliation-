from dataclasses import dataclass
from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.db.models import UniqueConstraint

class user(models.Model):
    id = models.AutoField(primary_key = True,
                          editable = False)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    deletedAt = models.DateTimeField(default = None, null=True)
    linkedId = models.IntegerField(null=True, blank=True)
    linkPrecedence = models.CharField(max_length = 25, default = "primary")
    email = models.EmailField(max_length = 100, default="")
    phonereg=RegexValidator('^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$')
    phoneNumber = models.CharField(validators = [phonereg], max_length = 13,default="")
    class Meta:
        constraints = [
            UniqueConstraint(fields=['email', 'phoneNumber'], name='unique_auto_custom')
        ]