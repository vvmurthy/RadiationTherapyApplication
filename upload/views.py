# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import os
import shutil
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import MySQLdb as db
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dsrt.settings import STATIC_ROOT
from dsrt.settings import BASE_DIR
from UserProfile.models import UserProfile
import zipfile
import sys
import dicom

sys.path.append(BASE_DIR + '/upload/app/')
import glob
import dicomdb
from .tasks import uploader_task
from .models import Patient

@login_required(login_url='/users/login/')
def view_patient(request, slug):
    return HttpResponse("something")

@login_required(login_url='/users/login/')
def view_patients(request):
    hospital = "All Hospitals"
    if not request.user.is_superuser:
        profile = UserProfile.objects.get(user=request.user)
        patients = Patient.objects.filter(fk_hospital_id=profile.institution)
        hospital = profile.institution.name
    else:
        patients = Patient.objects.all()
    return render(request, "uploader/patients.html", {'patients':patients, 'hospital':hospital})

# Create your views here.
# Process the uploaded dicom files
# Store the information into the database
def processUploadedFile(raw_file_path, patientName, user_id):
    # the input is a zip file
    with zipfile.ZipFile(raw_file_path, 'r') as zipObject:  # create zipfile object
        # unzip the file in a folder named by patientName
        directory_extract_to = os.path.join(STATIC_ROOT, 'data', str(user_id), patientName)
        if not os.path.exists(directory_extract_to):
            os.makedirs(directory_extract_to)
        zipObject.extractall(directory_extract_to)
    # Process the dicom files to give the output

    rootDir = os.path.join(STATIC_ROOT, 'data', str(user_id),
                           patientName)  # set the directory you want to start from
    r = uploader_task.delay(rootDir, user_id, patientName)
    #r = uploader_task(rootDir, user_id, patientName)
    return r

@login_required(login_url='/users/login/')
def uploadForm(request):
    # Get the user upload the files
    # user = request.POST['user']
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':  # check whether a form has been submitted

        # Check that user has assigned hospital.
        if not profile.institution:
            return HttpResponse("Please enter hospital affiliation in options")
        patientName = request.POST['patientName']
        if not patientName:
            return HttpResponse("Please Enter Patient Name in left hand text box")
        uploadedFileObject = request.FILES['dcmZipFile']
        # send file object to new function for processing
        if not os.path.exists(os.path.join(STATIC_ROOT, 'raw')):
            os.mkdir(os.path.join(STATIC_ROOT, 'raw'))
        raw_file_path = os.path.join(STATIC_ROOT, 'raw', uploadedFileObject.name)
        # where the uploaded file is first stored

        (name, ext) = os.path.splitext(raw_file_path)
        if ext == '.zip':
            with open(raw_file_path, 'wb+') as destination:  # write the uploaded file to the raw directory
                for chunk in uploadedFileObject.chunks():
                    destination.write(chunk)
        else:
            return HttpResponse('Please Upload a zip file')

        # Does not handle no DICOM files being included in the zip file
        # raw_file_path is the zip file
        user_id = request.user.id
        res = processUploadedFile(raw_file_path, patientName, user_id)

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
        return render(request, 'uploader/uploader.html', {'hospital':profile.institution})
