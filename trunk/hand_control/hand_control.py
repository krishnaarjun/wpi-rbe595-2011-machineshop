#!/usr/bin/python

# Copyright (c) 2011, Aaron Fineman
# Based off code by Roman Stanchak and Nirav Patel (http://eclecti.cc)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import os
import opencv
from opencv import cv
from opencv import highgui

haar_file = '../haar/1256617233-1-haarcascade_hand.xml'
#size = cv.cvSize(640, 480)
size = cv.cvSize(1280, 800)
camera = highgui.cvCreateCameraCapture(0)

def detectObject(image):
  grayscale = cv.cvCreateImage(size, 8, 1)
  #cv.cvFlip(image, None, 1)
  cv.cvCvtColor(image, grayscale, cv.CV_BGR2GRAY)
  storage = cv.cvCreateMemStorage(0)
  cv.cvClearMemStorage(storage)
  cv.cvEqualizeHist(grayscale, grayscale)
  cascade = cv.cvLoadHaarClassifierCascade(haar_file, cv.cvSize(1,1))
  objects = cv.cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2, 
                                   cv.CV_HAAR_DO_CANNY_PRUNING,
                                   cv.cvSize(100,100))

  if objects:
    for i in objects:
      cv.cvRectangle(image, cv.cvPoint( int(i.x), int(i.y)),
                     cv.cvPoint(int(i.x+i.width), int(i.y+i.height)),
                     cv.CV_RGB(0,255,0), 3, 8, 0)

def get_image():
  img = highgui.cvQueryFrame(camera)
  #img = opencv.cvGetMat(img)
  return opencv.adaptors.Ipl2PIL(img)

def main():
  highgui.cvNamedWindow("Guardian", 1)
  while True:
    image = highgui.cvQueryFrame(camera)
    detectObject(image)
    highgui.cvShowImage("Guardian", image)

    if highgui.cvWaitKey(20) != -1:
      break
  highgui.cvDestroyWindow("Guardian")

if __name__ == "__main__":
  main()
