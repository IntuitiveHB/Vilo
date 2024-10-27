from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from authentication.utils import Util


@receiver(post_save, sender='authentication.CustomUser')
def after_user_created(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            token = RefreshToken.for_user(instance).access_token

            current_site = Site.objects.get_current().domain
            # relative_link = reverse('email-verify')
            relative_link = '/email-activation'
            # protocol = 'https' if request.is_secure() else 'http'
            # absurl = protocol+'://'+ ...
            absurl = current_site + relative_link+"?token="+str(token)

            new_pass = Util.generate_random_password(16)
            user = get_user_model().objects.get(pk=instance.pk)
            user.set_password(new_pass)
            user.save(update_fields=['password'])

            data = {
                'user': instance.full_name,
                'email': instance.email,
                'pwd': new_pass,
                'domain': absurl,
                'subject': 'Verify your email.',
                'template': 'email_welcome_template.html',
            }

            Util.send_email(data)
    else:
        pass
