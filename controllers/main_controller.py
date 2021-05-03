from flask import Blueprint, render_template
from flask import current_app as app
from CNN.RoadSignClassifier import RoadSignClassifier
from forms.upload_form import UploadForm
import numpy as np
import matplotlib.pyplot as plt
import io
import os
import base64

main_controller = Blueprint("main_controller", __name__, template_folder='templates')


@main_controller.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        image_file = form.image.data
        RSC_CNN = RoadSignClassifier()
        predicted_data = RSC_CNN.predict(image_file)
        predicted_data = predicted_data.ravel()
        indexes_of_max_val = (-predicted_data).argsort()[:5]
        result = []
        percentage = "{:.2%}".format(predicted_data[indexes_of_max_val[0]])
        result.append(f'{RSC_CNN.CLASSES[indexes_of_max_val[0]]} ({percentage})')
        pic_hash = ""
        
        if predicted_data[indexes_of_max_val[0]] < 0.90:
            labels = []
            data = predicted_data[indexes_of_max_val]
            for i in range(5):
                labels.append(RSC_CNN.CLASSES[indexes_of_max_val[i]])

            data = np.append(data, 1-np.sum(data))
            labels.append('Others')

            for i in range(6):
                labels[i] = f'{labels[i]} - ' + "{:.1%}".format(data[i])

            fig1, ax1 = plt.subplots(figsize=(12, 4))
            ax1.set_title('Recognition result')
            ax1.pie(data, shadow=True, startangle=90)
            ax1.legend(labels, loc="upper left")
            ax1.axis('equal')

            pic_IObytes = io.BytesIO()
            plt.savefig(pic_IObytes, format='png')
            plt.close(fig1)
            pic_IObytes.seek(0)
            pic_hash = base64.b64encode(pic_IObytes.read()).decode('utf-8')

            plt.figure(figsize=(15, 3))
            plt.rcParams.update({'font.size': 15})
            for i in range(5):
                plt.subplot(1, 5, i+1)
                plt.grid(False)
                plt.xticks([])
                plt.yticks([])
                plt.xlabel('{}'.format(RoadSignClassifier.CLASSES[indexes_of_max_val[i]]))
                class_image = plt.imread(os.path.join(app.root_path, 'static', 'img', f'{indexes_of_max_val[i]}.png'))
                plt.imshow(class_image, aspect="auto")
        else:
            plt.figure(figsize=(2, 2))
            plt.rcParams.update({'font.size': 10})
            plt.gcf().subplots_adjust(bottom=0.15)
            plt.tight_layout()
            plt.grid(False)
            plt.xticks([])
            plt.yticks([])
            plt.xlabel('{}'.format(RoadSignClassifier.CLASSES[indexes_of_max_val[0]]))
            class_image = plt.imread(os.path.join(app.root_path, 'static', 'img', f'{indexes_of_max_val[0]}.png'))
            plt.imshow(class_image, aspect="auto")

        pic_IObytes = io.BytesIO()
        plt.savefig(pic_IObytes, format='png')
        plt.close()
        pic_IObytes.seek(0)
        previews = base64.b64encode(pic_IObytes.read()).decode('utf-8')
        image = base64.b64encode(image_file.read()).decode('utf-8')
        return render_template('index.html', image=image, form=form, text=result, plot=pic_hash, previews=previews)

    return render_template('index.html', form=form)




