import user_operations as user_operations
from dir_operations import getting_path, nocontain, obj_of_current_dir, get_directories_in_current_path, inlist, slash
from model import File
from model2 import Folder
from google.appengine.ext import blobstore
from google.appengine.ext import ndb


def get_obj_of_current_file():
    return obj_of_current_dir().files


def get_numoffiles_in_live_path():
    return len(obj_of_current_dir().files)


def obj_of_file(file_name):
    user = user_operations.get_user_for_model()
    root_dir_object = obj_of_current_dir()
    path = getting_path(file_name, root_dir_object)
    id = user.key.id() + path
    return ndb.Key("File", id).get()


def adding(upload, filename, datetime):
    user = user_operations.get_user_for_model()
    current_dir = obj_of_current_dir()
    id = user.key.id() + getting_path(filename, current_dir)
    key = ndb.Key("File", id)

    if nocontain(key, current_dir.files):
        object = File(id=id)
        object.name = filename
        object.date = datetime
        object.blob = upload.key()
        object.put()
        current_dir.files.append(key)
        current_dir.put()
        return "file added!"
    else:
        blobstore.delete(upload.key())
        return "A file with this name already exists in this directory!"

def delete(name):
    user = user_operations.get_user_for_model()
    object = obj_of_current_dir()
    p = getting_path(name, object)
    id = user.key.id() + p
    key = ndb.Key("File", id)
    blobobj = key.get().blob
    object.files.remove(key)
    blobstore.delete(blobobj)
    key.delete()
    object.put()
