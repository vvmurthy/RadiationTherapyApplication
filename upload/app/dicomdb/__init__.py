import os
os.environ["DJANGO_SETTINGS_MODULE"] = './../../../dsrt/settings.py'
from upload.models import Patient, Study, Series
import CTImage,RPPlan,RTDose,RTStructureset
from django.core.exceptions import ObjectDoesNotExist
import datetime
type_dict = {
    'RTSTRUCT': RTStructureset,
    'RTDOSE': RTDose,
    'RTPLAN': RPPlan,
    'CT'    : CTImage
}
def parse(dicom_dataframe,user,patientName):
    #do the first three step and call different method to do the different thing
    try:
        patient = Patient.objects.get(PatientName = patientName )
    except ObjectDoesNotExist:
        print("creating new patient")
        patient = Patient()
        patient.PatientName = str(patientName)
        patient.BirthDate = datetime.datetime.strptime(dicom_dataframe.PatientBirthDate, "%Y%m%d").date()
        patient.Gender = str(dicom_dataframe.PatientSex)
        patient.EthnicGroup = str(dicom_dataframe.EthnicGroup)
        patient.fk_user_id = user
        patient.save()
    try:
        study = Study.objects.get(StudyInstanceUID = dicom_dataframe.StudyInstanceUID)
    except ObjectDoesNotExist:
        #print("creating new study")
        study = Study()
        study.StudyInstanceUID = dicom_dataframe.StudyInstanceUID
        study.StudyDate = datetime.datetime.strptime(dicom_dataframe.StudyDate, "%Y%m%d").date()
        study.StudyDescription = dicom_dataframe.StudyDescription
        study.TotalSeries = 0
        study.fk_patient_id = patient
        study.fk_user_id = user
        #study.TotalSeries += 1
        study.save()

    try:
        series = Series.objects.get(SeriesInstanceUID = dicom_dataframe.SeriesInstanceUID)
    except ObjectDoesNotExist:
        #print("creating new series")
        series = Series()
        series.SeriesInstanceUID = dicom_dataframe.SeriesInstanceUID
        # series.SeriesDate = datetime.datetime.strptime(dicom_dataframe.Revi    ewDate,"%Y%m%d").date()
        series.SeriesDescription = dicom_dataframe.SeriesDescription
        series.SeriesType = dicom_dataframe.Modality
        series.Modality = dicom_dataframe.Modality
        series.SeriesNumber = dicom_dataframe.SeriesNumber
        series.PhysicianOfRecord = dicom_dataframe.PhysiciansOfRecord
        series.Manufacturer = dicom_dataframe.Manufacturer
        series.fk_study_id = study
        series.fk_patient_id = patient
        series.fk_user_id = user
        series.save()

    res = type_dict[dicom_dataframe.Modality].parse(dicom_dataframe,user,patient,study,series)
    return res