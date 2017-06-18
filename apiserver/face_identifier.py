import numpy as np
import pickle
from PIL import Image
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC

import openface, redis
from cumera.celeryconf import app
from demos.classifier import align, net
from models import FaceImage
from redis_cli import REDIS_CONNECTION_POOL


class Face:
    def __init__(self, rep, identity):
        self.rep = rep
        self.identity = identity

    def __repr__(self):
        return "{{id: {}, rep[0:5]: {}}}".format(
            str(self.identity),
            self.rep[0:5]
        )


class FaceIdentifier:
    def __init__(self):
        self.users = ['unknown']
        self.__training = False
        self.r = redis.Redis(connection_pool=REDIS_CONNECTION_POOL)
        self.r.delete('images')
        dummy = "data/faces/raw/2jeonghan/2jeonghan-"
        for i in range(22):
            self.process_frame(dummy + str(i) + '.jpg', 'unknown')

    def train_svm(self, username):
        self.__training = True
        train_svm.delay()
        self.__training = False
        return

    @staticmethod
    def get_data(images):
        X = []
        y = []
        for img in images:
            X.append(img.rep)
            y.append(img.identity)

        numIdentities = len(set(y)) - 1
        if numIdentities == 0:
            return None

        X = np.vstack(X)
        y = np.array(y)

        return (X, y)

    @staticmethod
    def process_frame(image_path, identity=None):
        r = redis.Redis(connection_pool=REDIS_CONNECTION_POOL)
        img = Image.open(image_path)
        width, hegiht = img.size
        buf = np.fliplr(np.asarray(img))
        rgbFrame = np.zeros((hegiht, width, 3), dtype=np.uint8)
        rgbFrame[:, :, 0] = buf[:, :, 2]
        rgbFrame[:, :, 1] = buf[:, :, 1]
        rgbFrame[:, :, 2] = buf[:, :, 0]

        bb = align.getLargestFaceBoundingBox(rgbFrame)
        bbs = [bb] if bb is not None else []
        for bb in bbs:
            landmarks = align.findLandmarks(rgbFrame, bb)
            alignedFace = align.align(96, rgbFrame, bb,
                                      landmarks=landmarks,
                                      landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
            if alignedFace is None:
                print 'No aligned face'
                continue

            rep = net.forward(alignedFace)
            if identity is not None:
                r.rpush('images', pickle.dumps(Face(rep, identity)))
            return rep

    def predict(self, image_path):
        if self.__training:
            return 'training'

        rep = self.process_frame(image_path)
        svm = pickle.loads(self.r.get('classifier'))

        if rep is None or svm is None:
            return 'unknown'

        return svm.predict(rep)[0]


@app.task
def train_svm():
    r = redis.Redis(connection_pool=REDIS_CONNECTION_POOL)
    images = list(map(lambda i: pickle.loads(i), r.lrange('images', 0, -1)))
    print("+ Training SVM on {} labeled images.".format(len(images)))
    d = FaceIdentifier.get_data(images)

    if d is None:
        SVM = None
        print "d is None"
        return
    else:
        (X, y) = d
        numIdentities = len(set(y))
        if numIdentities < 1:
            print "Invalid training"
            return

    param_grid = [
        {'C': [1, 10, 100, 1000],
         'kernel': ['linear']},
        {'C': [1, 10, 100, 1000],
         'gamma': [0.001, 0.0001],
         'kernel': ['rbf']}
    ]

    svm_str = pickle.dumps(GridSearchCV(SVC(C=1), param_grid, cv=5).fit(X, y))
    r.set('classifier', svm_str)

identifier = FaceIdentifier()
