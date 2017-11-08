from uuid import uuid4
import boto
import os.path
from flask import current_app as app
from werkzeug.utils import secure_filename


def s3_upload(source_file, upload_dir=None, acl='public-read'):
    """ Uploads WTForm File Object to Amazon S3

        Expects following app.config attributes to be set:
            AWS_KEY             :   S3 API Key
            AWS_SECRET          :   S3 Secret Key
            S3_BUCKET           :   What bucket to upload to
            S3_UPLOAD_DIRECTORY :   Which S3 Directory.

        The default sets the access rights on the uploaded file to
        public-read.  It also generates a unique filename via
        the uuid4 function combined with the file extension from
        the source file.
    """

    if upload_dir is None:
        upload_dir = app.config["S3_UPLOAD_DIRECTORY"]

    source_filename = secure_filename(source_file.data.filename)
    source_extension = os.path.splitext(source_filename)[1]

    destination_filename = uuid4().hex + source_extension

    # Connect to S3 and upload file.
    conn = boto.connect_s3(app.config["AWS_KEY"], app.config["AWS_SECRET"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    sml = b.new_key("/".join([upload_dir, destination_filename]))
    sml.set_contents_from_string(source_file.data.read())
    sml.set_acl(acl)

    return destination_filename