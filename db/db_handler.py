import os
import pandas as pd
import numpy as np
import uuid

imageInfoName = './db/database/imageInfo.csv'
circleRegionInfo = './db/database/circleRegionInfo.csv'
boxRegionInfo = './db/database/boxRegionInfo.csv'
polygonInfo = './db/database/polygonInfo.csv'

def generateUid(id):
    uid = uuid.uuid1() if(id == None) else id
    return uid

class Module:
    def __init__(self):
        print('initialization')
        self.imagesInfo = pd.DataFrame(
            columns=['image-name', 'selected-classes', 'comment', 'image-original-height', 'image-original-width', 'image-src']
        )
        self.imageCircleRegions = pd.DataFrame(
            columns=['region-id', 'image-src', 'class', 'comment', 'tags', 'rx', 'ry', 'rw', 'rh']
        )
        self.imageBoxRegions = pd.DataFrame(
            columns=['region-id', 'image-src', 'class', 'comment', 'tags', 'x', 'y', 'w', 'h']
        )
        self.imagePolygonRegions = pd.DataFrame(
            columns=['region-id', 'image-src', 'class', 'comment', 'tags', 'points']
        )

        self.readDataFromDatabase()
        pass

    def readDataFromDatabase(self):
        global imageInfoName, circleRegionInfo, boxRegionInfo, polygonInfo

        self.checkFilesExistence(((imageInfoName, self.imagesInfo), (circleRegionInfo, self.imageCircleRegions), (boxRegionInfo, self.imageBoxRegions), (polygonInfo, self.imagePolygonRegions)))
        self.imagesInfo           = pd.read_csv(imageInfoName)
        self.imageCircleRegions  = pd.read_csv(circleRegionInfo)
        self.imageBoxRegions     = pd.read_csv(boxRegionInfo)
        self.imagePolygonRegions = pd.read_csv(polygonInfo)

    def checkFilesExistence(self, *args):
        global imageInfoName, circleRegionInfo, boxRegionInfo, polygonInfo
        for arguman in args[0]:
            # print(arguman)
            if not os.path.exists(arguman[0]):
                # print('nn')
                arguman[1].to_csv(arguman[0], index=False)
        # if not os.path.exists(imageInfoName):
        #     self.imagesInfo.to_csv(imageInfoName, index=False)

        # if not os.path.exists(circleRegionInfo):
        #     self.imageCircleRegions.to_csv(circleRegionInfo, index=False)

        # if not os.path.exists(boxRegionInfo):
        #     self.imageBoxRegions.to_csv(boxRegionInfo, index=False)

        # if not os.path.exists(polygonInfo):
        #     self.imagePolygonRegions.to_csv(polygonInfo, index=False)

    # def regionType(self, type):
    #     def regionType(type):
    #         if type == 'circle':
    #             return self.circleRegion
    #         elif type == 'box':
    #             return self.boxRegion
    #         elif type == 'polygon':
    #             return self.polygonRegion
    #         else:
    #             return self.otherRegion
    
    def saveRegionInfo(self, type, imageSrc, data):
        def regionType(type):
            # print(type)
            if type == 'circle':
                return self.circleRegion
            elif type == 'box':
                return self.boxRegion
            elif type == 'polygon':
                return self.polygonRegion
            else:
                return self.otherRegion

        regionData = {}
        regionData['region-id'] = data['id']
        regionData['image-src'] = imageSrc
        regionData['class']     = data['cls']
        regionData['comment']   = data['comment']
        regionData['tags']      = ';'.join(data['tags'])

        regionFunction = regionType(type)
        regionFunction(regionData, data)

        # return regionData

    def saveRegionInDB(self, database, idColumn, uid, data, status): # TODO if region then use one or zero changeSatus, remove in their
        
        index = self.findInfoInDb(database, idColumn, uid)
        print(index)
        if index is not None:
            print('data founded', idColumn, uuid.UUID)
            for key, value in data.items():
                _value = value[0] if status == 0 else value
                database.at[index, key] = _value
        else:
            # print(data)
            df = pd.DataFrame.from_dict(data)
            database = pd.concat([database, df], ignore_index=True)
            # print(database.head())
        return database
    
    def circleRegion(self, regionData, data):
        coords = data['coords']
        regionData['rx'] = [coords['rx']]
        regionData['ry'] = [coords['ry']]
        regionData['rw'] = [coords['rw']]
        regionData['rh'] = [coords['rh']]

        self.imageCircleRegions = self.saveRegionInDB(self.imageCircleRegions, 'region-id', regionData['region-id'], regionData, 1)


    def boxRegion(self, regionData, data):
        coords = data['coords']
        regionData['x'] = [coords['x']]
        regionData['y'] = [coords['y']]
        regionData['w'] = [coords['w']]
        regionData['h'] = [coords['h']]

        self.imageBoxRegions = self.saveRegionInDB(self.imageBoxRegions, 'region-id', regionData['region-id'], regionData, 1)
        

    def polygonRegion(self, regionData, data):
        # dar dast sakht!!!!
        regionData['points'] = ';'.join(e for e in ['-'.join(str(coord) for coord in point) for point in data['points']])
        print('honaouz sakhte nashodeh!!!')
        self.imagePolygonRegions = self.saveRegionInDB(self.imagePolygonRegions, 'region-id', regionData['region-id'], regionData, 1)
        

    def otherRegion(self, regionData, data):
        # dar dast sakht!!!!
        print('hanouz sakhte nashodeh!!!')
        print('database vase in type nadarim felan')
    
    def getImageData(self, data):
        imageData = {}
        imageData['image-name'] = [data['name']]
        imageData['image-src'] = [data['src']]
        imageData['comment'] = [data['comment']]
        imageData['selected-classes'] = [';'.join(data['cls'])]
        pixelSize = data['pixelSize'] if 'pixelSize' in data else {}
        imageData['image-original-height'] = [pixelSize['h']] if pixelSize != {} else []
        imageData['image-original-width'] = [pixelSize['w']] if pixelSize != {} else []
        
        return imageData
    
    def findInfoInDb(self, database, uid_columns, uid):
        # print(uid, uid_columns)
        # print(database.head())
        idx = database[database[uid_columns] == uid].index.values
        # print(idx)
        if len(idx) > 0:
            return idx[0]
        
        return None
    
    def saveDataAutomatically(self, *args):
        for arguman in args[0]:
            arguman[1].to_csv(arguman[0], index=False)

    def handleNewData(self, data):
        imageData = self.getImageData(data)
        self.imagesInfo = self.saveRegionInDB(self.imagesInfo, 'image-src', imageData['image-src'][0], imageData, 0)
        
        for region in data['regions']: #TODO: ADD Regions as remnants for each image -> for deletion process
            # print(region)
            self.saveRegionInfo(region['type'], data['src'], region)
        
        # save data automatically 
        self.saveDataAutomatically(((imageInfoName, self.imagesInfo), (circleRegionInfo, self.imageCircleRegions), (boxRegionInfo, self.imageBoxRegions), (polygonInfo, self.imagePolygonRegions)))
        
    def handleActiveImageData(self, data):
        imageData = self.getImageData(data)
        print(data)
        self.imagesInfo = self.saveRegionInDB(self.imagesInfo, 'image-src', imageData['image-src'][0], imageData, 0)
        
        self.imagesInfo.to_csv(imageInfoName, index=False)

    
    def __str__(self):
        return 'database'  