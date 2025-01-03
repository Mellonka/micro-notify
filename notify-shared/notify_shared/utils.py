import datetime as dt


def now(tz: dt._TzInfo | None = dt.UTC) -> dt.datetime:
    return dt.datetime.now(tz=tz)
