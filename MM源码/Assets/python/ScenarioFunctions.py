#Set aside for scenario specific functions, the epic game should never use this file
# does anyone actually read these comments?

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import CustomFunctions
import CvEspionageAdvisor


# globals
cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer


class ScenarioFunctions:

	def addPopupWB(self, szText, sDDS):
		szTitle = CyGameTextMgr().getTimeStr(CyGame().getGameTurn(), False)
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xRes = screen.getXResolution()
		yRes = screen.getYResolution()
		popup = PyPopup.PyPopup(-1)
		popup.addDDS(sDDS, 0, 0, 500, 800)
		popup.addSeparator()
		popup.setHeaderString(szTitle)
		popup.setBodyString(szText)
		popup.setPosition((xRes - 840) / 2,(yRes - 640) / 2)
		popup.setSize(840, 640)
		popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

	def cannotResearch(self, ePlayer, eTech, bTrade):
		pPlayer = gc.getPlayer(ePlayer)
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			return True
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_RETURN_OF_WINTER):
			if gc.getTechInfo(eTech).getEra() == gc.getInfoTypeForString('ERA_MEDIEVAL'):
				return True


		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			if not pPlayer.isHuman():
				if eTech in [gc.getInfoTypeForString('TECH_ORDERS_FROM_HEAVEN'), gc.getInfoTypeForString('TECH_HONOR'), gc.getInfoTypeForString('TECH_WAY_OF_THE_EARTHMOTHER'), gc.getInfoTypeForString('TECH_WAY_OF_THE_FORESTS')]:
					return True

		return False

	def cannotConstruct(self,pCity,eBuilding,bContinue,bTestVisible,bIgnoreCost):

		pPlayer = gc.getPlayer(pCity.getOwner())
##		iBuildingClass = gc.getBuildingInfo(eBuilding).getBuildingClassType()
##		eTeam = gc.getTeam(pPlayer.getTeam())

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			if not pPlayer.isHuman():
				if eBuilding == gc.getInfoTypeForString('BUILDING_HERON_THRONE'):
					return True
		return False

	def cannotDoCivic(self, ePlayer, eCivic):
		pPlayer = gc.getPlayer(ePlayer)
		eTeam = gc.getTeam(pPlayer.getTeam())
		iCiv = pPlayer.getCivilizationType()

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			if pPlayer.getTeam() == 1:
				if eCivic in [gc.getInfoTypeForString('CIVIC_UNDERCOUNCIL'), gc.getInfoTypeForString('CIVIC_NO_MEMBERSHIP')]:
					return True

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				if eCivic in [gc.getInfoTypeForString('CIVIC_UNDERCOUNCIL'), gc.getInfoTypeForString('CIVIC_NO_MEMBERSHIP')]:
					return True
			elif iCiv == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				if eCivic in [gc.getInfoTypeForString('CIVIC_OVERCOUNCIL'), gc.getInfoTypeForString('CIVIC_NO_MEMBERSHIP')]:
					return True

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_GREY):
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
				if eCivic in [gc.getInfoTypeForString('CIVIC_UNDERCOUNCIL'), gc.getInfoTypeForString('CIVIC_NO_MEMBERSHIP')]:
					return True
			elif iCiv == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				if eCivic in [gc.getInfoTypeForString('CIVIC_OVERCOUNCIL'), gc.getInfoTypeForString('CIVIC_NO_MEMBERSHIP')]:
					return True
			elif iCiv == gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
				if eCivic in [gc.getInfoTypeForString('CIVIC_UNDERCOUNCIL'), gc.getInfoTypeForString('CIVIC_OVERCOUNCIL')]:
					return True

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_WAGES_OF_SIN):
			if eCivic in [gc.getInfoTypeForString('CIVIC_UNDERCOUNCIL'), gc.getInfoTypeForString('CIVIC_NO_MEMBERSHIP')]:
				if iCiv in [gc.getInfoTypeForString('CIVILIZATION_ELOHIM'),gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'),gc.getInfoTypeForString('CIVILIZATION_MALAKIM'),gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')]:
					return True
			if eCivic == gc.getInfoTypeForString('CIVIC_OVERCOUNCIL') or eCivic == gc.getInfoTypeForString('CIVIC_NO_MEMBERSHIP'):
				if iCiv in [gc.getInfoTypeForString('CIVILIZATION_CALABIM'), gc.getInfoTypeForString('CIVILIZATION_INFERNAL'),gc.getInfoTypeForString('CIVILIZATION_SHEAIM'),gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')]:
					return True
		return False

	def cannotTrain(self, pCity, eUnit, bContinue, bTestVisible, bIgnoreCost, bIgnoreUpgrades):
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
			if pPlayer.isHuman():
				return True

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			if pPlayer.isHuman():
				if eUnit != gc.getInfoTypeForString('UNIT_HUNTER'):
					return True
			else:
				return True

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			if not pPlayer.isHuman():
				if gc.getUnitInfo(eUnit).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_NAVAL'):
					if eUnit != gc.getInfoTypeForString('UNIT_WORKBOAT'):
						return True

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
			if eUnit == gc.getInfoTypeForString('UNIT_SETTLER'):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_PERPENTACH'):
					return True

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			if not pPlayer.isHuman():
				if gc.getTeam(pPlayer.getTeam()).isHuman():
					if isWorldUnitClass(gc.getUnitInfo(eUnit).getUnitClassType()):
						return True

		return False

	def onEndPlayerTurn(self, iGameTurn, iPlayer):
		'Called at the end of a players turn'

		pPlayer = gc.getPlayer(iPlayer)


	def doTurn(self):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_WALL):
			self.doTurnAgainstTheWall()
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT):
			self.doTurnBarbarianAssault()
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
			self.doTurnBeneathTheHeel()
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			self.doTurnFallOfCuantine()
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			self.doTurnGrandMenagerie()
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			if gc.getPlayer(0).isHuman():
				self.doTurnIntoTheDesertMalakim()
			else:
				self.doTurnIntoTheDesertCalabim()
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			self.doTurnLordOfTheBalors()
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			self.doTurnMulcarnReborn()
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_RETURN_OF_WINTER):
			self.doTurnReturnOfWinter()
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			self.doTurnTheBlackTower()
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
			self.doTurnTheMomus()
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			self.doTurnSplinteredCourt()
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			self.doTurnTheRadiantGuard()

	def doTurnAgainstTheWall(self):
		iPlayer = 0
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.getNumCities() < 5:
			if gc.getGame().getScenarioCounter() != 0:
				gc.getGame().changeScenarioCounter(-1 * gc.getGame().getScenarioCounter())
		else:
			gc.getGame().changeScenarioCounter(1)
			if gc.getGame().getScenarioCounter() == 100:
				gc.getGame().setWinner(pPlayer.getTeam(), 2)

	def doTurnBarbarianAssault(self):
		if gc.getGame().countCivPlayersAlive() > 5:
			gc.getGame().changeCutLosersCounter(-1)
			if gc.getGame().getCutLosersCounter() == 0:
				iClanOfEmbers = gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS')
				iWorstPlayerRank = -1
				iWorstPlayer = -1
				for iPlayer in range(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.isAlive():
						if pPlayer.getCivilizationType() != iClanOfEmbers:
							if gc.getGame().getPlayerRank(iPlayer) > iWorstPlayerRank:
								iWorstPlayerRank = gc.getGame().getPlayerRank(iPlayer)
								iWorstPlayer = iPlayer
				gc.getPlayer(iWorstPlayer).setAlive(False)
				gc.getGame().changeCutLosersCounter(50)

	def doTurnBeneathTheHeel(self):
		iPlayer = 0
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.getGold() >= 80:
			pCity = pPlayer.getCapitalCity()
			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_RECRUIT_MERCENARY')
			triggerData = pPlayer.initTriggeredData(iEvent, true, -1, pCity.getX(), pCity.getY(), iPlayer, pCity.getID(), -1, -1, -1, -1)
		eTeam = gc.getTeam(3) #Calabim
		iTeam2 = 0 #Hippus
		if eTeam.isAlive():
			if eTeam.AI_getAtPeaceCounter(iTeam2) > 50:
				if eTeam.isHasMet(iTeam2):
					if eTeam.getAtWarCount(True) == 0:
						eTeam.declareWar(iTeam2, False, WarPlanTypes.WARPLAN_TOTAL)
		pCity = gc.getPlayer(1).getCapitalCity() #Illians
		pPlot = pCity.plot()
		bWin = False
		iBarnaxus = gc.getInfoTypeForString('EQUIPMENT_PIECES_OF_BARNAXUS')
		iPromBarnaxus = gc.getInfoTypeForString('PROMOTION_PIECES_OF_BARNAXUS')
		for i in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.getUnitType() == iBarnaxus:
				bWin = True
			if pUnit.isHasPromotion(iPromBarnaxus):
				bWin = True
		if bWin:
			gc.getGame().setWinner(pPlayer.getTeam(), 2)

	def doTurnFallOfCuantine(self):
		iPlayer = 0 #Decius
		pPlayer = gc.getPlayer(iPlayer)
		if gc.getGame().getScenarioCounter() == 7:
			gc.getGame().setWinner(pPlayer.getTeam(), 2)
		if gc.getGame().getScenarioCounter() == 6:
			gc.getGame().changeScenarioCounter(1)
			iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_FALL_OF_CUANTINE_FLEE')
			triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, 0, -1, -1, -1, -1, -1)
		if gc.getGame().getScenarioCounter() == 3:
			gc.getGame().changeScenarioCounter(1)
			cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_LANUN",()), iPlayer)
			eTeam = gc.getTeam(pPlayer.getTeam())
			if not eTeam.isAtWar(1):
				eTeam.declareWar(1, True, WarPlanTypes.WARPLAN_TOTAL)
			eTeam.setPermanentWarPeace(1, True)
			CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
		if gc.getGame().getScenarioCounter() == 0:
			pPlot = CyMap().plot(24,12)
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getOwner() == iPlayer:
					if gc.getGame().getScenarioCounter() == 0:
						gc.getGame().changeScenarioCounter(1)
						pCity = pPlot.getPlotCity()
						pPlayer.acquireCity(pCity,False,False)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_ORDER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_CONFESSOR",()), iPlayer)
						CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_CONFESSOR_BALLOON",()),'',1,'Art/Interface/Buttons/Units/Priest Order.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
						CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)

		pPlot = CyMap().plot(16,2)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_JUNGLE_ALTAR'):
			iChance = gc.getHandicapInfo(gc.getGame().getHandicapType()).getLairSpawnRate()
			if gc.getGame().getSorenRandNum(100, "Fall of Cuantine") < iChance:
				iRnd = gc.getGame().getSorenRandNum(100, "Fall of Cuantine")
				if iRnd < 50:
					iUnit = gc.getInfoTypeForString('UNIT_FREAK')
				else:
					iUnit = gc.getInfoTypeForString('UNIT_DROWN')
				bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
				bPlayer.initUnit(iUnit, 16, 2, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	def doTurnGrandMenagerie(self):
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		bBear = False
		bElephant = False
		bGorilla = False
		bGriffon = False
		bLion = False
		bTiger = False
		bWolf = False

		bSpider = False
		bScorpion = False
		bPanther = False
		bBaboon = False

		iSpider =gc.getInfoTypeForString('UNITCLASS_GIANT_SPIDER')
		iScorpion =gc.getInfoTypeForString('UNITCLASS_SCORPION')
		iPanther =gc.getInfoTypeForString('UNITCLASS_PANTHER')
		iBaboon =gc.getInfoTypeForString('UNITCLASS_BABOON')

		iBear = gc.getInfoTypeForString('UNITCLASS_BEAR')
		iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
		iElephant = gc.getInfoTypeForString('UNITCLASS_ELEPHANT')
		iForest = gc.getInfoTypeForString('FEATURE_FOREST')
		iGorilla = gc.getInfoTypeForString('UNITCLASS_GORILLA')
		iGriffon = gc.getInfoTypeForString('UNITCLASS_GRIFFON')
		iJungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
		iLion = gc.getInfoTypeForString('UNITCLASS_LION')
		iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
		iTiger = gc.getInfoTypeForString('UNITCLASS_TIGER')
		iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
		iWolf = gc.getInfoTypeForString('UNITCLASS_WOLF')
		iBird = gc.getInfoTypeForString('UNITCLASS_HAWK')

		if bPlayer.getUnitClassCount(iBird) < 1:
			bBird = True
			lBird = []
		if bPlayer.getUnitClassCount(iBaboon) < 1:
			bBaboon = True
			lBaboon = []
		if bPlayer.getUnitClassCount(iPanther) < 1:
			bPanther = True
			lPanther = []
		if bPlayer.getUnitClassCount(iSpider) < 1:
			bSpider = True
			lSpider = []
		if bPlayer.getUnitClassCount(iScorpion) < 1:
			bScorpion = True
			lScorpion = []

		if bPlayer.getUnitClassCount(iBear) < 2:
			bBear = True
			lBear = []
		if bPlayer.getUnitClassCount(iGorilla) < 1:
			bGorilla = True
			lGorilla = []
		if bPlayer.getUnitClassCount(iLion) < 2:
			bLion = True
			lLion = []
		if bPlayer.getUnitClassCount(iTiger) < 1:
			bTiger = True
			lTiger = []
		if bPlayer.getUnitClassCount(iWolf) < 2:
			bWolf = True
			lWolf = []
		if bPlayer.getUnitClassCount(iElephant) == 0:
			bElephant = True
			lElephant = []
		if bPlayer.getUnitClassCount(iGriffon) == 0:
			bGriffon = True
			lGriffon = []
		if (bBaboon or bPanther or bSpider or bScorpion or bBear or bElephant or bGorilla or bGriffon or bLion or bTiger or bWolf):
			for i in xrange (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if not pPlot.isVisibleToCivTeam():
					if bBear:
						if pPlot.getTerrainType() == iTundra:
							lBear.append(pPlot)
					if bElephant:
						if pPlot.getTerrainType() == iPlains:
							lElephant.append(pPlot)
					if bGorilla:
						if pPlot.getFeatureType() == iJungle:
							lGorilla.append(pPlot)

					if bBaboon:
						if pPlot.getFeatureType() == iJungle:
							lBaboon.append(pPlot)
					if bPanther:
						if pPlot.getFeatureType() == iJungle:
							lPanther.append(pPlot)
					if bSpider:
						if pPlot.getFeatureType() == iForest:
							lSpider.append(pPlot)
					if bScorpion:
						if pPlot.getTerrainType() == iDesert:
							lScorpion.append(pPlot)

					if bGriffon:
						if pPlot.isPeak():
							lGriffon.append(pPlot)
					if bLion:
						if pPlot.getTerrainType() == iDesert:
							lLion.append(pPlot)
					if bTiger:
						if pPlot.getFeatureType() == iJungle:
							lTiger.append(pPlot)
					if bWolf:
						if pPlot.getFeatureType() == iForest:
							lWolf.append(pPlot)
					if bBird:
						if pPlot.getFeatureType() == iForest:
							lBird.append(pPlot)
		if bBear:
			if len(lBear) > 0:
				pPlot = lBear[CyGame().getSorenRandNum(len(lBear), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_POLAR_BEAR'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bElephant:
			if len(lElephant) > 0:
				pPlot = lElephant[CyGame().getSorenRandNum(len(lElephant), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_ELEPHANT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bGorilla:
			if len(lGorilla) > 0:
				pPlot = lGorilla[CyGame().getSorenRandNum(len(lGorilla), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_GORILLA'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bGriffon:
			if len(lGriffon) > 0:
				pPlot = lGriffon[CyGame().getSorenRandNum(len(lGriffon), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_GRIFFON'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bLion:
			if len(lLion) > 0:
				pPlot = lLion[CyGame().getSorenRandNum(len(lLion), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_LION'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bTiger:
			if len(lTiger) > 0:
				pPlot = lTiger[CyGame().getSorenRandNum(len(lTiger), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_TIGER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bWolf:
			if len(lWolf) > 0:
				pPlot = lWolf[CyGame().getSorenRandNum(len(lWolf), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_WOLF'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		if bSpider:
			if len(lSpider) > 0:
				pPlot = lSpider[CyGame().getSorenRandNum(len(lSpider), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_GIANT_SPIDER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bScorpion:
			if len(lScorpion) > 0:
				pPlot = lScorpion[CyGame().getSorenRandNum(len(lScorpion), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_SCORPION'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bBaboon:
			if len(lBaboon) > 0:
				pPlot = lBaboon[CyGame().getSorenRandNum(len(lBaboon), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_BABOON'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bPanther:
			if len(lPanther) > 0:
				pPlot = lPanther[CyGame().getSorenRandNum(len(lPanther), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_PANTHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		iPlayer = 0 #Falamar
		pCity = gc.getPlayer(iPlayer).getCapitalCity()
		if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_GRAND_MENAGERIE')) > 0:
			gc.getGame().setWinner(gc.getPlayer(iPlayer).getTeam(), 2)

	def doTurnIntoTheDesertCalabim(self):
		iPlayer = 1 #Decius
		if gc.getGame().getGameTurn() == 3:
			cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_GOVERNOR",()), iPlayer)
		if gc.getGame().getScenarioCounter() > 0:
			if CyGame().getSorenRandNum(100, "Disciple Spawn") < 10:
				iVarn = 0
				pVarnPlayer = gc.getPlayer(iVarn)
				if pVarnPlayer.isAlive():
					pPlot = CyMap().plot(30,23)
					if not pPlot.isVisibleEnemyUnit(iVarn):
						pVarnPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_EMPYREAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if gc.getGame().getScenarioCounter() > 1:
			gc.getGame().changeScenarioCounter(-1)
			if gc.getGame().getScenarioCounter() == 1:
				cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_ATTACK",()), iPlayer)
		if gc.getGame().getScenarioCounter() == 1:
			bValid = True
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if not pLoopPlayer.isHuman():

					(pCity, iter) = pLoopPlayer.firstCity(False)
					while(pCity):
						if (not pCity.isNone() and pCity.getOwner() == iPlayer): #only valid cities

							if pCity.isHasReligion(gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')):
								bValid = False

						(pCity, iter) = pLoopPlayer.nextCity(iter, False)


			if bValid:
				gc.getGame().setWinner(gc.getPlayer(iPlayer).getTeam(), 2)

	def doTurnIntoTheDesertMalakim(self):
		if gc.getGame().getScenarioCounter() > 100:
			gc.getGame().changeScenarioCounter(-1)
			if gc.getGame().getScenarioCounter() == 100:
				iPlayer = 0 #Decius
				cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_COUNCIL",()), iPlayer)
				gc.getGame().changeScenarioCounter(-1)

	def doTurnLordOfTheBalors(self):
		iManeChance = 4 + int(gc.getGame().getHandicapType())
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
		iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
		iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')

		iManes = gc.getInfoTypeForString('UNIT_MANES')

##		pVarn = gc.getPlayer(0)
##		pCapria = gc.getPlayer(0)
##		pKeelyn = gc.getPlayer(2)
##		pEinion = gc.getPlayer(3)
##		pBasium = gc.getPlayer(4)

		pHyborem = gc.getPlayer(5)
		pJudecca = gc.getPlayer(6)
		pSallos = gc.getPlayer(7)
		pOuzza = gc.getPlayer(8)
		pMeresin = gc.getPlayer(9)
		pStatius = gc.getPlayer(10)
		pLethe = gc.getPlayer(11)

		iBarb = gc.getBARBARIAN_PLAYER()
		pBarb = gc.getPlayer(iBarb)

		iTaint = 0

		cf.giftUnitToPlayer(iManes, iBarb)

		for iPlayer in xrange(gc.getMAX_PLAYERS()-1,-1,-1):#Cyclying backwards makes sure that Demon Lords won't have temptation events just after they die
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isAlive():
				if pPlayer.getCivilizationType() == iInfernal:
					if pPlayer.getUnitClassCount(cf.getHero(pPlayer)) > 0:
						iTaint += 1
					else:
						(pLoopCity, iter) = pPlayer.firstCity(False)
						while(pLoopCity):
							if (not pLoopCity.isNone() and pLoopCity.getOwner() == iPlayer): #only valid cities
								pPlot = pLoopCity.plot()
								pPlayerNew = pBarb
								maxSecondCult = 0
								for jPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
									if jPlayer != iPlayer:
										pjPlayer = gc.getPlayer(jPlayer)
										if pjPlayer.isAlive():
											if pjPlayer.getStateReligion() == iVeil:
												if pLoopCity.getCulture(jPlayer) > maxSecondCult:
													pPlayerNew = pjPlayer
													maxSecondCult = pLoopCity.getCulture(jPlayer)
								pPlayerNew.acquireCity(pLoopCity, True, False)
								pLoopCity.setCivilizationType(iInfernal)
								for i in xrange(pPlot.getNumUnits()):
									pLoopUnit = pPlot.getUnit(i)
									if pLoopUnit.getOwner() == iPlayer:
										newUnit = pPlayerNew.initUnit(pLoopUnit.getUnitType(), pLoopUnit.getX(), pLoopUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
										newUnit.convert(pLoopUnit)
							(pLoopCity, iter) = pPlayer.nextCity(iter, False)

						pPlayer.setAlive(False)

				elif pPlayer.getCivilizationType() != iMercurians:
					iTeam = pPlayer.getTeam()
					eTeam = gc.getTeam(iTeam)

					bTempt = False
					if gc.getGame().getSorenRandNum(216, "Tempt") < 66:
						bTempt = True
						lList = []

					if pHyborem.isAlive():
						if not eTeam.isAtWar(pHyborem.getTeam()):
							if eTeam.getAtWarCount(True) < 1 or pPlayer.getStateReligion() != iVeil or eTeam.AI_getAtPeaceCounter(5) >= 216:
								eTeam.setPermanentWarPeace(5, False)
								gc.getTeam(pHyborem.getTeam()).declareWar(iTeam, True, WarPlanTypes.WARPLAN_TOTAL)
								gc.getTeam(pHyborem.getTeam()).makePeace(gc.getBARBARIAN_TEAM())
								eTeam.setPermanentWarPeace(5, True)

								eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), -1)
								if pPlayer.isHuman():
									cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEAL_DONE",()),'art/interface/popups/Hyborem.dds')
						elif bTempt:
							if pPlayer.canConvert(iVeil):
								lList += ['Hyborem']
					if pJudecca.isAlive():
						if not eTeam.isAtWar(pJudecca.getTeam()):
							if eTeam.getAtWarCount(True) < 1 or eTeam.AI_getAtPeaceCounter(6) >= 166:
								eTeam.setPermanentWarPeace(6, False)
								gc.getTeam(pJudecca.getTeam()).declareWar(iTeam, True, WarPlanTypes.WARPLAN_TOTAL)
								gc.getTeam(pHyborem.getTeam()).makePeace(gc.getBARBARIAN_TEAM())
								eTeam.setPermanentWarPeace(6, True)

								eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), -1)
								if pPlayer.isHuman():
									cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEAL_DONE",()),'art/interface/popups/Judecca.dds')
						elif bTempt:
							bValid = False
							lJudeccaData = []
							for i in xrange(5):
								if gc.getPlayer(i).isAlive() and gc.getPlayer(i).getTeam() != iTeam:
									if not eTeam.isAtWar(i):
										lJudeccaData = lJudeccaData + [i]
										bValid = True
							if bValid:
								lList += ['Judecca']
								iJudeccaData = lJudeccaData[CyGame().getSorenRandNum(len(lJudeccaData), "Pick Target")-1]
					if pSallos.isAlive():
						if not eTeam.isAtWar(pSallos.getTeam()):
							if eTeam.getAtWarCount(True) < 1 or eTeam.AI_getAtPeaceCounter(7) >= 66:
								eTeam.setPermanentWarPeace(7, False)
								gc.getTeam(pSallos.getTeam()).declareWar(iTeam, True, WarPlanTypes.WARPLAN_TOTAL)
								gc.getTeam(pHyborem.getTeam()).makePeace(gc.getBARBARIAN_TEAM())
								eTeam.setPermanentWarPeace(7, True)

								eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), -1)
								if pPlayer.isHuman():
									cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEAL_DONE",()),'art/interface/popups/Sallos.dds')
						elif bTempt:
							lList += ['Sallos']
					if pOuzza.isAlive():
						if not eTeam.isAtWar(pOuzza.getTeam()):
							if eTeam.getAtWarCount(True) < 1 or eTeam.AI_getAtPeaceCounter(8) >= 66:
								eTeam.setPermanentWarPeace(8, False)
								gc.getTeam(pOuzza.getTeam()).declareWar(iTeam, True, WarPlanTypes.WARPLAN_TOTAL)
								gc.getTeam(pHyborem.getTeam()).makePeace(gc.getBARBARIAN_TEAM())
								eTeam.setPermanentWarPeace(8, True)


								eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), -1)

								if pPlayer.isHuman():
									cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEAL_DONE",()),'art/interface/popups/Ouzza.dds')
						elif bTempt:
							(pLoopCity, iter) = pPlayer.firstCity(False)
							while(pLoopCity):
								if (not pLoopCity.isNone() and pLoopCity.getOwner() == iPlayer): #only valid cities
									if pLoopCity.getPopulation() > 1:
										lList += ['Ouzza']
										break
								(pLoopCity, iter) = pPlayer.nextCity(iter, False)
					if pMeresin.isAlive():
						if not eTeam.isAtWar(pMeresin.getTeam()):
							if eTeam.getAtWarCount(True) < 1 or eTeam.AI_getAtPeaceCounter(9) >= 36:
								eTeam.setPermanentWarPeace(9, False)
								gc.getTeam(pMeresin.getTeam()).declareWar(iTeam, True, WarPlanTypes.WARPLAN_TOTAL)
								gc.getTeam(pHyborem.getTeam()).makePeace(gc.getBARBARIAN_TEAM())
								eTeam.setPermanentWarPeace(9, True)

								eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), -1)
								if pPlayer.isHuman():
									cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEAL_DONE",()),'art/interface/popups/Meresin.dds')
						elif bTempt:
							lList += ['Meresin']
					if pStatius.isAlive():
						if not eTeam.isAtWar(pStatius.getTeam()):
							if eTeam.getAtWarCount(True) < 1 or eTeam.AI_getAtPeaceCounter(10) >= 166:
								eTeam.setPermanentWarPeace(10, False)
								gc.getTeam(pStatius.getTeam()).declareWar(iTeam, True, WarPlanTypes.WARPLAN_TOTAL)
								gc.getTeam(pHyborem.getTeam()).makePeace(gc.getBARBARIAN_TEAM())
								eTeam.setPermanentWarPeace(10, True)

								eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), -1)
								if pPlayer.isHuman():
									cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEAL_DONE",()),'art/interface/popups/Statius.dds')
						elif bTempt:

							# listCities = PyPlayer(iPlayer).getCityList()
							# while len(listCities) > 0:
								# pLoopCity = listCities.pop(CyGame().getSorenRandNum(len(listCities), "Statius Redemption"))
								# if gc.getPlayer(pLoopCity.getOriginalOwner()).getCivilizationType() == iInfernal:
									# iStatiusData = pLoopCity.getID()
									# lList += ['Statius']
									# break


							(pLoopCity, iter) = pPlayer.firstCity(False)
							while(pLoopCity):
								if (not pLoopCity.isNone() and pLoopCity.getOwner() == iPlayer): #only valid cities
									if gc.getPlayer(pLoopCity.getOriginalOwner()).getCivilizationType() == iInfernal:
										iStatiusData = pLoopCity.getID()
										lList += ['Statius']
										break
								(pLoopCity, iter) = pPlayer.nextCity(iter, False)
					if pLethe.isAlive():
						if not eTeam.isAtWar(pLethe.getTeam()):
							if eTeam.getAtWarCount(True) < 1 or eTeam.AI_getAtPeaceCounter(11) >= 36:
								eTeam.setPermanentWarPeace(11, False)
								gc.getTeam(pLethe.getTeam()).declareWar(iTeam, True, WarPlanTypes.WARPLAN_TOTAL)
								gc.getTeam(pHyborem.getTeam()).makePeace(gc.getBARBARIAN_TEAM())
								eTeam.setPermanentWarPeace(11, True)


								eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), -1)
								if pPlayer.isHuman():
									cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEAL_DONE",()),'art/interface/popups/Lethe.dds')
						elif bTempt:
							# (pLoopUnit, iter) = pPlayer.firstUnit(False)
							# while(pLoopUnit):
								# if not pLoopUnit.isDead(): #is the unit alive and valid?
									# if pLoopUnit.isAlive():
										# iLetheData = pLoopUnit.getID()
										# lList += ['Lethe']
										# break
								# (pLoopUnit, iter) = pPlayer.nextUnit(iter, False)


							listUnits = PyPlayer(iPlayer).getUnitList()
							while len(listUnits) > 0:
								pUnit = listUnits.pop(CyGame().getSorenRandNum(len(listUnits), "Lethe suicide"))
								if pUnit.isAlive():
									iLetheData = pUnit.getID()
									lList += ['Lethe']
									break

					if bTempt:
						if len(lList) > 2:
							sLeader = lList[CyGame().getSorenRandNum(len(lList), "Pick Leader")-1]

							if sLeader == 'Hyborem':
								iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_HYBOREM')
								triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, -1, -1, -1, -1, -1, -1)
							elif sLeader == 'Judecca':
								iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_JUDECCA')
								triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, iJudeccaData, -1, -1, -1, -1, -1)
							elif sLeader == 'Sallos':
								if pPlayer.getLeaderType() in [gc.getInfoTypeForString('LEADER_EINION'), gc.getInfoTypeForString('LEADER_VARN')]:
									iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_SALLOS_MALE')
								else:
									iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_SALLOS_FEMALE')
								triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, -1, -1, -1, -1, -1, -1)
							elif sLeader == 'Ouzza':
								iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_OUZZA')
								triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, -1, -1, -1, -1, -1, -1)
							elif sLeader == 'Meresin':
								iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_MERESIN')
								triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, -1, -1, -1, -1, -1, -1)
							elif sLeader == 'Statius':
								pCity = pPlayer.getCity(iStatiusData)
								iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_STATIUS')
								triggerData = pPlayer.initTriggeredData(iEvent, True, iStatiusData, pCity.getX(), pCity.getY(), -1, -1, -1, -1, -1, -1)
							elif sLeader == 'Lethe':
								pUnit = pPlayer.getUnit(iLetheData)
								iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_LETHE')
								triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pUnit.getX(), pUnit.getY(), -1, -1, -1, -1, iLetheData, -1)



		cf.giftUnit(iManes, iInfernal, iTaint)
		iTaint //= 2
		if iTaint > 0:
			iHallowed = gc.getInfoTypeForString('FEATURE_HALLOWED_GROUND')
			iEvil = gc.getInfoTypeForString('ALIGNMENT_EVIL')
			iGood = gc.getInfoTypeForString('ALIGNMENT_GOOD')
			for iX in xrange(CyMap().getGridWidth()-1,-1,-1):
				bFane = True
				for iY in xrange(CyMap().getGridHeight()-1,-1,-1):
					pPlot = CyMap().plot(iX,iY)
					if bFane:
						if iX < 51:
							if pPlot.getFeatureType() == iHallowed:
								bFane = False
								break

							elif iY < 35:
								if pPlot.isOwned():
									if gc.getPlayer(pPlot.getOwner()).getAlignment() == iGood:
										bFane = False
										break
						if pPlot.isOwned():
							if gc.getPlayer(pPlot.getOwner()).getAlignment() == iEvil:
								pPlot.changePlotCounter(iTaint)
								continue
						else:
							pPlot.changePlotCounter(iTaint)
							continue
					elif pPlot.isWater():
						pPlot.changePlotCounter(-pPlot.getPlotCounter())
						continue


	def doTurnMulcarnReborn(self):
		if gc.getGame().getGameTurn() == 5:
			iPlayer = cf.getOpenPlayer()
			iTeam = 1
			bSpawned = False
			pPlot = CyMap().plot(68,18)
			pPlot.setMoveDisabledAI(False)
			pPlot.setMoveDisabledHuman(False)
			pPlot = CyMap().plot(58,38)
			pPlot.setMoveDisabledAI(False)
			pPlot.setMoveDisabledHuman(False)
			if CyGame().getTrophyValue("TROPHY_WB_CIV_DECIUS") == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DECIUS_MALAKIM_INTRO",())
				CyGame().addPlayerAdvanced(iPlayer, iTeam, gc.getInfoTypeForString('LEADER_DECIUS'), gc.getInfoTypeForString('CIVILIZATION_MALAKIM'))
				gc.getPlayer(iPlayer).setAlignment(gc.getInfoTypeForString('ALIGNMENT_GOOD'))
				pPlot = CyMap().plot(68,18)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_SWORDSMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_SWORDSMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				bSpawned = True
			if CyGame().getTrophyValue("TROPHY_WB_CIV_DECIUS") == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DECIUS_CALABIM_INTRO",())
				CyGame().addPlayerAdvanced(iPlayer, iTeam, gc.getInfoTypeForString('LEADER_DECIUS'), gc.getInfoTypeForString('CIVILIZATION_CALABIM'))
				gc.getPlayer(iPlayer).setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_MOROI'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_MOROI'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				bSpawned = True
			if bSpawned:
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_HUNTER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_WORKER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_DECIUS'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('EQUIPMENT_NETHER_BLADE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

				if gc.getTeam(iTeam).isHuman():
					cf.addPopup(szText,'art/interface/popups/Decius.dds')
	def doTurnReturnOfWinter(self):
		pPlayer = gc.getPlayer(2) #Tethira
		if pPlayer.isAlive():
			if CyGame().getSorenRandNum(100, "Return of Winter") < (gc.getGame().getHandicapType() * 5):
				pCity = pPlayer.getCapitalCity()
				pTargetCity = gc.getPlayer(0).getCapitalCity()
				iUnit = gc.getInfoTypeForString('UNIT_WARRIOR')
				if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
					iUnit = gc.getInfoTypeForString('UNIT_AXEMAN')
				if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
					iUnit = gc.getInfoTypeForString('UNIT_CHAMPION')
				newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, pTargetCity.getX(), pTargetCity.getY(), 0, False, False, MissionAITypes.NO_MISSIONAI, newUnit.plot(), newUnit)
		pPlayer = gc.getPlayer(4) #Cardith
		if pPlayer.isAlive():
			if CyGame().getSorenRandNum(100, "Return of Winter") < (gc.getGame().getHandicapType() * 5):
				pCity = pPlayer.getCapitalCity()
				pTargetCity = gc.getPlayer(1).getCapitalCity()
				iUnit = gc.getInfoTypeForString('UNIT_WARRIOR')
				if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
					iUnit = gc.getInfoTypeForString('UNIT_AXEMAN')
				if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
					iUnit = gc.getInfoTypeForString('UNIT_CHAMPION')
				newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, pTargetCity.getX(), pTargetCity.getY(), 0, False, False, MissionAITypes.NO_MISSIONAI, newUnit.plot(), newUnit)

	def doTurnSplinteredCourt(self):
		if gc.getGame().getScenarioCounter() == 7:
			gc.getGame().changeScenarioCounter(-7)
		else:
			gc.getGame().changeScenarioCounter(1)

		iLjosalfar = gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR')
		iSvartalfar = gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')
		iCalabim = gc.getInfoTypeForString('CIVILIZATION_CALABIM')
		iDoviello = gc.getInfoTypeForString('CIVILIZATION_DOVIELLO')
		iDuin = gc.getInfoTypeForString('UNIT_DUIN')
		iWerewolf = gc.getInfoTypeForString('UNIT_WEREWOLF')
		iVampire = gc.getInfoTypeForString('PROMOTION_VAMPIRE')
		iWeak = gc.getInfoTypeForString('PROMOTION_WEAK')
		iStrong = gc.getInfoTypeForString('PROMOTION_STRONG')
		iImmigrants = gc.getInfoTypeForString('EVENTTRIGGER_IMMIGRANTS')
		iParith = gc.getGame().getTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH")
		iSmelting = gc.getInfoTypeForString('TECH_SMELTING')
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isAlive():
				iCiv = pPlayer.getCivilizationType()
				if iCiv in [iLjosalfar, iSvartalfar]:
					if gc.getGame().getScenarioCounter() == 0:
						if pPlayer.getNumCities() > 0:
							if CyGame().getSorenRandNum(100, "Immigrants") < 10:
								pCity = PyPlayer(iPlayer).getCityList()[CyGame().getSorenRandNum(pPlayer.getNumCities(), "Pick Immigrant City")-1]
								triggerData = pPlayer.initTriggeredData(iImmigrants, True, -1, pCity.getX(), pCity.getY(), iPlayer, pCity.getID(), -1, -1, -1, -1)
				elif iCiv == iDoviello:
					if gc.getGame().getScenarioCounter() == 0:#Dawn
						for pLoopUnit in PyPlayer(iPlayer).getUnitList():
							iUnit = pLoopUnit.getScenarioCounter()
							if iUnit != -1:
								newUnit = pPlayer.initUnit(iUnit, pLoopUnit.getX(), pLoopUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.convert(pLoopUnit)
								newUnit.setScenarioCounter(-1)
					elif gc.getGame().getScenarioCounter() == 4:#Dusk
						for pLoopUnit in PyPlayer(iPlayer).getUnitList():
							if not pLoopUnit.isOnlyDefensive():
								if pLoopUnit.isAlive():
									iUnit = pLoopUnit.getUnitType()
									if iUnit != iDuin:
										newUnit = pPlayer.initUnit(iWerewolf, pLoopUnit.getX(), pLoopUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
										newUnit.convert(pLoopUnit)
										newUnit.setScenarioCounter(iUnit)
				elif iCiv == iCalabim:
					if gc.getGame().getScenarioCounter() == 0:#Dawn
						for pLoopUnit in PyPlayer(iPlayer).getUnitList():
							if pLoopUnit.isHasPromotion(iVampire):
								pLoopUnit.setHasPromotion(iStrong, False)
								pLoopUnit.setHasPromotion(iWeak, True)
					elif gc.getGame().getScenarioCounter() == 4:#Dusk
						for pLoopUnit in PyPlayer(iPlayer).getUnitList():
							if pLoopUnit.isHasPromotion(iVampire):
								pLoopUnit.setHasPromotion(iWeak, False)
								pLoopUnit.setHasPromotion(iStrong, True)

				if iParith > 1 and pPlayer.isHuman():
					if gc.getTeam(pPlayer.getTeam()).isHasTech(iSmelting):
						szText = CyTranslator().getText("TXT_KEY_WB_THE_SPLINTERED_COURT_PARITH", ((gc.getUnitInfo(iParith).getDescription(), )))
						cf.addPlayerPopup(szText, iPlayer)
						pCity = pPlayer.getCapitalCity()
						if not pCity is None:
							newUnit = pPlayer.initUnit(iParith, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							gc.getGame().setTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH", 0)

	def doTurnTheBlackTower(self):
		bSanctuary = False
		if gc.getPlayer(2).isAlive():
			bSanctuary = True
		if gc.getPlayer(3).isAlive():
			bSanctuary = True
		if gc.getPlayer(4).isAlive():
			bSanctuary = True
		if bSanctuary:
			gc.getPlayer(1).changeSanctuaryTimer(1)
		iPlayer = 0 #Falamar
		pPlayer = gc.getPlayer(iPlayer)
		lTechs = ['TECH_FANATICISM', 'TECH_WARHORSES', 'TECH_IRON_WORKING', 'TECH_CONSTRUCTION', 'TECH_ARCHERY', 'TECH_POISONS']
		lUnits = ['UNIT_DONAL', 'UNIT_MAGNADINE', 'UNIT_GUYBRUSH', 'UNIT_BARNAXUS', 'UNIT_GILDEN', 'UNIT_ALAZKAN']
		lCivs = ['CIVILIZATION_BANNOR', 'CIVILIZATION_HIPPUS', 'CIVILIZATION_LANUN', 'CIVILIZATION_LUCHUIRP', 'CIVILIZATION_LJOSALFAR', 'CIVILIZATION_SVARTALFAR']
		for i in xrange(len(lUnits)):
			iUnit = gc.getInfoTypeForString(lUnits[i])
			if CyGame().getUnitCreatedCount(iUnit) == 0:
				if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString(lTechs[i])):
					bValid = True
					(pCity, iter) = pPlayer.firstCity(False)
					while(pCity):
						if (not pCity.isNone() and pCity.getOwner() == iPlayer): #only valid cities
							if (bValid and pCity.getCivilizationType() == gc.getInfoTypeForString(lCivs[i])):
								pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_WB_THE_BLACK_TOWER_HERO",()),'',1,gc.getUnitInfo(iUnit).getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
								bValid = False
						(pCity, iter) = pPlayer.nextCity(iter, False)

	def doTurnTheMomus(self):
		if not gc.getTeam(0).isAtWar(1): #if Falamar isnt at war with Perpentach
			gc.getGame().changeScenarioCounter(1)
			if gc.getGame().getScenarioCounter() == 20:
				gc.getGame().changeScenarioCounter(-20)
				iBestPlayer = -1
				iPerpentach = gc.getInfoTypeForString('LEADER_PERPENTACH')
				iRnd = CyGame().getSorenRandNum(100, "The Momus")
				if iRnd < 30:
					for iLoopTeam in xrange(gc.getMAX_TEAMS()):
						eTeam = gc.getTeam(iLoopTeam)
						if eTeam.isAlive():
							if iLoopTeam != 1: #Perpentach
								for iLoopTeam2 in xrange(gc.getMAX_TEAMS()):
									eTeam2 = gc.getTeam(iLoopTeam2)
									if eTeam2.isAlive():
										if iLoopTeam2 != 1: # Perpentach
											if iLoopTeam != iLoopTeam2:
												eTeam.setPermanentWarPeace(iLoopTeam2, False)
												eTeam.declareWar(iLoopTeam2, False, WarPlanTypes.WARPLAN_TOTAL)
												eTeam.setPermanentWarPeace(iLoopTeam2, True)
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_ALL_WAR",()),'art/interface/popups/Perpentach.dds')
				if iRnd >= 30 and iRnd < 70:
					iBestRank = 100
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if not pLoopPlayer.isBarbarian():
								if pLoopPlayer.getLeaderType() != iPerpentach:
									if gc.getGame().getPlayerRank(iLoopPlayer) < iBestRank:
										iBestPlayer = iLoopPlayer
										iBestRank = gc.getGame().getPlayerRank(iLoopPlayer)
				if iRnd >= 70:
					lList = []
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if not pLoopPlayer.isBarbarian():
								if pLoopPlayer.getLeaderType() != iPerpentach:
									lList.append(iLoopPlayer)
					if len(lList) >= 1:
						iBestPlayer = lList[CyGame().getSorenRandNum(len(lList), "The Momus")-1]
				if iBestPlayer != -1:
					iBestTeam = gc.getPlayer(iBestPlayer).getTeam()
					for iLoopTeam in xrange(gc.getMAX_TEAMS()):
						eTeam = gc.getTeam(iLoopTeam)
						if eTeam.isAlive():
							if iLoopTeam != iBestTeam:
								if not eTeam.isBarbarian():
									if iLoopTeam != 1: #Perpentach
										for iLoopTeam2 in xrange(gc.getMAX_TEAMS()):
											eTeam2 = gc.getTeam(iLoopTeam2)
											if eTeam2.isAlive():
												if not eTeam2.isBarbarian():
													if iLoopTeam2 != 1: # Perpentach
														if iLoopTeam != iLoopTeam2:
															eTeam.setPermanentWarPeace(iLoopTeam2, False)
															if iLoopTeam2 == iBestTeam:
																eTeam.declareWar(iLoopTeam2, False, WarPlanTypes.WARPLAN_TOTAL)
															else:
																eTeam.makePeace(iLoopTeam2)
															eTeam.setPermanentWarPeace(iLoopTeam2, True)
					pPlayer = gc.getPlayer(iBestPlayer)
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_FALAMAR'):
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_FALAMAR",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MAHON'):
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_MAHON",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SALLOS'):
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_SALLOS",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BEERI'):
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_BEERI",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_ULDANOR'):
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_ULDANOR",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TYA'):
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_TYA",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_WEEVIL'):
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_WEEVIL",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_FURIA'):
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_FURIA",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MELISANDRE'):
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_MELISANDRE",()),'art/interface/popups/Perpentach.dds')

	def doTurnTheRadiantGuard(self):
		if CyGame().getGameTurn() == 3:
			cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_CAPRIA",()),'art/interface/popups/Capria.dds')
		if CyGame().getGameTurn() == 40:
			pPlot = CyMap().plot(29,3)
			if pPlot.isCity():
				if pPlot.getOwner() == 2: #Hyborem
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_CAPRIA_2",()),'art/interface/popups/Capria.dds')
		if CyGame().getGameTurn() == 50:
			pPlot = CyMap().plot(29,3)
			if pPlot.isCity():
				if pPlot.getOwner() == 2: #Hyborem
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_CAPRIA_3",()),'art/interface/popups/Capria.dds')
		if CyGame().getGameTurn() == 60:
			pPlot = CyMap().plot(29,3)
			if pPlot.isCity():
				if pPlot.getOwner() == 2: #Hyborem
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_CAPRIA_LOST",()),'art/interface/popups/Capria.dds')
					gc.getPlayer(3).setAlive(False) #Capria
		iPlayer = 2 #Hyborem
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			(pCity, iter) = pPlayer.firstCity(False)
			while(pCity):
				if (not pCity.isNone() and pCity.getOwner() == iPlayer): #only valid cities

					iCounter = 160 - gc.getGame().getScenarioCounter()
					if iCounter == 160:
						iCounter = 125
					iRnd = CyGame().getSorenRandNum(iCounter, "doTurnTheRadiantGuard")
					iProm = -1
					iUnit = -1
					iNum = 1
					if iRnd > 20 and iRnd <= 25:
						iUnit = gc.getInfoTypeForString('UNIT_AXEMAN')
						iProm = gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
						iNum = 2
					elif iRnd <= 30:
						iUnit = gc.getInfoTypeForString('UNIT_SPECTRE')
					elif iRnd <= 35:
						iUnit = gc.getInfoTypeForString('UNIT_HORSEMAN')
					elif iRnd <= 40:
						iUnit = gc.getInfoTypeForString('UNIT_HORSEMAN')
						iNum = 2
					elif iRnd <= 45:
						iUnit = gc.getInfoTypeForString('UNIT_HELLHOUND')
					elif iRnd <= 50:
						iUnit = gc.getInfoTypeForString('UNIT_HELLHOUND')
						iNum = 2
					elif iRnd <= 55:
						iUnit = gc.getInfoTypeForString('UNIT_PIT_BEAST')
					elif iRnd <= 60:
						iUnit = gc.getInfoTypeForString('UNIT_PIT_BEAST')
						iNum = 2
					elif iRnd <= 65:
						iUnit = gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_VEIL')
					elif iRnd <= 70:
						iUnit = gc.getInfoTypeForString('UNIT_IRA')
					elif iRnd <= 75:
						iUnit = gc.getInfoTypeForString('UNIT_IRA')
						iNum = 2
					elif iRnd <= 80:
						iUnit = gc.getInfoTypeForString('UNIT_CHAMPION')
					elif iRnd <= 85:
						iUnit = gc.getInfoTypeForString('UNIT_BEAST_OF_AGARES')
					elif iRnd <= 90:
						iUnit = gc.getInfoTypeForString('UNIT_RANGER')
					elif iRnd <= 95:
						iUnit = gc.getInfoTypeForString('UNIT_HORSE_ARCHER')
					elif iRnd <= 100:
						iUnit = gc.getInfoTypeForString('UNIT_MANTICORE')
					elif iRnd <= 105:
						iUnit = gc.getInfoTypeForString('UNIT_HIGH_PRIEST_OF_THE_VEIL')
					elif iRnd <= 110:
						iUnit = gc.getInfoTypeForString('UNIT_IMMORTAL')
						iProm = gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
					elif iRnd <= 115:
						iUnit = gc.getInfoTypeForString('UNIT_EIDOLON')
						iProm = gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
					elif iRnd <= 120:
						iUnit = gc.getInfoTypeForString('UNIT_LICH')
						iProm = gc.getInfoTypeForString('PROMOTION_EXTENSION1')
					else:
						iUnit = gc.getInfoTypeForString('UNIT_BALOR')
						iProm = gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
					if iRnd > 140:
						iNum = 2
					if iUnit != -1:
						for i in xrange (iNum):
							newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
							newUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, 5, 13, 0, False, False, MissionAITypes.NO_MISSIONAI, newUnit.plot(), newUnit)
							if iProm != -1:
								newUnit.setHasPromotion(iProm, True)
				(pCity, iter) = pPlayer.nextCity(iter, False)


	def gameStart(self):
		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iTerrain = pPlot.getTerrainType()
			iImprovement = pPlot.getImprovementType()
			if iImprovement != -1:
				iBonus = gc.getImprovementInfo(iImprovement).getBonusConvert()
				if iBonus > -1:
					pPlot.setBonusType(iBonus)

			if pPlot.getPlotCounter() > 0:
				iBonus = pPlot.getBonusType(-1)


		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_GREY):
			pPlayer = gc.getPlayer(0)
			if pPlayer.isHuman():
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_AGAINST_THE_GREY_INTRO_MALAKIM",()), 'art/interface/popups/Against the Grey.dds')
			else:
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_AGAINST_THE_GREY_INTRO_CALABIM",()), 'art/interface/popups/Against the Grey.dds')

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_WALL):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_AGAINST_THE_WALL_INTRO",()), 'art/interface/popups/Against the Wall.dds')
			if CyGame().isHasTrophy("TROPHY_WB_BARBARIAN_ASSAULT"):
				gc.getPlayer(4).setAlive(False)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_INTRO",()), 'art/interface/popups/Barbarian Assault.dds')

			iForest = gc.getInfoTypeForString('FEATURE_FOREST')
			iJungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive():
					if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS'):
						pPlot = pPlayer.getStartingPlot()
						iX = pPlot.getX()
						iY = pPlot.getY()
						for iDirection in xrange(DirectionTypes.NUM_DIRECTION_TYPES):
							pLoopPlot = plotDirection(iX, iY, DirectionTypes(iDirection))

							if not pLoopPlot.isNone():
								if pLoopPlot.getFeatureType() in [iForest, iJungle]:
									pLoopPlot.setFeatureType(-1, -1)
						iUnit = -1
						iCiv = pPlayer.getCivilizationType()
						if iCiv == gc.getInfoTypeForString('CIVILIZATION_AMURITES'):
							iUnit = gc.getInfoTypeForString('UNIT_ADEPT')
						elif iCiv == gc.getInfoTypeForString('CIVILIZATION_BANNOR'):
							iUnit = gc.getInfoTypeForString('UNIT_AXEMAN')
						elif iCiv == gc.getInfoTypeForString('CIVILIZATION_HIPPUS'):
							iUnit = gc.getInfoTypeForString('UNIT_HORSEMAN')
						elif iCiv == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
							iUnit = gc.getInfoTypeForString('UNIT_ARCHER')
						elif iCiv == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
							iUnit = gc.getInfoTypeForString('UNIT_WOOD_GOLEM')
						elif iCiv == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
							iUnit = gc.getInfoTypeForString('UNIT_ARCHER')
						if iUnit != -1:
							pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_INTRO",()), 'art/interface/popups/Beneath the Heel.dds')

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BLOOD_OF_ANGELS):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_INTRO",()), 'art/interface/popups/Blood of Angels.dds')
			iXP = gc.getGame().getTrophyValue("TROPHY_WB_LUCIAN_XP")
			if iXP > 0:
				iPlayer = 0 #Mahala
				self.giftHeroXP(iPlayer, gc.getInfoTypeForString('UNIT_LUCIAN'), iXP)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_INTRO",()), 'art/interface/popups/Fall of Cuantine.dds')
			gc.getGame().setReligionSlotTaken(gc.getInfoTypeForString('RELIGION_THE_ORDER'), True)
			gc.getGame().setReligionSlotTaken(gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'), True)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_INTRO",()), 'art/interface/popups/Gift of Kylorin.dds')

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_INTRO",()), 'art/interface/popups/Grand Menagerie.dds')

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			if gc.getPlayer(0).isHuman():
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_INTRO",()), 'art/interface/popups/Into the Desert.dds')
			if gc.getPlayer(1).isHuman():
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_INTRO",()), 'art/interface/popups/Into the Desert Calabim.dds')

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			eBarbTeam = gc.getTeam(gc.getBARBARIAN_TEAM())
			gc.getPlayer(gc.getBARBARIAN_PLAYER()).setHasTrait(gc.getInfoTypeForString('TRAIT_FALLOW'), True)

			listInfernalStart = [CyMap().plot(6,45),CyMap().plot(29,32),CyMap().plot(44,37),CyMap().plot(61,26),CyMap().plot(73,8),CyMap().plot(74,30)]
			listInvaderStart = [CyMap().plot(3,13),CyMap().plot(15,8),CyMap().plot(26,8),CyMap().plot(37,9),CyMap().plot(47,10)]

			for iPlayer in xrange(gc.getMAX_PLAYERS()):#This had to be moved to a seperate loop so as to prevent the invaders from capturing infernal workers
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive():
					if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL') and pPlayer.getLeaderType() != gc.getInfoTypeForString('LEADER_HYBOREM'):
						pNewPlot = listInfernalStart.pop(CyGame().getSorenRandNum(len(listInfernalStart), "Infernal Start"))
						pNewPlot.setBonusType(-1)
						pNewPlot.setImprovementType(-1)
						pPlayer.setStartingPlot(pNewPlot, True)
						for iUnit in xrange(pNewPlot.getNumUnits()):
							pUnit = pPlot.getUnit(iUnit)
							pUnit.jumpToNearestValidPlot()

						for pLoopUnit in PyPlayer(iPlayer).getUnitList():
							pLoopUnit.setXY(pNewPlot.getX(), pNewPlot.getY(), True, True, False)


						pPlayer.initUnit(gc.getUnitClassInfo(cf.getHero(pPlayer)).getDefaultUnitIndex(), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_NORTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_SETTLE, DirectionTypes.DIRECTION_NORTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_SETTLE, DirectionTypes.DIRECTION_NORTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LONGBOWMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_NORTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_TAR_DEMON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_NORTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_VEIL'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_NORTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ADEPT'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_NORTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WORKER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_NORTH)
						gc.getTeam(pPlayer.getTeam()).makePeace(gc.getBARBARIAN_TEAM())

			iCount = 0
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive():
					if pPlayer.isHuman():
						iCount += 1
						pHumanPlayer = pPlayer
					if not pPlayer.getCivilizationType() in [ gc.getInfoTypeForString('CIVILIZATION_INFERNAL'), gc.getInfoTypeForString('CIVILIZATION_BARBARIAN')]:
						pNewPlot = listInvaderStart.pop(CyGame().getSorenRandNum(len(listInvaderStart), "Invader Start"))
						pNewPlot.setBonusType(-1)
						pNewPlot.setImprovementType(-1)
						pPlayer.setStartingPlot(pNewPlot, True)
						for iUnit in xrange(pNewPlot.getNumUnits()):
							pUnit = pPlot.getUnit(iUnit)
							pUnit.jumpToNearestValidPlot()

						for iPlotIndex in xrange(CyMap().numPlots()):
							pLoopPlot = CyMap().plotByIndex(iPlotIndex)
							iTeam = pPlayer.getTeam()
							if pLoopPlot.isRevealed (iTeam, False):
								pLoopPlot.setRevealed(iTeam, False, False, iTeam)
								pLoopPlot.updateVisibility()

						iBalor = gc.getInfoTypeForString('UNIT_BALOR')
						for pLoopUnit in PyPlayer(iPlayer).getUnitList():
							pLoopUnit.setXY(pNewPlot.getX(), pNewPlot.getY(), True, True, False)
							if pLoopUnit.getUnitType() == iBalor:
								pLoopUnit.jumpToNearestValidPlot()


			if iCount == 1:
				iLeader = pHumanPlayer.getLeaderType()
				if iLeader == gc.getInfoTypeForString('LEADER_EINION'):
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_INTRO_EINION",()), 'art/interface/popups/Lord of the Balors.dds')
				elif iLeader == gc.getInfoTypeForString('LEADER_BASIUM'):
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_INTRO_BASIUM",()), 'art/interface/popups/Lord of the Balors.dds')
				elif iLeader == gc.getInfoTypeForString('LEADER_CAPRIA'):
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_INTRO_CAPRIA",()), 'art/interface/popups/Lord of the Balors.dds')
				elif iLeader == gc.getInfoTypeForString('LEADER_KEELYN'):
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_INTRO_KEELYN",()), 'art/interface/popups/Lord of the Balors.dds')
				elif iLeader == gc.getInfoTypeForString('LEADER_VARN'):
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_INTRO_VARN",()), 'art/interface/popups/Lord of the Balors.dds')


			iBarrow = gc.getInfoTypeForString('IMPROVEMENT_BARROW')
			iDungeon = gc.getInfoTypeForString('IMPROVEMENT_DUNGEON')
			iNecrototem = gc.getInfoTypeForString('IMPROVEMENT_NECROTOTEM')
			iHellfire = gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE')
			iTower = gc.getInfoTypeForString('IMPROVEMENT_TOWER')
			iPit = gc.getInfoTypeForString('IMPROVEMENT_PIT')

			iScout = gc.getInfoTypeForString('UNIT_SCOUT')
			iSkeleton = gc.getInfoTypeForString('UNIT_SKELETON')
			iWarrior = gc.getInfoTypeForString('UNIT_WARRIOR')
			iSpectre = gc.getInfoTypeForString('UNIT_SPECTRE')
			iImp = gc.getInfoTypeForString('UNIT_IMP')
			iBalor = gc.getInfoTypeForString('UNIT_BALOR')
			iPitBeast = gc.getInfoTypeForString('UNIT_PIT_BEAST')
			iHound = gc.getInfoTypeForString('UNIT_HELLHOUND')

			iDemon = gc.getInfoTypeForString('PROMOTION_DEMON')

			bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
			for i in xrange (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if not pPlot.isNone():
					if pPlot.getPlotCounter() > 0:
						if not (pPlot.isWater() or pPlot.isPeak() or pPlot.isImpassable() or pPlot.isOwned()):
							iImprovement = pPlot.getImprovementType()
							if iImprovement == -1:
								if pPlot.getY() > 10 and gc.getGame().getSorenRandNum(10000, "Necrototem") < 90:
									pPlot.setImprovementType(iNecrototem)
								elif pPlot.getY() > 18 and gc.getGame().getSorenRandNum(10000, "Hellfire") < 90:
									pPlot.setImprovementType(iHellfire)
								elif gc.getGame().getSorenRandNum(10000, "Pit") < 90:
									pPlot.setImprovementType(iPit)
							elif iImprovement == iHellfire:
								bPlayer.initUnit(iBalor, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								bPlayer.initUnit(iImp, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							elif iImprovement == iBarrow:
								bPlayer.initUnit(iSkeleton, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							elif iImprovement == iDungeon:
								newUnit = bPlayer.initUnit(iWarrior, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.setHasPromotion(iDemon, True)
							elif iImprovement == iTower:
								newUnit = bPlayer.initUnit(iScout, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.setHasPromotion(iDemon, True)
							elif iImprovement == iPit:
								bPlayer.initUnit(iHound, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								bPlayer.initUnit(iPitBeast, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

			if CyGame().isHasTrophy("TROPHY_WB_BARBARIAN_ASSAULT"):
				gc.getGame().setOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS, True)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_INTRO",()), 'art/interface/popups/Mulcarn Reborn.dds')
			if CyGame().getTrophyValue("TROPHY_WB_CIV_AMELANCHIER") != gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
				gc.getPlayer(5).setAlive(False)
			if CyGame().getTrophyValue("TROPHY_WB_CIV_VOLANNA") != gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
				gc.getPlayer(6).setAlive(False)

			iXP = gc.getGame().getTrophyValue("TROPHY_WB_LUCIAN_XP")
			if iXP > 0:
				iPlayer = 4 #Mahala
				self.giftHeroXP(iPlayer, gc.getInfoTypeForString('UNIT_LUCIAN'), iXP)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_RETURN_OF_WINTER):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_INTRO",()), 'art/interface/popups/Return of Winter.dds')

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_BLACK_TOWER_INTRO",()), 'art/interface/popups/The Black Tower.dds')


			if CyGame().isHasTrophy("TROPHY_WB_BARBARIAN_ASSAULT"):
				gc.getPlayer(6).setAlive(False)
			if CyGame().isHasTrophy("TROPHY_WB_LORD_OF_THE_BALORS"):
				gc.getPlayer(5).setAlive(False)

			iHandicap = gc.getGame().getHandicapType()
			if iHandicap > 3:
				for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if pLoopPlayer.isAlive():
						if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
							pCity = pLoopPlayer.getCapitalCity()
							pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
							if iHandicap > 4:
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_WORKER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_WORKER, DirectionTypes.DIRECTION_SOUTH)
								if iHandicap > 5:
									pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_PYRE_ZOMBIE'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
									if iHandicap > 6:
										pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
										if iHandicap > 7:
											pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_SETTLE, DirectionTypes.DIRECTION_SOUTH)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_CULT):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_CULT_INTRO",()), 'art/interface/popups/The Cult.dds')

			iMushroom = gc.getInfoTypeForString('BONUS_MUSHROOMS')
			iGoodyHut = gc.getInfoTypeForString('IMPROVEMENT_GOODY_HUT')

			for iX in xrange(36, CyMap().getGridWidth()):
				for iY in xrange(CyMap().getGridHeight()):
					if pPlot.getBonusType(-1) != -1:
						pPlot.setBonusType(iMushroom)
					if pPlot.getImprovementType() == iGoodyHut:
						pPlot.setImprovementType(-1)


			bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
			if not CyGame().isHasTrophy("TROPHY_WB_BARBARIAN_ASSAULT"):
				newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_OGRE'), 40, 8, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), True)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS'), True)
				newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_OGRE'), 40, 8, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), True)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS'), True)
			if not CyGame().isHasTrophy("TROPHY_WB_LORD_OF_THE_BALORS"):
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_BALOR'), 43, 28, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_BALOR'), 43, 28, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			iXP = gc.getGame().getTrophyValue("TROPHY_WB_LUCIAN_XP")
			if iXP > 0:

				iPlayer = 1 #Mahala
				self.giftHeroXP(iPlayer, gc.getInfoTypeForString('UNIT_LUCIAN'), iXP)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_INTRO",()), 'art/interface/popups/The Momus.dds')

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_INTRO",()), 'art/interface/popups/The Radiant Guard.dds')

			iPlayer = 0 #Falamar
			pPlayer = gc.getPlayer(iPlayer)
			iHandicap = gc.getGame().getHandicapType()
			if iHandicap < 5:
				pPlot = CyMap().plot(16,7)
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RADIANT_GUARD'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)
				if iHandicap < 4:
					pPlot = CyMap().plot(16,23)
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RADIANT_GUARD'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)
					if iHandicap < 3:
						pPlot = CyMap().plot(18,16)
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RADIANT_GUARD'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)
						if iHandicap < 2:
							pPlot = CyMap().plot(16,9)
							pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RATHA'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
							if iHandicap < 1:
								pPlot = CyMap().plot(16,29)
								pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RATHA'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_SPLINTERED_COURT_INTRO",()), 'art/interface/popups/The Splintered Court.dds')

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_WAGES_OF_SIN):
			iCount = 0
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive():
					if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
						iTeam = pPlayer.getTeam()
						eTeam = gc.getTeam(iTeam)
						eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), 1)

					if pPlayer.isHuman():
						iCount += 1
						pHumanPlayer = pPlayer
			if iCount == 1:
				iCiv = pHumanPlayer.getCivilizationType()
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
					szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_INTRO_MALAKIM",())
				elif iCiv == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
					szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_INTRO_ELOHIM",())
				elif iCiv == gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
					szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_INTRO_MERCURIANS",())
				elif iCiv == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
					szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_INTRO_LJOSALFAR",())

				elif iCiv == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
					szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_INTRO_SHEAIM",())
				elif iCiv == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
					szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_INTRO_INFERNAL",())
				elif iCiv == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
					szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_INTRO_SVARTALFAR",())
				elif iCiv == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
					szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_INTRO_CALABIM",())
				self.addPopupWB(szText, 'art/interface/popups/Wages of Sin.dds')

	def getGoalTag(self, pPlayer):
		szBuffer = u"<font=2>"
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_WALL):
			if gc.getGame().getScenarioCounter() == 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_AGAINST_THE_WALL_GOAL_1", (), gc.getInfoTypeForString("COLOR_RED"))
			else:
				iCount = 100 - gc.getGame().getScenarioCounter()
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_AGAINST_THE_WALL_GOAL_2", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT):
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_BARBARIAN_ASSAULT_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_BENEATH_THE_HEEL_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BLOOD_OF_ANGELS):
			if gc.getGame().getScenarioCounter() == 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_BLOOD_OF_ANGELS_GOAL_1", (), gc.getInfoTypeForString("COLOR_RED"))
			else:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_BLOOD_OF_ANGELS_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			if gc.getGame().getScenarioCounter() == 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_FALL_OF_CUANTINE_GOAL_0", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 1:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_FALL_OF_CUANTINE_GOAL_1", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 2:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_FALL_OF_CUANTINE_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 3:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_FALL_OF_CUANTINE_GOAL_3", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 4:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_FALL_OF_CUANTINE_GOAL_4", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 5:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_FALL_OF_CUANTINE_GOAL_5", (), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GIFT_OF_KYLORIN_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):

			iPlayer = 0 #Falamar
			pPlayer = gc.getPlayer(iPlayer)
			pCity = pPlayer.getCapitalCity()

			if not pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_CARNIVAL')) > 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL_CARNIVAL", (), gc.getInfoTypeForString("COLOR_RED"))

			else:
				iSubdueAnimal = gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL')
				bHunter = False
				(pLoopUnit, iter) = pPlayer.firstUnit(False)
				while(pLoopUnit):
					if not pLoopUnit.isDead(): #is the unit alive and valid?
						if pLoopUnit.isHasPromotion(iSubdueAnimal):
							bHunter = True
							break
					(pLoopUnit, iter) = pPlayer.nextUnit(iter, False)

				if not bHunter:
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL_HUNTER", (), gc.getInfoTypeForString("COLOR_RED"))
				else:
					pCity = gc.getPlayer(iPlayer).getCapitalCity()
					iCount = 10

					bLion = True
					bWolf = True
					bTiger = True
					bPanther = True
					bBear = True
					bBaboon = True
					bGorilla = True
					bElephant = True
					bGriffon = True
					bSpider = True
					bScorpion = True
					bGiant = True
					bBird = True
					bTortoise = True
					bSeaSerpent = True

					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_SEA_SERPENT_TANK')) > 0:
						iCount -= 1
						bTortoise = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TORTOISE_TANK')) > 0:
						iCount -= 1
						bTortoise = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_AVIARY')) > 0:
						iCount -= 1
						bBird = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_GIANT_CAGE')) > 0:
						iCount -= 1
						bGiant = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_LION_CAGE')) > 0:
						iCount -= 1
						bLion = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_WOLF_PEN')) > 0:
						iCount -= 1
						bWolf = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TIGER_CAGE')) > 0:
						iCount -= 1
						bTiger = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_PANTHER_CAGE')) > 0:
						iCount -= 1
						bPanther = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_DANCING_BEAR')) > 0:
						iCount -= 1
						bBear = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_BABOON_CAGE')) > 0:
						iCount -= 1
						bBaboon = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_GORILLA_CAGE')) > 0:
						iCount -= 1
						bGorilla = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_ELEPHANT_PEN')) > 0:
						iCount -= 1
						bElephant = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_GRIFFON_CAGE')) > 0:
						iCount -= 1
						bGriffon = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_SPIDER_PEN')) > 0:
						iCount -= 1
						bSpider = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_SCORPION_PEN')) > 0:
						iCount -= 1
						bScorpion = False

					if iCount < 1:
						szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL_BUILD_MENAGERIE", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))
					else:
						szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))


		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			pPlayer = gc.getPlayer(0)
			if pPlayer.isHuman():
				if gc.getGame().getScenarioCounter() == 0:
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_GOAL_0", (), gc.getInfoTypeForString("COLOR_RED"))
				if gc.getGame().getScenarioCounter() > 100:
					iCount = gc.getGame().getScenarioCounter() - 100
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_GOAL_1", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))
				if gc.getGame().getScenarioCounter() == 99:
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))
			else:
				if gc.getGame().getScenarioCounter() == 0:
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_GOAL_0", (), gc.getInfoTypeForString("COLOR_RED"))
				if gc.getGame().getScenarioCounter() > 1:
					iCount = gc.getGame().getScenarioCounter()
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_GOAL_1", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))
				if gc.getGame().getScenarioCounter() == 1:
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			iCount = 0
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive():
					if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
						if pPlayer.getUnitClassCount(cf.getHero(pPlayer)) > 0:
							iCount += 1

			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_LORD_OF_THE_BALORS_GOAL", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_RETURN_OF_WINTER):
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_RETURN_OF_WINTER_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			bSanctuary = False
			if gc.getPlayer(2).isAlive():
				bSanctuary = True
			if gc.getPlayer(3).isAlive():
				bSanctuary = True
			if gc.getPlayer(4).isAlive():
				bSanctuary = True
			if bSanctuary:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_BLACK_TOWER_GOAL_1", (), gc.getInfoTypeForString("COLOR_RED"))
			else:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_BLACK_TOWER_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_CULT):
			if gc.getGame().getScenarioCounter() == 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_CULT_GOAL_1", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 1:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_CULT_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 2:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_CULT_GOAL_3", (), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_MOMUS_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_SPLINTERED_COURT_LJOSALFAR_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))
			elif pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_SPLINTERED_COURT_SVARTALFAR_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_DAWN", (), gc.getInfoTypeForString("COLOR_RED"))
			elif gc.getGame().getScenarioCounter() == 1:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_MORNING", (), gc.getInfoTypeForString("COLOR_RED"))
			elif gc.getGame().getScenarioCounter() == 2:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_NOON", (), gc.getInfoTypeForString("COLOR_RED"))
			elif gc.getGame().getScenarioCounter() == 3:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_AFTERNOON", (), gc.getInfoTypeForString("COLOR_RED"))
			elif gc.getGame().getScenarioCounter() == 4:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_DUSK", (), gc.getInfoTypeForString("COLOR_RED"))
			elif gc.getGame().getScenarioCounter() == 5:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_EARLY_NIGHT", (), gc.getInfoTypeForString("COLOR_RED"))
			elif gc.getGame().getScenarioCounter() == 6:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_MIDNIGHT", (), gc.getInfoTypeForString("COLOR_RED"))
			elif gc.getGame().getScenarioCounter() == 7:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_LATE_NIGHT", (), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			if gc.getGame().getScenarioCounter() > 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_RADIANT_GUARD_GOAL", ((gc.getGame().getScenarioCounter(), )), gc.getInfoTypeForString("COLOR_RED"))
			else:
				if gc.getTeam(0).isAtWar(1):
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_RADIANT_GUARD_GOAL_DEFEAT_BASIUM", (), gc.getInfoTypeForString("COLOR_RED"))
				if gc.getTeam(0).isAtWar(2):
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_RADIANT_GUARD_GOAL_DEFEAT_HYBOREM", (), gc.getInfoTypeForString("COLOR_RED"))

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_WAGES_OF_SIN):
			iCount = 0
			if pPlayer.getCivilizationType() in [gc.getInfoTypeForString('CIVILIZATION_ELOHIM'), gc.getInfoTypeForString('CIVILIZATION_MALAKIM'), gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'), gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR')]:
				for iPlayer in xrange(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.isAlive():
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
							iCount += 1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
							iCount += 1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
							iCount += 1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
							iCount += 1
			if pPlayer.getCivilizationType() in [gc.getInfoTypeForString('CIVILIZATION_SHEAIM'), gc.getInfoTypeForString('CIVILIZATION_CALABIM'), gc.getInfoTypeForString('CIVILIZATION_INFERNAL'), gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')]:
				for iPlayer in xrange(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.isAlive():
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
							iCount += 1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
							iCount += 1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
							iCount += 1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
							iCount += 1
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_WAGES_OF_SIN_GOAL", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))

		szBuffer = szBuffer + "</font>"
		return szBuffer

	def getHeroXP(self, iPlayer, iUnit):
		iXP = -1
		pPlayer = gc.getPlayer(iPlayer)
		for pLoopUnit in PyPlayer(iPlayer).getUnitList():
			if pLoopUnit.getUnitType() == iUnit:
				if pLoopUnit.getExperience() > iXP:
					iXP = pLoopUnit.getExperience()
		return iXP

	def giftHeroXP(self, iPlayer, iUnit, iXP):
		pPlayer = gc.getPlayer(iPlayer)
		(pLoopUnit, iter) = pPlayer.firstUnit(False)
		while(pLoopUnit):
			if not pLoopUnit.isDead(): #is the unit alive and valid?
				if pLoopUnit.getUnitType() == iUnit:
					if pLoopUnit.getExperience() > iXP:
						pLoopUnit.changeExperience(iXP, -1, False, False, False)
						break
			(pLoopUnit, iter) = pPlayer.nextUnit(iter, False)

	def onCityAcquired(self, iPreviousOwner, iNewOwner, pCity, bConquest, bTrade):
		pPlayer = gc.getPlayer(iNewOwner)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT):
			if pPlayer.isHuman():
				if gc.getPlayer(iPreviousOwner).getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS'):
					iUnit = gc.getInfoTypeForString('UNIT_GURID')
					if CyGame().getUnitCreatedCount(iUnit) == 0:
						cf.addUnit(iUnit)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			if pPlayer.getTeam() == 0:
				if pCity.at(47,28):#Tebryn's Capital
					gc.getGame().setWinner(0, 2)


		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BLOOD_OF_ANGELS):
			if pPlayer.getTeam() == 0:
				if pCity.getName() == "Torrolerial":
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_TORROLERIAL",()), 'art/interface/popups/Blood of Angels Torrolerial.dds')
					gc.getGame().changeScenarioCounter(1)
					gc.getTeam(0).setPermanentWarPeace(2, False)
					gc.getTeam(0).setPermanentWarPeace(3, False)
					eTeam = gc.getTeam(0) #Doviello & Illians
					eTeam.meet(2, False)
					eTeam.meet(3, False)
					eTeam.declareWar(2, False, WarPlanTypes.WARPLAN_TOTAL)
					eTeam.declareWar(3, False, WarPlanTypes.WARPLAN_TOTAL)
					gc.getTeam(0).setPermanentWarPeace(2, True)
					gc.getTeam(0).setPermanentWarPeace(3, True)
				if pCity.getName() == "Midgar":
					gc.getGame().setWinner(0, 2)
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_VICTORY",()), 'art/interface/popups/Blood of Angels Victory.dds')


		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			if pPlayer.isHuman():
				iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_THE_BLACK_TOWER_PICK_CIV')
				triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCity.getX(), pCity.getY(), iNewOwner, pCity.getID(), -1, -1, -1, -1)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			if pPlayer.isHuman():
				if pCity.getName() == "Bastradam":
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_CAPRIA_WON",()),'art/interface/popups/Capria.dds')
					gc.getGame().changeTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_CAPRIA_ALLY", 1)
					pPlayer = gc.getPlayer(0) #Falamar
					iX = pCity.getX()
					iY = pCity.getY()
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KNIGHT'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LONGBOWMAN'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LONGBOWMAN'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_ORDER'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_ORDER'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_ORDER'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CRUSADER'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CRUSADER'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PALADIN'), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					gc.getPlayer(3).setAlive(False) #Capria
					
					CyMap().plot(29, 2).setMoveDisabledAI(False)
					CyMap().plot(29, 2).setMoveDisabledHuman(False)


		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			if gc.getPlayer(iPreviousOwner).getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				cf.removeReligion(gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'), pCity)





	def onCityBuilt(self, pCity):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			if pPlayer.isHuman():
				iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_THE_BLACK_TOWER_PICK_CIV')
				triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCity.getX(), pCity.getY(), iPlayer, pCity.getID(), -1, -1, -1, -1)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			pCity.setPopulation(3)
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_BARBARIAN'):
				if pCity.getX() > 51 or pCity.getY() > 33:
					pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_INFERNAL'))
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DEMONIC_CITIZENS'), 1)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL'), 1)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MAGE_GUILD'), 1)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ELDER_COUNCIL'), 1)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TRAINING_YARD'), 1)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARCHERY_RANGE'), 1)

	def onCityRazed(self, city, iPlayer):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			if city.isHolyCityByType(gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS')):
				if gc.getGame().getScenarioCounter() == 4:
					gc.getGame().changeScenarioCounter(1)
				cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_MASK",()), iPlayer)
				bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
				newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_DROWN'), 15, 17, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)
				newUnit2 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_DROWN'), 15, 19, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)

				pPlayer = gc.getPlayer(0) #Decius
				(pLoopUnit, iter) = pPlayer.firstUnit(False)
				while(pLoopUnit):
					if not pLoopUnit.isDead(): #is the unit alive and valid?
						if pLoopUnit.getUnitType() == gc.getInfoTypeForString('UNIT_ROSIER_OATHTAKER'):
							pLoopUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER_WALKING'), True)
							break
					(pLoopUnit, iter) = pPlayer.nextUnit(iter, False)


		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			iPlayer = 1 #Decius (in the Calabim version)
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isHuman():
				if city.getName() == "Dirage":
					if gc.getGame().getScenarioCounter() == 0:
						gc.getGame().changeScenarioCounter(75)
						cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_DIRGE_RAZED",()), iPlayer)
						pCity = pPlayer.getCapitalCity()
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_NIGHTWATCH'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pPlayer = gc.getPlayer(0) #Varn
						pCity = pPlayer.getCapitalCity()
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_EMPYREAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						eTeam = gc.getTeam(pPlayer.getTeam())
						eTeam.setHasTech(gc.getInfoTypeForString('TECH_HONOR'), True, 0, True, False)
						# eTeam.signDefensivePact(gc.getTeam(2))
						# eTeam.signDefensivePact(gc.getTeam(3))
						# eTeam.signDefensivePact(gc.getTeam(5))
						eTeam.signDefensivePact(2)
						eTeam.signDefensivePact(3)
						eTeam.signDefensivePact(5)
						CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)

	def onImprovementDestroyed(self, iImprovement, iOwner, iX, iY):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			iPlayer = 0 #Decius
			if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BARROW'):
				if (iX == 19 and iY == 23):
					pPlayer = gc.getPlayer(iPlayer)
					pPlot = CyMap().plot(29,21)
					bValid = False
					for i in xrange(pPlot.getNumUnits(), -1, -1):
						pLoopUnit = pPlot.getUnit(i)
						if pLoopUnit.getUnitType() == gc.getInfoTypeForString('UNIT_CATAPULT'):
							bValid = True
							newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CATAPULT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							newUnit.convert(pLoopUnit)
							newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), False)
					if bValid:
						cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_CATAPULTS",()), iPlayer)

			if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_JUNGLE_ALTAR'):
				if (iX == 16 and iY == 1):
					cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_TWISTED_MEN",()), iOwner)
					if gc.getGame().getScenarioCounter() == 2:
						gc.getGame().changeScenarioCounter(1)

	def atRangeJungleAltar(self, pCaster, pPlot):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			if pCaster.isHuman():
				if gc.getGame().getScenarioCounter() == 1:
					if pPlot.at(16,1):
						pPlot.setPythonActive(False)
						iPlayer = 0 #Decius
						cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_MUIRIN",()), iPlayer)
						if gc.getGame().getScenarioCounter() == 1:
							gc.getGame().changeScenarioCounter(1)

	def onMoveJungleAltar(self, pCaster, pPlot):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			iPlayer = pCaster.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isHuman():
				if pPlot.at(34,12):
					cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_ALTAR",()), iPlayer)
					pPlot.setPythonActive(False)
				if pPlot.at(70,37):
					szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_ALTAR_TO_DIS",())
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
						szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_ALTAR_TO_DIS_KEELYN",())
					cf.addPlayerPopup(szText, iPlayer)
					pPlot.setPythonActive(False)

	def onMoveMirrorOfHeaven(self, pCaster, pPlot):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			if gc.getGame().getScenarioCounter() == 0:
				iPlayer = pCaster.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isHuman():
					if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
						gc.getGame().changeScenarioCounter(175)
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_MIRROR_OF_HEAVEN",()),'art/interface/popups/Varn.dds')
						pPlot = CyMap().plot(30,23)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_EMPYREAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						eTeam = gc.getTeam(1) #Flauros
						eTeam.declareWar(0, False, WarPlanTypes.WARPLAN_TOTAL)

	def onMovePortal(self, pCaster, pPlot):

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_CULT):
			iPlayer = pCaster.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			iX = pPlot.getPortalExitX()
			iY = pPlot.getPortalExitY()
			if not (iX == 0 and iY ==0):
				pExitPlot = CyMap().plot(iX,iY)
				if not pExitPlot.isNone():
					pCaster.setXY(iX, iY, False, True, True)


			if pPlayer.isHuman():
				if pPlot.at(21,15):
					if gc.getGame().getScenarioCounter() == 0:
						gc.getGame().changeScenarioCounter(1)
						CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
						for iY in xrange(18, 31, 1):
							pPlot = CyMap().plot(21,iY)
							pPlot.setMoveDisabledAI(False)
				if pPlot.at(42,30):
					if gc.getGame().getScenarioCounter() == 1:

						pPlot = CyMap().plot(21,16)
						pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_DOOR_NORTH_OPEN'), 0)

						pPlot.setPythonActive(False)
						pPlot = CyMap().plot(21,15)
						pPlot.setPythonActive(False)

						pPlot = CyMap().plot(21,15)#South door now skips dungeon
						pPlot.setPortalExitX(0)
						pPlot.setPortalExitY(0)
						pPlot = CyMap().plot(21,16)#North door now skips dungeon
						pPlot.setPortalExitX(0)
						pPlot.setPortalExitY(0)

						gc.getGame().changeScenarioCounter(1)
						CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)

						iDragon =gc.getInfoTypeForString('UNIT_EURABATRES')
						pPlayer = gc.getPlayer(3) #Cardith
						if CyGame().getUnitCreatedCount(iDragon) == 0:
							pPlayer.initUnit(iDragon, 8,28, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						iDragon =gc.getInfoTypeForString('UNIT_ABASHI')
						pPlayer = gc.getPlayer(4) #Os-Gabella
						if CyGame().getUnitCreatedCount(iDragon) == 0:
							pPlayer.initUnit(iDragon, 29,26, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
						iDragon =gc.getInfoTypeForString('UNIT_THALATTH')
						if CyGame().getUnitCreatedCount(iDragon) == 0:
							bPlayer.initUnit(iDragon, 13, 29, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						iDragon =gc.getInfoTypeForString('UNIT_ACHERON')
						py = PyPlayer(50)#Barbarian
						iDragon =gc.getInfoTypeForString('UNIT_THALATTH')
						if CyGame().getUnitCreatedCount(iDragon) == 0:
							bPlayer.initUnit(iDragon, 13, 29, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)


	def onMoveWarningPost(self, pCaster, pPlot):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			iPlayer = pCaster.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
			if pPlayer.isHuman():
				iHeld = gc.getInfoTypeForString('PROMOTION_HELD')
				if pPlot.at(4,14):
					if not (pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_AIR')) or pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR2'))):
						pCaster.setXY(4, 13, False, True, True)
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_WARD_AIR",()),'art/interface/popups/Dain.dds')
					else:
						iManes = gc.getInfoTypeForString('UNIT_MANES')
						for pLoopUnit in PyPlayer(gc.getBARBARIAN_PLAYER()).getUnitList():
							if pLoopUnit.getUnitType() == iManes:
								pLoopUnit.setHasPromotion(iHeld, False)

				if pPlot.at(16,11):
					if not (pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE')) or pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE2'))):
						pCaster.setXY(17, 11, False, True, True)
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_WARD_FIRE",()),'art/interface/popups/Dain.dds')
					else:
						iPyreZombie = gc.getInfoTypeForString('UNIT_PYRE_ZOMBIE')
						iSpectre = gc.getInfoTypeForString('UNIT_SPECTRE')

						for pUnit in PyPlayer(gc.getBARBARIAN_PLAYER()).getUnitList():
							if pUnit.getUnitType() in [iPyreZombie, iSpectre]:
								pUnit.setHasPromotion(iHeld, False)

				if pPlot.at(23, 6):
					iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_GIFT_OF_KYLORIN_SECRET_DOOR')
					triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, 0, -1, -1, -1, -1, -1)
				if pPlot.at(8, 4):
					iWoodGolem = gc.getInfoTypeForString('UNIT_WOOD_GOLEM')
					for pUnit in PyPlayer(gc.getBARBARIAN_PLAYER()).getUnitList():
						if pUnit.getUnitType() == iWoodGolem:
							pUnit.setHasPromotion(iHeld, False)

					pPlot.setPythonActive(False)
				if pPlot.at(19,16):
					if pPlayer.isHuman():
						if pCaster.getUnitType() != gc.getInfoTypeForString('UNIT_WIZARD'):
							pCaster.kill(True, 0)
						else:
							iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_GIFT_OF_KYLORIN_MESHABBER')
							triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, 0, -1, -1, -1, -1, -1)
				if pPlot.at(28,1):
					if pPlayer.isHuman():
						if pCaster.getUnitType() == gc.getInfoTypeForString('UNIT_WIZARD'):
							cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_POTION_OF_INVISIBILITY",()),'art/interface/popups/Dain.dds')
							pPlot = CyMap().plot(27,1)
							pUnit = pPlot.getUnit(0)
							pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_INVISIBLE'), True)
							pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POTION_OF_INVISIBILITY'), True)

				if pPlot.at(37,15):
					if not (pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_METAMAGIC')) or pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC2'))):
						pCaster.setXY(37, 14, False, True, True)
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_WARD_METAMAGIC",()),'art/interface/popups/Dain.dds')
					else:

						iGolem = gc.getInfoTypeForString('UNIT_NULLSTONE_GOLEM')
						for pUnit in PyPlayer(gc.getBARBARIAN_PLAYER()).getUnitList():
							if pUnit.getUnitType() == iGolem:
								pUnit.setHasPromotion(iHeld, False)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			iPlayer = pCaster.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isHuman():
				if pPlot.at(33,14):
					pPlot.setImprovementType(-1)
					CyEngine().addLandmark(pPlot, "The Conquerers' Pass")
					szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONQUERERS_PASS",())
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
						szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONQUERERS_PASS_KEELYN",())
					cf.addPlayerPopup(szText, iPlayer)

				if pPlot.at(50,12):
					pPlot.setImprovementType(-1)
					CyEngine().addLandmark(pPlot, "The Pass of Sorrows")
					szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_SORROWS_PASS",())
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
						szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_SORROWS_PASS_KEELYN",())
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_VARN'):
						szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_SORROWS_PASS_VARN",())
					cf.addPlayerPopup(szText, iPlayer)

				if pPlot.at(2, 16):
					pPlot.setImprovementType(-1)
					CyEngine().addLandmark(pPlot, "The Forgotten Pass")
					szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_FORGOTTEN_PASS",())
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
						szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_FORGOTTEN_PASS_KEELYN",())
					cf.addPlayerPopup(szText, iPlayer)

				if pPlot.at(29, 36):
					cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_FREE_CHAMPION",()), iPlayer)
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), 29, 38, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ADEPT'), 29, 38, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					newUnit.setDamage(90, PlayerTypes.NO_PLAYER)
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), 29, 38, UnitAITypes.UNITAI_RESERVE, DirectionTypes.DIRECTION_SOUTH)
					newUnit.setDamage(90, PlayerTypes.NO_PLAYER)
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SWORDSMAN'), 29, 38, UnitAITypes.UNITAI_RESERVE, DirectionTypes.DIRECTION_SOUTH)
					newUnit.setDamage(90, PlayerTypes.NO_PLAYER)
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CAPRIA'):
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DONAL'), 29, 38, UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setDamage(90, PlayerTypes.NO_PLAYER)
					else:
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ADVENTURER'), 29, 38, UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setDamage(90, PlayerTypes.NO_PLAYER)
					CyMap().plot(29,37).setFeatureType(-1, -1)
					CyMap().plot(29,38).setImprovementType(-1)
					pPlot.setPythonActive(False)

	def onReligionFounded(self, iReligion, iFounder):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			pPlayer = gc.getPlayer(iFounder)
			pCity = gc.getGame().getHolyCity(iReligion)
			if iReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RADIANT_GUARD'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RADIANT_GUARD'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RATHA'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_EMPYREAN'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_EMPYREAN'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIGHTBRINGER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_RELIGION_EMPYREAN", ())
				cf.addPlayerPopup(szText, iFounder)
			elif iReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_OCTOPUS_OVERLORDS'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_OVERLORDS'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_OVERLORDS'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DROWN'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_STYGIAN_GUARD'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_RELIGION_OVERLORDS", ())
				cf.addPlayerPopup(szText, iFounder)
			elif iReligion == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CRUSADER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CRUSADER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CRUSADER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_ORDER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_ORDER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_THE_ORDER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_RELIGION_ORDER", ())
				cf.addPlayerPopup(szText, iFounder)
			elif iReligion == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PARAMANDER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PARAMANDER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_KILMORPH'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_KILMORPH'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DWARVEN_SOLDIER_RUNES'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_RELIGION_RUNES", ())
				cf.addPlayerPopup(szText, iFounder)
			elif iReligion == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SATYR'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SATYR'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_FAWN'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_LEAVES'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_LEAVES'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_FELLOWSHIP_OF_LEAVES'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_RELIGION_LEAVES", ())
				cf.addPlayerPopup(szText, iFounder)

	def onTechAcquired(self, iTechType, iTeam, iPlayer, bAnnounce):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			if iTechType == gc.getInfoTypeForString('TECH_ORDERS_FROM_HEAVEN'):
				if iTeam == 0: #Decius's Team
					pPlayer = gc.getPlayer(0) #Decius
					pCity = pPlayer.getCapitalCity()
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ROSIER_OATHTAKER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COURAGE'), True)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			if gc.getTeam(iTeam).isHuman():
				if iTechType == gc.getInfoTypeForString('TECH_SMELTING'):
					if not gc.getGame().isHasTrophy("TROPHY_WB_SPLINTER_COURT_PARITH"):
						for iPlayer in xrange(gc.getMAX_PLAYERS()):
							pLoopPlayer = gc.getPlayer(iPlayer)
							if pLoopPlayer.getTeam() == iTeam:
								if pLoopPlayer.isHuman():
									iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_SPLINTERED_COURT_PARITH')
									triggerData = pLoopPlayer.initTriggeredData(iEvent, True, -1, -1, -1, -1, -1, -1, -1, -1, -1)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BLOOD_OF_ANGELS):
			if gc.getTeam(iTeam).isHuman():
				if iTechType == gc.getInfoTypeForString('TECH_FANATICISM'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_BRIGIT",()),'art/interface/popups/Brigit.dds')
					pPlayer = gc.getPlayer(iPlayer)
					iTeam = pPlayer.getTeam()
					pPlot = CyMap().plot(47,47)
					pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
				elif iTechType == gc.getInfoTypeForString('TECH_RAGE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_ODIO",()),'art/interface/popups/Mahon.dds')
					pPlayer = gc.getPlayer(iPlayer)
					iTeam = pPlayer.getTeam()
					pPlot = CyMap().plot(27,45)
					pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)

	def onUnitCreated(self, pUnit):
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iUnitType = pUnit.getUnitType()

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			if pUnit.isBarbarian():
				if pUnit.getRace() == gc.getInfoTypeForString('PROMOTION_ORC'):
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON'), True)
				elif pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'):
					if pUnit.plot().getPlotCounter() > 50:
						iUnit = cf.getUnholyVersion(pUnit)
						if iUnit == -1:
							pUnit.kill(True,iPlayer)
						else:
							newUnit = pPlayer.initUnit(iUnit, pUnit.getX(),pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							newUnit.convert(pUnit)

			elif pPlayer.getNumCities() < 1:
				if iUnitType == gc.getInfoTypeForString('UNIT_SETTLER'):
					iCiv = pPlayer.getCivilizationType()
					if iCiv == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
						pUnit.setReligion(gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'))
					elif iCiv == gc.getInfoTypeForString('CIVILIZATION_BANNOR'):
						pUnit.setReligion(gc.getInfoTypeForString('RELIGION_THE_ORDER'))
					elif iCiv == gc.getInfoTypeForString('CIVILIZATION_BALSERAPHS'):
						pUnit.setReligion(gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'))



		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			if iUnitType == gc.getInfoTypeForString('UNIT_WIZARD'):
				if pPlayer.isHuman():
					pUnit.setAvatarOfCivLeader(True)
					for iProm in xrange(gc.getNumPromotionInfos()):
						info = gc.getPromotionInfo(iProm)
						if pUnit.isHasPromotion(iProm):
							iBonus = info.getBonusPrereq()
							if iBonus != -1:
								if gc.getBonusInfo(iBonus).isMana():
									pUnit.setHasPromotion(iProm, False)
					pUnit.changeFreePromotionPick(-1)
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELLSTAFF'), True)
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEALING_SALVE'), True)

			elif iUnitType == gc.getInfoTypeForString('EQUIPMENT_TREASURE'):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_INVISIBLE'), False)



		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BLOOD_OF_ANGELS):

			if iUnitType == gc.getInfoTypeForString('UNIT_PONTIF'):
				pUnit.setReligion(gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'))

			if gc.getTeam(pUnit.getTeam()).isHuman():
				if iUnitType == gc.getInfoTypeForString('UNIT_ODIO'):
					pUnit.changeImmortal(1)
					pUnit.kill(True, pUnit.getOwner())
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_ODIO_VICTORY",()), 'art/interface/popups/Mahon.dds')
					gc.getGame().setWinner(0, 2)
				if iUnitType == gc.getInfoTypeForString('UNIT_BRIGIT'):
					pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))
					pUnit.changeImmortal(1)
					pUnit.kill(True, pUnit.getOwner())
					pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_BRIGIT_VICTORY",()), 'art/interface/popups/Brigit.dds')
					gc.getGame().setWinner(0, 2)




		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			if pUnit.isAlive():
				if pUnit.getReligion() ==-1:
					if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
						pUnit.setReligion(gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'))
					if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
						pUnit.setReligion(gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'))



		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
			if pPlayer.isHuman():
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BOUNTY_HUNTER'), True)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			if iUnitType == gc.getInfoTypeForString('UNIT_ROSIER_OATHTAKER'):
				pPlot = CyMap().plot(16,1)
				pPlot.setMoveDisabledHuman(False)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			if pPlayer.isHuman():
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT1'), True)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			if iUnitType == gc.getInfoTypeForString('UNIT_AURIC_ASCENDED'):
				for iPlayer in xrange(gc.getMAX_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iPlayer)
					if pLoopPlayer.isAlive():
						if pLoopPlayer.getTeam() != 0:
							gc.getPlayer(iPlayer).changeDisableProduction(1000)
				iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
				iGrass = gc.getInfoTypeForString('TERRAIN_GRASS')
				iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
				iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
				iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
				for i in xrange (CyMap().numPlots()):
					pPlot = CyMap().plotByIndex(i)
					if pPlot.getFeatureType() == -1:
						if pPlot.getImprovementType() == -1:
							if not pPlot.isWater():
								iTerrain = pPlot.getTerrainType()
								if iTerrain == iTundra:
									pPlot.setTerrainType(iSnow,True,True)
								elif iTerrain == iGrass:
									pPlot.setTerrainType(iTundra,True,True)
								elif iTerrain == iPlains:
									pPlot.setTerrainType(iTundra,True,True)
								elif iTerrain == iDesert:
									pPlot.setTerrainType(iPlains,True,True)
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_AURIC_ASCENDED",()),'art/interface/popups/Auric Ascended.dds')



		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
			if pUnit.isAlive():
				if not pUnit.isOnlyDefensive():
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MUTATED'), True)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				if pUnit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_ARCHER'):
					pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, 5, 13, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_WAGES_OF_SIN):
			if iUnitType == gc.getInfoTypeForString('UNIT_VALIN'):
				if gc.getGame().getUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_VALIN')) == 1:
					bGood = True
					for iPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								iCiv = pLoopPlayer.getCivilizationType()
								if iCiv == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_VALIN_CALABIM",())
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_VALIN_ELOHIM",())
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_VALIN_MALAKIM",())
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_VALIN_SHEAIM",())

								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_VALIN_ELOHIM",())
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_VALIN_LJOSALFAR",())
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_VALIN_SVARTALFAR",())
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_VALIN_INFERNAL",())
								cf.addPopup(szText,'art/interface/popups/Valin Phanuel.dds')

			if iUnitType == gc.getInfoTypeForString('UNIT_ROSIER'):
				if gc.getGame().getUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_ROSIER')) == 1:
					bGood = True
					for iPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								iCiv = pLoopPlayer.getCivilizationType()
								if iCiv == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_ROSIER_CALABIM",())
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_ROSIER_ELOHIM",())
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_ROSIER_MALAKIM",())
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_ROSIER_SHEAIM",())

								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_ROSIER_ELOHIM",())
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_ROSIER_LJOSALFAR",())
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_ROSIER_SVARTALFAR",())
								elif iCiv == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_ROSIER_SHEAIM",())
								cf.addPopup(szText,'art/interface/popups/Rosier the Fallen.dds')

	def onUnitKilled(self, pUnit, iAttacker):
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iUnitType = pUnit.getUnitType()

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			iRosier = gc.getInfoTypeForString('UNIT_ROSIER_OATHTAKER')
			if iUnitType == iRosier:
				if gc.getGame().getScenarioCounter() < 6:
					iPlayer = 0 #Decius
					cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_ROSIER_KILLED",()), iPlayer)
					gc.getPlayer(iPlayer).setAlive(False)
			if gc.getGame().getScenarioCounter() == 5:
				if iUnitType == gc.getInfoTypeForString('UNIT_DROWN'):
					unitID = pUnit.getID()
					bValid = True
					iX = 16
					iY = 18
					for iiX in xrange(iX-1, iX+2, 1):
						for iiY in xrange(iY-1, iY+2, 1):
							pPlot = CyMap().plot(iiX,iiY)
							for i in xrange(pPlot.getNumUnits()):
								pLoopUnit = pPlot.getUnit(i)
								if pLoopUnit.getUnitType() == gc.getInfoTypeForString('UNIT_DROWN'):
									if pLoopUnit.getID() != unitID:
										bValid = False
					if bValid:
						gc.getGame().changeScenarioCounter(1)
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_FALL_OF_CUANTINE_ROSIER')
						iPlayer = 0 #Decius
						pPlayer = gc.getPlayer(iPlayer)
						triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, 0, -1, -1, -1, -1, -1)
						for iUnit in xrange(pPlayer.getNumUnits()):
							pLoopUnit = pPlayer.getUnit(iUnit)
							if pLoopUnit.getUnitType() == iRosier:
								pLoopUnit.kill(True,0)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			if pUnit.getOwner() == gc.getBARBARIAN_PLAYER():
				iUnitClass = pUnit.getUnitClassType()
				iPlayer = 0 #Falamar
				szText = -1
				if gc.getGame().getUnitClassCreatedCount(iUnitClass) == 2:
					if iUnitClass == gc.getInfoTypeForString('UNITCLASS_BEAR'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_BEAR",())
					elif iUnitClass == gc.getInfoTypeForString('UNITCLASS_LION'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_LION",())
					elif iUnitClass == gc.getInfoTypeForString('UNITCLASS_WOLF'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_WOLF",())
				if gc.getGame().getUnitClassCreatedCount(iUnitClass) == 1:
					if iUnitClass == gc.getInfoTypeForString('UNITCLASS_ELEPHANT'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_ELEPHANT",())
					elif iUnitClass == gc.getInfoTypeForString('UNITCLASS_GORILLA'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_GORILLA",())
					elif iUnitClass == gc.getInfoTypeForString('UNITCLASS_GRIFFON'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_GRIFFON",())
					elif iUnitClass == gc.getInfoTypeForString('UNITCLASS_GIANT_SPIDER'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_SPIDER",())
					elif iUnitClass == gc.getInfoTypeForString('UNITCLASS_TIGER'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_TIGER",())

					elif iUnitClass == gc.getInfoTypeForString('UNITCLASS_PANTHER'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_PANTHER",())
					elif iUnitClass == gc.getInfoTypeForString('UNITCLASS_SCORPION'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_SCORPION",())
					elif iUnitClass == gc.getInfoTypeForString('UNITCLASS_BABOON'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_BABOON",())
					elif iUnitClass == gc.getInfoTypeForString('UNITCLASS_HAWK'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_HAWK",())
				if szText != -1:
					cf.addPlayerPopup(szText, iPlayer)


		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			if pUnit.isAlive() and not pUnit.isImmortal():
				iUnit = cf.getUnholyVersion(pUnit)
				if iUnit != -1:
					pPlayer = gc.getPlayer(1) #Tebryn
					pCity = pPlayer.getCapitalCity()
					if not pCity.atPlot(pUnit.plot()):
##					if pUnit.getX() != pCity.getX() or pUnit.getY() != pCity.getY():
						newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UNDEAD'), True)

						if gc.getTeam(pPlayer.getTeam()).isBuildingClassMaxedOut(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_NECROMANCY'),0):
							lMana = [	gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
									gc.getInfoTypeForString('BONUS_MANA_DEATH'),
									gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'),
									gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
									gc.getInfoTypeForString('BONUS_MANA_SHADOW')]

							for iMana in lMana:
								if pPlayer.getNumAvailableBonuses(iMana) > 0:
									pUnit.changeFreePromotionPick(1)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			pPlayer = gc.getPlayer(pUnit.getOwner())
			if gc.getGame().getScenarioCounter() == 0:
				if iUnitType == gc.getInfoTypeForString('UNIT_BASIUM'):
					if gc.getTeam(0).isAtWar(pPlayer.getTeam()):
						gc.getGame().setOption(GameOptionTypes.GAMEOPTION_COMPLETE_KILLS, False)
						gc.getPlayer(0).initCity(0,2)
						for iPlayer in xrange(gc.getMAX_PLAYERS()):
							if iPlayer != 0:
								pPlayer = gc.getPlayer(iPlayer)
								if pPlayer.isAlive():
									pPlayer.setAlive(False)
						gc.getGame().setWinner(0, 2) #Falamar wins
					else:
						gc.getGame().setWinner(2, 2) #Hyborem wins
				if iUnitType == gc.getInfoTypeForString('UNIT_HYBOREM'):
					if gc.getTeam(0).isAtWar(pPlayer.getTeam()):
						gc.getGame().setOption(GameOptionTypes.GAMEOPTION_COMPLETE_KILLS, False)
						gc.getPlayer(0).initCity(0,2)
						for iPlayer in xrange(gc.getMAX_PLAYERS()):
							if iPlayer != 0:
								pPlayer = gc.getPlayer(iPlayer)
								if pPlayer.isAlive():
									pPlayer.setAlive(False)
						gc.getGame().setWinner(0, 2) #Falamar wins
					else:
						gc.getGame().setWinner(1, 2) #Basium wins
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				if gc.getGame().getScenarioCounter() > 0:
					gc.getGame().changeScenarioCounter(-1)
					if gc.getGame().getScenarioCounter() == 0:
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_THE_RADIANT_GUARD_CHOOSE_SIDES')
						iPlayer = 0 #Falamar
						triggerData = gc.getPlayer(iPlayer).initTriggeredData(iEvent, True, -1, -1, -1, 0, -1, -1, -1, -1, -1)
						for i in xrange (CyMap().numPlots()):
							pPlot = CyMap().plotByIndex(i)
							if pPlot.getX() <= 9:
								pPlot.setMoveDisabledHuman(False)
						pPlayer = gc.getPlayer(1) #Basium
						pCity = pPlayer.getCapitalCity()
						iX = pCity.getX()
						iY = pCity.getY()
						iUnit = gc.getInfoTypeForString('UNIT_BASIUM')
						newUnit = pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)
						iUnit = gc.getInfoTypeForString('UNIT_ANGEL')
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						iUnit = gc.getInfoTypeForString('UNIT_SERAPH')
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						iUnit = gc.getInfoTypeForString('UNIT_OPHANIM')
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						iUnit = gc.getInfoTypeForString('UNIT_VALKYRIE')
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						iUnit = gc.getInfoTypeForString('UNIT_CHAMPION')
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlot = CyMap().plot(75,47)
						pPlot.setMoveDisabledHuman(False)
					CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)

###Qgqqqqq's request
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):# or pPlayer.isBarbarian():
				if pUnit.getRace() == gc.getInfoTypeForString('PROMOTION_DEMON'):
					if pUnit.getDuration() < 1:
						if not pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO')):
							iManes = gc.getInfoTypeForString('UNIT_MANES')
							if iUnitType != iManes:
								cf.giftUnitToPlayer(iManes, iPlayer, pUnit.getExperience(), pUnit.plot(), iPlayer, pUnit.getReligion())

		if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AURIC'):
			if pUnit.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_AURIC'):
				cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_AURIC_KILLED",()), iPlayer)
				pPlayer.setAlive(False)


	def onUnitLost(self, pUnit):
		'Unit Lost'
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_DECIUS'):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GREAT_GENERAL')):
				iDecius = gc.getInfoTypeForString('UNIT_DECIUS')
				if pUnit.getScenarioCounter() == iDecius:
					pCity = pPlayer.getCapitalCity()
					if not pCity.isNone():
						pPlayer.initUnit(iDecius, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			if pPlayer.isHuman():
				if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_WIZARD'):
					if not pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION')):
						pPlayer.setAlive(False)

	def onVictory(self, iPlayer, iVictory):
		pPlayer = gc.getPlayer(iPlayer)
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_GREY):
			gc.getGame().changeTrophyValue("TROPHY_WB_AGAINST_THE_GREY", 1)
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_AGAINST_THE_GREY_VICTORY_CALABIM",())
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_AGAINST_THE_GREY_VICTORY_MALAKIM",())
			self.addPopupWB(szText, 'art/interface/popups/Against the Grey.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_WALL):
			gc.getGame().changeTrophyValue("TROPHY_WB_AGAINST_THE_WALL", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_AGAINST_THE_WALL_VICTORY",()), 'art/interface/popups/Against the Wall Victory.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT):
			gc.getGame().changeTrophyValue("TROPHY_WB_BARBARIAN_ASSAULT", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_VICTORY",()), 'art/interface/popups/Barbarian Assault.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
			gc.getGame().changeTrophyValue("TROPHY_WB_BENEATH_THE_HEEL", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_VICTORY",()), 'art/interface/popups/Beneath the Heel.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BLOOD_OF_ANGELS):
			gc.getGame().changeTrophyValue("TROPHY_WB_BLOOD_OF_ANGELS", 1)
			iXP = self.getHeroXP(iPlayer, gc.getInfoTypeForString('UNIT_LUCIAN'))
			if iXP > gc.getGame().getTrophyValue("TROPHY_WB_LUCIAN_XP"):
				gc.getGame().setTrophyValue("TROPHY_WB_LUCIAN_XP", iXP)
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			gc.getGame().changeTrophyValue("TROPHY_WB_FALL_OF_CUANTINE", 1)
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			gc.getGame().changeTrophyValue("TROPHY_WB_GIFT_OF_KYLORIN", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_VICTORY",()), 'art/interface/popups/Gift of Kylorin.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			gc.getGame().changeTrophyValue("TROPHY_WB_GRAND_MENAGERIE", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_VICTORY",()), 'art/interface/popups/Grand Menagerie Victory.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			gc.getGame().changeTrophyValue("TROPHY_WB_INTO_THE_DESERT", 1)
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_VICTORY",()), 'art/interface/popups/Into the Desert.dds')
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_VICTORY",()), 'art/interface/popups/Into the Desert Calabim.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			gc.getGame().changeTrophyValue("TROPHY_WB_LORD_OF_THE_BALORS", 1)
			if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_EINION'):
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONCLUSION_EINION",())

			if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BASIUM'):
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONCLUSION_BASIUM",())
			if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CAPRIA'):
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONCLUSION_CAPRIA",())
			if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONCLUSION_KEELYN",())
			if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_VARN'):
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONCLUSION_VARN",())
			self.addPopupWB(szText, 'art/interface/popups/Lord of the Balors Victory.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			gc.getGame().changeTrophyValue("TROPHY_WB_MULCARN_REBORN", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_VICTORY",()), 'art/interface/popups/Mulcarn Reborn Victory.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_RETURN_OF_WINTER):
			gc.getGame().changeTrophyValue("TROPHY_WB_RETURN_OF_WINTER", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_VICTORY",()), 'art/interface/popups/Return of Winter Victory.dds')
			iXP = self.getHeroXP(iPlayer, gc.getInfoTypeForString('UNIT_LUCIAN'))
			if iXP > gc.getGame().getTrophyValue("TROPHY_WB_LUCIAN_XP"):
				gc.getGame().setTrophyValue("TROPHY_WB_LUCIAN_XP", iXP)
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			gc.getGame().changeTrophyValue("TROPHY_WB_THE_BLACK_TOWER", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_BLACK_TOWER_VICTORY",()), 'art/interface/popups/The Black Tower Victory.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_CULT):
			gc.getGame().changeTrophyValue("TROPHY_WB_THE_CULT", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_CULT_VICTORY",()), 'art/interface/popups/The Cult.dds')
			iXP = self.getHeroXP(iPlayer, gc.getInfoTypeForString('UNIT_LUCIAN'))
			if iXP > gc.getGame().getTrophyValue("TROPHY_WB_LUCIAN_XP"):
				gc.getGame().setTrophyValue("TROPHY_WB_LUCIAN_XP", iXP)
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
			gc.getGame().changeTrophyValue("TROPHY_WB_THE_MOMUS", 1)
			szText = CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_VICTORY_PERPENTACH",())
			if CyGame().isHasTrophy("TROPHY_WB_THE_MOMUS_BEERI_ALLY"):
				szText = CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_VICTORY_BEERI",())
			self.addPopupWB(szText, 'art/interface/popups/The Momus Victory.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			gc.getGame().changeTrophyValue("TROPHY_WB_THE_SPLINTERED_COURT", 1)
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				gc.getGame().setTrophyValue("TROPHY_WB_THE_SPLINTERED_COURT_LJOSALFAR", 1)
				gc.getGame().setTrophyValue("TROPHY_WB_THE_SPLINTERED_COURT_SVARTALFAR", 0)
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_SPLINTERED_COURT_VICTORY_LJOSALFAR",()), 'art/interface/popups/The Splintered Court Ljosalfar Victory.dds')
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				gc.getGame().setTrophyValue("TROPHY_WB_THE_SPLINTERED_COURT_LJOSALFAR", 0)
				gc.getGame().setTrophyValue("TROPHY_WB_THE_SPLINTERED_COURT_SVARTALFAR", 1)
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_SPLINTERED_COURT_VICTORY_SVARTALFAR",()), 'art/interface/popups/The Splintered Court Svartalfar Victory.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			gc.getGame().changeTrophyValue("TROPHY_WB_THE_RADIANT_GUARD", 1)
			szText = CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_VICTORY_BASIUM",())
			if CyGame().isHasTrophy("TROPHY_WB_THE_RADIANT_GUARD_HYBOREM_ALLY"):
				szText = CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_VICTORY_HYBOREM",())
			self.addPopupWB(szText, 'art/interface/popups/The Radiant Guard.dds')
		elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_WAGES_OF_SIN):
			gc.getGame().changeTrophyValue("TROPHY_WB_WAGES_OF_SIN", 1)
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_CONCLUSION_ELOHIM",())
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_CONCLUSION_MALAKIM",())

			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
				szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_CONCLUSION_MERCURIANS",())
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_CONCLUSION_LJOSALFAR",())

			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_CONCLUSION_SVARTALFAR",())
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_CONCLUSION_INFERNAL",())


			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_CONCLUSION_CALABIM",())
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_CONCLUSION_SHEAIM",())
			self.addPopupWB(szText, 'art/interface/popups/Wages of Sin Victory.dds')

	def openChest(self, caster, pPlot):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			if caster.getUnitType() != gc.getInfoTypeForString('UNIT_WIZARD'):
				if caster.getOwner() == 0:
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_LOCKED",()),'art/interface/popups/Dain.dds')
				return False

			if pPlot.at(17,4):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_MAELSTROM",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_AIR'), True)
				gc.getGame().changeScenarioCounter(1)

			if pPlot.at(28, 17):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_HASTE",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_BODY'), True)
				gc.getGame().changeScenarioCounter(1)

			if pPlot.at(20, 20):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_CHAOS_MARAUDER",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_CHAOS'), True)

			if pPlot.at(29, 13):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_CREATION",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_CREATION'), True)
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BLESSED'), True)
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MORALE'), True)
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POTION_OF_RESTORATION'), True)
				caster.setDamage(0, PlayerTypes.NO_PLAYER)
				caster.setLevel(max(1, caster.getLevel()-2))

			if pPlot.at(25, 4):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_RAISE_SKELETON",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH'), True)

			if pPlot.at(37, 21):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_ESCAPE",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DIMENSIONAL'), True)
				gc.getGame().changeScenarioCounter(1)
				gc.getGame().setWinner(0, 2)

			if pPlot.at(35, 22):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_STONESKIN",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_EARTH'), True)

			if pPlot.at(15, 1):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_ENCHANTED_BLADE",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_ENCHANTMENT'), True)
				gc.getGame().changeScenarioCounter(1)

			if pPlot.at(20, 16):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_RUST",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_ENTROPY'), True)
				gc.getGame().changeScenarioCounter(1)

			if pPlot.at(27, 11):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_FIREBALL",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_FIRE'), True)
				gc.getGame().changeScenarioCounter(1)

			if pPlot.at(1, 12):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_TEMPERANCE",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_FORCE'), True)
				gc.getGame().changeScenarioCounter(1)


			if pPlot.at(4, 5):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_SLOW",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_ICE'), True)
				gc.getGame().changeScenarioCounter(1)

			if pPlot.at(35, 14):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_EINHERJAR",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_LAW'), True)
				gc.getGame().changeScenarioCounter(1)

			if pPlot.at(8, 8):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_DESTROY_UNDEAD",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_LIFE'), True)
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN'), True)
				gc.getGame().changeScenarioCounter(1)

			if pPlot.at(27, 22):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_FLOATING_EYE",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_METAMAGIC'), True)
				gc.getGame().changeScenarioCounter(1)

			if pPlot.at(34, 10):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_CHARM",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_MIND'), True)
				gc.getGame().changeScenarioCounter(1)

			if pPlot.at(24, 11):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_BLOOM",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_NATURE'), True)
				gc.getGame().changeScenarioCounter(1)


			if pPlot.at(29, 8):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_SHADOWWALK",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SHADOW'), True)


			if pPlot.at(8, 14):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_COURAGE",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT'), True)
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COURAGE'), True)

			if pPlot.at(25, 17):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_BLIND",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SUN'), True)

			if pPlot.at(20, 11):
				cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_SPRING",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_WATER'), True)
				gc.getGame().changeScenarioCounter(1)



			iTreasure = gc.getInfoTypeForString('EQUIPMENT_TREASURE')
			pTreasure = -1
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getUnitType() == iTreasure:
					if pUnit.getOwner() == caster.getOwner():
						pTreasure = pUnit
			if pTreasure != -1:
				pTreasure.kill(True, 0)
			return False
		return True

	def playerDefeated(self, pPlayer):
		if gc.getGame().getGameTurn() > 5:
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AMELANCHIER'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_AMELANCHIER",()),'art/interface/popups/Amelanchier.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BEERI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_BEERI",()),'art/interface/popups/Beeri.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CAPRIA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_CAPRIA",()),'art/interface/popups/Capria.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CHARADON'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_CHARADON",()),'art/interface/popups/Charadon.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_DAIN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_DAIN",()),'art/interface/popups/Dain.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_EINION'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_EINION",()),'art/interface/popups/Einion.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_HAFGAN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_HALFGAN",()),'art/interface/popups/Halfgan.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SHEELBA'):
					for iTeam in xrange(gc.getMAX_TEAMS()):
						eTeam = gc.getTeam(iTeam)
						if eTeam.isAlive():
							if eTeam.isHuman():
								gc.getGame().setWinner(iTeam, 2)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TASUNKE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_TASUNKE",()),'art/interface/popups/Tasunke.dds')

			elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AURIC'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_DEFEATED_AURIC",()),'art/interface/popups/Auric.dds')
					for iTeam in xrange(gc.getMAX_TEAMS()):
						eTeam = gc.getTeam(iTeam)
						if eTeam.isAlive():
							if not eTeam.isHuman():
								gc.getGame().setWinner(iTeam, 2)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BEERI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_DEFEATED_BEERI",()),'art/interface/popups/Beeri.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_EINION'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_DEFEATED_EINION",()),'art/interface/popups/Einion.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_GARRIM'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_DEFEATED_GARRIM",()),'art/interface/popups/Garrim.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MAHON'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_DEFEATED_MAHON",()),'art/interface/popups/Mahon.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SANDALPHON'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_DEFEATED_SANDALPHON",()),'art/interface/popups/Sandalphon.dds')

			elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BLOOD_OF_ANGELS):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AURIC'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_DEFEATED_AURIC",()),'art/interface/popups/Auric.dds')
					for iTeam in xrange(gc.getMAX_TEAMS()):
						eTeam = gc.getTeam(iTeam)
						if eTeam.isAlive():
							if not eTeam.isHuman():
								gc.getGame().setWinner(iTeam, 2)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_HANNAH'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_DEFEATED_HANNAH",()),'art/interface/popups/Hannah.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MAHALA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_DEFEATED_MAHALA",()),'art/interface/popups/Lucian.dds')
					for iTeam in xrange(gc.getMAX_TEAMS()):
						eTeam = gc.getTeam(iTeam)
						if eTeam.isAlive():
							if not eTeam.isHuman():
								gc.getGame().setWinner(iTeam, 2)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SABATHIEL'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_DEFEATED_SABATHIEL",()),'art/interface/popups/Sabathiel.dds')

			elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_HYBOREM'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_HYBOREM",()),'art/interface/popups/Hyborem.dds')

				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_JUDECCA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_JUDECCA",()),'art/interface/popups/Judecca.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_OUZZA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_OUZZA",()),'art/interface/popups/Ouzza.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_STATIUS'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_STATIUS",()),'art/interface/popups/Statius.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_LETHE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_LETHE",()),'art/interface/popups/Lethe.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MERESIN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_MERESIN",()),'art/interface/popups/Meresin.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SALLOS'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_SALLOS",()),'art/interface/popups/Sallos.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BASIUM'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_BASIUM",()),'art/interface/popups/Basium.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CAPRIA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_CAPRIA",()),'art/interface/popups/Capria.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_KEELYN",()),'art/interface/popups/Keelyn.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_VARN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_VARN",()),'art/interface/popups/Varn.dds')

				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_EINION'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_EINION",()),'art/interface/popups/Einion.dds')
				iCount = 0
				iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
				for iPlayer in xrange(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.isAlive():
						if pPlayer.getCivilizationType() == iInfernal:
							iCount += 1
				if iCount == 0:
					for iPlayer in xrange(gc.getMAX_PLAYERS()):
						pPlayer = gc.getPlayer(iPlayer)
						if pPlayer.isAlive():
							if pPlayer.isHuman():
								gc.getGame().setWinner(pPlayer.getTeam(), 2)

			elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):

				if pPlayer.isHuman():
					iPlayer = pPlayer.getID()
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

				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_DUMANNIOS'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_DUMANNIOS",()),'art/interface/popups/Dumannios.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_RIUROS'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_RIUROS",()),'art/interface/popups/Riuros.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_ANAGANTIOS'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_ANAGANTIOS",()),'art/interface/popups/Anagantios.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MAHALA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_MAHALA",()),'art/interface/popups/Mahala.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AMELANCHIER'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_AMELANCHIER",()),'art/interface/popups/Amelanchier.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_VOLANNA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_VOLANNA",()),'art/interface/popups/Volanna.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_RHOANNA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_RHOANNA",()),'art/interface/popups/Rhoanna.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_FALAMAR'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_FALAMAR",()),'art/interface/popups/Falamar.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CAPRIA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_CAPRIA",()),'art/interface/popups/Capria.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_DECIUS'):
					if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_DECIUS_CALABIM",()),'art/interface/popups/Decius.dds')
					elif pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
						cf.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_DECIUS_MALAKIM",()),'art/interface/popups/Decius.dds')
				elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AURIC'):
					gc.getGame().setWinner(1, 2) #Falamar Wins

			elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_RETURN_OF_WINTER):

				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BRAEDEN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_DEFEATED_AURIC",()),'art/interface/LeaderHeads/Braeden.dds')
					iPlayer = 0 #Mahala
					gc.getPlayer(iPlayer).setAlive(False)

				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CARDITH'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_CARDITH_DEFEATED",()),'art/interface/popups/Cardith.dds')
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								pLoopPlayer.changeGold(250)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KOUN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_KOUN_DEFEATED",()),'art/interface/popups/Koun.dds')
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								pCity = pLoopPlayer.getCapitalCity()
								iX = pCity.getX()
								iY =pCity.getY()
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_OVERLORDS'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_OVERLORDS'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_KILMORPH'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_KILMORPH'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_LEAVES'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_LEAVES'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TETHIRA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_TETHIRA_DEFEATED",()),'art/interface/popups/Tethira.dds')
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								for iUnit in xrange(pLoopPlayer.getNumUnits()):
									pUnit = pLoopPlayer.getUnit(iUnit)
									pUnit.changeExperience(2, -1, False, False, False)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_THESSALONICA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_THESSALONICA_DEFEATED",()),'art/interface/popups/Thessalonica.dds')
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								(pCity, iter) = pLoopPlayer.firstCity(False)
								while(pCity):
									if (not pCity.isNone() and pCity.getOwner() == iLoopPlayer): #only valid cities
										pCity.changeCulture(iLoopPlayer, 300, True)
									(pCity, iter) = pLoopPlayer.nextCity(iter, False)


			elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TEBRYN'):
					gc.getGame().setWinner(0, 2) #Falamar Wins

			elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MELISANDRE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DEFEATED_MELISANDRE",()),'art/interface/popups/Melisandre.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_FURIA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DEFEATED_FURIA",()),'art/interface/popups/Furia.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_WEEVIL'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DEFEATED_WEEVIL",()),'art/interface/popups/Weevil.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TYA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DEFEATED_TYA",()),'art/interface/popups/Tya.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_ULDANOR'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DEFEATED_ULDANOR",()),'art/interface/popups/Uldanor.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SALLOS'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DEFEATED_SALLOS",()),'art/interface/popups/Sallos.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MAHON'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DEFEATED_MAHON",()),'art/interface/popups/Mahon.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BEERI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DEFEATED_BEERI",()),'art/interface/popups/Beeri.dds')
				bValid = True
				if not gc.getPlayer(1).isAlive(): #Perpentach
					gc.getGame().setWinner(0, 2)
					bValid = False
				if gc.getPlayer(2).isAlive(): #Melisandre
					bValid = False
				if gc.getPlayer(3).isAlive(): #Furia
					bValid = False
				if gc.getPlayer(4).isAlive(): #Weevil
					bValid = False
				if gc.getPlayer(5).isAlive(): #Tya
					bValid = False
				if gc.getPlayer(6).isAlive(): #Uldanor
					bValid = False
				if gc.getPlayer(8).isAlive(): #Sallos
					bValid = False
				if gc.getPlayer(9).isAlive(): #Mahon
					bValid = False
				if bValid:
					if gc.getPlayer(7).isAlive(): #Beeri
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_THE_MOMUS_BEERIS_OFFER')
						triggerData = gc.getPlayer(0).initTriggeredData(iEvent, True, -1, -1, -1, 0, -1, -1, -1, -1, -1)
					else:
						gc.getGame().setWinner(0, 2)

			elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
				bWin = False
				iLjosalfar = gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR')
				iSvartalfar = gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')
				iHumanPlayer = -1
				if pPlayer.getCivilizationType() == iLjosalfar:
					bWin = True
					iWinningTeam = 1
					if gc.getPlayer(0).isAlive():
						bWin = False
					if gc.getPlayer(1).isAlive():
						bWin = False
					if gc.getPlayer(2).isAlive():
						bWin = False
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								if pLoopPlayer.getCivilizationType() == iSvartalfar:
									iHumanPlayer = iLoopPlayer
				elif pPlayer.getCivilizationType() == iSvartalfar:
					bWin = True
					iWinningTeam = 0
					if gc.getPlayer(3).isAlive():
						bWin = False
					if gc.getPlayer(4).isAlive():
						bWin = False
					if gc.getPlayer(5).isAlive():
						bWin = False
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								if pLoopPlayer.getCivilizationType() == iLjosalfar:
									iHumanPlayer = iLoopPlayer
				if iHumanPlayer != -1:
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AMELANCHIER'):
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_SPLINTERED_COURT_DEFEATED_AMELANCHIER')
						triggerData = gc.getPlayer(iHumanPlayer).initTriggeredData(iEvent, True, -1, -1, -1, iHumanPlayer, -1, -1, -1, -1, -1)
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_THESSA'):
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_SPLINTERED_COURT_DEFEATED_THESSA')
						triggerData = gc.getPlayer(iHumanPlayer).initTriggeredData(iEvent, True, -1, -1, -1, iHumanPlayer, -1, -1, -1, -1, -1)
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_RIVANNA'):
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_SPLINTERED_COURT_DEFEATED_RIVANNA')
						triggerData = gc.getPlayer(iHumanPlayer).initTriggeredData(iEvent, True, -1, -1, -1, iHumanPlayer, -1, -1, -1, -1, -1)
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_VOLANNA'):
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_SPLINTERED_COURT_DEFEATED_VOLANNA')
						triggerData = gc.getPlayer(iHumanPlayer).initTriggeredData(iEvent, True, -1, -1, -1, iHumanPlayer, -1, -1, -1, -1, -1)
					if not bWin:
						if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_ARENDEL'):
							cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_SPLINTERED_COURT_DEFEATED_ARENDEL",()),'art/interface/popups/Arendel.dds')
						elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_FAERYL'):
							cf.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_SPLINTERED_COURT_DEFEATED_FAERYL",()),'art/interface/popups/Faeryl.dds')
				if bWin:
					gc.getGame().setWinner(iWinningTeam, 2)

			elif gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_WAGES_OF_SIN):
				iCalabim = gc.getInfoTypeForString('CIVILIZATION_CALABIM')
				iElohim = gc.getInfoTypeForString('CIVILIZATION_ELOHIM')
				iMalakim = gc.getInfoTypeForString('CIVILIZATION_MALAKIM')
				iSheaim = gc.getInfoTypeForString('CIVILIZATION_SHEAIM')

				iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
				iSvartalfar = gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')
				iLjosalfar = gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR')
				iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')

				for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if pLoopPlayer.isAlive():
						if pLoopPlayer.isHuman():
							pHumanPlayer = pLoopPlayer
				iCount = 0
				if (pHumanPlayer.getCivilizationType() == iElohim or pHumanPlayer.getCivilizationType() == iMalakim or pHumanPlayer.getCivilizationType() == iMercurians or pHumanPlayer.getCivilizationType() == iLjosalfar):
					if gc.getPlayer(1).isAlive(): #Flauros
						iCount += 1
					if gc.getPlayer(3).isAlive(): #Faeryl
						iCount += 1
					if gc.getPlayer(5).isAlive(): #Os-Gabella
						iCount += 1
					if gc.getPlayer(6).isAlive(): #Hyborem
						iCount += 1
				if (pHumanPlayer.getCivilizationType() == iSheaim or pHumanPlayer.getCivilizationType() == iCalabim or pHumanPlayer.getCivilizationType() == iInfernal or pHumanPlayer.getCivilizationType() == iSvartalfar):
					if gc.getPlayer(0).isAlive(): #Varn
						iCount += 1
					if gc.getPlayer(2).isAlive(): #Arendel
						iCount += 1
					if gc.getPlayer(4).isAlive(): #Ethne
						iCount += 1
					if gc.getPlayer(7).isAlive(): #Basium
						iCount += 1
				if iCount < 1:
					gc.getGame().setWinner(pHumanPlayer.getTeam(), 2)
				szText = -1
				bGood = True
				if pPlayer.getCivilizationType() == iCalabim:
					bGood = False
				if pPlayer.getCivilizationType() == iInfernal:
					bGood = False
				if pPlayer.getCivilizationType() == iSheaim:
					bGood = False
				if pPlayer.getCivilizationType() == iSvartalfar:
					bGood = False

				if iCount == 1:
					if bGood:
						if pHumanPlayer.getCivilizationType() == iCalabim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_3_CALABIM",())
						if pHumanPlayer.getCivilizationType() == iSheaim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_3_SHEAIM",())

						if pHumanPlayer.getCivilizationType() == iSvartalfar:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_3_SVARTALFAR",())
						if pHumanPlayer.getCivilizationType() == iInfernal:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_3_INFERNAL",())

					if not bGood:
						if pHumanPlayer.getCivilizationType() == iElohim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_3_ELOHIM",())
						if pHumanPlayer.getCivilizationType() == iMalakim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_3_MALAKIM",())

						if pHumanPlayer.getCivilizationType() == iLjosalfar:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_3_LJOSALFAR",())
						if pHumanPlayer.getCivilizationType() == iMercurians:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_3_MERCURIANS",())

				if iCount == 2:
					if bGood:
						if pHumanPlayer.getCivilizationType() == iCalabim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_2_CALABIM",())
						if pHumanPlayer.getCivilizationType() == iSheaim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_2_SHEAIM",())

						if pHumanPlayer.getCivilizationType() == iSvartalfar:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_2_SVARTALFAR",())
						if pHumanPlayer.getCivilizationType() == iInfernal:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_2_INFERNAL",())

					if not bGood:
						if pHumanPlayer.getCivilizationType() == iElohim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_2_ELOHIM",())
						if pHumanPlayer.getCivilizationType() == iMalakim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_2_MALAKIM",())

						if pHumanPlayer.getCivilizationType() == iLjosalfar:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_2_LJOSALFAR",())
						if pHumanPlayer.getCivilizationType() == iMercurians:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_2_MERCURIANS",())


				if iCount == 3:
					if bGood:
						if pHumanPlayer.getCivilizationType() == iCalabim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_1_CALABIM",())
						if pHumanPlayer.getCivilizationType() == iSheaim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_1_SHEAIM",())


						if pHumanPlayer.getCivilizationType() == iSvartalfar:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_1_SHEAIM",())
						if pHumanPlayer.getCivilizationType() == iInfernal:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_1_INFERNAL",())

					if not bGood:
						if pHumanPlayer.getCivilizationType() == iElohim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_1_ELOHIM",())
						if pHumanPlayer.getCivilizationType() == iMalakim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_1_MALAKIM",())

						if pHumanPlayer.getCivilizationType() == iLjosalfar:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_1_LJOSALFAR",())
						if pHumanPlayer.getCivilizationType() == iMercurians:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_1_MERCURIANS",())

				if szText != -1:
					szTitle = CyGameTextMgr().getTimeStr(CyGame().getGameTurn(), False)
					popup = PyPopup.PyPopup(-1)
					popup.addDDS('art/interface/popups/Talia.dds', 0, 0, 384, 384)
					popup.addSeparator()
					popup.setHeaderString(szTitle)
					popup.setBodyString(szText)
					popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

