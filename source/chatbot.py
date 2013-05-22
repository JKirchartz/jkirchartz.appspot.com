import webapp2, re, httplib, time, random
import logging as log
from datetime import datetime
from urllib import urlencode
import libs.simplejson as json
from libs.pyquery import PyQuery as pq
from libs.untinyurl import untiny
from google.appengine.api import xmpp
from google.appengine.ext.webapp import xmpp_handlers

DEFAULT_MSG = "Hey, I'm KirchBot, Joel's robot assistant. What can I do for you?"
HELP_MSG    = "Hit up DuckDuckGo's 'Instant Answers' with \ddg <query>.\n"
HELP_MSG   += "Google it with \google <query>.\n"
HELP_MSG   += "Unshorten a url with \untiny <url>.\n"
HELP_MSG   += "Get a bukk.it image with \\bukkit <(optional, image name or extension)>.\n"
HELP_MSG   += "Roll the dice \\roll <sides (optional, default 6)>.\n"
WRONG_MSG   = "Sorry, You appear to be under the impression that I would "
WRONG_MSG  += "understand what you wanted me to do..."

HEADERS = {"User-agent":"KirchBot@jkirchartz.appspotchat.com, A Robot Assistant"}
BUKKIT = []

class XMPPHandler(xmpp_handlers.CommandHandler):

    def unhandled_command(self,message=None):
        message.reply(WRONG_MSG)

    def text_message(self,message=None):
        m_body = str(message.body)
        if re.match("^(hello|hi|hey|yo|help)",m_body.strip(), re.I):
            message.reply(DEFAULT_MSG+"\n\n"+HELP_MSG)
        else:
            message.reply(WRONG_MSG)

    def help_command(self,message=None):
        message.reply(HELP_MSG)

    def bukkit_command(self,message=None):
        m_body = str(message.body)[7:].strip()
        if len(BUKKIT) == 0:
            try:
                data = pq("http://bukk.it/")
                for img in data('tr > td > a'):
                    BUKKIT.append(img.attrib['href'])
            except Exception, e:
                log.error(e)
        if len(m_body) == 0:
            output = random.choice(BUKKIT)
        else:
            matching = [s for s in BUKKIT if m_body.upper() in s.upper()]
            if len(matching):
                output = random.choice(matching)
            else:
                output = " doesn't have anything like that..."

        message.reply("http://bukk.it/"+output);

    def roll_command(self,message=None):
        m_body = str(message.body)[5:].strip()
        random.seed(message.sender+str(datetime.now()))
        try:
            if re.match("\\d+",m_body):
                output = random.randrange(int(m_body))
            else:
                output = random.randrange(6)
        except Exception, e:
            output = "Oopsies, it rolled under the couch. Try again."
            log.error(e)

        message.reply(str(output))


    def google_command(self,message=None):
        m_body = str(message.body)[7:]
        output = "".join(["https://lmgtfy.com/?",
            urlencode({'q':m_body.strip()})])
        message.reply(output)

    def untiny_command(self,message=None):
        m_body = str(message.body)[7:]
        message.reply(untiny(m_body.strip()))

    def ddg_command(self,message=None):
        m_body = str(message.body)[4:].strip()
        params = urlencode({'q':m_body,'format':'json','no_html':1})
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
            output += "Uhh. IDK... Try going straight to the source:"

        if not data["Redirect"]:
            output += "\n"
            output += "".join(["https://duckduckgo.com/?",
                 urlencode({'q':m_body})])

        message.reply(output)


app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                            debug=True)
