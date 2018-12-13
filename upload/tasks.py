from __future__ import absolute_import
from dsrt.settings import STATIC_ROOT
from dsrt.settings import BASE_DIR
import os



from celery.decorators import task

# from celery.utils.log import get_task_logger
from celery import shared_task


import dicom
import glob
import sys
sys.path.append(BASE_DIR + '/upload/app/')

import dicomdb
from AlgoEngine.app.AlgoEngine.RadiationTherapyDecisionSupport.Python.AlgoEngine import AlgoManager

os.environ.setdefault('DJANGO_SETTINGS_MODULE','dsrt.settings')

@task(name="analyse dicom file and store it into data")
def uploader_task(rootDir, user_id, patientName):

    files = sorted(glob.glob(rootDir + '/*.dcm'), reverse=True)
    for file in files:
        if file:
            df = dicom.read_file(file)
            res = dicomdb.parse(df,user_id,patientName)
            if res:
                continue
            else:
                print("Something is wrong")
                return False
    
    # Run ovh / sts generation and similarity
    am = AlgoManager(str(res.pk), False)
    am.run()

    return True
