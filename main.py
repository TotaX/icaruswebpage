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

class News(db.Model):
    number = db.StringProperty(required=True)
    month = db.StringProperty(required=True)
    link = db.StringProperty(required=True)
    title_link = db.StringProperty(required=True)
    desc = db.StringProperty()

class MainPage(webapp.RequestHandler):
    def get(self):        
        news_for_index = db.GqlQuery("SELECT * FROM News")
        template_values = {'lista_de_news': news_for_index}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path,template_values))

class AboutPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'about.html')
        self.response.out.write(template.render(path,None))

class PrivacyPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'privacy.html')
        self.response.out.write(template.render(path,None))

class GalleryPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'gallery.html')
        self.response.out.write(template.render(path,None))
        
class SitemapPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'sitemap.html')
        self.response.out.write(template.render(path,None))        

class ContactsPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'contacts.html')
        self.response.out.write(template.render(path,None))
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

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)

application = webapp.WSGIApplication(
                                     [  ('/', MainPage),
                                        ('/sitemap', SitemapPage),
                                        ('/about',AboutPage),
                                        ('/privacy',PrivacyPage),
                                        ('/contacts',ContactsPage),
                                        ('/gallery',GalleryPage),                                        
                                       LogSenderHandler.mapping()
                                      ],
                                     debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
