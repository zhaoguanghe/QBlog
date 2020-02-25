"""
This script runs the QBlog application using a development server.
tornado托管flask,参考：https://blog.csdn.net/a3335581/article/details/87916234
"""

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from QBlog import app    #这里要和runflask.py对应

if __name__ == '__main__':
    server = HTTPServer(WSGIContainer(app))
    server.listen(5555) #flask默认的端口
    IOLoop.instance().start()