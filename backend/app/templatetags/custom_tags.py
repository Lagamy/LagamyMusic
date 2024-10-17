from django import template

register = template.Library()


@register.filter
def has_music(genre_music_map):
    return any(music_list for music_list in genre_music_map.values() if music_list) # same as:

# def has_music(genre_music_map):
#     for music_list in genre_music_map.values():
#         if music_list:
#             return True
#     return False
