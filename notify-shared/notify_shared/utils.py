import datetime as dt


def now(tz: dt.tzinfo | None = dt.UTC) -> dt.datetime:
    return dt.datetime.now(tz=tz)
