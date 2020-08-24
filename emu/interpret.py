from enum import Enum, auto
from emu.db import get_db
from flask import current_app, g, session
import re
from typing import Dict, List


def interpret(input: str) -> Dict[str, List[str]]:
    """
    Parse + execute given input
    Args:
        input : raw input from user

    Returns:
        dict (to be JSONified) containing line(s) of returned information
    """
    try:
        session["hdfs_wd"]
    except KeyError:
        session["hdfs_wd"] = 1
    try:
        session["local_wd"]
    except KeyError:
        session["local_wd"] = 1
    command_dispatch = [(re.compile("^hdfs dfs \-mkdir"), _hdfs_mkdir),
                        (re.compile("^hdfs dfs \-chown"), _hdfs_chown),
                        (re.compile("^hdfs dfs \-ls"), _hdfs_ls),
                        (re.compile("^hdfs dfs \-rm"), _hdfs_rm),
                        (re.compile("^help"), _help)]
    for (pattern, callback) in command_dispatch:
        match = re.match(pattern, input)
        if match:
            return {"lines": callback(input[match.end():])}
    return {"lines": [f"sh: Command {input.split(' ')[0]} not recognized"]}


def remove_spcs(input: str) -> str:
    while len(input) > 0 and input[0] == ' ':
        input = input[1:]
    while len(input) > 0 and input[-1] == ' ':
        input = input[:-1]
    return input


def _get_valid_file_path(path: str) -> int:
    """
    Validate file path and return its ID #
    Args:
        path: single string containing path to desired file
    Returns:
        file ID on success, None if path invalid
    """
    dirs = [d for d in path.split('/') if d != '']
    parent_id = 1
    db = get_db()
    check = None
    for dir in dirs:
        query = """SELECT id FROM hdfs_file
                WHERE id IS ? AND f_type IS 'd';"""
        check = db.execute(query, (parent_id,)).fetchone()
        if check is None:
            return None
        query = """SELECT id FROM hdfs_file
                WHERE f_name IS ? and f_parent_id IS ?;"""
        check = db.execute(query, (dir, parent_id)).fetchone()
        if check is None:
            return None
        parent_id = check['id']
    return check['id']


def _hdfs_make_one_dir(arg: str) -> str:
    """
    Helper function for _hdfs_mkdir(); processes a single arg (path),
    returns blank str on success, string w/ error message if dir path is
    invalid or already exists
    """
    db = get_db()
    parent_id = 1
    dirs = [d for d in arg.split('/') if d != '']
    for dir in dirs[:-1]:
        query = """SELECT id FROM hdfs_file
                WHERE f_name IS ? AND f_type IS 'd' AND f_parent_id IS ?;"""
        check = db.execute(query, (dir, parent_id)).fetchone()
        if check is None:
            return f"hdfs dfs -mkdir: {dir}: No such directory"
        parent_id = check["id"]

    query = """SELECT f_name FROM hdfs_file
            WHERE f_name IS ? AND f_parent_id IS ?;"""
    if db.execute(query, (dirs[-1], parent_id)).fetchone() is not None:
        return f"hdfs dfs -mkdir: {dirs[-1]}: File exists"

    query = """INSERT INTO hdfs_file
            (f_name, f_type, f_parent_id)
            VALUES
            (?, 'd', ?);"""
    db.execute(query, (dirs[-1], parent_id))
    db.commit()
    return ""


def _hdfs_mkdir(args: str) -> List[str]:
    """
    Make new directory in HDFS
    CLI usage: `hdfs dfs -mkdir [path/to/new/dir] ...`
    Args:
        args : a single string containing one or more valid paths to new dirs
    Returns:
        List of empty string or strings on success
    """
    args = remove_spcs(args)
    if len(args) < 1:
        return ["Usage: `hdfs dfs -mkdir [path/to/new/dir] ...`"]
    result = []
    for arg in args.split(' '):
        result.append(_hdfs_make_one_dir(arg))
    return result


def _hdfs_ls(args: str) -> List[str]:
    """
    Check contents of directory in HDFS
    CLI usage: `hdfs dfs -ls [/path/to/dir] ...`
    Args:
        args : single string containing one or more valid paths
    Returns:
        List of strings containing details of contents, or error msg on failure
    """
    args = remove_spcs(args)
    num_args = len([i for i in args.split(' ') if i != ''])
    db = get_db()
    if num_args > 1:
        return ["usage: `hdfs dfs -ls path`"]
    elif num_args == 0:
        query = """SELECT f_type, f_permissions, u_id, grp_id, f_size,
                last_edited, f_name FROM hdfs_file
                WHERE
                f_parent_id IS 1"""
        children = db.execute(query).fetchall()
        if len(children) > 0:
            results = [f"Found {len(children)} items"]
            results += [f"{c[0]} {c[1]} {c[2]} {c[3]} {c[4]} {c[5]} {c[6]}" for c in children]
            return results
        else:
            return [""]
    id = _get_valid_file_path(args)
    query = "SELECT f_type FROM hdfs_file WHERE id IS ?;"
    result = db.execute(query, (id,)).fetchone()
    if result is None:
        return [""]
    if result["f_type"] == "d":
        query = """SELECT f_type, f_permissions, u_id, grp_id, f_size,
                last_edited, f_name FROM hdfs_file
                WHERE
                f_parent_id IS ?"""
        children = db.execute(query, (id,)).fetchall()
        if len(children) > 0:
            results = [f"Found {len(children)} items"]
            results += [f"{c[0]} {c[1]} {c[2]} {c[3]} {c[4]} {c[5]} {c[6]}" for c in children]
            return results
        else:
            return [""]
    elif result["f_type"] == "-":
        query = """SELECT f_type, f_permissions, u_id, grp_id, f_size,
                last_edited, f_name FROM hdfs_file
                WHERE
                id IS ?"""
        file = db.execute(query, (id,)).fetchone()
        results = [f"""{file['f_type']} {file['f_permissions']}
                    {file['fu_id']} {file['grp_id']}, {file['f_size']}
                    {file['last_edited']} {file['f_name']}"""]
        return results
    else:
        return ["hdfs dfs -ls: invalid file type"]


def _hdfs_chown(args: str) -> List[str]:
    """
    Change ownership of file in HDFS
    CLI usage: `hdfs dfs -chown [username] [path/to/file]`
    Args:
        args: single string containing required args
    Returns:
        List of empty string upon success, List containing error msg on failure
    """
    args = remove_spcs(args).split(' ')
    if len(args) != 2:
        return ["Usage: `hdfs dfs -chown [username] [path/to/file]`"]
    id = _get_valid_file_path(args[1])
    if id is None:
        return ["sh: hdfs dfs -chown: invalid path"]
    query = """UPDATE hdfs_file SET u_id = ? WHERE id = ?;"""
    db = get_db()
    db.execute(query, (args[0], id))
    db.commit()
    return [""]

def _hdfs_rm(args: str) -> List[str]:
    """
    Delete file from HDFS
    CLI usage: `hdfs dfs -rm path/to/file`
    Args:
        args: single string containing path to file to delete
    Returns:
        Nothing upon success, error message on failure
    """
    args = remove_spcs(args)
    if len(args.split(' ')) != 1:
        return ["Usage: `hdfs dfs -rm path/to/file`"]
    id = _get_valid_file_path(args)
    if id is None:
        return ["sh: hdfs dfs -rm: invalid file path"]
    query = """DELETE FROM hdfs_file
            WHERE id IS ?;"""
    db = get_db()
    db.execute(query, (id,))
    db.commit()
    return [""]


def _help(args):
    results = ["emu help",
                "----------------------------",
                "Allowed commands:",
                "`hdfs dfs -mkdir [path/to/new/dir]: create new directory`",
                "`hdfs dfs -ls [path/to/file]`: list files or files in directory",
                "`hdfs dfs -chown [path/to/file]`: change ownership of file or directory",
                "`hdfs dfs -rm [path/to/file]`: remove file or directory",
                "`help [cmd]`: get help message for specific command, eg `help hdfs dfs -rm`"]
    args = remove_spcs(args)
    if args == '':
        return results
    elif args == 'hdfs dfs -mkdir':
        return [results[3]]
    elif args == 'hdfs dfs -ls':
        return [results[4]]
    elif args == 'hdfs dfs -chown':
        return [results[5]]
    elif args == 'hdfs dfs -rm':
        return [results[6]]
    elif args == 'help':
        return [results[7]]
    else:
        return ["sh: help: argument not recognized. enter `help` to see all commands"]
