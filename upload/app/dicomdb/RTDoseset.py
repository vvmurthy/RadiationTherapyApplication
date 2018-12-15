from django.core.exceptions import ObjectDoesNotExist

try:
	from utils import *
except ImportError:
	from .utils import *
from upload.models import RTDVH, RTROI
from upload.models import RTDose
from upload.models import RTDoseImage

from dicompylercore import dicomparser, dvhcalc
from dicompylercore import dvh as dvhlib


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
        dose.ReferencedRTPlanSequence = dataframe.ReferencedRTPlanSequence[0].ReferencedSOPInstanceUID
        dose.ReferencedStructureSetSequence = dataframe.ReferencedStructureSetSequence[0].ReferencedSOPInstanceUID
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
        doseImage.ImageOrientationPatient = str(dataframe.ImageOrientationPatient)
        doseImage.ImagePositionPatient = str(dataframe.ImagePositionPatient)
        doseImage.PhotometricInterpretation = dataframe.PhotometricInterpretation
        doseImage.PixelSpacing = dataframe.PixelSpacing
        doseImage.NumberOfFrames = int(dataframe.NumberOfFrames)
        doseImage.ImageData = dataframe.pixel_array
        doseImage.fk_patient_id = patient
        doseImage.fk_study_id = study
        doseImage.fk_series_id = series
        doseImage.fk_dose_id = dose
        doseImage.save()

    #DVH information is under this tag
    dvhSequence = dataframe.DVHSequence
    for i, item in enumerate(dvhSequence):
        #create a dvh for each ROI
        referencedROI = item.DVHReferencedROISequence[0].ReferencedROINumber
        ref_roi = RTROI.objects.get(ROINumber=referencedROI, 
                    fk_patient_id=patient, fk_study_id=study)
        try:
            
            dvh = RTDVH.objects.get(DVHReferencedROI=ref_roi, fk_study_id=study)
        except ObjectDoesNotExist:
            dvh = RTDVH()
            dvh.DVHDoseScaling = item.DVHDoseScaling
            dvh.DVHMaximumDose = item.DVHMaximumDose
            dvh.DVHMeanDose = item.DVHMeanDose
            dvh.DVHMinimumDose = item.DVHMinimumDose
            dvh.DVHNumberOfBins = item.DVHNumberOfBins
            dvh.DVHReferencedROI = ref_roi
            dvh.DVHType = item.DVHType
            dvh.DVHVolumeUnits = item.DVHVolumeUnits
            dvh.DoseUnits = item.DoseUnits

            # Generate the dvh using dicompyler
            create_dvh = dvhlib.DVH.from_dicom_dvh(dataframe, referencedROI)
            create_dvh = create_dvh.cumulative
            dvh.DVHCounts = str(create_dvh.counts.tostring())
            dvh.DVHBins = str(create_dvh.bins.tostring())

            dvh.fk_patient_id = patient
            dvh.fk_study_id = study
            dvh.fk_series_id = series
            dvh.fk_dose_id = dose
            dvh.save()

    # TODO: link in isodose curves
    #IsdoseSequence = getIsodose(dataframe)
    return True
