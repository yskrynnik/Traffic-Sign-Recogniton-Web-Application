from flask import Flask
from config import Config
from flask_uploads import UploadSet, IMAGES, configure_uploads

from controllers.main_controller import main_controller

app = Flask(__name__)
app.config.from_object(Config)

images = UploadSet('Images', IMAGES)
configure_uploads(app, (images,))

app.register_blueprint(main_controller)

if __name__ == '__main__':
    app.run()
