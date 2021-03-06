from upload.models import CTImages
from django.core.exceptions import ObjectDoesNotExist
import sys
import numpy as np

def parse(dataframe, user, patient, study, series):
    try:
        Image = CTImages.objects.get(SOPInstanceUID=dataframe.SOPInstanceUID)
    except ObjectDoesNotExist:
        Image = CTImages()
        Image.SOPInstanceUID = dataframe.SOPInstanceUID
        Image.SOPClassUID = dataframe.SOPClassUID
        Image.ImageType = dataframe.ImageType
        Image.PhotometricInterpretation = dataframe.PhotometricInterpretation if "PhotometricInterpretation" in dataframe and dataframe.PhotometricInterpretation else None
        Image.RescaleSlope = dataframe.RescaleSlope
        Image.RescaleIntercept = dataframe.RescaleIntercept
        Image.SliceLocation = dataframe.SliceLocation
        Image.PixelSpacing = ','.join([str(point) for point in np.array(dataframe.PixelSpacing)])
        Image.ImageOrientationPatient = ','.join([str(point) for point in np.array(dataframe.ImageOrientationPatient)])
        Image.ImagePositionPatient = ','.join([str(point) for point in np.array(dataframe.ImagePositionPatient)])
        Image.SliceThickness = dataframe.SliceThickness
        Image.BodypartExamined = dataframe.BodyPartExamined if "BodyPartExamined" in dataframe and dataframe.BodyPartExamined else None
        Image.Rows = dataframe.Rows
        Image.Columns = dataframe.Columns
        Image.fk_series_id = series
        Image.fk_study_id = study
        Image.fk_patient_id = patient
    try:
        Image.save()
    except:
        print(sys.exc_info())
        return False

    return True
