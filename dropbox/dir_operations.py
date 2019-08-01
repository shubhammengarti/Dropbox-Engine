import user_operations as user_operations
from model2 import Folder as modelfolder
from google.appengine.ext import ndb

slash = "/"
rootname = "root"

def obj_of_current_dir():
    return get_key_of_current_dir().get()

def get_key_of_current_dir():
    user = user_operations.get_user_for_model()
    return user.c_dir

def get_the_key_of_parent_directory():
    return get_key_of_current_dir().get().root_dir


def set_directory_root(my_user):
    directory_id = my_user.key.id() + slash
    directory = modelfolder(id=directory_id)

    directory.parent_directory = None
    directory.name = rootname
    directory.path = slash
    directory.put()

    my_user.root_directory = directory.key
    my_user.put()


def get_directories_in_current_path():
    return get_key_of_current_dir().get().directs


def get_total_directories_in_current_path():
    return len(get_key_of_current_dir().get().directs)


def is_in_root_directory():
    current_directory = obj_of_current_dir()
    return True if current_directory.root_dir is None else False


def getting_path(n, parent_dir_object):
    if is_in_root_directory():
        return parent_dir_object.path + n
    else:
        return parent_dir_object.path + "/" + n


def check_if_directory_is_empty(dir):
    return not dir.files and not dir.directs

def nocontain(key, list):
    return key not in list


def inlist(key, list):
    return True if key in list else False


def add_dir(name, parent):
    user = user_operations.get_user_for_model()
    parent_object = parent.get()
    p = getting_path(name, parent_object)
    id = user.key.id() + p
    dir = modelfolder(id=id)
    dir_key = dir.key

    if nocontain(dir_key, parent_object.directs):
        parent_object.directs.append(dir_key)
        parent_object.put()
        dir.root_dir = parent
        dir.name = name
        dir.path = p
        dir.put()
    else:
        print "Directory Exists"


def deleting_directory(name):
    my_user = user_operations.get_user_for_model()

    parent_directory_object = obj_of_current_dir()

    directory_id = my_user.key.id() + getting_path(name, parent_directory_object)
    directory_key = ndb.Key("Folder", directory_id)
    directory_object = directory_key.get()

    if check_if_directory_is_empty(directory_object):

        parent_directory_object.directs.remove(directory_key)
        parent_directory_object.put()
        directory_key.delete()


def home():
    user = user_operations.get_user_for_model()
    user.c_dir = ndb.Key("Folder", user.key.id() + slash)
    user.put()


def nav_dir(name):
    user = user_operations.get_user_for_model()
    path = user.key.id() + getting_path(name, obj_of_current_dir())
    key = ndb.Key("Folder", path)
    user.c_dir = key
    user.put()
