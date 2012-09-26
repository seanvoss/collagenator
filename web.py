import tornado.ioloop
import tornado.web
import os
import Image
import urllib2
import StringIO
import time
import json
from multiprocessing import Process, Pool
from collage import Collage
import Image
import cStringIO
import re

THUMB_SIZE = 70, 70

def makethumb(arg,path='static/img',extension='.jpg'):
    path = 'static/img/'+str(arg[0])+'.jpg'
    orig = 'static/orig/'+str(arg[0])+'.jpg'
    if os.path.exists(path) and os.path.exists(orig):
        try:
            Image.open(path).verify()
            return
        except Exception, err:
            print err
            
    img = urllib2.urlopen(arg[1]).read()
    img = Image.open(StringIO.StringIO(img))
    img.save(orig)
    width, height = img.size

    if width > height:
       delta = width - height
       left = int(delta/2)
       upper = 0
       right = height + left
       lower = height
    else:
       delta = height - width
       left = 0
       upper = int(delta/2)
       right = width
       lower = width + upper

    img = img.crop((left, upper, right, lower))
    img.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(path)
    return 

class MainHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render('index.html');

    def post(self):
        keys = dict((k, self.get_argument(k)) for k in self.request.arguments )
        pool = Pool(3)
        p = pool.map(makethumb, keys.items(), 1)
        pool.close()
        pool.join()
        self.write(self.request.arguments)
class CollageHandler(tornado.web.RequestHandler):

    def post(self):
        print time.time()
        imgData = self.request.body.replace('data:image/png;base64,','')
        print time.time()
        tempimg = cStringIO.StringIO(imgData.decode('base64'))
        print time.time()

        im = Image.open(tempimg)
        path = 'static/collage/'+str(time.time())+'.jpg'
        im.save(path,quality=95)
        self.write(path)
        return
        #js = json.loads(self.request.body)
        #print js
        infiles = []
        for k,v in js.items():
            v["src"] = k
            infiles.append(v)
        self.write(Collage.build(infiles))
    def get(self):
       self.post()
    
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": False,
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/collage",CollageHandler),
], **settings)



if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
