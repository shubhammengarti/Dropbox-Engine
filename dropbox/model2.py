from google.appengine.ext import ndb



class Folder(ndb.Model):

    name, path = ndb.StringProperty(), ndb.StringProperty()

    root_dir, directs, files = ndb.KeyProperty(), ndb.KeyProperty(repeated=True), ndb.KeyProperty(repeated=True)


class User(ndb.Model):
    root, c_dir = ndb.KeyProperty(), ndb.KeyProperty()
