import re

from time import sleep

import aiomysql

INSECURE_PATTERNS = [
    "'\s+OR",
    "\d+=\d+",
    "--",
    r"/\*",
    "#",
    "CREATE",
    "SELECT",
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP"
]

INSECURE_PATTERNS = [re.compile(pattern, re.IGNORECASE)
                     for pattern in INSECURE_PATTERNS]


class SecurityException(Exception):
    pass


class DbException(Exception):
    pass


async def db_connect(loop):
    while True:
        try:
            return await aiomysql.create_pool(
                host='mysql',
                user='dbuser', password='zJ2plyhR9', db='cpanel',
                charset='utf8mb4',
                cursorclass=aiomysql.DictCursor,
                loop=loop
            )
        except Exception:
            sleep(10)


def assert_secure(user_input):
    for pattern in INSECURE_PATTERNS:
        match = pattern.search(user_input)
        if match:
            raise SecurityException(
                "Hacking attempt detected. "
                "Forbidden sequence found: {}".format(match.group()))


async def find_user(db, login, password):
    assert_secure(login)
    assert_secure(password)

    sql = "SELECT * FROM `users`" \
          "WHERE `login`='{}' AND `password`='{}'".format(login, password)
    try:
        async with db.get() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                return await cursor.fetchone()
    except Exception as e:
        raise DbException('Failed to execute query {}: {}'.format(sql, e))
