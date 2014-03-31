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
import threading


# import markdown2





consumer_key = 'oparrish-4096'
consumer_secret ='c112c6417738f06a'
evernoteHost = "www.evernote.com"
userStoreUri = "https://" + evernoteHost + "/edam/user"
temp_credential_request_uri = "https://" + evernoteHost + "/oauth"
resource_owner_authorization_uri = "https://" + evernoteHost + "/OAuth.action"
token_request_uri = "https://" + evernoteHost + "/oauth"


class EvernoteThread(threading.Thread):
    """docstring for EvernoteThread"""
    def __init__(self, action, token, cmd, notebook=None):
        super(EvernoteThread, self).__init__()
        self.action = action
        self.token = token
        self.cmd = cmd
        self.notebook = notebook

    def run(self):
        if self.action == 'load_notebooks':
            self.load_notebooks()
        elif self.action == 'send_note':
            self.send_note()

    def load_notebooks(self):
        ec = EvernoteClient(token=self.token)
        user = ec.get_user_store().getUser()
        sublime.status_message('Connected Evernote user: %s' % user.username)
        notestore = ec.get_note_store()
        notebooks = notestore.listNotebooks()
        notenames = []
        for notebook in notebooks:
            notenames.append(notebook.name)

        cmd = self.cmd
        def on_select(index):
            if index < 0:
                return
            notebook = notebooks[index]
            et = EvernoteThread('send_note', self.token, self.cmd, notebook=notebook)
            et.start()
            ProcessThread(et, "Sending to evernote", "Send to evernote success")

        cmd.window.show_quick_panel(notenames, on_select)

    def send_note(self):
        cmd = self.cmd
        ec = EvernoteClient(token=self.token)
        notestore = ec.get_note_store()
        notebook = self.notebook
        note = Note()
        note.title = cmd.view.name() if cmd.view.name() and len(cmd.view.name()) else os.path.split(cmd.view.file_name())[1]
        note.notebookGuid = notebook.guid
        note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>'

        _, ext = os.path.splitext(cmd.view.file_name())

        if ext in ['.md', '.markdown', '.mdown']:
            note.content += cmd.to_markdown_html()
        else:
            note.content += '<pre>'
            content = StringIO(cmd.view.substr(sublime.Region(0, cmd.view.size())))
            while True:
                line = content.readline()
                if not line:
                    break
                note.content += line
            note.content += '</pre>'
        note.content += '</en-note>'
        notestore.createNote(note)


class ProcessThread(threading.Thread):
    """docstring for ProcessThread"""
    def __init__(self, thread, message, success_message):
        super(ProcessThread, self).__init__()
        self.thread = thread
        self.message = message
        self.successs_message = success_message
        self.size = 8
        self.addend = 1
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if not self.thread.is_alive():
            sublime.status_message(self.successs_message)
            return
        before = i % self.size
        after = self.size - 1 - before
        sublime.status_message("%s [%s=%s]" % (self.message, ' ' * before, ' ' * after))

        if not after:
            self.addend = -1
        if not before:
            self.addend = 1
        i += self.addend
        sublime.set_timeout(lambda: self.run(i), 100)




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
        et = EvernoteThread('load_notebooks', dev_token, self)
        et.start()
        ProcessThread(et, 'Load Evernote Notebooks', 'Load evernote noteboosk success!')

    def run(self, edit):
        self.send_note()
