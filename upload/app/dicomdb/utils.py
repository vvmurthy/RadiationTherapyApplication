
from dsrt.settings import STATIC_ROOT
import os
import glob
from upload.models import CTImages
from collections import OrderedDict
import dicom
import numpy as np
def _getIsodose(dataframe,SOPID):
    pass
def count_rois(dicom_dataframe):
    '''

    :param dicom_dataframe: a dataframe structure parsed by pydicom
    :return: num_roi: number of ROI in a structure dicom file
    '''
    num_roi = len(dicom_dataframe.ROIContourSequence)
    return num_roi

def getIsodose(dataframe,user,patient):
    DataPath = os.path.join(STATIC_ROOT,'data',str(user.userid),patient.PatientName)
    imageBlock,SOPID = getImageBlock(patient.patientID, DataPath)
    isodoseDict = _getIsodose(dataframe,SOPID)
    return isodoseDict


def getImageBlock(data_path, patient_id, study_id, series_id):
    """
    Gets an image block for a specific patient from the local
    filesystem based off their Patient ID and name

    Parameters
    ----------
    data_path : str
        location of the file in local memory
    patient_id : str
        patient to query CTs of
    study_id : str
        study to query CTs of
    series_id : str
        series to query CTs of
    
    Returns
    ------
    imageBlock : 3D NdArray
        Ordered images in an array
    SOPID : dict
        slice location keys bound to the SOPInstanceID of the generating 
        file
    
    Raises
    ------
    Assertion Error : if no files for the patient are found
    """

    # Get CT scan SOPInstanceUIDs
    ids = CTImages.objects.values_list('SOPInstanceUID', flat=True).filter(fk_patient_id=patient_id, fk_study_id=study_id,
        fk_series_id=series_id)
    print(data_path)
    ct_files = glob.glob(data_path + '/' + 'CT*.dcm')
    if len(ct_files) == 0:
        raise AssertionError("No files found")
    num_ct_scans = len(ct_files)
    SOPID = OrderedDict()
    images = OrderedDict()
    for file in ct_files:
        df = dicom.read_file(file)
        if(df.SOPInstanceUID not in ids):
            continue

        if df.pixel_array is not None:
            # Based on the slicelocation to find where is the head where is the feet
            images[float(df.SliceLocation)] = (df.SOPInstanceUID, df.pixel_array)
        else:
            print("No images")
            raise AssertionError("no images found")
    layer = 0

    if len(images.keys()) < 1:
        raise AssertionError("no images found in db")

    # the larger number of slicelocation is at the top, so reverse the order
    # The head is the largest value of slicelocation
    # images = OrderedDict(sorted(images.items(),reverse=True))
    imageBlock = np.zeros((df.Rows, df.Columns, len(images)))
    for key in sorted(images.keys())[::-1]:
        value = images[key]
        SOPID[key] = value[0]
        imageBlock[:, :, layer] = value[1] 
        layer += 1
    return imageBlock, SOPID