import sys

from django.core.exceptions import ObjectDoesNotExist
import numpy as np
try:
	from utils import *
except ImportError:
	from .utils import *
from upload.models import RTROI, RTContour
from upload.models import RTStructureSet


def parse(dicom_dataframe,user,patient,study,series):
    try:
        structure_set = RTStructureSet.objects.get(SOPInstanceUID=dicom_dataframe.SOPInstanceUID)
    except ObjectDoesNotExist:
        structure_set = RTStructureSet()
        structure_set.SOPInstanceUID = dicom_dataframe.SOPInstanceUID
        structure_set.SOPClassUID = dicom_dataframe.SOPClassUID
        structure_set.TotalROIs = count_rois(dicom_dataframe)
        structure_set.fk_series_id = series
        structure_set.fk_study_id = study
        structure_set.fk_patient_id = patient
        structure_set.fk_user_id = user
        structure_set_id = structure_set.save()


    # parse the ROI sequence
    roi_sequence = dicom_dataframe.ROIContourSequence
    roi_label_sequence = dicom_dataframe.StructureSetROISequence

    for roi in roi_sequence:
        try:
            rt_roi = RTROI.objects.get(fk_structureset_id=structure_set,ROINumber=roi.ReferencedROINumber)
        except ObjectDoesNotExist:
            rt_roi = RTROI()
            rt_roi.ROIName = [x.ROIName for x in roi_label_sequence if
                              x.ROINumber == roi.ReferencedROINumber][0]
            rt_roi.ROIDisplayColor = roi.ROIDisplayColor
            rt_roi.ROINumber = roi.ReferencedROINumber
            # Make a function to calculate the volume of ROI, given its contour information
            # rt_roi.Volume =
            if "ContourSequence" in roi:
                contour_sequence = roi.ContourSequence
                rt_roi.Volume = 50
                rt_roi.TotalContours = len(contour_sequence)
                rt_roi.fk_structureset_id = structure_set
                rt_roi.fk_series_id = series
                rt_roi.fk_study_id = study
                rt_roi.fk_patient_id = patient
                rt_roi.fk_user_id = user
                rt_roi.save()
                # loop the contour
                for contour in contour_sequence:
                    try:
                        rt_contour = RTContour.objects.get(fk_structureset_id=structure_set, fk_roi_id=rt_roi,
                                                           ReferencedSOPInstanceUID=contour.ContourImageSequence[
                                                               0].ReferencedSOPInstanceUID)
                        if rt_contour.ContourData != contour.ContourData:
                            rt_contour.NumberOfContourPoints += int(contour.NumberOfContourPoints)
                            contourarray = np.array(contour.ContourData)
                            contourString = ','.join([str(contourpoint) for contourpoint in contourarray])
                            rt_contour.ContourData = rt_contour.ContourData + ',' + contourString
                            rt_contour.save()

                    except ObjectDoesNotExist:
                        rt_contour = RTContour()
                        rt_contour.ContourGeometricType = contour.ContourGeometricType
                        rt_contour.NumberOfContourPoints = contour.NumberOfContourPoints
                        contourarray = np.array(contour.ContourData)
                        rt_contour.ContourData = ','.join([str(contourpoint) for contourpoint in contourarray])
                        rt_contour.ReferencedSOPClassUID = contour.ContourImageSequence[0].ReferencedSOPClassUID
                        rt_contour.ReferencedSOPInstanceUID = contour.ContourImageSequence[0].ReferencedSOPInstanceUID
                        rt_contour.fk_roi_id = rt_roi
                        rt_contour.fk_structureset_id = structure_set
                        rt_contour.save()

            else:
                continue



    return True
