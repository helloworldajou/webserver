import numpy as np
from PIL import Image
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC

import openface
from apiserver.models import FaceImage
from demos.classifier import align, net


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
        self.images = []
        self.users = ['unknown']
        self.svm = None

        dummy = "data/faces/raw/2jeonghan/2jeonghan-1.png"
        for i in range(5):
            self.processFrame(dummy, 0)

    def trainSVM(self, username):
        if username not in self.users:
            self.users.append(username)
        identity = self.users.index(username)

        face_images = FaceImage.objects.filter(user__username=username)
        files = map(lambda x: x.file.path, face_images)
        for file in files:
            self.processFrame(file, identity)

        print("+ Training SVM on {} labeled images.".format(len(files)))
        d = self.getData()

        if d is None:
            SVM = None
            print "d is None"
            return
        else:
            (X, y) = d
            numIdentities = len(set(y + [-1]))
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
        self.svm = GridSearchCV(SVC(C=1), param_grid, cv=5).fit(X, y)
        return

    def getData(self):
        X = []
        y = []
        for img in self.images:
            X.append(img.rep)
            y.append(img.identity)

        numIdentities = len(set(y + [-1])) - 1
        if numIdentities == 0:
            return None

        X = np.vstack(X)
        y = np.array(y)
        return (X, y)

    def processFrame(self, imagePath, identity=None):
        img = Image.open(imagePath)
        width, hegiht = img.size
        buf = np.fliplr(np.asarray(img))
        rgbFrame = np.zeros((hegiht, width, 3), dtype=np.uint8)
        rgbFrame[:, :, 0] = buf[:, :, 2]
        rgbFrame[:, :, 1] = buf[:, :, 1]
        rgbFrame[:, :, 2] = buf[:, :, 0]

        # bbs = align.getAllFaceBoundingBoxes(rgbFrame)
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
            self.images.append(Face(rep, identity))

            return rep

    def predict(self, imagePath):
        rep = self.processFrame(imagePath)
        return self.users[self.svm.predict(rep)[0]]


identifier = FaceIdentifier()