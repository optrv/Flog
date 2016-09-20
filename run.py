from flog import app
app.run(debug = True, threaded = True)
# app.run(debug = True, processes = 4)

# Tornado
# from tornado.wsgi import WSGIContainer
# from tornado.httpserver import HTTPServer
# from tornado.ioloop import IOLoop
# from flog import app
# http_server = HTTPServer(WSGIContainer(app))
# http_server.listen(5000)
# IOLoop.instance().start()

# Gevent
# from gevent.wsgi import WSGIServer
# from flog import app
# http_server = WSGIServer(('', 5000), app)
# http_server.serve_forever()