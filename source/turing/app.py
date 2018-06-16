# coding: utf-8

import os
import sys
import logging
import threading

from traitlets.config import Application, catch_config_error
from .version import __version__
from traitlets import (
    Unicode, Integer, List, Instance, Bool
)

import orm
from sqlalchemy.orm import scoped_session

from tornado.log import app_log, access_log, gen_log
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.httpclient
import tornado.web
import tornado.gen
from ._data import DATA_FILES_PATH
from datetime import datetime
import signal
import atexit
from .log import CoroutineLogFormatter, log_request
from .routers import routers
from .traitlets_extend import URLPrefix

if sys.version_info[:2] < (3, 6):
    raise ValueError("Python < 3.6 not supported: %s" % sys.version)

common_aliases = {
    'log-level': 'Application.log_level',
    'f': 'Turing.config_file',
    'config': 'Turing.config_file',
    'db': 'Turing.neo4j_uri',
}

aliases = {
    'ip': 'Turing.ip',
    'port': 'Turing.port',
    'pid-file': 'Turing.pid_file',
    'log-file': 'Turing.extra_log_file',
}

token_aliases = {}
token_aliases.update(common_aliases)
aliases.update(common_aliases)

flags = {
    'debug': ({'Application': {'log_level': logging.DEBUG}},
              "set log level to logging.DEBUG (maximize logging output)"),
}


class Turing(Application):
    """An Application for starting a Multi-User server."""
    name = 'turing'
    version = __version__

    config_file = Unicode('config.py', config=True, help="The config file to load")

    db_url = Unicode("",
                     config=True, help="db_url connect to mysql")

    pid_file = Unicode('', config=True, help="""File to write PID""")

    base_url = URLPrefix('/', config=True, help="The base URL of the entire application")

    extra_log_file = Unicode('', config=True, help="Set a logging.FileHandler on this file.")

    extra_log_handlers = List(Instance(logging.Handler), config=True, help="Extra log handlers to set on logger")

    debug_switch = Bool(False, config=True, help="是否开启调试模式")

    listen_port = Integer(9050, config=True, help="The port for this process")
    listen_ip = Unicode('', config=True,  help="The ip for this process")

    data_files_path = Unicode(DATA_FILES_PATH, config=True, help="The location of data files")

    handlers = List()
    _log_formatter_cls = CoroutineLogFormatter
    http_server = None


    def _log_level_default(self):
        return logging.INFO

    def _log_datefmt_default(self):
        """Exclude date from default date format"""
        return "%Y-%m-%d %H:%M:%S"

    def _log_format_default(self):
        """override default log format to include time"""
        return "%(color)s[%(levelname)1.1s %(asctime)s.%(msecs)\
        .03d %(name)s %(module)s:%(lineno)d]%(end_color)s %(message)s"

    def init_logging(self):
        # This prevents double log messages because tornado use a root logger that
        # self.log is a child of. The logging module dipatches log messages to a log
        # and all of its ancenstors until propagate is set to False.
        self.log.propagate = False

        if self.extra_log_file:
            self.extra_log_handlers.append(
                logging.FileHandler(self.extra_log_file)
            )

        _formatter = self._log_formatter_cls(
            fmt=self.log_format,
            datefmt=self.log_datefmt,
        )
        for handler in self.extra_log_handlers:
            if handler.formatter is None:
                handler.setFormatter(_formatter)
            self.log.addHandler(handler)

        # hook up tornado 3's loggers to our app handlers
        for log in (app_log, access_log, gen_log):
            # ensure all log statements identify the application they come from
            log.name = self.log.name
        logger = logging.getLogger('tornado')
        logger.propagate = True
        logger.parent = self.log
        logger.setLevel(self.log.level)

    def write_pid_file(self):
        pid = os.getpid()
        if self.pid_file:
            self.log.debug("Writing PID %i to %s", pid, self.pid_file)
            with open(self.pid_file, 'w') as f:
                f.write('%i' % pid)

    def sigterm(self, signum, frame):
        self.log.critical("Received SIGTERM, shutting down")
        self.io_loop.stop()
        self.atexit()

    _atexit_ran = False

    def atexit(self):
        """atexit callback"""
        if self._atexit_ran:
            return
        self._atexit_ran = True
        # run the cleanup step (in a new loop, because the interrupted one is unclean)
        tornado.ioloop.IOLoop.clear_current()
        loop = tornado.ioloop.IOLoop()
        loop.make_current()
        loop.run_sync(self.cleanup)

    def init_signal(self):
        signal.signal(signal.SIGTERM, self.sigterm)

    @tornado.gen.coroutine
    def cleanup(self):
        """Shutdown our various subprocesses and cleanup runtime files."""
        # finally stop the loop once we are all cleaned up
        if self.pid_file and os.path.exists(self.pid_file):
            self.log.info("Cleaning up PID file %s", self.pid_file)
            os.remove(self.pid_file)

        self.log.info("...done安全退出")

    def init_db(self):
        self.session_factory = orm.new_session_factory(self.db_url, pool_recycle=3600)

    # thread-local storage of db objects
    _local = Instance(threading.local, ())

    @property
    def db(self):
        if not hasattr(self._local, "db"):
            self._local.db = scoped_session(self.session_factory)()
        return self._local.db

    def init_tornado_settings(self):
        """Set up the tornado settings dict."""
        version_hash = datetime.now().strftime("%Y%m%d%H%M%S")

        settings = dict(
            log_function=log_request,
            config=self.config,
            log=self.log,
            db=self.db,
            base_url=self.base_url,
            version_hash=version_hash,
            debug=self.debug_switch,
            jwt_secret="my_secret_key",
            jwt_algorithm='HS256',
            jwt_exp=600, #jwt有效期秒数
            jwt_option={
                'verify_signature': True,
                'verify_exp': True,
                'verify_nbf': False,
                'verify_iat': True,
                'verify_aud': False
            }
        )

        self.tornado_settings = settings

    def init_tornado_application(self):
        """Instantiate the tornado Application object"""
        # db.generate_mapping()
        self.tornado_application = tornado.web.Application(routers, **self.tornado_settings)

    @tornado.gen.coroutine
    @catch_config_error
    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.load_config_file(self.config_file, os.path.dirname(os.path.realpath(__file__)))
        self.init_logging()
        self.write_pid_file()
        self.init_db()
        self.init_tornado_settings()
        self.init_tornado_application()

    @tornado.gen.coroutine
    def start(self):
        """Start the whole thing"""

        # start the webserver
        self.http_server = tornado.httpserver.HTTPServer(self.tornado_application, xheaders=True)
        try:
            self.http_server.listen(self.listen_port, address=self.listen_ip)
        except Exception:
            self.log.error("Failed to bind to %s:%s", self.listen_ip, self.listen_port)
            raise
        else:
            self.log.info("listening on %s:%s", self.listen_ip, self.listen_port)

        self.log.info("now running at %s:%s", self.listen_ip, self.listen_port)
        # register cleanup on both TERM and INT
        atexit.register(self.atexit)
        self.init_signal()

    @tornado.gen.coroutine
    def launch_instance_async(self, argv=None):
        try:
            yield self.initialize(argv)
            yield self.start()
        except Exception as e:
            self.log.exception("")
            self.exit(1)

    @classmethod
    def launch_instance(cls, argv=None):
        self = cls.instance()
        io_loop = tornado.ioloop.IOLoop.current()
        io_loop.add_callback(self.launch_instance_async, argv)
        try:
            io_loop.start()
        except KeyboardInterrupt:
            print("\nInterrupted")


