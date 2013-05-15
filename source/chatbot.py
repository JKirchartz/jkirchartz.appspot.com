import webapp2, re, logging
from urllib import urlencode
from untinyurl import untiny
from google.appengine.api import xmpp
from google.appengine.ext.webapp import xmpp_handlers

DEFAULT_MSG = "Hey, I'm Joel's robot assistant. What can I do for you?"
HELP_MSG    = "Get a duckduckgo link with \ddg <query>.\n"
HELP_MSG   += "Unshorten a url with \untiny <url>."
WRONG_MSG   = "Sorry, I don't get what you want me to do..."

class XMPPHandler(xmpp_handlers.CommandHandler):

    def unhandled_command(self,message=None):
        logging.warn(message)
        message.reply(WRONG_MSG);

    def text_message(self,message=None):
        logging.warn(message)
        m_body = str(message.body)
        if re.match("^(hello|hi|hey|yo|help)",m_body.strip(), re.I):
            message.reply(DEFAULT_MSG+" "+HELP_MSG)
        else:
            message.reply(WRONG_MSG)

    def ddg_command(self,message=None):
        logging.warn(message)
        m_body = str(message.body)[4:]
        output = "".join(["https://ddg.gg/?",
            urlencode({'q':m_body.strip()})])
        message.reply(output)

    def untiny_command(self,message=None):
        logging.warn(message)
        m_body = str(message.body())[7:]
        message.reply(untiny(m_body.strip()))

app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                            debug=True)
