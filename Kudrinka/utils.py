from django.utils.text import slugify
import random
import string


def unique_slug_generator(model_instance, title, slug_field):
    """

    :param model_instance:
    :param title:
    :param slug_field:
    :return:
    """

    slug = slugify(title)
    model_class = model_instance.__class__

    while model_class._default_manager.filter(slug=slug).exists():
        object_id = model_class._default_manager.latest('id')
        object_id = object_id.id + 1

        slug = '{slug}-{object_id}'
    return slug


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#
# def unique_slug_generator(instance, new_slug=None):
#     if new_slug is not None:
#         slug = new_slug
#     else:
#         # We are using .lower() method for case insensitive
#         # you can use instance.<fieldname> if you want to use another field
#         str = replace_all(instance.name.lower())
#         slug = slugify(str)
#
#     Klass = instance.__class__
#     qs_exists = Klass.objects.filter(slug=slug).exists()
#     if qs_exists:
#         new_slug = "{slug}-{randstr}".format(
#             slug=slug,
#             randstr=random_string_generator(size=4)
#         )
#         return unique_slug_generator(instance, new_slug=new_slug)
#     return slug
#
#
# def replace_all(text):
#     rep = {
#         'ı': 'i',
#         'ş': 's',
# #         'ü': 'u',
# #         'ö': 'o',
# #         'ğ': 'g',
# #         'ç': 'c'
# #     }
# #     for i, j in rep.items():
# #         text = text.replace(i, j)
# #     return text
#
#
#
