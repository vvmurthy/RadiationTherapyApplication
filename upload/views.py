# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import os
import shutil
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
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
from dicomdb.utils import getImageBlock
from .tasks import uploader_task
from .models import *
import matplotlib
matplotlib.use('SVG')
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import json

PatientDirBase = os.path.join(STATIC_ROOT, 'data') 


@login_required(login_url='/users/login/')
def view_studies(request, slug):
    """
    API call to view the patient's studies

    slug : str
        The patient ID of the patient whose dashboard to query
    """
    patient = Patient.objects.get(id=slug)
    studies = Study.objects.filter(fk_patient_id=slug)
    return render(request, "uploader/studies.html", {"studies":studies, 
        "patient":patient.PatientName, "patient_id":slug})

@login_required(login_url='/users/login/')
def view_series(request, slug, study_id):
    """
    API call to view the patient's CT series

    slug : str
        The patient ID of the patient whose dashboard to query
    study_id : str
        Patient study id to view
    """
    patient = Patient.objects.get(id=slug)
    studies = Study.objects.get(fk_patient_id=slug, id=study_id)
    series = Series.objects.filter(fk_patient_id=slug, fk_study_id=study_id, Modality="CT")
    return render(request, "uploader/series.html", {"series":series, 
        "patient":patient.PatientName, "patient_id":slug, "study_id":study_id})

@login_required(login_url='/users/login/')
def view_patient(request, slug, study_id, series_id):
    """
    API call to view the patient details

    slug : str
        The patient ID of the patient whose dashboard to query
    study : str
        The study ID for the patient to query the dashboard
    series : str
        The series ID for the patient to query in the dashboard
    """
    patient = Patient.objects.get(id=slug)
    rootDir = os.path.join(PatientDirBase, patient.PatientName)
    try:
        # Get the DVH pane names as well
        rois = []
        study = Study.objects.get(id=study_id)
        series = Series.objects.get(id=series_id)
        rt_rois = RTDVH.objects.filter(fk_study_id=study, fk_patient_id=patient)

        # Get number of CTs
        number_of_cts = CTImages.objects.filter(fk_study_id=study, fk_patient_id=patient, fk_series_id=series)

        for roi_raw in rt_rois:
            roi = roi_raw.DVHReferencedROI
            roi_info = {}
            roi_original = roi.roi_id
            roi_info["name"] = roi_original.ROIName
            roi_info["rt_roi_id"] = roi.id
            rois.append(roi_info)
        return render(request, "uploader/patient.html", {
            "patient":patient.PatientName, "id":slug,
            "rois":rois, "study":study_id, "series":series_id, "number_of_cts":number_of_cts})
    except AssertionError:
        return HttpResponse(status=500)
 

@login_required(login_url='/users/login/')
def view_patients(request):
    hospital = "All Hospitals"
    if not request.user.is_superuser:
        profile = UserProfile.objects.get(user=request.user)
        patients = Patient.objects.filter(fk_hospital_id=profile.institution)
        if profile.institution is not None:
            hospital = profile.institution.name
        else:
            hospital = "No hospital selected"
    else:
        patients = Patient.objects.all()
    return render(request, "uploader/patients.html", {'patients':patients, 'hospital':hospital})

@login_required(login_url="/users/login/")
def find_similar(request):
    
    # Get all patient similarities in similarities table
    # send them to frontend
    return HttpResponse()


# Create your views here.
# Process the uploaded dicom files
# Store the information into the database
def processUploadedFile(raw_file_path, patientName, user_id):
    # the input is a zip file
    with zipfile.ZipFile(raw_file_path, 'r') as zipObject:  # create zipfile object
        # unzip the file in a folder named by patientName
        directory_extract_to = os.path.join(STATIC_ROOT, 'data')
        if not os.path.exists(directory_extract_to):
            os.makedirs(directory_extract_to)
        zipObject.extractall(directory_extract_to)
    # Process the dicom files to give the output
    r = uploader_task(os.path.join(directory_extract_to, raw_file_path.split("/")[-1].split(".zip")[0]), user_id, patientName)
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

        for file_object in sorted(os.listdir(folder_path))[::-1]:
            file_object_path = os.path.join(folder_path, file_object)
            if os.path.isfile(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)

                # After do all things return a HTML　to front end
        # return HttpResponse("Upload \n {}, {}, {}".format(res.status,res.id,res.get()))
        return render(request, 'uploader/uploader.html', {'hospital':profile.institution, "response_message":
            "upload successful"})
    else:
        return render(request, 'uploader/uploader.html', {'hospital':profile.institution})
