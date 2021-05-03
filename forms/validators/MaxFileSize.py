from wtforms import ValidationError


class MaxFileSize(object):
    def __init__(self, size, message=None):
        self.size = size
        if not message:
            message = f'Maximum file size is { self.size // (1024 * 1024) } MB.'
        self.message = message

    def __call__(self, form, field):
        f = field.data
        f.seek(0, 2)
        file_size = f.tell()
        f.seek(0)
        if file_size > self.size:
            raise ValidationError(self.message)
