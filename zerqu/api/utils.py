# coding: utf-8

from flask import request
from ..models import db
from ..errors import APIException


def int_or_raise(key, value=0, maxvalue=None):
    try:
        num = int(request.args.get(key, value))
        if maxvalue is not None and num > maxvalue:
            return maxvalue
        return num
    except ValueError:
        raise APIException(
            description='Require int type on %s parameter' % key
        )


def cursor_query(model, desc=True, filter_func=None):
    """Return a cursor query on the given model. The model must has id as
    the primary key.
    """
    cursor = int_or_raise('cursor', 0)
    count = int_or_raise('count', 20, 100)
    query = db.session.query(model.id)

    if cursor and desc:
        query = query.filter(model.id < cursor)
    elif cursor and not desc:
        query = query.filter(model.id > cursor)
    if filter_func:
        query = filter_func(query)

    if desc:
        query = query.order_by(model.id.desc())
    else:
        query = query.order_by(model.id.asc())

    ids = [i for i, in query.limit(count)]
    data = model.cache.get_many(ids)

    if len(data) < count:
        return data, 0

    cursor = data[-1].id
    return data, cursor


def pagination(total):
    page = int_or_raise('page', 1)
    if page < 1:
        raise APIException(description='page should be larger than 1')

    perpage = int_or_raise('perpage', 20, 100)
    if perpage < 10:
        raise APIException(description='perpage should be larger than 10')

    pages = int((total - 1) / perpage) + 1
    if page > pages:
        raise APIException(
            description='page should be smaller than total pages'
        )

    rv = {
        'total': total,
        'pages': pages,
        'page': page,
        'perpage': perpage,
        'prev': None,
        'next': None,
    }

    if page > 1:
        rv['prev'] = page - 1
    if page < pages:
        rv['next'] = page + 1
    return rv