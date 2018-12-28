#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging  # Log messages to file
import csv  # work with CSV files
from PIL import Image, ImageDraw, ImageFont  # image manipulations
from os import path  # files and directories operations


class Scribe:
    """
    Description:This is a simple class to create a text inside a image file,
    where the image file names, numbers and the text are in a csv file.
    Author: Marcos Angelo Molizane
    Date: 2016-08-02
    License> GPL V2
    """

    def __init__(self, location=""):
        self._path = location
        self._error = ""
        self._datafolder = "data"
        self._imgfolder = "original"
        self._imgprocfolder = "processed"
        self._fonts = "fonts"
        self._msg_no_name = "Sem identificação"
        logging.basicConfig(filename="Si.log", filemode="w", format="%(asctime)s [%(levelname)s] %(message)s"
                            , datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.DEBUG)

    def start(self, file="imagens.csv"):

        print("[INFO] Starting process Scribe imaginem")
        logging.info("Starting process Scribe imaginem")
        logging.info("Opening images data file: %s" % path.join(self._path, self._datafolder, file))

        if path.isfile(path.join(self._path, self._datafolder, file)):

            try:
                data = csv.reader(open(path.join(self._path, self._datafolder, file)), delimiter=';')
                # Jump the header line
                next(data)

                if data != "" or len(list(data)) > 0:

                    for line in data:

                        # Image that have x, X, 0 or 000 on first column doesn't will be processed
                        if line[1].lower() != "x" and line[1] != "0" and line[1] != "000":

                            if line[1] == "":
                                line[1] = self._msg_no_name

                            # print("Processing image \"%s.JPG\"" % line[0])
                            logging.info("Processing image \"%s.jpg\"" % line[0])

                            # verify image
                            self.write_text(line[1], line[0], line[0] + ".jpg", fontsize=75)

                            # Verify image files with " ([number])" in filename
                            terminate = False
                            i = 2

                            while terminate is False:

                                alternative_image = '{} ({}).jpg'.format(line[0], i)

                                if path.isfile(path.join(self._path, self._imgfolder, alternative_image)):
                                    self.write_text(line[1], line[0], alternative_image)
                                    i += 1
                                else:
                                    terminate = True
                else:
                    print("[ERROR] No image data file in: \"%s\"" % path.join(self._path, self._datafolder, file))
                    logging.error("No image data file in: \"%s\"" % path.join(self._path, self._datafolder, file))

            except Exception as ex:
                print("[ERROR] %s" % ex)
                logging.error("%s" % ex)

        else:
            print("[ERROR] Data file \"%s\" not found" % path.join(self._path, self._datafolder, file))
            logging.error("Data file \"%s\" not found" % path.join(self._path, self._datafolder, file))

        print("[INFO] Process ended")
        logging.info("Process ended")

    def write_text(self, text, number, image, bg="#ffffff", fg="#000000", font="timesi.ttf",
                           font_number="timesbd.ttf", fontsize=135):

        # verify image file excists
        if path.isfile(path.join(self._path, self._imgfolder, image)):

            # print("Formating image parameters \"%s\"" % image)
            logging.info("Formating parameters to image \"%s\"" % image)

            fnt = ImageFont.truetype(path.join(self._path, self._fonts, font), fontsize)
            fnt_n = ImageFont.truetype(path.join(self._path, self._fonts, font_number), fontsize)

            # Open image file
            img = Image.open(path.join(self._path, self._imgfolder, image))

            # Formating font size according with image size
            (img_x, img_y) = img.size
            (font_w, font_h) = fnt.getsize(text)
            (fontn_w, fontn_h) = fnt_n.getsize(number)

            # Draw the text on picture
            text_img = ImageDraw.Draw(img)

            # Create a rectangle on botton left (image name)
            # Note: left margin, x, wheight, top botton margins
            text_img.rectangle((0, img_y, font_w + 70, img_y - font_h - 25), fg)

            # Positioning text's name inside rectangle
            text_img.text((38, img_y - font_h - 25), text, font=fnt, fill=bg)

            # Create a rectangle on top right (image number)
            text_img.rectangle((img_x, fontn_h + 23, img_x - fontn_w - 28, 0), fg)

            # Positioning text's number inside rectangle
            text_img.text((img_x - fontn_w - 12, 0), number, font=fnt_n, fill=bg)

            # delete the altered image "object"
            del text_img

            # print("Saving new image \"%s\"" % path.join(self._path, self._imgprocfolder, image))
            logging.info("Saving new image \"%s\"" % path.join(self._path, self._imgprocfolder, image))

            # Save the altered image with a new name
            img.save(path.join(self._path, self._imgprocfolder, image), "JPEG", quality=80)
        else:
            logging.warn("Image file \"" + image + "\" not found")
            # print("File \"" + image + "\" not found")