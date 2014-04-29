#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Turbidsoul Chen
# @Date:   2013-11-19 14:47:00
# @Last Modified 2014-04-29

from evernote.api.client import EvernoteClient

dev_token = "S=s1:U=8d8b3:E=14baa1366de:C=14452623ae1:P=1cd:A=en-devtoken:V=2:H=4cf650744f76de023dc43d4b124d3e75"

ec = EvernoteClient(token=dev_token)
user = ec.get_user_store().getUser()
print(user.username)
note_store = ec.get_note_store()
notebooks = note_store.listNotebooks()
for notebook in notebooks:
    print(notebook.name)

