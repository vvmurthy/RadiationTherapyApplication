# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import os
import shutil
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import MySQLdb as db
from django.shortcuts import render, redirect
from users.models import User
from dsrt.settings import STATIC_ROOT
from dsrt.settings import BASE_DIR
import zipfile
import sys
import dicom

sys.path.append(BASE_DIR + '/upload/app/')
import glob
import dicomdb
from tasks import uploader_task


# Create your views here.
# Process the uploaded dicom files
# Store the information into the database
def processUploadedFile(raw_file_path, patientName, user):
    # the input is a zip file
    zipObject = zipfile.ZipFile(raw_file_path.encode('utf8'), 'r')  # create zipfile object
    # unzip the file in a folder named by patientName
    directory_extract_to = os.path.join(STATIC_ROOT, 'data', str(user.userid), patientName)
    if not os.path.exists(directory_extract_to):
        os.makedirs(directory_extract_to)
    zipObject.extractall(directory_extract_to)
    zipObject.close()
    # Process the dicom files to give the output

    rootDir = os.path.join(STATIC_ROOT, 'data', str(user.userid),
                           patientName)  # set the directory you want to start from
    r = uploader_task.delay(rootDir, user.id, patientName)
    return r


def uploadForm(request):
    # Get the user upload the files
    # user = request.POST['user']
    user = User.objects.get(pk=1)
    if request.method == 'POST':  # check whether a form has been submitted
        html = ''
        # !!we should let user to type in the name of the file
        patientName = request.POST['patientName']
        uploadedFileObject = request.FILES['dcmZipFile']
        # send file object to new function for processing
        raw_file_path = os.path.join(STATIC_ROOT, 'raw', uploadedFileObject.name)
        # where the uploaded file is first stored

        (name, ext) = os.path.splitext(raw_file_path)
        print(ext)
        if ext == '.zip':
            with open(raw_file_path, 'wb+') as destination:  # write the uploaded file to the raw directory
                for chunk in uploadedFileObject.chunks():
                    destination.write(chunk)
        else:
            return HttpResponse('Please Upload a zip file')

        # Does not handle no DICOM files being included in the zip file
        # raw_file_path is the zip file
        res = processUploadedFile(raw_file_path, patientName, user)

        # Delete the files in the raw folder
        folder_path = os.path.join(STATIC_ROOT, 'raw')

        for file_object in os.listdir(folder_path):
            file_object_path = os.path.join(folder_path, file_object)
            if os.path.isfile(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)

                # After do all things return a HTML　to front end
        # return HttpResponse("Upload \n {}, {}, {}".format(res.status,res.id,res.get()))
        return HttpResponse("upload successfully")
    else:
        return render(request, 'uploader/uploader.html')
