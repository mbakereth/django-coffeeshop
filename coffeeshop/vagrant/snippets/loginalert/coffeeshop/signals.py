import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

log = logging.getLogger('login')

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):    
    ip = request.META.get('REMOTE_ADDR')
    uri = request.META.get('PATH_INFO')
    if (request.META.get('QUERY_STRING')):
        uri += '?' + request.META.get('QUERY_STRING')

    log.info('login success {user} {ip} {uri}'.format(
        user=user,
        ip=ip,
        uri=uri
    ))

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs): 
    ip = request.META.get('REMOTE_ADDR')
    uri = request.META.get('PATH_INFO')
    if (request.META.get('QUERY_STRING')):
        uri += '?' + request.META.get('QUERY_STRING')

    log.info('logout success {user} {ip} {uri}'.format(
        user=user,
        ip=ip,
        uri=uri
    ))

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    user = credentials['username']
    ip = request.META.get('REMOTE_ADDR')
    uri = request.META.get('PATH_INFO')
    if (request.META.get('QUERY_STRING')):
        uri += '?' + request.META.get('QUERY_STRING')

    log.info('login failure {user} {ip} {uri}'.format(
        user=user,
        ip=ip,
        uri=uri
    ))
