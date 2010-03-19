

import unittest
import os, sys

# Shared resources
BASE_RESOURCE_PATH = os.path.join( os.getcwd(), ".." )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
# append the proper platforms folder to our path, xbox is the same as win32
env = ( os.environ.get( "OS", "win32" ), "win32", )[ os.environ.get( "OS", "win32" ) == "xbox" ]
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "platform_libraries", env ) )

import re, string
from pysqlite2 import dbapi2 as sqlite
from gamedatabase import *
import dbupdate, importsettings


class TestImportSettings(unittest.TestCase):
	
	def setUp(self):
		self.databasedir = os.path.join( os.getcwd(), 'TestDataBase')
		self.gdb = GameDataBase(self.databasedir)
		self.gdb.connect()
		self.gdb.dropTables()
		self.gdb.createTables()
	
	def test_ImportSettings(self):		
		si = importsettings.SettingsImporter()
		si.importSettings(self.gdb, self.databasedir, RCBMock())
		
		rcbSettingRows = RCBSetting(self.gdb).getAll()
		self.assertTrue(rcbSettingRows != None)
		self.assertTrue(len(rcbSettingRows) == 1)
			
		rcbSetting = rcbSettingRows[0]
		self.assertEqual(rcbSetting[10], 'V0.3')
		self.assertEqual(rcbSetting[11], 'False')
		self.assertEqual(rcbSetting[12], 'False')
		self.assertEqual(rcbSetting[13], 'True')
		self.assertEqual(rcbSetting[14], 'True')
		self.assertEqual(rcbSetting[15], 'True')
		self.assertEqual(rcbSetting[16], 'True')
		
		consoleRows = Console(self.gdb).getAll()
		self.assertTrue(consoleRows != None)
		self.assertTrue(len(consoleRows) == 2)
		
		amiga = consoleRows[0]
		self.assertEqual(amiga[1], 'Amiga')		
		self.assertEqual(amiga[2], 'The Amiga 500 is also known as the A500 (or its code name Rock Lobster).')
		self.assertEqual(amiga[3], 'E:\Emulatoren\data\consoleImages\uae.png')
		
		superNintendo = consoleRows[1]
		self.assertEqual(superNintendo[1], 'Super Nintendo')
		self.assertEqual(superNintendo[2], 'The Super Nintendo (SNES) is a 16-bit video game console released in 1990.')
		self.assertEqual(superNintendo[3], 'E:\Emulatoren\data\consoleImages\zsnes.png')
		
		romCollectionRows = RomCollection(self.gdb).getAll()
		self.assertTrue(consoleRows != None)
		self.assertTrue(len(consoleRows) == 2)
		
		collV1 = romCollectionRows[0]
		self.assertEqual(collV1[1], 'Collection V1')
		console = Console(self.gdb).getObjectById(collV1[2])
		self.assertEqual(console[1], 'Amiga')
		self.assertEqual(collV1[3], 'E:\Emulatoren\WINUAE\winuae.exe -f "E:\Emulatoren\WINUAE\Configurations\Host\Amiga 500.uae" {-%I% "%ROM%"}')
		self.assertEqual(collV1[4], 'True')
		self.assertEqual(collV1[5], 'True')
		self.assertEqual(collV1[6], 'TestDataBase\Collection V1\parserConfig.xml')
		self.assertEqual(collV1[7], 'True')
		self.assertEqual(collV1[8], 'False')
		self.assertEqual(collV1[9], 'False')
		self.assertEqual(collV1[10], '_Disk')
		self.assertEqual(collV1[11], 'Text')
		self.assertEqual(collV1[12], 'False')
		self.assertEqual(collV1[13], 'False')
		
		collV2 = romCollectionRows[1]
		self.assertEqual(collV2[1], 'Collection V2')
		console = Console(self.gdb).getObjectById(collV2[2])
		self.assertEqual(console[1], 'Amiga')
		self.assertEqual(collV2[3], 'E:\Emulatoren\WINUAE\winuae.exe {-%I% "%ROM%"}')
		self.assertEqual(collV2[4], 'True')
		self.assertEqual(collV2[5], 'True')
		self.assertEqual(collV2[6], 'TestDataBase\Collection V2\parserConfig.xml')
		self.assertEqual(collV2[7], 'True')
		self.assertEqual(collV2[8], 'False')
		self.assertEqual(collV2[9], 'True')
		self.assertEqual(collV2[10], '_Disk')
		self.assertEqual(collV2[11], 'Text')
		self.assertEqual(collV2[12], 'False')
		self.assertEqual(collV2[13], 'False')
		
		collV3 = romCollectionRows[2]
		self.assertEqual(collV3[1], 'Collection V3')
		console = Console(self.gdb).getObjectById(collV3[2])
		self.assertEqual(console[1], 'Super Nintendo')
		self.assertEqual(collV3[3], 'E:\Emulatoren\SNES\zsnes.exe -m "%ROM%"')	
		self.assertEqual(collV3[4], 'True')
		self.assertEqual(collV3[5], 'True')
		self.assertEqual(collV3[6], 'TestDataBase\Collection V3\parserConfig.xml')
		self.assertEqual(collV3[7], 'True')
		self.assertEqual(collV3[8], 'False')
		self.assertEqual(collV3[9], 'False')
		self.assertEqual(collV3[10], '_Disk')
		self.assertEqual(collV3[11], 'Text')
		self.assertEqual(collV3[12], 'False')
		self.assertEqual(collV3[13], 'False')


		fileTypes = FileType(self.gdb).getAll()
		self.assertEqual(fileTypes[0][1], 'rom')
		self.assertEqual(fileTypes[1][1], 'screenshottitle')
		self.assertEqual(fileTypes[2][1], 'screenshotingame')
		self.assertEqual(fileTypes[3][1], 'cover')
		self.assertEqual(fileTypes[4][1], 'cartridge')
		self.assertEqual(fileTypes[5][1], 'manual')
		self.assertEqual(fileTypes[6][1], 'ingamevideo')
		self.assertEqual(fileTypes[7][1], 'trailer')
		self.assertEqual(fileTypes[8][1], 'description')
		self.assertEqual(fileTypes[9][1], 'configuration')
		
		paths = Path(self.gdb).getAll()
		self.assertTrue(paths != None)
		self.assertTrue(len(paths) == 27)


class RCBMock():
	def writeMsg(self, msg):
		pass
	

unittest.main()