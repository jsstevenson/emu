from enum import Enum, auto
from emu.db import get_db
from flask import current_app
import re

# TODO big
"""
How to initialize location in directory?
"""


class Interpreter(object):
    def __init__(self, working_dir=[1], hdfs_working_dir=[1], setup_sql=None):
        """
        Constructor function.

        Args:
          * working_dir: List of file IDs (ints) corresponding to initial dir.
          * hdfs_working_dir: Same as working_dir.
            By default, root dirs in both local and HDFS should have ID 1.
          * setup_sql: String, path to prewritten sql initialization
        """
        self.working_dir = working_dir
        self.hdfs_working_dir = hdfs_working_dir
        self.current_input = None
        self.command_dispatch = {
                re.compile("^hdfs dfs \-mkdir"): self._hdfs_mkdir,
                re.compile("^hdfs dfs \-chown"): self._hdfs_chown,
                re.compile("^hdfs dfs \-put"): self._hdfs_put,
                re.compile("^hdfs dfs \-get"): self._hdfs_get,
                re.compile("^hdfs dfs \-ls"): self._hdfs_ls,
                re.compile("^hdfs dfs \-cat"): self._hdfs_cat,
                re.compile("^hdfs dfs \-help"): self._hdfs_help
                }
        if setup_sql:
            with current_app.open_resource(setup_sql) as f:
                get_db().executescript(f.read().decode('utf8'))


    def interpret(self, input):
        self.current_input = input
        for cmd in self.command_dispatch:
            match = re.match(cmd[0], self.current_input)
            if match:
                self.current_input = self.current_input[match.end():]
                return cmd[1]()


    def _hdfs_mkdir(self):
        """
        HDFS command `mkdir`
        User-facing args:
            [path] : (required) full relative path of directory to make
        """
        return Exception


    def _hdfs_chown(self):
        return Exception


    def _hdfs_put(self):
        return Exception


    def _hdfs_get(self):
        return Exception


    def _hdfs_ls(self):
        return Exception


    def _hdfs_cat(self):
        return Exception


    def _hdfs_help(self):
        return Exception


    def _ls(self, args):
        """
        UNIX command `ls`
        Args:
            args: String (can be empty)
        User-facing args:
            [file] : file/directory to list from
        """
        db = get_db()
        children = (get_db()
                .execute(
                "SELECT f.file_name FROM files f WHERE f.file_parent_id = ?",
                (self.working_dir,)
                ).fetchall())
