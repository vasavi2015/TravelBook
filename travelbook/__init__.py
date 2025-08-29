# Make PyMySQL behave like MySQLdb so we can use MySQL without native compilation.
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    # Local dev can still work with SQLite without PyMySQL.
    pass
