import json

from aiohttp.test_utils import TestServer, TestClient, loop_context

from main import create_app


with open('news.json') as f:
    data = json.load(f)
    data['news'].sort(key=lambda k: k['id'])
    DELETED_NEWS = list(filter(lambda k: k['deleted'] == True, data['news']))[0]['id']
    MAX_ID_NEWS = data['news'][-1]['id']


with loop_context() as loop:
    app = loop.run_until_complete(create_app())
    client = TestClient(TestServer(app=app), loop=loop)
    loop.run_until_complete(client.start_server())

    async def test_get_route():
        resp = await client.get("/")
        assert resp.status == 200
        resp = await client.get("/%g" % DELETED_NEWS)
        assert resp.status == 404
        resp = await client.get("/%g" % (MAX_ID_NEWS + 1))
        assert resp.status == 404

    loop.run_until_complete(test_get_route())
    loop.run_until_complete(client.close())
