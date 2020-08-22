DROP TABLE IF EXISTS files;
DROP TABLE IF EXISTS env;

CREATE TABLE local_file (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    f_name TEXT NOT NULL,
    f_type TEXT CHECK( f_type IN ('-', 'd') ) NOT NULL,
    f_size INTEGER DEFAULT 0 NOT NULL,
    f_permissions INTEGER DEFAULT 644 NOT NULL,
    f_parent_id INTEGER NOT NULL,
    last_edited DATETIME DEFAULT 'now' NOT NULL,
    data BLOB DEFAULT ''
);

CREATE TABLE hdfs_file (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    u_id TEXT DEFAULT 'hadoop' NOT NULL,
    grp_id TEXT DEFAULT 'supergroup' NOT NULL,
    f_name TEXT NOT NULL,
    f_type TEXT CHECK( f_type IN ('-', 'd') ) NOT NULL,
    f_size INTEGER DEFAULT 0 NOT NULL,
    f_permissions INTEGER DEFAULT 644 NOT NULL,
    f_parent_id INTEGER NOT NULL,
    last_edited DATETIME DEFAULT 'now' NOT NULL,
    data BLOB DEFAULT ''
);

/* local root directory */
INSERT INTO local_file(f_name, f_type, f_parent_id)
VALUES (
    'root',
    'd',
    -1
)

/* hdfs root directory */
INSERT INTO hdfs_file(f_name, f_type, f_parent_id)
VALUES (
    'root',
    'd',
    -1
);

