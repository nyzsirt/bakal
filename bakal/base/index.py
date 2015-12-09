#!/opt/python/bin/python -E
# -*- coding: utf-8 -*-

# import logging
# import os
# import socket
# import sys
# import pickle
# import fcntl
# import gc
# import settings
# import os
#
# import flask
# from flask import Flask
# from flask import g
# from flask import request
# from flask import session
# from flask import flash
# from flask import render_template
# from flask.ext.babel import gettext
# from flask.ext.babel import Babel, gettext, ngettext
#
# # utils
# from utils.generate_nav_actions import generate_nav_actions
#
# # controllers
# from bakal.controllers.hostname import HostnameController
# from bakal.controllers.gateway import GatewayController
# from bakal.controllers.bridge import BridgeController
# from bakal.controllers.dns import DNSController
# from bakal.controllers.dhcp import DHCPController
#
# # forms
# from bakal.forms.actions import ACTIONS
# from bakal.forms.hostname import HostnameForm
# from logger import logger

from bakal import app



# app.secret_key = os.urandom(24)
# babel = Babel(app)
#
# # update secret key on every start-up
# app.config.update(SECRET_KEY=os.urandom(24))
#
# # get environment variable for development mode
# if os.environ.get("env") == "development":
#     app.config.update(DEBUG=True)
#
# handler = logging.FileHandler(settings.LOGPATH)
# formatter = logging.Formatter(settings.LOGFORMAT)
# handler.setFormatter(formatter)
# handler.setLevel(logging.DEBUG)
# app.logger.addHandler(handler)

# @babel.localeselector
# def get_locale():
#     """try to guess the language from the user accept
#     header the browser transmits.
#     """
#     return request.accept_languages.best_match(["tr", "en"])

@app.route("/")
def root_redirection():
    """Redirect to main handler"""
    # redirection redirects to plain http URI
    # because of apache proxy
    return "Hello World"

# @app.errorhandler(500)
# def error_page(error):
#     """custom 500 page"""
#     flash(gettext(u"An error occured!"), "error")
#     return render_template("500.html", error=error
#         , error_code=500, nav={}, actions={}), 500
#
# @app.route("/wizard/", methods=("GET", "POST"))
# @app.route("/wizard/<action>", methods=("GET", "POST"))
# @app.route("/wizard/<action>/<interface>", methods=("GET", "POST"))
# def form(action="", interface=""):
#     """
#         URL distpatcher.
#         Get required parameters from URL & call appropriate
#         controller for relevant form
#         @param action: String (form name)
#         @param interface: String (eth1, eth2 ...)
#     """
#
#     if action == "heartbeat":
#         try:
#             #every heartbeat adds 2 seconds of alive duration
#             session["heartbeat"] += 2
#         except KeyError:
#             # status 200 means everything is okay and heartbeat connection should continue
#             session["heartbeat"] = 0
#             session["status"] = 200
#
#
#         responseobj = {} #Responseobj will be returned which will include status
#         if session["heartbeat"] >= 240:
#             #4 minutes is warning level to check if user is still using the wizard
#             # status 500 means heartbeat connection will be paused and user will choose to reset it or leave it.
#             responseobj["status"] = 500
#             session["status"] = 500
#         else:
#             responseobj["status"] = 200
#             session["status"] = 200
#
#         responseobj["lifetime"] = session["heartbeat"]
#
#         return flask.jsonify(responseobj)
#     elif action == "resetheartbeat":
#         session["heartbeat"] = 0
#         session["status"] = 200
#
#         return flask.jsonify({})
#
#
#     logging_prefix = "index.form"
#     logger.debug("{}: {}".format(logging_prefix, "Begin"))
#     try:
#         workingmode = session["workingmode"]
#     except KeyError:
#         # if workingmode is not set, try to read from saved form
#         if os.path.exists(os.path.join(settings.BASEPATH, "formsaves", "hostname")):
#             with open(os.path.join(settings.BASEPATH, "formsaves", "hostname"), "rb") as f:
#                 hostnameform = HostnameForm(pickle.load(f))
#             # set working mode from previous form submits
#             session["workingmode"] = hostnameform.workingmode.data.lower()
#             workingmode = session["workingmode"]
#         else:
#             workingmode = ""
#             if action not in ["", "hostname"]:
#                 flash(gettext(u"You need to set hostname first!"), "error")
#                 return form(action="hostname")
#     logger.debug("{}: {}".format(logging_prefix, "action: '{}', interface: '{}'".format(action, interface)))
#     controller = get_controller(action, interface, workingmode)
#     if request.method == "POST":
#         try:
#             view = controller.process_form()
#             # form processed successfuly, get the next form
#             if view[0]:
#                 logger.debug("{}: {}".format(logging_prefix, "len(view) = '{}'".format(len(view))))
#                 if len(view) == 2:
#                     return view[1]
#                 else:
#                     workingmode = session["workingmode"]
#                     next_action_name = generate_nav_actions(action, next_action_str=True)
#                     logger.debug("{}: {}".format(logging_prefix, "next_action_name = '{}'".format(next_action_name)))
#                     return get_controller(next_action_name, interface, workingmode).generate_view()
#             else:
#                 logger.debug("{}: {}".format(logging_prefix, "view[0] = '{}'".format(view[0])))
#         except Exception as e:
#             error_page(e)
#             logger.error(e)
#     else:
#         logger.debug("{}: {}".format(logging_prefix, "request.method = '{}'".format(request.method)))
#         if action == "success":
#             return render_template("success.html", actions=ACTIONS)
#     return controller.generate_view()
#
#
# def get_controller(action, interface, workingmode):
#     # ensure that action is defined in action list
#     if action in ACTIONS.keys():
#         # load required action controller
#         if action == "hostname":
#             # controller object includes required form logic
#             # returns required form views or process and validates forms
#             controller = HostnameController(action)
#         elif action == "gateway":
#             # if working mode is bridge, warn user
#             if workingmode == "bridge":
#                 flash(gettext(u"You are in Bridge mode currently"), "error")
#                 return HostnameController(action="hostname")
#             controller = GatewayController(action, interface)
#         elif action == "bridge":
#             # if working mode is gateway, warn user
#             if workingmode == "gateway":
#                 flash(gettext("You are in Gateway mode currently"), "error")
#                 return HostnameController(action="hostname")
#             controller = BridgeController(action)
#         elif action == "dns":
#             controller = DNSController(action)
#         elif action == "dhcp":
#             controller = DHCPController(action)
#         elif action == "filtering":
#             controller = FilteringController(action)
#     # if any action defined in URL or
#     # defined action does not exist
#     # use "hostname" as default action
#     else:
#         controller = HostnameController("hostname")
#     return controller
#
# @app.before_first_request
# def protect_file_descriptors():
#     # LSG-1857
#     for sock in filter(lambda x: type(x) == socket._socketobject, gc.get_objects()):
#         try:
#             fd = sock.fileno()
#         except IOError:
#             continue
#         old_flags = fcntl.fcntl(fd, fcntl.F_GETFD)
#         fcntl.fcntl(fd, fcntl.F_SETFD, old_flags | fcntl.FD_CLOEXEC)
#
# if __name__ == "__main__":
#     if os.environ.get("env") != "development":
#         pid = str(os.getpid())
#         if os.path.isfile(settings.PIDFILE):
#             with open(settings.PIDFILE, "r") as f:
#                 saved_pid = int(f.read())
#             if saved_pid != pid:
#                 print "%s already exists, exiting" % settings.PIDFILE
#                 sys.exit()
#         else:
#             with open(settings.PIDFILE, "w") as f:
#                 f.write(pid)
#     # main loop
#     app.run(host=settings.HOST, port=settings.PORT)
#     # terminate the server and remove PID file
#     if os.environ.get("env") != "development":
#         os.unlink(settings.PIDFILE)
