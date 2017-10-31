import MySQLdb
import settings
class DataFetcher():
    def __init__(self):
        #build connection
        #save the connection with the class
        self.db_connection = MySQLdb.connect(settings.hostname, settings.username,settings.password, settings.database)

    #extract ovh
    def fetch_ovh(self,studyID):
        '''
        extract ovh feature
        :return: dicts
        {OAR1:
        OAR2:
        bin_values:
        overlap_area:

        '''
        pass


    def fetch_sts(self,studyID):
        '''
        extract sts
        :return:
        '''
        pass

    def fetch_RoiBlock(self,studyID):
        '''
        based on the studyID, fetch it's all Rois
        we need fetch following things to construct
        block_shape
        slice_position_z
        contour_data
        image_orientation
        image_position
        pixel_spacing
        :param studyID:

        #use function getContours

        :return: dict all Rois
        {
            oar
        }
        '''

    def fetch_similarity(self,studyID):
        '''
        find similarity of this studyID
        :param studyID:
        :return:dict
        {
            studyID:similarity
        }
        '''
        pass

    def save_ovh(self,ovh,StudyID):
        '''
        calculate the overlap area at first and then save it with ovh data under StudyID
        :param ovh:
        :param StudyID:
        :return:
        '''

    def save_sts(self,sts,StudyID):
        '''
        definition is the same as save_ovh
        :param ovh:
        :param StudyID:
        :return:
        '''
        pass

    def save_similarity(self,similarity_paris,StudyID):
        '''
        save the similarity pairs under StudyID
        :param similarity_paris:
        :param StudyID:
        :return:
        '''
        pass

