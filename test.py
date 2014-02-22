#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Turbidsoul Chen
# @Date:   2013-11-19 14:47:00
# @Last Modified by:   Turbidsoul Chen
# @Last Modified time: 2014-02-22 16:06:45

from evernote.api.client import EvernoteClient



key = 'kick191'
secret = '17a3c38e0749bf5e'
sandbox_auth_token = 'S=s1:U=8d8b3:E=14baa1366de:C=14452623ae1:P=1cd:A=en-devtoken:V=2:H=4cf650744f76de023dc43d4b124d3e75'
product_auth_token = 'S=s25:U=29e3c4:E=14baa4564fc:C=14452943904:P=1cd:A=en-devtoken:V=2:H=0dac7129124e3b3109e11e1468a0df5c'


sandbox_base_url = 'https://sandbox.evernote.com'
product_base_url = 'https://www.evernote.com'

if __name__ == '__main__':
    ec = EvernoteClient(token=sandbox_auth_token)
    notestore = ec.get_note_store()
    for nb in notestore.listNotebooks():
        print(nb.name)