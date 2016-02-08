#!/usr/bin/env python2.7
# coding=utf8

from __future__ import unicode_literals, print_function

from FaceRecognition import *


def save_face(src_file, dest_filename):
    img = Image()
    position = img.cut_face(src_file)
    print(position)
    rect = tuple(position[0])

    img.face_roi('cut.png', rect)
    fina = img.resize(img.read('cut.png'), (100, 100))
    img.save(dest_filename, fina)

