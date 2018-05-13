import asyncio
import logging
import uuid
from hashlib import md5

import jinja2
from aiohttp import web
from aiohttp_jinja2 import setup as jinja_setup, render_template
from db import db_connect, find_user, SecurityException, DbException

from flags import task_ids, flags


def generate_token():
    return str(uuid.uuid4())


class IndexView(web.View):
    def __init__(self, request, team_id):
        super().__init__(request)
        self.team_id = team_id

    @property
    def tokens(self):
        return self.request.app['tokens']

    @property
    def current_token(self):
        return self.tokens.get(self.team_id, None)

    @property
    def db(self):
        return self.request.app['db']

    async def get(self):
        if 'token' in self.request.query:
            token = generate_token()
            self.tokens[self.team_id] = token
            self.log_request('Generated token: {}'.format(token))
            return web.Response(text=token)

        response = render_template('index.html', self.request, None)
        return response

    async def post(self):
        form = None
        try:
            form = await self.request.post()

            user_token = form.get('token', None)
            login = form.get('login', None)
            password = form.get('password', None)

            if not self.current_token or self.current_token != user_token:
                self.log_with_form(
                    form, 'Token mismatch: expected {}'.format(self.current_token))
                return web.HTTPFound(self.request.path)

            if not login or not password:
                self.log_with_form(form, 'Bad request')
                return web.Response(text='Bad request', status=400)

            self.tokens[self.team_id] = None

            password = md5(password.encode()).hexdigest()
            user = await find_user(self.db, login, password)

            if not user:
                raise PermissionError('Неверный логин или пароль')

            flag = flags[self.team_id]
            self.log_with_form(form, 'Success, flag is {}'.format(flag))

            return render_template(
                'success.html', self.request, {'flag': flag })

        except (PermissionError, SecurityException, DbException) as e:
            self.log_with_form(form, 'Fail, error is {}'.format(e))
            return render_template(
                'index.html', self.request, {'error': str(e)})

        except Exception:
            self.log_with_form(form, 'Unexpected exception', method=logging.exception)
            raise

    @classmethod
    @web.middleware
    async def team_middleware(cls, request, handler):
        if handler != cls:
            return await handler(request)
        task_id = request.match_info.get('task_id', None)
        team_id = task_ids.index(task_id) if task_id in task_ids else None
        if team_id is None:
            return web.Response(text='Not found', status=404)
        else:
            return await handler(request, team_id)

    def log_request(self, message, method=logging.info):
        method('Team: {}. {}'.format(self.team_id, message))

    def log_with_form(self, form, message='', method=logging.info):
        self.log_request('Form: {}. {}'.format(repr(form), message), method)


async def spawn_app(loop=None):
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] [%(levelname)s] %(message)s)'
    )
    if not loop:
        loop = asyncio.get_event_loop()
    app = web.Application(middlewares=[IndexView.team_middleware])

    jinja_setup(app, loader=jinja2.FileSystemLoader('./templates/'))

    app.router.add_view('/{task_id}/', IndexView)
    app.router.add_static('/static/', path='./static')

    app['tokens'] = {}
    app['db'] = await db_connect(loop)

    return app


async def main(loop):
    app = await spawn_app(loop)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)
    await site.start()
    print("Started")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.run_forever()
