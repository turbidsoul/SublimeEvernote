#coding:utf-8
import os
import sys

# import markdown2
import sublime
import sublime_plugin

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
# from html import XHTML




consumer_key = 'oparrish-4096'
consumer_secret ='c112c6417738f06a'
evernoteHost = "www.evernote.com"
userStoreUri = "https://" + evernoteHost + "/edam/user"
temp_credential_request_uri = "https://" + evernoteHost + "/oauth"
resource_owner_authorization_uri = "https://" + evernoteHost + "/OAuth.action"
token_request_uri = "https://" + evernoteHost + "/oauth"


class SendToEvernoteCommand(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view
        self.window = sublime.active_window()
        self.settings = sublime.load_settings('SublimeEvernote.sublime-settings')

    # def to_markdown_html(self):
    #     region = sublime.Region(0, self.view.size())
    #     encoding = self.view.encoding()
    #     if encoding == 'Undefined':
    #         encoding = 'utf-8'
    #     elif encoding == 'Western (Windows 1252)':
    #         encoding = 'windows-1252'
    #     contents = self.view.substr(region)

    #     markdown_html = markdown2.markdown(contents, extras=['footnotes', 'fenced-code-blocks', 'cuddled-lists', 'code-friendly', 'metadata'])

    #     return markdown_html


    def send_note(self,**kwargs):
        
        dev_token = self.settings.get('dev_token')
        if not dev_token:
            sublime.message_dialog('dev_token is not setting. please go to https://www.evernote.com/api/DeveloperToken.action ')
            return

    def run(self, edit):
        self.send_note()
