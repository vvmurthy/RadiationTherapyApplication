from upload.models import CTImages
from django.core.exceptions import ObjectDoesNotExist
import sys

def parse(dataframe, user, patient, study, series):
    try:
        Image = CTImages.objects.get(SOPInstanceUID=dataframe.SOPInstanceUID)
    except ObjectDoesNotExist:
        Image = CTImages()
        Image.SOPInstanceUID = dataframe.SOPInstanceUID
        Image.SOPClassUID = dataframe.SOPClassUID
        Image.ImageType = dataframe.ImageType
        Image.PhotometricInterpretation = dataframe.PhotometricInterpretation
        Image.RescaleSlope = dataframe.RescaleSlope
        Image.RescaleIntercept = dataframe.RescaleIntercept
        Image.SliceLocation = dataframe.SliceLocation
        Image.PixelSpacing = dataframe.PixelSpacing
        Image.ImageOrientationPatient = dataframe.ImageOrientationPatient
        Image.ImagePositionPatient = dataframe.ImagePositionPatient
        Image.SliceThickness = dataframe.SliceThickness
        Image.BodypartExamined = dataframe.BodyPartExamined
        Image.Rows = dataframe.Rows
        Image.Columns = dataframe.Columns
        Image.fk_series_id = series
        Image.fk_study_id = study
        Image.fk_patient_id = patient
        Image.fk_user_id = user
    try:
        Image.save()
    except:
        print sys.exc_info()
        return False

    return True
