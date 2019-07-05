import json
from datetime import datetime

from aiohttp import web

with open('news.json', 'r') as f:
    NEWS = json.load(f)

with open('comments.json', 'r') as f:
    COMMENTS = json.load(f)


async def news(request):
    _id = request.match_info.get('id', False)
    date_now = datetime.now().isoformat(sep='T')

    data = NEWS.copy()
    comments = COMMENTS.copy()
    data['news'].sort(key=lambda k: k['date'])
    data['news'] = list(filter(lambda k: k['date'] <= date_now and not k['deleted'],
                               data['news'])
                        )
    for news in data['news']:
        news['comments_count'] = len(list(filter(lambda k: k['news_id'] == news['id'],
                                                 comments['comments']))
                                     )
    if _id:
        data['news'] = list(filter(lambda k: k['id'] == int(_id),
                                   data['news'])
                            )
        if not data['news']:
            raise web.HTTPNotFound()
        news_comments = list(filter(lambda k: k['news_id'] == int(_id),
                                    comments['comments']))
        news_comments.sort(key=lambda k: k['date'])
        data['news'][0]['comments'] = news_comments

    else:
        data['news_count'] = len(data['news'])
    return web.Response(text=str(data))


if __name__ == '__main__':
    app = web.Application()

    app.add_routes([web.get('/', news),
                    web.get('/{id}', news),
                    ])

    web.run_app(app)
