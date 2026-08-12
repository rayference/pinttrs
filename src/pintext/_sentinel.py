class _Nothing:
    """
    Sentinel used to detect unset arguments.

    A single instance of this class is exposed as :data:`NOTHING`.
    """

    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __repr__(self) -> str:
        return "NOTHING"

    def __bool__(self) -> bool:
        return False


#: Sentinel denoting an unset argument.
NOTHING = _Nothing()
