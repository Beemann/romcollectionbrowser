# -*- coding: iso-8859-15 -*-

import os, sys, re
import codecs

#taken from apple movie trailer script (thanks to Nuka1195 and others)
# Shared resources
BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
# append the proper platforms folder to our path, xbox is the same as win32
env = ( os.environ.get( "OS", "win32" ), "win32", )[ os.environ.get( "OS", "win32" ) == "xbox" ]
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "platform_libraries", env ) )

from pyparsing import *
from string import lowercase

class DescriptionParser:
	
	def parseDescription(self, descFile, descParseInstruction, gamename):
		print descFile
		
		star = Suppress(Literal('*') +LineEnd())
		star = star.setResultsName('star')
		crc = Word(printables) +Suppress(LineEnd())
		crc = crc.setResultsName('crc')
		game = Literal(gamename) +Suppress(LineEnd())
		#game = SkipTo(NotAny('\r') +Suppress(LineEnd()))
		game = game.setResultsName('game')
		platform = Suppress(Literal('Platform: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		platform = platform.setResultsName('platform')
		region = Suppress(Literal('Region: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		region = region.setResultsName('region')
		media = Suppress(Literal('Media: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		media = media.setResultsName('media')
		controller = Suppress(Literal('Controller: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		controller = controller.setResultsName('controller')
		genre = Suppress(Literal('Genre: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		genre = genre.setResultsName('genre')				
		year = Suppress(Literal('Release Year: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		year = year.setResultsName('year')				
		dev = Suppress(Literal('Developer: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		dev = dev.setResultsName('developer')				
		publisher = Suppress(Literal('Publisher: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		publisher = publisher.setResultsName('publisher')
		players = Suppress(Literal('Players: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		players = players.setResultsName('players')
		line = Suppress(Combine(OneOrMore(Literal('_'))))
		line = line.setResultsName('line')
		desc = SkipTo(star)
		desc = desc.setResultsName('description')
		delimiter = Suppress(Optional(SkipTo(LineEnd())))
		
		grammar = star + crc +game +platform + region + media + controller + genre \
			+ year + dev +publisher +players +line + star +desc +delimiter

		file = OneOrMore(grammar)
		results = file.parseFile(descFile)
		#print str(results.asXML())
		
		return results
		
	
	def parseDescriptionSearch(self, descFile, descParseInstruction, gamename):
		print descFile
		
		#TODO Entries before game?
		game = Suppress(SkipTo(Literal(gamename))) +Literal(gamename) +Suppress(LineEnd())
		#game = SkipTo(NotAny('\r') +Suppress(LineEnd()))
		game = game.setResultsName('game')
		platform = Suppress(Literal('Platform: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		platform = platform.setResultsName('platform')
		region = Suppress(Literal('Region: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		region = region.setResultsName('region')
		media = Suppress(Literal('Media: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		media = media.setResultsName('media')
		controller = Suppress(Literal('Controller: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		controller = controller.setResultsName('controller')
		#TODO Item Delimiter		
		genre = Suppress(Literal('Genre: ')) +commaSeparatedList
		genre = genre.setResultsName('genre')				
		year = Suppress(Literal('Release Year: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		year = year.setResultsName('year')				
		dev = Suppress(Literal('Developer: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		dev = dev.setResultsName('developer')				
		publisher = Suppress(Literal('Publisher: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		publisher = publisher.setResultsName('publisher')
		players = Suppress(Literal('Players: ')) +SkipTo(NotAny('\r') +Suppress(LineEnd()))
		players = players.setResultsName('players')
		line = Suppress(Combine(OneOrMore(Literal('_'))))
		line = line.setResultsName('line')
		star = Suppress(Literal('*') +LineEnd())
		star = star.setResultsName('star')
		#desc = SkipTo(star)
		desc = ZeroOrMore(unicode(Word(printables + alphas8bit))) +SkipTo(star)
		desc = desc.setResultsName('description')
		delimiter = Suppress(Optional(SkipTo(LineEnd())))
		
		gamegrammar = game +platform + region + media + controller + genre \
			+ year + dev +publisher +players +line + star +desc +delimiter
		
		filegrammar = OneOrMore(gamegrammar)
		
		fh = open(str(descFile), 'r')
		fileAsString = fh.read()		
		fileAsString = fileAsString.decode('iso-8859-15')		
				
		results = filegrammar.parseString(fileAsString)		
		
		return results
		
	
	def parseDescriptionConfig(self, descFile, descParseInstruction, gamename):
		print descFile
		
		#TODO Entries before game?
		star = Suppress(Literal('*')) +Suppress(LineEnd())
		star = star.setResultsName('star')
		#crc = Optional(~LineEnd() +commaSeparatedList).setDebug() +Suppress(LineEnd())
		crc = Optional(~LineEnd() +delimitedList(',')) +SkipTo(LineEnd()) +Suppress(LineEnd())
		crc = crc.setResultsName('crc')
		
		#TODO handle different delimiters?
		
		#game = Suppress(SkipTo(Literal())) +Literal(gamename) +Suppress(LineEnd())
		game = Optional(~LineEnd() +delimitedList(',')) +SkipTo(LineEnd()).setDebug()
		game = game.setResultsName('game')
		#TODO csv + \r\n +optional?
		platform = Suppress(Literal('Platform: ')) +(Optional(~LineEnd() +commaSeparatedList))
		platform = platform.setResultsName('platform')
		region = Suppress(Literal('Region: ')) +(Optional(~LineEnd() +commaSeparatedList))
		region = region.setResultsName('region')
		media = Suppress(Literal('Media: ')) +(Optional(~LineEnd() +commaSeparatedList))
		media = media.setResultsName('media')
		controller = Suppress(Literal('Controller: ')) +(Optional(~LineEnd() +commaSeparatedList))
		controller = controller.setResultsName('controller')
		#TODO Item Delimiter		
		genre = Suppress(Literal('Genre: ')) +(Optional(~LineEnd() +commaSeparatedList))
		genre = genre.setResultsName('genre')				
		year = Suppress(Literal('Release Year: ')) +(Optional(~LineEnd() +commaSeparatedList))
		year = year.setResultsName('year')				
		dev = Suppress(Literal('Developer: ')) +(Optional(~LineEnd() +commaSeparatedList))
		dev = dev.setResultsName('developer')				
		publisher = Suppress(Literal('Publisher: ')) +(Optional(~LineEnd() +commaSeparatedList))
		publisher = publisher.setResultsName('publisher')
		players = Suppress(Literal('Players: ')) +(Optional(~LineEnd() +commaSeparatedList))
		players = players.setResultsName('players')
		line = Suppress(Combine(OneOrMore(Literal('_'))))
		line = line.setResultsName('line')
		#star = Suppress(Literal('*') +LineEnd())
		#star = star.setResultsName('star')
		#desc = SkipTo(star)
		desc = ZeroOrMore(unicode(Word(printables + alphas8bit))) +SkipTo(star)
		desc = desc.setResultsName('description')
		delimiter = Suppress(SkipTo(LineEnd()))
		
		gamegrammar = star +crc +game +platform + region + media + controller + genre \
			+ year + dev +publisher +players +line + star +desc +delimiter
		
		filegrammar = OneOrMore(gamegrammar)
		
		fh = open(str(descFile), 'r')
		fileAsString = fh.read()		
		fileAsString = fileAsString.decode('iso-8859-15')		
				
		results = filegrammar.parseString(fileAsString)		
		
		return results




dp = DescriptionParser()
results = dp.parseDescriptionConfig('E:\\Emulatoren\\data\\Amiga\\Collection V1\\synopsis\\synopsis.txt', '', 'Football Glory')
print results
results = dp.parseDescriptionConfig('E:\\Emulatoren\\data\\Amiga\\Collection V1\\synopsis\\synopsis.txt', '', 'Formula One Grand Prix')
print results.asDict()
print results['genre']
del dp