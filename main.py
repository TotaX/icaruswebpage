import os
import logging
import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext import db
from google.appengine.api import users


RANGO_DE_PROFILES = range(1,11)
class News(db.Model):
    number = db.StringProperty(required=True)
    month = db.StringProperty(required=True)
    link = db.StringProperty(required=True)
    title_link = db.StringProperty(required=True)
    desc = db.StringProperty()

class MainPage(webapp.RequestHandler):
    def get(self):        
        news_for_index = db.GqlQuery("SELECT * FROM News ORDER BY month,number DESC LIMIT 4")
        
        list_of_files = RANGO_DE_PROFILES
        #TEMPLTES VALUES FOR THE INDEX
        template_values = {
        'lista_de_news': news_for_index,
        'list_of_portfolio': list_of_files
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path,template_values))

class AboutPage(webapp.RequestHandler):
    def get(self):
                
        list_of_files = RANGO_DE_PROFILES
        #TEMPLTES VALUES FOR THE INDEX
        template_values = {
        'list_of_portfolio': list_of_files
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/about.html')
        self.response.out.write(template.render(path,template_values))

class PrivacyPage(webapp.RequestHandler):
    def get(self):
                
        list_of_files = RANGO_DE_PROFILES
        #TEMPLTES VALUES FOR THE INDEX
        template_values = {
        'list_of_portfolio': list_of_files
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/privacy.html')
        self.response.out.write(template.render(path,template_values))

class GalleryPage(webapp.RequestHandler):
    def get(self):
                
        list_of_files = RANGO_DE_PROFILES
        template_values = {
        'list_of_portfolio': list_of_files
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/gallery.html')
        self.response.out.write(template.render(path,template_values))
        
class SitemapPage(webapp.RequestHandler):
    def get(self):
        
        list_of_files = RANGO_DE_PROFILES
        template_values = {
        'list_of_portfolio': list_of_files
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/sitemap.html')
        self.response.out.write(template.render(path,template_values))        

class ContactsPage(webapp.RequestHandler):
    def get(self):
        list_of_files = RANGO_DE_PROFILES
        template_values = {
        'list_of_portfolio': list_of_files
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/contacts.html')
        self.response.out.write(template.render(path,template_values))
        
    def post(self):
        sender = 'fernando@icarusdev.com.ar'        
        subject = 'Contact from website'
        body = self.request.get('message')          
        message = mail.EmailMessage(sender=sender, subject=subject)
        message.to = 'contact@icarusdev.com.ar'
        message.body = body
        message.reply_to = self.request.get('email')
        message.send()
        self.redirect('/contacts')

#admin
class AddNewsPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if  users.is_current_user_admin():
                greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                            (user.nickname(), users.create_logout_url("/"))) 
                self.response.out.write("""
                <html><body>%s
                        <form action="" method="post" name="create_news">
                        <fieldset>
                            <div class="field">
                                <label for="title_link">Title:</label>
                                <input type="text" name="title_link" maxlength="100">
                            </div>
                            <div class="field">
                                <label for="link">Link:</label>
                                <input type="text" name="link">
                            </div>
                            <div class="field">
                                <label for="month">Month:</label>
                                <input type="text" name="month">
                            </div>
                            <div class="field">
                                <label for="day">Day Number:</label>
                                <input type="text" name="day">
                            </div>
                            <div class="field">
                                <label for="desc">Description:</label>
                                <textarea rows="10" cols="40" name="desc"></textarea>
                            </div>
                            <input type="submit" value="Save News">
                            </fieldset>
                        </form>
                    </body></html>
                            """ % greeting)
            else:
                    self.response.out.write("""<html><body>I'm sorry %s!, you don't have admin access.. 
                    try with your admin account (<a href=\"%s\">sign out</a>)</body></html>"""
                    %  (user.nickname(),users.create_logout_url("/")))
        else:
            greeting = ("<a href=\"%s\">Sign in or register</a>." % users.create_login_url("/addNews"))
            self.response.out.write("<html><body>%s</body></html>" % greeting )
            
    def post(self):
        title_link = self.request.get('title_link')
        link = self.request.get('link')
        month = self.request.get('month')
        day = self.request.get('day')
        desc = self.request.get('desc')
        newNews = News(number=day, desc=desc, month=month,link=link, title_link=title_link)
        newNews.put()
        

application = webapp.WSGIApplication(
                                     [  ('/', MainPage),
                                        ('/sitemap', SitemapPage),
                                        ('/about',AboutPage),
                                        ('/privacy',PrivacyPage),
                                        ('/contacts',ContactsPage),
                                        ('/gallery',GalleryPage),
                                        ('/addNews',AddNewsPage)
                                      ],
                                     debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
