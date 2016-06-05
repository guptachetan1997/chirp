from django import template
from chirps.models import chirp

register = template.Library()

@register.filter
def check_if_liked(user_id, chirp_id):
    try:
        chirp_data = chirp.objects.get(id = chirp_id)
        return chirp_data.like.filter(id = user_id).exists()
    except chirp.DoesNotExist:
        return 'Unknown'
