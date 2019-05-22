#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  This file is part of the `pypath` python module
#
#  Copyright
#  2014-2019
#  EMBL, EMBL-EBI, Uniklinik RWTH Aachen, Heidelberg University
#
#  File author(s): Dénes Türei (turei.denes@gmail.com)
#                  Nicolàs Palacio
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: http://pypath.omnipathdb.org/
#

import random
import os
import sys

import pypath.log as log


class Session(object):
    """
    PyPath session object. Contains mainly the session ID and the
    logger.

    :arg str label:
        Optional, ``None`` by default. Sets the session name/ID. If none
        is passed, generates a random 5 character ID.
    :arg int log_verbosity:
        Optional, ``0`` by default. Sets the level of verbosity for the
        logger.

    :var str label:
        The session name/ID.
    :var int log_verbosity:
        The level of log verbosity.
    :var log pypat.log.Logger:
        Instance of the logger object.
    :var str logfile:
        The file name recording the log messages.
    """

    def __init__(self, label=None, log_verbosity=0):

        self.label = label or self.gen_session_id()
        self.log_verbosity = log_verbosity
        self.start_logger()
        self.log.msg('Session `%s` started.' % self.label)


    @staticmethod
    def gen_session_id(length=5):
        """
        Generates a string of alphanumeric characters randomly.

        :arg int length:
            Optional, ``5`` by default. The length of the random string.

        :returns:
            (**str**) -- A random alphanumeric string of defined length.
        """

        abc = '0123456789abcdefghijklmnopqrstuvwxyz'

        return ''.join(random.choice(abc) for i in range(length))


    def start_logger(self):
        """
        Creates a logger for this session which will be served to all
        modules.
        """

        self.logfile = 'pypath-%s.log' % self.label
        self.log = log.Logger(self.logfile, verbosity = self.log_verbosity)


    def __del__(self):

        self.log.msg('Session `%s` finished.' % self.label)


class Logger(object):


    def __init__(self, name = None):

        self._log_name = name or self.__class__.__name__
        self._logger = get_log()


    def _log(self, msg = '', level = 0):
        """
        Writes a message into the logfile.
        """

        self._logger.msg(msg = msg, label = self._log_name, level = level)


    def _console(self, msg = ''):
        """
        Writes a message to the console and also to the logfile.
        """

        self._logger.console(msg = msg, label = self._log_name)


def get_session():
    """
    Creates new session or returns the one already created.
    """

    mod = sys.modules[__name__]

    if not hasattr(mod, 'session'):

        new_session()

    return sys.modules[__name__].session


def get_log():
    """
    Returns the ``log.Logger`` instance belonging to the session.
    """

    return get_session().log


def new_session(label = None, log_verbosity = 0):
    """
    Creates a new session. In case one already exists it will be deleted.

    Parameters
    ----------
    label : str
        A custom name for the session.
    log_verbosity : int
        Verbositiy level passed to the logger.
    """

    mod = sys.modules[__name__]

    if hasattr(mod, 'session'):

        delattr(mod, 'session')

    setattr(mod, 'session', Session(label, log_verbosity))
