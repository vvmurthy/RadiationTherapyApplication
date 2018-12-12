import os
os.environ["DJANGO_SETTINGS_MODULE"] = './../../../dsrt/settings.py'
from upload.models import Patient, Study, Series
try:
	import CTImage,RPPlan,RTDose,RTStructureset
except ImportError:
	from .CTImage import *
	from .RPPlan import *
	from .RTDose import *
	from .RTStructureset import *
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib.auth.models import User
from UserProfile.models import UserProfile


import logging

type_dict = {
    'RTSTRUCT': RTStructureset,
    'RTDOSE': RTDose,
    'RTPLAN': RPPlan,
    'CT'    : CTImage
}

def make_patient(dicom_dataframe, patientName, profile):
    patient = Patient()
    patient.PatientName = str(patientName)
    patient.BirthDate = datetime.datetime.strptime(dicom_dataframe.PatientBirthDate, "%Y%m%d").date() if ("PatientBirthDate" in dicom_dataframe) and dicom_dataframe.PatientBirthDate else None
    patient.Gender = str(dicom_dataframe.PatientSex) if "PatientSex" in dicom_dataframe else None
    patient.EthnicGroup = str(dicom_dataframe.EthnicGroup) if "EthnicGroup" in dicom_dataframe else None
    patient.fk_hospital_id = profile.institution
    patient.save()
    return patient

def parse(dicom_dataframe,user_id,patientName):
    #do the first three step and call different method to do the different thing
    logging.info("Starting parsing now")

    user = User.objects.get(pk=user_id)
    profile = UserProfile.objects.get(user=user)
    try:
        patients = Patient.objects.get(PatientName = patientName)
        if not isinstance(patients, list):
            patients = [patients,]
        patient = None
        for patient_query in patients:
            if patient_query.fk_hospital_id == profile.institution:
                patient = patient_query
                break
        
        if patient == None:
            patient = make_patient(dicom_dataframe, patientName, profile)
    except ObjectDoesNotExist:
        print("creating new patient")
        patient = make_patient(dicom_dataframe, patientName, profile)

    logging.info("Parsing Study") 
    try:
        study = Study.objects.get(StudyInstanceUID = dicom_dataframe.StudyInstanceUID)
    except ObjectDoesNotExist:
        print("creating new study")
        study = Study()
        study.StudyInstanceUID = dicom_dataframe.StudyInstanceUID
        study.StudyDate = datetime.datetime.strptime(dicom_dataframe.StudyDate, "%Y%m%d").date() if ("StudyDate" in dicom_dataframe) and dicom_dataframe.StudyDate else None
        study.StudyDescription = str(dicom_dataframe.StudyDescription) if "StudyDescription" in dicom_dataframe else None
        study.TotalSeries = 0
        study.fk_patient_id = patient
        #study.TotalSeries += 1
        study.save()

    logging.info("Parsing Series")
    try:
        series = Series.objects.get(SeriesInstanceUID = dicom_dataframe.SeriesInstanceUID)
    except ObjectDoesNotExist:
        print("creating new series")
        series = Series()
        series.SeriesInstanceUID = dicom_dataframe.SeriesInstanceUID
        # series.SeriesDate = datetime.datetime.strptime(dicom_dataframe.Revi    ewDate,"%Y%m%d").date()
        series.SeriesDescription = str(dicom_dataframe.SeriesDescription) if "SeriesDescription" in dicom_dataframe else None
        series.SeriesType = dicom_dataframe.Modality
        series.Modality = dicom_dataframe.Modality
        series.SeriesNumber = dicom_dataframe.SeriesNumber
        series.PhysicianOfRecord = str(dicom_dataframe.PhysiciansOfRecord) if "PhysiciansOfRecord" in dicom_dataframe else None
        series.Manufacturer = str(dicom_dataframe.Manufacturer) if "Manufacturer" in dicom_dataframe else None
        series.fk_study_id = study
        series.fk_patient_id = patient
        series.save()

    print("processing data of modality: " + str(dicom_dataframe.Modality))
    res = type_dict[dicom_dataframe.Modality].parse(dicom_dataframe, user, patient, study, series)
    logging.info("Parsing completed. Starting OVH / STS extraction")
    if res:
        return study
    else:
        return None
