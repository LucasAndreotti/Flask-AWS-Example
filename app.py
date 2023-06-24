from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from s3 import s3_upload
from dynamodb import dynamodb_scan, dynamodb_put_item
from time import time

app = Flask(__name__)
app.config.from_object("config")

class UploadForm(FlaskForm):
    example = FileField("Example File")

@app.route("/", methods=["POST", "GET"])
def upload_page():
    form = UploadForm()
    if form.validate_on_submit():
        output = s3_upload(form.example)
        item = {
            "image_url": "https://s3.amazonaws.com/" + app.config["infra-ti-s3"] + "/" + output,
            "name": output,
            "date": int(time())
        }
        flash('by LucasAndreotti {src} uploaded to S3 as {dst}'.format(src=form.example.data.filename, dst=output))
        dynamodb_put_item(item)
    entries = dynamodb_scan()
    return render_template('example.html', form=form, entries=entries)

if __name__ == '__main__':
    app.run()
