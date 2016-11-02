#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class LoginForm(forms.Form):
    user = forms.CharField()
    pwd = forms.CharField()
    code = forms.CharField()