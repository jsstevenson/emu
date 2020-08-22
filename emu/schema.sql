DROP TABLE IF EXISTS files;
DROP TABLE IF EXISTS env;

CREATE TABLE local_file (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    f_name TEXT NOT NULL,
    f_type TEXT NOT NULL,
    f_size INTEGER NOT NULL,
    f_permissions INTEGER NOT NULL,
    f_parent_id INTEGER NOT NULL,
    last_edited DATETIME NOT NULL,
    data BLOB
);

CREATE TABLE hdfs_file (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grp_id TEXT NOT NULL,
    f_name TEXT NOT NULL,
    f_type TEXT NOT NULL,
    f_size INTEGER NOT NULL,
    f_permissions INTEGER NOT NULL,
    f_parent_id INTEGER NOT NULL,
    last_edited DATETIME NOT NULL,
    data BLOB
)
