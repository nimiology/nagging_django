import os
import random
import string


def slug_generator(num):
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)
    return "".join(random.choice(letters) for _ in range(num))


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_file(location, instance, filename):
    name, ext = get_filename_ext(filename)
    return f"{location}/{slug_generator(40)}{ext}"


def user_profile_upload_file(instance, filename):
    return upload_file(f'{instance.id}/profile', instance, filename)


def artist_profile_upload_file(instance, filename):
    return upload_file(f'{instance.owner.id}/artist/profile', instance, filename)


def art_image_upload_file(instance, filename):
    return upload_file(f'{instance.owner.id}/art/image', instance, filename)
