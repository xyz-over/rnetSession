import asyncio
import json
import rnet
from rnet import Client, Emulation, HeaderMap, Jar, Cookie

session = None
async def ClientSession():
    global session
    if session is None:
        session = Client(emulation=Emulation.Chrome142)
    return session
StringToJson = json.loads

class Response:
    def __init__(self, content: bytes,resp: rnet.Response):
        self.content = content
        self.headers = resp.headers
        self._cookies = resp.cookies
        self.cookies = {}
        self.text = None
        self._json = None

        try:
            self.text = content.decode('utf-8')
        except:pass
        try:
            if self.text:
                self._json = json.loads(self.text)
        except:pass

        for cookie in self._cookies:
            self.cookies[cookie.name] = cookie.value

    def json(self):
        return self._json

class tools:
    def __init__(self):pass

    async def initData(self,headers,data,json,proxy) -> dict:
        info = {
            'form':None,
            'body':None,
            'data':data,
            'headers':await self.getHeaders(headers),
            'json':json,
            'proxy':proxy
        }
        if info['proxy']:
            if 'http://' not in info['proxy']:
                info['proxy'] = 'http://' + info['proxy']
            info['proxy'] = rnet.Proxy.http(info['proxy'])
        if type(info['data']) is dict:
            info['form'] = await tool.getData(info['data'])
        elif type(info['data']) is bytes or type(info['data']) is str:
            info['body'] = info['data']
        return info

    async def getHeaders(self,headers:dict):
        h = HeaderMap()
        if headers is None:
            return h
        for key,value in headers.items():
            h.insert(key, value)
        return h
    async def getData(self,data:dict):
        arr=[]
        if data is None:
            return None
        if type(data) is dict:
            for key, value in data.items():
                arr.append((key, value))
            return arr
        return data
tool = tools()

async def get(url,headers=None,cookies=None,params=None,data=None,timeout=30,proxy=None):
    return await request(url,headers=headers,cookies=cookies,params=params,data=data,json=None,timeout=timeout,proxy=proxy,method='GET')

async def post(url,headers=None,cookies=None,params=None,data=None,json=None,timeout=30,proxy=None):
    return await request(url,headers=headers,cookies=cookies,params=params,data=data,json=json,timeout=timeout,proxy=proxy,method='POST')

async def request(url,**kwargs):
    session = await ClientSession()
    reqInfo = await tool.initData(kwargs.get('headers'),kwargs.get('data'),kwargs.get('json'),kwargs.get('proxy'))
    kwargs.update(reqInfo)
    if kwargs.get('method')=='POST':
        await session.post(url=url,)
        resp = await session.post(url, **kwargs)
    else:
        resp = await session.get(url, **kwargs)
    return Response(await resp.bytes(), resp)

