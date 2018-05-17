import pyodbc


class SlateDB:
    """
    Wrapper for a Slate ODBC connection.
    """

    def __init__(self, server, port, db, username, password, driver=None):
        self._driver = driver or pyodbc.drivers()[-1]
        self._server = server
        self._port = port
        self._host = "{}, {}".format(self._server, self._port)
        self._db = db
        self._username = username
        self._password = password
        self._conn_parms = parms = {'driver': self._driver,
                                    'server': self._host,
                                    'uid': self._username,
                                    'pwd': self._password}

    def select(self, sql: str, binds: tuple = None, max_rows: int or None = None, as_dict: bool = False):
        """
        Execute the given select sql.

        Parameters
        ----------
        sql : str
            A valid sql statement.
        binds : tuple
            A tuple of any bind variables to use in the prepared sql.
        max_rows : int or None
            The maximum number of rows to retrieve. If none, all rows will be returned.
        as_dict : bool
            If True, results will be returned as dicts. Otherwise they will be returned as pyodbc rows.

        Yields
        -------
        results : generator
            A generator of results as either a native pyodbc Row or as a dict.

        Examples
        --------
        >>> db = SlateDB("server", "port", "db", "username", "password")
        >>> for row in db.select("select * from people"):
        >>>     print(row.id, row.name)
        "1234 Kent, Clark"
        "1544 Wayne, Bruce"
        >>> db.select("select * where name = ?", binds=("Your Name",))
        # yield all rows matching "Your Name"
        >>> db.select("select * where name = ?", binds=("Your Name",), max_rows=10)
        # yield first 10 rows matching "Your Name"
        >>> list(db.select("select * from person where last = ?", ("Smith",), as_dict=True))
        [
            {"id": "123456", "last": "Smith", "first": "John", ...},
            {"id": "15484", "last": "Smith", "first": "Bob", ...},
            ...
        ]
        """
        with pyodbc.connect(**self._conn_parms) as db:
            with db.cursor() as c:
                if binds:
                    c.execute(sql, binds)
                else:
                    c.execute(sql)
                if max_rows:
                    i = 0
                    while i <= max_rows:
                        results = c.fetchmany(1)
                        if not results:
                            break
                        else:
                            i += 1
                            if as_dict:
                                yield self._todict(results[0])
                            else:
                                yield results[0]
                else:
                    while True:
                        results = c.fetchmany(1)
                        if not results:
                            break
                        else:
                            if as_dict:
                                yield self._todict(results[0])
                            else:
                                yield results[0]
    @staticmethod
    def _todict(row):
        return dict(zip([x[0] for x in row.cursor_description], row))