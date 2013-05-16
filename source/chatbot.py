import webapp2, re, httplib, time
import simplejson as json
import logging as log
from urllib import urlencode
from untinyurl import untiny
from google.appengine.api import xmpp
from google.appengine.ext.webapp import xmpp_handlers

DEFAULT_MSG = "Hey, I'm Joel's robot assistant. What can I do for you?"
HELP_MSG    = "Hit up DuckDuckGo's 'Instant Answers' with \ddg <query>.\n"
HELP_MSG   += "Google it with \google <query>. \n"
HELP_MSG   += "Unshorten a url with \untiny <url>."
WRONG_MSG   = "Sorry, You appear to be under the impression that I would "
WRONG_MSG  += "understand what you wanted me to do..."
HEADERS = {"User-agent":"jkirchartz@appspot.com, A Robot Assistant"}

class XMPPHandler(xmpp_handlers.CommandHandler):

    def unhandled_command(self,message=None):
        message.reply(WRONG_MSG);

    def text_message(self,message=None):
        m_body = str(message.body)
        if re.match("^(hello|hi|hey|yo|help|\\help)",m_body.strip(), re.I):
            message.reply(DEFAULT_MSG+" "+HELP_MSG)
        else:
            message.reply(WRONG_MSG)

    def google_command(self,message=None):
        m_body = str(message.body)[7:]
        output = "".join(["https://lmgtfy.com/?",
            urlencode({'q':m_body.strip()})])
        message.reply(output)

    def untiny_command(self,message=None):
        m_body = str(message.body)[7:]
        message.reply(untiny(m_body.strip()))

    def ddg_command(self,message=None):
        m_body = str(message.body)[4:]
        params = urlencode({'q':m_body.strip(),'format':'json'})
        conn = httplib.HTTPConnection('api.duckduckgo.com')
        output = ""
        try:
            conn.request('GET',"http://api.duckduckgo.com/?"+params,HEADERS)
            result = conn.getresponse()
            data = json.loads(str(result.read()))
        except Exception, e:
            log.error(e)

        if data["Answer"]:
            output += data["Answer"]
        elif data["Definition"]:
            output += data["Definition"]
        elif data["Redirect"]:
            output += data["Redirect"]
        else:
            output += "Uhh. IDK try again later or go straight to the source:"

        if not data["Redirect"]:
            output += "\n"
            output += "".join(["https://duckduckgo.com/?",
                urlencode({'q':m_body.strip()})])

        output = re.sub(r"<[^>]+>","",output)
        message.reply(output)


app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                            debug=True)
