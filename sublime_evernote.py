#coding:utf-8
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import markdown2
import sublime
import sublime_plugin
from evernote.api.client import EvernoteClient
from evernote.edam.type.ttypes import Note
from io import StringIO

# import markdown2

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

    def to_markdown_html(self):
        region = sublime.Region(0, self.view.size())
        encoding = self.view.encoding()
        if encoding == 'Undefined':
            encoding = 'utf-8'
        elif encoding == 'Western (Windows 1252)':
            encoding = 'windows-1252'
        contents = self.view.substr(region)
        markdown_html = markdown2.markdown(contents, extras=['footnotes', 'fenced-code-blocks', 'cuddled-lists', 'code-friendly', 'pyshell'])
        return markdown_html


    def send_note(self,**kwargs):
        dev_token = self.settings.get('dev_token')
        if not dev_token:
            sublime.error_message('dev_token is not setting, please go to "https://www.evernote.com/api/DeveloperToken.action" get a dev token.')
            return
        ec = EvernoteClient(token=dev_token)
        userstore = ec.get_user_store()
        user = userstore.getUser()
        sublime.status_message('Connected Evernote user: %s' % user.username)
        notestore = ec.get_note_store()
        notebooks = notestore.listNotebooks()
        notenames = []
        for notebook in notebooks:
            notenames.append(notebook.name)

        def on_select(index):
            notebook = notebooks[index]
            note = Note()
            note.title = self.view.name() if self.view.name() and len(self.view.name()) else os.path.split(self.view.file_name())[1]
            note.notebookGuid = notebook.guid
            note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
            note.content += '<en-note>'

            _, ext = os.path.splitext(self.view.file_name())

            if ext in ['.md', '.markdown', '.mdown']:
                note.content += self.to_markdown_html()
            else:
                note.content += '<pre>'
                content = StringIO(self.view.substr(sublime.Region(0, self.view.size())))
                while True:
                    line = content.readline()
                    if not line:
                        break
                    note.content += line
                note.content += '</pre>'
            note.content += '</en-note>'
            notestore.createNote(note)

        self.window.show_quick_panel(notenames, on_select)

    def run(self, edit):
        self.send_note()
