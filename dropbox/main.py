import jinja2
import os
import re
import webapp2
import display
from handler import blobstore
from handler import DownHandler, UpHandler
from model2 import Folder
import file_operations, user_operations, dir_operations
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HeadHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        if user_operations.checking_login():
            if not user_operations.present_user_in_model():
                user_operations.adding_new_user(user_operations.get_present_user())
            if self.request.get('directory_name') != '':
                dir_operations.nav_dir(self.request.get('directory_name'))
                self.redirect('/')

            directory_names = user_operations.getting_names(dir_operations.get_directories_in_current_path())
            name_of_file = user_operations.getting_names(file_operations.get_obj_of_current_file())
            size_of_file = user_operations.get_file_size(file_operations.get_obj_of_current_file())
            creating_file = user_operations.get_file_creation(file_operations.get_obj_of_current_file())
            file_kind = user_operations.get_file_kind(file_operations.get_obj_of_current_file())
            total_size_of_file = user_operations.get_total_totalsize(file_operations.get_obj_of_current_file())
            total_files = file_operations.get_numoffiles_in_live_path()
            total_directory = dir_operations.get_total_directories_in_current_path()
            length = len(name_of_file)

            url = user_operations.get_logout_url(self)

            template = JINJA_ENVIRONMENT.get_template('/template/main.html')
            self.response.write(template.render({'url': url,
                                                 'user': user_operations.get_present_user(),
                                                 'directories': directory_names,
                                                 'files': name_of_file,
                                                 'size' : size_of_file,
                                                 'create': creating_file,
                                                 'kind' : file_kind,
                                                 'len': length,
                                                 'totalSize':total_size_of_file,
                                                 'totalFiles': total_files,
                                                 'totalDirs': total_directory,
                                                 'current_path': dir_operations.obj_of_current_dir().path,
                                                 'is_not_in_root': not dir_operations.is_in_root_directory(),
                                                 'upload_url': blobstore.create_upload_url('/upload')}))

        else:
            url = user_operations.get_login_url(self)
            template = JINJA_ENVIRONMENT.get_template('/template/login.html')
            self.response.write(template.render({'url': url}))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        button_value = self.request.get('button')

        if button_value == 'Add':
            absolute_name = re.sub(r"[/;]", '', self.request.get('value')).lstrip()
            if not (absolute_name is None or absolute_name == ''):
                dir_operations.add_dir(absolute_name, dir_operations.get_key_of_current_dir())
            self.redirect('/')

        elif button_value == 'Delete':
            name, kind = self.request.get('name'), self.request.get('kind')
            if kind == 'file':
                file_operations.delete(name)
            elif kind == 'directory':
                dir_operations.deleting_directory(name)
            self.redirect('/')

        elif button_value == 'Up':
            user = user_operations.get_user_for_model()
            if not dir_operations.is_in_root_directory():
                user.c_dir = dir_operations.get_the_key_of_parent_directory()
                user.put()
            self.redirect('/')

        elif button_value == 'Home':
            user = user_operations.get_user_for_model()
            user.c_dir = ndb.Key(Folder, user.key.id() + dir_operations.slash)
            user.put()
            self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', HeadHandler),
    ('/upload', UpHandler),
    ('/download', DownHandler)
], debug=True)
