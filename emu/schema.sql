DROP TABLE IF EXISTS local_file;
DROP TABLE IF EXISTS hdfs_file;

CREATE TABLE local_file (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    f_name TEXT NOT NULL,
    f_type TEXT CHECK( f_type IN ('-', 'd') ) NOT NULL,
    f_size INTEGER DEFAULT 0 NOT NULL,
    f_permissions INTEGER DEFAULT 644 NOT NULL,
    f_parent_id INTEGER NOT NULL,
    last_edited DATETIME DEFAULT current_timestamp NOT NULL,
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
    last_edited DATETIME DEFAULT current_timestamp NOT NULL,
    data BLOB DEFAULT ''
);
