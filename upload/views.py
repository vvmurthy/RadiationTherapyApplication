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
from .models import Patient, Study, Series
import matplotlib
matplotlib.use('SVG')
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import json

PatientDirBase = os.path.join(STATIC_ROOT, 'data') 
ct_images = {}

def make_ct_image(current_ct, ct_block):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    fig.subplots_adjust(wspace=0, hspace=0)
    ax.imshow(ct_block[:, :, current_ct], cmap='gray')
    ax.axis('off')
    plt.tight_layout()
    img = BytesIO()
    fig.savefig(img, format="png", bbox_inches='tight', pad_inches=0, transparent=True)
    base = base64.b64encode(img.getvalue())
    return base 

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
def view_cts(request, slug, study_id, series_id):
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
    rootDir = os.path.join(PatientDirBase, slug, patient.PatientName)
    try:
        cts, _ = getImageBlock(rootDir, slug, study_id, series_id)
        ct_images[int(slug)] = cts
        current_ct = 0
        base = make_ct_image(current_ct, cts)
        return render(request, "uploader/patient.html", {"image":base, 
            "patient":patient.PatientName, "id":slug, "ct_index":current_ct})
    except AssertionError:
        return HttpResponse(500)

@login_required(login_url='/users/login/')
def scroll_cts(request):
    ct_index = request.GET.get("ct_index")
    delta = int(request.GET.get("delta"))
    id = int(request.GET.get("id"))
    ct_block = ct_images[id]

    if ct_block is not None:
        current_ct = int(ct_index) + delta
        if(current_ct == -1):
            current_ct = ct_block.shape[2] - 1
        elif(current_ct == ct_block.shape[2]):
            current_ct = 0
        
        base = make_ct_image(current_ct, ct_block)
        json_data = {}
        json_data["imgsrc"] = base.decode('utf-8')
        json_data["index"] = current_ct
        return JsonResponse(json_data)
    else:
        return HttpResponse(500)

@login_required(login_url='/users/login/')
def remove_ct(request):
    id = request.GET.get("id")
    del ct_images[int(id)] 
    return HttpResponse(200) 

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
        directory_extract_to = os.path.join(STATIC_ROOT, 'data', str(user_id), patientName)
        if not os.path.exists(directory_extract_to):
            os.makedirs(directory_extract_to)
        zipObject.extractall(directory_extract_to)
    # Process the dicom files to give the output
    r = uploader_task.delay(directory_extract_to, user_id, patientName)
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
