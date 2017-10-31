from celery.decorators import task
from celery.utils.log import get_task_logger
from models import User
import dicom
import glob
from app import dicomdb
logger = get_task_logger(__name__)

@task(name="analyse dicom file and store it into data")
def uploader_task(rootDir, user_id, patientName):
    logger.info("Storing the data into the database")

    user = User.objects.get(id = user_id)
    files = glob.glob(rootDir + '/*.dcm')
    for file in files:
        if file:
            df = dicom.read_file(file)
            res = dicomdb.parse(df,user,patientName)
            if res:
                continue
            else:
                return False
    return True
