import datetime
import display
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import dir_operations as dir_op
import file_operations as file_op
import user_operations as user_op


class DownHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        name = self.request.get('file_name')
        object = file_op.obj_of_file(name)
        self.send_blob(object.blob,save_as=object.name)

class UpHandler(blobstore_handlers.BlobstoreUploadHandler):
    e = "e"

    def post(self):
        up = self.get_uploads()
        if len(up) == 0:
            display.give_error(self, '/', "No File Selected")
        else:
            global e
            for upload in up:
                filename = blobstore.BlobInfo(upload.key()).filename
                e = file_op.adding(upload, filename, datetime.datetime.now())
                display.give_error(self, '/', e)
