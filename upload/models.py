# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from users.models import User
import dicom
# Create your models here.
class Patient(models.Model):
    class Meta:
        db_table = 'patients'
    PatientName = models.CharField(max_length=200)
    BirthDate = models.DateField(null=True)
    Gender = models.CharField(max_length=20,null=True)
    EnthicGroup = models.CharField(max_length=200,null=True)
    fk_user_id = models.ForeignKey(User)

class Study(models.Model):
    class Meta:
        db_table = 'studies'
    StudyInstanceUID = models.CharField(max_length=200)
    StudyDate = models.DateField(null=True)
    StudyDescription = models.CharField(max_length=200,null=True)
    TotalSeries = models.IntegerField()
    fk_patient_id = models.ForeignKey(Patient)
    fk_user_id = models.ForeignKey(User)

class Series(models.Model):
    class Meta:
        db_table = 'series'
    SeriesInstanceUID = models.CharField(max_length=200)
    SeriesDate = models.DateField(null=True)
    SeriesDescription = models.CharField(max_length=200,null=True)
    SeriesType = models.CharField(max_length=100)
    Modality = models.CharField(max_length=100)
    SeriesNumber = models.CharField(max_length=100,null=True)
    PhysicianOfRecord = models.CharField(max_length=100,null=True)
    Manufacturer = models.CharField(max_length=50,null=True)
    fk_study_id = models.ForeignKey(Study)
    fk_patient_id = models.ForeignKey(Patient)
    fk_user_id = models.ForeignKey(User)

class CTImages(models.Model):
    class Meta:
        db_table = 'ct_images'
    SOPInstanceUID = models.CharField(max_length=200)
    SOPClassUID = models.CharField(max_length=100)
    ImageType = models.CharField(max_length=100)
    PhotometricInterpretation = models.CharField(max_length=20,null=True)
    RescaleSlope = models.IntegerField()
    RescaleIntercept = models.IntegerField()
    SliceLocation = models.IntegerField()
    PixelSpacing = models.CharField(max_length=50)
    ImageOrientationPatient = models.CharField(max_length=100)
    ImagePositionPatient = models.CharField(max_length=100)
    SliceThickness = models.CharField(max_length=100)
    BodypartExamined = models.CharField(max_length=100)
    Rows = models.IntegerField()
    Columns = models.IntegerField()
    fk_series_id = models.ForeignKey(Series)
    fk_study_id = models.ForeignKey(Study)
    fk_patient_id = models.ForeignKey(Patient)
    fk_user_id = models.ForeignKey(User)

class RTStructureSet(models.Model):
    class Meta:
        db_table = 'rt_structureset'
    SOPInstanceUID = models.CharField(max_length=200)
    SOPClassUID = models.CharField(max_length=100)
    TotalROIs = models.IntegerField()
    fk_series_id = models.ForeignKey(Series)
    fk_study_id = models.ForeignKey(Study)
    fk_patient_id = models.ForeignKey(Patient)
    fk_user_id = models.ForeignKey(User)

class RTROI(models.Model):
    class Meta:
        db_table = 'rt_rois'
    ROIName = models.CharField(max_length=100)
    ROIDisplayColor = models.CharField(max_length=100)
    ROINumber = models.CharField(max_length=10)
    Volume = models.FloatField()
    TotalContours = models.IntegerField()
    fk_structureset_id = models.ForeignKey(RTStructureSet)

class RTContour(models.Model):
    class Meta:
        db_table = 'rt_contour'
    ContourGeometricType = models.CharField(max_length=100)
    NumberOfContourPoints = models.IntegerField()
    ContourData = models.TextField()
    ReferencedSOPClassUID = models.CharField(max_length=100)
    ReferencedSOPInstanceUID = models.CharField(max_length=100)
    fk_roi_id = models.ForeignKey(RTROI)
    fk_structureset_id = models.ForeignKey(RTStructureSet)

class RTDose(models.Model):
    class Meta:
        db_table = 'rt_dose'
    SOPClassUID = models.CharField(max_length=100)
    SOPInstanceUID = models.CharField(max_length=100)
    DoseGridScaling = models.CharField(max_length=100)
    DoseSummationType = models.CharField(max_length=100,null=True)
    DoseType = models.CharField(max_length=100,null=True)
    DoseUnits = models.CharField(max_length=100,null=True)
    ReferencedRTPlanSequence = models.CharField(max_length=100)
    ReferencedStructureSetSequence = models.CharField(max_length=100)
    fk_series_id = models.ForeignKey(Series)
    fk_study_id = models.ForeignKey(Study)
    fk_patient_id = models.ForeignKey(Patient)
    fk_user_id = models.ForeignKey(User)

class RTDoseImage(models.Model):
    class Meta:
        db_table = 'rt_dose_image'
    Columns = models.IntegerField()
    Rows = models.IntegerField()
    ImageOrientationPatient = models.CharField(max_length=20)
    ImagePositionPatient = models.CharField(max_length=20)
    PhotometricInterpretation = models.CharField(max_length=20,null=True)
    PixelSpacing = models.CharField(max_length=20)
    NumberOfFrames = models.IntegerField()
    ImageData = models.TextField()
    fk_dose_id = models.ForeignKey(RTDose)
    fk_series_id = models.ForeignKey(Series)
    fk_study_id = models.ForeignKey(Study)
    fk_patient_id = models.ForeignKey(Patient)
    fk_user_id = models.ForeignKey(User)

class RTDVH(models.Model):
    class Meta:
        db_table = 'rt_dvh'
    DVHDoseScaling = models.CharField(max_length=20)
    DVHMaximumDose = models.FloatField()
    DVHMeanDose = models.FloatField()
    DVHMinimumDose = models.FloatField()
    DVHNumberOfBins = models.IntegerField()
    DVHReferencedROI = models.CharField(max_length=10)
    DVHType = models.CharField(max_length=10,null=True)
    DVHVolumeUnits = models.CharField(max_length=10)
    DoseType = models.CharField(max_length=10)
    DoseUnits = models.CharField(max_length=10)
    DVHData = models.TextField()
    fk_dose_id = models.ForeignKey(RTDose)
    fk_series_id = models.ForeignKey(Series)
    fk_study_id = models.ForeignKey(Study)
    fk_patient_id = models.ForeignKey(Patient)
    fk_user_id = models.ForeignKey(User)


class RTIsDose(models.Model):
    class Meta:
        db_table = 'rt_isdose'

    RowPosition = models.TextField()
    ColumnPosition = models.TextField()
    IsDoseValue = models.IntegerField()
    fk_ct_image_id = models.ForeignKey(CTImages)
    fk_dose_id = models.ForeignKey(RTDose)
    fk_series_id = models.ForeignKey(Series)
    fk_study_id = models.ForeignKey(Study)
    fk_patient_id = models.ForeignKey(Patient)
