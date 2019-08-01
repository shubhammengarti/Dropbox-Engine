import re

from google.appengine.api import users as ndbusers
from model2 import User
from google.appengine.ext import ndb
import dir_operations as fromdir_operations
from model2 import Folder as modelfolder
import model as File


def get_present_user():
    return ndbusers.get_current_user()

def get_user_for_model():
    user = get_present_user()
    if user:
        user_key = ndb.Key("User", user.user_id())
        return user_key.get()

def checking_login():
    if get_present_user():
        return True
    else:
        return False

def present_user_in_model():
    if get_user_for_model():
        return True
    else:
        return False


def adding_new_user(user):
    my_user = User(id=user.user_id())
    fromdir_operations.set_directory_root(my_user)

    my_user.c_dir = ndb.Key("Folder", my_user.key.id() + fromdir_operations.slash)
    my_user.put()

def getting_names(items):
    names = list()

    for item in items:
        names.append(item.get().name)
    return names


def get_file_size(files):
    size = list()
    for e in files:
        size.append(File.get_file_size(e.get().blob))
    return size


def get_total_totalsize(files):
    totalsize = 0;
    for e in files:
        totalsize += File.get_file_size(e.get().blob)
    return totalsize;


def get_file_creation(files):
    size = list()
    for e in files:
        size.append(File.get_file_creation(e.get().blob))
    return size


def get_file_kind(files):
    size = list()
    for e in files:
        size.append(File.get_file_type(e.get().blob))
    return size


def sort_list(list):
    return sorted(list, key=lambda item: item.get().name.lower())


def get_login_url(main_page):
    return ndbusers.create_login_url(main_page.request.uri)


def get_logout_url(main_page):
    return ndbusers.create_logout_url(main_page.request.uri)
