import webapp2, re, logging
from urllib import urlencode
from untinyurl import untiny
from google.appengine.api import xmpp

class XMPPHandler(webapp2.RequestHandler):
    def ddg_command(self,message=None):
        logging.info(message)
        m_body = message.arg
        output = "https://ddg.gg/?"
        output += urlencode({'q':m_body.strip()[4:]})
        message.reply(output)

    def untiny_command(self,message=None):
        logging.info(message)
        m_body = message.arg
        output = untiny(m_body.strip[7:])
        message.reply(output)

    def post(self):
        message = xmpp.Message(self.request.POST)
        m_body = message.body
        if re.match("(hello|hi|hey|yo|help)",m_body, re.I):
            output = "Hey, I'm Joel's robot assistant. What can I do for you?"
            output += "\nGet a duckduckgo link with \ddg <query>.\nUn-shorten"
            output += " a url with \untiny <url>."

        message.reply(output)

app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                            debug=True)
