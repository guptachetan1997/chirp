from django import template
from chirps.models import Chirp

register = template.Library()

@register.filter
def check_if_liked(user_id, chirp_id):
    try:
        chirp_data = Chirp.objects.get(id = chirp_id)
        return chirp_data.like.filter(id = user_id).exists()
    except Chirp.DoesNotExist:
        return 'Unknown'
