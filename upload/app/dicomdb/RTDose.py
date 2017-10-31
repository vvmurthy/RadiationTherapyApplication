from django.core.exceptions import ObjectDoesNotExist

import utils
from upload.models import RTDVH
from upload.models import RTDose
from upload.models import RTDoseImage


def parse(dataframe,user,patient,study,series):
    try:
        dose = RTDose.objects.get(SOPInstanceUID=dataframe.SOPInstanceUID)
    except ObjectDoesNotExist:
        dose = RTDose()
        dose.SOPInstanceUID = dataframe.SOPInstanceUID
        dose.SOPClassUID = dataframe.SOPClassUID
        dose.DoseGridScaling = dataframe.DoseGridScaling
        dose.DoseSummationType = dataframe.DoseSummationType
        dose.DoseType = dataframe.DoseType
        dose.DoseUnits = dataframe.DoseUnits
        dose.ReferencedRTPlanSequence = dataframe.ReferencedRTPlanSequence
        dose.ReferencedStructureSetSequence = dataframe.ReferencedStructureSetSequence
        dose.fk_user_id = user
        dose.fk_patient_id = patient
        dose.fk_study_id = study
        dose.fk_series_id = series
        dose.save()

    try:
        doseImage = RTDoseImage.objects.get(fk_dose_id = dose)
    except ObjectDoesNotExist:
        doseImage = RTDoseImage()
        doseImage.Columns = dataframe.Columns
        doseImage.Rows = dataframe.Rows
        doseImage.ImageOrientationPatient = dataframe.ImageOrientationPatient
        doseImage.ImagePositionPatient = dataframe.ImagePositionPatient
        doseImage.PhotometricInterpretation = dataframe.PhotometricInterpretation
        doseImage.PixelSpacing = dataframe.PixelSpacing
        doseImage.NumberOfFrames = int(dataframe.NumberOfFrames)
        doseImage.ImageData = dataframe.pixel_array
        doseImage.fk_user_id = user
        doseImage.fk_patient_id = patient
        doseImage.fk_study_id = study
        doseImage.fk_series_id = series
        doseImage.fk_dose_id = dose
        doseImage.save()

    #DVH information is under this tag
    dvhSequence = dataframe.DVHSequence
    for item in dvhSequence:
        #create a dvh for each ROI
        referencedROI = item.DVHReferencedROISequence[0].ReferencedROINumber
        try:
            dvh = RTDVH.objects.get(DVHReferencedROI=referencedROI)
        except ObjectDoesNotExist:
            dvh = RTDVH()
            dvh.DVHDoseScaling = item.DVHDoseScaling
            dvh.DVHMaximumDose = item.DVHMaximumDose
            dvh.DVHMeanDose = item.DVHMeanDose
            dvh.DVHMinimumDose = item.DVHMinimumDose
            dvh.DVHNumberOfBins = item.DVHNumberOfBins
            dvh.DVHReferencedROI = referencedROI
            dvh.DVHType = item.DVHType
            dvh.DVHVolumeUnits = item.DVHVolumeUnits
            dvh.DoseUnits = item.DoseUnits
            dvh.DVHData = item.DVHData
            dvh.fk_user_id = user
            dvh.fk_patient_id = patient
            dvh.fk_study_id = study
            dvh.fk_series_id = series
            dvh.fk_dose_id = dose
            dvh.save()

    IsdoseSequence = utils.getIsodose(dataframe)