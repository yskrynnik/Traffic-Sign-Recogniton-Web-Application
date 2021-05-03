from flask_wtf import FlaskForm
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from forms.validators.MaxFileSize import MaxFileSize

images = UploadSet('Images', IMAGES)


class UploadForm(FlaskForm):
    image = FileField('Image Field', validators=[
        FileRequired(),
        FileAllowed(images, 'Only images can be uploaded!'),
        MaxFileSize(5 * 1024 * 1024)
    ])
    submit = SubmitField('Recognize image')

