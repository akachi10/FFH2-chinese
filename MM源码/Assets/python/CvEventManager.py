# Sid Meier's Civilization 4
# Copyright Firaxis Games 2006
#
# CvEventManager
# This class is passed an argsList from CvAppInterface.onEvent
# The argsList can contain anything from mouse location to key info
# The EVENTLIST that are being notified can be found

from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import CvDebugTools
#import CvWBPopups
import PyHelpers
import Popup as PyPopup
import CvCameraControls
import CvTopCivs
import sys
#import CvWorldBuilderScreen
import CvAdvisorUtils
import CvTechChooser

import CvIntroMovieScreen
import CustomFunctions
import ScenarioFunctions

#FfH: Card Game: begin
import CvSomniumInterface
import CvCorporationScreen
#FfH: Card Game: end

#FfH: Added by Kael 10/15/2008 for OOS Logging
import OOSLogger
#FfH: End Add

## Ultrapack ##
import WBCityEditScreen
import WBUnitScreen
import WBPlayerScreen
import WBGameDataScreen
import WBPlotScreen
import CvPlatyBuilderScreen
## Ultrapack ##

import Blizzards		#Added in Blizzards: TC01

import math


# globals
cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
sf = ScenarioFunctions.ScenarioFunctions()
game = gc.getGame()

#FfH: Card Game: begin
cs = CvCorporationScreen.cs
#FfH: Card Game: end

Blizzards = Blizzards.Blizzards()		#Added in Blizzards: TC01


# globals
###################################################
class CvEventManager:
	def __init__(self):
		#################### ON EVENT MAP ######################
		#print "EVENTMANAGER INIT"

		self.bCtrl = False
		self.bShift = False
		self.bAlt = False
		self.bAllowCheats = False

		# OnEvent Enums
		self.EventLButtonDown=1
		self.EventLcButtonDblClick=2
		self.EventRButtonDown=3
		self.EventBack=4
		self.EventForward=5
		self.EventKeyDown=6
		self.EventKeyUp=7

		self.__LOG_MOVEMENT = 0
		self.__LOG_BUILDING = 0
		self.__LOG_COMBAT = 0
		self.__LOG_CONTACT = 0
		self.__LOG_IMPROVEMENT =0
		self.__LOG_CITYLOST = 0
		self.__LOG_CITYBUILDING = 0
		self.__LOG_TECH = 0
		self.__LOG_UNITBUILD = 0
		self.__LOG_UNITKILLED = 1
		self.__LOG_UNITLOST = 0
		self.__LOG_UNITPROMOTED = 0
		self.__LOG_UNITSELECTED = 0
		self.__LOG_UNITPILLAGE = 0
		self.__LOG_GOODYRECEIVED = 0
		self.__LOG_GREATPERSON = 0
		self.__LOG_RELIGION = 0
		self.__LOG_RELIGIONSPREAD = 0
		self.__LOG_GOLDENAGE = 0
		self.__LOG_ENDGOLDENAGE = 0
		self.__LOG_WARPEACE = 0
		self.__LOG_PUSH_MISSION = 0

		## EVENTLIST
		self.EventHandlerMap = {
			'mouseEvent'				: CvEventManager.onMouseEvent.__get__(self,CvEventManager),
			'kbdEvent'					: CvEventManager.onKbdEvent.__get__(self,CvEventManager),
			'ModNetMessage'				: CvEventManager.onModNetMessage.__get__(self,CvEventManager),
			'Init'						: CvEventManager.onInit.__get__(self,CvEventManager),
			'Update'					: CvEventManager.onUpdate.__get__(self,CvEventManager),
			'UnInit'					: CvEventManager.onUnInit.__get__(self,CvEventManager),
			'OnSave'					: CvEventManager.onSaveGame.__get__(self,CvEventManager),
			'OnPreSave'					: CvEventManager.onPreSave.__get__(self,CvEventManager),
			'OnLoad'					: CvEventManager.onLoadGame.__get__(self,CvEventManager),
			'GameStart'					: CvEventManager.onGameStart.__get__(self,CvEventManager),
			'GameEnd'					: CvEventManager.onGameEnd.__get__(self,CvEventManager),
			'plotRevealed'				: CvEventManager.onPlotRevealed.__get__(self,CvEventManager),
			'plotFeatureRemoved'		: CvEventManager.onPlotFeatureRemoved.__get__(self,CvEventManager),
			'plotPicked'				: CvEventManager.onPlotPicked.__get__(self,CvEventManager),
			'nukeExplosion'				: CvEventManager.onNukeExplosion.__get__(self,CvEventManager),
			'gotoPlotSet'				: CvEventManager.onGotoPlotSet.__get__(self,CvEventManager),
			'BeginGameTurn'				: CvEventManager.onBeginGameTurn.__get__(self,CvEventManager),
			'EndGameTurn'				: CvEventManager.onEndGameTurn.__get__(self,CvEventManager),
			'BeginPlayerTurn'			: CvEventManager.onBeginPlayerTurn.__get__(self,CvEventManager),
			'EndPlayerTurn'				: CvEventManager.onEndPlayerTurn.__get__(self,CvEventManager),
			'endTurnReady'				: CvEventManager.onEndTurnReady.__get__(self,CvEventManager),
			'combatResult'				: CvEventManager.onCombatResult.__get__(self,CvEventManager),
			'combatLogCalc'				: CvEventManager.onCombatLogCalc.__get__(self,CvEventManager),
			'combatLogHit'				: CvEventManager.onCombatLogHit.__get__(self,CvEventManager),
			'improvementBuilt'			: CvEventManager.onImprovementBuilt.__get__(self,CvEventManager),
			'improvementDestroyed'		: CvEventManager.onImprovementDestroyed.__get__(self,CvEventManager),
			'routeBuilt'				: CvEventManager.onRouteBuilt.__get__(self,CvEventManager),
			'firstContact'				: CvEventManager.onFirstContact.__get__(self,CvEventManager),
			'cityBuilt'					: CvEventManager.onCityBuilt.__get__(self,CvEventManager),
			'cityRazed'					: CvEventManager.onCityRazed.__get__(self,CvEventManager),
			'cityAcquired'				: CvEventManager.onCityAcquired.__get__(self,CvEventManager),
			'cityAcquiredAndKept'		: CvEventManager.onCityAcquiredAndKept.__get__(self,CvEventManager),
			'cityLost'					: CvEventManager.onCityLost.__get__(self,CvEventManager),
			'cultureExpansion'			: CvEventManager.onCultureExpansion.__get__(self,CvEventManager),
			'cityGrowth'				: CvEventManager.onCityGrowth.__get__(self,CvEventManager),
			'cityDoTurn'				: CvEventManager.onCityDoTurn.__get__(self,CvEventManager),
			'cityBuildingUnit'			: CvEventManager.onCityBuildingUnit.__get__(self,CvEventManager),
			'cityBuildingBuilding'		: CvEventManager.onCityBuildingBuilding.__get__(self,CvEventManager),
			'cityRename'				: CvEventManager.onCityRename.__get__(self,CvEventManager),
			'cityHurry'					: CvEventManager.onCityHurry.__get__(self,CvEventManager),
			'selectionGroupPushMission'	: CvEventManager.onSelectionGroupPushMission.__get__(self,CvEventManager),
			'unitMove'					: CvEventManager.onUnitMove.__get__(self,CvEventManager),
			'unitSetXY'					: CvEventManager.onUnitSetXY.__get__(self,CvEventManager),
			'unitCreated'				: CvEventManager.onUnitCreated.__get__(self,CvEventManager),
			'unitBuilt'					: CvEventManager.onUnitBuilt.__get__(self,CvEventManager),
			'unitKilled'				: CvEventManager.onUnitKilled.__get__(self,CvEventManager),
			'unitLost'					: CvEventManager.onUnitLost.__get__(self,CvEventManager),
			'unitPromoted'				: CvEventManager.onUnitPromoted.__get__(self,CvEventManager),
			'unitSelected'				: CvEventManager.onUnitSelected.__get__(self,CvEventManager),
			'UnitRename'				: CvEventManager.onUnitRename.__get__(self,CvEventManager),
			'unitPillage'				: CvEventManager.onUnitPillage.__get__(self,CvEventManager),
			'unitSpreadReligionAttempt'	: CvEventManager.onUnitSpreadReligionAttempt.__get__(self,CvEventManager),
			'unitGifted'				: CvEventManager.onUnitGifted.__get__(self,CvEventManager),
			'unitBuildImprovement'		: CvEventManager.onUnitBuildImprovement.__get__(self,CvEventManager),
			'goodyReceived'				: CvEventManager.onGoodyReceived.__get__(self,CvEventManager),
			'greatPersonBorn'			: CvEventManager.onGreatPersonBorn.__get__(self,CvEventManager),
			'buildingBuilt'				: CvEventManager.onBuildingBuilt.__get__(self,CvEventManager),
			'projectBuilt'				: CvEventManager.onProjectBuilt.__get__(self,CvEventManager),
			'techAcquired'				: CvEventManager.onTechAcquired.__get__(self,CvEventManager),
			'techSelected'				: CvEventManager.onTechSelected.__get__(self,CvEventManager),
			'religionFounded'			: CvEventManager.onReligionFounded.__get__(self,CvEventManager),
			'religionSpread'			: CvEventManager.onReligionSpread.__get__(self,CvEventManager),
			'religionRemove'			: CvEventManager.onReligionRemove.__get__(self,CvEventManager),
			'corporationFounded'		: CvEventManager.onCorporationFounded.__get__(self,CvEventManager),
			'corporationSpread'			: CvEventManager.onCorporationSpread.__get__(self,CvEventManager),
			'corporationRemove'			: CvEventManager.onCorporationRemove.__get__(self,CvEventManager),
			'goldenAge'					: CvEventManager.onGoldenAge.__get__(self,CvEventManager),
			'endGoldenAge'				: CvEventManager.onEndGoldenAge.__get__(self,CvEventManager),
			'chat'						: CvEventManager.onChat.__get__(self,CvEventManager),
			'victory'					: CvEventManager.onVictory.__get__(self,CvEventManager),
			'vassalState'				: CvEventManager.onVassalState.__get__(self,CvEventManager),
			'changeWar'					: CvEventManager.onChangeWar.__get__(self,CvEventManager),
			'setPlayerAlive'			: CvEventManager.onSetPlayerAlive.__get__(self,CvEventManager),
			'playerChangeStateReligion'	: CvEventManager.onPlayerChangeStateReligion.__get__(self,CvEventManager),
			'playerGoldTrade'			: CvEventManager.onPlayerGoldTrade.__get__(self,CvEventManager),
			'windowActivation'			: CvEventManager.onWindowActivation.__get__(self,CvEventManager),
			'gameUpdate'				: CvEventManager.onGameUpdate.__get__(self,CvEventManager),		# sample generic event
		}

		################## Events List ###############################
		#
		# Dictionary of Events, indexed by EventID (also used at popup context id)
		# entries have name, beginFunction, applyFunction [, randomization weight...]
		#
		# Normal events first, random events after
		#
		################## Events List ###############################
		self.Events={
			CvUtil.EventEditCityName : ('EditCityName', self.__eventEditCityNameApply, self.__eventEditCityNameBegin),
			CvUtil.EventPlaceObject : ('PlaceObject', self.__eventPlaceObjectApply, self.__eventPlaceObjectBegin),
			CvUtil.EventAwardTechsAndGold: ('AwardTechsAndGold', self.__eventAwardTechsAndGoldApply, self.__eventAwardTechsAndGoldBegin),
			CvUtil.EventEditUnitName : ('EditUnitName', self.__eventEditUnitNameApply, self.__eventEditUnitNameBegin),
## Platy Builder ##
			CvUtil.EventWBLandmarkPopup : ('WBLandmarkPopup', self.__eventWBLandmarkPopupApply, self.__eventWBScriptPopupBegin),
			CvUtil.EventShowWonder: ('ShowWonder', self.__eventShowWonderApply, self.__eventShowWonderBegin),
			1111 : ('WBPlayerScript', self.__eventWBPlayerScriptPopupApply, self.__eventWBScriptPopupBegin),
			2222 : ('WBCityScript', self.__eventWBCityScriptPopupApply, self.__eventWBScriptPopupBegin),
			3333 : ('WBUnitScript', self.__eventWBUnitScriptPopupApply, self.__eventWBScriptPopupBegin),
			4444 : ('WBGameScript', self.__eventWBGameScriptPopupApply, self.__eventWBScriptPopupBegin),
			5555 : ('WBPlotScript', self.__eventWBPlotScriptPopupApply, self.__eventWBScriptPopupBegin),
#Magister Start
			6666 : ('WBPlayerRename', self.__eventEditPlayerNameApply, self.__eventEditPlayerNameBegin),
			6777 : ('WBPlayerRename', self.__eventEditCivNameApply, self.__eventEditCivNameBegin),
			6888 : ('WBPlayerRename', self.__eventEditCivShortNameApply, self.__eventEditCivShortNameBegin),
			6999 : ('WBPlayerRename', self.__eventEditCivAdjApply, self.__eventEditCivAdjBegin),
#Magister Stop
## Platy Builder ##
		}
## FfH Card Game: begin
		self.Events[CvUtil.EventSelectSolmniumPlayer] = ('selectSolmniumPlayer', self.__EventSelectSolmniumPlayerApply, self.__EventSelectSolmniumPlayerBegin)
		self.Events[CvUtil.EventSolmniumAcceptGame] = ('solmniumAcceptGame', self.__EventSolmniumAcceptGameApply, self.__EventSolmniumAcceptGameBegin)
		self.Events[CvUtil.EventSolmniumConcedeGame] = ('solmniumConcedeGame', self.__EventSolmniumConcedeGameApply, self.__EventSolmniumConcedeGameBegin)
## FfH Card Game: end

#################### EVENT STARTERS ######################
	def handleEvent(self, argsList):
		'EventMgr entry point'
		# extract the last 6 args in the list, the first arg has already been consumed
		self.origArgsList = argsList	# point to original
		tag = argsList[0]				# event type string
		idx = len(argsList)-6
		bDummy = False
		self.bDbg, bDummy, self.bAlt, self.bCtrl, self.bShift, self.bAllowCheats = argsList[idx:]
		ret = 0
		if self.EventHandlerMap.has_key(tag):
			fxn = self.EventHandlerMap[tag]
			ret = fxn(argsList[1:idx])
		return ret

#################### EVENT APPLY ######################
	def beginEvent( self, context, argsList=-1 ):
		'Begin Event'
		entry = self.Events[context]
		return entry[2]( argsList )

	def applyEvent( self, argsList ):
		'Apply the effects of an event '
		context, playerID, netUserData, popupReturn = argsList

		if context == CvUtil.PopupTypeEffectViewer:
			return CvDebugTools.g_CvDebugTools.applyEffectViewer( playerID, netUserData, popupReturn )

		entry = self.Events[context]

		if ( context not in CvUtil.SilentEvents ):
			self.reportEvent(entry, context, (playerID, netUserData, popupReturn) )
		return entry[1]( playerID, netUserData, popupReturn ) # the apply function

	def reportEvent(self, entry, context, argsList):
		'Report an Event to Events.log '
		if (gc.getGame().getActivePlayer() != -1):
			message = "DEBUG Event: %s (%s)" %(entry[0], gc.getActivePlayer().getName())
			CyInterface().addImmediateMessage(message,"")
			CvUtil.pyPrint(message)
		return 0

#################### ON EVENTS ######################
	def onKbdEvent(self, argsList):
		'keypress handler - return 1 if the event was consumed'

		eventType,key,mx,my,px,py = argsList
		game = gc.getGame()

		if (self.bAllowCheats):
			# notify debug tools of input to allow it to override the control
			argsList = (eventType,key,self.bCtrl,self.bShift,self.bAlt,mx,my,px,py,gc.getGame().isNetworkMultiPlayer())
			if ( CvDebugTools.g_CvDebugTools.notifyInput(argsList) ):
				return 0

		if ( eventType == self.EventKeyDown ):
			theKey=int(key)

#FfH: Added by Kael 07/05/2008
			if (theKey == int(InputTypes.KB_LEFT)):
				if self.bCtrl:
						CyCamera().SetBaseTurn(CyCamera().GetBaseTurn() - 45.0)
						return 1
				elif self.bShift:
						CyCamera().SetBaseTurn(CyCamera().GetBaseTurn() - 10.0)
						return 1

			if (theKey == int(InputTypes.KB_RIGHT)):
					if self.bCtrl:
							CyCamera().SetBaseTurn(CyCamera().GetBaseTurn() + 45.0)
							return 1
					elif self.bShift:
							CyCamera().SetBaseTurn(CyCamera().GetBaseTurn() + 10.0)
							return 1
#FfH: End Add

			CvCameraControls.g_CameraControls.handleInput( theKey )

			if (self.bAllowCheats):
				# Shift - T (Debug - No MP)
				if (theKey == int(InputTypes.KB_T)):
					if ( self.bShift ):
						CvEventManager.beginEvent(self,CvUtil.EventAwardTechsAndGold)
						#self.beginEvent(CvUtil.EventCameraControlPopup)
						return 1

				elif (theKey == int(InputTypes.KB_W)):
					if ( self.bShift and self.bCtrl):
						CvEventManager.beginEvent(self,CvUtil.EventShowWonder)
						return 1

				# Shift - ] (Debug - currently mouse-overd unit, health += 10
				elif (theKey == int(InputTypes.KB_LBRACKET) and self.bShift ):
					unit = CyMap().plot(px, py).getUnit(0)
					if ( not unit.isNone() ):
						d = min( unit.maxHitPoints()-1, unit.getDamage() + 10 )
						unit.setDamage( d, PlayerTypes.NO_PLAYER )

				# Shift - [ (Debug - currently mouse-overd unit, health -= 10
				elif (theKey == int(InputTypes.KB_RBRACKET) and self.bShift ):
					unit = CyMap().plot(px, py).getUnit(0)
					if ( not unit.isNone() ):
						d = max( 0, unit.getDamage() - 10 )
						unit.setDamage( d, PlayerTypes.NO_PLAYER )

				elif (theKey == int(InputTypes.KB_F1)):
					if ( self.bShift ):
						CvScreensInterface.replayScreen.showScreen(False)
						return 1
					# don't return 1 unless you want the input consumed

				elif (theKey == int(InputTypes.KB_F2)):
					if ( self.bShift ):
						import CvDebugInfoScreen
						CvScreensInterface.showDebugInfoScreen()
						return 1

				elif (theKey == int(InputTypes.KB_F3)):
					if ( self.bShift ):
						CvScreensInterface.showDanQuayleScreen(())
						return 1

				elif (theKey == int(InputTypes.KB_F4)):
					if ( self.bShift ):
						CvScreensInterface.showUnVictoryScreen(())
						return 1

		return 0

	def onModNetMessage(self, argsList):
		'Called whenever CyMessageControl().sendModNetMessage() is called - this is all for you modders!'

		iData1, iData2, iData3, iData4, iData5 = argsList

#		print("Modder's net message!")
#		CvUtil.pyPrint( 'onModNetMessage' )

#FfH Card Game: begin
		if iData1 == CvUtil.Somnium : # iData1 == 0 : Solmnium message, iData2 = function, iData3 to iData5 = parameters
			if iData2 == 0 :
				if (iData3 == gc.getGame().getActivePlayer()):
					self.__EventSelectSolmniumPlayerBegin()
			elif iData2 == 1 :
				if (iData4 == gc.getGame().getActivePlayer()):
					self.__EventSolmniumConcedeGameBegin((iData3, iData4))
			else :
				cs.applyAction(iData2, iData3, iData4, iData5)
# FfH Card Game: end

## OOS fix by Snarko
		elif (iData1 == CvUtil.ChangeCiv): #iData1 is unused, to allow for a condition here. It must not be zero (would trigger somnium)
			CyGame().reassignPlayerAdvanced(iData2, iData3, -1)
## Declare war to Barbarians.
		elif (iData1 == CvUtil.BarbarianWar):
			gc.getTeam(iData2).declareWar(iData3, False, WarPlanTypes.WARPLAN_TOTAL)
#Magister
##		elif (iData1 == CvUtil.HyboremWhisper):
##			pPlayer = gc.getPlayer(iData2)
##			pPlot = CyMap().plot(iData3, iData4)
##			pCity = pPlot.getPlotCity()
##			pPlayer.acquireCity(pCity, False, True)

	def onInit(self, argsList):
		'Called when Civ starts up'
		CvUtil.pyPrint( 'OnInit' )

	def onUpdate(self, argsList):
		'Called every frame'
		fDeltaTime = argsList[0]

		# allow camera to be updated
		CvCameraControls.g_CameraControls.onUpdate( fDeltaTime )

	def onWindowActivation(self, argsList):
		'Called when the game window activates or deactivates'
		bActive = argsList[0]

	def onUnInit(self, argsList):
		'Called when Civ shuts down'
		CvUtil.pyPrint('OnUnInit')

	def onPreSave(self, argsList):
		"called before a game is actually saved"
		CvUtil.pyPrint('OnPreSave')

	def onSaveGame(self, argsList):
		"return the string to be saved - Must be a string"
		return ""

	def onLoadGame(self, argsList):
		try:
			import SaveDiagnostics
			SaveDiagnostics.onLoadGame()
		except:
			print("SaveDiagnostics.onLoadGame failed")
			import traceback
			traceback.print_exc()
		CvAdvisorUtils.resetNoLiberateCities()
		return 0

	def onGameStart(self, argsList):
		'Called at the start of the game'

		# lfgr 05/2020: Print some statistics
		# Mostly borrowed from victory screen
		print( "--------------------------" )
		print( "STARTING NEW GAME" )
		print( "Mapscript: %s" % gc.getMap().getMapScriptName() )
		print( "Map size: %s" % gc.getWorldInfo(gc.getMap().getWorldSize()).getTextKey() )
		print( "Game speed: %s" % gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getTextKey() )
		print( "Climate: %s" % gc.getClimateInfo(gc.getMap().getClimate()).getTextKey() )
		print( "Sea level: %s" % gc.getSeaLevelInfo(gc.getMap().getSeaLevel()).getTextKey() )
		print( "Starting era: %s" % gc.getEraInfo(gc.getGame().getStartEra()).getTextKey() )

		print( "Options:" )
		for eOption in xrange( gc.getNumGameOptionInfos() ) :
			if gc.getGame().isOption( eOption ) :
				print( " %s" % gc.getGameOptionInfo( eOption ).getType() )

		print( "Players:" )
		for ePlayer, pyPlayer in PyHelpers.PyGame().iterAliveCivPlayers() :
			pyPlayer.getLeaderHeadDescription()
			print( " #%d: %s/%s" % ( pyPlayer.getID(), pyPlayer.getName(), pyPlayer.getCivilizationName() ) )
		print( "--------------------------" )


		if CyGame().getWBMapScript():
			sf.gameStart()
		else:
			introMovie = CvIntroMovieScreen.CvIntroMovieScreen()
			introMovie.interfaceScreen()

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_THAW):
# Enhanced End of Winter - Adpated from FlavourMod

			FLAT_WORLDS = [ # map scripts with wrapping but no equator
				"ErebusWrap", "Erebus", "Erebus_mst",
			]
			MAX_EOW_PERCENTAGE = 0.25						# percentage of EoW on total game turns
			THAW_DELAY_PERCENTAGE = 0.05					# don't start thawing for x percent of EoW

			# forest varieties
			DECIDUOUS_FOREST = 0
			CONIFEROUS_FOREST = 1
			SNOWY_CONIFEROUS_FOREST = 2

			dice = gc.getGame().getSorenRand()

			iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
			iGrass = gc.getInfoTypeForString('TERRAIN_GRASS')
			iMarsh = gc.getInfoTypeForString('TERRAIN_MARSH')
			iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
			iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
			iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
			iIce = gc.getInfoTypeForString('FEATURE_ICE')
			iForest = gc.getInfoTypeForString('FEATURE_FOREST')
			iJungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
			iBlizzard = gc.getInfoTypeForString('FEATURE_BLIZZARD')

			iFloodPlains = gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')#Magister

#			iTotalGameTurns = gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getGameTurnInfo(0).iNumGameTurnsPerIncrement
#			iMaxEOWTurns = max(1, int(iTotalGameTurns * MAX_EOW_PERCENTAGE))
#			iThawDelayTurns = max(1, int(iMaxEOWTurns * THAW_DELAY_PERCENTAGE))

			iMaxLatitude = max(CyMap().getTopLatitude(), abs(CyMap().getBottomLatitude()))
			bIsFlatWorld = not (CyMap().isWrapX() or CyMap().isWrapY()) or CyMap().getMapScriptName() in FLAT_WORLDS

			for i in xrange (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				eTerrain = pPlot.getTerrainType()
				eFeature = pPlot.getFeatureType()
				iVariety = pPlot.getFeatureVariety()
				eBonus = pPlot.getBonusType(TeamTypes.NO_TEAM)

				iTurns = dice.get(110, "Thaw") + 40
				iTurns = (iTurns * gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getVictoryDelayPercent()) / 100
				if not bIsFlatWorld:
					iLatitude = abs(pPlot.getLatitude())
					iTurns = int(iTurns * ((float(iLatitude) / iMaxLatitude) ** 0.4))
#				iTurns += iThawDelayTurns

				# cover erebus' oceans and lakes in ice
				if pPlot.isWater():
					if bIsFlatWorld:
						if dice.get(100, "Flat World Ice") < 90:
							pPlot.setTempFeatureType(iIce, 0, iTurns)
					elif iLatitude + 10 > dice.get(50, "Ice"):
						pPlot.setTempFeatureType(iIce, 0, iTurns)

				# change terrains to colder climate versions
				if eTerrain == iTundra:
					if dice.get(100, "Tundra to Snow") < 90:
						pPlot.setTempTerrainType(iSnow, iTurns)
				elif eTerrain == iGrass:
					if eFeature != iJungle:
						if dice.get(100, "Grass to Snow or Tundra") < 60:
							pPlot.setTempTerrainType(iSnow, iTurns)
						else:
							pPlot.setTempTerrainType(iTundra, iTurns)
				elif eTerrain == iPlains:
					if dice.get(100, "Plains to Snow or Tundra") < 30:
						pPlot.setTempTerrainType(iSnow, iTurns)
					else:
						pPlot.setTempTerrainType(iTundra, iTurns)
				elif eTerrain == iDesert:
					if dice.get(100, "Desert to Tundra or Plains") < 50:
						pPlot.setTempTerrainType(iTundra, iTurns)
					else:
						pPlot.setTempTerrainType(iPlains, iTurns)
				elif eTerrain == iMarsh:
					pPlot.setTempTerrainType(iGrass, iTurns)

				# change forests to colder climate versions
				if eFeature == iForest:
					if iVariety == DECIDUOUS_FOREST:
						pPlot.setTempFeatureType(iForest, CONIFEROUS_FOREST, iTurns)
					elif iVariety == CONIFEROUS_FOREST:
						pPlot.setTempFeatureType(iForest, SNOWY_CONIFEROUS_FOREST, iTurns)
				elif eFeature == iJungle:
					pPlot.setTempFeatureType(iForest, DECIDUOUS_FOREST, iTurns)
				elif eFeature == iFloodPlains:
					pPlot.setTempFeatureType(FeatureTypes.NO_FEATURE, -1, iTurns)
				elif eFeature == FeatureTypes.NO_FEATURE:
					if dice.get(100, "Spawn Blizzard") < 5:
						pPlot.setFeatureType(iBlizzard, -1)

				# temporarily remove invalid bonuses or replace them (if food) with a valid surrogate
				if eBonus != BonusTypes.NO_BONUS and not gc.getBonusInfo(eBonus).isMana():
					pPlot.setBonusType(BonusTypes.NO_BONUS)
					if not pPlot.canHaveBonus(eBonus, True):
						if gc.getBonusInfo(eBonus).getYieldChange(YieldTypes.YIELD_FOOD) > 0:
							iPossibleTempFoodBonuses = []
							for iLoopBonus in xrange(gc.getNumBonusInfos()):
								if gc.getBonusInfo(iLoopBonus).getYieldChange(YieldTypes.YIELD_FOOD) > 0:
									if pPlot.canHaveBonus(iLoopBonus, True):
										iPossibleTempFoodBonuses.append(iLoopBonus)
							pPlot.setBonusType(eBonus)
							if len(iPossibleTempFoodBonuses) > 0:
								pPlot.setTempBonusType(iPossibleTempFoodBonuses[dice.get(len(iPossibleTempFoodBonuses), "Temp Food Bonus")], iTurns)
							else:
								pPlot.setTempBonusType(BonusTypes.NO_BONUS, iTurns)
						else:
							pPlot.setBonusType(eBonus)
							pPlot.setTempBonusType(BonusTypes.NO_BONUS, iTurns)
					else:
						pPlot.setBonusType(eBonus)
			Blizzards.doBlizzardTurn()
# End Enhanced End of Winter


		iElohim = gc.getInfoTypeForString('CIVILIZATION_ELOHIM')
		iLjosalfar = gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR')
		iSvartalfar = gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')
		iBannor = gc.getInfoTypeForString('CIVILIZATION_BANNOR')
		iClan = gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS')
		iKhazad = gc.getInfoTypeForString('CIVILIZATION_KHAZAD')
		iHippus = gc.getInfoTypeForString('CIVILIZATION_HIPPUS')
		iMalakim = gc.getInfoTypeForString('CIVILIZATION_MALAKIM')
		iCalabim = gc.getInfoTypeForString('CIVILIZATION_CALABIM')
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
		iMercurian = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')

		iHannah = gc.getInfoTypeForString('LEADER_HANNAH')

		iCodeOfLaws = gc.getInfoTypeForString('TECH_CODE_OF_LAWS')
		iOrdersFromHeaven = gc.getInfoTypeForString('TECH_ORDERS_FROM_HEAVEN')
		iWayOfEarthmother = gc.getInfoTypeForString('TECH_WAY_OF_THE_EARTHMOTHER')
		iWayOfForest = gc.getInfoTypeForString('TECH_WAY_OF_THE_FORESTS')
		iMessageFromDeep = gc.getInfoTypeForString('TECH_MESSAGE_FROM_THE_DEEP')
		iDeception = gc.getInfoTypeForString('TECH_DECEPTION')

		iEvil = gc.getInfoTypeForString('ALIGNMENT_EVIL')
		iNeutral = gc.getInfoTypeForString('ALIGNMENT_NEUTRAL')
		iGood = gc.getInfoTypeForString('ALIGNMENT_GOOD')

		iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
		iEmpyrean = gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')
		iRunes = gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH')
		iLeaves = gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')
		iUndertow = gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS')
		iEsus = gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS')
		iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
		iDragon = gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON')
		iHand = gc.getInfoTypeForString('RELIGION_WHITE_HAND')
		iOne = gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE')
		bDraw = gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			player = gc.getPlayer(iPlayer)
			if player.isAlive():
				iRel = player.getStateReligion()
				if iRel != -1:
					if iRel == iOrder:
						player.setAlignment(iGood)
					elif iRel == iEmpyrean:
						if player.getAlignment() == iEvil:
							player.setAlignment(iNeutral)
					elif iRel == iRunes:
						if player.getAlignment() == iEvil:
							player.setAlignment(iNeutral)
					elif iRel == iUndertow:
						if player.getAlignment() == iGood:
							player.setAlignment(iNeutral)
					elif iRel == iEsus:
						if player.getAlignment() == iGood:
							player.setAlignment(iNeutral)
					elif iRel == iVeil:
						player.setAlignment(iEvil)
					elif iRel == iHand:
						if bDraw:
							player.setAlignment(iEvil)
						elif player.getAlignment() == iGood:
							player.setAlignment(iNeutral)

				iCiv = player.getCivilizationType()
				eTeam = gc.getTeam(player.getTeam())
				if iCiv == iElohim:
					cf.showUniqueImprovements(iPlayer)
				elif iCiv == iLjosalfar:
					if not eTeam.isHasTech(iWayOfForest):
						iDiscount = eTeam.getResearchCost(iWayOfForest)/3
						eTeam.setResearchProgress(iWayOfForest, iDiscount,iPlayer)
					if CyGame().isCivEverActive(iSvartalfar):
						for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
							player2 = gc.getPlayer(iPlayer2)
							if player2.isAlive():
								if player2.getCivilizationType() == iSvartalfar:
									player.AI_changeAttitudeExtra(iPlayer2,-3)
				elif iCiv == iSvartalfar:
					if not eTeam.isHasTech(iDeception):
						iDiscount = eTeam.getResearchCost(iDeception)/4
						eTeam.setResearchProgress(iDeception, iDiscount,iPlayer)
					if CyGame().isCivEverActive(iLjosalfar):
						for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
							player2 = gc.getPlayer(iPlayer2)
							if player2.isAlive():
								if player2.getCivilizationType() == iLjosalfar:
									player.AI_changeAttitudeExtra(iPlayer2,-2)
				elif iCiv == iBannor:
					if not eTeam.isHasTech(iOrdersFromHeaven):
						iDiscount = eTeam.getResearchCost(iOrdersFromHeaven)/3
						eTeam.setResearchProgress(iOrdersFromHeaven, iDiscount,iPlayer)
					if not eTeam.isHasTech(iCodeOfLaws):
						iDiscount = eTeam.getResearchCost(iCodeOfLaws)/3
						eTeam.setResearchProgress(iCodeOfLaws, iDiscount,iPlayer)
					if CyGame().isCivEverActive(iClan):
						for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
							player2 = gc.getPlayer(iPlayer2)
							if player2.isAlive():
								if player2.getCivilizationType() == iClan:
									player.AI_changeAttitudeExtra(iPlayer2,-2)
				elif iCiv == iKhazad:
					if not eTeam.isHasTech(iWayOfEarthmother):
						iDiscount = eTeam.getResearchCost(iWayOfEarthmother)/4
						eTeam.setResearchProgress(iWayOfEarthmother, iDiscount,iPlayer)
					if CyGame().isCivEverActive(iHippus):
						for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
							player2 = gc.getPlayer(iPlayer2)
							if player2.isAlive():
								if player2.getCivilizationType() == iHippus:
									player.AI_changeAttitudeExtra(iPlayer2,-3)
				elif iCiv == iMalakim:
					if CyGame().isCivEverActive(iCalabim):
						for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
							player2 = gc.getPlayer(iPlayer2)
							if player2.isAlive():
								if player2.getCivilizationType() == iCalabim:
									player.AI_changeAttitudeExtra(iPlayer2,-3)
									player2.AI_changeAttitudeExtra(iPlayer,-7)
				elif iCiv == iInfernal:
					eTeam.makePeace(gc.getBARBARIAN_TEAM())
				elif iCiv == iMercurian:
					if CyGame().isCivEverActive(iInfernal):
						for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
							player2 = gc.getPlayer(iPlayer2)
							if player2.isAlive():
								if player2.getCivilizationType() == iInfernal:
									player.AI_changeAttitudeExtra(iPlayer2,-7)
									player2.AI_changeAttitudeExtra(iPlayer,-5)
				if player.getLeaderType() == iHannah:
					if not eTeam.isHasTech(iMessageFromDeep):
						iDiscount = eTeam.getResearchCost(iMessageFromDeep)/5
						eTeam.setResearchProgress(iMessageFromDeep, iDiscount,iPlayer)

		if not gc.getGame().isNetworkMultiPlayer():
			t = "TROPHY_FEAT_INTRODUCTION"
			if not CyGame().isHasTrophy(t):
				CyGame().changeTrophyValue(t, 1)
				sf.addPopupWB(CyTranslator().getText("TXT_KEY_FFH_INTRO",()),'art/interface/popups/FfHIntro.dds')

		if CyGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_BARBARIANS')) == False and (not CyGame().getWBMapScript()):
			iGoblinFort = gc.getInfoTypeForString('IMPROVEMENT_GOBLIN_FORT')
			bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
			for i in xrange (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.getImprovementType() == iGoblinFort:
					newDefenseUnit1 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER_SCORPION_CLAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_LAIRGUARDIAN, DirectionTypes.DIRECTION_SOUTH)
					newDefenseUnit1.setUnitAIType(gc.getInfoTypeForString('UNITAI_LAIRGUARDIAN'))

		if not CyGame().getWBMapScript():
			if not CyGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_BARBARIANS')):
				iGoblinFort = gc.getInfoTypeForString('IMPROVEMENT_GOBLIN_FORT')
				bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
				eTeam = gc.getTeam(gc.getBARBARIAN_TEAM())
				iUnit = gc.getInfoTypeForString('UNIT_GOBLIN')
				iPromotion1 = gc.getInfoTypeForString('PROMOTION_LAIR_GUARDIAN')
				iPromotion2 = gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY')
				iPromotion3 = gc.getInfoTypeForString('PROMOTION_SCORPION_CLAN')
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ARCHERY')) or CyGame().getStartEra() > gc.getInfoTypeForString('ERA_ANCIENT'):
					iUnit = gc.getInfoTypeForString('UNIT_ARCHER_SCORPION_CLAN')
				for i in xrange (CyMap().numPlots()):
					pPlot = CyMap().plotByIndex(i)
					if pPlot.getImprovementType() == iGoblinFort:
						newUnit = bPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_LAIRGUARDIAN, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setHasPromotion(iPromotion1, True)
						newUnit.setHasPromotion(iPromotion2, True)
						newUnit.setHasPromotion(iPromotion3, True)

			if gc.getGame().getGameTurnYear() == gc.getDefineINT("START_YEAR") and not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_START):
				for iPlayer in xrange(gc.getMAX_PLAYERS()):
					player = gc.getPlayer(iPlayer)
					if player.isAlive() and player.isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
						popupInfo.setText(u"showDawnOfMan")
						popupInfo.addPopup(iPlayer)
			else:
				CyInterface().setSoundSelectionReady(True)

		if gc.getGame().isPbem():
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iPlayer)
				if player.isAlive() and player.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_DETAILS)
					popupInfo.setOption1(False)
					popupInfo.addPopup(iPlayer)

		# Super Forts
		CyMap().calculateCanalAndChokePoints()

		CvAdvisorUtils.resetNoLiberateCities()

	def onGameEnd(self, argsList):
		'Called at the End of the game'
		print("Game is ending")
		return

	def onBeginGameTurn(self, argsList):
		'Called at the beginning of the end of each turn'
		iGameTurn = argsList[0]


		if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('UNITCLASS_ORTHUS'), 0):
			if not CyGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_ORTHUS')):
				iOrthusTurn = 75
				bOrthus = False
				if CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
					if iGameTurn >= iOrthusTurn / 3 * 2:
						bOrthus = True
				elif CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_NORMAL'):
					if iGameTurn >= iOrthusTurn:
						bOrthus = True
				elif CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
					if iGameTurn >= iOrthusTurn * 3 / 2:
						bOrthus = True
				elif CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
					if iGameTurn >= iOrthusTurn * 3:
						bOrthus = True
				if bOrthus:
					pPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
					iUnit = gc.getInfoTypeForString('UNIT_ORTHUS')
					cf.addUnit(iUnit)
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_ORTHUS_CREATION",()), str(gc.getUnitInfo(iUnit).getImage()))

		if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('UNITCLASS_BADB'), 0):
			iBadbTurn = 400
			bBadb = False
			iGameTurn = CyGame().getGameTurn()
			if CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
				if iGameTurn >= iBadbTurn / 3 * 2:
					bBadb = True
			elif CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_NORMAL'):
				if iGameTurn >= iBadbTurn:
					bBadb = True
			elif CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
				if iGameTurn >= iBadbTurn * 3 / 2:
					bBadb = True
			elif CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
				if iGameTurn >= iBadbTurn * 3:
					bBadb = True
			if bBadb:
				pBliz = cf.findImprovement(gc.getInfoTypeForString('IMPROVEMENT_BADBS_BLIZZARD'))
				if pBliz != -1:
					iUnit = gc.getInfoTypeForString('UNIT_BADB')
					newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(iUnit, pBliz.getX(), pBliz.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		if not CyGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_PLOT_COUNTER')):
			cf.doHellTerrain()


		iWW = gc.getInfoTypeForString('IMPROVEMENT_WHISPERING_WOOD')
		for pPlotWW in cf.findImprovements(iWW):
			if pPlotWW.isPythonActive():
				iX = pPlotWW.getX()
				iY = pPlotWW.getY()
				iRange = 1
				for iiX in xrange(iX-iRange, iX+1+iRange, 1):
					for iiY in xrange(iY-iRange, iY+1+iRange, 1):
						pLoopPlot = CyMap().plot(iiX, iiY)
						if pLoopPlot.isNone():continue
						for iLoopTeam in xrange(gc.getMAX_TEAMS()):
							if not pLoopPlot.isVisible(iLoopTeam, False):
								pLoopPlot.setRevealed(iLoopTeam, False, False, -1)

# GameSpeedTypes:
 # -1 = NO_GAMESPEED
 # 0 = GAMESPEED_MARATHON
 # 1 = GAMESPEED_EPIC
 # 2 = GAMESPEED_NORMAL
 # 3 = GAMESPEED_QUICK

		iRnd = 7 - CyGame().getGameSpeedType()
		if iGameTurn % (iRnd) == 0:
			iBB = gc.getInfoTypeForString('IMPROVEMENT_BADBS_BLIZZARD')
			lBB = cf.findImprovements(iBB)
			if len(lBB) > 0:
				pPlotBB = lBB[0]
				eSpell = gc.getInfoTypeForString('SPELL_EXPLORE_LAIR_BADBS_BLIZZARD')
				iIce = gc.getInfoTypeForString('BONUS_MANA_ICE')
				iBl = gc.getInfoTypeForString('FEATURE_BLIZZARD')
				lCold = [gc.getInfoTypeForString('TERRAIN_TUNDRA'),gc.getInfoTypeForString('TERRAIN_SNOW'),gc.getInfoTypeForString('TERRAIN_GLACIER'),gc.getInfoTypeForString('TERRAIN_WASTELAND')]
				iBestValue = 0
				pBestPlot = -1
				for i in xrange (CyMap().numPlots()):
					pTargetPlot = CyMap().plotByIndex(i)
					if pTargetPlot == pPlotBB:
						continue
					if pTargetPlot.isPeak():
						continue
					if pTargetPlot.isWater():
						continue
					if pTargetPlot.getBonusType(-1) != -1:
						continue
					iValue = 0
					iImp = pTargetPlot.getImprovementType()
					if iImp == -1:
						iValue += 100
					elif gc.getImprovementInfo(iImp).isPermanent():
						continue
					if pTargetPlot.getTerrainType() in lCold:
						iValue += 1000
					iValue += CyGame().getSorenRandNum(1000, "Badb move ")
					if not pTargetPlot.isOwned():
						iValue += 1000
					if iValue > iBestValue:
						iBestValue = iValue
						pBestPlot = pTargetPlot
				if pBestPlot != -1:
					sCaption = CvUtil.convertToStr(gc.getImprovementInfo(iBB).getDescription())
					lCaptionPlayers = []
					for i in xrange(CyEngine().getNumSigns()):
						pSign = CyEngine().getSignByIndex(i)
						if pSign.getCaption() == sCaption:
							loopPlayer = pSign.getPlayerType()
							lCaptionPlayers.append(loopPlayer)
							CyEngine().removeSign(pSign.getPlot(),loopPlayer)
					for loopPlayer in lCaptionPlayers:
						CyEngine().addSign(pBestPlot,loopPlayer, sCaption)

					iBadb = gc.getInfoTypeForString('UNIT_BADB')
					for i in xrange(pPlotBB.getNumUnits()):
						pUnit = pPlotBB.getUnit(i)
						if iBadb in [pUnit.getUnitType(), pUnit.getScenarioCounter()] or pUnit.getDelayedSpell() == eSpell:
							pUnit.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True)
							break
					else:
						bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
						iCount = bPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_BADB'))
						while iCount > 1:
							for pUnit in PyPlayer(gc.getBARBARIAN_PLAYER()).getUnitList():
								if iBadb in [pUnit.getUnitType(), pUnit.getScenarioCounter()]:
									pUnit.kill(False, -1)
									break
						if iCount == 1:
							for pUnit in PyPlayer(gc.getBARBARIAN_PLAYER()).getUnitList():
								if iBadb in [pUnit.getUnitType(), pUnit.getScenarioCounter()]:
									pUnit.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True)
									break


					iBonusReal = pPlotBB.getRealBonusType()
					if iBonusReal == iIce:
						pPlotBB.setBonusType(-1)
					else:
						pPlotBB.setBonusType(iBonusReal)
					pPlotBB.changeTempTerrainTimer(1-pPlotBB.getTempTerrainTimer())
					iReal = pPlotBB.getRealImprovementType()
					if iReal == iBB:
						pPlotBB.setImprovementType(-1)
					else:
						pPlotBB.setImprovementType(iReal)

					pBestPlot.setTempBonusType(iIce, iRnd)

					pBestPlot.setImprovementType(iBB)
					pBestPlot.setBonusType(iIce)
					pBestPlot.setFeatureType(iBl, 0)



		if CyGame().getWBMapScript():
			sf.doTurn()

# FfH Card Game: begin
		cs.doTurn()
# FfH Card Game: end

		Blizzards.doBlizzardTurn()		#Added in Blizzards: TC01

#		if( CyGame().getAIAutoPlay(self) == 0 ) :
		if( game.getAIAutoPlay(game.getActivePlayer()) == 0 ) :
			CvTopCivs.CvTopCivs().turnChecker(iGameTurn)

	def onEndGameTurn(self, argsList):
		'Called at the end of the end of each turn'
		iGameTurn = argsList[0]

	def onBeginPlayerTurn(self, argsList):
		'Called at the beginning of a players turn'
		iGameTurn, iPlayer = argsList
		pPlayer = gc.getPlayer(iPlayer)

		if pPlayer.isAlive() and not pPlayer.isBarbarian():
			player = PyPlayer(iPlayer)
			iTeam = pPlayer.getTeam()
			eTeam = gc.getTeam(iTeam)
			iCurrentEra = pPlayer.getCurrentEra()
			iStateReligion = pPlayer.getStateReligion()
			iCiv = pPlayer.getCivilizationType()
			infoCiv = gc.getCivilizationInfo(iCiv)
			iLeader = pPlayer.getLeaderType()
			iBarbTrait = gc.getInfoTypeForString('TRAIT_BARBARIAN')
			iTeamB = gc.getBARBARIAN_TEAM()
			bTeam = gc.getTeam(iTeamB)


			iSidar = gc.getInfoTypeForString('CIVILIZATION_SIDAR')

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_KHAZAD'):
				cf.doTurnKhazad(iPlayer)
			elif iCiv == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
				cf.doTurnLuchuirp(iPlayer)
				
			if pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_CRUSADE')):
				cf.doCrusade(iPlayer)
			elif pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_OVERCOUNCIL')):
				bShareMaps = CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_SHARE_MAPS'))
				bAdvancedTactics = gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS)
				if bAdvancedTactics or bShareMaps:
					iOvercouncil = gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')
					if pPlayer.isLoyalMember(iOvercouncil):
						for jPlayer in xrange(gc.getMAX_PLAYERS()):
							if iPlayer != jPlayer:
								pPlayer2 = gc.getPlayer(jPlayer)
								if pPlayer2.isAlive():
									if pPlayer2.isBarbarian():continue
									if pPlayer2.isFullMember(iOvercouncil):
										jTeam = pPlayer2.getTeam()
										if jTeam != iTeam:
											if bAdvancedTactics:
												if pPlayer.getNumCities() > 0:
													if not eTeam.isHasEmbassy(jTeam):
														eTeam.setHasEmbassy(jTeam,True)
											if bShareMaps:
												gc.getTeam(jTeam).changeStolenVisibilityTimer(iTeam,1)
												if pPlayer2.getCivilizationType() == iSidar:continue
												eTeam.changeStolenVisibilityTimer(jTeam,1)
			elif pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_UNDERCOUNCIL')):
				if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS):
					iUndercouncil = gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')
					if pPlayer.isLoyalMember(iUndercouncil):
						for jPlayer in xrange(gc.getMAX_PLAYERS()):
							if iPlayer != jPlayer:
								pPlayer2 = gc.getPlayer(jPlayer)
								if pPlayer2.isAlive():
									if pPlayer2.isBarbarian():continue
									if pPlayer2.isFullMember(iUndercouncil):
										jTeam = pPlayer2.getTeam()
										if jTeam != iTeam:
											if pPlayer.getNumCities() > 0:
												if not eTeam.isHasEmbassy(jTeam):
													eTeam.setHasEmbassy(jTeam, True)

					if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_EYES_AND_EARS_NETWORK')):

						for jPlayer in xrange(gc.getMAX_PLAYERS()):
							if iPlayer == jPlayer:continue
							pPlayer2 = gc.getPlayer(jPlayer)
							if pPlayer2.isAlive():
								if pPlayer2.isBarbarian():continue
								if pPlayer2.getCivilizationType() == iSidar:continue
								iTeam2 = pPlayer2.getTeam()
								eTeam2 = gc.getTeam(iTeam2)
								if eTeam2.isAlive():
									if eTeam.isHasMet(iTeam2):
										eTeam.changeStolenVisibilityTimer(iTeam2, 2)


			if iCiv == iSidar:
				for iTeam2 in xrange(gc.getMAX_TEAMS()):
					if iTeam == iTeam2:continue
					eTeam2 = gc.getTeam(iTeam2)
					if eTeam2.isAlive():
						while eTeam2.isStolenVisibility(iTeam):
							eTeam2.changeStolenVisibilityTimer(iTeam, -1)
			else:

				pCapital = pPlayer.getCapitalCity()
				if not pCapital.isNone():
					pCPlot = pCapital.plot()
					if not pCPlot.isNone():
						for jPlayer in xrange(gc.getMAX_PLAYERS()):
							if iPlayer != jPlayer:
								pPlayer2 = gc.getPlayer(jPlayer)
								if pPlayer2.isAlive():
									jTeam = pPlayer2.getTeam()
									if jTeam != iTeam:
										if eTeam.isHasEmbassy(jTeam):
											if not pCPlot.isRevealed(jTeam, False):
												pCPlot.setRevealed(jTeam, True, False, iTeam)


			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_FOXMEN'):
				if CyGame().getSorenRandNum(7, "Volatile Alignment") < 2:
					iGood  = gc.getInfoTypeForString('ALIGNMENT_GOOD')
					iNeutral = gc.getInfoTypeForString('ALIGNMENT_NEUTRAL')
					iEvil = gc.getInfoTypeForString('ALIGNMENT_EVIL')
					lAlignments = [
									# gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getAlignment(),#This does not seem to be exposed to python
									pPlayer.getAlignment(),
									pPlayer.getAlignment(),
									iGood,
									iNeutral,
									iNeutral,
									iNeutral,
									iEvil
									]
					iAlignment = lAlignments.pop(CyGame().getSorenRandNum(len(lAlignments), "Tali Fickle Alignment"))
					if pPlayer.getAlignment() != iAlignment:
						if pPlayer.isHuman():
							sAlignment = CyTranslator().getText("TXT_KEY_ALIGNMENT_NEUTRAL", ())
							if iAlignment == iGood:
								sAlignment = CyTranslator().getText("TXT_KEY_ALIGNMENT_GOOD", ())
							if iAlignment == iEvil:
								sAlignment = CyTranslator().getText("TXT_KEY_ALIGNMENT_EVIL", ())
							cf.addPopup(CyTranslator().getText("TXT_KEY_MESSAGE_TALI_ALIGNMENT",(sAlignment,)), 'Art/Interface/Buttons/Religions/Foxmen.dds')
						pPlayer.setAlignment(iAlignment)
						
						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_EMPYREAN')) > 0:
							bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN') or pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')) or iAlignment == iGood
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN_HOSTILE')
							
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
											
						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_BROTHERHOOD')) > 0:
							bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS') or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_PACIFISM')) or iAlignment == iGood
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD_HOSTILE')
							iCalabim = gc.getInfoTypeForString('CIVILIZATION_CALABIM')
							iTempleBlind = gc.getInfoTypeForString('BUILDING_TEMPLE_BLIND_BROTHERHOOD')
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if loopCity.getCivilizationType() == iCalabim:
								
									if loopCity.getNumBuilding(iTempleHostile) or loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleBlind, 1)
										
								else:
									if bFriendly:
										if loopCity.getNumBuilding(iTempleHostile):
											loopCity.setNumRealBuilding(iTempleHostile, 0)
											loopCity.setNumRealBuilding(iTempleFriendly, 1)
											loopCity.setNumRealBuilding(iTempleBlind, 0)
										else:
											loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
											loopCity.setBuildingProduction(iTempleHostile, 0)
											if loopCity.getProductionBuilding () == iTempleHostile:
												loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
									else:
										if loopCity.getNumBuilding(iTempleFriendly):
											loopCity.setNumRealBuilding(iTempleFriendly, 0)
											loopCity.setNumRealBuilding(iTempleHostile, 1)
											loopCity.setNumRealBuilding(iTempleBlind, 0)
										else:
											loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
											loopCity.setBuildingProduction(iTempleFriendly, 0)
											if loopCity.getProductionBuilding () == iTempleFriendly:
												loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
											
											
						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARTIFICERY')) > 0:
							bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RINGGIVER') or iAlignment == iGood or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_ARETE'))
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_ARTIFICERY')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_ARTIFICERY_HOSTILE')
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
											
											
						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_ORDER')) > 0:
							bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ORDER') or iAlignment == iGood
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER_HOSTILE')
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)

						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_UNBLEMISHED')) > 0:
							bFriendly = pPlayer.getStateReligion() in [gc.getInfoTypeForString('RELIGION_UNBLEMISHED'),gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')] or iAlignment == iGood
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED_HOSTILE')
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
											
											
						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_KILMORPH')) > 0:
							bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH') or (iAlignment != iEvil and pPlayer.getStateReligion() != gc.getInfoTypeForString('RELIGION_FOXMEN'))
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH_HOSTILE')

							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
						
						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_OVERLORDS')) > 0:
							bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS') or iAlignment != iGood
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS_HOSTILE')
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
											
						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_GAMBLING_HOUSE')) > 0:
							bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY') or iAlignment != iGood
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE_HOSTILE')
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
											
											
						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_ANOINTED')) > 0:
							bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_ANOINTED') or iAlignment == iEvil
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED_HOSTILE')
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)

						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_VEIL')) > 0:
							bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL') or iAlignment == iEvil
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL_HOSTILE')
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
											
											
						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOPHET')) > 0:
							bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_EMBER_LEGION') or iAlignment == iEvil
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_TOPHET_HOSTILE')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE_HOSTILE')
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
											
						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_INTERSTICE')) > 0:
							bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COVEN') or iAlignment == iEvil
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_INTERSTICE')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_INTERSTICE_HOSTILE')
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
											
						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_HAND')) > 0:
							bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_WHITE_HAND')
							if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
								iAuricPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
								if iAuricPlayer != -1:
									pAuricPlayer = gc.getPlayer(iAuricPlayer)
									if pAuricPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AURIC')) > 0:
										iTeam = pPlayer.getTeam()
										eTeam = gc.getTeam(iTeam)
										iAuricTeam = pAuricPlayer.getTeam()
										if iAuricTeam == iTeam:
											bFriendly = True
										elif eTeam.isVassal(iTeam):
											bFriendly = True
										elif eTeam.isAtWar(iAuricTeam):
											bFriendly = False
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND_HOSTILE')
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
											
						if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_APHOTIC_THRONE')) > 0:
							bFriendly = (pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS') or pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')) ) or iAlignment == iEvil
							iTempleFriendly = gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE')
							iTempleHostile = gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE_HOSTILE')
							
							for pyCity in PyPlayer(iPlayer).getCityList():
								loopCity = pyCity.GetCy()
								if bFriendly:
									if loopCity.getNumBuilding(iTempleHostile):
										loopCity.setNumRealBuilding(iTempleHostile, 0)
										loopCity.setNumRealBuilding(iTempleFriendly, 1)
									else:
										loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
										loopCity.setBuildingProduction(iTempleHostile, 0)
										if loopCity.getProductionBuilding () == iTempleHostile:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
								else:
									if loopCity.getNumBuilding(iTempleFriendly):
										loopCity.setNumRealBuilding(iTempleFriendly, 0)
										loopCity.setNumRealBuilding(iTempleHostile, 1)
									else:
										loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
										loopCity.setBuildingProduction(iTempleFriendly, 0)
										if loopCity.getProductionBuilding () == iTempleFriendly:
											loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)



			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_INSANE')):
				if CyGame().getSorenRandNum(1000, "Insane") < 20:
					iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_TRAIT_INSANE')
					triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, iPlayer, -1, -1, -1, -1, -1)

			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_ADAPTIVE')):
				iBaseCycle = 100
				iCycle = (iBaseCycle * gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getVictoryDelayPercent()) / 100
				for i in xrange(10):
					if (i * iCycle) - 5 == iGameTurn:
						iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_TRAIT_ADAPTIVE')
						triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, iPlayer, -1, -1, -1, -1, -1)


			if not eTeam.isAVassal():#Vassals do not control their own diplomacy
				if pPlayer.hasTrait(iBarbTrait):
					if bTeam.isAtWar(iTeam):
						if 2 * CyGame().getPlayerScore(iPlayer) < 3*CyGame().getPlayerScore(CyGame().getRankPlayer(1)):
							bTeam.makePeace(iTeam)
							if pPlayer.isHuman() and iPlayer == CyGame().getActivePlayer():
								cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_BARBARIAN_RESTORE_TRUCE",()), 'art/interface/popups/Barbarian.dds')
					elif not cf.grace():
						if 3 * CyGame().getPlayerScore(iPlayer) >= 4 * CyGame().getPlayerScore(CyGame().getRankPlayer(1)):

							for iEvent in [gc.getInfoTypeForString('EVENT_SUMMON_HYBOREM'), gc.getInfoTypeForString('EVENT_SUMMON_JUDECCA'), gc.getInfoTypeForString('EVENT_SUMMON_LETHE'), gc.getInfoTypeForString('EVENT_SUMMON_MERESIN'), gc.getInfoTypeForString('EVENT_SUMMON_OUZZA'), gc.getInfoTypeForString('EVENT_SUMMON_SALLOS'), gc.getInfoTypeForString('EVENT_SUMMON_STATIUS')]:
								if pPlayer.getEventOccured(iEvent):
									break
							else:
								if bTeam.canDeclareWar(iTeam):
									bTeam.declareWar(iTeam, False, WarPlanTypes.WARPLAN_TOTAL)
									if pPlayer.isHuman() and iPlayer == CyGame().getActivePlayer():
										cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_BARBARIAN_DECLARE_WAR",()), 'art/interface/popups/Barbarian.dds')


				else:

					for iEvent in [gc.getInfoTypeForString('EVENT_SUMMON_HYBOREM'), gc.getInfoTypeForString('EVENT_SUMMON_JUDECCA'), gc.getInfoTypeForString('EVENT_SUMMON_LETHE'), gc.getInfoTypeForString('EVENT_SUMMON_MERESIN'), gc.getInfoTypeForString('EVENT_SUMMON_OUZZA'), gc.getInfoTypeForString('EVENT_SUMMON_SALLOS'), gc.getInfoTypeForString('EVENT_SUMMON_STATIUS')]:
						if pPlayer.getEventOccured(iEvent):
							break
					else:
						if bTeam.canDeclareWar(iTeam):
							bTeam.declareWar(iTeam, False, WarPlanTypes.WARPLAN_TOTAL)
							if pPlayer.isHuman() and iPlayer == CyGame().getActivePlayer():
								cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_BARBARIAN_DECLARE_WAR",()), 'art/interface/popups/Barbarian.dds')


		cf.doCitiesTurn(iPlayer)

		if not pPlayer.isHuman():
			if not CyGame().getWBMapScript():
				cf.warScript(iPlayer)


	def onEndPlayerTurn(self, argsList):
		'Called at the end of a players turn'
		iGameTurn, iPlayer = argsList
		pPlayer = gc.getPlayer(iPlayer)
		if gc.getGame().getElapsedGameTurns() == 1:
			if pPlayer.isHuman():
				if pPlayer.canRevolution(0):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_CHANGECIVIC)
					popupInfo.addPopup(iPlayer)
		CvAdvisorUtils.resetAdvisorNags()
		CvAdvisorUtils.endTurnFeats(iPlayer)
		if CyGame().getWBMapScript():
			sf.onEndPlayerTurn(iGameTurn, iPlayer)

		if pPlayer.isAlive() and not pPlayer.isBarbarian():
			player = PyPlayer(iPlayer)
			iTeam = pPlayer.getTeam()
			eTeam = gc.getTeam(iTeam)
			iCurrentEra = pPlayer.getCurrentEra()
			iStateReligion = pPlayer.getStateReligion()
			iCiv = pPlayer.getCivilizationType()
			iLeader = pPlayer.getLeaderType()
			iBarbTrait = gc.getInfoTypeForString('TRAIT_BARBARIAN')
			iTeamB = gc.getBARBARIAN_TEAM()
			bTeam = gc.getTeam(iTeamB)


			if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_WHITE_HAND')) > 0:
				iWH = gc.getInfoTypeForString('RELIGION_WHITE_HAND')

				iAuric = gc.getInfoTypeForString('LEADER_AURIC')
				iAuricClass = gc.getInfoTypeForString('UNITCLASS_AURIC')
				iAuricPlayer = cf.getLeader(iAuric)
				iAuricTeam = -1
				if iAuricPlayer != -1:

					if iCiv == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):

						for iHandCleric, iAvatarClass, iAvatar in [
																	(iAuric, iAuricClass,gc.getInfoTypeForString('UNIT_AURIC')),
																	(gc.getInfoTypeForString('LEADER_ANAGANTIOS'), gc.getInfoTypeForString('UNITCLASS_ANAGANTIOS'), gc.getInfoTypeForString('UNIT_ANAGANTIOS')),
																	(gc.getInfoTypeForString('LEADER_DUMANNIOS'), gc.getInfoTypeForString('UNITCLASS_DUMANNIOS'), gc.getInfoTypeForString('UNIT_DUMANNIOS')),
																	(gc.getInfoTypeForString('LEADER_RIUROS'), gc.getInfoTypeForString('UNITCLASS_RIUROS'), gc.getInfoTypeForString('UNIT_RIUROS'))
							]:
							if iLeader == iHandCleric:
								if CyGame().getUnitClassCreatedCount(iAvatarClass) == 0:
									cf.giftUnitToPlayer(iAvatar, iPlayer, 0, -1, -1,iWH)

								if pPlayer.canConvert(iWH):
									pPlayer.setLastStateReligion(iWH)
									pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))
								break

					pAuricPlayer = gc.getPlayer(iAuricPlayer)
					if pAuricPlayer.getUnitClassCount(iAuricClass) > 0:
						iAuricTeam = pAuricPlayer.getTeam()
				if iAuricTeam == -1:

					pass
				elif iTeam == iAuricTeam:
					pass
				elif iLeader != iAuric:
					if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
						if iStateReligion == iWH:
							if eTeam.isAtWar(iAuricTeam):
								pPlayer.setLastStateReligion(-1)
								iStateReligion = -1
							elif iTeam != iAuricTeam:
								gc.getTeam(iAuricTeam).assignVassal(iTeam, True)
						elif pPlayer.canConvert(iWH):
							if eTeam.isVassal(iAuricTeam):
								pPlayer.setLastStateReligion(iWH)
								pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))



			if iCiv != gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				iInfernalPact = gc.getInfoTypeForString('PROJECT_INFERNAL_PACT')

				if eTeam.getProjectCount(iInfernalPact) > 0:


					iAV = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
					lPacts = [	(gc.getInfoTypeForString('LEADER_HYBOREM'), gc.getInfoTypeForString('EVENT_SUMMON_HYBOREM')),
								(gc.getInfoTypeForString('LEADER_JUDECCA'),gc.getInfoTypeForString('EVENT_SUMMON_JUDECCA')),
								(gc.getInfoTypeForString('LEADER_LETHE'), gc.getInfoTypeForString('EVENT_SUMMON_LETHE')),
								(gc.getInfoTypeForString('LEADER_MERESIN'), gc.getInfoTypeForString('EVENT_SUMMON_MERESIN')),
								(gc.getInfoTypeForString('LEADER_OUZZA'), gc.getInfoTypeForString('EVENT_SUMMON_OUZZA')),
								(gc.getInfoTypeForString('LEADER_SALLOS'), gc.getInfoTypeForString('EVENT_SUMMON_SALLOS')),
								(gc.getInfoTypeForString('LEADER_STATIUS'), gc.getInfoTypeForString('EVENT_SUMMON_STATIUS')),
								]

					for iDemon, iEvent in lPacts:
						if pPlayer.getLeaderType() == iDemon:continue
						if pPlayer.getEventOccured(iEvent):

							bBreak = False
							iDemonPlayer = cf.getLeader(iDemon)
							if iDemonPlayer == -1:
								bBreak = True
							else:
								pDemonPlayer = gc.getPlayer(iDemonPlayer)
								iDemonTeam = pDemonPlayer.getTeam()
								if iAV != pPlayer.getStateReligion():
									if not CyGame().getWBMapScript():
										bBreak = True
										pDemonPlayer.AI_changeAttitudeExtra(iPlayer,-12)
										gc.getTeam(iDemonTeam).setHasPrepareWar(iTeam,True)
								iAvatar = cf.getHero(pDemonPlayer)
								if pDemonPlayer.getUnitClassCount(iAvatar) < 1:
									bBreak = True
	##								eTeam.changeProjectCount(iInfernalPact, -1)
								if eTeam.isAtWar(iDemonTeam):
									bBreak = True
							if bBreak:
								pPlayer.resetEventOccured(iEvent)
								if pPlayer.isHuman():
									infoD = gc.getLeaderHeadInfo(iDemon)
									cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_INFERNAL_PACT_BROKEN",(infoD.getDescription(), )), infoD.getButton())


								if not pPlayer.hasTrait( gc.getInfoTypeForString('TRAIT_BARBARIAN')):
									bTeam = gc.getTeam(gc.getBARBARIAN_TEAM())
									iTeam = pPlayer.getTeam()
									if not bTeam.isAtWar(iTeam):
										if bTeam.canDeclareWar(iTeam):
											bTeam.declareWar(iTeam, False, WarPlanTypes.WARPLAN_TOTAL)

										if pPlayer.isHuman():
											cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_BARBARIAN_DECLARE_WAR",()), 'art/interface/popups/Barbarian.dds')



		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LOAD_SCREEN):#I have repurposed this to be Control Whole Team
			if not (gc.getGame().isGameMultiPlayer () or gc.getGame().isHotSeat() or gc.getGame().isNetworkMultiPlayer()):#In hotseat games this may result in skipping players. I imagine there would be similar issues in other multiplayer games
				if pPlayer.isHuman():
					iTeam = pPlayer.getTeam()
					if gc.getTeam(iTeam).getNumMembers() > 1:
						for iLoopPlayer in xrange(iPlayer,gc.getMAX_PLAYERS()):
							pLoopPlayer = gc.getPlayer(iLoopPlayer)
							if iTeam == pLoopPlayer.getTeam():
								if pLoopPlayer.isAlive():
									if not pLoopPlayer.isHuman():
										CyGame().reassignPlayerAdvanced(iPlayer, iLoopPlayer, -1)
										break
						else:
							for iLoopPlayer in xrange(0,iPlayer):
								pLoopPlayer = gc.getPlayer(iLoopPlayer)
								if iTeam == pLoopPlayer.getTeam():
									if pLoopPlayer.isAlive():
										if not pLoopPlayer.isHuman():
											CyGame().reassignPlayerAdvanced(iPlayer, iLoopPlayer, -1)
											break

	def onEndTurnReady(self, argsList):
		iGameTurn = argsList[0]

	def onFirstContact(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Contact'
		iTeamX,iHasMetTeamY = argsList
		if (not self.__LOG_CONTACT):
			return
		CvUtil.pyPrint('Team %d has met Team %d' %(iTeamX, iHasMetTeamY))

	def onCombatResult(self, argsList):
		'Combat Result'
		pWinner,pLoser = argsList

		iPlayerW = pWinner.getOwner()
		playerX = PyPlayer(iPlayerW)

		iTypeWinner = pWinner.getUnitType()
		unitX = PyInfo.UnitInfo(iTypeWinner)

		iPlayerL = pLoser.getOwner()
		playerY = PyPlayer(iPlayerL)

		iTypeLoser = pLoser.getUnitType()
		unitY = PyInfo.UnitInfo(iTypeLoser)

		if pLoser.getDuration() == 0 and pLoser.getCaptureUnitType(pWinner.getCivilizationType()) == -1:
			iUnitCombatLoser = pLoser.getUnitCombatType()
			iBeast = gc.getInfoTypeForString('UNITCOMBAT_BEAST')
			iAnimal = gc.getInfoTypeForString('UNITCOMBAT_ANIMAL')
			iCasswallawn = gc.getInfoTypeForString('PROMOTION_CASSWALLAWN')
			lBeasts = [iAnimal, iBeast]


			if pLoser.getUnitType() == gc.getInfoTypeForString('UNIT_AURIC_ASCENDED'):
				pLoser.changeImmortal(1)
				pLoser.setDamage(0, iPlayerL)
			if pLoser.getUnitType() == gc.getInfoTypeForString('UNIT_OS_GABELLA'):
				pLoser.changeImmortal(1)
				pLoser.setDamage(0, iPlayerL)

			if pLoser.getUnitType() == gc.getInfoTypeForString('UNIT_KHALIDA'):
				pLoser.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'), True)
				pLoser.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING2'), True)
				iNum = CyGame().getSorenRandNum(cf.getNumBonusEffective(iPlayerL, gc.getInfoTypeForString('BONUS_MANA_DEATH'), pLoser),"Khalida Suicide")
				if iNum > 0:
					pLoser.setBaseCombatStr(pLoser.baseCombatStr() + iNum)
					pLoser.setBaseCombatStrDefense(pLoser.baseCombatStrDefense() + iNum)
				# pLoser.changeImmortal(1)
				pLoser.setHasCasted(False)
				pLoser.setMadeAttack(False)
				pLoser.setDamage(0, iPlayerL)



			if (iUnitCombatLoser == iAnimal and pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL')) ) or (iUnitCombatLoser == iBeast and pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUBDUE_BEASTS'))):#This should stop units captured instead of killed from leaving sluaghs or dragon bones behind
				pLoser.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION'),True)
			else:

				pPlayerW = gc.getPlayer(iPlayerW)
				pPlayerL = gc.getPlayer(iPlayerL)

				if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SCAVENGER')):
					cf.scavenge(pWinner, pLoser)


				if pWinner.getDuration() == 0:
					if pLoser.isHasPromotion(iCasswallawn):
						if pWinner.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ADEPT'):
							if CyGame().getSorenRandNum(7, pWinner.getName().encode('latin_1','replace') + ' Becomes Casswallawn in place of'+ pLoser.getName().encode('latin_1','replace')) < 5:
								CyInterface().addMessage(iPlayerW,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_CASSWALLAWN_USURPED",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Units/Gastrius.dds',ColorTypes(8),pWinner.getX(),pWinner.getY(),True,True)
								CyInterface().addMessage(iPlayerL,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_CASSWALLAWN_USURPED",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Units/Gastrius.dds',ColorTypes(7),pWinner.getX(),pWinner.getY(),True,True)
								infoLoser = gc.getUnitInfo(pLoser.getUnitType())
								for iProm in [iCasswallawn, gc.getInfoTypeForString('PROMOTION_CHANNELING1'), gc.getInfoTypeForString('PROMOTION_CHANNELING2'), gc.getInfoTypeForString('PROMOTION_CHANNELING3'), gc.getInfoTypeForString('PROMOTION_CHANNELING4'), gc.getInfoTypeForString('PROMOTION_AFFINITY_METAMAGIC')]:
									if pLoser.isHasPromotion(iProm):
										pWinner.setHasPromotion(iProm, True)
										if not infoLoser.getFreePromotions(iProm):
											pLoser.setHasPromotion(iProm, False)

					iHero = gc.getInfoTypeForString('PROMOTION_HERO')
					if pLoser.isHasPromotion(iHero):
						if pLoser.getDuration() == 0:
							if not pWinner.isHasPromotion(iHero):
								if CyGame().getSorenRandNum(7, "Hero " + pWinner.getName().encode('latin_1','replace') + ' slayer of '+ pLoser.getName().encode('latin_1','replace')) < 1:
									pWinner.setHasPromotion(iHero, True)

				if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MIMIC')):
					listDontCopy = [	gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'),
								gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS'),
								gc.getInfoTypeForString('PROMOTION_MITHRIL_WEAPONS'),
								gc.getInfoTypeForString('PROMOTION_GREAT_GENERAL'),
								gc.getInfoTypeForString('PROMOTION_DIVINE'),
								gc.getInfoTypeForString('PROMOTION_CHANNELING4'),
								gc.getInfoTypeForString('PROMOTION_CHANNELING3'),
								gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'),
								gc.getInfoTypeForString('PROMOTION_MERCENARY'),
								gc.getInfoTypeForString('PROMOTION_MERCENARY_RECRUITER'),
								gc.getInfoTypeForString('PROMOTION_CANNOT_CAST'),
								gc.getInfoTypeForString('PROMOTION_IMMORTAL'),
								gc.getInfoTypeForString('PROMOTION_TARGET_WEAKEST'),
								iCasswallawn
								]

					listProms = []
					iCount = 0
					for iProm in xrange(gc.getNumPromotionInfos()):
						if pLoser.isHasPromotion(iProm):
							if iProm in listDontCopy:
								continue
							info = gc.getPromotionInfo(iProm)
							if info.isGraphicalOnly():
								continue
							if info.isEquipment():
								continue
							if info.isRace():
								continue
							if info.getAIWeight() < 0:
								continue
							if pWinner.isHasPromotion(iProm):
								iCount += 1
							else:
								listProms.append(iProm)
					if len(listProms) > 0:
						iCount += 1
						iProm = listProms[CyGame().getSorenRandNum(len(listProms), "Mimic" + pWinner.getName().encode('latin_1','replace') + ' slayer of '+ pLoser.getName().encode('latin_1','replace'))]
						infoProm = gc.getPromotionInfo(iProm)
						pWinner.setHasPromotion(iProm, True)
						CyInterface().addMessage(iPlayerW,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PROMOTION_STOLEN", (infoProm.getDescription(),)),'',1,infoProm.getButton(),ColorTypes(8),pWinner.getX(),pWinner.getY(),True,True)
						CyInterface().addMessage(iPlayerL,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PROMOTION_STOLEN", (infoProm.getDescription(),)),'',1,infoProm.getButton(),ColorTypes(7),pWinner.getX(),pWinner.getY(),True,True)
					if iCount >= 20:
						if pPlayerW.isHuman():
							t = "TROPHY_FEAT_MIMIC_20"
							if not CyGame().isHasTrophy(t):
								CyGame().changeTrophyValue(t, 1)

				iGodslayer = gc.getInfoTypeForString('PROMOTION_GODSLAYER')
				iAvatar = gc.getInfoTypeForString('PROMOTION_AVATAR')

				iCaveaAngelorum = gc.getInfoTypeForString('PROMOTION_ANGELORUM_CAVEA')
				iCaptusAngelorum = gc.getInfoTypeForString('PROMOTION_CAPTUS_CAVEAE_ANGELORUM')

				iCaveaSawol = gc.getInfoTypeForString('PROMOTION_SAWOL_CAVEA')
				iCaptusSawol = gc.getInfoTypeForString('PROMOTION_CAPTUS_CAVEAE_SAWOL')

				iNetherblade = gc.getInfoTypeForString('PROMOTION_NETHER_BLADE')
				iNBind = gc.getInfoTypeForString('PROMOTION_NETHERBIND')

				iCustos = gc.getInfoTypeForString('PROMOTION_CUSTOS_JUDICII')
				iCarcer = gc.getInfoTypeForString('PROMOTION_INCARCERATUS_JUDICII')

					
				if pWinner.isHasPromotion(iGodslayer):
					cf.makeMortal(pLoser)
					if pLoser.isHasPromotion(iAvatar):
						pLoser.setHasPromotion(iAvatar, False)
						gc.getPlayer(iPlayerL).AI_changeAttitudeExtra(iPlayerW,-12)
						pLoser.kill(True, iPlayerW)
				elif pLoser.isHasPromotion(iGodslayer):
					cf.makeMortal(pWinner)
					if pWinner.isHasPromotion(iAvatar):
						pWinner.setHasPromotion(iAvatar, False)
						gc.getPlayer(iPlayerW).AI_changeAttitudeExtra(iPlayerL,-12)
						pWinner.kill(True, iPlayerL)
				if pWinner.isHasPromotion(iNetherblade):
					pLoser.setHasPromotion(iNBind, True)
					cf.makeMortal(pLoser)
					if isWorldUnitClass(pLoser.getUnitClassType()):
						gc.getPlayer(iPlayerL).AI_changeAttitudeExtra(iPlayerW,-7)
						pLoser.kill(True, iPlayerW)
				elif pLoser.isHasPromotion(iNetherblade):
					cf.makeMortal(pWinner)
					if isWorldUnitClass(pWinner.getUnitClassType()):
						pWinner.setHasPromotion(iNBind, True)
						gc.getPlayer(iPlayerW).AI_changeAttitudeExtra(iPlayerL,-7)
						pWinner.kill(True, iPlayerL)
				if pWinner.isHasPromotion(iCaveaSawol):
					pLoser.setHasPromotion(iCaptusSawol, True)
					cf.makeMortal(pLoser)
					if isWorldUnitClass(pLoser.getUnitClassType()):
						gc.getPlayer(iPlayerL).AI_changeAttitudeExtra(iPlayerW,-7)
##						pLoser.kill(True, iPlayerW)
				if pWinner.isHasPromotion(iCaveaAngelorum):
					if pLoser.getRace() in [gc.getInfoTypeForString('PROMOTION_DEMON'),gc.getInfoTypeForString('PROMOTION_ANGEL')]:
						pLoser.setHasPromotion(iCaptusAngelorum, True)
						cf.makeMortal(pLoser)
						if isWorldUnitClass(pLoser.getUnitClassType()):
							gc.getPlayer(iPlayerL).AI_changeAttitudeExtra(iPlayerW,-7)
						pLoser.kill(True, iPlayerW)
					elif pLoser.isHasPromotion(gc.getInfoTypeForString('PROMOTION_POSSESSED')):
						pLoser.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POSSESSED'), False)
				elif pWinner.isHasPromotion(iCustos):
					if pLoser.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON')):
						pLoser.setHasPromotion(iCarcer, True)
						cf.makeMortal(pLoser)
						if isWorldUnitClass(pLoser.getUnitClassType()):
							gc.getPlayer(iPlayerL).AI_changeAttitudeExtra(iPlayerW,-7)
						pLoser.kill(True, iPlayerW)
					elif pLoser.isHasPromotion(gc.getInfoTypeForString('PROMOTION_POSSESSED')):
						pLoser.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POSSESSED'), False)
				iX = pWinner.getX()
				iY = pWinner.getY()
				if pLoser.isAlive():
					if iTypeWinner == gc.getInfoTypeForString('UNIT_EMRYS'):
						if iUnitCombatLoser == gc.getInfoTypeForString('UNITCOMBAT_ADEPT'):
							if not isLimitedUnitClass(pLoser.getUnitClassType()):
								if CyGame().getSorenRandNum(100, pWinner.getName().encode('latin_1','replace') + ' recruits '+ pLoser.getName().encode('latin_1','replace')) < 2*pWinner.getLevel() - pLoser.getLevel() +2*pWinner.getExperience() - pLoser.getExperience():
									newUnit = pPlayerW.initUnit(iTypeLoser, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
									cf.removeAffinities(newUnit)
									newUnit.finishMoves()
									newUnit.setDamage(90, iPlayerW)
									newUnit.setLevel(pLoser.getLevel())
									newUnit.setExperience(pLoser.getExperience(), -1)
									newUnit.setName(pLoser.getNameNoDesc())
									newUnit.setReligion(pLoser.getReligion())
									for iCount in xrange(gc.getNumPromotionInfos()):
										if pLoser.isHasPromotion(iCount) and not gc.getPromotionInfo(iCount).isEquipment():
											newUnit.setHasPromotion(iCount, True)
									if pWinner.isHiddenNationality():
										newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)

					if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VILE_TOUCH')):
						pLoser.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WITHERED'), True)
					if pWinner.getDamageTypeCombat(gc.getInfoTypeForString('DAMAGE_POISON')) > 0:
						if pLoser.getDamage() > 0:
							if not pLoser.isHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED')):
								if pLoser.getDamageTypeResist(gc.getInfoTypeForString('DAMAGE_POISON')) < 100:
									if CyGame().getSorenRandNum(100,"Poisoned") >= pLoser.getDamageTypeResist(gc.getInfoTypeForString('DAMAGE_POISON')):
										pLoser.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED'), True)
					iRavenous = gc.getInfoTypeForString('PROMOTION_RAVENOUS')
					iWerewolf = gc.getInfoTypeForString('PROMOTION_WEREWOLF')
					lImmuneLycanthropy = [	iWerewolf,
							gc.getInfoTypeForString('PROMOTION_WEREWOLF_SLAYING'),
							gc.getInfoTypeForString('PROMOTION_IMMUNE_DISEASE'),
							gc.getInfoTypeForString('PROMOTION_SPIRIT3'),
							gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT'),
							gc.getInfoTypeForString('PROMOTION_ILLUSION'),
							gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION')
							]
					if pWinner.isHasPromotion(iRavenous):
						if not pLoser.isImmortal():
							if not iUnitCombatLoser in lBeasts:
								pWinner.setHasPromotion(iRavenous, False)
					if pLoser.isHasPromotion(iWerewolf):
						if pWinner.isAlive() and pWinner.getDamage() > 0:
							if not pWinner.getUnitCombatType() in lBeasts:
								for iProm in lImmuneLycanthropy:
									if pWinner.isHasPromotion(iProm):
										break
								else:
									iChance = pLoser.getLevel() - pWinner.getLevel()
									if iTypeLoser == gc.getInfoTypeForString('UNIT_DUIN'):
										iChance += 5
									elif iTypeLoser == gc.getInfoTypeForString('UNIT_GREATER_WEREWOLF'):
										iChance += 3
									elif iTypeLoser == gc.getInfoTypeForString('UNIT_WEREWOLF'):
										iChance += 2
									elif iTypeLoser == gc.getInfoTypeForString('UNIT_RAVENOUS_WEREWOLF'):
										iChance += 1
									if iChance > 0:
										if CyGame().getSorenRandNum(100, "Spread Lycanthropy" + pWinner.getName().encode('latin_1','replace') + ' slayer of '+ pLoser.getName().encode('latin_1','replace')) < iChance:
											sName = pWinner.getName()
											CyInterface().addMessage(iPlayerW,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SPREAD_LYCANTHROPY",(sName,)),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Promotions/Werewolf.dds',ColorTypes(7),iX,iY,True,True)
											CyInterface().addMessage(iPlayerL,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SPREAD_LYCANTHROPY",(sName,)),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Promotions/Werewolf.dds',ColorTypes(8),iX,iY,True,True)
											newUnit = pPlayerW.initUnit(gc.getInfoTypeForString('UNIT_RAVENOUS_WEREWOLF'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.NO_DIRECTION)
											cf.makeMortal(pWinner)
											pWinner.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION'), True)
											newUnit.convert(pWinner)
											newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION'), False)
					if pWinner.isHasPromotion(iWerewolf):
						if pLoser.isAlive():
							if not iUnitCombatLoser in lBeasts:
								for iProm in lImmuneLycanthropy:
									if pLoser.isHasPromotion(iProm):
										break
								else:
									iChance = pWinner.getLevel() - pLoser.getLevel()
									sName = pLoser.getName()
									if iTypeWinner == gc.getInfoTypeForString('UNIT_DUIN'):
										iChance += 5
									elif iTypeWinner == gc.getInfoTypeForString('UNIT_GREATER_WEREWOLF'):
										iChance += 3
										if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CANNOT_CAST')):
											pWinner.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CANNOT_CAST'), False)
											CyInterface().addMessage(iPlayerW,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WEREWOLF_CAN_CAST",(sName,)),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Promotions/Werewolf.dds',ColorTypes(8),iX,iY,True,True)
									elif iTypeWinner == gc.getInfoTypeForString('UNIT_WEREWOLF'):
										iChance += 2
									elif iTypeWinner == gc.getInfoTypeForString('UNIT_RAVENOUS_WEREWOLF'):
										iChance += 1
									iChance *= 10
									if iChance > 0:
										if CyGame().getSorenRandNum(100, "Spread Lycanthropy " + pWinner.getName().encode('latin_1','replace') + ' slayer of '+ pLoser.getName().encode('latin_1','replace')) < iChance:
											sName = pLoser.getName()
											CyInterface().addMessage(iPlayerL,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SPREAD_LYCANTHROPY",(sName,)),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Promotions/Werewolf.dds',ColorTypes(7),iX,iY,True,True)
											CyInterface().addMessage(iPlayerW,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SPREAD_LYCANTHROPY",(sName,)),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Promotions/Werewolf.dds',ColorTypes(8),iX,iY,True,True)
											newUnit = pPlayerW.initUnit(gc.getInfoTypeForString('UNIT_RAVENOUS_WEREWOLF'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.NO_DIRECTION)
											newUnit.setScenarioCounter(iTypeLoser)
											newUnit.setLevel(pLoser.getLevel())
											newUnit.setExperience(pLoser.getExperience(), -1)
											newUnit.setName(sName)
											newUnit.setReligion(pLoser.getReligion())
											newUnit.setDamage(pLoser.getDamage()/2, pWinner.getOwner())
											newUnit.finishMoves()
											for iCount in xrange(gc.getNumPromotionInfos()):
												if pLoser.isHasPromotion(iCount) and not gc.getPromotionInfo(iCount).isEquipment():
													newUnit.setHasPromotion(iCount, True)
											cf.makeMortal(pLoser)
											pLoser.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION'), True)
				else:
					iNaval = gc.getInfoTypeForString('UNITCOMBAT_NAVAL')
					if iUnitCombatLoser == iNaval:
						if pWinner.isHiddenNationality() and pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BOARDING')):
							newUnit = pPlayerW.initUnit(iTypeLoser, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
							newUnit.finishMoves()
							newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)
							newUnit.setDamage(90, iPlayerW)
							newUnit.setLevel(pLoser.getLevel())
							newUnit.setExperience(pLoser.getExperience(), -1)
							newUnit.setName(pLoser.getNameNoDesc())
							newUnit.setReligion(pLoser.getReligion())
							for iCount in xrange(gc.getNumPromotionInfos()):
								if pLoser.isHasPromotion(iCount) and not gc.getPromotionInfo(iCount).isEquipment():
									newUnit.setHasPromotion(iCount, True)

						## Advanced Tactics Start - ships and siege engines can be captured
						## adopted from mechaerik War Prize ModComp
						elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS):
							if pWinner.getSummoner() == -1 and pWinner.getDuration() == 0:
								if pLoser.canMoveInto(pWinner.plot(), True, True, False):
	##								if unitX.getUnitCombatType() == iNaval:
									if unitY.getUnitCombatType() == iNaval:
										if CyGame().getSorenRandNum(100, "WarPrizes Naval" + pWinner.getName().encode('latin_1','replace') + ' slayer of '+ pLoser.getName().encode('latin_1','replace')) <= 25:
											newUnit = pPlayerW.initUnit(iTypeLoser, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
											newUnit.finishMoves()
											newUnit.setDamage(75, iPlayerW)
											if pPlayerW.isHuman():
												CyInterface().addMessage(iPlayerW,False,20,CyTranslator().getText("TXT_KEY_MISC_WARPRIZES_SUCCESS",(pLoser.getName(),)),'',0,gc.getUnitInfo(iTypeLoser).getButton(),ColorTypes(gc.getInfoTypeForString("COLOR_GREEN")), iX, iY, True,True)
											if pPlayerL.isHuman():
												CyInterface().addMessage(iPlayerL,False,20,CyTranslator().getText("TXT_KEY_MISC_WARPRIZES_FAILURE",(pLoser.getName(),)),'',0,gc.getUnitInfo(iTypeLoser).getButton(),ColorTypes(gc.getInfoTypeForString("COLOR_RED")), pLoser.getX(), pLoser.getY(), True,True)
				## End Advanced Tactics
				##



		if not self.__LOG_COMBAT:
			return
		if playerX and playerX and unitX and playerY:
			CvUtil.pyPrint('Player %d Civilization %s Unit %s has defeated Player %d Civilization %s Unit %s'
				%(playerX.getID(), playerX.getCivilizationName(), unitX.getDescription(),
				playerY.getID(), playerY.getCivilizationName(), unitY.getDescription()))

	def onCombatLogCalc(self, argsList):
		'Combat Result'
		genericArgs = argsList[0][0]
		cdAttacker = genericArgs[0]
		cdDefender = genericArgs[1]
		iCombatOdds = genericArgs[2]
		CvUtil.combatMessageBuilder(cdAttacker, cdDefender, iCombatOdds)

	def onCombatLogHit(self, argsList):
		'Combat Message'
		global gCombatMessages, gCombatLog
		genericArgs = argsList[0][0]
		cdAttacker = genericArgs[0]
		cdDefender = genericArgs[1]
		iIsAttacker = genericArgs[2]
		iDamage = genericArgs[3]

		if cdDefender.eOwner == cdDefender.eVisualOwner:
			szDefenderName = gc.getPlayer(cdDefender.eOwner).getNameKey()
		else:
			szDefenderName = localText.getText("TXT_KEY_TRAIT_PLAYER_UNKNOWN", ())
		if cdAttacker.eOwner == cdAttacker.eVisualOwner:
			szAttackerName = gc.getPlayer(cdAttacker.eOwner).getNameKey()
		else:
			szAttackerName = localText.getText("TXT_KEY_TRAIT_PLAYER_UNKNOWN", ())

		if (iIsAttacker == 0):
			combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_HIT", (szDefenderName, cdDefender.sUnitName, iDamage, cdDefender.iCurrHitPoints, cdDefender.iMaxHitPoints))
			CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
			CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
			if (cdDefender.iCurrHitPoints <= 0):
				combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_DEFEATED", (szAttackerName, cdAttacker.sUnitName, szDefenderName, cdDefender.sUnitName))
				CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
				CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
		elif (iIsAttacker == 1):
			combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_HIT", (szAttackerName, cdAttacker.sUnitName, iDamage, cdAttacker.iCurrHitPoints, cdAttacker.iMaxHitPoints))
			CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
			CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
			if (cdAttacker.iCurrHitPoints <= 0):
				combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_DEFEATED", (szDefenderName, cdDefender.sUnitName, szAttackerName, cdAttacker.sUnitName))
				CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
				CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)

	def onImprovementBuilt(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Improvement Built'
		iImprovement, iX, iY = argsList
		if iImprovement != -1:
			pPlot = CyMap().plot(iX, iY)
			if not pPlot.isCity():
				info = gc.getImprovementInfo(iImprovement)
				iBonus = info.getBonusConvert()
				if iBonus != -1:
					pPlot.setBonusType(iBonus)

				iRel = -1
				iCiv = -1
				if pPlot.isOwned():
					if not pPlot.isBarbarian():
						pPlayer = gc.getPlayer(pPlot.getOwner())
						iRel = pPlayer.getStateReligion()
						iCiv = pPlayer.getCivilizationType()

				if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_GRAVE'):
					pPlot.setFeatureType(-1,-1)
				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_SCALED'):
					pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_OASIS'),-1)
				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_SHIMMERING'):
					pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_HALLOWED_GROUND'),-1)
					pPlot.changePlotCounter(-100)
				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_SHIELD'):
					pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_HALLOWED_GROUND'),-1)
					pPlot.changePlotCounter(-100)
				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_PIT'):
					pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_TORMENTED_SOULS'),-1)
					pPlot.changePlotCounter(100)
				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_SIEGE'):
					pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_TORMENTED_SOULS'),-1)
				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_DRACOLICH'):
					pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_TORMENTED_SOULS'),-1)
				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_SEED'):
					pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT'),-1)
				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_FURNACE'):
					pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FLAMES'),-1)

				if info.isUnique():

					if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WHISPERING_WOOD'):
						pPlot.setMoveDisabledAI(True)

					# elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BADBS_BLIZZARD'):
						# iBadb = gc.getInfoTypeForString('UNIT_BADB')
						# if CyGame().getUnitCreatedCount(iBadb) == 0:
							# newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(iBadb, iX, iY, UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_SOUTH)
							# newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAIR_GUARDIAN'), True)
							# newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SLOW'), True)

					elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS'):
						bFoundDisabled = not CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_WHITE_HAND'))

						iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
						iGrass = gc.getInfoTypeForString('TERRAIN_GRASS')
						iMarsh = gc.getInfoTypeForString('TERRAIN_MARSH')
						iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
						iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
						iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
						iGlacier = gc.getInfoTypeForString('TERRAIN_GLACIER')
						iWaste = gc.getInfoTypeForString('TERRAIN_WASTELAND')
						iBlizzard = gc.getInfoTypeForString('FEATURE_BLIZZARD')
						iIce = gc.getInfoTypeForString('FEATURE_ICE')
						iForest = gc.getInfoTypeForString('FEATURE_FOREST')

						pPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
						pPlot.setTerrainType(iGlacier, True, True)
						iSnowRange = 3
						for iiX in xrange(iX-iSnowRange, iX+1+iSnowRange, 1):
							for iiY in xrange(iY-iSnowRange, iY+1+iSnowRange, 1):
								pLoopPlot = CyMap().plot(iiX,iiY)
								if pLoopPlot.isNone():continue
								if pLoopPlot.isWater():continue
								iTerrain = pLoopPlot.getTerrainType()
								if iTerrain in [iGrass, iPlains]:#, iMarsh]:
									pLoopPlot.setTerrainType(iTundra, True, True)
								elif iTerrain == iDesert:
									pLoopPlot.setTerrainType(iPlains, True, True)
								if pLoopPlot.getFeatureType() == iForest:
									pLoopPlot.setFeatureType(iForest, 2)#Snowy Conifer Forest


						iSnowRange = 2
						for iiX in xrange(iX-iSnowRange, iX+1+iSnowRange, 1):
							for iiY in xrange(iY-iSnowRange, iY+1+iSnowRange, 1):
								pLoopPlot = CyMap().plot(iiX,iiY)
								if pLoopPlot.isNone():continue
								if pLoopPlot.isWater():continue
								if bFoundDisabled:
									pLoopPlot.setFoundDisabled(True)
								if pLoopPlot.getTerrainType() in [iPlains, iMarsh]:
									pLoopPlot.setTerrainType(iTundra, True, True)
								elif iTerrain == iTundra:
									pLoopPlot.setTerrainType(iSnow, True, True)
								elif iTerrain == iWaste:
									pLoopPlot.setTerrainType(iGlacier, True, True)

						iSnowRange = 1
						for iiX in xrange(iX-iSnowRange, iX+1+iSnowRange, 1):
							for iiY in xrange(iY-iSnowRange, iY+1+iSnowRange, 1):
								pLoopPlot = CyMap().plot(iiX,iiY)
								if pLoopPlot.isNone():continue
								if pLoopPlot.isWater():continue
##									if pLoopPlot.getFeatureType() == -1:
##										pPlot.setFeatureType(iIce, 1)
##									continue
								iTerrain = pLoopPlot.getTerrainType()
								if iTerrain in [iGlacier, iSnow]:
									if pLoopPlot.getFeatureType() == -1:
										pPlot.setFeatureType(iBlizzard, 1)
								elif iTerrain == iTundra:
									pLoopPlot.setTerrainType(iSnow, True, True)
								elif iTerrain == iWaste:
									pLoopPlot.setTerrainType(iGlacier, True, True)

						pPlot.setBonusType(gc.getInfoTypeForString('BONUS_MANA_ICE'))


					elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_POOL_OF_TEARS'):
						pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_OASIS'),-1)

					elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_CARCER'):
						pPlot.setRouteType(gc.getInfoTypeForString('ROUTE_ROAD'))
						pPlot.setMinLevel(9)

					elif iImprovement in [gc.getInfoTypeForString('IMPROVEMENT_YGGDRASIL'), gc.getInfoTypeForString('IMPROVEMENT_HERVES_MAUSOLEUM')]:
						pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT'), 1)

					elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_MAJENS_WORKSHOP'):
						pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FOREST_NEW'), 1)

					elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_CLOCKWORK_CITY'):
						pPlot.setRouteType(gc.getInfoTypeForString('ROUTE_RAILROAD'))

					elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES'):
						pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'), True, True)
						pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FOREST'), 1)
						# newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(gc.getInfoTypeForString('EQUIPMENT_MASK_KYLORIN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					# elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_TAPESTRY_HOUSE'):
						# newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(gc.getInfoTypeForString('EQUIPMENT_MASK_GABELLA'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					# elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_GRAVE_OF_ASMODAY'):
						# newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(gc.getInfoTypeForString('EQUIPMENT_MASK_ASMODAY'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					# elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER'):
						# newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(gc.getInfoTypeForString('EQUIPMENT_MASK_BARBATOS'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					# elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_REMNANTS_OF_PATRIA'):
						# newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(gc.getInfoTypeForString('EQUIPMENT_MASK_ALEXIS'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)


				elif info.isActsAsCity():
					if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS):

						if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_CITADEL'):
							if iRel == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
								iImprovement = gc.getInfoTypeForString('IMPROVEMENT_CITADEL_OF_LIGHT')
								pPlot.setImprovementType(iImprovement)

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_CITADEL_OF_LIGHT'):
							if iRel != gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
								iImprovement = gc.getInfoTypeForString('IMPROVEMENT_CITADEL')
								pPlot.setImprovementType(iImprovement)

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE'):
							pPlot.changePlotCounter(100)
							if iRel != gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
								if iCiv not in [gc.getInfoTypeForString('CIVILIZATION_INFERNAL'),gc.getBARBARIAN_PLAYER()]:
									pPlot.setOwner(gc.getBARBARIAN_PLAYER())



						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_PIRATE_PORT'):
							if iCiv not in [gc.getInfoTypeForString('CIVILIZATION_LANUN'),gc.getBARBARIAN_PLAYER()]:
								pPlot.setOwner(gc.getBARBARIAN_PLAYER())

							if pPlot.isOwned():
								pPlayer = gc.getPlayer(pPlot.getOwner())
								if not pPlayer.isHasTech(gc.getInfoTypeForString('TECH_OPTICS')):
									pPlot.setImprovementType( gc.getInfoTypeForString('IMPROVEMENT_PIRATE_HARBOR'))

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_PIRATE_HARBOR'):
							if iCiv not in [gc.getInfoTypeForString('CIVILIZATION_LANUN'),gc.getBARBARIAN_PLAYER()]:
								pPlot.setOwner(gc.getBARBARIAN_PLAYER())

							if pPlot.isOwned():
								pPlayer = gc.getPlayer(pPlot.getOwner())
								if not pPlayer.isHasTech(gc.getInfoTypeForString('TECH_SAILING')):
									pPlot.setImprovementType( gc.getInfoTypeForString('IMPROVEMENT_PIRATE_COVE'))

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_PIRATE_COVE'):
							if iCiv not in [gc.getInfoTypeForString('CIVILIZATION_LANUN'),gc.getBARBARIAN_PLAYER()]:
								pPlot.setOwner(gc.getBARBARIAN_PLAYER())


				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_LUMBERMILL'):
					iForest = gc.getInfoTypeForString('FEATURE_FOREST')
					if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT'):
						if CyGame().getSorenRandNum(100, "Treant Spawn Chance") < gc.getDefineINT('TREANT_SPAWN_CHANCE')/2:
							newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(gc.getInfoTypeForString('UNIT_TREANT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							newUnit.setDuration(2)
							newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)
							lVarieties = []
							for iDirection in xrange(DirectionTypes.NUM_DIRECTION_TYPES):
								pPlot2 = plotDirection(iX, iY, DirectionTypes(iDirection))
								if not pPlot2.isNone():
									if pPlot2.getFeatureType() == iForest:
										lVarieties.append(pPlot2.getFeatureVariety())
							if len(lVarieties) > 0:
								iVariety = lVarieties.pop(CyGame().getSorenRandNum(len(lVarieties), "Choose Forest Variety based on adjacent"))
							elif pPlot.getTerrainType() in [gc.getInfoTypeForString('TERRAIN_SNOW'),gc.getInfoTypeForString('TERRAIN_TUNDRA')]:
								iVariety = 2
							else:
								iVariety = CyGame().getSorenRandNum(2, "Choose Forest Variety")
							pPlot.setFeatureType(iForest, iVariety)

							pPlot.setRealFeatureType(gc.getInfoTypeForString('FEATURE_FOREST'))
							pPlot.setRealFeatureVariety(iVariety)
							pPlot.changeTempFeatureTimer(CyGame().getSorenRandNum(30, "Lumbermill Depletion") )

				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_HOMESTEAD'):
					if iCiv != gc.getInfoTypeForString('CIVILIZATION_GRIGORI'):
						iImprovement = gc.getInfoTypeForString('IMPROVEMENT_FARM')
						pPlot.setImprovementType(iImprovement)
				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_GRAVEYARD'):
					gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(gc.getInfoTypeForString('UNIT_SLUAGH'), iX, iY, UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_SOUTH)

				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES'):
					iDragon = gc.getInfoTypeForString('PROMOTION_DRAGON')
					iSluagh = gc.getInfoTypeForString('UNIT_SLUAGH')
					iBonus = pPlot.getBonusType(-1)
					if iBonus == -1 or not gc.getBonusInfo(iBonus).isMana():
						for i in xrange(pPlot.getNumUnits()):
							pUnit = pPlot.getUnit(i)
							if pUnit.getUnitType() == iSluagh:
								if pUnit.isHasPromotion(iDragon):
									iUnit = pUnit.getScenarioCounter()
									if -1 < iUnit < gc.getNumUnitInfos():
										infoUnit = gc.getUnitInfo(iUnit)
										iBonus = infoUnit.getPrereqAndBonus()
										pPlot.setBonusType(iBonus)
										break
						else:
							if not CyGame().getWBMapScript():
								listMana = []
								for iLoopBonus in xrange(gc.getNumBonusInfos()):
									if gc.getBonusInfo(iLoopBonus).isMana():
										listMana.append(iLoopBonus)
								if len(listMana) > 0:
									iBonus = listMana.pop(CyGame().getSorenRandNum(len(listMana), "Dragon Bones pick random mana"))
									pPlot.setBonusType(iBonus)
									iDragon = gc.getInfoTypeForString('SPECIALUNIT_DRAGON')
									listDragons = []
									for iUnit in xrange(gc.getNumUnitInfos()):
										infoUnit = gc.getUnitInfo(iUnit)
										if infoUnit.getSpecialUnitType() == iDragon:
											if iBonus == infoUnit.getPrereqAndBonus():
												if not isWorldUnitClass(infoUnit.getUnitClassType()):
													listDragons.append(iUnit)
									if len(listDragons) > 0:
										iDragon = listDragons[CyGame().getSorenRandNum(len(listDragons), "Dragon Bones species")]
										newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(gc.getInfoTypeForString('UNIT_SLUAGH'), iX, iY, UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_SOUTH)
										newUnit.setScenarioCounter(iDragon)
										infoUnit = gc.getUnitInfo(iDragon)
										sUnitName =infoUnit.getDescription()
										newUnit.setName(sUnitName + "'s Sluagh")
										for iProm in xrange(gc.getNumPromotionInfos()):
											if infoUnit.getFreePromotions(iProm):
												newUnit.setHasPromotion(iProm, True)

				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_CITY_RUINS'):
					if pPlot.getBonusType(-1) == gc.getInfoTypeForString('BONUS_MANA_ICE'):
						if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_WHITE_HAND')) > 0:
							if CyGame().getHolyCity(gc.getInfoTypeForString('RELIGION_WHITE_HAND')).isNone():
								iLetum = gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS')
								pLetum = cf.findImprovement(iLetum)
								if pLetum == -1:
									if not pPlot.isCity():
										pPlot.setImprovementType(iLetum)
##
##				elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_WARDING'):
##					pPlot.changeTempImprovementTimer(2)


		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Improvement %s was built at %d, %d'
			%(PyInfo.ImprovementInfo(iImprovement).getDescription(), iX, iY))

	def onImprovementDestroyed(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Improvement Destroyed'
		iImprovement, iOwner, iX, iY = argsList
		pPlot = CyMap().plot(iX, iY)

		iRealImprovement = pPlot.getRealImprovementType()

		iTimerFeature = pPlot.getTempFeatureTimer()
		iRealFeature = pPlot.getRealFeatureType()
		iRealFeatureVariety = pPlot.getRealFeatureVariety()

		if iImprovement != -1:

			if gc.getImprovementInfo(iImprovement).isUnique():
				CyEngine().removeLandmark(pPlot)

			if iImprovement in [gc.getInfoTypeForString('IMPROVEMENT_BARROW'), gc.getInfoTypeForString('IMPROVEMENT_GRAVEYARD')]:
				if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_HALLOWED_GROUND'):
					if iRealFeature == gc.getInfoTypeForString('FEATURE_HALLOWED_GROUND'):
						iRealFeature = -1
						iRealFeatureVariety = -1
					pPlot.setFeatureType(iRealFeature,iRealFeatureVariety)

			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_MAELSTROM'):
				pPlot.setMoveDisabledAI(False)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_NECROTOTEM'):
				CyGame().changeGlobalCounter(-2)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_WARDING'):
				pPlot.setMinLevel(0)
				if iRealImprovement != iImprovement:
					pPlot.setImprovementType(iRealImprovement)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_CARCER'):
				pPlot.setMinLevel(0)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WHISPERING_WOOD'):
				pPlot.setMoveDisabledAI(False)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS'):
				iSnowRange = 3
				for iiX in xrange(iX-iSnowRange, iX+1+iSnowRange, 1):
					for iiY in xrange(iY-iSnowRange, iY+1+iSnowRange, 1):
						pLoopPlot = CyMap().plot(iiX,iiY)
						pLoopPlot.setFoundDisabled(False)


			if CyGame().getWBMapScript():
				sf.onImprovementDestroyed(iImprovement, iOwner, iX, iY)

		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Improvement %s was Destroyed at %d, %d'
			%(PyInfo.ImprovementInfo(iImprovement).getDescription(), iX, iY))

	def onRouteBuilt(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Route Built'
		iRoute, iX, iY = argsList

		pPlot = CyMap().plot(iX, iY)
		# if iRoute == gc.getInfoTypeForString('ROUTE_RAILROAD'):
			# if pPlot.isPeak():
				# pPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)

		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Route %s was built at %d, %d'
			%(gc.getRouteInfo(iRoute).getDescription(), iX, iY))

	def onPlotRevealed(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Plot Revealed'
		pPlot = argsList[0]
		iTeam = argsList[1]

	def onPlotFeatureRemoved(self, argsList):
		'Plot Revealed'
		pPlot = argsList[0]
		iFeatureType = argsList[1]
		pCity = argsList[2] # This can be null
		##Does not seem to work with AutoRaze
		# if iFeatureType == gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT'):
			# iForest = gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT')
			# iTerrain = pPlot.getTerrainType()
		# ##	DECIDUOUS_FOREST = 0
		# ##	CONIFEROUS_FOREST = 1
		# ##	SNOWY_CONIFEROUS_FOREST = 2
			# iVariety = 0
			# lVarieties = []
			# iX = pPlot.getX()
			# iY = pPlot.getY()
			# if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
				# iVariety = 2
			# else:
				# for iDirection in xrange(DirectionTypes.NUM_DIRECTION_TYPES):
					# pPlot2 = plotDirection(iX, iY, DirectionTypes(iDirection))
					# if not pPlot2.isNone():
						# if pPlot2.getFeatureType() == iForest:
							# lVarieties.append(pPlot2.getFeatureVariety())
				# if len(lVarieties) > 0:
					# iVariety = lVarieties.pop(CyGame().getSorenRandNum(len(lVarieties), "Choose Forest Variety based on adjacent"))
				# elif iTerrain in [gc.getInfoTypeForString('TERRAIN_SNOW'),gc.getInfoTypeForString('TERRAIN_TUNDRA')]:
					# iVariety = 2
				# else:
					# iVariety = CyGame().getSorenRandNum(2, "Choose Forest Variety")
			# pPlot.setFeatureType(iForest, iVariety)

	def onPlotPicked(self, argsList):
		'Plot Picked'
		pPlot = argsList[0]
		CvUtil.pyPrint('Plot was picked at %d, %d'
			%(pPlot.getX(), pPlot.getY()))

	def onNukeExplosion(self, argsList):
		'Nuke Explosion'
		pPlot, pNukeUnit = argsList
		CvUtil.pyPrint('Nuke detonated at %d, %d'
			%(pPlot.getX(), pPlot.getY()))

	def onGotoPlotSet(self, argsList):
		'Nuke Explosion'
		pPlot, iPlayer = argsList

	def onBuildingBuilt(self, argsList):
		'Building Completed'
		pCity, iBuildingType = argsList
		player = pCity.getOwner()
		pPlayer = gc.getPlayer(player)
		iTeam = pPlayer.getTeam()
		eTeam = gc.getTeam(iTeam)
		pPlot = pCity.plot()
		iX = pCity.getX()
		iY = pCity.getY()
		game = gc.getGame()
		infoBuilding = gc.getBuildingInfo(iBuildingType)
		iBuildingClass = infoBuilding.getBuildingClassType()
		iStateReligion = pPlayer.getStateReligion()

		iAlignment = pPlayer.getAlignment()
		iLeader = pPlayer.getLeaderType()
		

		if not gc.getGame().isNetworkMultiPlayer() and (pCity.getOwner() == gc.getGame().getActivePlayer()) and isWorldWonderClass(iBuildingClass):
	## Platy Builder ##
			if not CyGame().GetWorldBuilderMode():
	## Platy Builder ##
				if gc.getBuildingInfo(iBuildingType).getMovie():
					# If this is a wonder...
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setData1(iBuildingType)
					popupInfo.setData2(pCity.getID())
					popupInfo.setData3(0)
					popupInfo.setText(u"showWonderMovie")
					popupInfo.addPopup(pCity.getOwner())


		listAltars =[	gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR'),
						gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_ANOINTED'),
						gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_BLESSED'),
						gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_CONSECRATED'),
						gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_DIVINE'),
						gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_EXALTED'),
						gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_FINAL')
						]
		if iBuildingType in listAltars:
			for iAltar in listAltars[:listAltars.index(iBuildingType)]:
				pCity.setNumRealBuilding(iAltar, False)

		elif iBuildingType == gc.getInfoTypeForString('BUILDING_HOSPITALITY'):
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')) or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_SACRIFICE_THE_WEAK')):
				pCity.setNumRealBuilding(iBuildingType, False)

		elif iBuildingType == gc.getInfoTypeForString('BUILDING_CELESTIAL_COMPASS'):
			cf.showUniqueImprovements(pCity.getOwner())

		elif iBuildingType == gc.getInfoTypeForString('BUILDING_SANGUINE_FOUNTAIN'):
			iDiscord = gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD')
			pSanguine = CyGame().getHolyCity(iDiscord)
			if pSanguine != -1:
				if pSanguine != pCity:
					pSanguine.setNumRealBuilding(iBuildingType, False)
					CyGame().clearHolyCity(iDiscord)
			for iPlayerLoop in xrange(gc.getMAX_PLAYERS()):
				pPlayerLoop = gc.getPlayer(iPlayerLoop)
				if pPlayerLoop.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SANGUINE_FOUNTAIN')) > 0:
					for pyCity in PyPlayer(iPlayerLoop).getCityList():
						loopCity = pyCity.GetCy()
						loopCity.setNumRealBuilding(iBuildingType, 0)

			CyGame().setHolyCity(iDiscord, pCity, False)
			pCity.setNumRealBuilding(iBuildingType, True)


		elif iBuildingType == gc.getInfoTypeForString('BUILDING_TOWER_OF_MASTERY'):
			iMastery = gc.getInfoTypeForString('PROMOTION_MASTERY')
			iAdept = gc.getInfoTypeForString('UNITCOMBAT_ADEPT')
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if iTeam == pUnit.getTeam():
					if pUnit.getUnitCombatType() == iAdept:
						pUnit.setHasPromotion(iMastery, True)

		elif iBuildingType == gc.getInfoTypeForString('BUILDING_CRUCIBLE'):
			CyEngine().addLandmark(pPlot, CvUtil.convertToStr(gc.getBuildingInfo(iBuildingType).getDescription()))
			CyCamera().JustLookAtPlot(pPlot)
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isHuman():
					if pLoopPlayer.isAlive():
						pPlot.setRevealed(pLoopPlayer.getTeam(), True, False, TeamTypes.NO_TEAM)
						CyInterface().addMessage(iLoopPlayer, True, 25, CyTranslator().getText("TXT_KEY_BUILDING_CRUCIBLE_PEDIA", ()), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, 'Art/Interface/Buttons/Projects/Glory_Everlasting.dds', gc.getInfoTypeForString('COLOR_RED'), pCity.getX(), pCity.getY(), True, True)

		elif iBuildingType == gc.getInfoTypeForString('BUILDING_GRAND_MENAGERIE'):
			if pPlayer.isHuman():
				if not CyGame().getWBMapScript():
					t = "TROPHY_FEAT_GRAND_MENAGERIE"
					if not CyGame().isHasTrophy(t):
						CyGame().changeTrophyValue(t, 1)

		elif iBuildingType == gc.getInfoTypeForString('BUILDING_INFERNAL_GRIMOIRE'):
			if CyGame().getSorenRandNum(100, "Infernal Grimoire") < 66:
				pPlot.changePlotCounter(60)
				pPlot2 = cf.findClearPlotImprovement(pPlot)
				if pPlot2 != -1:
					pPlot2.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE'))
					if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS):
						pPlot2.setOwner(gc.getBARBARIAN_PLAYER())
					bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

					iBound = gc.getInfoTypeForString('PROMOTION_BOUND_BY_COMPACT')
					iHN = gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY')
					iR = gc.getInfoTypeForString('PROMOTION_REBEL')

					for iUnit in [gc.getInfoTypeForString('UNIT_BEAST_OF_AGARES'),gc.getInfoTypeForString('UNIT_BALOR'),gc.getInfoTypeForString('UNIT_EIDOLON'),gc.getInfoTypeForString('UNIT_IMP')]:
						newUnit = bPlayer.initUnit(iUnit, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
						newUnit.setHasPromotion(iBound, True)
						newUnit.setHasPromotion(iHN, True)
						newUnit.setHasPromotion(iR, True)
						if newUnit.canMoveOrAttackInto(pPlot, False):
							newUnit.attack(pPlot, False)

					CyInterface().addMessage(pCity.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_INFERNAL_GRIMOIRE_BALOR",()),'AS2D_BALOR',1,'Art/Interface/Buttons/Units/Balor.dds',ColorTypes(7),newUnit.getX(),newUnit.getY(),True,True)
					if pCity.getOwner() == CyGame().getActivePlayer():
						cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_INFERNAL_GRIMOIRE_BALOR",()), 'art/interface/popups/Balor.dds')

		elif iBuildingType == gc.getInfoTypeForString('BUILDING_EYES_AND_EARS_NETWORK'):
			iPlayer = pCity.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			iTeam = pPlayer.getTeam()
			eTeam = gc.getTeam(iTeam)
			iSidar = gc.getInfoTypeForString('CIVILIZATION_SIDAR')
			for jPlayer in xrange(gc.getMAX_PLAYERS()):
				if iPlayer == jPlayer:continue
				pPlayer2 = gc.getPlayer(jPlayer)
				if pPlayer2.isAlive():
					if pPlayer2.isBarbarian():continue
					if pPlayer2.getCivilizationType() == iSidar:continue
					iTeam2 = pPlayer2.getTeam()
					eTeam2 = gc.getTeam(iTeam2)
					if eTeam2.isAlive():
						if eTeam.isHasMet(iTeam2):
							eTeam.changeStolenVisibilityTimer(iTeam2, 2)

		elif iBuildingType == gc.getInfoTypeForString('BUILDING_PLANAR_GATE'):
			if pCity.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')) < 1:
				pCity.setNumRealBuilding(iBuildingType, 0)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED'), 1)

		elif iBuildingType in [gc.getInfoTypeForString('BUILDING_NEW_MULYR'), gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND')]:
			bAuricAlive = False
			iSnowRange = 0
			iSnowOdds = 0
			if iBuildingType == gc.getInfoTypeForString('BUILDING_NEW_MULYR'):
				bAuricAlive = True
				iSnowRange += 2
				iSnowOdds += 2

			iAuricLeader = gc.getInfoTypeForString('LEADER_AURIC')
			iAuricPlayer = cf.getLeader(iAuricLeader)
			if iAuricPlayer != -1:
				pAuricPlayer = gc.getPlayer(iAuricPlayer)
				if pAuricPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AURIC')) > 0:
					bAuricAlive = True
					if eTeam.isAtWar(pAuricPlayer.getTeam()):
						if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
							if CyGame().getSorenRandNum(100, "Auric Revolt in " + pCity.getName().encode('latin_1','replace')) < 15:
								pCity.changeOccupationTimer(3)
								pCity.changeHurryAngerTimer(1)
								CyInterface().addMessage(player,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_AURIC_REVOLT", ()),'',1,'Art/Interface/Buttons/Units/Auric Ascended.dds',ColorTypes(7),iX,iY,True,True)
			if bAuricAlive:
				if iStateReligion == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
					iSnowRange += 1
				for sRitual in [	'PROJECT_SAMHAIN',
									'PROJECT_THE_WHITE_HAND',
									'PROJECT_THE_DEEPENING',
									'PROJECT_THE_DRAW',
									'PROJECT_ASCENSION'
									]:
					if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString(sRitual)) > 0:
						iSnowRange += 1
				if iSnowRange > 0:
					iSnowOdds += iSnowRange//2
					iSnowOdds += max(0,cf.getNumBonusEffective(player, gc.getInfoTypeForString('BONUS_MANA_ICE'), -1) + pCity.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_ICE')))
					iSnowOdds -= max(0,cf.getNumBonusEffective(player, gc.getInfoTypeForString('BONUS_MANA_FIRE'), -1) + pCity.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_FIRE')))
					iSnowOdds -= max(0,cf.getNumBonusEffective(player, gc.getInfoTypeForString('BONUS_MANA_NATURE'), -1) + pCity.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_NATURE')))
					if iSnowOdds > 1:#There is no use wasting resources when nothing would get done
						iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
						iGlacier = gc.getInfoTypeForString('TERRAIN_GLACIER')
						iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
						iForest = gc.getInfoTypeForString('FEATURE_FOREST')
						iJungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
						lClearFeatures = [	gc.getInfoTypeForString('FEATURE_FLAMES'),
											gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'),
											gc.getInfoTypeForString('FEATURE_SCRUB'),
											gc.getInfoTypeForString('FEATURE_OBSIDIAN_PLAINS')
											]
						for iiX in xrange(iX-iSnowRange, iX+1+iSnowRange, 1):
							for iiY in xrange(iY-iSnowRange, iY+1+iSnowRange, 1):
								pLoopPlot = CyMap().plot(iiX,iiY)
								if pLoopPlot.isNone():continue
								if pLoopPlot.isWater():continue
								if not pLoopPlot.isWithinCultureRange(player):continue
								if pLoopPlot.getImprovementType() == iSmoke:
									pLoopPlot.setImprovementType(-1)
								iDistance = CyMap().calculatePathDistance(pLoopPlot, pPlot)
								if iSnowOdds > iDistance > -1:
									iTimer = CyGame().getSorenRandNum(iSnowOdds - iDistance, "Snowfall - Founding New Mulyr/Temple of the Hand in " + pCity.getName().encode('latin_1','replace'))
									if iTimer > 1:
										if pLoopPlot.getTerrainType() in [iSnow, iGlacier]:
											if pLoopPlot.isHasTempTerrain():
												if pLoopPlot.getTempTerrainTimer() < iTimer:
													pLoopPlot.changeTempTerrainTimer(iTimer - pLoopPlot.getTempTerrainTimer())
										else:
											iTimer += 1
											if pLoopPlot.getPlotCounter() < 50:
												pLoopPlot.setTempTerrainType(iSnow, iTimer)
											else:
												pLoopPlot.setTempTerrainType(iGlacier, iTimer)
										iFeature = pLoopPlot.getFeatureType()
										if iFeature == -1:
											if pLoopPlot.isHasTempFeature():
												if pLoopPlot.getRealFeatureType() in lClearFeatures:
													if pLoopPlot.getTempFeatureTimer() < iTimer:
														pLoopPlot.changeTempFeatureTimer(iTimer - pLoopPlot.getTempFeatureTimer())
										elif iFeature == iForest:
											if pLoopPlot.getFeatureVariety() == 2:
												if pLoopPlot.isHasTempFeature():
													if pLoopPlot.getTempFeatureTimer() < iTimer:
														pLoopPlot.changeTempFeatureTimer(iTimer - pLoopPlot.getTempFeatureTimer())
											else:
												pLoopPlot.setTempFeatureType(iForest, 2, iTimer)
										elif iFeature == iJungle:
											pLoopPlot.setTempFeatureType(iForest, 2, iTimer)
										elif iFeature in lClearFeatures:
											pLoopPlot.setTempFeatureType(-1, -1, iTimer)

		iShrine = infoBuilding.getGlobalReligionCommerce()
		if iShrine != -1:
			CyGame().setHolyCity(iShrine, pCity, False)
		
		if infoBuilding.getSpecialBuildingType() == gc.getInfoTypeForString('SPECIALBUILDING_TEMPLE'):

			infoBuilding = gc.getBuildingInfo(iBuildingType)
			iBuildingClass = infoBuilding.getBuildingClassType()
			iStateReligion = pPlayer.getStateReligion()

			iAlignment = pPlayer.getAlignment()
			iLeader = pPlayer.getLeaderType()
			iGood = gc.getInfoTypeForString('ALIGNMENT_GOOD')
			iEvil = gc.getInfoTypeForString('ALIGNMENT_EVIL')
			if iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_EMPYREAN'):
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN') or pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')) or iAlignment == iGood
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN'), bFriendly)
				
			elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_BROTHERHOOD'):
				if pCity.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD_HOSTILE'), False)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD'), False)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BLIND_BROTHERHOOD'), True)
				else:
					bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS') or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_PACIFISM')) or iAlignment == iGood
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD_HOSTILE'), not bFriendly)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD'), bFriendly)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BLIND_BROTHERHOOD'), False)
				
			elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_ARTIFICERY'):
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RINGGIVER') or iAlignment == iGood or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_ARETE'))
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARTIFICERY_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARTIFICERY'), bFriendly)

			elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_ORDER'):
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ORDER') or iAlignment == iGood
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER'), bFriendly)

			elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_UNBLEMISHED'):
				bFriendly = pPlayer.getStateReligion() in [gc.getInfoTypeForString('RELIGION_UNBLEMISHED'),gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')] or iAlignment == iGood
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED'), bFriendly)
				
			elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_KILMORPH'):
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH') or (iAlignment != iEvil and pPlayer.getStateReligion() != gc.getInfoTypeForString('RELIGION_FOXMEN'))
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH'), bFriendly)

			elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_OVERLORDS'):
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS') or iAlignment != iGood
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS'), bFriendly)

			elif iBuildingClass ==  gc.getInfoTypeForString('BUILDINGCLASS_GAMBLING_HOUSE'):
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY') or iAlignment != iGood
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE'), bFriendly)

			elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_ANOINTED'):
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_ANOINTED') or iAlignment == iEvil
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED'), bFriendly)
				
			elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_VEIL'):
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL') or iAlignment == iEvil
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL'), bFriendly)
				
			elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_TOPHET'):
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_EMBER_LEGION') or iAlignment == iEvil
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TOPHET_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TOPHET'), bFriendly)
				
			elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_INTERSTICE'):
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COVEN') or  (iAlignment == iEvil and pCity.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_CALABIM'))
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_INTERSTICE_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_INTERSTICE'), bFriendly)

			elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_HAND'):
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_WHITE_HAND')
				if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
					iAuricPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
					if iAuricPlayer != -1:
						pAuricPlayer = gc.getPlayer(iAuricPlayer)
						if pAuricPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AURIC')) > 0:
							iTeam = pPlayer.getTeam()
							eTeam = gc.getTeam(iTeam)
							iAuricTeam = pAuricPlayer.getTeam()
							if iAuricTeam == iTeam:
								bFriendly = True
							elif eTeam.isVassal(iTeam):
								bFriendly = True
							elif eTeam.isAtWar(iAuricTeam):
								bFriendly = False
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND'), bFriendly)

			elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_APHOTIC_THRONE'):
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS') or pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')) or iAlignment == iEvil
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE'), bFriendly)



		CvAdvisorUtils.buildingBuiltFeats(pCity, iBuildingType)

		if (not self.__LOG_BUILDING):
			return
		CvUtil.pyPrint('%s was finished by Player %d Civilization %s'
			%(PyInfo.BuildingInfo(iBuildingType).getDescription(), pCity.getOwner(), gc.getPlayer(pCity.getOwner()).getCivilizationDescription(0)))

	def onProjectBuilt(self, argsList):
		'Project Completed'
		pCity, iProjectType = argsList
		game = gc.getGame()
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		if not gc.getGame().isNetworkMultiPlayer() and pCity.getOwner() == gc.getGame().getActivePlayer():
	## Platy Builder ##
			if not CyGame().GetWorldBuilderMode():
	## Platy Builder ##
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(iProjectType)
				popupInfo.setData2(pCity.getID())
				popupInfo.setData3(2)
				popupInfo.setText(u"showWonderMovie")
				popupInfo.addPopup(iPlayer)

		iTeam = pPlayer.getTeam()
		eTeam = gc.getTeam(iTeam)
		iIllians = gc.getInfoTypeForString('CIVILIZATION_ILLIANS')
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')

		iBarbPlayer = gc.getBARBARIAN_PLAYER()
		bPlayer = gc.getPlayer(iBarbPlayer)

		if iProjectType == gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'):
			pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))
			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_INFERNAL_PACT')
			triggerData = pPlayer.initTriggeredData(iEvent, True, pCity.getID(), pCity.getX(), pCity.getY(), iPlayer, -1, -1, -1, -1, -1)

		elif iProjectType == gc.getInfoTypeForString('PROJECT_MANIFEST_TRISTAN'):
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_TRISTAN'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_NORTH)
			iDuration = cf.getNumBonusEffective(iPlayer, gc.getInfoTypeForString('BONUS_MANA_SPIRIT'), newUnit)
			newUnit.setDuration(iDuration)

		elif iProjectType == gc.getInfoTypeForString('PROJECT_RITES_OF_OGHMA'):
			i = 7
			iSize = CyMap().getWorldSize()
			if iSize == gc.getInfoTypeForString('WORLDSIZE_DUEL'):
				i -= 3
			elif iSize == gc.getInfoTypeForString('WORLDSIZE_TINY'):
				i =- 2
			elif iSize == gc.getInfoTypeForString('WORLDSIZE_SMALL'):
				i -= 1
			elif iSize == gc.getInfoTypeForString('WORLDSIZE_LARGE'):
				i += 1
			elif iSize == gc.getInfoTypeForString('WORLDSIZE_HUGE'):
				i += 3
			cf.addBonus('BONUS_MANA',i,'Art/Interface/Buttons/WorldBuilder/mana_button.dds')
			cf.addBonusWithinBorders('BONUS_MANA',i/4,'Art/Interface/Buttons/WorldBuilder/mana_button.dds',iPlayer)


		elif iProjectType == gc.getInfoTypeForString('PROJECT_PURGE_THE_UNFAITHFUL'):
			StateBelief = pPlayer.getStateReligion()
			for pyCity in PyPlayer(iPlayer).getCityList():
				loopCity = pyCity.GetCy()
				iRnd = CyGame().getSorenRandNum(2, "Purge of the Unfaithful in " + loopCity.getName().encode('latin_1','replace'))
				if StateBelief == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
					iRnd -= 1
				for iTarget in xrange(gc.getNumReligionInfos()):
					if StateBelief != iTarget and loopCity.isHasReligion(iTarget):
						if cf.removeReligion(iTarget, loopCity):
							iRnd += 1
				if iRnd > 0:
					loopCity.setOccupationTimer(iRnd)

		elif iProjectType == gc.getInfoTypeForString('PROJECT_BIRTHRIGHT_REGAINED'):
			pPlayer.setFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL, False)

		elif iProjectType == gc.getInfoTypeForString('PROJECT_BLOOD_OF_THE_PHOENIX'):
			for loopUnit in PyPlayer(iPlayer).getUnitList():
				if loopUnit.isAlive():
					if loopUnit.getUnitCombatType() != UnitCombatTypes.NO_UNITCOMBAT:
						loopUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMORTAL'), True)

		elif iProjectType == gc.getInfoTypeForString('PROJECT_GENESIS'):
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.getTeam() == iTeam:
					iCiv = pLoopPlayer.getCivilizationType()
					if not iCiv in [iInfernal, iIllians]:
						cf.genesis(iLoopPlayer)
			cf.genesis(iPlayer)


		elif iProjectType == gc.getInfoTypeForString('PROJECT_HALLOWING_OF_THE_ELOHIM'):
			iRel = gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS')
			if not pCity.isHasReligion(iRel):
				pCity.setHasReligion(iRel,True,False,False)

		elif iProjectType == gc.getInfoTypeForString('PROJECT_ELEGY_OF_THE_SHEAIM'):
			iRel = gc.getInfoTypeForString('RELIGION_COVEN')
			if not pCity.isHasReligion(iRel):
				pCity.setHasReligion(iRel,True,False,False)



#High AC rituals
		elif iProjectType == gc.getInfoTypeForString('PROJECT_BANE_DIVINE'):
			iMatronae = gc.getInfoTypeForString('RELIGION_MATRONAE')
			iCabal = gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL')
			iOne = gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE')
			iDivine = gc.getInfoTypeForString('PROMOTION_DIVINE')
			iCombatDisciple = gc.getInfoTypeForString('UNITCOMBAT_DISCIPLE')
			iDeath = gc.getInfoTypeForString('DAMAGE_DEATH')
			iFire=gc.getInfoTypeForString('DAMAGE_FIRE')
			iCold = gc.getInfoTypeForString('DAMAGE_COLD')
			iHoly = gc.getInfoTypeForString('DAMAGE_HOLY')
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive():
					for loopUnit in PyPlayer(iLoopPlayer).getUnitList():
						if gc.getUnitInfo(loopUnit.getUnitType()).getPrereqReligion() not in [-1, iOne, iMatronae, iCabal]:
							loopUnit.setHasPromotion(iDivine, False)
							iDamageMin = 25
							iDamageMax = 50
							if loopUnit.getUnitCombatType() == iCombatDisciple:
								iDamageMin *= 2
								iDamageMax *= 2
							loopUnit.doDamageNoCaster(iDamageMin, iDamageMax, iDeath, False)
							loopUnit.doDamageNoCaster(iDamageMin, iDamageMax, iFire, False)
							loopUnit.doDamageNoCaster(iDamageMin, iDamageMax, iCold, False)
							loopUnit.doDamageNoCaster(iDamageMin, iDamageMax, iHoly, False)
							if loopUnit.getUnitCombatType() == iCombatDisciple:
								loopUnit.kill(False, iPlayer)
								
			if not pCity.isHasReligion(iMatronae):
				pCity.setHasReligion(iMatronae,True,False,False)
			pPlayer.foundReligion(iMatronae, iMatronae, True)

		elif iProjectType == gc.getInfoTypeForString('PROJECT_GLORY_EVERLASTING'):
			iDemon = gc.getInfoTypeForString('PROMOTION_DEMON')
			iUndead = gc.getInfoTypeForString('PROMOTION_UNDEAD')
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive():
					for loopUnit in PyPlayer(iLoopPlayer).getUnitList():
						if loopUnit.getRace() in [iDemon, iUndead]:
							loopUnit.kill(False, pCity.getOwner())

#Beast making rituals
		elif iProjectType == gc.getInfoTypeForString('PROJECT_PACT_OF_THE_NILHORN'):
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HILL_GIANT'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_NORTH)
			newUnit1.setName("Larry")
			newUnit1.AI_setGroupflag(10)
			newUnit1.setUnitAIType(gc.getInfoTypeForString('UNITAI_ATTACK_CITY'))

			newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HILL_GIANT'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_NORTH)
			newUnit2.setName("Curly")
			newUnit2.AI_setGroupflag(10)
			newUnit2.setUnitAIType(gc.getInfoTypeForString('UNITAI_ATTACK_CITY'))

			newUnit3 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HILL_GIANT'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_NORTH)
			newUnit3.setName("Moe")
			newUnit3.AI_setGroupflag(10)
			newUnit3.setUnitAIType(gc.getInfoTypeForString('UNITAI_ATTACK_CITY'))

			newUnit4 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HILL_GIANT'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_NORTH)
			newUnit4.setName("Shemp")
			newUnit4.AI_setGroupflag(10)
			newUnit4.setUnitAIType(gc.getInfoTypeForString('UNITAI_ATTACK_CITY'))

			newUnit5 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HILL_GIANT'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_NORTH)
			newUnit5.setName("Ted")
			newUnit5.AI_setGroupflag(10)
			newUnit5.setUnitAIType(gc.getInfoTypeForString('UNITAI_ATTACK_CITY'))

			newUnit6 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HILL_GIANT'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_NORTH)
			newUnit6.setName("Curly Joe")
			newUnit6.AI_setGroupflag(10)
			newUnit6.setUnitAIType(gc.getInfoTypeForString('UNITAI_ATTACK_CITY'))

#some AI help
			if pPlayer.isHuman():
				newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)
				newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)
				newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)

		elif iProjectType == gc.getInfoTypeForString('PROJECT_NATURES_REVOLT'):
			lHeroicPromotions = [	gc.getInfoTypeForString('PROMOTION_HEROIC_DEFENSE'),
									gc.getInfoTypeForString('PROMOTION_HEROIC_DEFENSE2'),
									gc.getInfoTypeForString('PROMOTION_HEROIC_STRENGTH'),
									gc.getInfoTypeForString('PROMOTION_HEROIC_STRENGTH2')
									]
			iHeld = gc.getInfoTypeForString('PROMOTION_HELD')
			
			iAxeman = gc.getInfoTypeForString('UNITCLASS_AXEMAN')
			iHunter = gc.getInfoTypeForString('UNITCLASS_HUNTER')
			iScout = gc.getInfoTypeForString('UNITCLASS_SCOUT')
			iWarrior = gc.getInfoTypeForString('UNITCLASS_WARRIOR')
			iWorker = gc.getInfoTypeForString('UNITCLASS_WORKER')
			iAssassin = gc.getInfoTypeForString('UNITCLASS_ASSASSIN')
			iArcher = gc.getInfoTypeForString('UNITCLASS_ARCHER')
			iLongbowman = gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN')
			iCrossbowman = gc.getInfoTypeForString('UNITCLASS_CROSSBOWMAN')
			iAdept = gc.getInfoTypeForString('UNITCLASS_ADEPT')
			iMage = gc.getInfoTypeForString('UNITCLASS_MAGE')
			iChampion = gc.getInfoTypeForString('UNITCLASS_CHAMPION')
			iFreak = gc.getInfoTypeForString('UNITCLASS_FREAK')
			iPhalanx = gc.getInfoTypeForString('UNITCLASS_PHALANX')
			iHorseman = gc.getInfoTypeForString('UNITCLASS_HORSEMAN')
			iHorseArcher = gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER')
			iRanger = gc.getInfoTypeForString('UNITCLASS_RANGER')
			iKnight = gc.getInfoTypeForString('UNITCLASS_KNIGHT')
			
			iWolf = gc.getInfoTypeForString('UNIT_WOLF')
			iWolfPack = gc.getInfoTypeForString('UNIT_WOLF_PACK')
			iLion = gc.getInfoTypeForString('UNIT_LION')
			iBear = gc.getInfoTypeForString('UNIT_BEAR')
			iBearPolar = gc.getInfoTypeForString('UNIT_POLAR_BEAR')
			iTiger = gc.getInfoTypeForString('UNIT_TIGER')
			
			iBaboon = gc.getInfoTypeForString('UNIT_BABOON')
			iBabySpider = gc.getInfoTypeForString('UNIT_BABY_SPIDER')
			iSpider = gc.getInfoTypeForString('UNIT_GIANT_SPIDER')
			iTortoise = gc.getInfoTypeForString('UNIT_GIANT_TORTOISE')
			iElephant = gc.getInfoTypeForString('UNIT_ELEPHANT')
			iMammoth = gc.getInfoTypeForString('UNIT_MAMMOTH')
			iGriffon = gc.getInfoTypeForString('UNIT_GRIFFON')
			iGorilla = gc.getInfoTypeForString('UNIT_GORILLA')
			iHawk = gc.getInfoTypeForString('UNIT_HAWK')
			iHyena = gc.getInfoTypeForString('UNIT_HYENA')
			iPride = gc.getInfoTypeForString('UNIT_LION_PRIDE')
			iScorpion = gc.getInfoTypeForString('UNIT_SCORPION')
			iPanther = gc.getInfoTypeForString('UNIT_PANTHER')
			iPegasus = gc.getInfoTypeForString('UNIT_PEGASUS')
			iSabertooth = gc.getInfoTypeForString('UNIT_SABERTOOTH')
			iSeaSerpent = gc.getInfoTypeForString('UNIT_SEA_SERPENT')
			iStag = gc.getInfoTypeForString('UNIT_STAG')
			iRottingWolf = gc.getInfoTypeForString('UNIT_ROTTING_WOLF')
			
			iWinterborn = gc.getInfoTypeForString('PROMOTION_WINTERBORN')
			
			py = PyPlayer(gc.getBARBARIAN_PLAYER())
			for pUnit in py.getUnitList():
				if not pUnit.isAlive():
					continue
				if pUnit.isHasPromotion(iHeld):
					continue
				if pUnit.isAnimal():
					for iProm in lHeroicPromotions:
						pUnit.setHasPromotion(iProm, True)
					continue
				bValid = False
				iUnitType = pUnit.getUnitClassType()
				if iUnitType == iWorker:
					iNewUnit = iWolf
					bValid = True
				elif iUnitType == iScout:
					iNewUnit = iLion
					bValid = True
				elif iUnitType == iWarrior:
					iNewUnit = iLion
					bValid = True
				elif iUnitType == iHunter:
					iNewUnit = iTiger
					bValid = True
				elif iUnitType == iRanger:
					iNewUnit = iSabertooth
					bValid = True
				elif iUnitType == iAssassin:
					iNewUnit = iPanther
					bValid = True
				elif iUnitType == iAdept:
					iNewUnit = iBaboon
					bValid = True
				elif iUnitType == iArcher:
					iNewUnit = iBabySpider
					bValid = True
				elif iUnitType == iLongbowman:
					iNewUnit = iSpider
					bValid = True
				elif iUnitType == iCrossbowman:
					iNewUnit = iScorpion
					bValid = True
				elif iUnitType == iMage:
					iNewUnit = iGorilla
					bValid = True
				elif iUnitType == iFreak:
					iNewUnit = iHyene
					bValid = True
				elif iUnitType == iHorseman:
					iNewUnit = iWolfPack
					bValid = True
				elif iUnitType == iHorseArcher:
					iNewUnit = iStag
					bValid = True
				elif iUnitType == iKnight:
					iNewUnit = iPegasus
					bValid = True
				elif iUnitType == iAxeman:
					iNewUnit = iBear
					if pUnit.isHasPromotion(iWinterborn):
						iNewUnit = iBearPolar
					bValid = True
				elif iUnitType == iPhalanx:
					iNewUnit = iElephant
					if pUnit.isHasPromotion(iWinterborn):
						iNewUnit = iMammoth
					bValid = True
				if bValid:
					newUnit = bPlayer.initUnit(iNewUnit, pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
					# newUnit = bPlayer.initUnit(iNewUnit, pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
					# newUnit = bPlayer.initUnit(iNewUnit, pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
					pUnit.kill(True, PlayerTypes.NO_PLAYER)
					newUnit.convert(pUnit)
			for iLoopPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive():
					py = PyPlayer(iLoopPlayer)
					for pUnit in py.getUnitList():
						if pUnit.isAlive():
							if pUnit.isAnimal():
								for iProm in lHeroicPromotions:
									pUnit.setHasPromotion(iProm, True)
			for iUnit in [gc.getInfoTypeForString('UNIT_GURID'), gc.getInfoTypeForString('UNIT_MARGALARD'), gc.getInfoTypeForString('UNIT_LEVIATHAN'), gc.getInfoTypeForString('UNIT_XIEN')]:
				if CyGame().getUnitCreatedCount(iUnit) == 0:
					cf.addUnit(iUnit)


		elif iProjectType == gc.getInfoTypeForString('PROJECT_STIR_FROM_SLUMBER'):
			pCity.setHasReligion(gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON'),True,True,True)
			listWyrmholds = [	gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_FEATHERED'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_BLOOD'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_SIEGE'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_GOLD'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_GRAVE'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_OBSIDIAN'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_FANG'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_RUNE'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_PIT'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_FURNACE'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_ELDER'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_WINTER'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_SHIELD'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_CORAL'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_VAULT'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_SEED'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_SHADOW'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_SHIMMERING'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_DAWN'),
								gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_SCALED')
								]
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_OMNISCIENCE')):
				listWyrmholds.append(gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_SPIRE'))
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_MALEVOLENT_DESIGNS')) and eTeam.isBuildingClassMaxedOut(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_NECROMANCY'),0):
				if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_SIDAR') and pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_SOUL_SHROUD')) < 1:
					listWyrmholds.append(gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_DRACOLICH'))
			for iWyrmhold in listWyrmholds:
				infoWyrmhold = gc.getImprovementInfo(iWyrmhold)
				iBonus = infoWyrmhold.getBonusConvert()
				if iBonus != -1:
					if cf.getNumBonusEffective(iPlayer, iBonus) < 1:
						continue
				iDragon = infoWyrmhold.getSpawnUnitType()
				if iDragon !=-1:
					if bPlayer.isUnitClassMaxedOut(gc.getUnitInfo(iDragon).getUnitClassType(), 0):
						continue
					if pPlayer.isUnitClassMaxedOut(gc.getUnitInfo(iDragon).getUnitClassType(), 0):
						continue
				pWyrmholdPlot = cf.findImprovement(iWyrmhold)
				if pWyrmholdPlot == -1:
					pWyrmholdPlot = cf.addLair(iWyrmhold)
					self.onImprovementBuilt([iWyrmhold, pWyrmholdPlot.getX(), pWyrmholdPlot.getY()])
				# elif iDragon !=-1:
					# if not bPlayer.isUnitClassMaxedOut(gc.getUnitInfo(iDragon).getUnitClassType(), 0):
						# newUnit = bPlayer.initUnit(iDragon, pWyrmholdPlot.getX(), pWyrmholdPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						# newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAIR_GUARDIAN'), True)

# White Hand Rituals
		elif iProjectType == gc.getInfoTypeForString('PROJECT_SAMHAIN'):

			for pyCity in PyPlayer(iPlayer).getCityList():
				loopCity = pyCity.GetCy()
				loopCity.changeHappinessTimer(20)

			iPlayerFrostling = iBarbPlayer
			if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
				iPlayerFrostling = cf.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
				if iPlayerFrostling == -1:
					iPlayerFrostling = iBarbPlayer

			cf.addUnit(gc.getInfoTypeForString('UNIT_MOKKA'), iPlayerFrostling)
			iCount = CyGame().countCivPlayersAlive() + int(CyGame().getHandicapType()) - 5
			for i in xrange(iCount):
				cf.addUnit(gc.getInfoTypeForString('UNIT_FROSTLING'), iPlayerFrostling)
				cf.addUnit(gc.getInfoTypeForString('UNIT_FROSTLING'), iPlayerFrostling)
				cf.addUnit(gc.getInfoTypeForString('UNIT_FROSTLING_ARCHER'), iPlayerFrostling)
				cf.addUnit(gc.getInfoTypeForString('UNIT_FROSTLING_WOLF_RIDER'), iPlayerFrostling)

		elif iProjectType == gc.getInfoTypeForString('PROJECT_THE_WHITE_HAND'):
			iBarbTeam = gc.getBARBARIAN_TEAM()
			bTeam = gc.getTeam(iBarbTeam)
			iDisciple = gc.getInfoTypeForString('UNIT_DISCIPLE_HAND')
			iHand = gc.getInfoTypeForString('RELIGION_WHITE_HAND')
			iHollowMan = gc.getInfoTypeForString('UNIT_HOLLOW_MAN')
			iLetum = gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS')
			iHN = gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY')
			iHidden = gc.getInfoTypeForString('PROMOTION_HIDDEN')
			iSluagh = gc.getInfoTypeForString('UNIT_SLUAGH')
			iHollowMan = gc.getInfoTypeForString('UNIT_HOLLOW_MAN')

			lBoundProm = [	gc.getInfoTypeForString('PROMOTION_NETHERBIND'),
							gc.getInfoTypeForString('PROMOTION_CAPTUS_CAVEAE_SAWOL'),
							gc.getInfoTypeForString('PROMOTION_CAPTUS_CAVEAE_ANGELORUM'),
							gc.getInfoTypeForString('PROMOTION_INCARCERATUS_JUDICII'),
							gc.getInfoTypeForString('PROMOTION_SOUL_FORGED'),
							gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH')
							]
			if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_STIR_FROM_SLUMBER')) < 1:
				lBoundProm.append(gc.getInfoTypeForString('PROMOTION_DRAGON'))
			listRemove = [
							gc.getInfoTypeForString('PROMOTION_HELD'),
							gc.getInfoTypeForString('PROMOTION_MAGIC_IMMUNE'),
							gc.getInfoTypeForString('PROMOTION_CANNOT_CAST')
						]

			iPriest = iDisciple
			if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_PRIESTHOOD')):
				iPriest = gc.getInfoTypeForString('UNIT_PRIEST_OF_WINTER')

			pCity.setHasReligion(iHand, True, True, True)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND'), 1)
			self.onBuildingBuilt([pCity, gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND')])

			cf.giftUnitToPlayer(iDisciple, iPlayer, 0, -1, -1,iHand)
			cf.giftUnitToPlayer(iPriest, iPlayer, 0, -1, -1,iHand)

			iAuricL = gc.getInfoTypeForString('LEADER_AURIC')
			iAuricPlayer = -1
			if pPlayer.getLeaderType() == iAuricL:
				iAuricPlayer = iPlayer
			elif CyGame().isLeaderEverActive(iAuricL):
				iAuricPlayer = cf.getLeader(iAuricL)
				if iAuricPlayer == -1:
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.getLeaderType() == iAuricL:
							if not pLoopPlayer.isAlive():
								pLoopPlayer.setAlive(True)
								iAuricPlayer = iLoopPlayer
								break
			else:
				iAuricPlayer = pPlayer.initNewEmpire(iAuricL, iIllians)

			if iAuricPlayer != -1:
				pAuricPlayer = gc.getPlayer(iAuricPlayer)

				pAuricPlayer.setLastStateReligion(iHand)
				pAuricPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength())
				iAuricTeam = pAuricPlayer.getTeam()
				eAuricTeam = gc.getTeam(iAuricTeam)

				if iAuricTeam != iTeam:
					eTeam.makePeace(iAuricTeam)
					eTeam.signOpenBorders(iAuricTeam)

				newUnit = pAuricPlayer.initUnit(iPriest, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

				pIntroitus = cf.findImprovement(iLetum)
				# if pIntroitus == -1:
					# pMulyr = CyGame().getHolyCity(iHand)
					# if not pMulyr.isNone():
						# pIntroitus= pMulyr.plot()

				if pIntroitus == -1:

					iGlacier = gc.getInfoTypeForString('TERRAIN_GLACIER')
					iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
					iWaste = gc.getInfoTypeForString('TERRAIN_WASTELAND')
					iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')

					pBestPlot = -1
					iBestPlot = -1
					for iLoop in xrange (CyMap().numPlots()):
						pLoopPlot = CyMap().plotByIndex(iLoop)
						iPlot = -1
						if pAuricPlayer.canFound(pLoopPlot.getX(), pLoopPlot.getY()):
							if pLoopPlot.getNumUnits() == 0:
								iPlot = CyGame().getSorenRandNum(50, "Place "+ pAuricPlayer.getName().encode('latin_1','replace'))

								iTerrain = pLoopPlot.getTerrainType()
								if iTerrain == iGlacier:
									iPlot += 100
								elif iTerrain == iSnow:
									iPlot += 75
								elif iTerrain == iWaste:
									iPlot += 50
								elif iTerrain == iTundra:
									iPlot += 25

								iPlot += 50
								iPlot += pLoopPlot.area().getNumTiles() * 2
								iPlot += pLoopPlot.area().getNumUnownedTiles() * 10
								if pLoopPlot.area().getNumTiles() < 3:
									iPlot -= 500
								if pLoopPlot.isAdjacentOwned():
									iPlot -= 200
								for jPlayer in xrange(gc.getMAX_PLAYERS()):
									lPlayer = gc.getPlayer(jPlayer)
									if lPlayer.isAlive():
										if lPlayer.getCivilizationType() == iIllians:
											pCapital = lPlayer.getCapitalCity()
											if not pCapital.isNone():
												iDistance = CyMap().calculatePathDistance(pLoopPlot, pCapital.plot())
												if iDistance == -1:
													iPlot += 50
												else:
													iPlot += iDistance
								iX = pLoopPlot.getX()
								iY = pLoopPlot.getY()
								## Check Big Fat Cross for other players, resources and terrain
								for iDirection in xrange(DirectionTypes.NUM_DIRECTION_TYPES):
									pCityPlot = plotDirection(iX, iY, DirectionTypes(iDirection))
									iPlot += (pCityPlot.getYield(YieldTypes.YIELD_PRODUCTION)-2)*20
									iPlot += (pCityPlot.getYield(YieldTypes.YIELD_COMMERCE)-2)*5
									iPlot += (pCityPlot.getYield(YieldTypes.YIELD_FOOD)-2)*5
									if pLoopPlot.isCity():
										iPlot -= 100
									if pLoopPlot.isAdjacentOwned():
										iPlot -= 30
									if pCityPlot.isWater():
										iPlot -= 15
									iCityBonus = pCityPlot.getBonusType(TeamTypes.NO_TEAM)
									if not iCityBonus == BonusTypes.NO_BONUS:
										iPlot += gc.getBonusInfo(iCityBonus).getYieldChange(YieldTypes.YIELD_PRODUCTION) * 20
										iPlot += gc.getBonusInfo(iCityBonus).getYieldChange(YieldTypes.YIELD_COMMERCE) * 10
									for jPlayer in xrange(gc.getMAX_PLAYERS()):
										lPlayer = gc.getPlayer(jPlayer)
										if lPlayer.isAlive():
											if pCityPlot.getCulture(jPlayer) > 100:
												iPlot -= 250
						if iPlot > iBestPlot:
							iBestPlot = iPlot
							pBestPlot = pLoopPlot

					if pBestPlot != -1:
						if not pBestPlot.isCity():
							pBestPlot.setImprovementType(iLetum)
							pIntroitus = pBestPlot

				if pIntroitus != -1:
					iX = pIntroitus.getX()
					iY = pIntroitus.getY()
					if pIntroitus != pCity.plot():
						pIntroitus.setOwner(iAuricPlayer)
						pIntroitus.setPlotType(PlotTypes.PLOT_HILLS, True, True)

					for i in xrange(pIntroitus.getNumUnits(), -1, -1):#I had a game where Auric had to fight Orthus for the Letum Frigus, and died before he could lead anyone.
						pUnit = pIntroitus.getUnit(i)
						iUnit = pUnit.getUnitType()

						if iUnit == iSluagh:
							for iProm in lBoundProm:
								if pUnit.isHasPromotion(iProm):
									break
							else:
								iUnit = pSluagh.getScenarioCounter()
								if -1 < iUnit < gc.getNumUnitInfos():
									if not isWorldUnitClass(gc.getUnitInfo(iUnit).getUnitClassType()):
										sName = pUnit.getNameNoDesc()[:pSluagh.getNameNoDesc().find("'s Sluagh")]
								
										newUnit = pAuricPlayer.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
										newUnit.convert(pUnit)
										newUnit.setReligion(iHand)
										for iProm in listRemove:
											newUnit.setHasPromotion(iProm, False)
										newUnit.setName(sName)


						
						elif pUnit.getTeam() != iAuricTeam:
							pUnit.setHasPromotion(iHidden, False)
							pUnit.setHasPromotion(iHN, False)
							pUnit.setHasCasted(True)
							pUnit.changeImmobileTimer(-pUnit.getImmobileTimer())
							iUTeam = gc.getTeam(pUnit.getTeam())

							if not pUnit.jumpToNearestValidPlot():
								pRefuge = cf.findClearPlot(pUnit, -1)
								if pRefuge != -1:
									pUnit.setXY(pRefuge.getX(), pRefuge.getY(), True, True, False)
								elif pUnit.isHiddenNationality() or iUTeam.isAtWar(iAuricTeam):# or iUTeam.isAtWar(iTeam):
									if pUnit.getReligion() == iHand:
										newUnit = pAuricPlayer.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
										newUnit.convert(pUnit)
										newUnit.setReligion(iHand)
									else:
										pUnit.kill(False, -1)


					liStartingUnits = [
										gc.getInfoTypeForString('UNIT_WORKER'),
										gc.getInfoTypeForString('UNIT_SUPPLIES'),
										gc.getInfoTypeForString('UNIT_SUPPLIES'),
										gc.getInfoTypeForString('UNIT_ADEPT'),
										gc.getInfoTypeForString('UNIT_JAVELIN_THROWER'),
										gc.getInfoTypeForString('UNIT_JAVELIN_THROWER'),
										gc.getInfoTypeForString('UNIT_JAVELIN_THROWER'),
										gc.getInfoTypeForString('UNIT_WARRIOR'),
										gc.getInfoTypeForString('UNIT_AXEMAN'),
										iPriest,
										iDisciple
										]
					iArea = pIntroitus.area()
					iNumConscripts = 1
					for iLoopTeam in xrange(gc.getMAX_TEAMS()):
						if iLoopTeam == iBarbTeam: continue
						eLoopTeam = gc.getTeam(iLoopTeam)
						if eAuricTeam.isAtWar(iLoopTeam):
							iNumConscripts += eLoopTeam.countNumUnitsByArea(iArea)/8
						elif iLoopTeam == iAuricTeam or eLoopTeam.isVassal(iAuricTeam):
							iNumConscripts -= eLoopTeam.countNumUnitsByArea(iArea)/4

					for i in xrange(iNumConscripts):
						liStartingUnits.append(pCity.getConscriptUnit())

					liRecruits = liStartingUnits + [iHollowMan,iHollowMan,iHollowMan]

					if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('UNITCLASS_AURIC'), 0):
						liRecruits += [gc.getInfoTypeForString('UNIT_AURIC')]
					if pAuricPlayer.getNumCities() < 1:
						liRecruits += [gc.getInfoTypeForString('UNIT_SETTLER')]


					for iUnit in liRecruits:
						pNewUnit = pAuricPlayer.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
						pCity.applyBuildEffects(pNewUnit)
						pNewUnit.setReligion(iHand)
						pNewUnit.finishMoves()

					if pIntroitus != pCity.plot():
						pIntroitus.setOwner(iAuricPlayer)

					if iAuricTeam != iTeam:
						pAuricPlayer.AI_changeAttitudeExtra(iPlayer, 7)
						eTeam.makePeace(iAuricTeam)
						eTeam.signOpenBorders(iAuricTeam)
						eTeam.signDefensivePact(iAuricTeam)

						if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS):
							eAuricTeam.setHasNonAggression(iTeam, True)
							if not eTeam.isHasEmbassy(iAuricTeam):
								eTeam.setHasEmbassy(iAuricTeam, True)
							if not eAuricTeam.isHasEmbassy(iTeam):
								eAuricTeam.setHasEmbassy(iTeam, True)


						for iLoopTeam in xrange(gc.getMAX_TEAMS()):
##							if iLoopTeam == iBarbTeam: continue
							if eTeam.isAtWar(iLoopTeam):
								if eAuricTeam.canDeclareWar(iLoopTeam):
									eAuricTeam.declareWar(iLoopTeam, False, WarPlanTypes.WARPLAN_LIMITED)
								else:
									eAuricTeam.setHasPrepareWar(iLoopTeam,True)
							elif eTeam.isHasPrepareWar(iLoopTeam):
								eAuricTeam.setHasPrepareWar(iLoopTeam,True)

						if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_PERMANENT_ALLIANCES):
							iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_PERMANENT_ALLIANCE')
							triggerData = pPlayer.initTriggeredData(iEvent, True, -1, iX, iY, iAuricPlayer, -1, -1, -1, -1, -1)

					for iHandLeader, iAvatar in [
													(gc.getInfoTypeForString('LEADER_ANAGANTIOS'),gc.getInfoTypeForString('UNIT_ANAGANTIOS')),
													(gc.getInfoTypeForString('LEADER_DUMANNIOS'),gc.getInfoTypeForString('UNIT_DUMANNIOS')),
													(gc.getInfoTypeForString('LEADER_RIUROS'),gc.getInfoTypeForString('UNIT_RIUROS'))
													]:

						iHandPlayer = cf.getLeader(iHandLeader)
						if iHandPlayer != -1:
							pHandPlayer = gc.getPlayer(iHandPlayer)
							if not pHandPlayer.isAlive():
								pHandPlayer.setAlive(True)
							pHandPlayer.setLastStateReligion(iHand)


							iTeamH = pHandPlayer.getTeam()

							if iTeamH != iAuricTeam and iTeamH != iTeam:
								eTeam.makePeace(iTeamH)
								# eAuricTeam.makePeace(iTeamH)
								# eTeam.signOpenBorders(iTeamH)
								eAuricTeam.signOpenBorders(iTeamH)
								pHandPlayer.AI_changeAttitudeExtra(iPlayer, 4)
								pHandPlayer.AI_changeAttitudeExtra(iAuricPlayer, 4)
								eAuricTeam.assignVassal(iTeamH, True)

								if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS):
									eAuricTeam.setHasNonAggression(iTeamH, True)
									eTeam.setHasNonAggression(iTeamH, True)
									if not eTeam.isHasEmbassy(iTeamH):
										eTeam.setHasEmbassy(iTeamH, True)
									if not eAuricTeam.isHasEmbassy(iTeamH):
										eAuricTeam.setHasEmbassy(iTeamH, True)

							liRecruits = liStartingUnits

							pCity1 = pCity
							if pHandPlayer.getNumCities() > 0:
								pCity1 = pHandPlayer.firstCity(False)[0]

								pCity1.setHasReligion(iHand, True, True, True)
								pCity1.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND'), 1)
								self.onBuildingBuilt([pCity1, gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND')])

							else:
								liRecruits += [gc.getInfoTypeForString('UNIT_SETTLER')]

							for iUnit in liRecruits + [iAvatar]:
								pNewUnit = pHandPlayer.initUnit(iUnit, pCity1.getX(), pCity1.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
								pNewUnit.setReligion(iHand)
								pNewUnit.finishMoves()
								pCity.applyBuildEffects(pNewUnit)
								if not pHandPlayer.isHuman():
									if iUnit == gc.getInfoTypeForString('UNIT_AURIC'):
										pNewUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAIR_GUARDIAN'), True)

							pIntroitus.setRevealed(pHandPlayer.getTeam(), True, False, -1)

							CyInterface().addMessage(iHandPlayer,True,25,CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_VICTORY", ()),'',1,'Art/Interface/Buttons/Improvements/Letum Frigus.dds',ColorTypes(8),iX,iY,True,True)

					CyInterface().addMessage(iAuricPlayer,True,25,CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_VICTORY", ()),'',1,'Art/Interface/Buttons/Improvements/Letum Frigus.dds',ColorTypes(8),iX,iY,True,True)

					pIntroitus.setFeatureType(gc.getInfoTypeForString('FEATURE_BLIZZARD'),-1)
##					pIntroitus.setImprovementType(-1)

					if pIntroitus.isCity():
						pMulyr = pIntroitus.getPlotCity()
##						if pMulyr.getTeam() != iTeam:
						pAuricPlayer.acquireCity(pMulyr, False, True)

					else:
						pAuricPlayer.initCity(iX, iY)

					if pIntroitus.isCity():
						pIntroitus.setBonusType(gc.getInfoTypeForString('BONUS_MANA_ICE'))
						pMulyr = pIntroitus.getPlotCity()
						pMulyr.setOccupationTimer(0)
						iChange = -9
						pTimer = pMulyr.getHurryAngerTimer()
						if pTimer < 9:
							iChange = 0 - pTimer
						pMulyr.changeHurryAngerTimer(iChange)
						if pMulyr.getRevolutionIndex() > 0:
							pMulyr.setRevolutionIndex(0)

						pMulyr.setName(CyTranslator().getText("TXT_KEY_CITY_NEW_MULYR", ()), False)
						gc.getGame().setHolyCity(iHand, pMulyr, True)
						pMulyr.setHasReligion(iHand, True, True, True)
						pMulyr.changePopulation(5)
						pMulyr.changeCulture(iAuricPlayer, 120, True)

					for iBuilding in xrange(gc.getNumBuildingInfos()):
						if pMulyr.canConstruct(iBuilding, False, False, False):
							info = gc.getBuildingInfo(iBuilding)
							if not isWorldWonderClass(info.getBuildingClassType()):
								pMulyr.setNumRealBuilding(iBuilding, 1)
								self.onBuildingBuilt([pMulyr, iBuilding])


						# pMulyr.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MAGE_GUILD'), 1)
						# pMulyr.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ELDER_COUNCIL'), 1)
						# pMulyr.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TRAINING_YARD'), 1)
						# pMulyr.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARCHERY_RANGE'), 1)
						# pMulyr.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_HUNTING_LODGE'), 1)
						# pMulyr.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DUNGEON'), 1)
						# pMulyr.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_WALLS'), 1)
						# pMulyr.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_PALISADE'), 1)
						# pMulyr.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MONUMENT'), 1)
						# pMulyr.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_AQUEDUCT'), 1)
						# pMulyr.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND'), 1)
						# self.onBuildingBuilt([pMulyr, gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND')])

					pAuricPlayer.setAlive(True)
					eAuricTeam.changeStolenVisibilityTimer(iTeam,1)
					eTeam.changeStolenVisibilityTimer(iAuricTeam,1)
					CyCamera().JustLookAtPlot(pIntroitus)

		elif iProjectType == gc.getInfoTypeForString('PROJECT_THE_DEEPENING'):

			iManaRaw = gc.getInfoTypeForString('BONUS_MANA')
			iManaIce = gc.getInfoTypeForString('BONUS_MANA_ICE')

			iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
			iGrass = gc.getInfoTypeForString('TERRAIN_GRASS')
			iMarsh = gc.getInfoTypeForString('TERRAIN_MARSH')
			iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
			iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
			iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
			iGlacier = gc.getInfoTypeForString('TERRAIN_GLACIER')
			iWaste = gc.getInfoTypeForString('TERRAIN_WASTELAND')
			iBlizzard = gc.getInfoTypeForString('FEATURE_BLIZZARD')
			iModifier = (gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getVictoryDelayPercent() * 20) / 100
			iTimer = 40 + iModifier
			for i in xrange (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				bValid = False
				if CyGame().getSorenRandNum(100, "The Deepening at plot " + str(i)) < 20:

					if pPlot.getBonusType(-1) == iManaRaw:
						pPlot.setBonusType(iManaIce)
					iTerrain = pPlot.getTerrainType()
					if pPlot.isWater():
						bValid = True
					elif iTerrain == iSnow:
						bValid = True
					elif iTerrain == iTundra:
						pPlot.setTempTerrainType(iSnow, CyGame().getSorenRandNum(iTimer, "Snow") + 10)
						bValid = True
					elif iTerrain == iGlacier:
						bValid = True
					elif iTerrain == iWaste:
						pPlot.setTempTerrainType(iGlacier, CyGame().getSorenRandNum(iTimer, "Glac") + 10)
						bValid = True
					elif iTerrain in [iGrass, iMarsh]:
						pPlot.setTempTerrainType(iTundra, CyGame().getSorenRandNum(iTimer, "Tundra") + 10)
						bValid = True
					elif iTerrain == iPlains:
						pPlot.setTempTerrainType(iTundra, CyGame().getSorenRandNum(iTimer, "Tundra") + 10)
						bValid = True
					elif iTerrain == iDesert:
						pPlot.setTempTerrainType(iPlains, CyGame().getSorenRandNum(iTimer, "Plains") + 10)
					if pPlot.getFeatureType() ==-1:
						bValid = False
					if bValid:
						if CyGame().getSorenRandNum(400, "The Deepening-Blizzard at plot " + str(i)) < 10:
							pPlot.setFeatureType(iBlizzard,-1)


		elif iProjectType == gc.getInfoTypeForString('PROJECT_THE_DRAW'):
			iAuricPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
			iAuric = gc.getInfoTypeForString('UNIT_AURIC')
			iWH = gc.getInfoTypeForString('RELIGION_WHITE_HAND')
			if iAuricPlayer != -1:
				pAuricPlayer = gc.getPlayer(iAuricPlayer)
				iAuricTeam = pAuricPlayer.getTeam()
				eAuricTeam = gc.getTeam(iAuricTeam)
				iBarbTeam = gc.getBARBARIAN_TEAM()
				pAuricPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_INSANE'),True)
##				pAuricPlayer.changeNoDiplomacyWithEnemies(1)
				for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if pLoopPlayer.isAlive():
						iLoopTeam = pLoopPlayer.getTeam()
						if iLoopTeam == iAuricTeam:
							pLoopPlayer.changeNoDiplomacyWithEnemies(1)
						else:
							eLoopTeam = gc.getTeam(iLoopTeam)
							if pLoopPlayer.getStateReligion() == iWH:
								eAuricTeam.assignVassal(iLoopTeam, True)
							elif eLoopTeam.isVassal(iAuricTeam):
								pLoopPlayer.setLastStateReligion(iWH)

				for iLoopTeam in xrange(gc.getMAX_TEAMS()):
					if iLoopTeam != iAuricTeam:
						if iLoopTeam != iBarbTeam:
							eLoopTeam = gc.getTeam(iLoopTeam)
							if eLoopTeam.isAlive():
								if not eLoopTeam.isAVassal():
									if eAuricTeam.canDeclareWar(iLoopTeam):
										eAuricTeam.declareWar(iLoopTeam, False, WarPlanTypes.WARPLAN_LIMITED)

				for loopUnit in PyPlayer(iAuricPlayer).getUnitList():
					if loopUnit.getUnitType() == iAuric:
						loopUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)
						loopUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMORTAL'), True)
						loopUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DIVINE'), True)
						loopUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING4'), True)
						loopUnit.setReligion(iWH)
					else:
						iDmg = loopUnit.getDamage() * 2
						if iDmg > 99:
							iDmg = 99
						if iDmg < 75:
							iDmg = 75
						loopUnit.setDamage(iDmg, iPlayer)
						
				for pyCity in PyPlayer(iAuricPlayer).getCityList():
					loopCity = pyCity.GetCy()
					iPop = int(loopCity.getPopulation() / 2)
					if iPop < 1:
						iPop = 1
					loopCity.setPopulation(iPop)

		elif iProjectType == gc.getInfoTypeForString('PROJECT_ASCENSION'):
			iWH = gc.getInfoTypeForString('RELIGION_WHITE_HAND')
			iAuricPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
			if iAuricPlayer != -1:
				pAuricPlayer = gc.getPlayer(iAuricPlayer)
				iAuricTeam = pAuricPlayer.getTeam()
				iAuricUnit = gc.getInfoTypeForString('UNIT_AURIC')
				
				(pUnit, iter) = pAuricPlayer.firstUnit(False)
				while(pUnit):
					if ( not pUnit.isDead() ): #is the unit alive and valid?
						if pUnit.getUnitType() == iAuricUnit:
							iDC = gc.getInfoTypeForString('BUILDING_DEMONIC_CITIZENS')
							for pyCity in PyPlayer(iAuricPlayer).getCityList():
								loopCity = pyCity.GetCy()
								loopCity.setNumRealBuilding(iDC, 1)
							cf.restoreTraits(pAuricPlayer)
							pAuricPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_FALLOW'),True)
							pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), False)
							pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMORTAL'), False)
							for iProm in xrange(gc.getNumPromotionInfos()):#Embodying Ice cuts off his access to other spheres of mana
								if pUnit.isHasPromotion(iProm):
									info = gc.getPromotionInfo(iProm)
									iBonus = info.getBonusPrereq()
									if iBonus != -1:
										if gc.getBonusInfo(iBonus).isMana():
											pUnit.setHasPromotion(iProm, False)

							newUnit = pAuricPlayer.initUnit(gc.getInfoTypeForString('UNIT_AURIC_ASCENDED'), pUnit.getX(), pUnit.getY(), UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_SOUTH)
							newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION'), True)
							pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION'), False)
							newUnit.convert(pUnit)
							newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION'), False)
							newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AVATAR'), True)
							newUnit.setScenarioCounter(iAuricUnit)
							newUnit.cast(gc.getInfoTypeForString('SPELL_SNOWFALL_GREATER'))
							break
					(pUnit, iter) = pAuricPlayer.nextUnit(iter, False)
				if pAuricPlayer.isHuman():
					t = "TROPHY_FEAT_ASCENSION"
					if not CyGame().isHasTrophy(t):
						CyGame().changeTrophyValue(t, 1)
				if not CyGame().getWBMapScript():
					iBestPlayer = -1
					iBestValue = 0
					eAuricTeam = gc.getTeam(iAuricTeam)
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if not pLoopPlayer.isBarbarian():
								if eAuricTeam.isAtWar(pLoopPlayer.getTeam()):
##								if not pLoopPlayer.getStateReligion() == iWH:
##									iTeam = pLoopPlayer.getTeam()
##									eTeam = gc.getTeam(iTeam)
##									if not (iTeam == iAuricTeam or eTeam.isVassal(iAuricTeam)):
									iValue = CyGame().getSorenRandNum(500, "Ascension")
									if pLoopPlayer.isHuman():
										iValue += 2000
									iValue += (20 - CyGame().getPlayerRank(iLoopPlayer)) * 50
									if iValue > iBestValue:
										iBestValue = iValue
										iBestPlayer = iLoopPlayer
					if iBestPlayer != -1:
						pBestPlayer = gc.getPlayer(iBestPlayer)
						pBestCity = pBestPlayer.getCapitalCity()
						if not pBestCity.isNone():
							if pBestPlayer.isHuman():
								iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_GODSLAYER')
								triggerData = pBestPlayer.initTriggeredData(iEvent, True, -1, pBestCity.getX(), pBestCity.getY(), iBestPlayer, -1, -1, -1, -1, -1)
							else:
								pBestPlayer.initUnit(gc.getInfoTypeForString('EQUIPMENT_GODSLAYER'), pBestCity.getX(), pBestCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					if CyGame().getUnitCreatedCount(gc.getInfoTypeForString('EQUIPMENT_GODSLAYER')) == 0:
						cf.addUnit(gc.getInfoTypeForString('EQUIPMENT_GODSLAYER'))

	def onSelectionGroupPushMission(self, argsList):
		'selection group mission'
		eOwner = argsList[0]
		eMission = argsList[1]
		iNumUnits = argsList[2]
		listUnitIds = argsList[3]
		if not self.__LOG_PUSH_MISSION:
			return
		if pHeadUnit:
			CvUtil.pyPrint("Selection Group pushed mission %d" %(eMission))

	def onUnitMove(self, argsList):
		'unit move'
		pPlot,pUnit,pOldPlot = argsList
		player = PyPlayer(pUnit.getOwner())
		unitInfo = PyInfo.UnitInfo(pUnit.getUnitType())
		if not self.__LOG_MOVEMENT:
			return
		if player and unitInfo:
			CvUtil.pyPrint('Player %d Civilization %s unit %s is moving to %d, %d'
				%(player.getID(), player.getCivilizationName(), unitInfo.getDescription(),
				pUnit.getX(), pUnit.getY()))

	def onUnitSetXY(self, argsList):
		'units xy coords set manually'
		pPlot,pUnit = argsList
		player = PyPlayer(pUnit.getOwner())
		unitInfo = PyInfo.UnitInfo(pUnit.getUnitType())
		if not self.__LOG_MOVEMENT:
			return

	def onUnitCreated(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Unit Completed'
		unit = argsList[0]

		iPlayer = unit.getOwner()
		player = PyPlayer(iPlayer)
		pPlayer = gc.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()
		eTeam = gc.getTeam(iTeam)

		pPlot = unit.plot()
		pArea = unit.area()
		iX = unit.getX()
		iY = unit.getY()

		iUnit = unit.getUnitType()
		infoUnit = gc.getUnitInfo(iUnit)
		iUnitClass = unit.getUnitClassType()
		iUnitCombat = unit.getUnitCombatType()
		iTierU = infoUnit.getTier()

		iStateReligion = pPlayer.getStateReligion()
		iRel = unit.getReligion()
		iLeader = pPlayer.getLeaderType()

		iCiv = pPlayer.getCivilizationType()
		infoCiv = gc.getCivilizationInfo(iCiv)
		iDefaultRace = infoCiv.getDefaultRace()
		iRace = unit.getRace()

		pCity = -1
		if pPlot.isCity():
			pCity = pPlot.getPlotCity()
			if pCity.getOwner() != iPlayer:
				pCity = -1

		iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
		iEmpyrean = gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')
		iRunes = gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH')
		iLeaves = gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')
		iUndertow = gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS')
		iEsus = gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS')
		iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
		iHand = gc.getInfoTypeForString('RELIGION_WHITE_HAND')
		iMatronae = gc.getInfoTypeForString('RELIGION_MATRONAE')

		iUnblemished = gc.getInfoTypeForString('RELIGION_UNBLEMISHED')
		iBrotherhood = gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS')
		iLaeran = gc.getInfoTypeForString('RELIGION_LAERAN_CORD')
		iFoxmen = gc.getInfoTypeForString('RELIGION_FOXMEN')
		iDragonCult = gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON')
		iStewards = gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY')
		iCoven = gc.getInfoTypeForString('RELIGION_COVEN')
		iAnointed = gc.getInfoTypeForString('RELIGION_ANOINTED')
		iOne = gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE')



		iPlenty = gc.getInfoTypeForString('RELIGION_HOUSE_OF_PLENTY')
		iRinggiver = gc.getInfoTypeForString('RELIGION_RINGGIVER')
		iEternalCabal = gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL')
		iGrey = gc.getInfoTypeForString('RELIGION_GREY_COUNCIL')
		iLegion = gc.getInfoTypeForString('RELIGION_EMBER_LEGION')
		iDiscord = gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD')



		iCalabim = gc.getInfoTypeForString('CIVILIZATION_CALABIM')
		iGrigori = gc.getInfoTypeForString('CIVILIZATION_GRIGORI')
		iIllians = gc.getInfoTypeForString('CIVILIZATION_ILLIANS')
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
		iKuriotates = gc.getInfoTypeForString('CIVILIZATION_KURIOTATES')
		iLjosalfar = gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR')
		iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
		iSheaim = gc.getInfoTypeForString('CIVILIZATION_SHEAIM')
		iSvartalfar = gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')



		iEvil = gc.getInfoTypeForString('ALIGNMENT_EVIL')

		iHero = gc.getInfoTypeForString('PROMOTION_HERO')
		iRebel = gc.getInfoTypeForString('PROMOTION_REBEL')
		iLoyal = gc.getInfoTypeForString('PROMOTION_LOYALTY')
		iChanneling1 = gc.getInfoTypeForString('PROMOTION_CHANNELING1')
		iChanneling2 = gc.getInfoTypeForString('PROMOTION_CHANNELING2')
		iChanneling3 = gc.getInfoTypeForString('PROMOTION_CHANNELING3')
		iChanneling4 = gc.getInfoTypeForString('PROMOTION_CHANNELING4')
		iUnholyTaint = gc.getInfoTypeForString('PROMOTION_UNHOLY_TAINT')

		iDivine = gc.getInfoTypeForString('PROMOTION_DIVINE')
		iDivine2 = gc.getInfoTypeForString('PROMOTION_DIVINE2')
		iZeal = gc.getInfoTypeForString('PROMOTION_ZEAL')

		if iUnit in [	gc.getInfoTypeForString('UNIT_CENTAUR_CHARGER'),
						gc.getInfoTypeForString('UNIT_CENTAUR_ARCHER'),
						gc.getInfoTypeForString('UNIT_CENTAUR'),
						gc.getInfoTypeForString('UNIT_CENTAUR_LANCER')
						]:
			iRace = gc.getInfoTypeForString('PROMOTION_CENTAUR')
			unit.setHasPromotion(iRace, True)
		elif unit.getCivilizationType() == iKuriotates:
			if iUnit in [	gc.getInfoTypeForString('UNIT_ADEPT'),
						gc.getInfoTypeForString('UNIT_MAGE'),
						gc.getInfoTypeForString('UNIT_ARCHMAGE'),
						gc.getInfoTypeForString('UNIT_HIGH_PRIEST_LAERAN')]:
				iRace = gc.getInfoTypeForString('PROMOTION_SERPENTINE')
				unit.setHasPromotion(iRace, True)
			elif iUnit in [	gc.getInfoTypeForString('UNIT_ASSASSIN'),
							gc.getInfoTypeForString('UNIT_BEASTMASTER'),
							gc.getInfoTypeForString('UNIT_HUNTER'),
							gc.getInfoTypeForString('UNIT_RANGER'),
							gc.getInfoTypeForString('UNIT_SCOUT'),
							gc.getInfoTypeForString('UNIT_SHADOW')
							]:
				iRace = gc.getInfoTypeForString('PROMOTION_MUSTEVAL')
				unit.setHasPromotion(iRace, True)

		if iUnit in [	gc.getInfoTypeForString('UNIT_ADEPT_LAMIA'),
						gc.getInfoTypeForString('UNIT_MAGE_LAMIA'),
						gc.getInfoTypeForString('UNIT_ARCHMAGE_LAMIA')]:
			iRace = gc.getInfoTypeForString('PROMOTION_SERPENTINE')
			unit.setHasPromotion(iRace, True)
		elif iUnit in [	gc.getInfoTypeForString('UNIT_MUSTEVAL_ASSASSIN'),
						gc.getInfoTypeForString('UNIT_MUSTEVAL_BEASTMASTER'),
						gc.getInfoTypeForString('UNIT_MUSTEVAL_HUNTER'),
						gc.getInfoTypeForString('UNIT_MUSTEVAL_RANGER'),
						gc.getInfoTypeForString('UNIT_MUSTEVAL_SCOUT')
						]:
			iRace = gc.getInfoTypeForString('PROMOTION_MUSTEVAL')
			unit.setHasPromotion(iRace, True)


		listMana = []
		for iLoopBonus in xrange(gc.getNumBonusInfos()):
			if gc.getBonusInfo(iLoopBonus).isMana():
				if pPlayer.getNumAvailableBonuses(iLoopBonus) > 0:
					listMana.append(iLoopBonus)

		bCrucible = PyHelpers.PyGame().doesBuildingExist(gc.getInfoTypeForString('BUILDING_CRUCIBLE'))
		if bCrucible:
			if len(listMana):
				bCrucible = False

		if unit.isMechUnit() or iUnitCombat in [gc.getInfoTypeForString('UNITCOMBAT_BEAST'), gc.getInfoTypeForString('UNITCOMBAT_ANIMAL')]:
			if iDefaultRace != -1:
				if unit.isHasPromotion(iDefaultRace):
					if not infoUnit.getFreePromotions(iDefaultRace):
						unit.setHasPromotion(iDefaultRace, False)

			if unit.isAnimal():
				if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_NATURES_REVOLT')) > 0:
					for sProm in [	'PROMOTION_HEROIC_DEFENSE',
							'PROMOTION_HEROIC_STRENGTH',
							'PROMOTION_HEROIC_DEFENSE2',
							'PROMOTION_HEROIC_STRENGTH2'
							]:
						iProm = gc.getInfoTypeForString(sProm)
						if iProm > -1:
							unit.setHasPromotion(iProm, True)

				if iUnit in [gc.getInfoTypeForString('UNIT_WOLF'), gc.getInfoTypeForString('UNIT_WOLF_PACK')]:
					if pPlot.getTerrainType() in [gc.getInfoTypeForString('TERRAIN_SNOW'), gc.getInfoTypeForString('TERRAIN_GLACIER')]:
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WINTERBORN'), True)

		if unit.getSpecialUnitType() == gc.getInfoTypeForString('SPECIALUNIT_PEOPLE'):
			if iUnit not in [ gc.getInfoTypeForString('UNIT_ADVENTURER'), gc.getInfoTypeForString('UNIT_REFUGEE')]:
				unit.setLevel(5)
				iExperience = unit.experienceNeeded()
				unit.setExperience(iExperience, -1)
				unit.setLevel(6)

			sName = unit.getNameNoDesc()
			if sName == pPlayer.getName():
				unit.setAvatarOfCivLeader(True)
			if sName == pPlayer.getNameKey():
				unit.setAvatarOfCivLeader(True)


			if iUnit == gc.getInfoTypeForString('UNIT_DECIUS'):
				pass
			#The code that prevents adventurers from being duplicated when they upgrade requires they all have unique names, but I figured I might as well give all GP unique names.
			elif sName == "":
				#Advanced Tactics - Diverse Grigori makes even more sense for great people like adventurers. It cannot be allowed for named adventurers though, of else the races might change every turn.
				if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS):
					if iCiv in [iKuriotates, iGrigori]:
						if iRace == -1 and unit.isAlive():
							listRaces = [-1]
							jCult = pPlot.calculateCulturePercent(iPlayer)
							if jCult < 100:
								for jPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
									jCult = pPlot.calculateCulturePercent(jPlayer)
									if jCult > 0:
										pjPlayer = gc.getPlayer(jPlayer)
										jCiv = pjPlayer.getCivilizationType()
										jCivInfo = gc.getCivilizationInfo(jCiv)
										jRace = jCivInfo.getDefaultRace()
										for i in xrange(jCult):
											listRaces.append(jRace)
							iChance = 40
							if len(listRaces) > 0 and CyGame().getSorenRandNum(100, "Grigori Racial Diversity-Great Person- "+unit.getName().encode('latin_1','replace')) <= iChance:

								listRaces = [	gc.getInfoTypeForString('PROMOTION_ORC'),
										gc.getInfoTypeForString('PROMOTION_ORC'),
										gc.getInfoTypeForString('PROMOTION_ORC'),
										gc.getInfoTypeForString('PROMOTION_ORC'),
										gc.getInfoTypeForString('PROMOTION_LIZARDMAN'),
										gc.getInfoTypeForString('PROMOTION_LIZARDMAN'),
										gc.getInfoTypeForString('PROMOTION_DWARF'),
										gc.getInfoTypeForString('PROMOTION_DWARF'),
										gc.getInfoTypeForString('PROMOTION_DWARF'),
										gc.getInfoTypeForString('PROMOTION_ELF'),
										gc.getInfoTypeForString('PROMOTION_ELF'),
										gc.getInfoTypeForString('PROMOTION_DARK_ELF'),
										gc.getInfoTypeForString('PROMOTION_DARK_ELF'),
										gc.getInfoTypeForString('PROMOTION_CENTAUR'),
										gc.getInfoTypeForString('PROMOTION_MUSTEVAL'),
										gc.getInfoTypeForString('PROMOTION_SERPENTINE'),
										gc.getInfoTypeForString('PROMOTION_NOMAD'),
										gc.getInfoTypeForString('PROMOTION_NOMAD'),
										gc.getInfoTypeForString('PROMOTION_WINTERBORN'),
										gc.getInfoTypeForString('PROMOTION_WINTERBORN'),
										gc.getInfoTypeForString('PROMOTION_WINTERBORN'),
										gc.getInfoTypeForString('PROMOTION_WINTERBORN'),
										-1,
										-1,
										-1,
										-1,
										-1,
										-1,
										-1	]
							if len(listRaces) > 0:
								iRace = listRaces.pop(CyGame().getSorenRandNum(len(listRaces), "Grigori or Kuriotates Racial Diversity-Great Person"))
								if iRace != -1:
									unit.setHasPromotion(iRace, True)

				if unit.getReligion() == -1 and pCity != -1:
					lReligions = []
					for iReligion in xrange(gc.getNumReligionInfos()):
						if pCity.isHasReligion(iReligion):
							if CyGame().getSorenRandNum(100, "Religion Adoption") <= gc.getDefineINT("RELIGION_ADOPTION_CHANCE"):
								lReligions += [iReligion]
								if iReligion == iStateReligion:
									lReligions += [iReligion]
					if len(lReligions) > 0:
						iReligion = lReligions.pop(CyGame().getSorenRandNum(len(lReligions), "Religion Adoption "+unit.getName().encode('latin_1','replace')))
						unit.setReligion(iReligion)
				unit.setName(cf.MarnokNameGenerator(unit))
			else:
				if iDefaultRace != -1 and unit.isHasPromotion(iDefaultRace):
					unit.setHasPromotion(iDefaultRace, False)
				#Great People of known races should have those races
				if iUnit == gc.getInfoTypeForString('UNIT_ADVENTURER'):
##					if sName == "Khord Tenhare":
					if sName == localText.getText('TXT_KEY_UNIT_ADVENTURER_5', ()):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
##					elif sName == "Kirien of Brigdarrow":
					elif sName == localText.getText('TXT_KEY_UNIT_ADVENTURER_21', ()):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WINTERBORN'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL1'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL2'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL'), True)
##					elif sName == "Lyrr, Son of Adulin":
					elif sName == localText.getText('TXT_KEY_UNIT_ADVENTURER_22', ()):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)
						unit.setReligion(iLeaves)
##					elif sName == "Volanna":
					elif sName == localText.getText('TXT_KEY_UNIT_ADVENTURER_12', ()):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_ELF'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDO'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MARKSMAN'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOW1'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NATURE1'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SCAVENGER'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEREWOLF'), True)
						unit.setReligion(iFoxmen)
						unit.setScenarioCounter(iUnit)
				elif iUnit == gc.getInfoTypeForString('UNIT_ARTIST'):
##					if sName == "Argase the Magician":
					if sName == localText.getText('TXT_KEY_UNIT_ARTIST_10', ()):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ARCANE'), True)
						unit.setHasPromotion(iChanneling1, True)
						unit.setHasPromotion(iChanneling2, True)
						unit.setLevel(4)
##					if sName == "Dhaunae the Illusionist":
					if sName == localText.getText('TXT_KEY_UNIT_ARTIST_19', ()):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSIONIST'), True)
						unit.setReligion(iEsus)
##					elif sName == "Furia the Mad":
					elif sName == localText.getText('TXT_KEY_UNIT_ARTIST_11', ()):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMORTAL'), True)
##					elif sName == "Taneath":
					elif sName == localText.getText('TXT_KEY_UNIT_ARTIST_5', ()):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUMMONER'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUNDERED'), True)
						unit.setReligion(iCoven)
##					elif sName == "Samawen the Ghost":
					elif sName == localText.getText('TXT_KEY_UNIT_ARTIST_8', ()):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STEALTH'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GREY'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOW1'), True)


##					elif sName == "Gwenhwyfar the Swanmay":
					elif sName == localText.getText('TXT_KEY_UNIT_ARTIST_24', ()):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_ELF'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EVANGELIST'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL'), True)
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUBDUE_BEASTS'), True)
						unit.setReligion(iLeaves)

				else:
					if iUnit == gc.getInfoTypeForString('UNIT_GREAT_GENERAL'):

	##					elif sName == "Captain Ostanes":
						if sName == localText.getText('TXT_KEY_UNIT_COMMANDER_1', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDO'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HORSELORD'), True)
							unit.setReligion(iStewards)
	##					elif sName == "Captain Uldanor":
						elif sName == localText.getText('TXT_KEY_UNIT_COMMANDER_2', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HORSELORD'), True)
							unit.setReligion(iFoxmen)

	##					elif sName == "Goroff Grist":
						elif sName == localText.getText('TXT_KEY_UNIT_COMMANDER_5', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_INQUISITOR'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_VALOR'), True)
							unit.setReligion(iOrder)
	##					elif sName == "Haerlond Gossam":
						elif sName == localText.getText('TXT_KEY_UNIT_COMMANDER_6', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_ELF'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BLIND'), True)

	##					if sName == "Mikel Alaunus":
						elif sName == localText.getText('TXT_KEY_UNIT_COMMANDER_10', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UNDEAD'), True)
							unit.setReligion(iEmpyrean)

	##					elif sName == "Tethira":
						elif sName == localText.getText('TXT_KEY_UNIT_COMMANDER_11', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MAGIC_RESISTANCE'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_VALOR'), True)
	##					elif sName == "Palpeious":
						elif sName == localText.getText('TXT_KEY_UNIT_COMMANDER_12', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), True)

	##					elif sName == "Rivanna the Wraith Lord":
						elif sName == localText.getText('TXT_KEY_UNIT_COMMANDER_13', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_ELF'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRE'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSIONIST'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUMMONER'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'), True)
							iEquipment = gc.getInfoTypeForString('EQUIPMENTCLASS_APHELION_AMULET')
							if gc.getGame().getUnitClassCreatedCount(iEquipment) == 0:
								gc.getGame().incrementUnitClassCreatedCount(iEquipment)
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_APHELION_AMULET'), True)

	##					elif sName == "David Allen Grossman":
						elif sName == localText.getText('TXT_KEY_UNIT_COMMANDER_22', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)
							unit.setReligion(iAnointed)
	##					elif sName == "Soloman Ka":
						elif sName == localText.getText('TXT_KEY_UNIT_COMMANDER_23', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_BODY'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PERFECT_SIGHT'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LOYALTY'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMUNE_DISEASE'), True)

	##					elif sName == "Arak the Erkling":
						elif sName == localText.getText('TXT_KEY_UNIT_COMMANDER_24', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ASPECT_OF_WAR'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PERFECT_SIGHT'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_INVISIBLE'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_ELF'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MARKSMAN'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CANNOT_CAST'), True)
							iEquipment = gc.getInfoTypeForString('EQUIPMENTCLASS_STARLIGHT_AMULET')
							if gc.getGame().getUnitClassCreatedCount(iEquipment) == 0:
								gc.getGame().incrementUnitClassCreatedCount(iEquipment)
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STARLIGHT_AMULET'), True)
							iEquipment = gc.getInfoTypeForString('EQUIPMENTCLASS_MIST')
							if gc.getGame().getUnitClassCreatedCount(iEquipment) == 0:
								gc.getGame().incrementUnitClassCreatedCount(iEquipment)
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIST'), True)
							iEquipment = gc.getInfoTypeForString('EQUIPMENTCLASS_RESOUNDING_SHIELD')
							if gc.getGame().getUnitClassCreatedCount(iEquipment) == 0:
								gc.getGame().incrementUnitClassCreatedCount(iEquipment)
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RESOUNDING_SHIELD'), True)

					elif iUnit == gc.getInfoTypeForString('UNIT_MERCHANT'):
	##					if sName == "Abdulkani the Mirage":
						if sName == localText.getText('TXT_KEY_UNIT_MERCHANT_4', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSIONIST'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STEALTH'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'), True)
							unit.setReligion(iEsus)

	##					elif sName == "Hamish Ovid the Candyman":
						elif sName == localText.getText('TXT_KEY_UNIT_MERCHANT_21', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DIVINE2'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_OCCISOR'), True)
							unit.setReligion(iAnointed)
					elif iUnit == gc.getInfoTypeForString('UNIT_PROPHET'):
	##					if sName == "Calwinna of Junil":
						if sName == localText.getText('TXT_KEY_UNIT_PROPHET_10', ()):
							unit.setHasPromotion(iDivine, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_LAW'), True)
							unit.setReligion(iOrder)
	##					elif sName == "Father Prespin":
						elif sName == localText.getText('TXT_KEY_UNIT_PROPHET_19', ()):
							unit.setHasPromotion(iDivine, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WINTERBORN'), True)
	##					elif sName == "Lanthis":
						elif sName == localText.getText('TXT_KEY_UNIT_PROPHET_16', ()):
							unit.setReligion(iEmpyrean)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PERFECT_SIGHT'), True)
	##					elif sName == "Lita the Witch":
						elif sName == localText.getText('TXT_KEY_UNIT_PROPHET_12', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_METAMAGIC'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ANGEL'), True)
							unit.setReligion(iLaeran)
	##					elif sName == "Nyarlat":
						elif sName == localText.getText('TXT_KEY_UNIT_PROPHET_7', ()):
							unit.setReligion(iUndertow)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHAOS1'), True)
	##					elif sName == "Pontif Elmin":
						elif sName == localText.getText('TXT_KEY_UNIT_PROPHET_17', ()):
							unit.setReligion(iOrder)
							unit.setHasPromotion(iDivine, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EXORCIST'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_VALOR'), True)
	##					elif sName == "Talia Gosam":
						elif sName == localText.getText('TXT_KEY_UNIT_PROPHET_11', ()):
							unit.setHasPromotion(iChanneling1, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ARCANE'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DIVINE'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NOMAD'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUBDUE_BEASTS'), True)
							unit.setReligion(iUnblemished)
	##					elif sName == "Vaghan of Lugus":
						elif sName == localText.getText('TXT_KEY_UNIT_PROPHET_20', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CROWN_OF_BRILLANCE'), True)
							unit.setHasPromotion(iDivine, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN2'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMUNE_DISEASE'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON_SLAYING'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MEDIC1'), True)
							unit.setReligion(iEmpyrean)
	##					elif sName == "Abnoba":
						elif sName == localText.getText('TXT_KEY_UNIT_PROPHET_14', ()):
							unit.setReligion(iVeil)
							unit.setHasPromotion(iDivine, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUMMONER'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUNDERED'), True)
							unit.setHasPromotion(iUnholyTaint, True)
	##					elif sName == "Cinnia":
						elif sName == localText.getText('TXT_KEY_UNIT_PROPHET_15', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)
							unit.setHasPromotion(iZeal, True)
							unit.setReligion(iUndertow)
	##					elif sName == "Oriol Peregrinus":
						elif sName == localText.getText('TXT_KEY_UNIT_PROPHET_21', ()):
							unit.setReligion(iEsus)
							unit.setHasPromotion(iDivine, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MEDIC1'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MEDIC2'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GUERILLA2'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOUNTAINEER'), True)

					elif iUnit == gc.getInfoTypeForString('UNIT_SCIENTIST'):
	##					if sName == "Bradeline":
						if sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_5', ()):
							unit.setHasPromotion(iChanneling1, True)
							unit.setHasPromotion(iUnholyTaint, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUMMONER'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EXTENSION1'), True)
	##					elif sName == "Luciaqua":
						elif sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_9', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELEMENTAL'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER'), True)
	##					elif sName == "Dentaro":
						elif sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_6', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT1'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT2'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT3'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT4'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT5'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WINTERBORN'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SCAVENGER'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_ENCHANTMENT'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING2'), True)
							unit.setReligion(iLaeran)
	##					elif sName == "Magister Cultuum":
						elif sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_20', ()):
							unit.setReligion(iLaeran)
							unit.setHasPromotion(iChanneling1, True)
							unit.setHasPromotion(iDivine, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MAGICALLY_LIBERAL'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MAGIC_IMMUNE'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_CREATION'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_METAMAGIC'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'), True)

	##					elif sName == "Magister Roth":
						elif sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_23', ()):
							unit.setReligion(iAnointed)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND2'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAW1'), True)

	##					elif sName == "Menolly NuValle":
						elif sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_8', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE'), True)
							unit.setHasPromotion(iZeal, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_VALOR'), True)
	##					elif sName == "Caer of Euphoria":
						elif sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_1', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ANGEL'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT3'), True)
	##					elif sName == "Tephus the Mistwalker":
						elif sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_4', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_METAMAGIC'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'), True)
							unit.setReligion(iLaeran)
	##					elif sName == "Thessalonica":
						elif sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_18', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HOMELAND'), True)
							unit.setHasPromotion(iZeal, True)
	##					elif sName == "Tya Kiri":
						elif sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_11', ()):
							unit.setHasPromotion(iChanneling1, True)
							unit.setHasPromotion(iChanneling2, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EXTENSION1'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELLSTAFF'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEALING_SALVE'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ARCANE'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT_GUIDE'), True)
	##					elif sName == "Asher the Encephalic":
						elif sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_14', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND'), True)
							unit.setHasPromotion(iChanneling2, True)
	##					elif sName == "Waldrun the Necromancer":
						elif sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_21', ()):
							unit.setHasPromotion(iChanneling2, True)
							unit.setHasPromotion(iChanneling1, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELLSTAFF'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_ELF'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BLIND'), True)

	##					elif sName == "Stolas the Dark":
						elif sName == localText.getText('TXT_KEY_UNIT_SCIENTIST_22', ()):
							unit.setReligion(iVeil)
							unit.setHasPromotion(iUnholyTaint, True)
							unit.setHasPromotion(iChanneling2, True)
							unit.setHasPromotion(iDivine, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRE'), True)


					elif iUnit == gc.getInfoTypeForString('UNIT_ENGINEER'):
	##					if sName == "Athos Ulthane":
						if sName == localText.getText('TXT_KEY_UNIT_ENGINEER_14', ()):
							unit.setReligion(iRunes)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HOMELAND'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTMENT2'), True)
	##					elif sName == "Khmer Otterfig":
						elif sName == localText.getText('TXT_KEY_UNIT_ENGINEER_1', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), True)
	##					elif sName == "Pistis Sophia":
						elif sName == localText.getText('TXT_KEY_UNIT_ENGINEER_18', ()):
							unit.setHasPromotion(iZeal, True)
							unit.setReligion(iBrotherhood)
	##					elif sName == "Valoel":
						elif sName == localText.getText('TXT_KEY_UNIT_ENGINEER_11', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HOMELAND'), True)
							unit.setHasPromotion(iZeal, True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON_SLAYING'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_LIFE'), True)
							unit.setReligion(iUnblemished)
	##					elif sName == "Techmage Errod":
						elif sName == localText.getText('TXT_KEY_UNIT_ENGINEER_21', ()):
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING1'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING2'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EXTENSION1'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_ENCHANTMENT'), True)
							unit.setReligion(iRinggiver)
		iRel = unit.getReligion()



		if iRel != -1:
			dGameOptionDisables = {
									iEmpyrean		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_0'),
									iBrotherhood	:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_1'),
									iRinggiver		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_2'),
									iUnblemished	:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_3'),
									iPlenty			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_4'),
									iOrder			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_5'),
									iMatronae		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_6'),
									iOne			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_7'),

									iEternalCabal	:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_8'),
									iLaeran			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_9'),
									iUndertow		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_10'),
									iGrey			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_11'),
									iRunes			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_12'),
									iLeaves			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_13'),
									iFoxmen			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_14'),
									iDragonCult		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_15'),

									iEsus			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_16'),
									iHand			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_17'),
									iStewards		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_18'),
									iDiscord		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_19'),
									iAnointed		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_20'),
									iVeil			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_21'),
									iLegion			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_22'),
									iCoven			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_23')
				}
			if iRel in dGameOptionDisables:
				iGameOption = dGameOptionDisables[iRel]
				if gc.getGame().isOption(iGameOption):
					unit.setReligion(-1)
					iRel = -1
			if iRel == iEmpyrean:
				if iCiv == iCalabim:
					unit.setHasPromotion(iRebel, True)
					unit.setHasPromotion(iLoyal, False)
			elif iRel == iRunes:
				if iStateReligion == iRel:
					if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_CIVILIAN'):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOUNTAINEER'), True)
			elif iRel == iDragonCult:
				if iUnit in [gc.getInfoTypeForString('UNIT_DISCIPLE_OF_ACHERON'), gc.getInfoTypeForString('UNIT_SON_OF_THE_INFERNO')]:
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), False)
			elif iRel == iDiscord:
				iNumWars = eTeam.getAtWarCount(False)
				if iNumWars < 1:
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LOYALTY'), False)
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REBEL'), True)
				elif pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD'):
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REBEL'), False)
					unit.changeFreePromotionPick(iNumWars)
					unit.setPromotionReady(True)
			elif iRel == iOne:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MAGIC_RESISTANCE'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SCOURGE'), True)
				if iStateReligion != -1:
					unit.setHasPromotion(iLoyal, False)
					unit.setHasPromotion(iRebel, True)
				if unit.isHasPromotion(iDivine):
					if unit.getUnitType() == gc.getInfoTypeForString('UNIT_LUONNOTAR'):
						unit.setHasPromotion(iDivine, False)
					else:
						CyInterface().addMessage(iPlayer, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_DEFROCK", (unit.getName(), )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, unit.getButton(), gc.getInfoTypeForString('COLOR_RED'), unit.getX(), unit.getY(), True, True)
						unit.kill(True, PlayerTypes.NO_PLAYER)


		if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_NAVAL'):
			if unit.isBarbarian():
				if pPlot.getImprovementType() in [gc.getInfoTypeForString('IMPROVEMENT_PIRATE_PORT'), gc.getInfoTypeForString('IMPROVEMENT_PIRATE_HARBOR'), gc.getInfoTypeForString('IMPROVEMENT_PIRATE_COVE')]:
					if pPlot.isOwned():
						iPlayerP = pPlot.getOwner()
						iDuration = pPlot.getUpgradeTimeLeft(pPlot.getImprovementType(),iPlayerP)
						unit.setDuration(iDuration)
						if iPlayerP == iPlayer:
							pPlayerP = gc.getPlayer(iPlayerP)
							if pPlayerP.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LANUN'):
								newUnit = pPlayerP.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.convert(unit)

		if iCiv == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
			if unit.isAlive():
				iXP = 0
				for iImprovement in xrange(gc.getNumImprovementInfos()):
					if gc.getImprovementInfo(iImprovement).isUnique():
						if pPlayer.getImprovementCount(iImprovement) > 0:
							iXP += 1
				iXP = CyGame().getSorenRandNum(iXP, "Elohim Unique Features")
				if iXP > 0:
					unit.changeExperience(iXP, -1, False, False, False)

		elif iCiv == iInfernal:
			if iUnitClass in [gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_VEIL'), gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_VEIL'), gc.getInfoTypeForString('UNITCLASS_BALOR')]:
				if pPlayer.getUnitClassCount(cf.getHero(pPlayer)) > 0:
					if iLeader == gc.getInfoTypeForString('LEADER_HYBOREM'):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_HYBOREM'), True)
					elif iLeader == gc.getInfoTypeForString('LEADER_JUDECCA'):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_JUDECCA'), True)
					elif iLeader == gc.getInfoTypeForString('LEADER_LETHE'):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_LETHE'), True)
					elif iLeader == gc.getInfoTypeForString('LEADER_MERESIN'):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_MERESIN'), True)
					elif iLeader == gc.getInfoTypeForString('LEADER_OUZZA'):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_OUZZA'), True)
					elif iLeader == gc.getInfoTypeForString('LEADER_SALLOS'):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_SALLOS'), True)
					elif iLeader == gc.getInfoTypeForString('LEADER_STATIUS'):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_STATIUS'), True)

			if unit.isAlive():
				if not isWorldUnitClass(unit.getUnitClassType()):
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POSSESSED'), True)
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EXORCIST'), False)
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BLESSED'), False)

		if iUnit in [	gc.getInfoTypeForString('UNIT_DEMAGOG'),
						gc.getInfoTypeForString('UNIT_PONTIF'),
						gc.getInfoTypeForString('UNIT_HERALD'),
						gc.getInfoTypeForString('UNIT_SOQED'),
						gc.getInfoTypeForString('UNIT_GREAT_GENERAL'),
						gc.getInfoTypeForString('UNIT_DONAL')
						]:
			unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RECRUITER'), True)

		if pCity != -1:
			if unit.isAlive():#I don't want Angels or especially Manes to be given living races. Statius's manes could return as manes when they die
				if not isWorldUnitClass(iUnitClass):
					if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_TOLERANT')):
						if iDefaultRace != -1 and iRace == iDefaultRace:
							if not isWorldUnitClass(unit.getUnitClassType()):
								jCult = pCity.calculateCulturePercent(iPlayer)
								if jCult < 100:
									unit.setHasPromotion(iDefaultRace, False)
									listRaces = [-1]
									for jPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
										jCult = pCity.calculateCulturePercent(jPlayer)
										if jCult > 0:
											pjPlayer = gc.getPlayer(jPlayer)
											jCiv = pjPlayer.getCivilizationType()
											jCivInfo = gc.getCivilizationInfo(jCiv)
											jRace = jCivInfo.getDefaultRace()
											for i in xrange(jCult):
												listRaces.append(jRace)
									iRace = listRaces.pop(CyGame().getSorenRandNum(len(listRaces), "Tolerant Trait Racial Selection "+unit.getName().encode('latin_1','replace')))
									if iRace != -1:
										unit.setHasPromotion(iRace, True)


					if infoUnit.getFreePromotions(gc.getInfoTypeForString('PROMOTION_VAMPIRE')):
						sName = unit.getNameNoDesc()
						if sName == '':
							sName = unit.getName()
						iTruncate = sName.find(", Thrall of ")
						if iTruncate != -1:
							sName = sName[:iTruncate]
							unit.setName(sName)

						pCity = pPlot.getPlotCity()
						sName += " von " + pCity.getName()
						unit.setName(sName)

						listMana = [
									(gc.getInfoTypeForString('BONUS_MANA_BODY'), gc.getInfoTypeForString('PROMOTION_BODY1'), gc.getInfoTypeForString('PROMOTION_BODY2'), gc.getInfoTypeForString('PROMOTION_BODY3'), gc.getInfoTypeForString('PROMOTION_AFFINITY_BODY')),
									(gc.getInfoTypeForString('BONUS_MANA_DEATH'), gc.getInfoTypeForString('PROMOTION_DEATH1'), gc.getInfoTypeForString('PROMOTION_DEATH2'), gc.getInfoTypeForString('PROMOTION_DEATH3'), gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH')),
									(gc.getInfoTypeForString('BONUS_MANA_MIND'), gc.getInfoTypeForString('PROMOTION_MIND1'), gc.getInfoTypeForString('PROMOTION_MIND2'), gc.getInfoTypeForString('PROMOTION_MIND3'), gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND')),
									(gc.getInfoTypeForString('BONUS_MANA_SHADOW'), gc.getInfoTypeForString('PROMOTION_SHADOW1'), gc.getInfoTypeForString('PROMOTION_SHADOW2'), gc.getInfoTypeForString('PROMOTION_SHADOW3'), gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'))
##									(gc.getInfoTypeForString('BONUS_MANA_SPIRIT'), gc.getInfoTypeForString('PROMOTION_SPIRIT1'), gc.getInfoTypeForString('PROMOTION_SPIRIT2'), gc.getInfoTypeForString('PROMOTION_SPIRIT3'), gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT'))
							]
						for iMana, iSpell1, iSpell2, iSpell3, iAffinity in listMana:
							iLiegeMana = CyGame().getSorenRandNum(pCity.getNumBonuses(iMana) + cf.getNumBonusEffective(iPlayer, iMana, unit), "Vampire Governor's vassal mana")/2
							if iLiegeMana > 1:
								if gc.getPromotionInfo(iSpell1).getUnitCombat(iUnitCombat) and not unit.isPromotionImmune(iSpell1):
									unit.setHasPromotion(iSpell1, True)
									self.onUnitPromoted([unit, iSpell1])
								if iLiegeMana > 3:
									if gc.getPromotionInfo(iSpell2).getUnitCombat(iUnitCombat) and not unit.isPromotionImmune(iSpell2):
										unit.setHasPromotion(iSpell2, True)
										self.onUnitPromoted([unit, iSpell2])
									if iLiegeMana > 7:
										if infoUnit.getFreePromotions(iChanneling3):
											if gc.getPromotionInfo(iSpell3).getUnitCombat(iUnitCombat) and not unit.isPromotionImmune(iSpell3):
												unit.setHasPromotion(iSpell3, True)
												self.onUnitPromoted([unit, iSpell3])

			if iUnit == gc.getInfoTypeForString('UNIT_SETTLER'):
				if gc.getPlayer(pCity.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')):
					if pCity.getPopulation() > 1:
						pCity.changePopulation(-1)
			if iUnit == gc.getInfoTypeForString('UNIT_DEVOUT'):

				if not PyHelpers.PyGame().doesBuildingExist(gc.getInfoTypeForString('BUILDING_CRUCIBLE')):

					iImprovement = pPlot.getImprovementType()

					if iImprovement == -1:
	##					lImprovements = range(gc.getNumImprovementInfos())
						lImprovements = [gc.getInfoTypeForString('IMPROVEMENT_PALUS'),gc.getInfoTypeForString('IMPROVEMENT_PYRE_OF_THE_SERAPHIC'),gc.getInfoTypeForString('IMPROVEMENT_MAELSTROM'),gc.getInfoTypeForString('IMPROVEMENT_TARCHS_TOWER'), gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER'), gc.getInfoTypeForString('IMPROVEMENT_GUARDIAN'),gc.getInfoTypeForString('IMPROVEMENT_POOL_OF_TEARS'), gc.getInfoTypeForString('IMPROVEMENT_REMNANTS_OF_PATRIA'), gc.getInfoTypeForString('IMPROVEMENT_TOMB_OF_SUCELLUS'), gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES'), gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES'),gc.getInfoTypeForString('IMPROVEMENT_RING_OF_CARCER'),gc.getInfoTypeForString('IMPROVEMENT_MIRROR_OF_HEAVEN'), gc.getInfoTypeForString('IMPROVEMENT_STANDING_STONES'), gc.getInfoTypeForString('IMPROVEMENT_ODIOS_PRISON'), gc.getInfoTypeForString('IMPROVEMENT_YGGDRASIL'),gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE'),gc.getInfoTypeForString('IMPROVEMENT_WHISPERING_WOOD'),gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL'),gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS'),gc.getInfoTypeForString('IMPROVEMENT_GRAVE_OF_ASMODAY'),gc.getInfoTypeForString('IMPROVEMENT_WODES_OAK'),gc.getInfoTypeForString('IMPROVEMENT_HERVES_MAUSOLEUM'),gc.getInfoTypeForString('IMPROVEMENT_TAPESTRY_HOUSE'), gc.getInfoTypeForString('IMPROVEMENT_CARNIVEANS_CRAG'), gc.getInfoTypeForString('IMPROVEMENT_TEMPLE_OF_ATONEMENT')]
						while len(lImprovements) > 0:
							iImprovement = lImprovements.pop(CyGame().getSorenRandNum(len(lImprovements), "Pilgrimage-Destination for "+ unit.getName().encode('latin_1','replace')))
							if iImprovement == -1:
								continue
	##						if not gc.getImprovementInfo(iImprovement).isUnique():
	##							continue
							if cf.getNumTeamImprovements(pPlayer, iImprovement) > 0:
								break
							iImprovement = -1

					if iImprovement != -1:

						bApply = False

						if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_PALUS'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_SENTRY')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SENTRY'), True)
								bApply = True
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND2'), True)
								bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_PYRE_OF_THE_SERAPHIC'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_IMMUNE_FIRE')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMUNE_FIRE'), True)
								bApply = True
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE1'), True)
								bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_MAELSTROM'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_AIR')):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AIR1')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR1'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_TARCHS_TOWER'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_AIR')):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AIR2')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR2'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER'):
							if gc.getPlayer(unit.getOwner()).getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'), True)
									bApply = True
							elif not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_UNDEAD_SLAYING')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UNDEAD_SLAYING'), True)
								bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_GUARDIAN'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_GOLEM_SLAYING')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GOLEM_SLAYING'), True)
								bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_POOL_OF_TEARS'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT')):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_SPIRIT2')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT2'), True)
									bApply = True
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_MEDIC1')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MEDIC1'), True)
								bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_REMNANTS_OF_PATRIA'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_METAMAGIC')):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_METAMAGIC2')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC2'), True)
									bApply = True
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_MAGIC_RESISTANCE')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MAGIC_RESISTANCE'), True)
								bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_TOMB_OF_SUCELLUS'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_LIFE')):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_LIFE2')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LIFE2'), True)
									bApply = True
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_MEDIC2')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MEDIC2'), True)
								bApply = True


						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES'):
							if iRel == gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON'):
								if not unit.isPromotionImmune(iZeal):
									unit.setHasPromotion(iZeal, True)
									bApply = True
							elif not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_DRAGON_SLAYING')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRAGON_SLAYING'), True)
								bApply = True

							iBonus = pPlot.getBonusType(-1)
							if iBonus == gc.getInfoTypeForString('BONUS_MANA_WATER'):

								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER')):
									if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_WATER1')):
										unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1'), True)
										bApply = True

							if iBonus == gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL')):
									if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_DIMENSIONAL1')):
										unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DIMENSIONAL1'), True)
										bApply = True
							if iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE')):
									if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_FIRE2')):
										unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE2'), True)
										bApply = True
							if iBonus == gc.getInfoTypeForString('BONUS_MANA_ICE'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_ICE')):
									if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_ICE1')):
										unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ICE1'), True)
										bApply = True
							if iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_CREATION')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_CREATION'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_FORCE')):
								if iRel == gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE'):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_FORCE'), True)
									bApply = True
								elif not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_FORCE1')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FORCE1'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_CARCER'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_COURAGE')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COURAGE'), True)
								bApply = True
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_VALOR')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_VALOR'), True)
								bApply = True
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_LOYALTY')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LOYALTY'), True)
								bApply = True
							if iRel == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_MIRROR_OF_HEAVEN'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_PERFECT_SIGHT')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PERFECT_SIGHT'), True)
								bApply = True
							if iRel == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_STANDING_STONES'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_EARTH')):
								if iRel == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_EARTH'), True)
									bApply = True
								elif not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_EARTH1')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EARTH1'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_ODIOS_PRISON'):
							if iRel == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_EARTH')):
									if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_EARTH2')):
										unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EARTH2'), True)
										bApply = True
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_BODY')):
									if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_BODY2')):
										unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BODY2'), True)
										bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_YGGDRASIL'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE')):
								if iRel == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE'), True)
									bApply = True
								elif not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_NATURE2')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NATURE2'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER')):
								if iRel == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER'), True)
									bApply = True
								elif not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_WATER1')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WHISPERING_WOOD'):
							if iRel == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL'):
							if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH')):
									if iRel == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
										unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'), True)
										bApply = True
									else:
										unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH1'), True)
										bApply = True
							elif pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN')):
									if iRel != gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
										unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'), True)
										bApply = True
									elif not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1')):
										unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1'), True)
										bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_IMMUNE_COLD')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMUNE_COLD'), True)
								bApply = True
							if iRel == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_IMMUNE_COLD')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMUNE_COLD'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_GRAVE_OF_ASMODAY'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_ENTROPY1')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENTROPY1'), True)
								bApply = True
							if iRel == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_UNHOLY_TAINT')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UNHOLY_TAINT'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WODES_OAK'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_SHADOW1')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOW1'), True)
								bApply = True
							if iRel == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_STEALTH')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STEALTH'), True)
									bApply = True
						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_HERVES_MAUSOLEUM'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL'), True)
								bApply = True
							if iRel == gc.getInfoTypeForString('RELIGION_FOXMEN'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_FAIR_WINDS')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FAIR_WINDS'), True)
									bApply = True

						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_TAPESTRY_HOUSE'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_SUMMONER')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUMMONER'), True)
								bApply = True
							if iRel == gc.getInfoTypeForString('RELIGION_COVEN'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_DIMENSIONAL1')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DIMENSIONAL1'), True)
									bApply = True
						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_CARNIVEANS_CRAG'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_CHAOS1')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHAOS1'), True)
								bApply = True
						elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_TEMPLE_OF_ATONEMENT'):
							if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_INQUISITOR')):
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_INQUISITOR'), True)
								bApply = True
							if iRel == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
								if not unit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_COMMAND1')):
									unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMAND1'), True)
									bApply = True



						if bApply:
							infoImp = gc.getImprovementInfo(iImprovement)
							sButton = infoImp.getButton()
							sImp = infoImp.getDescription()
							sName = unit.getName()
							iX = unit.getX()
							iY = unit.getY()
							CyInterface().addMessage(iPlayer, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MESSAGE_PILGRIMAGE", (sName, sImp)), 'AS2D_FEATUREGROWTH', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, ColorTypes(8),iX, iY, True, True)


			if iRace == gc.getInfoTypeForString('PROMOTION_DEMON'):
				if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')) > 0:
					unit.changeExperience(6, -1, False, False, False)

					iMana = gc.getUnitInfo(unit.getUnitType()).getPrereqAndBonus()
					if iMana != -1:
						iNum = cf.getNumSupplimentalMana(iPlayer, iMana, unit)
						if iNum > 0:
							unit.changeFreePromotionPick(iNum)

					if iUnit == gc.getInfoTypeForString('UNIT_BEAST_OF_AGARES'):
						if not gc.getPlayer(pCity.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')):
							if unit.canCast(gc.getInfoTypeForString('SPELL_BEAST_FEAST'), False):
								unit.cast(gc.getInfoTypeForString('SPELL_BEAST_FEAST'))


			elif iRace == gc.getInfoTypeForString('PROMOTION_GOLEM'):
				if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_ADULARIA_CHAMBER')) > 0:
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STEALTH'), True)
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN'), True)
				if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_BLASTING_WORKSHOP')) > 0:
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE2'), True)
				if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_DWARVEN_SMITHY')) > 0:
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), True)
				if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_GOLEM_TRACKS')) > 0:
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOBILITY2'), True)
				if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_PALLENS_ENGINE')) > 0:
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PERFECT_SIGHT'), True)
				if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TOWER_OF_ALTERATION')) > 0:
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), True)


			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_RIDE_OF_THE_NINE_KINGS')) > 0:
				if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_MOUNTED'):
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WARCRY'), True)

			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TOWER_OF_MASTERY')) > 0:
				if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_ADEPT'):
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MASTERY'), True)

			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TOMB_OF_ARAWN')) > 0:
				bDeathA = unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH')) or unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'))
				bDeath1 = unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH1')) or unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1'))
				bDeath2 = unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH2')) or unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN2'))
				bDeath3 = unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH3')) or unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN3'))

				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'), False)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH1'), False)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH2'), False)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH3'), False)

				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'), bDeathA)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1'), bDeath1)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN2'), bDeath2)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN3'), bDeath3)

			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_PLANAR_GATE')) > 0 or pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED')) > 0:
				if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_ADEPT') or unit.isHasPromotion(iUnholyTaint):
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EXTENSION1'), True)

			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_UNHARMED_MARTYRS')) > 0:
				if unit.isAlive():
					if not isWorldUnitClass(unit.getUnitClassType()):
						iReligion = iOne
						if iRel != iReligion:
							if CyGame().getSorenRandNum(33, "Martyr "+unit.getName().encode('latin_1','replace')) <= 7:
								unit.setReligion(iReligion)
								iRel = iReligion
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MAGIC_RESISTANCE'), True)
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SCOURGE'), True)


		#Eliminate Dragon bones when the dragons arise
		if infoUnit.getSpecialUnitType() == gc.getInfoTypeForString('SPECIALUNIT_DRAGON'):
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES'):
				if pPlot.getBonusType(-1) == infoUnit.getPrereqAndBonus():
					pPlot.setBonusType(-1)
					pPlot.setImprovementType(-1)


		if pPlot.getImprovementType() in [gc.getInfoTypeForString('IMPROVEMENT_BARROW'), gc.getInfoTypeForString('IMPROVEMENT_GRAVEYARD'), gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL'),gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS')]:
			if iUnit == gc.getInfoTypeForString('UNIT_SLUAGH'):

				iLevel =1+CyGame().getSorenRandNum(7, "Grave Sluagh level "+unit.getName().encode('latin_1','replace'))
				unit.setLevel(iLevel)
				iExperience = unit.experienceNeeded() - CyGame().getSorenRandNum(iLevel, "Grave Sluagh experience " + unit.getName().encode('latin_1','replace'))
				unit.setExperience(iExperience, -1)


				listRaces = []
				if pPlot.isOwned():
					pjPlayer = gc.getPlayer(pPlot.getOwner())
					iCiv = pjPlayer.getCivilizationType()
					iCivInfo = gc.getCivilizationInfo(iCiv)
					iRace = iCivInfo.getDefaultRace()
					listRaces.append(iRace)

				lSluagh = [
							gc.getInfoTypeForString('UNIT_WORKER'),
							gc.getInfoTypeForString('UNIT_WARRIOR'),
							gc.getInfoTypeForString('UNIT_WARRIOR'),
							gc.getInfoTypeForString('UNIT_BLOODPET'),
							gc.getInfoTypeForString('UNIT_SCOUT'),
							gc.getInfoTypeForString('UNIT_SCOUT'),
							gc.getInfoTypeForString('UNIT_HORSEMAN'),
							gc.getInfoTypeForString('UNIT_HORSEMAN'),
							gc.getInfoTypeForString('UNIT_CHARIOT'),
							gc.getInfoTypeForString('UNIT_HUNTER'),
							gc.getInfoTypeForString('UNIT_HUNTER'),
							gc.getInfoTypeForString('UNIT_ASSASSIN'),
							gc.getInfoTypeForString('UNIT_ASSASSIN'),
							gc.getInfoTypeForString('UNIT_RANGER'),
							gc.getInfoTypeForString('UNIT_AXEMAN'),
							gc.getInfoTypeForString('UNIT_AXEMAN'),
							gc.getInfoTypeForString('UNIT_SWORDSMAN'),
							gc.getInfoTypeForString('UNIT_SWORDSMAN'),
							gc.getInfoTypeForString('UNIT_CHAMPION'),
							gc.getInfoTypeForString('UNIT_DRAGON_SLAYER'),
							gc.getInfoTypeForString('UNIT_BATTLEMASTER'),
							gc.getInfoTypeForString('UNIT_ARCHER'),
							gc.getInfoTypeForString('UNIT_ARCHER'),
							gc.getInfoTypeForString('UNIT_ARCHER'),
							gc.getInfoTypeForString('UNIT_LONGBOWMAN'),
							gc.getInfoTypeForString('UNIT_CROSSBOWMAN'),
							gc.getInfoTypeForString('UNIT_CROSSBOWMAN'),
							gc.getInfoTypeForString('UNIT_ADEPT'),
							gc.getInfoTypeForString('UNIT_MAGE')
							]
				pCity = CyMap().findCity(iX, iY, PlayerTypes.NO_PLAYER, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, pPlayer.getCity(-1))
				if pCity != -1:
					iConscript = pCity.getConscriptUnit()
					if iConscript != -1:
						for i in range(3):
							lSluagh.append(pCity.getConscriptUnit())
					lReligions = [-1,-1]
					for iR in xrange(gc.getNumReligionInfos()):
						if pCity.isHasReligion(iR):
							lReligions.append(iR)
							if pCity.isHolyCityByType(iR):
								lReligions.append(iR)
					unit.setReligion(lReligions.pop(CyGame().getSorenRandNum(len(lReligions), "Grave Religion")))

					jPlayer = pCity.getOwner()
					if jPlayer != -1:
						pjPlayer = gc.getPlayer(jPlayer)
						jCiv = pjPlayer.getCivilizationType()
						jCivInfo = gc.getCivilizationInfo(jCiv)
						jRace = jCivInfo.getDefaultRace()
						listRaces.append(jRace)
						if pCity.calculateCulturePercent(jPlayer) < 100:
							for jPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
								jCult = pCity.calculateCulturePercent(jPlayer)//5
								if jCult > 0:
									pjPlayer = gc.getPlayer(jPlayer)
									jCiv = pjPlayer.getCivilizationType()
									jCivInfo = gc.getCivilizationInfo(jCiv)
									jRace = jCivInfo.getDefaultRace()
									for i in xrange(jCult):
										listRaces.append(jRace)
				if pPlot.isOwned():
					jPlayer = pPlot.getOwner()
					if jPlayer != -1:
						pjPlayer = gc.getPlayer(jPlayer)
						jCiv = pjPlayer.getCivilizationType()
						jCivInfo = gc.getCivilizationInfo(jCiv)
						jRace = jCivInfo.getDefaultRace()
						listRaces.append(jRace)
						if pPlot.calculateCulturePercent(jPlayer) < 100:
							for jPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
								jCult = pPlot.calculateCulturePercent(jPlayer)//5
								if jCult > 0:
									pjPlayer = gc.getPlayer(jPlayer)
									jCiv = pjPlayer.getCivilizationType()
									jCivInfo = gc.getCivilizationInfo(jCiv)
									jRace = jCivInfo.getDefaultRace()
									for i in xrange(jCult):
										listRaces.append(jRace)


				if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS'):
					lSluagh = [gc.getInfoTypeForString('UNIT_DISCIPLE_HAND'),gc.getInfoTypeForString('UNIT_PRIEST_OF_WINTER'),gc.getInfoTypeForString('UNIT_DISCIPLE_HAND'),gc.getInfoTypeForString('UNIT_PRIEST_OF_WINTER')]
					listRaces = [gc.getInfoTypeForString('PROMOTION_WINTERBORN')]
					unit.setReligion(gc.getInfoTypeForString('RELIGION_WHITE_HAND'))


				if len(listRaces) > 0:
					iRace = listRaces.pop(CyGame().getSorenRandNum(len(listRaces), "Grave Sluagh race"))
					if iRace != -1:
						unit.setHasPromotion(iRace, True)
				if len(lSluagh) > 0:
					iUnit = lSluagh.pop(CyGame().getSorenRandNum(len(lSluagh), "Grave of Whom"))
					unit.setScenarioCounter(iUnit)
					infoUnit = gc.getUnitInfo(iUnit)
					iUnitClass = infoUnit.getUnitClassType()
					iUnitCombat = infoUnit.getUnitCombatType()

					lGravePromotions = [gc.getInfoTypeForString('PROMOTION_WEAK'), gc.getInfoTypeForString('PROMOTION_STRONG'), gc.getInfoTypeForString('PROMOTION_RUSTED')]

					for iProm in xrange(gc.getNumPromotionInfos()):
##						if iProm in lGravePromotions:
##							continue
						infoProm = gc.getPromotionInfo(iProm)
						if infoUnit.getFreePromotions(iProm):
							continue
						if infoProm.getUnitCombat(iUnitCombat):
							if not -1 < infoProm.getMinLevel() < iLevel:
								continue
							if infoProm.getBonusPrereq() not in [-1, pPlot.getBonusType(-1)]:
								continue
							if infoProm.isRace():
								continue
							if infoProm.isEquipment():
								continue

							iPrereq = infoProm.getPrereqPromotion()
							if iPrereq != -1:
								infoProm = gc.getPromotionInfo(iPrereq)
								if infoUnit.getFreePromotions(iPrereq):
									continue
								if infoProm.getUnitCombat(iUnitCombat):
									if not -1 < infoProm.getMinLevel() < iLevel:
										continue
									if infoProm.getBonusPrereq() not in [-1, pPlot.getBonusType(-1)]:
										continue
									if infoProm.isRace():
										continue
									if infoProm.isEquipment():
										continue

									iPrereq2 = infoProm.getPrereqPromotion()
									if iPrereq2 != -1:
										infoProm = gc.getPromotionInfo(iPrereq2)
										if infoUnit.getFreePromotions(iPrereq2):
											continue
										if infoProm.getUnitCombat(iUnitCombat):
											if not -1 < infoProm.getMinLevel() < iLevel:
												continue
											if infoProm.getBonusPrereq() not in [-1, pPlot.getBonusType(-1)]:
												continue
											if infoProm.isRace():
												continue
											if infoProm.isEquipment():
												continue

											iPrereq3 = infoProm.getPrereqPromotion()
											if iPrereq3 != -1:
												infoProm = gc.getPromotionInfo(iPrereq3)
												if infoUnit.getFreePromotions(iPrereq3):
													continue
												if infoProm.getUnitCombat(iUnitCombat):
													if not -1 < infoProm.getMinLevel() < iLevel:
														continue
													if infoProm.getBonusPrereq() not in [-1, pPlot.getBonusType(-1)]:
														continue
													if infoProm.isRace():
														continue
													if infoProm.isEquipment():
														continue
												iPrereq4 = infoProm.getPrereqPromotion()
												if iPrereq4 != -1:
													infoProm = gc.getPromotionInfo(iPrereq4)
													if infoUnit.getFreePromotions(iPrereq4):
														continue
													if infoProm.getUnitCombat(iUnitCombat):
														if not -1 < infoProm.getMinLevel() < iLevel:
															continue
														if infoProm.getBonusPrereq() not in [-1, pPlot.getBonusType(-1)]:
															continue
														if infoProm.isRace():
															continue
														if infoProm.isEquipment():
															continue
														lGravePromotions.append(iPrereq4)
													lGravePromotions.append(iPrereq3)

											lGravePromotions.append(iPrereq2)


									lGravePromotions.append(iPrereq)

							iPrereq = infoProm.getPromotionPrereqAnd()
							if iPrereq != -1:
								infoProm = gc.getPromotionInfo(iPrereq)
								if infoUnit.getFreePromotions(iPrereq):
									continue
								if infoProm.getUnitCombat(iUnitCombat):
									if not -1 < infoProm.getMinLevel() < iLevel:
										continue
									if infoProm.getBonusPrereq() not in [-1, pPlot.getBonusType(-1)]:
										continue
									if infoProm.isRace():
										continue
									if infoProm.isEquipment():
										continue
									lGravePromotions.append(iPrereq)

							iPrereq = infoProm.getPrereqOrPromotion1()
							if iPrereq != -1:
								iProm = iPrereq
								infoProm = gc.getPromotionInfo(iPrereq)
								if infoUnit.getFreePromotions(iPrereq):
									continue
								if infoProm.getUnitCombat(iUnitCombat):
									if not -1 < infoProm.getMinLevel() < iLevel:
										continue
									if infoProm.getBonusPrereq() not in [-1, pPlot.getBonusType(-1)]:
										continue
									if infoProm.isRace():
										continue
									if infoProm.isEquipment():
										continue
									lGravePromotions.append(iPrereq)
							iPrereq = infoProm.getPrereqOrPromotion2()
							if iPrereq != -1:
								iProm = iPrereq
								infoProm = gc.getPromotionInfo(iPrereq)
								if infoUnit.getFreePromotions(iPrereq):
									continue
								if infoProm.getUnitCombat(iUnitCombat):
									if not -1 < infoProm.getMinLevel() < iLevel:
										continue
									if infoProm.getBonusPrereq() not in [-1, pPlot.getBonusType(-1)]:
										continue
									if infoProm.isRace():
										continue
									if infoProm.isEquipment():
										continue
									lGravePromotions.append(iPrereq)



							lGravePromotions.append(iProm)


					while iLevel > 1 and len(lGravePromotions) > 1:
						iGravePromotion = lGravePromotions.pop(CyGame().getSorenRandNum(len(lGravePromotions), "Grave Sluagh Promotion"))
						if iGravePromotion != -1:
							if unit.isHasPromotion(iGravePromotion):
								continue
							infoGraveProm = gc.getPromotionInfo(iGravePromotion)

							iPrereq = infoGraveProm.getPrereqPromotion()
							if iPrereq != -1:
								if not unit.isHasPromotion(iPrereq):
									if iPrereq in lGravePromotions:
										infoGraveProm = gc.getPromotionInfo(iPrereq)
										iPrereq2 = infoGraveProm.getPrereqPromotion()
										if iPrereq2 != -1:
											if not unit.isHasPromotion(iPrereq2):
												if iPrereq2 in lGravePromotions:
													infoGraveProm = gc.getPromotionInfo(iPrereq2)
													iPrereq3 = infoGraveProm.getPrereqPromotion()
													if iPrereq3 != -1:
														if not unit.isHasPromotion(iPrereq3):
															if iPrereq3 in lGravePromotions:
																infoGraveProm = gc.getPromotionInfo(iPrereq3)
																iPrereq4 = infoGraveProm.getPrereqPromotion()
																if iPrereq4 != -1:
																	if not unit.isHasPromotion(iPrereq4):
																		if iPrereq2 in lGravePromotions:
																			unit.setHasPromotion(iPrereq4, True)
																			iLevel -= 1
																		continue
																unit.setHasPromotion(iPrereq3, True)
																iLevel -= 1
															continue
													unit.setHasPromotion(iPrereq2, True)
													iLevel -= 1
												continue
										unit.setHasPromotion(iPrereq, True)
										iLevel -= 1
									continue
							iPrereq = infoGraveProm.getPromotionPrereqAnd()
							if iPrereq != -1:
								if not unit.isHasPromotion(iPrereq):
									if iPrereq in lGravePromotions:
										infoGraveProm = gc.getPromotionInfo(iPrereq)
										iPrereq2 = infoGraveProm.getPromotionPrereqAnd()
										if iPrereq2 != -1:
											if not unit.isHasPromotion(iPrereq2):
												if iPrereq2 in lGravePromotions:
													infoGraveProm = gc.getPromotionInfo(iPrereq2)
													iPrereq3 = infoGraveProm.getPromotionPrereqAnd()
													if iPrereq3 != -1:
														if not unit.isHasPromotion(iPrereq3):
															if iPrereq3 in lGravePromotions:
																infoGraveProm = gc.getPromotionInfo(iPrereq3)
																iPrereq4 = infoGraveProm.getPromotionPrereqAnd()
																if iPrereq4 != -1:
																	if not unit.isHasPromotion(iPrereq4):
																		if iPrereq2 in lGravePromotions:
																			unit.setHasPromotion(iPrereq4, True)
																			iLevel -= 1
																		continue
																unit.setHasPromotion(iPrereq3, True)
																iLevel -= 1
															continue
													unit.setHasPromotion(iPrereq2, True)
													iLevel -= 1
												continue
										unit.setHasPromotion(iPrereq, True)
										iLevel -= 1
									continue

							if iPrereq != -1:
								if not unit.isHasPromotion(iPrereq):
									if iPrereq in lGravePromotions:
										unit.setHasPromotion(iPrereq, True)
										iLevel -= 1
									continue
							iPrereq = infoGraveProm.getPrereqOrPromotion1()
							if iPrereq != -1:
								if not unit.isHasPromotion(iPrereq):
									if iPrereq in lGravePromotions:
										unit.setHasPromotion(iPrereq, True)
										iLevel -= 1
									continue
							unit.setHasPromotion(iGravePromotion, True)
							iLevel -= 1

				unit.setName(cf.MarnokNameGenerator(unit) + "'s Sluagh")
				unit.setDuration(CyGame().getSorenRandNum(21, "Grave Sluagh Duration "+unit.getName().encode('latin_1','replace')))

				if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_HALLOWED_GROUND'):
					if cf.getUnitAlignment(unit) == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
						unit.cast(gc.getInfoTypeForString('SPELL_PURGE_EVIL'))


			elif pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_HALLOWED_GROUND'):
				if pPlot.getTempFeatureTimer() > 0:
					if iUnit == gc.getInfoTypeForString('UNIT_TOMB_WARDEN'):
						iDuration = unit.getDuration()
						if iDuration < 0:
							iDuration = 1
						iDuration = 1 + CyGame().getSorenRandNum(1+iDuration, "Hallowed Ground")
						if unit.getRace() == gc.getInfoTypeForString('PROMOTION_DEMON'):
							iDuration *= -1
						pPlot.changeTempFeatureTimer(iDuration)


			elif iUnit in [gc.getInfoTypeForString('UNIT_SKELETON'),gc.getInfoTypeForString('UNIT_SPECTRE'),gc.getInfoTypeForString('UNIT_WRAITH')]:
				iSluagh = gc.getInfoTypeForString('UNIT_SLUAGH')
				lBoundProm = [	gc.getInfoTypeForString('PROMOTION_NETHERBIND'),
								gc.getInfoTypeForString('PROMOTION_CAPTUS_CAVEAE_ANGELORUM'),
								gc.getInfoTypeForString('PROMOTION_INCARCERATUS_JUDICII'),
								gc.getInfoTypeForString('PROMOTION_SOUL_FORGED'),
								gc.getInfoTypeForString('PROMOTION_ADVENTURER')
								]
				lSluagh = []
				for i in xrange(pPlot.getNumUnits(), -1, -1):
					pSluagh = pPlot.getUnit(i)
					if pSluagh.getUnitType() == iSluagh:
						if pSluagh.isDelayedDeath():
							continue
						for iProm in lBoundProm:
							if pSluagh.isHasPromotion(iProm):
								break
						else:
							iUnit = pSluagh.getScenarioCounter()
							if -1 < iUnit < gc.getNumUnitInfos():
								if isWorldUnitClass(gc.getUnitInfo(iUnit).getUnitClassType()):
									continue
								else:
									lSluagh.append(pSluagh)
				if len(lSluagh) > 0:
					pSluagh = lSluagh.pop(CyGame().getSorenRandNum(len(lSluagh), "Necromancy on Graveyard at X" +str(iX)+", Y " +str(iY)))
					iUnit = pSluagh.getScenarioCounter()
					sName = pSluagh.getNameNoDesc()[:pSluagh.getNameNoDesc().find("'s Sluagh")]
					unit.convert(pSluagh)
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), False)
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CANNOT_CAST'), False)
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MAGIC_IMMUNE'), False)
					unit.setName(sName)

					if unit.getScenarioCounter() == -1:
						unit.setScenarioCounter(iUnit)


		if CyGame().isReligionFounded(iMatronae):
			if unit.getReligion() not in [-1, iOne, iMatronae]:
				iGodlessPercent = CyGame().calculateReligionPercent(iMatronae) + CyGame().calculateReligionPercent(iOne)
				if iGodlessPercent > 0:
					if CyGame().getSorenRandNum(100, "Compact limits miracles") < iGodlessPercent:
						unit.setHasPromotion(iDivine, False)
						unit.setHasPromotion(iZeal, False)
						unit.setReligion(-1)
						iRel = -1

		if bCrucible:
			if not iUnit in [gc.getInfoTypeForString('UNIT_MORRIGAN'), gc.getInfoTypeForString('UNIT_CLIODNA'), gc.getInfoTypeForString('UNIT_SARABRIDE')]:

				if iRace in [	gc.getInfoTypeForString('PROMOTION_ANGEL'),
								gc.getInfoTypeForString('PROMOTION_DEMON'),
								gc.getInfoTypeForString('PROMOTION_ELEMENTAL'),
								gc.getInfoTypeForString('PROMOTION_GOLEM'),
								gc.getInfoTypeForString('PROMOTION_ILLUSION'),
								gc.getInfoTypeForString('PROMOTION_UNDEAD')
								]:
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), False)
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)

				unit.setHasPromotion(iUnholyTaint, False)
				if not unit.isHasPromotion(iChanneling2):
					unit.setHasPromotion(iChanneling1, False)
				if not unit.isHasPromotion(iChanneling3):
					unit.setHasPromotion(iChanneling2, False)

		else:
			if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_DISCIPLE') and iRel == infoUnit.getPrereqReligion():
				if unit.isHasPromotion(iDivine):
					if unit.canCast(gc.getInfoTypeForString('SPELL_ADJUST_ARDA'), False):
						pass
				if unit.getDuration() == 0 and not isWorldUnitClass(iUnitClass) and not unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ARDA0')):
					if iRel != -1:
						listAffinities = []
						if iRel == iOrder:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_LAW')
											]
							if unit.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_BANNOR'):
								listAffinities.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE'))
						elif iRel == iEmpyrean:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN')
											]
						elif iRel == iRunes:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_EARTH')
											]
						elif iRel == iLeaves:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE')
											]
						elif iRel == iUndertow:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER'),
											gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND')
											]
						elif iRel == iEsus:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'),
											]
						elif iRel == iVeil:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY')
											]
						elif iRel == iHand:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_ICE')
											]
						elif iRel == iUnblemished:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_LIFE'),
											gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE')
											]
						elif iRel == iBrotherhood:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT')
											]
						elif iRel == iLaeran:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_METAMAGIC')
											]
						elif iRel == iFoxmen:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_AIR')
											]
						elif iRel == iStewards:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND')
											]
						elif iRel == iCoven:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL')
											]
						elif iRel == iAnointed:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_BODY')
											]
						elif iRel == iOne:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_FORCE')
											]
						elif iRel == iPlenty:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_CREATION')
											]
						elif iRel == iRinggiver:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_ENCHANTMENT')
											]
						elif iRel == iEternalCabal:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN')
											]
						elif iRel == iGrey:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_FORCE')
											]
						elif iRel == iLegion:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE')
											]
						elif iRel == iDiscord:
							listAffinities = [
											gc.getInfoTypeForString('PROMOTION_AFFINITY_CHAOS')
											]

						if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')):
							if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DEATH_MANA')):
								if gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH') in listAffinities:
									listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'))
								if gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN') in listAffinities:
									listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'))
							if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_ENTROPY_MANA')):
								if gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY') in listAffinities:
									listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY'))
							if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_SHADOW_MANA')):
								if gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW') in listAffinities:
									listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'))
							if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DIMENSIONAL_MANA')):
								if gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL') in listAffinities:
									listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL'))
							if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_CHAOS_MANA')):
								if gc.getInfoTypeForString('PROMOTION_AFFINITY_CHAOS') in listAffinities:
									listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_CHAOS'))
						elif pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')):
							if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_SUN_MANA')):
								if gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN') in listAffinities:
									listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'))
						for iAffinity in listAffinities:
							if unit.isHasPromotion(iAffinity) or unit.isPromotionImmune(iAffinity):
								listAffinities.remove(iAffinity)
						if len(listAffinities) > 0:
							listArdas =[
											gc.getInfoTypeForString('PROMOTION_ARDA0'),
											gc.getInfoTypeForString('PROMOTION_ARDA1'),
											gc.getInfoTypeForString('PROMOTION_ARDA2'),
											gc.getInfoTypeForString('PROMOTION_ARDA3'),
											gc.getInfoTypeForString('PROMOTION_ARDA4'),
											gc.getInfoTypeForString('PROMOTION_ARDA5'),
											gc.getInfoTypeForString('PROMOTION_ARDA6'),
											gc.getInfoTypeForString('PROMOTION_ARDA7'),
											gc.getInfoTypeForString('PROMOTION_ARDA8'),
											gc.getInfoTypeForString('PROMOTION_ARDA9'),
											gc.getInfoTypeForString('PROMOTION_ARDA10')
										]
							iArdaIndex = 4
							for iArdaIndex in range(len(listArdas)):
								if unit.isHasPromotion(listArdas[iArdaIndex]):
									break
							else:
								iArdaIndex = 4
							listAffinities = list(set(listAffinities))
							iAffinity = listAffinities[0]
							if len(listAffinities) > 1:
								iAffinity = listAffinities[CyGame().getSorenRandNum(len(listAffinities), "Religious Affinity type for " +unit.getName().encode('latin_1','replace'))]

							iMana = gc.getPromotionInfo(iAffinity).getBonusPrereq()
							if iMana != -1:
								iNumMana = cf.getNumBonusEffective(iPlayer, iMana, unit)
								if iNumMana > 1:
									iMaxOdds = 2000/iArdaIndex + pPlayer.getUnitClassCount(iUnitClass)
									if unit.isHasPromotion(iZeal):
										iMaxOdds /= 2
									if infoUnit.getFreePromotions(iDivine):
										iMaxOdds /= 15
										if infoUnit.getFreePromotions(iDivine2):
											iMaxOdds /= 10
									if CyGame().getSorenRandNum(iMaxOdds, "Religion Affinity - "+unit.getName().encode('latin_1','replace')) < iNumMana:
										unit.setHasPromotion(iAffinity, True)


			elif iUnit in [ gc.getInfoTypeForString('UNIT_RADIANT_GUARD'), gc.getInfoTypeForString('UNIT_RATHA')]:
				iNumMana = cf.getNumBonusEffective(iPlayer, gc.getInfoTypeForString('BONUS_MANA_SUN'), unit)
				if iNumMana > 1:
					iMaxOdds = 500 + pPlayer.getUnitClassCount(iUnitClass)
					if unit.isHasPromotion( iZeal):
						iMaxOdds /= 2
					if CyGame().getSorenRandNum(iMaxOdds, "Radiant Guard Affinity - "+unit.getName().encode('latin_1','replace')) < iNumMana:
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'), True)


			elif iUnit == gc.getInfoTypeForString('UNIT_ASMODAY'):
				iMask = gc.getInfoTypeForString('EQUIPMENT_MASK_ASMODAY')
				iRange =2
				for iiX in xrange(iX-iRange, iX+1+iRange, 1):
					for iiY in xrange(iY-iRange, iY+1+iRange, 1):
						pLoopPlot = CyMap().plot(iiX,iiY)
						for iLoopUnit in xrange(pPlot.getNumUnits()):
							loopUnit = pLoopPlot.getUnit(iLoopUnit)
							if loopUnit.getUnitType() == iMask:
								loopUnit.kill(True, iPlayer)
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MASK_OF_ESUS'), True)
								break
			elif iUnit == gc.getInfoTypeForString('UNIT_BARBATOS'):
				iMask = gc.getInfoTypeForString('EQUIPMENT_MASK_BARBATOS')
				iRange =2
				for iiX in xrange(iX-iRange, iX+1+iRange, 1):
					for iiY in xrange(iY-iRange, iY+1+iRange, 1):
						pLoopPlot = CyMap().plot(iiX,iiY)
						for iLoopUnit in xrange(pPlot.getNumUnits()):
							loopUnit = pLoopPlot.getUnit(iLoopUnit)
							if loopUnit.getUnitType() == iMask:
								loopUnit.kill(True, iPlayer)
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MASK_OF_ESUS'), True)
								break
			elif iUnit == gc.getInfoTypeForString('UNIT_WODE'):
				iMask = gc.getInfoTypeForString('EQUIPMENT_MASK_ALEXIS')
				iRange =2
				for iiX in xrange(iX-iRange, iX+1+iRange, 1):
					for iiY in xrange(iY-iRange, iY+1+iRange, 1):
						pLoopPlot = CyMap().plot(iiX,iiY)
						for iLoopUnit in xrange(pPlot.getNumUnits()):
							loopUnit = pLoopPlot.getUnit(iLoopUnit)
							if loopUnit.getUnitType() == iMask:
								loopUnit.kill(True, iPlayer)
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MASK_OF_ESUS'), True)
								break


			elif iUnit in [ gc.getInfoTypeForString('UNIT_ANGEL_OF_DEATH'), gc.getInfoTypeForString('UNIT_TOMB_WARDEN')]:
				iNumMana = cf.getNumBonusEffective(iPlayer, gc.getInfoTypeForString('BONUS_MANA_DEATH'), unit)
				if iNumMana > 1:
					iMaxOdds = 500 + pPlayer.getUnitClassCount(iUnitClass)
					if unit.isHasPromotion( iZeal):
						iMaxOdds /= 2
					if CyGame().getSorenRandNum(iMaxOdds, "Angel of Death Affinity - "+unit.getName().encode('latin_1','replace')) < iNumMana:
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'), True)


			elif iUnit == gc.getInfoTypeForString('UNIT_DISCIPLE_OF_ACHERON'):
				iNumMana = CyGame().getSorenRandNum(cf.getNumBonusEffective(iPlayer, gc.getInfoTypeForString('BONUS_MANA_FIRE'), unit), "Bhall Orc Affinity- "+unit.getName().encode('latin_1','replace'))
				if iNumMana > 1:
					iMaxOdds = 500 + pPlayer.getUnitClassCount(iUnitClass)
					if unit.isHasPromotion( iZeal):
						iMaxOdds /= 2
					if pCity != -1:
						if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_ETERNAL_FLAME')) > 0:
							iMaxOdds /= 2
					if pCity != -1:
						if CyGame().getSorenRandNum(iMaxOdds, "Disciple of Acheron- "+unit.getName().encode('latin_1','replace')) < iNumMana:
							unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE'), True)



			elif iUnit in [ gc.getInfoTypeForString('UNIT_BALOR'), gc.getInfoTypeForString('UNIT_DRAGON_PIT')]:


				listWeightedAffinities = []

				listAffinities = [	gc.getInfoTypeForString('PROMOTION_AFFINITY_AIR'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_BODY'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_CHAOS'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_CREATION'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_EARTH'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_ENCHANTMENT'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_FORCE'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_ICE'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_LAW'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_METAMAGIC'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER')
									]

				for iAffinity in listAffinities:
					infoAffinity = gc.getPromotionInfo(iAffinity)
					iMana = infoAffinity.getBonusPrereq()
					for i in range(cf.getNumBonusEffective(iPlayer, iMana, unit)):
						listWeightedAffinities.append(iAffinity)

				if len(listWeightedAffinities) > 0:
					iAffinity = listWeightedAffinities.pop(CyGame().getSorenRandNum(len(listWeightedAffinities), "Affinity-Balor-"+ str(unit.getID()) ) )
					unit.setHasPromotion(iAffinity, True)
					self.onUnitPromoted([unit, iAffinity])

				if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE')):
					unit.setReligion(iLegion)
				elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL')):
					unit.setReligion(iCoven)
				elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_BODY')):
					unit.setReligion(iAnointed)
				elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_CHAOS')):
					unit.setReligion(iDiscord)
				elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND')):
					unit.setReligion(iStewards)
				elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_ICE')):
					unit.setReligion(iHand)
				elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW')):
					unit.setReligion(iEsus)
				elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER')):
					unit.setReligion(iUndertow)

				if iCiv == iInfernal:
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BOUND_BY_COMPACT'), True)
				elif unit.isBarbarian():
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BOUND_BY_COMPACT'), True)
					if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE'):
						iDuration = cf.getNumBonusEffective(iPlayer, gc.getInfoTypeForString('BONUS_MANA_ENTROPY'))
						unit.setDuration(iDuration)
						if pPlot.isOwned():
							iPlayerP = pPlot.getOwner()
							if iPlayerP != iPlayer:
								pPlayerP = gc.getPlayer(iPlayerP)
								if pPlayerP.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
									newUnit = pPlayerP.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
									newUnit.convert(unit)

		if unit.getSpecialUnitType() == gc.getInfoTypeForString('SPECIALUNIT_DRAGON'):
			if unit.isBarbarian():
				if not isWorldUnitClass(iUnitClass):
					if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_STIR_FROM_SLUMBER')) > 0:
						if pPlot.isOwned():
							iPlayerP = pPlot.getOwner()
							if iPlayerP != iPlayer:
								pPlayerP = gc.getPlayer(iPlayerP)
								if pPlayerP.getStateReligion() == gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON'):
									info = gc.getUnitInfo(iUnit)
									if not pPlayerP.isUnitClassMaxedOut(iUnitClass, 0):
										iBonus = info.getPrereqAndBonus()
										if iBonus != -1:
											if cf.getNumBonusEffective(iPlayerP, iBonus, -1) > 1 + cf.getNumBonusEffective(iPlayer, iBonus, -1):
												if (pPlayerP.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD') and iUnit in [	gc.getInfoTypeForString('UNIT_DRAGON_CORAL'), gc.getInfoTypeForString('UNIT_DRAGON_DAWN'), gc.getInfoTypeForString('UNIT_DRAGON_GOLD'), gc.getInfoTypeForString('UNIT_DRAGON_RUNE'), gc.getInfoTypeForString('UNIT_DRAGON_SHIELD'), gc.getInfoTypeForString('UNIT_DRAGON_SHIMMERING')]) or (pPlayerP.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_NEUTRAL') and iUnit in [	gc.getInfoTypeForString('UNIT_DRAGON_ELDER'), gc.getInfoTypeForString('UNIT_DRAGON_FANG'), gc.getInfoTypeForString('UNIT_DRAGON_FEATHERED'), gc.getInfoTypeForString('UNIT_DRAGON_GRAVE'), gc.getInfoTypeForString('UNIT_DRAGON_SCALED'), gc.getInfoTypeForString('UNIT_DRAGON_SEED'), gc.getInfoTypeForString('UNIT_DRAGON_SPIRE')]) or ( pPlayerP.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL') and iUnit in [	gc.getInfoTypeForString('UNIT_DRAGON_BLOOD'), gc.getInfoTypeForString('UNIT_DRAGON_FURNACE'), gc.getInfoTypeForString('UNIT_DRAGON_OBSIDIAN'), gc.getInfoTypeForString('UNIT_DRAGON_PIT'), gc.getInfoTypeForString('UNIT_DRAGON_SHADOW'), gc.getInfoTypeForString('UNIT_DRAGON_SIEGE'), gc.getInfoTypeForString('UNIT_VAULT_WYRM'), gc.getInfoTypeForString('UNIT_DRAGON_WINTER'), gc.getInfoTypeForString('UNIT_DRACOLICH')]):
													newUnit = pPlayerP.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
													newUnit.convert(unit)


		if iUnit == gc.getInfoTypeForString('UNIT_AUREALIS'):
			unit.setIgnoreHide(True)
			for iProm in [
							gc.getInfoTypeForString('PROMOTION_INVISIBLE'),
							gc.getInfoTypeForString('PROMOTION_HIDDEN'),
							gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'),
							gc.getInfoTypeForString('PROMOTION_STEALTH'),
							gc.getInfoTypeForString('PROMOTION_PARANOID'),
							gc.getInfoTypeForString('PROMOTION_BLUR'),
							gc.getInfoTypeForString('PROMOTION_SHADOWWALK'),
							gc.getInfoTypeForString('PROMOTION_BLIND')
							]:
				unit.setHasPromotion(iProm, False)


		elif iUnit == gc.getInfoTypeForString('UNIT_KRAKEN'):
			if unit.isBarbarian():
				if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE'):
					unit.setDuration(3)

					if pPlot.isOwned():
						iPlayerP = pPlot.getOwner()
						if iPlayerP != iPlayer:
							pPlayerP = gc.getPlayer(iPlayerP)
							if pPlayerP.getStateReligion() == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
								newUnit = pPlayerP.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.convert(unit)
								newUnit.setDuration(2)
							elif pPlayerP.getStateReligion() == gc.getInfoTypeForString('RELIGION_MATRONAE'):
								unit.kill(True, PlayerTypes.NO_PLAYER)
								return

		elif iUnit == gc.getInfoTypeForString('UNIT_RUNEWYN'):
			unit.setLevel(7)

		elif iUnit == gc.getInfoTypeForString('UNIT_AUTOMATON'):

			iBonus = pPlot.getBonusType(-1)
			if iBonus != -1:
				if gc.getBonusInfo(iBonus).isMana():
					lAdd = []
					lRemove = []
					if iBonus == gc.getInfoTypeForString('BONUS_MANA_AIR'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_AIR'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_BODY'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_BODY'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_CHAOS'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_CREATION'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH'):
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SIDAR') or pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL') or pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD') or (pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')) and CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DEATH_MANA'))):
							lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'))
						else:
							lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_EARTH'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_EARTH'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_ENCHANTMENT'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_ENCHANTMENT'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FORCE'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_FORCE'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ICE'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_ICE'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LAW'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_LAW'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_LIFE'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_METAMAGIC'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_MIND'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_NATURE'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SHADOW'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SUN'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'))
					elif iBonus == gc.getInfoTypeForString('BONUS_MANA_WATER'):
						lAdd.append(gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER'))
					for iProm in lAdd:
						infoAffinity = gc.getPromotionInfo(iProm)
						if infoAffinity != -1:
							iMana = infoAffinity.getBonusPrereq()
							if iMana != -1:
								unit.setHasPromotion(iProm, iMana == iBonus)


		elif iUnit == gc.getInfoTypeForString('UNIT_SETTLER'):
			if pPlayer.getNumCities() == 0:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STARTING_SETTLER'), True)

		elif iUnit == gc.getInfoTypeForString('UNIT_REFUGEE'):
			for iiX in xrange(iX-1, iX+2, 1):
				for iiY in xrange(iY-1, iY+2, 1):
					pLoopPlot = CyMap().plot(iiX,iiY)
					if not pLoopPlot.isNone():
						if pLoopPlot.isCity():
							pCityFleeing = pLoopPlot.getPlotCity()
							pCityFleeing.applyBuildEffects(unit)
							if iDefaultRace != -1 and unit.isHasPromotion(iDefaultRace):
								unit.setHasPromotion(iDefaultRace, False)
							listRaces = [	-1, -1	]
							jCult = pPlot.calculateCulturePercent(iPlayer)
							if jCult < 100:
								for jPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
									jCult = pPlot.calculateCulturePercent(jPlayer)
									if jCult > 0:
										pjPlayer = gc.getPlayer(jPlayer)
										jCiv = pjPlayer.getCivilizationType()
										jCivInfo = gc.getCivilizationInfo(jCiv)
										jRace = jCivInfo.getDefaultRace()
										for i in xrange(jCult):
											listRaces.append(jRace)
							listRaces = [-1]
							for jPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
								jCult = pPlot.calculateCulturePercent(jPlayer)
								if jCult > 0:
									pjPlayer = gc.getPlayer(jPlayer)
									jCiv = pjPlayer.getCivilizationType()
									jCivInfo = gc.getCivilizationInfo(jCiv)
									jRace = jCivInfo.getDefaultRace()
									for i in xrange(jCult):
										listRaces.append(jRace)
							if len(listRaces) > 0:
								iRace = listRaces.pop(CyGame().getSorenRandNum(len(listRaces), "Refugee Race"))
								if iRace != -1:
									unit.setHasPromotion(iRace, True)

							if pCityFleeing.getPopulation() > 1:
								pCityFleeing.changePopulation(-1)
								iCulture = pCityFleeing.getCulture(pCityFleeing.getOwner())
								iCulture /= pCityFleeing.getPopulation()
								iCulture /= 1 + pCityFleeing.getCultureLevel()
								# Note:
								# -1 = NO_CULTURELEVEL
								# 0 = CULTURELEVEL_NONE
								# 1 = CULTURELEVEL_POOR
								# 2 = CULTURELEVEL_FLEDGLING
								# 3 = CULTURELEVEL_DEVELOPING
								# 4 = CULTURELEVEL_REFINED
								# 5 = CULTURELEVEL_INFLUENTIAL
								# 6 = CULTURELEVEL_LEGENDARY

								#iCulture = CyGame().getSorenRandNum(pCityFleeing.getCulture(iCulture), "Refugee Culture")
								unit.changeExperience(iCulture, -1, False, False, False)
								unit.setPermanentSummon(False)
								unit.setSummoner(-1)
								pCityFleeing.changeCulture(pCityFleeing.getOwner(), -iCulture, True)

								for i in xrange(pPlot.getNumUnits()):
									loopUnit = pPlot.getUnit(i)
									if loopUnit.getOwner() == unit.getOwner():
										if loopUnit.cargoSpaceAvailable(gc.getInfoTypeForString('SPECIALUNIT_PEOPLE'), gc.getInfoTypeForString('DOMAIN_LAND')) > 0:
											unit.setTransportUnit(loopUnit)
											break


		elif iUnit == gc.getInfoTypeForString('UNIT_EARTH_ELEMENTAL'):
			if pPlot.isPeak():
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), False)
			elif pPlot.isHills():
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), False)

		elif iUnit in [gc.getInfoTypeForString('UNIT_TREANT'), gc.getInfoTypeForString('UNIT_GUARDIAN_VINES')]:
			iFeature = pPlot.getFeatureType()
			if iFeature == -1:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), False)
#				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)

			elif iFeature == gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE'), True)

			elif iFeature == gc.getInfoTypeForString('FEATURE_FOREST'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NATURE2'), True)
				if pPlot.getFeatureVariety() == 2: #SNOWY_CONIFEROUS_FOREST
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WINTERBORN'), True)

			elif iFeature == gc.getInfoTypeForString('FEATURE_FOREST_NEW'):
				pass#unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)

			elif iFeature == gc.getInfoTypeForString('FEATURE_JUNGLE'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AMPHIBIOUS'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISON_RESISTANCE'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NATURE1'), True)

			elif iFeature == gc.getInfoTypeForString('FEATURE_FOREST_BURNT'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_VULNERABLE_TO_FIRE'), False)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE_RESISTANCE'), True)

			elif iFeature == gc.getInfoTypeForString('FEATURE_SCRUB'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUN1'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NOMAD'), True)

			elif iFeature == gc.getInfoTypeForString('FEATURE_OASIS'):
				#unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NOMAD'), True)

			if pPlot.isWater():
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER_WALKING'), True)
			elif pPlot.isRiverSide():
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AMPHIBIOUS'), True)
			if pPlot.isHills():
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GUERILLA2'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GUERILLA1'), True)
			if pPlot.isPeak():
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GUERILLA2'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GUERILLA1'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOUNTAINEER'), True)

			iImprovement = pPlot.getImprovementType()
			if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_SMOKE'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENRAGED'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE1'), True)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_LUMBERMILL'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENRAGED'), True)
			elif iImprovement in [gc.getInfoTypeForString('IMPROVEMENT_YGGDRASIL'), gc.getInfoTypeForString('IMPROVEMENT_TOMB_OF_SUCELLUS')]:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_LIFE'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE'), True)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WODES_OAK'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSIONIST'), True)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WHISPERING_WOOD'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND2'), True)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_HERVES_MAUSOLEUM'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR2'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE'), True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL'), True)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_FORCE'), True)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BARROW'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UNDEAD_SLAYING'), True)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_CITY_RUINS'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER2'), True)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_RUINS'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER1'), True)
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_SHIP_WRECK'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BOARDING'), True)

		elif iUnit == gc.getInfoTypeForString('UNIT_WITCH_HUNTER'):
			for iTrait in [	gc.getInfoTypeForString('TRAIT_ARCANE'),
							gc.getInfoTypeForString('TRAIT_SUMMONER'),
							gc.getInfoTypeForString('TRAIT_SUNDERED')
								]:
				if pPlayer.hasTrait(iTrait):
					unit.setHasPromotion(iRebel, True)
					unit.setHasPromotion(iLoyal, False)


				lPactEvents =[gc.getInfoTypeForString('EVENT_SUMMON_HYBOREM'), gc.getInfoTypeForString('EVENT_SUMMON_JUDECCA'), gc.getInfoTypeForString('EVENT_SUMMON_LETHE'), gc.getInfoTypeForString('EVENT_SUMMON_MERESIN'), gc.getInfoTypeForString('EVENT_SUMMON_OUZZA'), gc.getInfoTypeForString('EVENT_SUMMON_SALLOS'), gc.getInfoTypeForString('EVENT_SUMMON_STATIUS')]
				for iEvent in lPactEvents:
					if pPlayer.getEventOccured(iEvent):
						unit.setHasPromotion(iRebel, True)
						unit.setHasPromotion(iLoyal, False)
						break

				for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
					if iPlayer == iPlayer2:continue
					pPlayer2 = gc.getPlayer(iPlayer2)
					if pPlayer2.isAlive():
						if pPlayer2.getCivilizationType() == iInfernal:
							pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)
						else:
							for iEvent in lPactEvents:
								if pPlayer2.getEventOccured(iEvent):
									pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)


		if iCiv == iMercurians:
			if unit.canCast(gc.getInfoTypeForString('SPELL_PURGE_EVIL'), False):
				unit.cast(gc.getInfoTypeForString('SPELL_PURGE_EVIL'))


		if isWorldUnitClass(iUnitClass):
			for iEquipment in xrange(gc.getNumUnitInfos()):
				infoEquipment = gc.getUnitInfo(iEquipment)
				if infoEquipment.isObject():
					iProm = infoEquipment.getEquipmentPromotion()
					if -1 < iProm < gc.getNumPromotionInfos():
						if infoUnit.getFreePromotions(iProm):
							if CyGame().isUnitClassMaxedOut(infoEquipment.getUnitClassType(), 0):
								if not unit.isMechUnit():#Barnaxus should carry his own pieces at all times
									unit.setHasPromotion(iProm, False)


			iDark = gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION')
			iIllusion = gc.getInfoTypeForString('PROMOTION_ILLUSION')
			if unit.isHasPromotion(iDark) or unit.isHasPromotion(iIllusion) or unit.getDuration() != 0:
				if unit.isAvatarOfCivLeader():
					unit.setAvatarOfCivLeader(False)
			else:
				unit.setScenarioCounter(iUnit)
				iSluagh = gc.getInfoTypeForString('UNIT_SLUAGH')
				iHeld = gc.getInfoTypeForString('PROMOTION_HELD')
				lBoundProm = [	gc.getInfoTypeForString('PROMOTION_NETHERBIND'),
								gc.getInfoTypeForString('PROMOTION_CAPTUS_CAVEAE_ANGELORUM'),
								gc.getInfoTypeForString('PROMOTION_SOUL_FORGED')
								]

				for pSluagh in PyPlayer(gc.getBARBARIAN_PLAYER()).getUnitList():

					if pSluagh.getUnitType() == iSluagh:
						if pSluagh.getScenarioCounter() == iUnit:
							for iProm in lBoundProm:
								if pSluagh.isHasPromotion(iProm):
									break
							else:
								unit.convert(pSluagh)
								unit.setHasPromotion(iHeld, False)
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CANNOT_CAST'), False)
								unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MAGIC_IMMUNE'), False)
								unit.setScenarioCounter(iUnit)
								unit.setSummoner(-1)
								sName = pSluagh.getNameNoDesc()[:pSluagh.getNameNoDesc().find("'s Sluagh")]
								if sName != unit.getNameNoDesc() and sName != unit.getName():
									unit.setName(sName)
								break

				if iUnit == gc.getInfoTypeForString('UNIT_APOPHIS_SERPENT'):
					iGoat = gc.getInfoTypeForString('UNIT_APOPHIS')
					iApophisClass = gc.getInfoTypeForString('UNITCLASS_APOPHIS')
					if CyGame().getUnitCreatedCount(iGoat) > 0:
						for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
							if iPlayer2 != iPlayer:
								pPlayer2 = gc.getPlayer(iPlayer2)
								if pPlayer2.getUnitClassCount(iApophisClass) > 0:
									for pUnit in PyPlayer(iPlayer2).getUnitList():
										if pUnit.getUnitType() == iGoat:
											unit.convert(pSluagh)
											unit.setHasPromotion(iHeld, False)
											unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CANNOT_CAST'), False)
											unit.setScenarioCounter(iUnit)
											unit.setSummoner(-1)
											break

				#Set Avatar units for leaders, and restore traits in case of resurrection
				if infoUnit.isAbandon():

					dAvatars = {	gc.getInfoTypeForString('UNITCLASS_ORTHUS')		:	'LEADER_BARBARIAN',
									gc.getInfoTypeForString('UNITCLASS_BASIUM')		:	'LEADER_BASIUM',
									gc.getInfoTypeForString('UNITCLASS_AURIC')		:	'LEADER_AURIC',
									gc.getInfoTypeForString('UNITCLASS_ANAGANTIOS')	:	'LEADER_ANAGANTIOS',
									gc.getInfoTypeForString('UNITCLASS_DUMANNIOS')	:	'LEADER_DUMANNIOS',
									gc.getInfoTypeForString('UNITCLASS_RIUROS')		:	'LEADER_RIUROS',
									gc.getInfoTypeForString('UNITCLASS_HYBOREM')	:	'LEADER_HYBOREM',
									gc.getInfoTypeForString('UNITCLASS_JUDECCA')	:	'LEADER_JUDECCA',
									gc.getInfoTypeForString('UNITCLASS_LETHE')		:	'LEADER_LETHE',
									gc.getInfoTypeForString('UNITCLASS_MERESIN')	:	'LEADER_MERESIN',
									gc.getInfoTypeForString('UNITCLASS_OUZZA')		:	'LEADER_OUZZA',
									gc.getInfoTypeForString('UNITCLASS_SALLOS')		:	'LEADER_SALLOS',
									gc.getInfoTypeForString('UNITCLASS_STATIUS')	:	'LEADER_STATIUS',
									gc.getInfoTypeForString('UNITCLASS_EURABATRES')	:	'LEADER_CARDITH',
									gc.getInfoTypeForString('UNITCLASS_GOSEA')		:	'LEADER_GOSEA',
									gc.getInfoTypeForString('UNITCLASS_DUIN')		:	'LEADER_DUIN',
									gc.getInfoTypeForString('UNITCLASS_OS_GABELLA')	:	'LEADER_OS-GABELLA'
									}
					if iUnitClass in dAvatars:
						if iLeader == gc.getInfoTypeForString(dAvatars[iUnitClass]):
							unit.setAvatarOfCivLeader(True)
							cf.restoreTraits(pPlayer)
							if iRel != iStateReligion:
								unit.setReligion(iStateReligion)#It makes sense for the official religion to be the avatar's religion too
							if iCiv == iIllians:#The upgradable Illian avatars can cause some complicaions
								#If these unit exist, it must be after The White Hand ritual is complete
								pPlayer.setLastStateReligion(iHand)
								pPlayer.setAlignment(iEvil)
								unit.setHasPromotion(iHero, True)#Auric's leutenants have the hero promotion only if avatars of thei respective leaders
								iDefaultUnit = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex()#The un-upgraded form
								if iUnit != iDefaultUnit:

									for pUnit in PyPlayer(gc.getBARBARIAN_PLAYER()).getUnitList():
										if pUnit.getScenarioCounter() == iDefaultUnit:
											if pUnit.getUnitType() == iSluagh:
												for iProm in lBoundProm:
													if pUnit.isHasPromotion(iProm):break
												else:
													unit.convert(pUnit)
													unit.setHasPromotion(iHeld, False)
													sName = pUnit.getNameNoDesc()[:pUnit.getNameNoDesc().find("'s Sluagh")]
													if sName != unit.getNameNoDesc() and sName != unit.getName():
														unit.setName(sName)
													break
									unit.setScenarioCounter(iDefaultUnit)
									unit.setSummoner(-1)
								iUpgrade = -1
								if iUnit == gc.getInfoTypeForString('UNIT_AURIC_ASCENDED'):
									pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_FALLOW'),True)
								elif iUnit == gc.getInfoTypeForString('UNIT_AURIC'):
									if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AVATAR')):
										iUpgrade = gc.getInfoTypeForString('UNIT_AURIC_ASCENDED')
									elif gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
										pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_INSANE'),True)
								elif iUnit == gc.getInfoTypeForString('UNIT_ANAGANTIOS'):
									if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AVATAR')):
										iUpgrade = gc.getInfoTypeForString('UNIT_HEIR_ANAGANTIOS')
									elif unit.isHasPromotion(iChanneling4):
										iUpgrade = gc.getInfoTypeForString('UNIT_HIGH_PRIEST_ANAGANTIOS')
									elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON')):
										iUpgrade = gc.getInfoTypeForString('UNIT_EIDOLON_ANAGANTIOS')
								elif iUnit == gc.getInfoTypeForString('UNIT_DUMANNIOS'):
									if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AVATAR')):
										iUpgrade = gc.getInfoTypeForString('UNIT_HEIR_DUMANNIOS')
									elif unit.isHasPromotion(iChanneling4):
										iUpgrade = gc.getInfoTypeForString('UNIT_HIGH_PRIEST_DUMANNIOS')
									elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON')):
										iUpgrade = gc.getInfoTypeForString('UNIT_EIDOLON_DUMANNIOS')
								elif iUnit == gc.getInfoTypeForString('UNIT_RIUROS'):
									if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AVATAR')):
										iUpgrade = gc.getInfoTypeForString('UNIT_HEIR_RIUROS')
									elif unit.isHasPromotion(iChanneling4):
										iUpgrade = gc.getInfoTypeForString('UNIT_HIGH_PRIEST_RIUROS')
									elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON')):
										iUpgrade = gc.getInfoTypeForString('UNIT_EIDOLON_RIUROS')
								if iUpgrade != -1:
									newUnit = pPlayer.initUnit(iUpgrade, iX, iY, UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_SOUTH)
									unit.setHasPromotion(iDark, True)
									unit.setAvatarOfCivLeader(False)
									unit.setScenarioCounter(-1)
									cf.makeMortal(unit)
									newUnit.convert(unit)
									newUnit.setHasPromotion(iDark, False)
									newUnit.setScenarioCounter(iDefaultUnit)
									newUnit.setDamage(unit.getDamage(), -1)
									newUnit.setHasCasted(unit.isHasCasted())
									newUnit.setMadeAttack(unit.isMadeAttack())
									newUnit.setMoves(unit.getMoves())
						else:
							if unit.isAvatarOfCivLeader():
								unit.setAvatarOfCivLeader(False)

		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')):
			unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_CREATION'), False)

		for sProm in [	'PROMOTION_UNHOLY_TAINT',
						'PROMOTION_ASPECT_OF_WAR',
						'PROMOTION_VAMPIRE',
						'PROMOTION_DEMON',
						'PROMOTION_UNDEAD',
						'PROMOTION_ELEMENTAL',
						'PROMOTION_EXORCIST',
						'PROMOTION_ANGEL',
						'PROMOTION_ANGEL_SLAYING',
						'PROMOTION_DEMON_SLAYING',
						'PROMOTION_WEREWOLF_SLAYING',
						'PROMOTION_ELF_SLAYING',
						'PROMOTION_DRAGON_SLAYING',
						'PROMOTION_DWARF_SLAYING',
						'PROMOTION_GOLEM_SLAYING',
						'PROMOTION_ORC_SLAYING',


						'PROMOTION_WEREWOLF',
						'PROMOTION_EARTH2',
						'PROMOTION_LAW3',
						'PROMOTION_LIFE3',
						'PROMOTION_MIND3',
						'PROMOTION_SPIRIT3',

						'PROMOTION_IMMUNE_DISEASE',
						'PROMOTION_PERFECT_SIGHT',
						'PROMOTION_HERO',
						'PROMOTION_LOYALTY',
						'PROMOTION_CHANGELING',
						'PROMOTION_CUSTOS_JUDICII',
						'PROMOTION_CHANNELING1',
						'PROMOTION_CHANNELING2',

						'PROMOTION_DEATH1',
						'PROMOTION_DEATH2',
						'PROMOTION_DEATH3',

						'PROMOTION_DEATH_ARAWN1',
						'PROMOTION_DEATH_ARAWN2',
						'PROMOTION_DEATH_ARAWN3',
						'PROMOTION_WATER_WALKING',
						'PROMOTION_WATER_WALKING_TEMP',

						'PROMOTION_AFFINITY_AIR',
						'PROMOTION_AFFINITY_BODY',
						'PROMOTION_AFFINITY_CHAOS',
						'PROMOTION_AFFINITY_CREATION',
						'PROMOTION_AFFINITY_DEATH',
						'PROMOTION_AFFINITY_DEATH_ARAWN',
						'PROMOTION_AFFINITY_DIMENSIONAL',
						'PROMOTION_AFFINITY_EARTH',
						'PROMOTION_AFFINITY_ENCHANTMENT',
						'PROMOTION_AFFINITY_ENTROPY',
						'PROMOTION_AFFINITY_FIRE',
						'PROMOTION_AFFINITY_FORCE',
						'PROMOTION_AFFINITY_ICE',
						'PROMOTION_AFFINITY_LAW',
						'PROMOTION_AFFINITY_LIFE',
						'PROMOTION_AFFINITY_METAMAGIC',
						'PROMOTION_AFFINITY_MIND',
						'PROMOTION_AFFINITY_NATURE',
						'PROMOTION_AFFINITY_SHADOW',
						'PROMOTION_AFFINITY_SPIRIT',
						'PROMOTION_AFFINITY_SUN',
						'PROMOTION_AFFINITY_WATER'

						]:
			iProm = gc.getInfoTypeForString(sProm)
			if unit.isHasPromotion(iProm):
				self.onUnitPromoted([unit, iProm])


#UNITAI for Adepts and Terraformers
##		if not pPlayer.isHuman() or pPlayer.isBarbarian():
		if not pPlayer.isBarbarian():
			bCanMageTerraform = False
			numTreeTerraformer=0
			iDivine = gc.getInfoTypeForString('PROMOTION_DIVINE')
			iNature = gc.getInfoTypeForString('PROMOTION_NATURE2')
			iNatureA = gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE')
			if unit.isHasPromotion(iNature) or unit.isHasPromotion(iNatureA):
				bCanMageTerraform = True
				neededTreeTerraformer = 1
				if iCiv in [iLjosalfar, iSvartalfar]:
					neededTreeTerraformer += pPlayer.getNumCities()/3
				for loopUnit in PyPlayer(iPlayer).getUnitList():
					if loopUnit.isHasPromotion(iNature) or loopUnit.isHasPromotion(iNatureA):
						if loopUnit.getUnitAIType() == gc.getInfoTypeForString('UNITAI_TERRAFORMER'):
							numTreeTerraformer += 1
				if numTreeTerraformer < neededTreeTerraformer:
					unit.setUnitAIType(gc.getInfoTypeForString('UNITAI_TERRAFORMER'))

			elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1')) or unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUN1')):
				bCanMageTerraform = True
			numbermageterrafomer = pPlayer.AI_getNumAIUnits(gc.getInfoTypeForString('UNITAI_TERRAFORMER')) - numTreeTerraformer
			if bCanMageTerraform:
				if numbermageterrafomer < 2:
					unit.setUnitAIType(gc.getInfoTypeForString('UNITAI_TERRAFORMER'))
			if not pPlayer.isHuman():
				if unit.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_ADEPT'):
					if pPlayer.countOwnedBonuses(gc.getInfoTypeForString('BONUS_MANA_WATER'), False) > 0:
						bCanMageTerraform = True
					if pPlayer.countOwnedBonuses(gc.getInfoTypeForString('BONUS_MANA_SUN'), False) > 0:
						bCanMageTerraform = True
					numbermanaupgrade = pPlayer.AI_getNumAIUnits(gc.getInfoTypeForString('UNITAI_MANA_UPGRADE'))
					bHasAI = False
					canupgrademana = False
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):
						if pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA')) > 0:
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_METAMAGIC')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_METAMAGIC')):
							canupgrademana = True
					elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_ALTERATION')):
						if pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA')) > 0:
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_ENCHANTMENT')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_LIFE')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_LIFE')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_FORCE')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_FORCE')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_NATURE')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_NATURE')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_BODY')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_BODY')):
							canupgrademana = True
					elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_DIVINATION')):
						if pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA')) > 0:
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_CREATION')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_CREATION')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_LAW')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_LAW')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_MIND')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_MIND')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_SPIRIT')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_SPIRIT')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_SUN')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_SUN')):
							canupgrademana = True
					elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_ELEMENTALISM')):
						if pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA')) > 0:
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_AIR')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_AIR')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_FIRE')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_FIRE')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_ICE')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_ICE')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_EARTH')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_EARTH')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_WATER')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_WATER')):
							canupgrademana = True
					elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_NECROMANCY')):
						if pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA')) > 0:
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_CHAOS')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_CHAOS')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_DEATH')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_DEATH')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_DIMENSIONAL')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_ENTROPY')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_ENTROPY')):
							canupgrademana = True
						elif pArea.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_SHADOW')) > pArea.getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_MANA_SHADOW')):
							canupgrademana = True
					if numbermanaupgrade == 0:
						unit.setUnitAIType(gc.getInfoTypeForString('UNITAI_MANA_UPGRADE'))
						bHasAI = True
					if canupgrademana:
						if pPlayer.countOwnedBonuses(gc.getInfoTypeForString('BONUS_MANA'), False) > numbermanaupgrade * 2:
							unit.setUnitAIType(gc.getInfoTypeForString('UNITAI_MANA_UPGRADE'))
							bHasAI = True
					if not bHasAI:
						if bCanMageTerraform:
							if numbermageterrafomer < 2:
								unit.setUnitAIType(gc.getInfoTypeForString('UNITAI_TERRAFORMER'))
								bHasAI = True
					if not bHasAI:
						pPlot = unit.plot()
						if pPlayer.AI_getNumAIUnits(gc.getInfoTypeForString('UNITAI_MAGE')) < pPlayer.getNumCities() / 2:
							unit.setUnitAIType(gc.getInfoTypeForString('UNITAI_MAGE'))
						elif pPlot.area().getAreaAIType(pPlayer.getTeam()) == AreaAITypes.AREAAI_DEFENSIVE:
							unit.setUnitAIType(gc.getInfoTypeForString('UNITAI_MAGE'))
						else:
							unit.setUnitAIType(gc.getInfoTypeForString('UNITAI_WARWIZARD'))
		if unit.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_ENGINEER'):
			if iRace == gc.getInfoTypeForString('PROMOTION_DWARF') or unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GUERILLA2')):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOUNTAINEER'), True)
			if not pPlayer.isHuman():
				if pPlayer.AI_getNumAIUnits(gc.getInfoTypeForString('UNITAI_WORKER')) > pPlayer.getNumCities()/2:
					unit.setUnitAIType(gc.getInfoTypeForString('UNITAI_ENGINEER'))

		if unit.getUnitClassType() in [ gc.getInfoTypeForString('UNITCLASS_PRIEST_RINGGIVER'), gc.getInfoTypeForString('UNITCLASS_PIXIE'), gc.getInfoTypeForString('UNITCLASS_WORKER')]:
			unit.setUnitAIType(gc.getInfoTypeForString('UNITAI_WORKER'))


		if CyGame().getWBMapScript():
			sf.onUnitCreated(unit)


		# lfgr 09/2019: Blizzard damage on unit creation is handled here.
		# damage on movement is handled in CvSpellInterface.onMoveBlizzard
		# if unit.plot().getFeatureType() == gc.getInfoTypeForString( "FEATURE_BLIZZARD" ) :
			# if not unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_WINTERBORN')):
				# unit.doDamage(10, 50, unit, gc.getInfoTypeForString('DAMAGE_COLD'), False)

		if not self.__LOG_UNITBUILD:
			return

	def onUnitBuilt(self, argsList):
		'Unit Completed'
		city = argsList[0]
		unit = argsList[1]
		player = PyPlayer(city.getOwner())
		iPlayer = unit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iUnitCombat = unit.getUnitCombatType()
		pPlot = unit.plot()

		if unit.getUnitType() == gc.getInfoTypeForString('UNIT_ADVENTURER'):
			infoU = gc.getUnitInfo(unit.getUnitType())
			for iProm in range(gc.getNumPromotionInfos()):
				if unit.isHasPromotion(iProm):
					if not infoU.getFreePromotions(iProm):
						unit.setHasPromotion(iProm, False)
			unit.setReligion(gc.getInfoTypeForString('RELIGION_FOXMEN'))
			unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DIVINE'), True)
			unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FAIR_WINDS'), True)
			unit.setName(cf.MarnokNameGenerator(unit))

		if unit.isAlive():
			if not isWorldUnitClass(unit.getUnitClassType()):
				# Advanced Tactics - Diverse Grigori (idea and base code taken from FFH Tweakmod)
				if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS):
					if pPlayer.getCivilizationType() in [gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'), gc.getInfoTypeForString('CIVILIZATION_GRIGORI')]:
						if unit.getRace() == -1:
							iChance = 40
							if CyGame().getSorenRandNum(100, "Grigori Racial Diversity "+ unit.getName().encode('latin_1','replace')) <= iChance:
								listRaces = [-1]
								jCult = city.calculateCulturePercent(iPlayer)
								if jCult < 100:
									for jPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
										jCult = city.calculateCulturePercent(jPlayer)
										if jCult > 0:
											pjPlayer = gc.getPlayer(jPlayer)
											jCiv = pjPlayer.getCivilizationType()
											jCivInfo = gc.getCivilizationInfo(jCiv)
											jRace = jCivInfo.getDefaultRace()
											for i in xrange(jCult):
												listRaces.append(jRace)
									iRace = listRaces.pop(CyGame().getSorenRandNum(len(listRaces), "Grigori Racial Diversity-"+ unit.getName().encode('latin_1','replace')))
									if iRace != -1:
										unit.setHasPromotion(iRace, True)

				# End Advanced Tactics

				if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS_HOSTILE')) > 0:
					if CyGame().getSorenRandNum(50, "Asylum "+ unit.getName().encode('latin_1','replace')) <= 3:
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)

				if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS')) > 0:
					if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENRAGED')):
						unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENRAGED'), False)

				if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_WARRENS')) > 0:
					if not isNationalUnitClass(unit.getUnitClassType()):
						if not unit.isMechUnit():
							if not iUnitCombat in [-1, gc.getInfoTypeForString('UNITCOMBAT_ADEPT'),gc.getInfoTypeForString('UNITCOMBAT_DISCIPLE')]:
		#						if unit.getUnitCombatType() != UnitCombatTypes.NO_UNITCOMBAT:
								newUnit = pPlayer.initUnit(unit.getUnitType(), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								city.applyBuildEffects(newUnit)


		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_DESERT_SHRINE')) > 0:
			if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_DISCIPLE'):
				iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
				iMirror = gc.getInfoTypeForString('IMPROVEMENT_MIRROR_OF_HEAVEN')
				iX = city.getX()
				iY = city.getY()
				iXP = 0
				for iiX in xrange(iX-3, iX+4, 1):
					for iiY in xrange(iY-3, iY+4, 1):
						pLoopPlot = CyMap().plot(iiX,iiY)
						if not pLoopPlot.isNone():
							if city.canWork(pLoopPlot):
								if pLoopPlot.getImprovementType() == iMirror:
									iXP += 2
								elif pLoopPlot.getTerrainType() == iDesert:
									if not pLoopPlot.isPeak():
										if pLoopPlot.getImprovementType() == -1:
											if pLoopPlot.getFeatureType() == -1:
												iXP += 1
				if iXP > 0:
					unit.changeExperience(iXP, -1, False, False, True)

		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_CHANCEL_OF_GUARDIANS')) > 0:
			if CyGame().getSorenRandNum(100, "Chancel of Guardians "+ unit.getName().encode('latin_1','replace')) < 20:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEFENSIVE'), True)

		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN_HOSTILE')) > 0:
			if gc.getInfoTypeForString('ALIGNMENT_EVIL') == cf.getUnitAlignment(unit, True):
				if CyGame().getSorenRandNum(100, "Temple of the EMpyrean Blind "+ unit.getName().encode('latin_1','replace')) < 5:
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BLIND'), True)

		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD_HOSTILE')) > 0:
			if CyGame().getSorenRandNum(100, "Safehouse Pacified "+ unit.getName().encode('latin_1','replace')) < 20:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PACIFIED'), True)

		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE_HOSTILE')) > 0:
			if CyGame().getSorenRandNum(100, "Aphotic Throne Paranoia "+ unit.getName().encode('latin_1','replace')) < 5:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PARANOID'), True)

		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE_HOSTILE')) > 0:
			if CyGame().getSorenRandNum(100, "Aphotic Throne Paranoia "+ unit.getName().encode('latin_1','replace')) < 10:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)

		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND_HOSTILE')) > 0:
			if unit.getReligion() == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
				if CyGame().getSorenRandNum(100, "Temple of the Hand Cold"+ unit.getName().encode('latin_1','replace')) < 20:
					unit.doDamageNoCaster(5, 90, gc.getInfoTypeForString('DAMAGE_COLD'), False)

		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARENA_HOSTILE')) > 0:
			if CyGame().getSorenRandNum(100, "Arena rebel "+ unit.getName().encode('latin_1','replace')) < 20:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REBEL'), True)
				if unit.canCast(gc.getInfoTypeForString('SPELL_ARENA_BATTLE'), False):
					unit.cast(gc.getInfoTypeForString('SPELL_ARENA_BATTLE'))

		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL_HOSTILE')) > 0:
			if CyGame().getSorenRandNum(100, "Veil "+ unit.getName().encode('latin_1','replace')) < 10:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POSSESSED'), True)

		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TOPHET')) > 0:
			if CyGame().getSorenRandNum(100, "Tophet "+ unit.getName().encode('latin_1','replace')) < 20:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE_RESISTANCE'), True)
		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TOPHET_HOSTILE')) > 0:
			if CyGame().getSorenRandNum(100, "Tophet hostile fire"+ unit.getName().encode('latin_1','replace')) < 20:
				unit.doDamageNoCaster(5, 90, gc.getInfoTypeForString('DAMAGE_FIRE'), False)

		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_INTERSTICE_HOSTILE')) > 0:
			if CyGame().getSorenRandNum(100, "Interstice "+ unit.getName().encode('latin_1','replace')) < 5:
				bWater = unit.getDomainType() == gc.getInfoTypeForString('DOMAIN_SEA')
				iBestValue = 0
				pBestPlot = -1
				for i in xrange (CyMap().numPlots()):
					iValue = 0
					pTargetPlot = CyMap().plotByIndex(i)
					if bWater == pTargetPlot.isWater():
						iValue = CyGame().getSorenRandNum(1000, "Escape miscast move "+ unit.getName().encode('latin_1','replace'))
						if not pTargetPlot.isOwned():
							iValue += 1000
						if pTargetPlot == pPlot:
							iValue = 0
						if pTargetPlot.isCity():
							iValue = 0
						if iValue > iBestValue:
							iBestValue = iValue
							pBestPlot = pTargetPlot
				if pBestPlot != -1:
					unit.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True)


		if unit.getUnitType() == gc.getInfoTypeForString('UNIT_ACHERON'):
			iDragonCult = gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON')
			city.setHasReligion(iDragonCult,True,True,True)
			if CyGame().getHolyCity(iDragonCult).isNone():
				gc.getGame().setHolyCity(iDragonCult, city, True)
##			pPlayer.setLastStateReligion(iDragonCult)
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_WYRMHOLD'), 1)
			city.changeCulture(city.getOwner(), 30, True)

			unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAIR_GUARDIAN'), True)
			unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)

			if(game.getAIAutoPlay(game.getActivePlayer()) == 0 ):
				szBuffer = CyTranslator().getText("TXT_KEY_POPUP_ACHERON_CREATION", (city.getName(),))
				cf.addPopup(szBuffer, str(gc.getUnitInfo(unit.getUnitType()).getImage()))

		if unit.getRace() == gc.getInfoTypeForString('PROMOTION_DWARF'):
			unit.changeExperience(city.getNumBonuses(gc.getInfoTypeForString ('BONUS_ALE')), -1, False, False, False)
		CvAdvisorUtils.unitBuiltFeats(city, unit)

		if not self.__LOG_UNITBUILD:
			return
		CvUtil.pyPrint('%s was finished by Player %d Civilization %s'
			%(PyInfo.UnitInfo(unit.getUnitType()).getDescription(), player.getID(), player.getCivilizationName()))

	def onUnitKilled(self, argsList):
		'Unit Killed'
		unit, iAttacker = argsList
		iPlayer = unit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		player = PyPlayer(iPlayer)
		attacker = PyPlayer(iAttacker)
		pPlot = unit.plot()
		iX = unit.getX()
		iY = unit.getY()
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		iAnimal = gc.getInfoTypeForString('UNITCOMBAT_ANIMAL')
		iBeast = gc.getInfoTypeForString('UNITCOMBAT_BEAST')
		iHeld = gc.getInfoTypeForString('PROMOTION_HELD')
		iHero = gc.getInfoTypeForString('PROMOTION_HERO')
		iMercenaryRecruiter = gc.getInfoTypeForString('PROMOTION_MERCENARY_RECRUITER')

		if unit.getGroup().getActivityType() == ActivityTypes.ACTIVITY_PLUNDER:
			unit.setBlockading(False)
			pPlot.setFlagDirty(True)#Platyping suggested trying to see if this fixes the blockading issue

		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANGELING')):
			if unit.canCast(gc.getInfoTypeForString('SPELL_ASSUME_TRUE_FORM'), False):
				unit.cast(gc.getInfoTypeForString('SPELL_ASSUME_TRUE_FORM'))

		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HERALDS_BLESSING')):
			unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HERALDS_BLESSING'), False)

		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DAHLIA_BAND')):
			if unit.getUnitType() == gc.getInfoTypeForString('UNIT_TRISTAN'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DAHLIA_BAND'), False)

		if unit.isHasPromotion(iHeld):
			unit.setHasPromotion(iHeld, False)
		if unit.isHasPromotion(iMercenaryRecruiter):
			unit.setHasPromotion(iMercenaryRecruiter, False)
		iLairGuardian = gc.getInfoTypeForString('PROMOTION_LAIR_GUARDIAN')
		if unit.isHasPromotion(iLairGuardian):
			unit.setHasPromotion(iLairGuardian, False)
			iHN = gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY')
			if unit.isHasPromotion(iHN):
				unit.setHasPromotion(iHN, False)
		# if unit.getUnitType() == gc.getInfoTypeForString('UNIT_ACHERON'):
			# iHoard = gc.getInfoTypeForString('EQUIPMENT_DRAGONS_HOARD')
			# if CyGame().getUnitCreatedCount(iHoard) == 0:
				# bPlayer.initUnit(iHoard, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		if unit.getUnitType() == gc.getInfoTypeForString('UNIT_KHALIDA'):
			unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'), True)
			unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING4'), True)
			unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING3'), True)
			unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING2'), True)
			iNum = 50 #CyGame().getSorenRandNum(cf.getNumBonusEffective(iPlayer, gc.getInfoTypeForString('BONUS_MANA_DEATH'), unit),"Khalida Suicide")
			if iNum > 0:
				unit.setBaseCombatStr(unit.baseCombatStr() + iNum)
				unit.setBaseCombatStrDefense(unit.baseCombatStrDefense() + iNum)
			#unit.changeImmortal(1)
			unit.setHasCasted(False)
			unit.setMadeAttack(False)
			unit.setDamage(0, iPlayer)

		if pPlot.isOwned():
			if gc.getPlayer(pPlot.getOwner()).countNumBuildings(gc.getInfoTypeForString('BUILDING_SOUL_SHROUD')):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATHPHAGE'), False)
				if not unit.isAvatarOfCivLeader():
					unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NETHERBIND'), True)

		bSoul = True
		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_NETHERBIND')) or unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CAPTUS_CAVEAE_ANGELORUM')):
			cf.makeMortal(unit)
			bSoul = False
		elif unit.getUnitCombatType() in [iAnimal, iBeast]:
			bSoul = False
		elif unit.isAlive() and not (unit.isImmortal() and pPlayer.getNumCities() > 0):
			if pPlot.isOwned():
				iPlayerSF = pPlot.getOwner()
				pPlayerSF = gc.getPlayer(iPlayerSF)

				if CyGame().getBuildingClassCreatedCount(gc.getInfoTypeForString('BUILDINGCLASS_SOUL_FORGE')) > 0:
					iSoulForge = gc.getInfoTypeForString('BUILDING_SOUL_FORGE')
					iSoulShroud = gc.getInfoTypeForString('BUILDING_SOUL_SHROUD')
					if pPlayerSF.countNumBuildings(iSoulForge) > 0:
						(loopCity, iter) = pPlayerSF.firstCity(False)
						while(loopCity):
							if (not loopCity.isNone() and loopCity.getOwner() == iPlayerSF): #only valid cities
								if loopCity.getNumRealBuilding(iSoulShroud) > 0:
									break
								if loopCity.getNumRealBuilding(iSoulForge) > 0:
									loopCity.changeProduction(unit.getExperience() + 10)
									CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SOUL_FORGE_DESTROY_SLUAGH",(gc.getUnitInfo(unit.getUnitType()).getDescription(), )),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/Buildings/Soulforge.dds',ColorTypes(gc.getInfoTypeForString("COLOR_RED")), iX, iY, True,True)
									CyInterface().addMessage(iPlayerSF,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SOUL_FORGE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/Buildings/Soulforge.dds',ColorTypes(gc.getInfoTypeForString("COLOR_GREEN")),loopCity.getX(),loopCity.getY(),True,True)
									bSoul = False
									break
							(loopCity, iter) = pPlayerSF.nextCity(iter, False)
			iBMC = gc.getInfoTypeForString('BUILDING_MOKKAS_CAULDRON')
			iBCMC = gc.getInfoTypeForString('BUILDINGCLASS_MOKKAS_CAULDRON')
			sArt = 'Art/Interface/Buttons/Buildings/Mokkas Cauldron.dds'
			iPlayerMC = -1
			iUnit = -1
			sText = -1

			if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATHPHAGE')):
				sText = "TXT_KEY_MESSAGE_DEATHPHAGE"
				sArt = 'Art/Interface/Buttons/Promotions/Cursed.dds'
				iPlayerMC = gc.getBARBARIAN_PLAYER()

				if pPlot.isOwned():
					iPlotPlayer = pPlot.getOwner()
					pPlotPlayer = gc.getPlayer(iPlotPlayer)
					if pPlotPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TOWER_OF_NECROMANCY')) > 0:
						if not (CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DEATH_MANA')) and pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL'))):
							iPlayerMC = iPlotPlayer

				iUnit = cf.getUnholyVersion(unit)
				pPlot = cf.findClearPlot(-1, pPlot)
				if pPlot == -1:
					iUnit = -1
				elif pPlot.isOwned():
					iPlotPlayer = pPlot.getOwner()
					pPlotPlayer = gc.getPlayer(iPlotPlayer)
					if pPlotPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_SOUL_SHROUD')) > 0:
						iUnit = -1

			if CyGame().getBuildingClassCreatedCount(iBCMC) > 0:
				if pPlot != -1:
					if pPlot.isCity():
						pCity = pPlot.getPlotCity()
						if pCity.getNumRealBuilding(iBMC) > 0:
							iPlayerMC = pCity.getOwner()
							iUnit = cf.getUnholyVersion(unit)
							sText = "TXT_KEY_MESSAGE_MOKKAS_CAULDRON"
			if iUnit == -1:
				iUMC = gc.getInfoTypeForString('EQUIPMENT_MOKKAS_CAULDRON')
				if CyGame().getUnitCreatedCount(gc.getInfoTypeForString('UNIT_MOKKA')) > 0 or CyGame().getUnitCreatedCount(iUMC) > 0 or CyGame().getBuildingClassCreatedCount(iBCMC) > 0:
					iPMC = gc.getInfoTypeForString('PROMOTION_MOKKAS_CAULDRON')
					for i in xrange(unit.plot().getNumUnits(), -1, -1):
						pUnit = unit.plot().getUnit(i)
						if pUnit.getUnitType() == iUMC or pUnit.isHasPromotion(iPMC):
							iPlayerMC = pUnit.getOwner()
							iUnit = cf.getUnholyVersion(unit)
							sText = "TXT_KEY_MESSAGE_MOKKAS_CAULDRON"
							break

			if iUnit != -1 and pPlot != -1:
				pPlayerMC = gc.getPlayer(iPlayerMC)
				newUnit = pPlayerMC.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATHPHAGE'), False)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UNDEAD'), True)
				self.onUnitPromoted([newUnit, gc.getInfoTypeForString('PROMOTION_UNDEAD')])


				newUnit.setDamage(50, PlayerTypes.NO_PLAYER)
				newUnit.finishMoves()
				if sText != -1:
					szBuffer = gc.getUnitInfo(newUnit.getUnitType()).getDescription()
					CyInterface().addMessage(iAttacker,True,25,CyTranslator().getText(sText,((szBuffer, ))),'AS2D_DISCOVERBONUS',1,sArt,ColorTypes(gc.getInfoTypeForString("COLOR_RED")), iX, iY,True,True)
					CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText(sText,((szBuffer, ))),'AS2D_DISCOVERBONUS',1,sArt,ColorTypes(gc.getInfoTypeForString("COLOR_RED")), iX, iY,True,True)
					CyInterface().addMessage(iPlayerMC,True,25,CyTranslator().getText(sText,((szBuffer, ))),'AS2D_DISCOVERBONUS',1,sArt,ColorTypes(gc.getInfoTypeForString("COLOR_GREEN")), iX, iY,True,True)
		if bSoul:
			cf.doAfterlife(unit)
			if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT_GUIDE')):
				iXP = unit.getExperience()
				if iXP > 0:
					py = PyPlayer(iPlayer)
					lUnits = []
					for pLoopUnit in py.getUnitList():
						# lfgr fix 12/2021: Units without unitcombat can't get promotions
						if pLoopUnit.isAlive() and pLoopUnit.getUnitCombatType() != UnitCombatTypes.NO_UNITCOMBAT:
							if not pLoopUnit.isOnlyDefensive():
								if not pLoopUnit.isDelayedDeath():
									if pLoopUnit.canAcquirePromotionAny():
										lUnits.append(pLoopUnit)

					if len(lUnits) > 0:
						pUnit = lUnits[CyGame().getSorenRandNum(len(lUnits), "Spirit Guide "+ unit.getName().encode('latin_1','replace'))-1]
						iXP /= 2
						pUnit.changeExperience(iXP, -1, False, False, False)
						unit.changeExperience(iXP * -1, -1, False, False, False)
						CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SPIRIT_GUIDE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/Promotions/SpiritGuide.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
		if CyGame().getWBMapScript():
			sf.onUnitKilled(unit, iAttacker)

#		if not self.__LOG_UNITKILLED:
#			return
#		CvUtil.pyPrint('Player %d Civilization %s Unit %s was killed by Player %d'
#			%(player.getID(), player.getCivilizationName(), PyInfo.UnitInfo(unit.getUnitType()).getDescription(), attacker.getID()))

	def onUnitLost(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Unit Lost'
		unit = argsList[0]
		iPlayer = unit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		player = PyPlayer(iPlayer)
		pPlot = unit.plot()
		iUnit = unit.getUnitType()


		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION')) or unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION')):
			if unit.isAvatarOfCivLeader():
				unit.setAvatarOfCivLeader(False)
			cf.makeMortal(unit)
			unit.setDuration(1)

		if unit.isImmortal() and unit.isBarbarian() and unit.getDuration()==0:
			newUnit = cf.addUnit(iUnit)
			newUnit.setDamage(90, -1)
			newUnit.setReligion(unit.getReligion())
			newUnit.setScenarioCounter(unit.getScenarioCounter())
			newUnit.setLevel(unit.getLevel())
			newUnit.setExperience(unit.getExperience(), -1)
			sName = unit.getNameNoDesc()
			if sName != newUnit.getNameNoDesc() and sName != newUnit.getName():
				newUnit.setName(sName)
			for iProm in xrange(gc.getNumPromotionInfos()):
				if gc.getPromotionInfo(iProm).isEquipment():continue
				newUnit.setHasPromotion(iProm, unit.isHasPromotion(iProm) )
			newUnit.changeImmortal(-1)

			sName = cf.getNameWithColorScheme(newUnit)
			sButton = newUnit.getButton()
			iX = newUnit.getX()
			iY = newUnit.getY()
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive():
					CyInterface().addMessage(iLoopPlayer, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_X_RESSURECTED", (sName, )), 'AS2D_CHARM_PERSON', 1, sButton, ColorTypes(7), iX, iY, True, True)

			return

		iAspectWar = gc.getInfoTypeForString('PROMOTION_ASPECT_OF_WAR')
		if unit.isHasPromotion(iAspectWar):
			if not unit.isImmortal():
				unit.setHasPromotion(iAspectWar, False)


		if unit.getUnitType() == gc.getInfoTypeForString('UNIT_DJINN'):
			if unit.getDelayedSpell() != -1:
				unit.changeImmobileTimer(-unit.getImmobileTimer())

		if pPlot != -1 and not pPlot.isNone():
			if iUnit == gc.getInfoTypeForString('UNIT_TREANT'):
				if unit.getRace() == gc.getInfoTypeForString('PROMOTION_ELEMENTAL'):#Illusions are excluded
					if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE')):
						if unit.canCast(gc.getInfoTypeForString('SPELL_BLOOM3_GREATER'), False):
							unit.cast(gc.getInfoTypeForString('SPELL_BLOOM3_GREATER'))
						elif unit.canCast(gc.getInfoTypeForString('SPELL_BLOOM2_GREATER'), False):
							unit.cast(gc.getInfoTypeForString('SPELL_BLOOM2_GREATER'))
						elif unit.canCast(gc.getInfoTypeForString('SPELL_BLOOM_GREATER'), False):
							unit.cast(gc.getInfoTypeForString('SPELL_BLOOM_GREATER'))
					if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_NATURE2')):
						if unit.canCast(gc.getInfoTypeForString('SPELL_BLOOM3'), False):
							unit.cast(gc.getInfoTypeForString('SPELL_BLOOM3'))
						elif unit.canCast(gc.getInfoTypeForString('SPELL_BLOOM2'), False):
							unit.cast(gc.getInfoTypeForString('SPELL_BLOOM2'))
						elif unit.canCast(gc.getInfoTypeForString('SPELL_BLOOM'), False):
							unit.cast(gc.getInfoTypeForString('SPELL_BLOOM'))
					if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER')):
						if unit.canCast(gc.getInfoTypeForString('SPELL_SPRING_GREATER'), False):
							unit.cast(gc.getInfoTypeForString('SPELL_SPRING_GREATER'))
					if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1')):
						if unit.canCast(gc.getInfoTypeForString('SPELL_SPRING'), False):
							unit.cast(gc.getInfoTypeForString('SPELL_SPRING'))
					if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN')):
						if unit.canCast(gc.getInfoTypeForString('SPELL_SCORCH_GREATER'), False):
							unit.cast(gc.getInfoTypeForString('SPELL_SCORCH_GREATER'))
					if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUN1')):
						if unit.canCast(gc.getInfoTypeForString('SPELL_SCORCH'), False):
							unit.cast(gc.getInfoTypeForString('SPELL_SCORCH'))
					if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE')):
						if unit.canCast(gc.getInfoTypeForString('SPELL_BLAZE_GREATER'), False):
							unit.cast(gc.getInfoTypeForString('SPELL_BLAZE_GREATER'))
					if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE1')):
						if unit.canCast(gc.getInfoTypeForString('SPELL_BLAZE'), False):
							unit.cast(gc.getInfoTypeForString('SPELL_BLAZE'))
					unit.changeImmobileTimer(-unit.getImmobileTimer())


		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_FORCE')):
			iWard = gc.getInfoTypeForString('IMPROVEMENT_RING_OF_WARDING')
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_WARDING'):
				iLevel = 0
				iAffinity = gc.getInfoTypeForString('PROMOTION_AFFINITY_FORCE')
				iMana = gc.getInfoTypeForString('BONUS_MANA_FORCE')
				for i in xrange(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(i)
					if pUnit.isHasPromotion(iAffinity):
						if unit.getID() != pUnit.getID():
							if pUnit.getImmobileTimer() < 1:
								if gc.getPlayer(pUnit.getOwner()).getDisableSpellcasting() == 0:
									iLevel = max(iLevel, min(pUnit.getLevel(), cf.getNumBonusEffective(pUnit.getOwner(), iMana, pUnit) ) )
				pPlot.setMinLevel(iLevel)
				if iLevel == 0:
					iReal = pPlot.getRealImprovementType()
					if iReal == iWard:
						pPlot.setImprovementType(-1)
					else:
						pPlot.setImprovementType(iReal)

		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPLIT_SOUL')):
			#It seems that a unit's summons have their summoner removed before this point
			iSeveredSoul = gc.getInfoTypeForString('UNIT_SEVERED_SOUL')
			if unit.getUnitType() != iSeveredSoul:
				for loopUnit in player.getUnitList():
					if loopUnit.getUnitType() == iSeveredSoul:#is it a specified type of summon?
						if loopUnit.getSummoner() == -1:#is it a summon of pUnit?
							loopUnit.kill(False, iPlayer)

		if unit.getDuration() > 0:
			if unit.getDelayedSpell() != -1:
				unit.changeImmobileTimer(-unit.getImmobileTimer())
			if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO')):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO'), False)

		if unit.getSummoner() != -1:
			pUnit = pPlayer.getUnit(unit.getSummoner())


			iSeveredSoul = gc.getInfoTypeForString('UNIT_SEVERED_SOUL')
			if pUnit.getUnitType() != iSeveredSoul:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPLIT_SOUL'), len( cf.listSummons(pUnit, iSeveredSoul) ) > 1)

			if unit.isAlive():
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRE')):#Sire of Spawn or Thrall
					pUnit.changeDamage(-20, PlayerTypes.NO_PLAYER)
					if not unit.isMadeAttack():
						pUnit.setMadeAttack(False)
					if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRE')) or unit.getUnitType() == gc.getInfoTypeForString('UNIT_BLOODPET'):
						if not unit.isHasCasted():
							pUnit.setHasCasted(False)
						pUnit.changeExperience(unit.getExperience() / 2, -1, False, False, False)
						unit.changeExperience(-unit.getExperience() / 2, -1, False, False, False)
						CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_SPELL_FEED_ON_SPAWN", (pUnit.getName(),unit.getName(),)),'',1,'Art/Interface/Buttons/Spells/Feed.dds',gc.getInfoTypeForString('COLOR_YELLOW'),pUnit.getX(),pUnit.getY(),True,True)

			unitInfo = gc.getUnitInfo(unit.getUnitType())
			if unit.getRace() == gc.getInfoTypeForString('PROMOTION_UNDEAD') or unitInfo.getFreePromotions(gc.getInfoTypeForString('PROMOTION_DEMON')):
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH')):
					iPercentXP = 0
					for iProm in [gc.getInfoTypeForString('PROMOTION_CHANNELING1'),gc.getInfoTypeForString('PROMOTION_CHANNELING2'),gc.getInfoTypeForString('PROMOTION_CHANNELING3'),gc.getInfoTypeForString('PROMOTION_CHANNELING4')]:
						if pUnit.isHasPromotion(iProm):
							iPercentXP += 25
					iXP = unit.getExperience()*iPercentXP/100
					if iXP > 0:
						pUnit.changeExperience(iXP, -1, False, False, False)
						unit.changeExperience(-iXP, -1, False, False, False)
			else:
				iMana = unitInfo.getPrereqAndBonus()
				if iMana != -1:
					if gc.getBonusInfo(iMana).isMana():
						iPercentXP = 0
						for iProm in [gc.getInfoTypeForString('PROMOTION_CHANNELING1'),gc.getInfoTypeForString('PROMOTION_CHANNELING2'),gc.getInfoTypeForString('PROMOTION_CHANNELING3'),gc.getInfoTypeForString('PROMOTION_CHANNELING4')]:
							if pUnit.isHasPromotion(iProm):
								iPercentXP += 25
						iXP = unit.getExperience()*iPercentXP/100
						if iXP > 0:
							dAffinities= {	gc.getInfoTypeForString('BONUS_MANA_AIR')			:	'PROMOTION_AFFINITY_AIR',
											gc.getInfoTypeForString('BONUS_MANA_BODY')			:	'PROMOTION_AFFINITY_BODY',
											gc.getInfoTypeForString('BONUS_MANA_CHAOS')			:	'PROMOTION_AFFINITY_CHAOS',
											gc.getInfoTypeForString('BONUS_MANA_CREATION')		:	'PROMOTION_AFFINITY_CREATION',
											# gc.getInfoTypeForString('BONUS_MANA_DEATH')		:	'PROMOTION_AFFINITY_DEATH',
											gc.getInfoTypeForString('BONUS_MANA_DEATH')			:	'PROMOTION_AFFINITY_DEATH_ARAWN',
											gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')	:	'PROMOTION_AFFINITY_DIMENSIONAL',
											gc.getInfoTypeForString('BONUS_MANA_EARTH')			:	'PROMOTION_AFFINITY_EARTH',
											gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT')	:	'PROMOTION_AFFINITY_ENCHANTMENT',
											gc.getInfoTypeForString('BONUS_MANA_ENTROPY')		:	'PROMOTION_AFFINITY_ENTROPY',
											gc.getInfoTypeForString('BONUS_MANA_FIRE')			:	'PROMOTION_AFFINITY_FIRE',
											gc.getInfoTypeForString('BONUS_MANA_FORCE')			:	'PROMOTION_AFFINITY_FORCE',
											gc.getInfoTypeForString('BONUS_MANA_ICE')			:	'PROMOTION_AFFINITY_ICE',
											gc.getInfoTypeForString('BONUS_MANA_LAW')			:	'PROMOTION_AFFINITY_LAW',
											gc.getInfoTypeForString('BONUS_MANA_LIFE')			:	'PROMOTION_AFFINITY_LIFE',
											gc.getInfoTypeForString('BONUS_MANA_METAMAGIC')		:	'PROMOTION_AFFINITY_METAMAGIC',
											gc.getInfoTypeForString('BONUS_MANA_MIND')			:	'PROMOTION_AFFINITY_MIND',
											gc.getInfoTypeForString('BONUS_MANA_NATURE')		:	'PROMOTION_AFFINITY_NATURE',
											gc.getInfoTypeForString('BONUS_MANA_SHADOW')		:	'PROMOTION_AFFINITY_SHADOW',
											gc.getInfoTypeForString('BONUS_MANA_SPIRIT')		:	'PROMOTION_AFFINITY_SPIRIT',
											gc.getInfoTypeForString('BONUS_MANA_SUN')			:	'PROMOTION_AFFINITY_SUN',
											gc.getInfoTypeForString('BONUS_MANA_WATER')			:	'PROMOTION_AFFINITY_WATER'
											}
							if iMana in dAffinities:
								iAffinity = gc.getInfoTypeForString(dAffinities[iMana])
								if pUnit.isHasPromotion(iAffinity):
									pUnit.changeExperience(iXP, -1, False, False, False)
									unit.changeExperience(-iXP, -1, False, False, False)


		cf.sluagh(unit)

		if CyGame().getWBMapScript():
			sf.onUnitLost(unit)

		if not self.__LOG_UNITLOST:
			return
		CvUtil.pyPrint('%s was lost by Player %d Civilization %s'
			%(PyInfo.UnitInfo(unit.getUnitType()).getDescription(), player.getID(), player.getCivilizationName()))

	def onUnitPromoted(self, argsList):
		'Unit Promoted'
		pUnit, iPromotion = argsList
		iPlayer = pUnit.getOwner()
		player = PyPlayer(iPlayer)
		pPlayer = gc.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()
		eTeam = gc.getTeam(iTeam)
		iCiv = pPlayer.getCivilizationType()
		pPlot = pUnit.plot()
		pArea = pUnit.area()

		iUnit = pUnit.getUnitType()
		iUnitClass = pUnit.getUnitClassType()
		infoUnit = gc.getUnitInfo(iUnit)
		infoProm = gc.getPromotionInfo(iPromotion)

		if pUnit.isPromotionImmune(iPromotion):
			pUnit.setPromotionReady(True)

		iSidar = gc.getInfoTypeForString('CIVILIZATION_SIDAR')
		iCabal = gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL')
		iChanneling1 = gc.getInfoTypeForString('PROMOTION_CHANNELING1')
		iChanneling2 = gc.getInfoTypeForString('PROMOTION_CHANNELING2')
		iChanneling3 = gc.getInfoTypeForString('PROMOTION_CHANNELING3')
		iChanneling4 = gc.getInfoTypeForString('PROMOTION_CHANNELING4')
		iUnholyTaint = gc.getInfoTypeForString('PROMOTION_UNHOLY_TAINT')
		if not (iCiv == iSidar or pUnit.getReligion() == iCabal) and gc.getInfoTypeForString('ALIGNMENT_EVIL') == cf.getUnitAlignment(pUnit, True):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN')):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'), True)
				if pUnit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH')):
					pUnit.setPromotionReady(True)
					pUnit.setLevel(max(1,pUnit.getLevel()-1))
			else:
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1')):
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1'), False)
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH1'), True)
					if pUnit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_DEATH1')):
						pUnit.setPromotionReady(True)
						pUnit.setLevel(max(1,pUnit.getLevel()-1))
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN2')):
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN2'), False)
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH2'), True)
					if pUnit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_DEATH2')):
						pUnit.setPromotionReady(True)
						pUnit.setLevel(max(1,pUnit.getLevel()-1))
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN3')):
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN3'), False)
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH3'), True)
					if pUnit.isPromotionImmune(gc.getInfoTypeForString('PROMOTION_DEATH3')):
						pUnit.setPromotionReady(True)
						pUnit.setLevel(max(1,pUnit.getLevel()-1))

		if iPromotion in [gc.getInfoTypeForString('PROMOTION_ILLUSION'), gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION')]:
			if pUnit.isAvatarOfCivLeader():
				pUnit.setAvatarOfCivLeader(False)
			cf.makeMortal(pUnit)
			pUnit.setDuration(1)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_ASPECT_OF_WAR'):
			if pUnit.getDuration() != 0 or pUnit.getSummoner() != -1 or not pUnit.isAlive() or pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION')) or pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION')):
				pUnit.setHasPromotion(iPromotion, False)
			elif not gc.getUnitInfo(pUnit.getUnitType()).getFreePromotions(iPromotion):
				iNumAspects = 0
				listUnits = PyHelpers.PyGame().getAllUnitList()
				for loopUnit in listUnits:
					if loopUnit is pUnit:continue
					if loopUnit.isHasPromotion(iPromotion):
						if loopUnit.isAlive():
							iNumAspects += 1
							if iNumAspects > 6:
								if not gc.getUnitInfo(loopUnit.getUnitType()).getFreePromotions(iPromotion):
									pUnit.setHasPromotion(iPromotion, False)
									break
						else:
							loopUnit.setHasPromotion(iPromotion, False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_CHANGELING'):
			if not -1 < pUnit.getScenarioCounter() < gc.getNumUnitInfos():
				pUnit.setScenarioCounter(pUnit.getUnitType())


		elif iPromotion == iChanneling1:
			if pUnit.getRace() != gc.getInfoTypeForString('PROMOTION_PUPPET'):
	##			if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_ADEPT'):
				listWeightedAffinities = []
				listAffinities = [	gc.getInfoTypeForString('PROMOTION_AIR1'),
									gc.getInfoTypeForString('PROMOTION_BODY1'),
									gc.getInfoTypeForString('PROMOTION_CHAOS1'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_CREATION'),
									# gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1'),
									# gc.getInfoTypeForString('PROMOTION_DEATH1'),
									gc.getInfoTypeForString('PROMOTION_DIMENSIONAL1'),
									gc.getInfoTypeForString('PROMOTION_EARTH1'),
									gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1'),
									gc.getInfoTypeForString('PROMOTION_ENTROPY1'),
									gc.getInfoTypeForString('PROMOTION_FIRE1'),
									gc.getInfoTypeForString('PROMOTION_FORCE1'),
									gc.getInfoTypeForString('PROMOTION_ICE1'),
									gc.getInfoTypeForString('PROMOTION_LAW1'),
									gc.getInfoTypeForString('PROMOTION_LIFE1'),
									gc.getInfoTypeForString('PROMOTION_METAMAGIC1'),
									gc.getInfoTypeForString('PROMOTION_MIND1'),
									gc.getInfoTypeForString('PROMOTION_NATURE1'),
									gc.getInfoTypeForString('PROMOTION_SHADOW1'),
									gc.getInfoTypeForString('PROMOTION_SPIRIT1'),
									gc.getInfoTypeForString('PROMOTION_SUN1'),
									gc.getInfoTypeForString('PROMOTION_WATER1')
									]

				if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')):
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DEATH_MANA')):
						if gc.getInfoTypeForString('PROMOTION_DEATH1') in listAffinities:
							listAffinities.remove(gc.getInfoTypeForString('PROMOTION_DEATH1'))
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_ENTROPY_MANA')):
						if gc.getInfoTypeForString('PROMOTION_ENTROPY1') in listAffinities:
							listAffinities.remove(gc.getInfoTypeForString('PROMOTION_ENTROPY1'))
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_SHADOW_MANA')):
						if gc.getInfoTypeForString('PROMOTION_SHADOW1') in listAffinities:
							listAffinities.remove(gc.getInfoTypeForString('PROMOTION_SHADOW1'))
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DIMENSIONAL_MANA')):
						if gc.getInfoTypeForString('PROMOTION_DIMENSIONAL1') in listAffinities:
							listAffinities.remove(gc.getInfoTypeForString('PROMOTION_DIMENSIONAL1'))
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_CHAOS_MANA')):
						if gc.getInfoTypeForString('PROMOTION_CHAOS1') in listAffinities:
							listAffinities.remove(gc.getInfoTypeForString('PROMOTION_CHAOS1'))
				elif pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')):
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_SUN_MANA')):
						if gc.getInfoTypeForString('PROMOTION_SUN1') in listAffinities:
							listAffinities.remove(gc.getInfoTypeForString('PROMOTION_SUN1'))

				lAlignment = [pPlayer.getAlignment(), cf.getUnitAlignment(pUnit, False)]

				if iCiv == iSidar or pUnit.getReligion() == iCabal or gc.getInfoTypeForString('ALIGNMENT_GOOD') in lAlignment:
					if gc.getInfoTypeForString('PROMOTION_DEATH1') in listAffinities:
						listAffinities.remove(gc.getInfoTypeForString('PROMOTION_DEATH1'))
				elif gc.getInfoTypeForString('ALIGNMENT_EVIL') in lAlignment:
					if gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1') in listAffinities:
						listAffinities.remove(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1'))

				if iCiv == iSidar or pUnit.getReligion() == iCabal or pUnit.getRace() == gc.getInfoTypeForString('PROMOTION_GREY'):
					listAffinities.append(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1'))

				if isWorldUnitClass(pUnit.getUnitClassType()):
					for iProm in listAffinities:
						if not pUnit.isHasPromotion(iProm):
							if gc.getUnitInfo(pUnit.getUnitType()).getFreePromotions(iProm):
								pUnit.setHasPromotion(iAffinity, True)
								self.onUnitPromoted([pUnit, iAffinity])
					listAffinities = []

				iNumSpheres = 1
				if CyGame().getSorenRandNum(6, "Petrarch "+str(pUnit.getID())) < 1:
					iNumSpheres = 2
				for iAffinity in listAffinities:
					if pUnit.isPromotionImmune(iAffinity):
						continue
					elif pUnit.isHasPromotion(iAffinity):
						iNumSpheres -= 1
						if iNumSpheres < 1:
							break
					else:
						infoAffinity = gc.getPromotionInfo(iAffinity)
						iMana = infoAffinity.getBonusPrereq()
						for i in range(cf.getNumBonusEffective(iPlayer, iMana, pUnit)):
							listWeightedAffinities.append(iAffinity)
				for i in range(iNumSpheres):
					if len(listWeightedAffinities) > 0:
						iAffinity = listWeightedAffinities.pop(CyGame().getSorenRandNum(len(listWeightedAffinities), "Affinity-Channeling1 " + str(pUnit.getID())))
						pUnit.setHasPromotion(iAffinity, True)
						self.onUnitPromoted([pUnit, iAffinity])

		elif iPromotion == iChanneling2:
			if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ADEPT'):
				listWeightedAffinities = []
				listAffinities = [	gc.getInfoTypeForString('PROMOTION_AFFINITY_AIR'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_BODY'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_CHAOS'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_CREATION'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_EARTH'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_ENCHANTMENT'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_FORCE'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_ICE'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_LAW'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_LIFE'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_METAMAGIC'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'),
									gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER')
									]

				if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')):
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DEATH_MANA')):
						if gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH') in listAffinities:
							listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'))
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_ENTROPY_MANA')):
						if gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY') in listAffinities:
							listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY'))
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_SHADOW_MANA')):
						if gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW') in listAffinities:
							listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'))
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DIMENSIONAL_MANA')):
						if gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL') in listAffinities:
							listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL'))
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_CHAOS_MANA')):
						if gc.getInfoTypeForString('PROMOTION_AFFINITY_CHAOS') in listAffinities:
							listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_CHAOS'))
				elif pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')):
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_SUN_MANA')):
						if gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN') in listAffinities:
							listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'))
				lAlignment = [pPlayer.getAlignment(), cf.getUnitAlignment(pUnit, False)]
				if iCiv == iSidar or pUnit.getReligion() == iCabal or gc.getInfoTypeForString('ALIGNMENT_GOOD') in lAlignment:
					if gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH') in listAffinities:
						listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'))
				elif gc.getInfoTypeForString('ALIGNMENT_EVIL') in lAlignment:
					if gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN') in listAffinities:
						listAffinities.remove(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'))

				if isWorldUnitClass(pUnit.getUnitClassType()):
					for iProm in listAffinities:
						if not pUnit.isHasPromotion(iProm):
							if gc.getUnitInfo(pUnit.getUnitType()).getFreePromotions(iProm):
								pUnit.setHasPromotion(iAffinity, True)
								self.onUnitPromoted([pUnit, iAffinity])
					listAffinities = []

				iNumSpheres = 1
				if CyGame().getSorenRandNum(6, "Petrarch "+str(pUnit.getID())) < 1:
					iNumSpheres = 2
				for iAffinity in listAffinities:
					if pUnit.isPromotionImmune(iAffinity):
						continue
					elif pUnit.isHasPromotion(iAffinity):
						iNumSpheres -= 1
						if iNumSpheres < 1:
							break
					else:
						infoAffinity = gc.getPromotionInfo(iAffinity)
						iMana = infoAffinity.getBonusPrereq()
						for i in range(cf.getNumBonusEffective(iPlayer, iMana, pUnit)):
							listWeightedAffinities.append(iAffinity)

				for i in range(iNumSpheres):
					if len(listWeightedAffinities) > 0:
						iAffinity = listWeightedAffinities.pop(CyGame().getSorenRandNum(len(listWeightedAffinities), "Affinity-Channeling2 "+ str(pUnit.getID())))
						pUnit.setHasPromotion(iAffinity, True)
						self.onUnitPromoted([pUnit, iAffinity])



		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_AIR'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_BODY'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BODY3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BODY3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BODY2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BODY1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_CHAOS'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHAOS3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHAOS3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHAOS2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHAOS1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'):

			if iCiv == iSidar or pUnit.getReligion() == iCabal or pUnit.getRace() == gc.getInfoTypeForString('PROMOTION_GREY'):
				pUnit.setHasPromotion(iPromotion, False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'), True)
			else:
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH3')):
					pUnit.changeFreePromotionPick(1)
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH3'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH2'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH1'), False)

				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN3'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN2'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'):
			if pUnit.getRace in [gc.getInfoTypeForString('PROMOTION_UNDEAD'),gc.getInfoTypeForString('PROMOTION_DEMON')]:
				pUnit.setHasPromotion(iPromotion, False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'), True)
			else:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH3'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH2'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH1'), False)

				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN3')):
					pUnit.changeFreePromotionPick(1)
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN3'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN2'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH_ARAWN1'), False)


		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DIMENSIONAL3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DIMENSIONAL3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DIMENSIONAL2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DIMENSIONAL1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_EARTH'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_EARTH3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EARTH3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EARTH2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EARTH1'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STONESKIN'), True)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_ENCHANTMENT'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTMENT3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTMENT3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTMENT2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENTROPY3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENTROPY3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENTROPY2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENTROPY1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_FORCE'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FORCE3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FORCE3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FORCE2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FORCE1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_ICE'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ICE3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ICE3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ICE2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ICE1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_LAW'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LAW3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAW3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAW2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAW1'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REBEL'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_LIFE'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LIFE3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LIFE3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LIFE2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LIFE1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_METAMAGIC'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND1'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHARMED'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_NATURE3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NATURE3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NATURE2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NATURE1'), False)

			if not pPlayer.isBarbarian():
				numTreeTerraformer = 0
				neededTreeTerraformer = 1
				if iCiv in [	gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'),
								gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')]:
					neededTreeTerraformer += (pPlayer.getNumCities() / 3)
				for loopUnit in PyPlayer(iPlayer).getUnitList():
					if loopUnit.isHasPromotion(iPromotion):
						if loopUnit.getUnitAIType() == gc.getInfoTypeForString('UNITAI_TERRAFORMER'):
							numTreeTerraformer += 1
				if numTreeTerraformer < neededTreeTerraformer:
					pUnit.setUnitAIType(gc.getInfoTypeForString('UNITAI_TERRAFORMER'))

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOW3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOW3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOW2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOW1'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BLUR'), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOWWALK'), True)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT3'), False)
			for iProm in [	gc.getInfoTypeForString('PROMOTION_SPIRIT3'),
							gc.getInfoTypeForString('PROMOTION_SPIRIT2'),
							gc.getInfoTypeForString('PROMOTION_SPIRIT1'),
							gc.getInfoTypeForString('PROMOTION_BURNING_BLOOD'),
							gc.getInfoTypeForString('PROMOTION_PARANOID'),
							gc.getInfoTypeForString('PROMOTION_CRAZED'),
							gc.getInfoTypeForString('PROMOTION_ENRAGED')]:
				pUnit.setHasPromotion(iProm, False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUN3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUN3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUN2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUN1'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER3')):
				pUnit.changeFreePromotionPick(1)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER3'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER2'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1'), False)


		elif iPromotion == gc.getInfoTypeForString('PROMOTION_SPIRIT3'):
			for iProm in [	gc.getInfoTypeForString('PROMOTION_BURNING_BLOOD'),
							gc.getInfoTypeForString('PROMOTION_PARANOID'),
							gc.getInfoTypeForString('PROMOTION_CRAZED'),
							gc.getInfoTypeForString('PROMOTION_ENRAGED')]:
				pUnit.setHasPromotion(iProm, False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_IMMUNE_DISEASE'):
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DISEASED'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PLAGUED'), False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WITHERED'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_PERFECT_SIGHT'):
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BLIND'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_MIND3'):
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHARMED'), False)

		elif iPromotion in [	gc.getInfoTypeForString('PROMOTION_LAW3'),
								gc.getInfoTypeForString('PROMOTION_HERO'),
								gc.getInfoTypeForString('PROMOTION_LOYALTY')]:
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REBEL'), False)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_WEREWOLF'):
			if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DUIN')) > 0:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REBEL'), False)


		elif iPromotion== gc.getInfoTypeForString('PROMOTION_EARTH2'):
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STONESKIN'), True)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_NATURE2'):
			if not pPlayer.isBarbarian():
				numTreeTerraformer = 0
				neededTreeTerraformer = 1
				if iCiv in [	gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'),
						gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')]:
					neededTreeTerraformer += (pPlayer.getNumCities() / 3)
				for loopUnit in PyPlayer(iPlayer).getUnitList():
					if loopUnit.isHasPromotion(iPromotion):
						if loopUnit.getUnitAIType() == gc.getInfoTypeForString('UNITAI_TERRAFORMER'):
							numTreeTerraformer += 1
				if numTreeTerraformer < neededTreeTerraformer:
					pUnit.setUnitAIType(gc.getInfoTypeForString('UNITAI_TERRAFORMER'))

		elif iPromotion in [ gc.getInfoTypeForString('PROMOTION_WATER_WALKING'), gc.getInfoTypeForString('PROMOTION_WATER_WALKING_TEMP')]:
			if pUnit.getDomainType() == gc.getInfoTypeForString('DOMAIN_SEA'):
				pUnit.setHasPromotion(iPromotion, False)


		elif iPromotion == gc.getInfoTypeForString('PROMOTION_PACT_WITH_HYBOREM'):
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_HYBOREM'))
			if iLeader != -1:
				if pPlayer.getLeaderType() != iLeader:
					if CyGame().isLeaderEverActive(iLeader):
						iPactPlayer = cf.getLeader(iLeader)
						pPactPlayer = gc.getPlayer(iPactPlayer)
						if pPactPlayer.isAlive():
							pPactPlayer.AI_changeAttitudeExtra(iPlayer,1)
##							iPactTeam = pPactPlayer.getTeam()
##							if iTeam != iPactTeam:
##								if eTeam.isAtWar(iPactTeam) or pPactPlayer.AI_getAttitude(iPlayer) == AttitudeTypes.ATTITUDE_FURIOUS:
##									pUnit.setHasPromotion(iPromotion, False)
##						else:
##							pUnit.setHasPromotion(iPromotion, False)
##					else:
##						pUnit.setHasPromotion(iPromotion, False)
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
			if iLeader != -1:
				pPlayer2 = gc.getPlayer(iLeader)
				pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)
		elif iPromotion == gc.getInfoTypeForString('PROMOTION_PACT_WITH_JUDECCA'):
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_JUDECCA'))
			if iLeader != -1:
				if pPlayer.getLeaderType() != iLeader:
					if CyGame().isLeaderEverActive(iLeader):
						iPactPlayer = cf.getLeader(iLeader)
						pPactPlayer = gc.getPlayer(iPactPlayer)
						if pPactPlayer.isAlive():
							pPactPlayer.AI_changeAttitudeExtra(iPlayer,1)
##							iPactTeam = pPactPlayer.getTeam()
##							if iTeam != iPactTeam:
##								if eTeam.isAtWar(iPactTeam) or pPactPlayer.AI_getAttitude(iPlayer) == AttitudeTypes.ATTITUDE_FURIOUS:
##									pUnit.setHasPromotion(iPromotion, False)
##						else:
##							pUnit.setHasPromotion(iPromotion, False)
##					else:
##						pUnit.setHasPromotion(iPromotion, False)
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
			if iLeader != -1:
				pPlayer2 = gc.getPlayer(iLeader)
				pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)
		elif iPromotion == gc.getInfoTypeForString('PROMOTION_PACT_WITH_LETHE'):
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_LETHE'))
			if iLeader != -1:
				if pPlayer.getLeaderType() != iLeader:
					if CyGame().isLeaderEverActive(iLeader):
						iPactPlayer = cf.getLeader(iLeader)
						pPactPlayer = gc.getPlayer(iPactPlayer)
						if pPactPlayer.isAlive():
							pPactPlayer.AI_changeAttitudeExtra(iPlayer,1)
##							iPactTeam = pPactPlayer.getTeam()
##							if iTeam != iPactTeam:
##								if eTeam.isAtWar(iPactTeam) or pPactPlayer.AI_getAttitude(iPlayer) == AttitudeTypes.ATTITUDE_FURIOUS:
##									pUnit.setHasPromotion(iPromotion, False)
##						else:
##							pUnit.setHasPromotion(iPromotion, False)
##					else:
##						pUnit.setHasPromotion(iPromotion, False)
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
			if iLeader != -1:
				pPlayer2 = gc.getPlayer(iLeader)
				pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)
		elif iPromotion == gc.getInfoTypeForString('PROMOTION_PACT_WITH_MERESIN'):
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_MERESIN'))
			if iLeader != -1:
				if pPlayer.getLeaderType() != iLeader:
					if CyGame().isLeaderEverActive(iLeader):
						iPactPlayer = cf.getLeader(iLeader)
						pPactPlayer = gc.getPlayer(iPactPlayer)
						if pPactPlayer.isAlive():
							pPactPlayer.AI_changeAttitudeExtra(iPlayer,1)
##							iPactTeam = pPactPlayer.getTeam()
##							if iTeam != iPactTeam:
##								if eTeam.isAtWar(iPactTeam) or pPactPlayer.AI_getAttitude(iPlayer) == AttitudeTypes.ATTITUDE_FURIOUS:
##									pUnit.setHasPromotion(iPromotion, False)
##						else:
##							pUnit.setHasPromotion(iPromotion, False)
##					else:
##						pUnit.setHasPromotion(iPromotion, False)
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
			if iLeader != -1:
				pPlayer2 = gc.getPlayer(iLeader)
				pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)
		elif iPromotion == gc.getInfoTypeForString('PROMOTION_PACT_WITH_OUZZA'):
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_OUZZA'))
			if iLeader != -1:
				if pPlayer.getLeaderType() != iLeader:
					if CyGame().isLeaderEverActive(iLeader):
						iPactPlayer = cf.getLeader(iLeader)
						pPactPlayer = gc.getPlayer(iPactPlayer)
						if pPactPlayer.isAlive():
							pPactPlayer.AI_changeAttitudeExtra(iPlayer,1)
##							iPactTeam = pPactPlayer.getTeam()
##							if iTeam != iPactTeam:
##								if eTeam.isAtWar(iPactTeam) or pPactPlayer.AI_getAttitude(iPlayer) == AttitudeTypes.ATTITUDE_FURIOUS:
##									pUnit.setHasPromotion(iPromotion, False)
##						else:
##							pUnit.setHasPromotion(iPromotion, False)
##					else:
##						pUnit.setHasPromotion(iPromotion, False)
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
			if iLeader != -1:
				pPlayer2 = gc.getPlayer(iLeader)
				pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)
		elif iPromotion == gc.getInfoTypeForString('PROMOTION_PACT_WITH_SALLOS'):
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_SALLOS'))
			if iLeader != -1:
				if pPlayer.getLeaderType() != iLeader:
					if CyGame().isLeaderEverActive(iLeader):
						iPactPlayer = cf.getLeader(iLeader)
						pPactPlayer = gc.getPlayer(iPactPlayer)
						if pPactPlayer.isAlive():
							pPactPlayer.AI_changeAttitudeExtra(iPlayer,1)
##							iPactTeam = pPactPlayer.getTeam()
##							if iTeam != iPactTeam:
##								if eTeam.isAtWar(iPactTeam) or pPactPlayer.AI_getAttitude(iPlayer) == AttitudeTypes.ATTITUDE_FURIOUS:
##									pUnit.setHasPromotion(iPromotion, False)
##						else:
##							pUnit.setHasPromotion(iPromotion, False)
##					else:
##						pUnit.setHasPromotion(iPromotion, False)
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
			if iLeader != -1:
				pPlayer2 = gc.getPlayer(iLeader)
				pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)
		elif iPromotion == gc.getInfoTypeForString('PROMOTION_PACT_WITH_STATIUS'):
			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_STATIUS'))
			if iLeader != -1:
				if pPlayer.getLeaderType() != iLeader:
					if CyGame().isLeaderEverActive(iLeader):
						iPactPlayer = cf.getLeader(iLeader)
						pPactPlayer = gc.getPlayer(iPactPlayer)
						if pPactPlayer.isAlive():
							pPactPlayer.AI_changeAttitudeExtra(iPlayer,1)
##							iPactTeam = pPactPlayer.getTeam()
##							if iTeam != iPactTeam:
##								if eTeam.isAtWar(iPactTeam) or pPactPlayer.AI_getAttitude(iPlayer) == AttitudeTypes.ATTITUDE_FURIOUS:
##									pUnit.setHasPromotion(iPromotion, False)
##						else:
##							pUnit.setHasPromotion(iPromotion, False)
##					else:
##						pUnit.setHasPromotion(iPromotion, False)

			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
			if iLeader != -1:
				pPlayer2 = gc.getPlayer(iLeader)
				pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)

		elif iPromotion == iUnholyTaint:
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_ARCANE')):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ARCANE'), True)
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_SUMMONER')):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUMMONER'), True)
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_SUNDERED')):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUNDERED'), True)



			iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
			if iLeader != -1:
				pPlayer2 = gc.getPlayer(iLeader)
				pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)


			iEmpyrean = gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')
			if pUnit.getReligion() == iEmpyrean:
				pUnit.setReligion(-1)
			if not pUnit.isHiddenNationality():
				for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
					pPlayer2 = gc.getPlayer(iPlayer2)
					if pPlayer2.isAlive():
						if pPlayer2.getStateReligion() == iEmpyrean:
							pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)


		elif iPromotion == gc.getInfoTypeForString('PROMOTION_ANGEL'):
			if pUnit.getUnitCombatType() != -1:
				iMana = gc.getUnitInfo(pUnit.getUnitType()).getPrereqAndBonus()
				iNum = 0
				if iMana != -1:
					if eTeam.isBuildingClassMaxedOut(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_DIVINATION'),0):
						iNum += 1 + CyGame().getSorenRandNum(max(0,cf.getNumBonusEffective(iPlayer, iMana))//pPlayer.getUnitClassCount(iUnitClass), "Tower Free Promotions "+ pUnit.getName().encode('latin_1','replace'))
				if iUnit in [gc.getInfoTypeForString('UNIT_ANGEL_OF_DEATH'),gc.getInfoTypeForString('UNIT_TOMB_WARDEN')]:
					if eTeam.isBuildingClassMaxedOut(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_NECROMANCY'),0):
						iMana = gc.getInfoTypeForString('BONUS_MANA_DEATH')
						iNum += 1 + CyGame().getSorenRandNum(max(0,cf.getNumBonusEffective(iPlayer, iMana))//pPlayer.getUnitClassCount(iUnitClass), "Tower Free Promotions "+ pUnit.getName().encode('latin_1','replace'))
				if iNum > 0:
					pUnit.changeFreePromotionPick(iNum)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_ELEMENTAL'):
			if pUnit.getUnitCombatType() != -1:
				iMana = gc.getUnitInfo(pUnit.getUnitType()).getPrereqAndBonus()
				if iMana != -1:
					if eTeam.isBuildingClassMaxedOut(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_THE_ELEMENTS'),0):
						iNum = 1 + CyGame().getSorenRandNum(max(0,cf.getNumBonusEffective(iPlayer, iMana))//pPlayer.getUnitClassCount(iUnitClass), "Tower Free Promotions "+ pUnit.getName().encode('latin_1','replace'))
						pUnit.changeFreePromotionPick(iNum)

		elif iPromotion == gc.getInfoTypeForString('PROMOTION_UNDEAD'):
			if pUnit.getUnitCombatType() != -1:
				if eTeam.isBuildingClassMaxedOut(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_NECROMANCY'),0):
					iMana = gc.getUnitInfo(pUnit.getUnitType()).getPrereqAndBonus()
					if iMana == -1:
						iMana = gc.getInfoTypeForString('BONUS_MANA_DEATH')
					iNum = 1 + CyGame().getSorenRandNum(max(0,cf.getNumBonusEffective(iPlayer, iMana))//pPlayer.getUnitClassCount(iUnitClass), "Tower Free Promotions "+ pUnit.getName().encode('latin_1','replace'))
					pUnit.changeFreePromotionPick(iNum)

			if pPlot.isOwned():
				iPlayerPlot = pPlot.getOwner()
				if gc.getPlayer(iPlayerPlot).countNumBuildings(gc.getInfoTypeForString('BUILDING_SOUL_SHROUD')):
					cf.makeMortal(pUnit)

					iPlayer = pUnit.getOwner()
					sName = "<color=%d,%d,%d,%d>%s</color>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), pUnit.getName() )
					CyInterface().addMessage(iPlayer, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_MORTALITY", (sName, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, pUnit.getButton(), gc.getInfoTypeForString('COLOR_RED'), pUnit.getX(), pUnit.getY(), True, True)
					if iPlayer != iPlayerPlot:
						CyInterface().addMessage(iPlayerPlot, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_MORTALITY", (sName, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, pUnit.getButton(), gc.getInfoTypeForString('COLOR_GREEN'), pUnit.getX(), pUnit.getY(), True, True)
					pUnit.kill(True, iPlayerPlot)

		if pUnit.getDuration() == 0 and not pUnit.isHiddenNationality():#Diplomatic penalties for common racial slaying promotions for armies of temporary summons seem like too much, and players shouldn't know whom to punish for HN units

			if iPromotion == gc.getInfoTypeForString('PROMOTION_UNDEAD'):
				iSidar = gc.getInfoTypeForString('CIVILIZATION_SIDAR')
				iMerc = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
				if CyGame().isCivEverActive(iSidar) or CyGame().isCivEverActive(iMerc):
					for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
						pPlayer2 = gc.getPlayer(iPlayer2)
						if pPlayer2.getCivilizationType() in [iSidar, iMerc]:
							if pPlayer2.isAlive():
								pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)

			elif iPromotion == gc.getInfoTypeForString('PROMOTION_VAMPIRE_SLAYING'):
				iCalabim = gc.getInfoTypeForString('CIVILIZATION_CALABIM')
				if CyGame().isCivEverActive(iCalabim):
					for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
						pPlayer2 = gc.getPlayer(iPlayer2)
						if pPlayer2.isAlive():
							if pPlayer2.getCivilizationType() == iCalabim:
								pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)

			elif iPromotion == gc.getInfoTypeForString('PROMOTION_DEMON'):
				iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
				if iLeader != -1:
					pPlayer2 = gc.getPlayer(iLeader)
					pPlayer2.AI_changeAttitudeExtra(iPlayer, -1)

			elif iPromotion == gc.getInfoTypeForString('PROMOTION_DEMON_SLAYING'):
				iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
				iMerc = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
				if CyGame().isCivEverActive(iInfernal) or CyGame().isCivEverActive(iMerc):
					for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
						pPlayer2 = gc.getPlayer(iPlayer2)
						if pPlayer2.isAlive():
							if pPlayer2.getCivilizationType() == iInfernal:
								pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)
							elif pPlayer2.getCivilizationType() == iMerc:
								pPlayer2.AI_changeAttitudeExtra(iPlayer,1)

			elif iPromotion == gc.getInfoTypeForString('PROMOTION_EXORCIST'):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POSSESSED'), False)
				iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
				iMerc = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
				if CyGame().isCivEverActive(iInfernal) or CyGame().isCivEverActive(iMerc):
					for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
						pPlayer2 = gc.getPlayer(iPlayer2)
						if pPlayer2.isAlive():
							if pPlayer2.getCivilizationType() == iInfernal:
								pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)
							elif pPlayer2.getCivilizationType() == iMerc:
								pPlayer2.AI_changeAttitudeExtra(iPlayer,1)

			elif iPromotion == gc.getInfoTypeForString('PROMOTION_ANGEL_SLAYING'):
				iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
				iMerc = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
				if CyGame().isCivEverActive(iInfernal) or CyGame().isCivEverActive(iMerc):
					for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
						pPlayer2 = gc.getPlayer(iPlayer2)
						if pPlayer2.isAlive():
							if pPlayer2.getCivilizationType() == iInfernal:
								pPlayer2.AI_changeAttitudeExtra(iPlayer,1)
							elif pPlayer2.getCivilizationType() == iMerc:
								pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)

			elif iPromotion == gc.getInfoTypeForString('PROMOTION_ELF_SLAYING'):
				iLjos = gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR')
				iSvart = gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')
				if CyGame().isCivEverActive(iLjos) or CyGame().isCivEverActive(iSvart):
					for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
						pPlayer2 = gc.getPlayer(iPlayer2)
						if pPlayer2.isAlive():
							if pPlayer2.getCivilizationType() in [iLjos, iSvart]:
								pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)

			elif iPromotion == gc.getInfoTypeForString('PROMOTION_DWARF_SLAYING'):
				iKhazad = gc.getInfoTypeForString('CIVILIZATION_KHAZAD')
				iLuchuirp = gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP')
				if CyGame().isCivEverActive(iKhazad) or CyGame().isCivEverActive(iLuchuirp):
					for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
						pPlayer2 = gc.getPlayer(iPlayer2)
						if pPlayer2.isAlive():
							if pPlayer2.getCivilizationType() in [iKhazad, iLuchuirp]:
								pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)

			elif iPromotion == gc.getInfoTypeForString('PROMOTION_GOLEM_SLAYING'):
				iLuchuirp = gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP')
				if CyGame().isCivEverActive(iLuchuirp):
					for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
						pPlayer2 = gc.getPlayer(iPlayer2)
						if pPlayer2.isAlive():
							if pPlayer2.getCivilizationType() == iLuchuirp:
								pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)

			elif iPromotion == gc.getInfoTypeForString('PROMOTION_ORC_SLAYING'):
				iClan = gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS')
				if CyGame().isCivEverActive(iClan):
					for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
						pPlayer2 = gc.getPlayer(iPlayer2)
						if pPlayer2.isAlive():
							if pPlayer2.getCivilizationType() == iClan:
								pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)

			elif iPromotion == gc.getInfoTypeForString('PROMOTION_DRAGON_SLAYING'):
				for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
					pPlayer2 = gc.getPlayer(iPlayer2)
					if pPlayer2.isAlive():
						if cf.isHasDragon(pPlayer2):
							pPlayer2.AI_changeAttitudeExtra(iPlayer,-1)

			elif iPromotion == gc.getInfoTypeForString('PROMOTION_WEREWOLF_SLAYING'):
				iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_DUIN'))
				if iLeader != -1:
					pPlayer2 = gc.getPlayer(iLeader)
					pPlayer2.AI_changeAttitudeExtra(iPlayer, -1)

		for iProm in xrange(gc.getNumPromotionInfos()):
			if pUnit.isPromotionImmune(iProm):
				pUnit.setHasPromotion(iProm, False)
##			if infoProm.isPromotionImmune(iProm):
##				pUnit.setHasPromotion(iProm, False)


		if not self.__LOG_UNITPROMOTED:
			return
		CvUtil.pyPrint('Unit Promotion Event: %s - %s' %(player.getCivilizationName(), pUnit.getName(),))

	def onUnitSelected(self, argsList):
		'Unit Selected'
		unit = argsList[0]
		player = PyPlayer(unit.getOwner())
		if (not self.__LOG_UNITSELECTED):
			return
		CvUtil.pyPrint('%s was selected by Player %d Civilization %s'
			%(PyInfo.UnitInfo(unit.getUnitType()).getDescription(), player.getID(), player.getCivilizationName()))

	def onUnitRename(self, argsList):
		'Unit is renamed'
		pUnit = argsList[0]
		if (pUnit.getOwner() == gc.getGame().getActivePlayer()):
			self.__eventEditUnitNameBegin(pUnit)

	def onUnitPillage(self, argsList):
		'Unit pillages a plot'
		pUnit, iImprovement, iRoute, iOwner = argsList
		iPlotX = pUnit.getX()
		iPlotY = pUnit.getY()
##		pPlot = CyMap().plot(iPlotX, iPlotY)
##		pPlayer = gc.getPlayer(pUnit.getOwner())

		if (not self.__LOG_UNITPILLAGE):
			return
		CvUtil.pyPrint("Player %d's %s pillaged improvement %d and route %d at plot at (%d, %d)"
			%(iOwner, PyInfo.UnitInfo(pUnit.getUnitType()).getDescription(), iImprovement, iRoute, iPlotX, iPlotY))

	def onUnitSpreadReligionAttempt(self, argsList):
		'Unit tries to spread religion to a city'
		pUnit, iReligion, bSuccess = argsList

##		iX = pUnit.getX()
##		iY = pUnit.getY()
##		pPlot = CyMap().plot(iX, iY)
##		pCity = pPlot.getPlotCity()
		if bSuccess:
			cf.makeMortal(pUnit)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION'), True)

	def onUnitGifted(self, argsList):
		'Unit is gifted from one player to another'
		pUnit, iGiftingPlayer, pPlotLocation = argsList

	def onUnitBuildImprovement(self, argsList):
		'Unit begins enacting a Build (building an Improvement or Route)'
		pUnit, iBuild, bFinished = argsList

	def onGoodyReceived(self, argsList):
		'Goody received'
		iPlayer, pPlot, pUnit, iGoodyType = argsList
		if (not self.__LOG_GOODYRECEIVED):
			return
		CvUtil.pyPrint('%s received a goody' %(gc.getPlayer(iPlayer).getCivilizationDescription(0)),)

	def onGreatPersonBorn(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Unit Promoted'
		pUnit, iPlayer, pCity = argsList
		player = PyPlayer(iPlayer)
		if pUnit.isNone() or pCity.isNone():
			return
		if (not self.__LOG_GREATPERSON):
			return
		CvUtil.pyPrint('A %s was born for %s in %s' %(pUnit.getName(), player.getCivilizationName(), pCity.getName()))

	def onTechAcquired(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Tech Acquired'
		iTechType, iTeam, iPlayer, bAnnounce = argsList
		# Note that iPlayer may be NULL (-1) and not a refer to a player object
		pPlayer = gc.getPlayer(iPlayer)
		# Show tech splash when applicable
		if iPlayer > -1 and bAnnounce and not CyInterface().noTechSplash():
			if gc.getGame().isFinalInitialized() and not gc.getGame().GetWorldBuilderMode():
				if not gc.getGame().isNetworkMultiPlayer() and iPlayer == gc.getGame().getActivePlayer():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setData1(iTechType)
					popupInfo.setText(u"showTechSplash")
					popupInfo.addPopup(iPlayer)

		if iTechType in [gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL'), gc.getInfoTypeForString('TECH_OMNISCIENCE')]:
			iMask = gc.getInfoTypeForString('EQUIPMENT_MASK_KYLORIN')
			if CyGame().getUnitCreatedCount(iMask) < 1:
				pHiddingPlace = cf.findImprovement(gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES'))
				if pHiddingPlace != -1:
					newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(iMask, pHiddingPlace.getX(), pHiddingPlace.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iTechType in [gc.getInfoTypeForString('TECH_PASS_THROUGH_THE_ETHER'), gc.getInfoTypeForString('TECH_OMNISCIENCE')]:
			iMask = gc.getInfoTypeForString('EQUIPMENT_MASK_GABELLA')
			if CyGame().getUnitCreatedCount(iMask) < 1:
				pHiddingPlace = cf.findImprovement(gc.getInfoTypeForString('IMPROVEMENT_TAPESTRY_HOUSE'))
				if pHiddingPlace != -1:
					newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(iMask, pHiddingPlace.getX(), pHiddingPlace.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iTechType in [gc.getInfoTypeForString('TECH_MALEVOLENT_DESIGNS'), gc.getInfoTypeForString('TECH_OMNISCIENCE')]:
			iMask = gc.getInfoTypeForString('EQUIPMENT_MASK_ASMODAY')
			if CyGame().getUnitCreatedCount(iMask) < 1 and CyGame().getUnitCreatedCount(gc.getInfoTypeForString('UNIT_ASMODAY'))< 1:
				pHiddingPlace = cf.findImprovement(gc.getInfoTypeForString('IMPROVEMENT_GRAVE_OF_ASMODAY'))
				if pHiddingPlace != -1:
					newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(iMask, pHiddingPlace.getX(), pHiddingPlace.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iTechType in [gc.getInfoTypeForString('TECH_RELIGIOUS_LAW'), gc.getInfoTypeForString('TECH_OMNISCIENCE')]:
			iMask = gc.getInfoTypeForString('EQUIPMENT_MASK_BARBATOS')
			if CyGame().getUnitCreatedCount(iMask) < 1 and CyGame().getUnitCreatedCount(gc.getInfoTypeForString('UNIT_BARBATOS')) < 1:
				pHiddingPlace = cf.findImprovement(gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER'))
				if pHiddingPlace != -1:
					newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(iMask, pHiddingPlace.getX(), pHiddingPlace.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iTechType in [gc.getInfoTypeForString('TECH_RAGE'), gc.getInfoTypeForString('TECH_OMNISCIENCE')]:
			iMask = gc.getInfoTypeForString('EQUIPMENT_MASK_ALEXIS')
			if CyGame().getUnitCreatedCount(iMask) < 1:
				pHiddingPlace = cf.findImprovement(gc.getInfoTypeForString('IMPROVEMENT_REMNANTS_OF_PATRIA'))
				if pHiddingPlace != -1:
					newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(iMask, pHiddingPlace.getX(), pHiddingPlace.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iTechType in [gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL'), gc.getInfoTypeForString('TECH_OMNISCIENCE')]:
			iMask = gc.getInfoTypeForString('EQUIPMENT_MASK_FAERYL')
			if CyGame().getUnitCreatedCount(iMask) < 1:
				iFaerylPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_FAERYL'))
				if iFaerylPlayer != -1:
					cf.giftUnitToPlayer(iMask, iFaerylPlayer, 0, -1, -1,-1)


		if iPlayer != -1 and iPlayer != gc.getBARBARIAN_PLAYER():
			pPlayer = gc.getPlayer(iPlayer)
			iStateReligion = pPlayer.getStateReligion()
			iReligion = -1
			iCiv = pPlayer.getCivilizationType()
			iPriestClass = -1
			if iTechType == gc.getInfoTypeForString('TECH_PRIESTHOOD'):
				iStateReligion = pPlayer.getStateReligion()
				if iStateReligion == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_ORDER')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_EMPYREAN')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_KILMORPH')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_LEAVES')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_OVERLORDS')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_ESUS')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_VEIL')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_WINTER')


				elif iStateReligion == gc.getInfoTypeForString('RELIGION_UNBLEMISHED'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_DRUID')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_SIRONA')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_HOUSE_OF_PLENTY'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_PLENTY')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_FOXMEN'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_FOXMEN')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_MATRONAE'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_APOSTATE')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_LAERAN_CORD'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_LAERAN')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_STEWARD')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_COVEN'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_MOBIUS_WITCH')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_ANOINTED'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_ANOINTED')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_LUONNOTAR')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_RINGGIVER'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_RINGGIVER')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_ARAWN')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_GREY_COUNCIL'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_GREY')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_EMBER_LEGION'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_EMBER_LEGION')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_DISCORD')


				if iPriestClass != -1:
					iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iPriestClass)
					if iUnit != -1:
						cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,iStateReligion)

			elif iTechType == gc.getInfoTypeForString('TECH_THEOLOGY'):
				iStateReligion = pPlayer.getStateReligion()
				if iStateReligion == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_ORDER')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_EMPYREAN')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_KILMORPH')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_LEAVES')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_OVERLORDS')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_ESUS')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_VEIL')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_WINTER')

				elif iStateReligion == gc.getInfoTypeForString('RELIGION_RINGGIVER'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_RINGGIVER')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_SIRONA')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_UNBLEMISHED'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_REBORN')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_LAERAN_CORD'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_LAERAN')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_DISCORD')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_ANOINTED'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_ANOINTED')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_LUONNOTAR')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_MATRONAE'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_APOSTATE')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_ARAWN')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_STEWARD')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_COVEN'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_EATER_OF_DREAMS')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_GREY_COUNCIL'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_GREY')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_HOUSE_OF_PLENTY'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_PLENTY')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_FOXMEN'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_FOXMEN')
				elif iStateReligion == gc.getInfoTypeForString('RELIGION_EMBER_LEGION'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_EMBER_LEGION')

				if iPriestClass != -1:
					iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iPriestClass)
					if iUnit != -1:
						cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,iStateReligion)

			elif iTechType == gc.getInfoTypeForString('TECH_ORDERS_FROM_HEAVEN'):
				iReligion = gc.getInfoTypeForString('RELIGION_THE_ORDER')
				iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_ORDER')
			elif iTechType == gc.getInfoTypeForString('TECH_HONOR'):
				iReligion = gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')
				iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_EMPYREAN')
			elif iTechType == gc.getInfoTypeForString('TECH_WAY_OF_THE_EARTHMOTHER'):
				iReligion = gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH')
				iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_KILMORPH')
			elif iTechType == gc.getInfoTypeForString('TECH_WAY_OF_THE_FORESTS'):
				iReligion = gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')
				iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_LEAVES')
			elif iTechType == gc.getInfoTypeForString('TECH_MESSAGE_FROM_THE_DEEP'):
				iReligion = gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS')
				iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_OVERLORDS')
			elif iTechType == gc.getInfoTypeForString('TECH_DECEPTION'):
				iReligion = gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS')
				iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_ESUS')
			elif iTechType == gc.getInfoTypeForString('TECH_CORRUPTION_OF_SPIRIT'):
				iReligion = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
				iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_VEIL')
			elif iTechType == gc.getInfoTypeForString('TECH_WAY_OF_THE_WISE') and pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_VARN'):
				iReligion = gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')
			elif iTechType == gc.getInfoTypeForString('TECH_ARCANE_LORE'):

				if iCiv == gc.getInfoTypeForString('CIVILIZATION_GRIGORI'):
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_7')):
						iReligion = gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE')

			elif iTechType == gc.getInfoTypeForString('TECH_SORCERY'):
				iClass = gc.getInfoTypeForString('UNITCLASS_MAGE')
				if iClass != -1:
					iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iClass)
					if iUnit != -1:
						cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,-1)

			elif iTechType == gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL'):
				iClass = gc.getInfoTypeForString('UNITCLASS_ARCHMAGE')
				if iClass != -1:
					iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iClass)
					if iUnit != -1:
						cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,-1)

			elif iTechType == gc.getInfoTypeForString('TECH_ANIMAL_MASTERY'):
				iClass = gc.getInfoTypeForString('UNITCLASS_BEASTMASTER')
				if iClass != -1:
					iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iClass)
					if iUnit != -1:
						cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,-1)

			elif iTechType == gc.getInfoTypeForString('TECH_WARHORSES'):
				iClass = gc.getInfoTypeForString('UNITCLASS_KNIGHT')
				if iClass != -1:
					iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iClass)
					if iUnit != -1:
						cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,-1)



			if iTechType == gc.getInfoTypeForString('TECH_MYSTICISM'):
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS'):
					iPriestClass = gc.getInfoTypeForString('UNITCLASS_DISCIPLE_EMBER_LEGION')
					if iPriestClass != -1:
						iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iPriestClass)
						if iUnit != -1:
							cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,gc.getInfoTypeForString('RELIGION_EMBER_LEGION'))

			if iTechType == gc.getInfoTypeForString('TECH_ELEMENTALISM'):
				iStateReligion = pPlayer.getStateReligion()
				if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_EMBER_LEGION'):

					if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_THEOLOGY')):
						iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_EMBER_LEGION')
						if iPriestClass != -1:
							iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iPriestClass)
							if iUnit != -1:
								cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,iStateReligion)
					elif pPlayer.isHasTech(gc.getInfoTypeForString('TECH_PRIESTHOOD')):
						iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_EMBER_LEGION')
						if iPriestClass != -1:
							iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iPriestClass)
							if iUnit != -1:
								cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,iStateReligion)
					else:
						iPriestClass = gc.getInfoTypeForString('UNITCLASS_DISCIPLE_EMBER_LEGION')
						if iPriestClass != -1:
							iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iPriestClass)
							if iUnit != -1:
								cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,iStateReligion)

				if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):

					if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_THEOLOGY')):
						iPriestClass = gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_WINTER')
						if iPriestClass != -1:
							iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iPriestClass)
							if iUnit != -1:
								cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,iStateReligion)
					elif pPlayer.isHasTech(gc.getInfoTypeForString('TECH_PRIESTHOOD')):
						iPriestClass = gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_WINTER')
						if iPriestClass != -1:
							iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iPriestClass)
							if iUnit != -1:
								cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,iStateReligion)
					else:
						iPriestClass = gc.getInfoTypeForString('UNITCLASS_DISCIPLE_HAND')
						if iPriestClass != -1:
							iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iPriestClass)
							if iUnit != -1:
								cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,iStateReligion)


			if iCiv == gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
				if iTechType == gc.getInfoTypeForString('TECH_ANIMAL_MASTERY'):
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_HERALD'), iPlayer)
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_HERALD'), iPlayer)
				elif iTechType == gc.getInfoTypeForString('TECH_DIVINE_ESSENCE'):
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_VALKYRIE'), iPlayer)
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_VALKYRIE'), iPlayer)
				elif iTechType == gc.getInfoTypeForString('TECH_GUILDS'):
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_ANGEL_OF_DEATH'), iPlayer)
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_ANGEL_OF_DEATH'), iPlayer)
				elif iTechType == gc.getInfoTypeForString('TECH_RAGE'):
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_SERAPH'), iPlayer)
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_SERAPH'), iPlayer)
				elif iTechType == gc.getInfoTypeForString('TECH_RIGHTEOUSNESS'):
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_REPENTANT_ANGEL'), iPlayer)
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_REPENTANT_ANGEL'), iPlayer)
				elif iTechType == gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL'):
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_RUNEWYN'), iPlayer)
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_RUNEWYN'), iPlayer)
				elif iTechType == gc.getInfoTypeForString('TECH_WARHORSES'):
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_OPHANIM'), iPlayer)
					cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_OPHANIM'), iPlayer)

			if not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ACHERON):

				if iTechType == gc.getInfoTypeForString('TECH_FANATICISM'):
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CARDITH'):
						cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_DRAGON_FANATIC_GOLD'), iPlayer)
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TEBRYN'):
						cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_DRAGON_FANATIC_OBSIDIAN'), iPlayer)
				elif iTechType == gc.getInfoTypeForString('TECH_RIGHTEOUSNESS') and iCiv == gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
					iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_CULT_OF_DRAGON_BONES')
					triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, iPlayer, -1, -1, -1, -1, -1)
				elif iTechType == gc.getInfoTypeForString('TECH_MALEVOLENT_DESIGNS') and pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TEBRYN'):
					iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_CULT_OF_DRAGON_BONES')
					triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, iPlayer, -1, -1, -1, -1, -1)


			if iReligion != -1:

				iUnitClass = gc.getReligionInfo(iReligion).getFreeUnitClass()
				if iPriestClass != -1:
					if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_PRIESTHOOD')):
						iUnitClass = iPriestClass
				if iUnitClass != -1:
					iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(iUnitClass)
					if iUnit != -1:
						cf.giftUnitToPlayer(iUnit, iPlayer, 0, -1, -1,iReligion)


				if iReligion == pPlayer.getFavoriteReligion():
					pCity = pPlayer.getCapitalCity()
					if not pCity.isNone():
						pCity.setHasReligion(iReligion,True,True,True)
				elif iTechType in [gc.getInfoTypeForString('TECH_ARCANE_LORE'), gc.getInfoTypeForString('TECH_WAY_OF_THE_WISE')]:
					pPlayer.foundReligion(iReligion, iReligion, True)

		if CyGame().getWBMapScript():
			sf.onTechAcquired(iTechType, iTeam, iPlayer, bAnnounce)

		if (not self.__LOG_TECH):
			return
		CvUtil.pyPrint('%s was finished by Team %d'
			%(PyInfo.TechnologyInfo(iTechType).getDescription(), iTeam))

	def onTechSelected(self, argsList):
		'Tech Selected'
		iTechType, iPlayer = argsList
		if (not self.__LOG_TECH):
			return
		CvUtil.pyPrint('%s was selected by Player %d' %(PyInfo.TechnologyInfo(iTechType).getDescription(), iPlayer))

	def onReligionFounded(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Religion Founded'
		iReligion, iFounder = argsList
		player = PyPlayer(iFounder)
		pPlayer = gc.getPlayer(iFounder)

		iCityId = gc.getGame().getHolyCity(iReligion).getID()
		pCity = pPlayer.getCity(iCityId)
		if pCity.isSettlement() or pCity.isNone():
			pCityC = pPlayer.getCapitalCity()
			if pCityC.isNone():
				iCityCId = pCityC.getID()
				if iCityCId != iCityId:
					gc.getGame().clearHolyCity(iReligion)
					pCity.setHasReligion(iReligion,False,False,True)
					pCityC.setHasReligion(iReligion,True,False,True)
					gc.getGame().setHolyCity(iReligion, pCity, False)
					iCityId = iCityCId

		if gc.getGame().isFinalInitialized() and not gc.getGame().GetWorldBuilderMode():
			if not gc.getGame().isNetworkMultiPlayer() and iFounder == gc.getGame().getActivePlayer():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(iReligion)
				popupInfo.setData2(iCityId)
				if iReligion in [	gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'),
									gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'),
									gc.getInfoTypeForString('RELIGION_WHITE_HAND'),
									gc.getInfoTypeForString('RELIGION_MATRONAE'),
									gc.getInfoTypeForString('RELIGION_UNBLEMISHED'),
									gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS'),
									gc.getInfoTypeForString('RELIGION_LAERAN_CORD'),
									gc.getInfoTypeForString('RELIGION_FOXMEN'),
									gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON'),
									gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY'),
									gc.getInfoTypeForString('RELIGION_COVEN'),
									gc.getInfoTypeForString('RELIGION_ANOINTED'),
									gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE')
									]:
					popupInfo.setData3(3)
				else:
					popupInfo.setData3(1)
				popupInfo.setText(u"showWonderMovie")
				popupInfo.addPopup(iFounder)

		if iReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
			iCiv = gc.getInfoTypeForString('CIVILIZATION_CALABIM')
			for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
				player2 = gc.getPlayer(iPlayer2)
				if player2.isAlive():
					if player2.getCivilizationType() == iCiv:
						player2.AI_changeAttitudeExtra(iFounder,-6)
		elif iReligion == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
			iCiv = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
			for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
				player2 = gc.getPlayer(iPlayer2)
				if player2.isAlive():
					if player2.getCivilizationType() == iCiv:
						player2.AI_changeAttitudeExtra(iFounder,-6)
		elif iReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
			iCiv = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
			for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
				player2 = gc.getPlayer(iPlayer2)
				if player2.isAlive():
					if player2.getCivilizationType() == iCiv:
						player2.AI_changeAttitudeExtra(iFounder,-2)

		elif iReligion == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS'):
			iCiv = gc.getInfoTypeForString('CIVILIZATION_ELOHIM')
			for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
				player2 = gc.getPlayer(iPlayer2)
				if player2.isAlive():
					if player2.getCivilizationType() == iCiv:
						player2.AI_changeAttitudeExtra(iFounder,3)
		elif iReligion == gc.getInfoTypeForString('RELIGION_COVEN'):
			iCiv = gc.getInfoTypeForString('CIVILIZATION_SHEAIM')
			for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
				player2 = gc.getPlayer(iPlayer2)
				if player2.isAlive():
					if player2.getCivilizationType() == iCiv:
						player2.AI_changeAttitudeExtra(iFounder,3)
		elif iReligion == gc.getInfoTypeForString('RELIGION_ANOINTED'):
			iCiv = gc.getInfoTypeForString('CIVILIZATION_CALABIM')
			for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
				player2 = gc.getPlayer(iPlayer2)
				if player2.isAlive():
					if player2.getCivilizationType() == iCiv:
						player2.AI_changeAttitudeExtra(iFounder,3)
		elif iReligion == gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY'):
			iCiv = gc.getInfoTypeForString('CIVILIZATION_BALSERAPHS')
			for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
				player2 = gc.getPlayer(iPlayer2)
				if player2.isAlive():
					if player2.getCivilizationType() == iCiv:
						player2.AI_changeAttitudeExtra(iFounder,3)


		if CyGame().getWBMapScript():
			sf.onReligionFounded(iReligion, iFounder)

		if (not self.__LOG_RELIGION):
			return
		CvUtil.pyPrint('Player %d Civilization %s has founded %s'
			%(iFounder, player.getCivilizationName(), gc.getReligionInfo(iReligion).getDescription()))

	def onReligionSpread(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Religion Has Spread to a City'
		iReligion, iOwner, pSpreadCity = argsList
		player = PyPlayer(iOwner)
		pPlayer = gc.getPlayer(iOwner)
		eTeam = gc.getTeam(pPlayer.getTeam())

		iCiv = pPlayer.getCivilizationType()
		iStateRel = pPlayer.getStateReligion()
		iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')

		iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
		iEmpyrean = gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')
		iRunes = gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH')
		iLeaves = gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')
		iUndertow = gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS')
		iEsus = gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS')
		iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')

		iHand = gc.getInfoTypeForString('RELIGION_WHITE_HAND')
		iMatronae = gc.getInfoTypeForString('RELIGION_MATRONAE')

		iUnblemished = gc.getInfoTypeForString('RELIGION_UNBLEMISHED')
		iBrotherhood = gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS')
		iLaeran = gc.getInfoTypeForString('RELIGION_LAERAN_CORD')
		iFoxmen = gc.getInfoTypeForString('RELIGION_FOXMEN')
		iDragonCult = gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON')
		iStewards = gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY')
		iCoven = gc.getInfoTypeForString('RELIGION_COVEN')
		iAnointed = gc.getInfoTypeForString('RELIGION_ANOINTED')
		iOne = gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE')



		iPlenty = gc.getInfoTypeForString('RELIGION_HOUSE_OF_PLENTY')
		iRinggiver = gc.getInfoTypeForString('RELIGION_RINGGIVER')
		iEternalCabal = gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL')
		iGrey = gc.getInfoTypeForString('RELIGION_GREY_COUNCIL')
		iLegion = gc.getInfoTypeForString('RELIGION_EMBER_LEGION')
		iDiscord = gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD')

		sName = pSpreadCity.getName()


		dGameOptionDisables = {
									iEmpyrean		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_0'),
									iBrotherhood	:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_1'),
									iRinggiver		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_2'),
									iUnblemished	:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_3'),
									iPlenty			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_4'),
									iOrder			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_5'),
									iMatronae		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_6'),
									iOne			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_7'),

									iEternalCabal	:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_8'),
									iLaeran			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_9'),
									iUndertow		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_10'),
									iGrey			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_11'),
									iRunes			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_12'),
									iLeaves			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_13'),
									iFoxmen			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_14'),
									iDragonCult		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_15'),

									iEsus			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_16'),
									iHand			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_17'),
									iStewards		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_18'),
									iDiscord		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_19'),
									iAnointed		:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_20'),
									iVeil			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_21'),
									iLegion			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_22'),
									iCoven			:	gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_23')
				}
		if iReligion in dGameOptionDisables:
			iGameOption = dGameOptionDisables[iReligion]
			if gc.getGame().isOption(iGameOption):
				pSpreadCity.setHasReligion(iReligion, False, True, True)
				gc.getGame().clearHolyCity(iReligion)
				return


		if iReligion == iMatronae:

			if iStateRel not in [-1, iMatronae] and pSpreadCity.isHasReligion(iStateRel):
				pSpreadCity.setOccupationTimer(3)
				CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MATRONAE_REVOLT",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Matronae.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

			if CyGame().getSorenRandNum(10, "Religious conflict") < 8:
				for iTarget in xrange(gc.getNumReligionInfos()):
					if iTarget != iMatronae:
						if pSpreadCity.isHasReligion(iTarget):
							result = CyGame().getSorenRandNum(100, "Matronae")
							if result > 35:
								if cf.removeReligion(iTarget, pSpreadCity):
									CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_MATRONAE",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Matronae.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

		elif pSpreadCity.isHasReligion(iMatronae):

			if CyGame().getSorenRandNum(10, "Religious conflict") < 8:
				for iTarget in xrange(gc.getNumReligionInfos()):
					if iTarget != iMatronae:
						if pSpreadCity.isHasReligion(iTarget):
							result = CyGame().getSorenRandNum(100, "Matronae")
							if result > 35:
								if cf.removeReligion(iTarget, pSpreadCity):
									CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_MATRONAE",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Matronae.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)



		if iReligion == iOne:

			if iStateRel != -1:
				if pSpreadCity.isHasReligion(iStateRel):
					pSpreadCity.setOccupationTimer(3)
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_THE_ONE_REVOLT",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/colorwheel.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

			if CyGame().getSorenRandNum(10, "Religious conflict") < 8:
				for iTarget in xrange(gc.getNumReligionInfos()):
					if iTarget != iOne:
						if pSpreadCity.isHasReligion(iTarget):
							result = CyGame().getSorenRandNum(100, "Children of the One")
							if result < 35:
								if cf.removeReligion(iOne, pSpreadCity):
									CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_LUONNOTAR_FLEE",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/colorwheel.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
									if pSpreadCity.getPopulation() > 1:
										pSpreadCity.changePopulation(-1)
									break
							elif cf.removeReligion(iTarget, pSpreadCity):
								CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_LUONNOTAR_ACCEPTED",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/colorwheel.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
		elif pSpreadCity.isHasReligion(iOne):
			result = CyGame().getSorenRandNum(100, "Children of the One")
			if result < 5:
				if cf.removeReligion(iOne, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_LUONNOTAR_FLEE",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/colorwheel.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
					if pSpreadCity.getPopulation() > 1:
						pSpreadCity.changePopulation(-1)
			elif cf.removeReligion(iOrder, pSpreadCity):
				CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_LUONNOTAR_ACCEPTED",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/colorwheel.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)



		if iReligion == iOrder:
			if iCiv == iInfernal:
				cf.removeReligion(iOrder, pSpreadCity)
			elif CyGame().getSorenRandNum(10, "Religious conflict") < 8:

				if pSpreadCity.isHasReligion(iVeil):
					result = CyGame().getSorenRandNum(100, "Order-Veil")
					if result < 35:
						if cf.removeReligion(iVeil, pSpreadCity):
							CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_ORDER_VEIL",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Order.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
							CyGame().changeGlobalCounter(-1)
							if pSpreadCity.getPopulation() > 1:
								pSpreadCity.changePopulation(-1)
					elif cf.removeReligion(iOrder, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_VEIL_ORDER",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Ashen.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				if pSpreadCity.isHasReligion(iUndertow):
					result = CyGame().getSorenRandNum(100, "Order-Overlords")
					if result < 35:
						if cf.removeReligion(iUndertow, pSpreadCity):
							CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_ORDER_OVERLORDS",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Order.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
							CyGame().changeGlobalCounter(-1)
							if pSpreadCity.getPopulation() > 1:
								pSpreadCity.changePopulation(-1)
					elif cf.removeReligion(iOrder, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_OVERLORDS_ORDER",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Overlords.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

			if iStateRel == iOrder and pSpreadCity.isHasReligion(iOrder):
				if CyGame().getGameTurn() != CyGame().getStartTurn():
					if pSpreadCity.getOccupationTimer() <= 0:
						if CyGame().getSorenRandNum(100, "Order Spawn") < gc.getDefineINT('ORDER_SPAWN_CHANCE'):
							if eTeam.isHasTech(gc.getInfoTypeForString('TECH_FANATICISM')):
								iUnit = gc.getInfoTypeForString('UNIT_CRUSADER')
								CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ORDER_SPAWN_CRUSADER",()),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Units/Crusader.dds',ColorTypes(8),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
							elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_PRIESTHOOD')):
								iUnit = gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_ORDER')
								CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ORDER_SPAWN_CONFESSOR",()),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Units/Priest Order.dds',ColorTypes(8),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
							else:
								iUnit = gc.getInfoTypeForString('UNIT_DISCIPLE_THE_ORDER')
								CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ORDER_SPAWN_ACOLYTE",()),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Units/Disciple Order.dds',ColorTypes(8),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
							newUnit = pPlayer.initUnit(iUnit, pSpreadCity.getX(), pSpreadCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		elif iReligion == iEmpyrean:

			if iCiv == iInfernal:
				cf.removeReligion(iEmpyrean, pSpreadCity)
			elif CyGame().getSorenRandNum(10, "Religious conflict") < 8:

				if pSpreadCity.isHasReligion(iEsus):
					result = CyGame().getSorenRandNum(100, "Empyrean-Esus")
					if result < 35:
						if cf.removeReligion(iVeil, pSpreadCity):
							CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_EMPYREAN_ESUS",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Empyrean.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
					elif cf.removeReligion(iEmpyrean, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_ESUS_EMPYREAN",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Council of Esus.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				if pSpreadCity.isHasReligion(iVeil):
					result = CyGame().getSorenRandNum(100, "Empyrean-Veil")
					if result < 35:
						if cf.removeReligion(iVeil, pSpreadCity):
							CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_EMPYREAN_VEIL",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Empyrean.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
							CyGame().changeGlobalCounter(-1)
							if pSpreadCity.getPopulation() > 1:
								pSpreadCity.changePopulation(-1)
					elif cf.removeReligion(iEmpyrean, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_VEIL_EMPYREAN",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Ashen.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

		elif iReligion == iRunes:

			if pSpreadCity.isHasReligion(iStewards):
				result = CyGame().getSorenRandNum(100, "Runes-Stewards")
				if result < 35:
					if cf.removeReligion(iStewards, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_RUNES_STEWARDS",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Runes.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				elif cf.removeReligion(iRunes, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_STEWARDS_RUNES",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/StewardsOfInequity.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

			if pSpreadCity.isHasReligion(iFoxmen):
				result = CyGame().getSorenRandNum(100, "Runes-Foxmen")
				if result < 35:
					if cf.removeReligion(iFoxmen, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_RUNES_TALI",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Runes.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				elif cf.removeReligion(iRunes, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_TALI_RUNES",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Foxmen.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)


		elif iReligion == iLeaves:

			if pSpreadCity.isHasReligion(iHand):
				result = CyGame().getSorenRandNum(100, "Leaves-Hand")
				if result < 35:
					if cf.removeReligion(iHand, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_LEAVES_HAND",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Thewhitehand.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				elif cf.removeReligion(iLeaves, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_HAND_LEAVES",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Fellowship.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)


		elif iReligion == iUndertow:
			if iCiv == iMercurians:
				cf.removeReligion(iUndertow, pSpreadCity)
			elif CyGame().getSorenRandNum(10, "Religious conflict") < 8:

				if pSpreadCity.isHasReligion(iOrder):
					result = CyGame().getSorenRandNum(100, "Overlords-Order")
					if result < 35:
						if cf.removeReligion(iOrder, pSpreadCity):
							CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_OVERLORDS_ORDER",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Overlords.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
							CyGame().changeGlobalCounter(1)
							if pSpreadCity.getPopulation() > 1:
								pSpreadCity.changePopulation(-1)
					elif cf.removeReligion(iUndertow, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_ORDER_OVERLORDS",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Order.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

		elif iReligion == iEsus:
			if CyGame().getSorenRandNum(10, "Religious conflict") < 8:

				if pSpreadCity.isHasReligion(iEmpyrean):
					result = CyGame().getSorenRandNum(100, "Esus-Empyrean")
					if result < 35:
						if cf.removeReligion(iEmpyrean, pSpreadCity):
							CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_ESUS_EMPYREAN",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Council of Esus.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
							if pSpreadCity.getPopulation() > 1:
								pSpreadCity.changePopulation(-1)
					elif cf.removeReligion(iEsus, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_EMPYREAN_ESUS",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Empyrean.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)#I got an error in this line when starting a game on the 21 civilization map, but have not yet discovered why nor been able to replicate it

		elif iReligion == iVeil:
			if iCiv == iMercurians:
				cf.removeReligion(iVeil, pSpreadCity)
			elif CyGame().getSorenRandNum(10, "Religious conflict") < 8:

				if pSpreadCity.isHasReligion(iOrder):
					result = CyGame().getSorenRandNum(100, "Veil-Order")
					if result < 35:
						if cf.removeReligion(iOrder, pSpreadCity):
							CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_VEIL_ORDER",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Ashen.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
							CyGame().changeGlobalCounter(1)
							if pSpreadCity.getPopulation() > 1:
								pSpreadCity.changePopulation(-1)
					elif cf.removeReligion(iVeil, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_ORDER_VEIL",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Order.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				if pSpreadCity.isHasReligion(iEmpyrean):
					result = CyGame().getSorenRandNum(100, "Veil-Empyrean")
					if result < 35:
						if cf.removeReligion(iEmpyrean, pSpreadCity):
							CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_VEIL_EMPYREAN",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Ashen.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)
							CyGame().changeGlobalCounter(1)
							if pSpreadCity.getPopulation() > 1:
								pSpreadCity.changePopulation(-1)
					elif cf.removeReligion(iVeil, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_EMPYREAN_VEIL",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Empyrean.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)



		elif iReligion == iUnblemished:
			if pSpreadCity.isHasReligion(iEternalCabal):
				result = CyGame().getSorenRandNum(100, "Unblemished-Cabal")
				if result > 35:
					if cf.removeReligion(iEternalCabal, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_SUCELLUS_ARAWN",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/TheUnblemished.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				elif cf.removeReligion(iUnblemished, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_ARAWN_SUCELLUS",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/EternalCabal.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

			if pSpreadCity.isHasReligion(iHand):
				result = CyGame().getSorenRandNum(100, "Unblemished-Hand")
				if result > 35:
					if cf.removeReligion(iHand, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_SUCELLUS_MULCARN",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/TheUnblemished.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				elif cf.removeReligion(iUnblemished, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_MULCARN_SUCELLUS",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/EternalCabal.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

		elif iReligion == iBrotherhood:
			if pSpreadCity.isHasReligion(iAnointed):
				result = CyGame().getSorenRandNum(100, "Brotherhood-Anointed")
				if result > 35:
					if cf.removeReligion(iAnointed, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_SIRONA_AERON",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Occis.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				elif cf.removeReligion(iBrotherhood, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_AERON_SIRONA",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/BrotherhoodOfWardens.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

		elif iReligion == iLaeran:

			if pSpreadCity.isHasReligion(iStewards):
				result = CyGame().getSorenRandNum(100, "Runes-Stewards")
				if result < 35:
					if cf.removeReligion(iStewards, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_OGHMA_STEWARDS",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Runes.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				elif cf.removeReligion(iLaeran, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_STEWARDS_OGHMA",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/LaeranCord.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)


		elif iReligion == iFoxmen:
			if pSpreadCity.isHasReligion(iRunes):
				result = CyGame().getSorenRandNum(100, "Runes-Foxmen")
				if result > 35:
					if cf.removeReligion(iFoxmen, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_RUNES_TALI",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Runes.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				elif cf.removeReligion(iRunes, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_TALI_RUNES",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Foxmen.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

			if pSpreadCity.isHasReligion(iHand):
				result = CyGame().getSorenRandNum(100, "Hand-Foxmen")
				if result < 35:
					if cf.removeReligion(iHand, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_HAND_TALI",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Thewhitehand.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				elif cf.removeReligion(iFoxmen, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_TALI_HAND",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Foxmen.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)


		elif iReligion == iHand:

			if pSpreadCity.isHasReligion(iFoxmen):
				result = CyGame().getSorenRandNum(100, "Hand-Foxmen")
				if result < 35:
					if cf.removeReligion(iFoxmen, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_HAND_TALI",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Foxmen.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				elif cf.removeReligion(iHand, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_TALI_HAND",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Thewhitehand.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)


			if pSpreadCity.isHasReligion(iLeaves):
				result = CyGame().getSorenRandNum(100, "Hand-Fellowship")
				if result < 35:
					if cf.removeReligion(iLeaves, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_HAND_TALI",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Fellowship.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				elif cf.removeReligion(iHand, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_TALI_HAND",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/Thewhitehand.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

			if pSpreadCity.isHasReligion(iUnblemished):
				result = CyGame().getSorenRandNum(100, "Unblemished-Hand")
				if result > 35:
					if cf.removeReligion(iHand, pSpreadCity):
						CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_SUCELLUS_MULCARN",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/TheUnblemished.dds',ColorTypes(14),pSpreadCity.getX(),pSpreadCity.getY(),True,True)

				elif cf.removeReligion(iUnblemished, pSpreadCity):
					CyInterface().addMessage(iOwner,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIOUS_CONFLICT_MULCARN_SUCELLUS",(sName,)),'AS2D_UNIT_BUILD_UNIT',1,'Art/Interface/Buttons/Religions/EternalCabal.dds',ColorTypes(5),pSpreadCity.getX(),pSpreadCity.getY(),True,True)


		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has spread to Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, player.getCivilizationName(), sName))

	def onReligionRemove(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Religion Has been removed from a City'
		iReligion, iOwner, pRemoveCity = argsList
		player = PyPlayer(iOwner)
		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has been removed from Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, player.getCivilizationName(), pRemoveCity.getName()))

	def onCorporationFounded(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Corporation Founded'
		iCorporation, iFounder = argsList
		player = PyPlayer(iFounder)
		if (not self.__LOG_RELIGION):
			return
		CvUtil.pyPrint('Player %d Civilization %s has founded %s'
			%(iFounder, player.getCivilizationName(), gc.getCorporationInfo(iCorporation).getDescription()))

	def onCorporationSpread(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Corporation Has Spread to a City'
		iCorporation, iOwner, pSpreadCity = argsList
		player = PyPlayer(iOwner)
		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has spread to Player %d Civilization %s city of %s'
			%(gc.getCorporationInfo(iCorporation).getDescription(), iOwner, player.getCivilizationName(), pSpreadCity.getName()))

	def onCorporationRemove(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Corporation Has been removed from a City'
		iCorporation, iOwner, pRemoveCity = argsList
		player = PyPlayer(iOwner)
		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has been removed from Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, player.getCivilizationName(), pRemoveCity.getName()))

	def onGoldenAge(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Golden Age'
		iPlayer = argsList[0]
		player = PyPlayer(iPlayer)
		if (not self.__LOG_GOLDENAGE):
			return
		CvUtil.pyPrint('Player %d Civilization %s has begun a golden age'
			%(iPlayer, player.getCivilizationName()))

	def onEndGoldenAge(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'End Golden Age'
		iPlayer = argsList[0]
		player = PyPlayer(iPlayer)
		if (not self.__LOG_ENDGOLDENAGE):
			return
		CvUtil.pyPrint('Player %d Civilization %s golden age has ended'
			%(iPlayer, player.getCivilizationName()))

	def onChangeWar(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'War Status Changes'
		bIsWar = argsList[0]
		iTeam = argsList[1]
		iRivalTeam = argsList[2]

	def onChat(self, argsList):
		'Chat Message Event'
		chatMessage = "%s" %(argsList[0],)

	def onSetPlayerAlive(self, argsList):
		'Set Player Alive Event'
		iPlayerID = argsList[0]
		bNewValue = argsList[1]
		CvUtil.pyPrint("Player %d's alive status set to: %d" %(iPlayerID, int(bNewValue)))

		pPlayer = gc.getPlayer(iPlayerID)
		if not bNewValue and gc.getGame().getGameTurnYear() >= 5:

			# lfgr 05/2020
			CvUtil.pyPrint( "Player %d eliminated on turn %d" % ( iPlayerID, CyGame().getGameTurn() ) )

			if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
				CyGame().changeGlobalCounter(5)
			elif pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
				CyGame().changeGlobalCounter(-5)
			if CyGame().getWBMapScript():
				sf.playerDefeated(pPlayer)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LOAD_SCREEN):#I have repurposed this to be Control Whole Team
			if not (gc.getGame().isGameMultiPlayer () or gc.getGame().isHotSeat() or gc.getGame().isNetworkMultiPlayer()):#In hotseat games this may result in skipping players. I imagine there would be similar issues in other multiplayer games
				if iPlayerID == CyGame().getActivePlayer():
					if pPlayer.isHuman():
						iTeam = pPlayer.getTeam()
						if gc.getTeam(iTeam).getNumMembers() > 1:
							for iLoopPlayer in xrange(iPlayerID,gc.getMAX_PLAYERS()):
								pLoopPlayer = gc.getPlayer(iLoopPlayer)
								if iTeam == pLoopPlayer.getTeam():
									if pLoopPlayer.isAlive():
										if not pLoopPlayer.isHuman():
											CyGame().reassignPlayerAdvanced(iPlayerID, iLoopPlayer, -1)
											break
							else:
								for iLoopPlayer in xrange(0,iPlayerID):
									pLoopPlayer = gc.getPlayer(iLoopPlayer)
									if iTeam == pLoopPlayer.getTeam():
										if pLoopPlayer.isAlive():
											if not pLoopPlayer.isHuman():
												CyGame().reassignPlayerAdvanced(iPlayerID, iLoopPlayer, -1)
												break

	def onPlayerChangeStateReligion(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList
		if iNewReligion != iOldReligion:
			pPlayer = gc.getPlayer(iPlayer)
			iTeam = pPlayer.getTeam()
			iLeader = pPlayer.getLeaderType()
			iCiv = pPlayer.getCivilizationType()

			iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
			iEmpyrean = gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')
			iRunes = gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH')
			iLeaves = gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')
			iUndertow = gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS')
			iEsus = gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS')
			iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
			iHand = gc.getInfoTypeForString('RELIGION_WHITE_HAND')


			iMatronae = gc.getInfoTypeForString('RELIGION_MATRONAE')
			iUnblemished = gc.getInfoTypeForString('RELIGION_UNBLEMISHED')
			iBrotherhood = gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS')
			iLaeranCord = gc.getInfoTypeForString('RELIGION_LAERAN_CORD')
			iFoxmen = gc.getInfoTypeForString('RELIGION_FOXMEN')
			iDragonCult = gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON')

			iStewards = gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY')
			iCoven = gc.getInfoTypeForString('RELIGION_COVEN')
			iAnointed = gc.getInfoTypeForString('RELIGION_ANOINTED')
			iOne = gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE')

			iPlenty = gc.getInfoTypeForString('RELIGION_HOUSE_OF_PLENTY')
			iRinggiver = gc.getInfoTypeForString('RELIGION_RINGGIVER')
			iEternalCabal = gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL')
			iGreyCcouncil = gc.getInfoTypeForString('RELIGION_GREY_COUNCIL')
			iEmberLegion = gc.getInfoTypeForString('RELIGION_EMBER_LEGION')
			iDiscord = gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD')




			iCitadel = gc.getInfoTypeForString('IMPROVEMENT_CITADEL')
			iCitadelOfLight = gc.getInfoTypeForString('IMPROVEMENT_CITADEL_OF_LIGHT')
			iHellFire = gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE')

			iAlignment = pPlayer.getAlignment()
			iGood = gc.getInfoTypeForString('ALIGNMENT_GOOD')
			iNeutral = gc.getInfoTypeForString('ALIGNMENT_NEUTRAL')
			iEvil = gc.getInfoTypeForString('ALIGNMENT_EVIL')
						
						


			if iNewReligion != -1:
				if gc.getLeaderHeadInfo(iLeader).getReligionWeightModifier(iNewReligion) < -99:
					pPlayer.setLastStateReligion(iOldReligion)
					iNewReligion = iOldReligion
					pPlayer.changeAnarchyTurns(-pPlayer.getAnarchyTurns())
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_GRIGORI'):
					pPlayer.setAlignment(iNeutral)
					iAlignment = pPlayer.getAlignment()
					pPlayer.setLastStateReligion(-1)
					iNewReligion = -1
					pPlayer.changeAnarchyTurns(-pPlayer.getAnarchyTurns())
				elif iNewReligion == iDragonCult:

					if not cf.isHasDragon(pPlayer):
						pPlayer.setLastStateReligion(iOldReligion)
						iNewReligion = iOldReligion
						pPlayer.changeAnarchyTurns(-pPlayer.getAnarchyTurns())
						
						
					if not pPlayer.isBarbarian():
						# pPlayer.setLastStateReligion(iOldReligion)
						# iNewReligion = iOldReligion
						# pPlayer.changeAnarchyTurns(-pPlayer.getAnarchyTurns())


						listEvilDragons = [
												gc.getInfoTypeForString('UNITCLASS_ABASHI'),
												gc.getInfoTypeForString('UNITCLASS_DRIFA'),
												gc.getInfoTypeForString('UNITCLASS_THALATTH'),

												gc.getInfoTypeForString('UNITCLASS_DRAGON_BLOOD'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_FURNACE'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_OBSIDIAN'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_PIT'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_SHADOW'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_SIEGE'),
												gc.getInfoTypeForString('UNITCLASS_DRACOLICH'),
												gc.getInfoTypeForString('UNITCLASS_VAULT_WYRM'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_WINTER')
											]
						listNeutralDragons = [
												gc.getInfoTypeForString('UNITCLASS_DRAGON_ELDER'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_FANG'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_GRAVE'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_FEATHERED'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_SCALED'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_SEED'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_SPIRE')
											]
						listGoodDragons = [
												gc.getInfoTypeForString('UNITCLASS_EURABATRES'),

												gc.getInfoTypeForString('UNITCLASS_DRAGON_CORAL'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_DAWN'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_GOLD'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_RUNE'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_SHIELD'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_SHIMMERING'),
												gc.getInfoTypeForString('UNITCLASS_DRAGON_SHIELD')
											]
						iCountEvil = 0
						iCountGood = 0
						iCountNeutral = 0
						eTeam = gc.getTeam(pPlayer.getTeam())
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
							iCountGood += 3
						elif pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
							iCountEvil += 2
						if pPlayer.getAlignment() == iGood:
							iCountGood += 2
						elif pPlayer.getAlignment() == iEvil:
							iCountEvil += 2
						for iUnitClass in listEvilDragons:
							iCountEvil += pPlayer.getUnitClassCount(iUnitClass)
							iCountEvil += eTeam.getUnitClassCount(iUnitClass)
						for iUnitClass in listGoodDragons:
							iCountGood += pPlayer.getUnitClassCount(iUnitClass)
							iCountGood += eTeam.getUnitClassCount(iUnitClass)
						for iUnitClass in listEvilDragons:
							iCountNeutral += pPlayer.getUnitClassCount(iUnitClass)
							iCountNeutral += eTeam.getUnitClassCount(iUnitClass)

						if iCountGood > iCountEvil + iCountNeutral:
							pPlayer.setAlignment(iGood)
						elif iCountEvil > iCountNeutral:
							pPlayer.setAlignment(iEvil)
						else:
							pPlayer.setAlignment(iNeutral)
						iAlignment = pPlayer.getAlignment()

				elif iNewReligion == iOne:
					pPlayer.setLastStateReligion(iOldReligion)
					iNewReligion = iOldReligion
					pPlayer.changeAnarchyTurns(-1)
				elif iNewReligion == iEmpyrean:
					if iCiv == gc.getInfoTypeForString('CIVILIZATION_CALABIM') or iLeader in [gc.getInfoTypeForString('LEADER_ALEXIS'), gc.getInfoTypeForString('LEADER_FLAUROS'), gc.getInfoTypeForString('LEADER_MAHON')]:
						pPlayer.setLastStateReligion(iOldReligion)
						iNewReligion = iOldReligion
						pPlayer.changeAnarchyTurns(-pPlayer.getAnarchyTurns())
					else:
						for pPlot in PyPlayer(iPlayer).getPlotsWithImprovement(iCitadel):
							pPlot.setImprovementType(iCitadelOfLight)

				elif iNewReligion == iOrder:
					pPlayer.setAlignment(iGood)


				elif iNewReligion == iFoxmen:
					if CyGame().getSorenRandNum(7, "Volatile Alignment") < 3:
						lAlignments = [
										# gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getAlignment(),#This does not seem to be exposed to python
										pPlayer.getAlignment(),
										pPlayer.getAlignment(),
										iGood,
										iNeutral,
										iNeutral,
										iNeutral,
										iEvil
										]
						iAlignment = lAlignments.pop(CyGame().getSorenRandNum(len(lAlignments), "Tali Fickle Alignment"))
						if pPlayer.getAlignment() != iAlignment:
							if pPlayer.isHuman():
								sAlignment = CyTranslator().getText("TXT_KEY_ALIGNMENT_NEUTRAL", ())
								if iAlignment == iGood:
									sAlignment = CyTranslator().getText("TXT_KEY_ALIGNMENT_GOOD", ())
								if iAlignment == iEvil:
									sAlignment = CyTranslator().getText("TXT_KEY_ALIGNMENT_EVIL", ())
								cf.addPopup(CyTranslator().getText("TXT_KEY_MESSAGE_TALI_ALIGNMENT",(sAlignment,)), 'Art/Interface/Buttons/Religions/Foxmen.dds')
							pPlayer.setAlignment(iAlignment)

				elif iNewReligion == iVeil:
					pPlayer.setAlignment(iEvil)
				elif iNewReligion == iDiscord:
					if gc.getTeam(pPlayer.getTeam()).getAtWarCount(True) == 0:
						iEnemy = -1
						iWorstAttitude = 0
						for iPlayerLoop in xrange(gc.getMAX_PLAYERS()):
							if cf.canStartWar(iPlayer,iPlayerLoop):
								iAttitude = pPlayer.AI_getAttitude(iPlayerLoop)
								if iAttitude < iWorstAttitude:
									iWorstAttitude = iAttitude
									iEnemy = iPlayerLoop
						if iEnemy > -1:
							cf.startWar(iPlayer, iEnemy, WarPlanTypes.WARPLAN_LIMITED)


				if iNewReligion != iHand and iLeader in [gc.getInfoTypeForString('LEADER_AURIC'), gc.getInfoTypeForString('LEADER_ANAGANTIOS'), gc.getInfoTypeForString('LEADER_DUMANNIOS'), gc.getInfoTypeForString('LEADER_RIUROS')]:
					pPlayer.setLastStateReligion(-1)
					iNewReligion = -1

				if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
					iAuricPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
					if iAuricPlayer != -1:
						pAuricPlayer = gc.getPlayer(iAuricPlayer)
						if pAuricPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AURIC')) > 0:
							iAuricTeam = pAuricPlayer.getTeam()

							if iNewReligion == iHand:
								eAuricTeam = gc.getTeam(iAuricTeam)
								iTeam = pPlayer.getTeam()
								if eAuricTeam.isAtWar(iTeam):
									pPlayer.setLastStateReligion(iOldReligion)
									pPlayer.changeAnarchyTurns(-pPlayer.getAnarchyTurns())

							elif gc.getTeam(pPlayer.getTeam()).isVassal(iAuricTeam):
								pPlayer.setLastStateReligion(iHand)
								iNewReligion = iHand


			iAlignment = pPlayer.getAlignment()
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_EMPYREAN')) > 0:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN') or pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')) or iAlignment == iGood
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN_HOSTILE')
				
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
								
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_BROTHERHOOD')) > 0:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS') or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_PACIFISM')) or iAlignment == iGood
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD_HOSTILE')
				iCalabim = gc.getInfoTypeForString('CIVILIZATION_CALABIM')
				iTempleBlind = gc.getInfoTypeForString('BUILDING_TEMPLE_BLIND_BROTHERHOOD')
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if loopCity.getCivilizationType() == iCalabim:
					
						if loopCity.getNumBuilding(iTempleHostile) or loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleBlind, 1)
							
					else:
						if bFriendly:
							if loopCity.getNumBuilding(iTempleHostile):
								loopCity.setNumRealBuilding(iTempleHostile, 0)
								loopCity.setNumRealBuilding(iTempleFriendly, 1)
								loopCity.setNumRealBuilding(iTempleBlind, 0)
							else:
								loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
								loopCity.setBuildingProduction(iTempleHostile, 0)
								if loopCity.getProductionBuilding () == iTempleHostile:
									loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
						else:
							if loopCity.getNumBuilding(iTempleFriendly):
								loopCity.setNumRealBuilding(iTempleFriendly, 0)
								loopCity.setNumRealBuilding(iTempleHostile, 1)
								loopCity.setNumRealBuilding(iTempleBlind, 0)
							else:
								loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
								loopCity.setBuildingProduction(iTempleFriendly, 0)
								if loopCity.getProductionBuilding () == iTempleFriendly:
									loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
								
								
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARTIFICERY')) > 0:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RINGGIVER') or iAlignment == iGood or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_ARETE'))
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_ARTIFICERY')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_ARTIFICERY_HOSTILE')
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
								
								
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_ORDER')) > 0:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ORDER') or iAlignment == iGood
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER_HOSTILE')
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)

			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_UNBLEMISHED')) > 0:
				bFriendly = pPlayer.getStateReligion() in [gc.getInfoTypeForString('RELIGION_UNBLEMISHED'),gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')] or iAlignment == iGood
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED_HOSTILE')
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
								
								
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_KILMORPH')) > 0:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH') or (iAlignment != iEvil and pPlayer.getStateReligion() != gc.getInfoTypeForString('RELIGION_FOXMEN'))
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH_HOSTILE')

				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
			
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_OVERLORDS')) > 0:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS') or iAlignment != iGood
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS_HOSTILE')
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
								
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_GAMBLING_HOUSE')) > 0:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY') or iAlignment != iGood
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE_HOSTILE')
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
								
								
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_ANOINTED')) > 0:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_ANOINTED') or iAlignment == iEvil
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED_HOSTILE')
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)

			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_VEIL')) > 0:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL') or iAlignment == iEvil
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL_HOSTILE')
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
								
								
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOPHET')) > 0:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_EMBER_LEGION') or iAlignment == iEvil
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_TOPHET_HOSTILE')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE_HOSTILE')
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
								
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_INTERSTICE')) > 0:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COVEN') or iAlignment == iEvil
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_INTERSTICE')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_INTERSTICE_HOSTILE')
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
								
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_THE_HAND')) > 0:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_WHITE_HAND')
				if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
					iAuricPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
					if iAuricPlayer != -1:
						pAuricPlayer = gc.getPlayer(iAuricPlayer)
						if pAuricPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AURIC')) > 0:
							iTeam = pPlayer.getTeam()
							eTeam = gc.getTeam(iTeam)
							iAuricTeam = pAuricPlayer.getTeam()
							if iAuricTeam == iTeam:
								bFriendly = True
							elif eTeam.isVassal(iTeam):
								bFriendly = True
							elif eTeam.isAtWar(iAuricTeam):
								bFriendly = False
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND_HOSTILE')
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)
								
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_APHOTIC_THRONE')) > 0:
				bFriendly = (iNewReligion == iEsus or pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')) ) or iAlignment == iEvil
				iTempleFriendly = gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE')
				iTempleHostile = gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE_HOSTILE')
				
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					if bFriendly:
						if loopCity.getNumBuilding(iTempleHostile):
							loopCity.setNumRealBuilding(iTempleHostile, 0)
							loopCity.setNumRealBuilding(iTempleFriendly, 1)
						else:
							loopCity.setBuildingProduction(iTempleFriendly, loopCity.getBuildingProduction(iTempleHostile))
							loopCity.setBuildingProduction(iTempleHostile, 0)
							if loopCity.getProductionBuilding () == iTempleHostile:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleFriendly,-1, False, True, False, True)
					else:
						if loopCity.getNumBuilding(iTempleFriendly):
							loopCity.setNumRealBuilding(iTempleFriendly, 0)
							loopCity.setNumRealBuilding(iTempleHostile, 1)
						else:
							loopCity.setBuildingProduction(iTempleHostile, loopCity.getBuildingProduction(iTempleFriendly))
							loopCity.setBuildingProduction(iTempleFriendly, 0)
							if loopCity.getProductionBuilding () == iTempleFriendly:
								loopCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iTempleHostile,-1, False, True, False, True)




			if iOldReligion == iFoxmen:
				iAdventurer = gc.getInfoTypeForString('PROMOTION_ADVENTURER')
				iDivine = gc.getInfoTypeForString('PROMOTION_DIVINE')
				for pUnit in PyPlayer(iPlayer).getUnitList():
					if pUnit.isHasPromotion(iAdventurer) and pUnit.isHasPromotion(iDivine) and pUnit.getReligion() == iFoxmen:
						info = gc.getUnitInfo(pUnit.getUnitType())
						CyInterface().addMessage(iPlayer, True, 25, localText.getText("TXT_KEY_MESSAGE_UNIT_ABANDON", (pUnit.getName(), )), '', 1, info.getButton(), ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)
						pUnit.kill(True, -1)

			
			
			if iOldReligion == iVeil and iCiv != gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS):
					for pPlot in PyPlayer(iPlayer).getPlotsWithImprovement(iHellFire):
						pPlot.setOwner(gc.getBARBARIAN_PLAYER())

				lPacts = [	(gc.getInfoTypeForString('LEADER_HYBOREM'), gc.getInfoTypeForString('EVENT_SUMMON_HYBOREM')),
							(gc.getInfoTypeForString('LEADER_JUDECCA'),gc.getInfoTypeForString('EVENT_SUMMON_JUDECCA')),
							(gc.getInfoTypeForString('LEADER_LETHE'), gc.getInfoTypeForString('EVENT_SUMMON_LETHE')),
							(gc.getInfoTypeForString('LEADER_MERESIN'), gc.getInfoTypeForString('EVENT_SUMMON_MERESIN')),
							(gc.getInfoTypeForString('LEADER_OUZZA'), gc.getInfoTypeForString('EVENT_SUMMON_OUZZA')),
							(gc.getInfoTypeForString('LEADER_SALLOS'), gc.getInfoTypeForString('EVENT_SUMMON_SALLOS')),
							(gc.getInfoTypeForString('LEADER_STATIUS'), gc.getInfoTypeForString('EVENT_SUMMON_STATIUS')),
							]

				for iDemon, iEvent in lPacts:
					if pPlayer.getLeaderType() == iDemon:continue
					if pPlayer.getEventOccured(iEvent):
						pPlayer.resetEventOccured(iEvent)
						if pPlayer.isHuman():
							infoD = gc.getLeaderHeadInfo(iDemon)
							cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_INFERNAL_PACT_BROKEN",(infoD.getDescription(), )), infoD.getButton())

						iDemonPlayer = cf.getLeader(iDemon)
						if iDemonPlayer != -1:
							pDemonPlayer = gc.getPlayer(iDemonPlayer)
							iDemonTeam = pDemonPlayer.getTeam()

							pDemonPlayer.AI_changeAttitudeExtra(iPlayer,-12)
							gc.getTeam(iDemonTeam).setHasPrepareWar(iTeam,True)

						if not pPlayer.hasTrait( gc.getInfoTypeForString('TRAIT_BARBARIAN')):
							bTeam = gc.getTeam(gc.getBARBARIAN_TEAM())
							iTeam = pPlayer.getTeam()
							if not bTeam.isAtWar(iTeam):
								if bTeam.canDeclareWar(iTeam):
									bTeam.declareWar(iTeam, False, WarPlanTypes.WARPLAN_TOTAL)

								if pPlayer.isHuman():
									cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_BARBARIAN_DECLARE_WAR",()), 'art/interface/popups/Barbarian.dds')






	def onPlayerGoldTrade(self, argsList):
		'Player Trades gold to another player'
		iFromPlayer, iToPlayer, iGoldAmount = argsList

	def onCityBuilt(self, argsList):
		'City Built'
		city = argsList[0]
		pPlot = city.plot()
		iPlayer = city.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iCiv = pPlayer.getCivilizationType()
		city.setPopulation(2)

		if not city.isCapital():
			listCityNames = []
			CivFile = open("Mods/Magister Modmod for FfH2/Assets/XML/Civilizations/CIV4CivilizationInfos.xml")
			bCiv = False
			for line in CivFile.readlines():
				if "<Type>" in line:
					sCiv = line[line.find(">") +1 : line.find("</")]
					if iCiv == gc.getInfoTypeForString(sCiv):
						bCiv = True
					else:
						bCiv = False
				elif bCiv:
					if "<City>" in line:
						txtKeyCity = line[line.find(">") +1 : line.find("</")]
						sName = localText.getText(txtKeyCity, ())
						bUsed = False
						for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
							pLoopPlayer = gc.getPlayer(iLoopPlayer)
							(loopCity, iter) = pLoopPlayer.firstCity(False)
							while(loopCity):
								if not loopCity.isNone(): #only valid cities
									if loopCity.getName() == sName:
										bUsed = True
										break
								(loopCity, iter) = pLoopPlayer.nextCity(iter, False)
							if bUsed:
								break
						if not bUsed:
							listCityNames.append(txtKeyCity)
			if len(listCityNames) > 0:
				txtKeyCity = listCityNames.pop(CyGame().getSorenRandNum(len(listCityNames), "Name city"))
				sName = localText.getText(txtKeyCity, ())
				city.setName(sName, False)


		if iCiv == gc.getInfoTypeForString('CIVILIZATION_KHAZAD'):
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DWARVEN_VAULT'), 1)
			cf.doTurnKhazad(iPlayer)

		elif iCiv == gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TRAINING_YARD'), 1)
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARCHERY_RANGE'), 1)
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_PALISADE'), 1)
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SIEGE_WORKSHOP'), 1)
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_FORGE'), 1)
			cf.removeReligion(gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'), city)
			cf.removeReligion(gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'), city)

		elif iCiv == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
			cf.removeReligion(gc.getInfoTypeForString('RELIGION_THE_ORDER'), city)
			cf.removeReligion(gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'), city)
			city.setHasReligion(gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'), True, True, True)
			city.setPopulation(3)
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ELDER_COUNCIL'), 1)
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TRAINING_YARD'), 1)
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARCHERY_RANGE'), 1)
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL'), 1)
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MAGE_GUILD'), 1)
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DEMONIC_CITIZENS'), 1)

		elif pPlayer.isBarbarian():
			eTeam = gc.getTeam(gc.getBARBARIAN_TEAM())
			iUnit = gc.getInfoTypeForString('UNIT_WARRIOR')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')) or CyGame().getStartEra() > gc.getInfoTypeForString('ERA_ANCIENT'):
				iUnit = gc.getInfoTypeForString('UNIT_AXEMAN')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')) or CyGame().getStartEra() > gc.getInfoTypeForString('ERA_CLASSICAL'):
				iUnit = gc.getInfoTypeForString('UNIT_OGRE')
			newUnit = pPlayer.initUnit(iUnit, city.getX(), city.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), True)
			iUnit = gc.getInfoTypeForString('UNIT_ARCHER')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BOWYERS')) or CyGame().getStartEra() > gc.getInfoTypeForString('ERA_CLASSICAL'):
				iUnit = gc.getInfoTypeForString('UNIT_LONGBOWMAN')
			newUnit2 = pPlayer.initUnit(iUnit, city.getX(), city.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
			newUnit3 = pPlayer.initUnit(iUnit, city.getX(), city.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
			newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), True)
			newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), True)
			if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_ARCHERY')) or CyGame().getStartEra() == gc.getInfoTypeForString('ERA_ANCIENT'):
				newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)
				newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)

		if CyGame().getWBMapScript():
			sf.onCityBuilt(city)

		if (city.getOwner() == CyGame().getActivePlayer())and ( CyGame().getAIAutoPlay(CyGame().getActivePlayer()) == 0 ):
			if not CyGame().GetWorldBuilderMode():#Platy WorldBuilder
				self.__eventEditCityNameBegin(city, False)
		CvUtil.pyPrint('City Built Event: %s' %(city.getName()))

	def onCityRazed(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'City Razed'
		city, iPlayer = argsList
		iOwner = city.findHighestCulture()
		iX = city.getX()
		iY = city.getY()
		pPlot = city.plot()

#### messages - wonder destroyed start by The_J (modified by Terkhen) ####
		if city.getNumWorldWonders() > 0:
			for i in range(gc.getNumBuildingInfos()):
				if city.getNumBuilding(i) > 0:
					pThisBuilding = gc.getBuildingInfo(i)
					if gc.getBuildingClassInfo(pThisBuilding.getBuildingClassType()).getMaxGlobalInstances() == 1:
						pConquerPlayer = gc.getPlayer(city.getOwner())
						iConquerTeam = pConquerPlayer.getTeam()
						sConquerName = pConquerPlayer.getName()
						sWonderName = pThisBuilding.getDescription()
						iX = city.getX()
						iY = city.getY()

						for iLoopPlayer in range (gc.getMAX_CIV_PLAYERS()):
							iLoopTeam = gc.getPlayer(iLoopPlayer).getTeam()
							if iLoopTeam == iConquerTeam or gc.getTeam(iLoopTeam).isHasMet(iConquerTeam):

								if iLoopPlayer == city.getOwner():
									sText = "TXT_KEY_YOU_DESTROYED_WONDER"
								else:
									sText = "TXT_KEY_DESTROYED_WONDER"
								CyInterface().addMessage(iLoopPlayer, False, 15, CyTranslator().getText(sText, (sConquerName,sWonderName)), '', 0,'Art/Interface/Buttons/General/warning_popup.dds', ColorTypes(gc.getInfoTypeForString("COLOR_RED")), iX, iY, True, True)
#### messages - wonder destroyed end ####

		# Partisans!
#		if city.getPopulation > 1 and iOwner != -1 and iPlayer != -1:
#			owner = gc.getPlayer(iOwner)
#			if not owner.isBarbarian() and owner.getNumCities() > 0:
#				if gc.getTeam(owner.getTeam()).isAtWar(gc.getPlayer(iPlayer).getTeam()):
#					if gc.getNumEventTriggerInfos() > 0: # prevents mods that don't have events from getting an error
#						iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_PARTISANS')
#						if iEvent != -1 and gc.getGame().isEventActive(iEvent) and owner.getEventTriggerWeight(iEvent) >= 0:
#							triggerData = owner.initTriggeredData(iEvent, True, -1, city.getX(), city.getY(), iPlayer, city.getID(), -1, -1, -1, -1)

		pPlayer = gc.getPlayer(iPlayer)
		ownerPlayer = gc.getPlayer(city.getOriginalOwner())

		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_CRUCIBLE')) > 0:
			CyEngine().removeLandmark(city.plot())
			CyInterface().addMessage(city.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_CRUCIBLE_RAZED", ()),'', 1, 'Art/Interface/Buttons/Projects/Glory_Everlasting.dds', gc.getInfoTypeForString('COLOR_GREEN'), city.getX(), city.getY(), True, True)

			listMana = []
			for iLoopBonus in xrange(gc.getNumBonusInfos()):
				if gc.getBonusInfo(iLoopBonus).isMana():
					listMana.append(iLoopBonus)

			for i in xrange(CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.isNone(): continue
				if pPlot.isCity():
					pCity = pPlot.getPlotCity()
					for iMana in listMana:
						iCount = 0
						for iBuilding in xrange(gc.getNumBuildingInfos()):
							if pCity.getNumBuilding(iBuilding) > 0:
								infoB = gc.getBuildingInfo(iBuilding)
								iNumBoni = infoB.getNumFreeBonuses()
								iNumBoni *= pCity.getNumBuilding(iBuilding)#Just in case duplicate buildings could be used in modmodmods
								if iNumBoni != 0:#Could be positive or negative
									for iBonus in [infoB.getFreeBonus(), infoB.getFreeBonus2(), infoB.getFreeBonus3()]:
										if iBonus == iMana:
											iCount += iNumBoni

						while pCity.getFreeBonus(iMana) > iCount:
							pCity.changeFreeBonus(iMana, -1)
						while pCity.getFreeBonus(iMana) < iCount:
							pCity.changeFreeBonus(iMana, 1)
							CyInterface().addMessage(pCity.getOwner(), True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_CRUCIBLE_RAZED_MANA_RESTORED", (gc.getBonusInfo(iMana).getDescription(),)) , '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBonusInfo(iMana).getButton(), gc.getInfoTypeForString('COLOR_RED'), pCity.getX(), pCity.getY(), True, True)#For testing purposes

				iBonusReal = pPlot.getRealBonusType()
				if iBonusReal not in [-1, pPlot.getBonusType(-1)]:
					if iBonusReal in listMana:
						pPlot.setBonusType(iBonusReal)
##						iImpReal = pPlot.getRealImprovementType()
##						if iImpReal not in [-1, pPlot.getImprovementType()]:
##							pPlot.setImprovementType(iImpReal)
						infoB = gc.getBonusInfo(iBonusReal)
						CyInterface().addMessage(0, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_CRUCIBLE_RAZED_MANA_RESTORED", (infoB.getDescription(),)), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, infoB.getButton(), gc.getInfoTypeForString('COLOR_RED'), pPlot.getX(), pPlot.getY(), True, True)#For testing purposes
						if pPlot.isOwned():
							CyInterface().addMessage(pPlot.getOwner(), True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_CRUCIBLE_RAZED_MANA_RESTORED", (infoB.getDescription(),)), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, infoB.getButton(), gc.getInfoTypeForString('COLOR_RED'), pPlot.getX(), pPlot.getY(), True, True)#For testing purposes


			listMagic =	[
						'PROMOTION_ARCANE',
						'PROMOTION_CHANNELING1',
						'PROMOTION_CHANNELING2',
						'PROMOTION_CHANNELING3',
						'PROMOTION_DIVINE',
						'PROMOTION_CHANNELING4',
						'PROMOTION_EXTENSION1',
						'PROMOTION_EXTENSION2',
						'PROMOTION_ILLUSIONIST',
						'PROMOTION_SUMMONER',
						'PROMOTION_SUNDERED',
						'PROMOTION_TWINCAST',
						'PROMOTION_UNHOLY_TAINT',
						'PROMOTION_VAMPIRE',
						'PROMOTION_WATER_WALKING',
						'PROMOTION_WATER_WALKING_TEMP',
						'PROMOTION_WITHERED'
						]

			listUnits = PyHelpers.PyGame().getAllUnitList()
			for pUnit in listUnits:
				sName = pUnit.getName()
				infoU = gc.getUnitInfo(pUnit.getUnitType())
				for sProm in listMagic:
					iProm = gc.getInfoTypeForString(sProm)
					if infoU.getFreePromotions(iProm):
						pUnit.setHasPromotion(iProm, True)
						infoP = gc.getPromotionInfo(iProm)
						sNamePromotion = infoP.getDescription()
						sButton = infoP.getButton()
						CyInterface().addMessage(pUnit.getOwner(), True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_CRUCIBLE_RAZED_PROMOTION_RESTORED", (sName, sNamePromotion,)), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_RED'), pPlot.getX(), pPlot.getY(), True, True)#For testing purposes


		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_LORUM_DIABOLI')) > 0:

			iBasium = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
			if iBasium != -1:
				pPlayer2 = gc.getPlayer(iBasium)
				pPlayer2.AI_changeAttitudeExtra(iPlayer, -66)
			lDemonLords = []
			iInf = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
			for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
				pPlayer2 = gc.getPlayer(iPlayer2)
				if pPlayer2.isAlive():
					if pPlayer2.getCivilizationType() == iInf:
						pPlayer2.AI_changeAttitudeExtra(iPlayer, 6)
						if pPlayer2.getNumCities() > 0:
							lDemonLords.append(iPlayer2)

			iIJ = gc.getInfoTypeForString('PROMOTION_INCARCERATUS_JUDICII')

			iVV = gc.getInfoTypeForString('PROMOTION_CAPTUS_CAVEAE_ANGELORUM')
			iNB = gc.getInfoTypeForString('PROMOTION_NETHERBIND')
			iSF= gc.getInfoTypeForString('PROMOTION_SOUL_FORGED')
			lPrisoners = []

			for pSluagh in PyPlayer(gc.getBARBARIAN_PLAYER()).getUnitList():
				if pSluagh.isHasPromotion(iIJ):
					pSluagh.setHasPromotion(iIJ, False)
					if pSluagh.isHasPromotion(iVV):continue
					if pSluagh.isHasPromotion(iNB):continue
					if pSluagh.isHasPromotion(iSF):continue
					lPrisoners.append(pSluagh)
			if len(lPrisoners) > 0 and len(lDemonLords) > 0:
				iBarb = gc.getInfoTypeForString('LEADER_BARBARIAN')
				dAvatars = {
						gc.getInfoTypeForString('UNIT_HYBOREM')	:	gc.getInfoTypeForString('LEADER_HYBOREM'),
						gc.getInfoTypeForString('UNIT_JUDECCA')	:	gc.getInfoTypeForString('LEADER_JUDECCA'),
						gc.getInfoTypeForString('UNIT_LETHE')	:	gc.getInfoTypeForString('LEADER_LETHE'),
						gc.getInfoTypeForString('UNIT_MERESIN')	:	gc.getInfoTypeForString('LEADER_MERESIN'),
						gc.getInfoTypeForString('UNIT_OUZZA')	:	gc.getInfoTypeForString('LEADER_OUZZA'),
						gc.getInfoTypeForString('UNIT_SALLOS')	:	gc.getInfoTypeForString('LEADER_SALLOS'),
						gc.getInfoTypeForString('UNIT_STATIUS')	:	gc.getInfoTypeForString('LEADER_STATIUS'),

						gc.getInfoTypeForString('UNIT_STEPHANOS')	:	iBarb,
						gc.getInfoTypeForString('UNIT_BUBOES')	:	iBarb,
						gc.getInfoTypeForString('UNIT_YERSINIA')	:	iBarb,
						gc.getInfoTypeForString('UNIT_ARS')	:	iBarb,
						gc.getInfoTypeForString('UNIT_WRATH')	:	iBarb
						}
				iManes = gc.getInfoTypeForString('UNIT_MANES')
				iHeld = gc.getInfoTypeForString('PROMOTION_HELD')
				lAddProm = [gc.getInfoTypeForString('PROMOTION_DEMON'), gc.getInfoTypeForString('PROMOTION_WARCRY'), gc.getInfoTypeForString('PROMOTION_MORALE')]
				iCount = 0
				while len(lPrisoners) > 0:
					pUnit = lPrisoners.pop(CyGame().getSorenRandNum(len(lPrisoners), "Free Demon"))
					iUnit = pUnit.getScenarioCounter()
					if not -1 < iUnit < gc.getNumUnitInfos():
						iUnit = gc.getInfoTypeForString('UNIT_MANES')
					iPlayer2 = -1
					if iUnit in dAvatars:
						iPlayer2 = cf.getLeader(dAvatars[iUnit])
						pPlayer2 = gc.getPlayer(iPlayer2)
						pPlayer2.AI_changeAttitudeExtra(iPlayer, 66)
					else:
						iPlayer2 = lDemonLords[CyGame().getSorenRandNum(len(lDemonLords), "Free Demon to someone")]
						pPlayer2 = gc.getPlayer(iPlayer2)
						pPlayer2.AI_changeAttitudeExtra(iPlayer, 1)
					if iPlayer2 > -1:
						if pPlayer2.getNumCities() > 0:
							py = PyPlayer(iPlayer2)
							iRnd = CyGame().getSorenRandNum(pPlayer2.getNumCities(), "Gift Unit")
							pCity = py.getCityList()[iRnd]
							iX = pCity.getX()
							iY = pCity.getY()
							newUnit = pPlayer2.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							sName = pUnit.getName()[:pUnit.getName ().find("'s Sluagh")]
							newUnit.convert(pUnit)
							newUnit.setHasPromotion(iHeld, False)
							newUnit.setName(sName)
							for iProm in lAddProm:
								newUnit.setHasPromotion(iProm, True)
							for iProm in xrange(gc.getNumPromotionInfos()):
								if gc.getPromotionInfo(iProm).isEquipment():
									newUnit.setHasPromotion(iProm, False)
							sName = "<color=%d,%d,%d,%d>%s</color>" %(pPlayer2.getPlayerTextColorR(), pPlayer2.getPlayerTextColorG(), pPlayer2.getPlayerTextColorB(), pPlayer2.getPlayerTextColorA(), newUnit.getName() )
							CyInterface().addMessage(iPlayer2, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_ESCAPE_ANGELORUM_CAVEA", (sName, )), 'AS2D_UNIT_FALLS', 1, gc.getUnitInfo(iUnit).getButton(), ColorTypes(8), iX, iY, True, True)
							if iPlayer != iPlayer2:
								CyInterface().addMessage(iPlayer, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_ESCAPE_ANGELORUM_CAVEA", (sName, )), 'AS2D_UNIT_FALLS', 1, gc.getUnitInfo(iUnit).getButton(), ColorTypes(7), iX, iY, True, True)
							iCount += 1
				if iCount > 0:
					szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_ESCAPE_ANGELORUM_CAVEA_NUMBER", (iCount, ))
					CyInterface().addMessage(iPlayer, True, 25, szBuffer, 'AS2D_UNIT_FALLS', 1, 'Art/Interface/Buttons/Equipment/AngelorumCavea.dds', ColorTypes(7), city.getX(), city.getY(), True, True)


			iCustos = gc.getInfoTypeForString('PROMOTION_CUSTOS_JUDICII')
			for loopUnit in PyHelpers.PyGame().getAllUnitList():
				if loopUnit.isHasPromotion(iCustos):
					loopUnit.setHasPromotion(iCustos, False)



		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_NULLSTONE_CITADEL')) > 0:
			iX = city.getX()
			iY = city.getY()
			for iiX in xrange(iX-3, iX+4, 1):
				for iiY in xrange(iY-3, iY+4, 1):
					pLoopPlot = CyMap().plot(iiX,iiY)
					if not pLoopPlot.isNone():
						for i in xrange(pLoopPlot.getNumUnits()):
							pUnit = pLoopPlot.getUnit(i)
							pUnit.setHasCasted(False)
			CyInterface().addMessage(city.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_NULLSTONE_UNBLOCK", ()),'',1,'Art/Interface/Buttons/Buildings/Castle.dds',gc.getInfoTypeForString('COLOR_GREEN'),iX,iY,True,True)

		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_SOUL_FORGE')) > 0:
			iX = city.getX()
			iY = city.getY()
			iSF = gc.getInfoTypeForString('PROMOTION_SOUL_FORGED')
			pPlot = CyMap().plot(0,0)
			for i in xrange(pPlot.getNumUnits(), -1, -1):
				pUnit = pPlot.getUnit(i)
				pUnit.setHasPromotion(iSF, False)
			CyInterface().addMessage(city.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SOUL_FORGE_DESTROYED", ()),'',1,'Art/Interface/Buttons/Buildings/Soulforge.dds',gc.getInfoTypeForString('COLOR_GREEN'),iX,iY,True,True)

		if not ownerPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')):
			iAngel = gc.getInfoTypeForString('UNIT_ANGEL')
			iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
			iManes = gc.getInfoTypeForString('UNIT_MANES')
			iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
			iVampire = gc.getInfoTypeForString('PROMOTION_VAMPIRE')
			iEoD = gc.getInfoTypeForString('UNIT_EATER_OF_DREAMS')
			iBoA = gc.getInfoTypeForString('UNIT_BEAST_OF_AGARES')

			iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
			iEmpyrean = gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')
			iRunes = gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH')
			iLeaves = gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')
			iUndertow = gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS')
			iEsus = gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS')
			iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
			iHand = gc.getInfoTypeForString('RELIGION_WHITE_HAND')
			iMatronae = gc.getInfoTypeForString('RELIGION_MATRONAE')

			iUnblemished = gc.getInfoTypeForString('RELIGION_UNBLEMISHED')
			iBrotherhood = gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS')
			iLaeran = gc.getInfoTypeForString('RELIGION_LAERAN_CORD')
			iFoxmen = gc.getInfoTypeForString('RELIGION_FOXMEN')
			iDragonCult = gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON')
			iStewards = gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY')
			iCoven = gc.getInfoTypeForString('RELIGION_COVEN')
			iAnointed = gc.getInfoTypeForString('RELIGION_ANOINTED')
			iOne = gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE')

			iAuricPlayer = -1
			if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_ASCENSION')) > 0:
				iAuricPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
				if iAuricPlayer != -1:
					if not gc.getPlayer(iAuricPlayer).hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')):
						iAuricPlayer = -1

			pPlot = city.plot()
			for i in xrange(pPlot.getNumUnits(), -1, -1):
				if city.getPopulation() < 2: break
				pUnit = pPlot.getUnit(i)
				if pUnit.getOwner() == iPlayer:
					if (pUnit.isHasPromotion(iVampire) and pUnit.isAlive()) or pUnit.getUnitType() in [iEoD, iBoA]:
						iPop = city.getPopulation()
						while iPop > 2:
							if pUnit.isHasPromotion(iVampire):
								if pUnit.canCast(gc.getInfoTypeForString('SPELL_FEAST'), False):
									pUnit.cast(gc.getInfoTypeForString('SPELL_FEAST'))
							if pUnit.getUnitType() == iEoD:
								if pUnit.canCast(gc.getInfoTypeForString('SPELL_CONSUME_SOUL'), False):
									pUnit.cast(gc.getInfoTypeForString('SPELL_CONSUME_SOUL'))
							elif pUnit.getUnitType() == iBoA:
								if pUnit.canCast(gc.getInfoTypeForString('SPELL_BEAST_FEAST'), False):
									pUnit.cast(gc.getInfoTypeForString('SPELL_BEAST_FEAST'))
							iPop -= 1

			for i in xrange(1 + city.getPopulation()/10):
				if city.isHasReligion(iOrder):
					cf.giftUnit(iAngel, iMercurians, 0, pPlot, city.getOwner(), iOrder)
				if city.isHasReligion(iEmpyrean):
					cf.giftUnit(iAngel, iMercurians, 0, pPlot, city.getOwner(), iEmpyrean)
				if city.isHasReligion(iRunes):
					cf.giftUnit(iAngel, iMercurians, 0, pPlot, city.getOwner(), iRunes)
				if city.isHasReligion(iUndertow):
					cf.giftUnit(iManes, iInfernal, 0, pPlot, city.getOwner(), iUndertow)
				if city.isHasReligion(iEsus):
					cf.giftUnit(iManes, iInfernal, 0, pPlot, city.getOwner(), iEsus)
				if city.isHasReligion(iVeil):
					cf.giftUnit(iManes, iInfernal, 0, pPlot, city.getOwner(), iVeil)
				if city.isHasReligion(iHand):
					if iAuricPlayer == -1:
						cf.giftUnit(iManes, iInfernal, 0, pPlot, city.getOwner(), iHand)
					else:
						cf.giftUnitToPlayer(iManes, iAuricPlayer, 0, pPlot, city.getOwner(), iHand)
						cf.giftUnitToPlayer(iManes, iAuricPlayer, 0, pPlot, city.getOwner(), iHand)
						cf.giftUnitToPlayer(iManes, iAuricPlayer, 0, pPlot, city.getOwner(), iHand)
				if city.isHasReligion(iUnblemished):
					cf.giftUnit(iAngel, iMercurians, 0, pPlot, city.getOwner(), iUnblemished)
				if city.isHasReligion(iBrotherhood):
					cf.giftUnit(iAngel, iMercurians, 0, pPlot, city.getOwner(), iBrotherhood)

				if city.isHasReligion(iStewards):
					cf.giftUnit(iManes, iInfernal, 0, pPlot, city.getOwner(), iStewards)
				if city.isHasReligion(iCoven):
					cf.giftUnit(iManes, iInfernal, 0, pPlot, city.getOwner(), iCoven)
				if city.isHasReligion(iAnointed):
					cf.giftUnit(iManes, iInfernal, 0, pPlot, city.getOwner(), iAnointed)

				if city.isHasReligion(iOne):
					break

##			if iAuricPlayer != -1:
##				if iOwner == iAuricPlayer:
##					for i in xrange(1+city.getPopulation()/4):
##						cf.giftUnitToPlayer(iManes, iAuricPlayer, 0, pPlot, city.getOwner(),iHand)

			if ownerPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
				for i in xrange(1+city.getPopulation()/3):
					cf.giftUnit(iManes, iInfernal, 0, pPlot, city.getOwner(),-1)

			elif ownerPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_NEUTRAL'):
				for i in xrange(1 + city.getPopulation()/10):
					cf.giftUnit(iManes, iInfernal, 0, pPlot, city.getOwner(),-1)
					cf.giftUnit(iManes, iInfernal, 0, pPlot, city.getOwner(),-1)
					cf.giftUnit(iAngel, iMercurians, 0, pPlot, city.getOwner(),-1)

			elif ownerPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
				for i in xrange(1 + city.getPopulation()/5):
					cf.giftUnit(iAngel, iMercurians, 0, pPlot, city.getOwner(),-1)

		if city.getNumBuilding(gc.getInfoTypeForString('BUILDING_NEW_MULYR')) > 0:
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS'))



		sName = "Inhabitant of " + city.getName().encode('latin_1','replace') + "'s Sluagh"
		listRaces = []
		iCulture = city.getCulture(iOwner)
		iPop = city.getPopulation()

		jCult = pPlot.calculateCulturePercent(iOwner)
		if jCult > 95:
			pjPlayer = gc.getPlayer(iOwner)
			if pjPlayer > -1:
				jCiv = pjPlayer.getCivilizationType()
				jCivInfo = gc.getCivilizationInfo(jCiv)
				jRace = jCivInfo.getDefaultRace()
				if jRace == gc.getInfoTypeForString('PROMOTION_DEMON'):
					iPop -= 1
				else:
					listRaces.append(jRace)
		else:
			for jPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
				jCult = pPlot.calculateCulturePercent(jPlayer)
				if jCult > 0:
					pjPlayer = gc.getPlayer(jPlayer)
					if pjPlayer > -1:
						jCiv = pjPlayer.getCivilizationType()
						jCivInfo = gc.getCivilizationInfo(jCiv)
						jRace = jCivInfo.getDefaultRace()
						if jRace == gc.getInfoTypeForString('PROMOTION_DEMON'):
							iPop -= 1
						else:
							for i in xrange(jCult):
								listRaces.append(jRace)

		for i in xrange(iPop):
			newUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(gc.getInfoTypeForString('UNIT_SLUAGH'), iX, iY, UnitAITypes.UNITAI_SETTLE, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setScenarioCounter(gc.getInfoTypeForString('UNIT_SETTLER'))
			newUnit.setName(sName)
			newUnit.setDuration(CyGame().getSorenRandNum(city.getPopulation(), sName+str(i) +"'s Duration"))
			iXP = min(500, CyGame().getSorenRandNum(iCulture/iPop, sName+str(i) +"'s Experience"))
			newUnit.setExperience(iXP, -1)
			iRel = CyGame().getSorenRandNum(gc.getNumReligionInfos(), sName+str(i)+"'s religion")
			if iRel != -1:
				if city.isHasReligion(iRel):
					newUnit.setReligion(iRel)
			if len(listRaces) > 0:
				iRace = listRaces[0]
				if len(listRaces) > 1:
					iRace = listRaces.pop(CyGame().getSorenRandNum(len(listRaces), sName+str(i)+"'s Race"))
				if iRace != -1:
					newUnit.setHasPromotion(iRace, True)


		if CyGame().getWBMapScript():
			sf.onCityRazed(city, iPlayer)

		CvUtil.pyPrint("City Razed Event: %s" %(city.getName(),))

	def onCityAcquired(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'City Acquired'
		iPreviousOwner,iNewOwner,pCity,bConquest,bTrade = argsList
		pPlayer = gc.getPlayer(iNewOwner)
		pPrevious = gc.getPlayer(iPreviousOwner)
		pOriginal = gc.getPlayer(pCity.getOriginalOwner())

		iCiv = pPlayer.getCivilizationType()
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
		iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
		iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
		iUndertow = gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS')
		if iCiv == iInfernal:
			cf.removeReligion(gc.getInfoTypeForString('RELIGION_THE_ORDER'), pCity)
			cf.removeReligion(gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'), pCity)
			pCity.setHasReligion(gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'), True, True, True)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DEMONIC_CITIZENS'), 1)

			if pCity.getCivilizationType() == iMercurians:
				pCity.setCivilizationType(iInfernal)
				CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

		else:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DEMONIC_CITIZENS'), 0)
			if iCiv == iMercurians:
				cf.removeReligion(iVeil, pCity)
				cf.removeReligion(iUndertow, pCity)
				if pCity.getCivilizationType() == iInfernal:
					pCity.setCivilizationType(iMercurians)
					CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

			elif iCiv == gc.getInfoTypeForString('CIVILIZATION_KHAZAD'):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DWARVEN_VAULT'), 1)
				cf.doTurnKhazad(iNewOwner)

		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_PLANAR_GATE')) > 0:
			if not pCity.hasBonus(gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_PLANAR_GATE'), False)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED'), True)

		iStateReligion = pPlayer.getStateReligion()
		iAlignment = pPlayer.getAlignment()
		iLeader = pPlayer.getLeaderType()
		iGood = gc.getInfoTypeForString('ALIGNMENT_GOOD')
		iEvil = gc.getInfoTypeForString('ALIGNMENT_EVIL')

		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN') or pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')) or iAlignment == iGood
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN'), bFriendly)
			
		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BLIND_BROTHERHOOD')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD_HOSTILE')) > 0:
		
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BLIND_BROTHERHOOD'), True)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD_HOSTILE'), False)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD'), False)
			else:
				bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS') or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_PACIFISM')) or iAlignment == iGood
				
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BLIND_BROTHERHOOD'), False)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD_HOSTILE'), not bFriendly)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD'), bFriendly)
			
		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_ARTIFICERY')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_ARTIFICERY_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RINGGIVER') or iAlignment == iGood or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_ARETE'))
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARTIFICERY_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARTIFICERY'), bFriendly)

		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ORDER') or iAlignment == iGood
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER'), bFriendly)

		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() in [gc.getInfoTypeForString('RELIGION_UNBLEMISHED'),gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')] or iAlignment == iGood
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED'), bFriendly)
			
		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH') or (iAlignment != iEvil and pPlayer.getStateReligion() != gc.getInfoTypeForString('RELIGION_FOXMEN'))
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH'), bFriendly)

		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS') or iAlignment != iGood
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS'), bFriendly)

		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY') or iAlignment != iGood
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE'), bFriendly)

		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_ANOINTED') or iAlignment == iEvil
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED'), bFriendly)
			
		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL') or iAlignment == iEvil
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL'), bFriendly)
			
		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TOPHET')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TOPHET_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_EMBER_LEGION') or iAlignment == iEvil
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TOPHET_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TOPHET'), bFriendly)
			
		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_INTERSTICE')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_INTERSTICE_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COVEN') or  (iAlignment == iEvil and pCity.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_CALABIM'))
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_INTERSTICE_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_INTERSTICE'), bFriendly)

		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_WHITE_HAND')
			if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
				iAuricPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
				if iAuricPlayer != -1:
					pAuricPlayer = gc.getPlayer(iAuricPlayer)
					if pAuricPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AURIC')) > 0:
						iTeam = pPlayer.getTeam()
						eTeam = gc.getTeam(iTeam)
						iAuricTeam = pAuricPlayer.getTeam()
						if iAuricTeam == iTeam:
							bFriendly = True
						elif eTeam.isVassal(iTeam):
							bFriendly = True
						elif eTeam.isAtWar(iAuricTeam):
							bFriendly = False
							
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND'), bFriendly)

		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE')) + pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE_HOSTILE')) > 0:
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS') or pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')) or iAlignment == iEvil
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE_HOSTILE'), not bFriendly)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE'), bFriendly)


		bRevolt = True
		for sBuilding in ['BUILDING_TOWER_OF_COMPLACENCY', 'BUILDING_PILLAR_OF_CHAINS', 'BUILDING_UNYIELDING_ORDER','BUILDING_UNYIELDING_ORDER_GREATER']:
			if pCity.getNumBuilding(gc.getInfoTypeForString(sBuilding)) > 0:
				bRevolt=False
				break
		if not bRevolt:
			pCity.setOccupationTimer(0)
			CyGame().changeCrime(-5)
			if pCity.getRevolutionIndex() > 0:
				pCity.setRevolutionIndex(0)


		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_EYES_AND_EARS_NETWORK')):
			iTeam = pPlayer.getTeam()
			eTeam = gc.getTeam(iTeam)
			iSidar = gc.getInfoTypeForString('CIVILIZATION_SIDAR')
			if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')):

				for jPlayer in xrange(gc.getMAX_PLAYERS()):
					if iNewOwner == jPlayer:continue
					pPlayer2 = gc.getPlayer(jPlayer)
					if pPlayer2.isAlive():
						if pPlayer2.isBarbarian():continue
						if pPlayer2.getCivilizationType() == iSidar:continue
						iTeam2 = pPlayer2.getTeam()
						eTeam2 = gc.getTeam(iTeam2)
						if eTeam2.isAlive():
							if eTeam.isHasMet(iTeam2):
								eTeam.changeStolenVisibilityTimer(iTeam2, 2)

			if pPrevious.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')):
				iTeam = pPrevious.getTeam()
				eTeam = gc.getTeam(iTeam)

				for iTeam2 in xrange(gc.getMAX_TEAMS()):
					if iTeam == iTeam2:continue
					eTeam2 = gc.getTeam(iTeam2)
					if eTeam2.isAlive():
						while eTeam.isStolenVisibility(iTeam2):
							eTeam.changeStolenVisibilityTimer(iTeam2, -1)




		if CyGame().getWBMapScript():
			sf.onCityAcquired(iPreviousOwner, iNewOwner, pCity, bConquest, bTrade)
## END FFH

	def onCityAcquiredAndKept(self, argsList):
		'City Acquired and Kept'
		iOwner,pCity = argsList

		#Functions added here tend to cause OOS issues

#### messages - wonder captured start by The_J (modified by Terkhen) ####
		#UI only stuff should be okay, though.
		if pCity.getNumWorldWonders() > 0:
			for i in range(gc.getNumBuildingInfos()):
				if pCity.getNumBuilding(i) > 0:
					pThisBuilding = gc.getBuildingInfo(i)
					if gc.getBuildingClassInfo(pThisBuilding.getBuildingClassType()).getMaxGlobalInstances() == 1:
						pConquerPlayer = gc.getPlayer(pCity.getOwner())
						iConquerTeam = pConquerPlayer.getTeam()
						sConquerName = pConquerPlayer.getName()
						sWonderName = pThisBuilding.getDescription()
						iX = pCity.getX()
						iY = pCity.getY()

						for iLoopPlayer in range (gc.getMAX_CIV_PLAYERS()):
							iLoopTeam = gc.getPlayer(iLoopPlayer).getTeam()
							if iLoopTeam == iConquerTeam or gc.getTeam(iLoopTeam).isHasMet(iConquerTeam):

								if iLoopPlayer == pCity.getOwner():
									sText = "TXT_KEY_YOU_CAPTURED_WONDER"
								else:
									sText = "TXT_KEY_CAPTURED_WONDER"

								if iLoopTeam == iConquerTeam:
									sColor = "COLOR_GREEN"
								else:
									sColor = "COLOR_RED"
								CyInterface().addMessage(iLoopPlayer, False, 15, CyTranslator().getText(sText, (sConquerName,sWonderName)), '', 0,'Art/Interface/Buttons/General/warning_popup.dds', ColorTypes(gc.getInfoTypeForString(sColor)), iX, iY, True, True)
#### messages - wonder captured end ####

		CvUtil.pyPrint('City Acquired and Kept Event: %s' %(pCity.getName()))

	def onCityLost(self, argsList):
		'City Lost'
		city = argsList[0]
		player = PyPlayer(city.getOwner())
		if (not self.__LOG_CITYLOST):
			return
		CvUtil.pyPrint('City %s was lost by Player %d Civilization %s'
			%(city.getName(), player.getID(), player.getCivilizationName()))

	def onCultureExpansion(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'City Culture Expansion'
		pCity = argsList[0]
		iPlayer = argsList[1]
		CvUtil.pyPrint("City %s's culture has expanded" %(pCity.getName(),))

	def onCityGrowth(self, argsList):
		'City Population Growth'
		pCity = argsList[0]
		iPlayer = argsList[1]
		CvUtil.pyPrint("%s has grown" %(pCity.getName(),))

	def onCityDoTurn(self, argsList):
		'City Production'
		pCity = argsList[0]
		iPlayer = argsList[1]
		pPlayer = gc.getPlayer(pCity.getOwner())

		if not pCity.isSettlement():
			if pCity.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_KURIOTATES') or pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_CITY_OF_A_THOUSAND_SLUMS')) > 0 or pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_ABUNDANCE')) > 0:
				pCity.setPlotRadius(3)


		iStateReligion = pPlayer.getStateReligion()
		iAlignment = pPlayer.getAlignment()
		iLeader = pPlayer.getLeaderType()
		iGood = gc.getInfoTypeForString('ALIGNMENT_GOOD')
		iEvil = gc.getInfoTypeForString('ALIGNMENT_EVIL')
		
		
		for iBuilding in xrange(gc.getNumBuildingInfos()):
			if pCity.getNumBuilding(iBuilding):
				infoBuilding = gc.getBuildingInfo(iBuilding)
				if infoBuilding.isRequiresCaster():
					iBonus = infoBuilding.getPrereqAndBonus()
					if iBonus != -1:
						if pCity.getNumBonuses(iBonus) < 1:
							pCity.changeFreeBonus(iBonus, 1)
							pCity.setNumRealBuilding(iBuilding, False)
							pCity.changeFreeBonus(iBonus, -1)
							pCity.setNumRealBuilding(iBuilding, True)
			

		iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_THE_ONE')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_THE_ONE_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == -1

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)
					

		iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN') or pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')) or iAlignment == iGood

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)
					
		iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS') or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_PACIFISM')) or iAlignment == iGood

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)
					
		iTempleFriendly = gc.getInfoTypeForString('BUILDING_ARTIFICERY')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_ARTIFICERY_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RINGGIVER') or iAlignment == iGood or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_ARETE'))

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)
					
		iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ORDER') or iAlignment == iGood

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)
					
		iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED_HOSTILE')
		bFriendly = pPlayer.getStateReligion() in [gc.getInfoTypeForString('RELIGION_UNBLEMISHED'),gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')] or iAlignment == iGood

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)
					
		iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH') or (iAlignment != iEvil and pPlayer.getStateReligion() != gc.getInfoTypeForString('RELIGION_FOXMEN'))

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)
					
		iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS') or iAlignment != iGood

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)
					
		iTempleFriendly = gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY') or iAlignment != iGood

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)

		iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_ANOINTED') or iAlignment == iEvil

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)
					
		iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL') or iAlignment == iEvil

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)
					
		iTempleFriendly = gc.getInfoTypeForString('BUILDING_TOPHET')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_TOPHET_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_EMBER_LEGION') or iAlignment == iEvil

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)
					
					
		iTempleFriendly = gc.getInfoTypeForString('BUILDING_INTERSTICE')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_INTERSTICE_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COVEN') or  (iAlignment == iEvil and pCity.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_CALABIM'))

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)
					
		iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_WHITE_HAND')
		if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
			iAuricPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
			if iAuricPlayer != -1:
				pAuricPlayer = gc.getPlayer(iAuricPlayer)
				if pAuricPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AURIC')) > 0:
					iTeam = pPlayer.getTeam()
					eTeam = gc.getTeam(iTeam)
					iAuricTeam = pAuricPlayer.getTeam()
					if iAuricTeam == iTeam:
						bFriendly = True
					elif eTeam.isVassal(iTeam):
						bFriendly = True
					elif eTeam.isAtWar(iAuricTeam):
						bFriendly = False

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)

		iTempleFriendly = gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE')
		iTempleHostile = gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE_HOSTILE')
		bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS') or pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')) or iAlignment == iEvil

		if pCity.getNumBuilding(iTempleFriendly) > 0 or pCity.getNumBuilding(iTempleHostile) > 0:
			pCity.setNumRealBuilding(iTempleHostile, not bFriendly)
			pCity.setNumRealBuilding(iTempleFriendly, bFriendly)
		else:
			iProduction = pCity.getBuildingProduction(iTempleFriendly) + pCity.getBuildingProduction(iTempleHostile)
			if iProduction > 0:
				if bFriendly:
					pCity.setBuildingProduction(iTempleFriendly, iProduction)
					pCity.setBuildingProduction(iTempleHostile, 0)
				else:
					pCity.setBuildingProduction(iTempleHostile, iProduction)
					pCity.setBuildingProduction(iTempleFriendly, 0)

		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_PLANAR_GATE')) > 0:
			if not pCity.hasBonus(gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_PLANAR_GATE'), False)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED'), True)

		elif pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED')) > 0:
			pass
		else:
			iProduction = pCity.getBuildingProduction(gc.getInfoTypeForString('BUILDING_PLANAR_GATE')) + pCity.getBuildingProduction(gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED'))
			if iProduction > 0:
				if pCity.hasBonus(gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')):
					pCity.setBuildingProduction(gc.getInfoTypeForString('BUILDING_PLANAR_GATE'), iProduction)
					pCity.setBuildingProduction(gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED'), 0)
				else:
					pCity.setBuildingProduction(gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED'), iProduction)
					pCity.setBuildingProduction(gc.getInfoTypeForString('BUILDING_PLANAR_GATE'), 0)


		iSlyph = gc.getInfoTypeForString('BUILDING_SLYPH_SEARCH')
		if pCity.getNumBuilding(iSlyph) > 0:
			iRel = gc.getInfoTypeForString('RELIGION_FOXMEN')
			iAir = gc.getInfoTypeForString('BONUS_MANA_AIR')
			iEarth = gc.getInfoTypeForString('BONUS_MANA_EARTH')
			iDuration = CyGame().getGameTurn() - pCity.getBuildingOriginalTime(iSlyph)
			if iDuration > min(2,(pCity.getNumBonuses(iAir) - pCity.getNumBonuses(iEarth))):

				if iDuration % (1+pCity.getNumBonuses(iAir)) == 0:
					ltFoxmenCities = []
					for iPlayerLoop in xrange(gc.getMAX_PLAYERS()):
						pPlayerLoop = gc.getPlayer(iPlayerLoop)
						if pPlayerLoop.getHasReligionCount(iRel):
							for pyCity in PyPlayer(iPlayerLoop).getCityList():
								loopCity = pyCity.GetCy()
								if loopCity.isHasReligion(iRel) and loopCity != pCity:
									ltFoxmenCities.append(loopCity)
					while pCity in ltFoxmenCities:
						ltFoxmenCities.remove(pCity)
					if len(ltFoxmenCities) > 1:
						pNewHolyCity = ltFoxmenCities.pop(CyGame().getSorenRandNum(len(ltFoxmenCities), "Foxmen find new Holy City "))
						if pNewHolyCity != pCity:
							pCity.setNumRealBuilding(iSlyph, 0)
							pCity.setHasReligion(iRel, pNewHolyCity.isHasReligion(iRel),False,False)
							CyGame().clearHolyCity(iRel)
							CyGame().setHolyCity(iRel, pNewHolyCity, False)
							pNewHolyCity.setNumRealBuilding(iSlyph, 1)
			elif not pCity.isHasReligion(iRel):
				pCity.setHasReligion(iRel,True,False,False)


		bRevolt = True
		for sBuilding in ['BUILDING_TOWER_OF_COMPLACENCY', 'BUILDING_PILLAR_OF_CHAINS', 'BUILDING_UNYIELDING_ORDER','BUILDING_UNYIELDING_ORDER_GREATER','BUILDING_DEMONIC_CITIZENS']:
			if pCity.getNumBuilding(gc.getInfoTypeForString(sBuilding)) > 0:
				bRevolt=False
				break
		if not bRevolt:
			pCity.setOccupationTimer(0)
			CyGame().changeCrime(-5)
			if pCity.getRevolutionIndex() > 0:
				pCity.setRevolutionIndex(0)
		else:
			if pCity.isHasReligion(gc.getInfoTypeForString('RELIGION_COVEN')):
				if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
					iDisrupt = pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_SLAVE'))/pPlayer.getNumCities()
					
					if pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_SLAVERY')):
						iDisrupt += pCity.getHurryAngerTimer()
					iDisrupt = CyGame().getSorenRandNum(iDisrupt, "Disrupt - Chainbreakers")
					pCity.changeRevolutionIndex(iDisrupt)
					CyGame().changeCrime(iDisrupt)
					if iDisrupt > 8:
						pCity.changeOccupationTimer(1)
						CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_CHAINBREAKERS_REVOLT", (pCity.getName(),)),'',1,'Art/Interface/Buttons/Religions/ChainBreakers.dds',ColorTypes(gc.getInfoTypeForString("COLOR_RED")),pCity.getX(),pCity.getY(),True,True)


		if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD'):

			if pCity.isProductionUnit():
				if pCity.getOccupationTimer() > 0 or pPlayer.getAnarchyTurns() > 0:
					iUnit = pCity.getProductionUnit()
					iProduction = pCity.getUnitProduction(iUnit)
					iProduction += pCity.getHurryAngerTimer()+pCity.getOccupationTimer() + pPlayer.getAnarchyTurns()
					pCity.setUnitProduction(iUnit, iProduction)
					while pCity.getProductionNeeded() < iProduction:
						newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pCity.applyBuildEffects(newUnit)
						iProduction -= pCity.getProductionNeeded()

						for j in xrange(pCity.getOrderQueueLength()):
							iOrderData = pCity.getOrderFromQueue(j)
							if iOrderData.eOrderType == OrderTypes.ORDER_TRAIN:
								pCity.popOrder(j, False, False)
								iUnit = pCity.getProductionUnit()
								break
						else:
							iUnit = pCity.getConscriptUnit()
						pCity.setUnitProduction(iUnit, iProduction)

		CvAdvisorUtils.cityAdvise(pCity, iPlayer)

	def onCityBuildingUnit(self, argsList):
		'City begins building a unit'
		pCity = argsList[0]
		iUnitType = argsList[1]
		if (not self.__LOG_CITYBUILDING):
			return
		CvUtil.pyPrint("%s has begun building a %s" %(pCity.getName(),gc.getUnitInfo(iUnitType).getDescription()))

	def onCityBuildingBuilding(self, argsList):
		'City begins building a Building'
		pCity = argsList[0]
		iBuildingType = argsList[1]
		if (not self.__LOG_CITYBUILDING):
			return
		CvUtil.pyPrint("%s has begun building a %s" %(pCity.getName(),gc.getBuildingInfo(iBuildingType).getDescription()))

	def onCityRename(self, argsList):
		'City is renamed'
		pCity = argsList[0]
		if (pCity.getOwner() == gc.getGame().getActivePlayer()):
			self.__eventEditCityNameBegin(pCity, True)

	def onCityHurry(self, argsList):
		'City is renamed'
		pCity = argsList[0]
		iHurryType = argsList[1]

	def onVictory(self, argsList):
		'Victory'
		iTeam, iVictory = argsList
		if (iVictory >= 0 and iVictory < gc.getNumVictoryInfos()):
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive():
					if pPlayer.isHuman():
						if pPlayer.getTeam() == iTeam:
							if CyGame().getWBMapScript():
								sf.onVictory(iPlayer, iVictory)
							else:
								iCiv = pPlayer.getCivilizationType()
								if iCiv == gc.getInfoTypeForString('CIVILIZATION_AMURITES'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_AMURITES", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_BALSERAPHS'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_BALSERAPHS", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_BANNOR'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_BANNOR", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_CALABIM", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_CLAN_OF_EMBERS", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_DOVIELLO", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_ELOHIM", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_GRIGORI'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_GRIGORI", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_HIPPUS'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_HIPPUS", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_ILLIANS", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_INFERNAL", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_KHAZAD'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_KHAZAD", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_KURIOTATES", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_LANUN'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_LANUN", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_LJOSALFAR", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_LUCHUIRP", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_MALAKIM", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_MERCURIANS", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_SHEAIM", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_SIDAR", 1)
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_SVARTALFAR", 1)

								if iVictory == gc.getInfoTypeForString('VICTORY_ALTAR_OF_THE_LUONNOTAR'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_ALTAR_OF_THE_LUONNOTAR", 1)
								elif iVictory == gc.getInfoTypeForString('VICTORY_CONQUEST'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_CONQUEST", 1)
								elif iVictory == gc.getInfoTypeForString('VICTORY_CULTURAL'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_CULTURAL", 1)
								elif iVictory == gc.getInfoTypeForString('VICTORY_DOMINATION'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_DOMINATION", 1)
								elif iVictory == gc.getInfoTypeForString('VICTORY_RELIGIOUS'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_RELIGIOUS", 1)
								elif iVictory == gc.getInfoTypeForString('VICTORY_SCORE'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_SCORE", 1)
								elif iVictory == gc.getInfoTypeForString('VICTORY_TIME'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_TIME", 1)
								elif iVictory == gc.getInfoTypeForString('VICTORY_TOWER_OF_MASTERY'):
									CyGame().changeTrophyValue("TROPHY_VICTORY_TOWER_OF_MASTERY", 1)

								if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_BARBARIAN_WORLD):
									CyGame().changeTrophyValue("TROPHY_VICTORY_BARBARIAN_WORLD", 1)
								if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_CHALLENGE_CUT_LOSERS):
									CyGame().changeTrophyValue("TROPHY_VICTORY_FINAL_FIVE", 1)
								if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_CHALLENGE_HIGH_TO_LOW):
									CyGame().changeTrophyValue("TROPHY_VICTORY_HIGH_TO_LOW", 1)
								if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_CHALLENGE_INCREASING_DIFFICULTY):
									CyGame().changeTrophyValue("TROPHY_VICTORY_INCREASING_DIFFICULTY", 1)

			victoryInfo = gc.getVictoryInfo(int(iVictory))
			CvUtil.pyPrint("Victory! Team %d achieves a %s victory"
				%(iTeam, victoryInfo.getDescription()))

	def onVassalState(self, argsList):
		'Vassal State'
		iMaster, iVassal, bVassal = argsList

		if (bVassal):
			CvUtil.pyPrint("Team %d becomes a Vassal State of Team %d"
				%(iVassal, iMaster))
		else:
			CvUtil.pyPrint("Team %d revolts and is no longer a Vassal State of Team %d"
				%(iVassal, iMaster))

	def onGameUpdate(self, argsList):
		'sample generic event, called on each game turn slice'
		genericArgs = argsList[0][0]	# tuple of tuple of my args
		turnSlice = genericArgs[0]

#FfH: 10/15/2008 Added by Kael for OOS logging.
		OOSLogger.doGameUpdate()
#FfH: End add

	def onMouseEvent(self, argsList):
		'mouse handler - returns 1 if the event was consumed'
		eventType,mx,my,px,py,interfaceConsumed,screens = argsList
		if ( px!=-1 and py!=-1 ):
			if ( eventType == self.EventLButtonDown ):
				if (self.bAllowCheats and self.bCtrl and self.bAlt and CyMap().plot(px,py).isCity() and not interfaceConsumed):
					# Launch Edit City Event
					CvEventManager.beginEvent(self, CvUtil.EventEditCity, (px,py) )
					return 1

				elif (self.bAllowCheats and self.bCtrl and self.bShift and not interfaceConsumed):
					# Launch Place Object Event
					CvEventManager.beginEvent(self, CvUtil.EventPlaceObject, (px, py) )
					return 1

		if ( eventType == self.EventBack ):
			return CvScreensInterface.handleBack(screens)
		elif ( eventType == self.EventForward ):
			return CvScreensInterface.handleForward(screens)

		return 0


#################### TRIGGERED EVENTS ##################

	def __eventPlaceObjectBegin(self, argsList):
		'Place Object Event'
		CvDebugTools.CvDebugTools().initUnitPicker(argsList)

	def __eventPlaceObjectApply(self, playerID, userData, popupReturn):
		'Place Object Event Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyUnitPicker( (popupReturn, userData) )

	def __eventAwardTechsAndGoldBegin(self, argsList):
		'Award Techs & Gold Event'
		CvDebugTools.CvDebugTools().cheatTechs()

	def __eventAwardTechsAndGoldApply(self, playerID, netUserData, popupReturn):
		'Award Techs & Gold Event Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyTechCheat( (popupReturn) )

	def __eventShowWonderBegin(self, argsList):
		'Show Wonder Event'
		CvDebugTools.CvDebugTools().wonderMovie()

	def __eventShowWonderApply(self, playerID, netUserData, popupReturn):
		'Wonder Movie Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyWonderMovie( (popupReturn) )

## Platy Builder ##

	def __eventEditUnitNameBegin(self, argsList):
		pUnit = argsList
		popup = PyPopup.PyPopup(CvUtil.EventEditUnitName, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData((pUnit.getID(), CyGame().getActivePlayer()))
		popup.setBodyString(localText.getText("TXT_KEY_RENAME_UNIT", ()))
		popup.createEditBox(pUnit.getNameNoDesc())
		popup.setEditBoxMaxCharCount(25)
		popup.launch()

	def __eventEditUnitNameApply(self, playerID, userData, popupReturn):
		unit = gc.getPlayer(userData[1]).getUnit(userData[0])
		newName = popupReturn.getEditBoxString(0)
		unit.setName(newName)
		if CyGame().GetWorldBuilderMode():
			WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeStats()
			WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeCurrentUnit()

	def __eventEditCityNameBegin(self, city, bRename):
		popup = PyPopup.PyPopup(CvUtil.EventEditCityName, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData((city.getID(), bRename, CyGame().getActivePlayer()))
		popup.setHeaderString(localText.getText("TXT_KEY_NAME_CITY", ()))
		popup.setBodyString(localText.getText("TXT_KEY_SETTLE_NEW_CITY_NAME", ()))
		popup.createEditBox(city.getName())
		popup.setEditBoxMaxCharCount(15)
		popup.launch()

	def __eventEditCityNameApply(self, playerID, userData, popupReturn):
		city = gc.getPlayer(userData[2]).getCity(userData[0])
		cityName = popupReturn.getEditBoxString(0)
		city.setName(cityName, not userData[1])
		if CyGame().GetWorldBuilderMode() and not CyGame().isInAdvancedStart():
			WBCityEditScreen.WBCityEditScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeStats() # lfgr fix: Added constructor parameter
## Platy Builder ##

#Magister Start
	def __eventEditPlayerNameBegin(self, argsList):
		pUnit = argsList
		popup = PyPopup.PyPopup(6666, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData((pPlayer.getID(),))
		popup.setBodyString(localText.getText("TXT_KEY_MENU_LEADER_NAME", ()))
		popup.createEditBox(pPlayer.getName())
		popup.launch()

	def __eventEditPlayerNameApply(self, playerID, userData, popupReturn):
		'Edit Player Name Event'
		newName = popupReturn.getEditBoxString(0)
		if (len(newName) > 25):
			newName = newName[:25]
		gc.getPlayer(playerID).setName(newName)
		if CyGame().GetWorldBuilderMode():
			WBPlayerScreen.WBPlayerScreen().placeStats()

	def __eventEditCivNameBegin(self, argsList):
		pUnit = argsList
		popup = PyPopup.PyPopup(6777, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData((pPlayer.getID(),))
		popup.setBodyString(localText.getText("TXT_KEY_RENAME_PLAYER", ()))
		popup.setBodyString(CyTranslator().getText("TXT_KEY_MENU_CIV_DESC", ()))
		popup.createEditBox(pPlayer.getCivilizationDescription(pPlayer.getID()))
		popup.launch()

	def __eventEditCivNameApply(self, playerID, userData, popupReturn):
		'Edit Player Name Event'
		pPlayer = gc.getPlayer(playerID)
		szNewDesc = pPlayer.getCivilizationDescription(playerID)
		szNewShort = pPlayer.getCivilizationShortDescription(playerID)
		szNewAdj = pPlayer.getCivilizationAdjective(playerID)
		sNew = popupReturn.getEditBoxString(0)
		if (len(sNew) > 25):
			sNew = sNew[:25]
		pPlayer.setCivName(sNew,szNewShort, szNewAdj)
		if CyGame().GetWorldBuilderMode():
			WBPlayerScreen.WBPlayerScreen().placeStats()

	def __eventEditCivShortNameBegin(self, argsList):
		pUnit = argsList
		popup = PyPopup.PyPopup(6888, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData((pPlayer.getID(),))
		popup.setBodyString(localText.getText("TXT_KEY_RENAME_PLAYER", ()))
		popup.setBodyString(CyTranslator().getText("TXT_KEY_MENU_CIV_SHORT_DESC", ()))
		popup.createEditBox(pPlayer.getCivilizationShortDescription(pPlayer.getID()))
		popup.launch()

	def __eventEditCivShortNameApply(self, playerID, userData, popupReturn):
		'Edit Player Name Event'
		pPlayer = gc.getPlayer(playerID)
		szNewDesc = pPlayer.getCivilizationDescription(playerID)
		szNewShort = pPlayer.getCivilizationShortDescription(playerID)
		szNewAdj = pPlayer.getCivilizationAdjective(playerID)
		sNew = popupReturn.getEditBoxString(0)
		if (len(sNew) > 25):
			sNew = sNew[:25]
		pPlayer.setCivName(szNewDesc,sNew, szNewAdj)
		if CyGame().GetWorldBuilderMode():
			WBPlayerScreen.WBPlayerScreen().placeStats()

	def __eventEditCivAdjBegin(self, argsList):
		pUnit = argsList
		popup = PyPopup.PyPopup(6999, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData((pPlayer.getID(),))
		popup.setBodyString(localText.getText("TXT_KEY_RENAME_PLAYER", ()))
		popup.setBodyString(CyTranslator().getText("TXT_KEY_MENU_CIV_ADJ", ()))
		popup.createEditBox(pPlayer.getCivilizationAdjective(pPlayer.getID()))
		popup.launch()

	def __eventEditCivAdjApply(self, playerID, userData, popupReturn):
		'Edit Player Name Event'
		pPlayer = gc.getPlayer(playerID)
		szNewDesc = pPlayer.getCivilizationDescription(playerID)
		szNewShort = pPlayer.getCivilizationShortDescription(playerID)
		szNewAdj = pPlayer.getCivilizationAdjective(playerID)
		sNew = popupReturn.getEditBoxString(0)
		if (len(sNew) > 25):
			sNew = sNew[:25]
		pPlayer.setCivName(szNewDesc,szNewShort, sNew)
		if CyGame().GetWorldBuilderMode():
			WBPlayerScreen.WBPlayerScreen().placeStats()
#Magister Stop

	def __eventWBPlayerScriptPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		gc.getPlayer(userData[0]).setScriptData(CvUtil.convertToStr(sScript))
		WBPlayerScreen.WBPlayerScreen().placeScript()
		return

	def __eventWBCityScriptPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		pCity = gc.getPlayer(userData[0]).getCity(userData[1])
		pCity.setScriptData(CvUtil.convertToStr(sScript))
		WBCityEditScreen.WBCityEditScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript() # lfgr fix: Added constructor parameter
		return

	def __eventWBUnitScriptPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		pUnit = gc.getPlayer(userData[0]).getUnit(userData[1])
		pUnit.setScriptData(CvUtil.convertToStr(sScript))
		WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
		return

	def __eventWBScriptPopupBegin(self):
		return

	def __eventWBGameScriptPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		CyGame().setScriptData(CvUtil.convertToStr(sScript))
		WBGameDataScreen.WBGameDataScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
		return

	def __eventWBPlotScriptPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		pPlot = CyMap().plot(userData[0], userData[1])
		pPlot.setScriptData(CvUtil.convertToStr(sScript))
		WBPlotScreen.WBPlotScreen().placeScript()
		return

	def __eventWBLandmarkPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		pPlot = CyMap().plot(userData[0], userData[1])
		iPlayer = userData[2]
		if userData[3] > -1:
			pSign = CyEngine().getSignByIndex(userData[3])
			iPlayer = pSign.getPlayerType()
			CyEngine().removeSign(pPlot, iPlayer)
		if len(sScript):
			if iPlayer == gc.getBARBARIAN_PLAYER():
				CyEngine().addLandmark(pPlot, CvUtil.convertToStr(sScript))
			else:
				CyEngine().addSign(pPlot, iPlayer, CvUtil.convertToStr(sScript))
		WBPlotScreen.iCounter = 10
		return
## Platy Builder ##

## FfH Card Game: begin
	def __EventSelectSolmniumPlayerBegin(self):
		iHUPlayer = gc.getGame().getActivePlayer()

		if iHUPlayer == -1 : return 0
		if not cs.canStartGame(iHUPlayer) : return 0

		popup = PyPopup.PyPopup(CvUtil.EventSelectSolmniumPlayer, EventContextTypes.EVENTCONTEXT_ALL)

		sResText = CyUserProfile().getResolutionString(CyUserProfile().getResolution())
		sX, sY = sResText.split("x")
		iXRes = int(sX)
		iYRes = int(sY)

		iW = 620
		iH = 650

		popup.setSize(iW, iH)
		popup.setPosition((iXRes - iW) / 2, 30)

		lStates = []

		for iPlayer in xrange(gc.getMAX_CIV_PLAYERS()) :
			pPlayer = gc.getPlayer(iPlayer)

			if pPlayer.isNone() : continue

			if pPlayer.isHuman() :
				lPlayerState = cs.getStartGameMPWith(iHUPlayer, iPlayer)
				if lPlayerState[0][0] in ["No", "notMet"] : continue
				lStates.append([iPlayer, lPlayerState])
			else :
				lPlayerState = cs.getStartGameAIWith(iHUPlayer, iPlayer)
				if lPlayerState[0][0] in ["No", "notMet"] : continue
				lStates.append([iPlayer, lPlayerState])

		lPlayerButtons = []

		popup.addDDS(CyArtFileMgr().getInterfaceArtInfo("SOMNIUM_POPUP_INTRO").getPath(), 0, 0, 512, 128)
		popup.addSeparator()
		#popup.setHeaderString(localText.getText("TXT_KEY_SOMNIUM_START", ()), CvUtil.FONT_CENTER_JUSTIFY)
		if len(lStates) == 0 :
			popup.setBodyString(localText.getText("TXT_KEY_SOMNIUM_NOONE_MET", ()))
		else :
			#popup.setBodyString(localText.getText("TXT_KEY_SOMNIUM_PLAY_WITH", ()))
			popup.addSeparator()
			popup.addSeparator()

			sText = u""
			for iPlayer, lPlayerState in lStates :
				pPlayer = gc.getPlayer(iPlayer)
				sPlayerName = pPlayer.getName()
				iPositiveChange = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getMemoryAttitudePercent(MemoryTypes.MEMORY_SOMNIUM_POSITIVE) / 100
				iNegativeChange = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getMemoryAttitudePercent(MemoryTypes.MEMORY_SOMNIUM_NEGATIVE) / 100
				bShift = True

				for item in lPlayerState :

					sTag = item[0]
					if (sTag == "atWar") :
						if len(sText) > 0 : sText += localText.getText("[NEWLINE]", ())
						sText += localText.getText("TXT_KEY_SOMNIUM_AT_WAR", (sPlayerName, ))

					elif (sTag == "InGame") :
						if len(sText) > 0 : sText += localText.getText("[NEWLINE]", ())
						sText += localText.getText("TXT_KEY_SOMNIUM_IN_GAME", (sPlayerName, ))

					elif (sTag == "relation") :
						delay = item[1]
						if (delay > 0) :
							if len(sText) > 0 : sText += localText.getText("[NEWLINE]", ())
							sText += localText.getText("TXT_KEY_SOMNIUM_GAME_DELAYED", (sPlayerName, delay))
						else :
							if bShift :
								bShift = False
								popup.addSeparator()
							popup.addButton(localText.getText("TXT_KEY_SOMNIUM_GAME_RELATION", (sPlayerName, iPositiveChange, iNegativeChange)))
							lPlayerButtons.append((iPlayer, -1))

					elif (sTag == "gold") :
						for iGold in item[1] :
							if bShift :
								bShift = False
								popup.addSeparator()
							if iGold == 0 :
								popup.addButton(localText.getText("TXT_KEY_SOMNIUM_GAME_FUN", (sPlayerName, )))
								lPlayerButtons.append((iPlayer, iGold))
							else :
								popup.addButton(localText.getText("TXT_KEY_SOMNIUM_GAME_GOLD", (sPlayerName, iGold)))
								lPlayerButtons.append((iPlayer, iGold))

			if len(sText) > 0 :
				popup.addSeparator()
				popup.addSeparator()
				popup.setBodyString(sText)

		popup.setUserData(tuple(lPlayerButtons))
		popup.launch()

	def __EventSelectSolmniumPlayerApply(self, playerID, userData, popupReturn):
		if userData :
			idButtonCliked = popupReturn.getButtonClicked()
			if idButtonCliked in range(len(userData)) :
				iOpponent, iGold = userData[idButtonCliked]

				pLeftPlayer = gc.getPlayer(playerID)
				pRightPlayer = gc.getPlayer(iOpponent)

				if not pRightPlayer.isHuman() :
					if (cs.canStartGame(playerID)) and (pLeftPlayer.isAlive()) and (pRightPlayer.isAlive()) :
						cs.startGame(playerID, iOpponent, iGold)
					else :
						CyInterface().addMessage(playerID, True, 25, CyTranslator().getText("TXT_KEY_SOMNIUM_CANT_START_GAME", (gc.getPlayer(iOpponent).getName(), )), '', 1, '', ColorTypes(7), -1, -1, False, False)
				else :
					if (cs.canStartGame(playerID)) and (cs.canStartGame(iOpponent)) and (pLeftPlayer.isAlive()) and (pRightPlayer.isAlive()) :
						if (iOpponent == gc.getGame().getActivePlayer()):
							self.__EventSolmniumAcceptGameBegin((playerID, iOpponent, iGold))
					else :
						CyInterface().addMessage(playerID, True, 25, CyTranslator().getText("TXT_KEY_SOMNIUM_CANT_START_GAME", (gc.getPlayer(iOpponent).getName(), )), '', 1, '', ColorTypes(7), -1, -1, False, False)

	def __EventSolmniumAcceptGameBegin(self, argslist):
		iPlayer, iOpponent, iGold = argslist
		if not gc.getPlayer(iOpponent).isAlive() : return 0

		popup = PyPopup.PyPopup(CvUtil.EventSolmniumAcceptGame, EventContextTypes.EVENTCONTEXT_ALL)

		popup.setUserData(argslist)

		popup.setHeaderString(localText.getText("TXT_KEY_SOMNIUM_START", ()))
		if iGold > 0 :
			popup.setBodyString(localText.getText("TXT_KEY_SOMNIUM_ACCEPT_GAME", (gc.getPlayer(iPlayer).getName(), iGold)))
		else :
			popup.setBodyString(localText.getText("TXT_KEY_SOMNIUM_ACCEPT_GAME_FUN", (gc.getPlayer(iPlayer).getName(), )))

		popup.addButton( localText.getText("AI_DIPLO_ACCEPT_1", ()) )
		popup.addButton( localText.getText("AI_DIPLO_NO_PEACE_3", ()) )

		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __EventSolmniumAcceptGameApply(self, playerID, userData, popupReturn):
		if userData :
			iPlayer, iOpponent, iGold = userData
			idButtonCliked = popupReturn.getButtonClicked()
			if idButtonCliked == 0 :
				if (cs.canStartGame(iPlayer)) and (cs.canStartGame(iOpponent)) and (gc.getPlayer(iPlayer).isAlive()) and (gc.getPlayer(iOpponent).isAlive()) :
					cs.startGame(iPlayer, iOpponent, iGold)
				else :
					CyInterface().addMessage(iPlayer, True, 25, CyTranslator().getText("TXT_KEY_SOMNIUM_CANT_START_GAME", (gc.getPlayer(iOpponent).getName(), )), '', 1, '', ColorTypes(7), -1, -1, False, False)
					CyInterface().addMessage(iOpponent, True, 25, CyTranslator().getText("TXT_KEY_SOMNIUM_CANT_START_GAME", (gc.getPlayer(iPlayer).getName(), )), '', 1, '', ColorTypes(7), -1, -1, False, False)
			else :
					CyInterface().addMessage(iPlayer, True, 25, CyTranslator().getText("TXT_KEY_SOMNIUM_REFUSE_GAME", (gc.getPlayer(iOpponent).getName(), iGold)), '', 1, '', ColorTypes(7), -1, -1, False, False)

	def __EventSolmniumConcedeGameBegin(self, argslist):
		popup = PyPopup.PyPopup(CvUtil.EventSolmniumConcedeGame, EventContextTypes.EVENTCONTEXT_ALL)

		popup.setUserData(argslist)

		popup.setHeaderString(localText.getText("TXT_KEY_SOMNIUM_START", ()))
		popup.setBodyString(localText.getText("TXT_KEY_SOMNIUM_CONCEDE_GAME", ()))

		popup.addButton( localText.getText("AI_DIPLO_ACCEPT_1", ()) )
		popup.addButton( localText.getText("AI_DIPLO_NO_PEACE_3", ()) )

		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __EventSolmniumConcedeGameApply(self, playerID, userData, popupReturn):
		if userData :
			idButtonCliked = popupReturn.getButtonClicked()
			if idButtonCliked == 0 :
				cs.endGame(userData[0], userData[1])
## FfH Card Game: end





