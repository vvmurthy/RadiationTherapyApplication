import MySQLdb
import numpy as np
import collections

class AlgoEngine():
    '''
    attribute
    self.StudyIDs
    '''
    def __init__(self):
        self.get_StudyID_list()

    #The entrance of the programe
    def run(self,StudyID):
        #extract OVH and STS for new case
        #store the OVH and STS
        #fetch OVH and STS of other cases
        #Do the similarity calculation
        #Save the result to database
        self.queryStudyID = StudyID
        ovh,sts,td = self.feature_extraction(StudyID)

        #Save features to the database
        try:
            self.save_features(ovh,sts,td)
        except:
            print("something happened")

        simlarity_pairs = self.similarity_calculation()

        #save similarity to the data
        try:
            self.save_similarity(simlarity_pairs)
        except:
            print("something happened")


    def _dissimilarity_calculation(self,study1, study2, type=None):
        '''
        calculate the dissimilarity between study 1 and study 2
        :param study1:
        :param study2:
        :return:
        '''
        if type == None:
            print("please enter a type(STS or OVH)")
            return False
        if type == 'STS':
            pass
        elif type == 'OVH':
            pass
        else:
            print("please enter a right type (STS or OVH)")
            return False


    def save_similarity(self,similarity_pair):
        '''
        save the similarity under self.queryStudy
        :param similarity_pair:
        :return:
        '''
        pass

    def similarity_calculation(self):
        '''
        fetch ovh and STS features of other study
        calculate dissimilarity between features
        calculate similarity between study pair
        :return: dict with dissimiarity and similarity
        '''
        pass
    def save_features(self,ovh,sts,td):
        '''
        save the ovh, sts, td under self.queryStudyID
        :param ovh: are a dictionary of dicts
        :param sts:
        :param td:
        :return:
        '''
        pass


    def feature_extraction(self,StudyID):
        '''
        call ovh, sts and td to get the ovh sts and td features
        :param StudyID:
        :return ovh: a histogram of ovh feature
        :return sts: a histogram of sts feature
        :return td: target dose
        '''
        pass


    #Get the list of all StudyIDs' names
    def get_StudyID_list(self):
        pass
