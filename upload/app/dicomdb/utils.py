
from dsrt.settings import STATIC_ROOT
import os
import glob
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
    imageBlock,SOPID = getImageBlock()
    isodoseDict = _getIsodose(dataframe,SOPID)
    return isodoseDict


def getImageBlock(patientID,DataPath):

    DATA_PATH = DataPath
    #####################
    ct_files = glob.glob(DATA_PATH + '/' + 'CT*.dcm')
    num_ct_scans = len(ct_files)
    SOPID = OrderedDict()
    images = OrderedDict()
    for file in ct_files:
        df = dicom.read_file(file)
        if df.pixel_array is not None:
            # Based on the slicelocation to find where is the head where is the feet
            images[df.SliceLocation] = (df.SOPInstanceUID, df.pixel_array)
        else:
            print("No images")
            return None
    layer = 0
    # the larger number of slicelocation is at the top, so reverse the order
    # The head is the largest value of slicelocation
    # images = OrderedDict(sorted(images.items(),reverse=True))
    imageBlock = np.zeros((df.Rows, df.Columns, len(images)))
    for key, value in images.items():
        SOPID[key] = value[0]
        imageBlock[:, :, layer] = value[1]
        layer += 1
    return imageBlock, SOPID