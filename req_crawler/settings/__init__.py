# -*- coding: utf-8 -*-
import os
from importlib import import_module


__all__ = ['environ', 'settings']

environ = os.environ.get('REQ_CRAWLER_SETTINGS', 'req_crawler.settings.base')
settings = import_module(environ)
