import secrets
import os


def save_picture(form_picture, app):
    rnd_hex = secrets.token_hex(8)
    filename, filextension = os.path.splitext(form_picture.filename)
    picture_filename = rnd_hex + filextension
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_filename)
    form_picture.save(picture_path)

    return picture_filename
