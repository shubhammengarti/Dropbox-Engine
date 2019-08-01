import jinja2
import os
import user_operations

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



def give_error(self, url,error):
    template = JINJA_ENVIRONMENT.get_template('/template/error.html')
    self.response.write(template.render({'url': url,'error': error}))
