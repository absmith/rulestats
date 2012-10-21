from django.db import models
from django_fields.fields import EncryptedCharField

# Create your models here.
class Firewall(models.Model):
    name = models.CharField(max_length=256)
    ip = models.IPAddressField()
    user = EncryptedCharField(max_length=1024)
    password = EncryptedCharField(max_length=1024)
    enable_password = EncryptedCharField(max_length=1024)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.ip)

class Rule(models.Model):
    firewall = models.ForeignKey(Firewall, related_name='rules')
    access_list = models.CharField(max_length=256)
    type = models.CharField(max_length=10)
    protocol = models.CharField(max_length=10)
    details = models.CharField(max_length=1024)
    max_hit_count = models.PositiveIntegerField()
    current_hit_count = models.PositiveIntegerField()
    hash = models.CharField(max_length=10)
    hash1 = models.CharField(max_length=32)
    last_modified=models.DateTimeField("Last modified",
                                    auto_now=True, auto_now_add=True)
    added_timestamp=models.DateTimeField("Added Timestamp", auto_now_add=True)
    max_hit_count_timestamp=models.DateTimeField()

    def save(self, *args, **kwargs):
        save = False
        if self.id:
            old_self = Rule.objects.get(id=self.id)
            if self.access_list !=  old_self.access_list:
                save = True
            elif self.type != old_self.type:
                save = True
            elif self.protocol != old_self.protocol:
                save = True
            elif self.details != old_self.details:
                save = True
            elif int(self.hit_count) != old_self.hit_count:
                save = True
            elif self.hash != old_self.hash:
                save = True
            elif self.hash1 != old_self.hash1:
                save = True
        else:
            save = True

        if save:
            super(Rule, self).save(*args, **kwargs)