## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Implementaion of miscellaneous game functions

import CvUtil
from CvPythonExtensions import *
import CvEventInterface
import CustomFunctions
import ScenarioFunctions

import PyHelpers
PyPlayer = PyHelpers.PyPlayer

# globals
cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
sf = ScenarioFunctions.ScenarioFunctions()

import CvModName

class CvGameUtils:
	"Miscellaneous game functions"
	def __init__(self):
		pass

	def isVictoryTest(self):
		return CyGame().getElapsedGameTurns() > 10

	def isVictory(self, argsList):
		eVictory = argsList[0]
		return True

	def isPlayerResearch(self, argsList):
		ePlayer = argsList[0]
		return True

	def getExtraCost(self, argsList):
		ePlayer = argsList[0]
		return 0

	def createBarbarianCities(self):
		return False

	def createBarbarianUnits(self):
		return False

	def skipResearchPopup(self,argsList):
		ePlayer = argsList[0]
		return False

	def showTechChooserButton(self,argsList):
		ePlayer = argsList[0]
		return True

	def getFirstRecommendedTech(self,argsList):
		ePlayer = argsList[0]
		return TechTypes.NO_TECH

	def getSecondRecommendedTech(self,argsList):
		ePlayer = argsList[0]
		eFirstTech = argsList[1]
		return TechTypes.NO_TECH

	def canRazeCity(self,argsList):
		iRazingPlayer, pCity = argsList
		return True

	def canDeclareWar(self,argsList):
		iAttackingTeam, iDefendingTeam = argsList
		return True

	def skipProductionPopup(self,argsList):
		pCity = argsList[0]
		return False

	def showExamineCityButton(self,argsList):
		pCity = argsList[0]
		return True

	def getRecommendedUnit(self,argsList):
		pCity = argsList[0]
		return UnitTypes.NO_UNIT

	def getRecommendedBuilding(self,argsList):
		pCity = argsList[0]
		return BuildingTypes.NO_BUILDING

	def updateColoredPlots(self):
		return False

	def isActionRecommended(self,argsList):
		pUnit = argsList[0]
		iAction = argsList[1]
		return False

	def unitCannotMoveInto(self,argsList):
		ePlayer = argsList[0]
		iUnitId = argsList[1]
		iPlotX = argsList[2]
		iPlotY = argsList[3]
		pUnit = gc.getPlayer(ePlayer).getUnit(iUnitId)
		pPlot = CyMap().plot(iPlotX, iPlotY)

		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_EXILE')):
			if pPlot.isOwned():
				if pPlot.getTeam() != pUnit.getTeam():
					if pUnit.isHiddenNationality():
						return True
					if gc.getTeam(pPlot.getTeam()).isAtWar(pUnit.getTeam()):
						return True

		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BOUND_BY_COMPACT')):
			if CyGame().getGlobalCounter() < 99:
				if gc.getTerrainInfo(pPlot.getTerrainType()).getTerrainDown() == -1:#i.e., is not Hell terrain
					if pPlot.isOwned():
						if pPlot.getTeam() != pUnit.getTeam():
							if gc.getPlayer(pPlot.getOwner()).getStateReligion() != gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
								return True
					else:
						return True

		if pPlot.isEnemyCity(pUnit):#The plot has a city or superfort whose owner is at war with unit's owner, or the unit is hidden nationality.
			if pPlot.isCity():#eliminates superforts that would count as isEnemyCity, since for some reason forts were being counted as having every building
				if not pUnit.isImmuneToMagic(): #Runewyns and Djinns are immune to and can dispell Rings of Warding
##					if pUnit.isHiddenNationality() or gc.getTeam(pUnit.getTeam()).isAtWar(pPlot.getTeam()):
					pCity = pPlot.getPlotCity()
				#The Ring of Warding (greater) spell-building prevents hostile summons, Angels, Demons, Elementals, and Undead from entering/attacking the city
					if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_RING_OF_WARDING')):
						if pUnit.getSummoner() != -1 or pUnit.isPermanentSummon() or pUnit.getDuration() > 0 or pUnit.getRace() in [gc.getInfoTypeForString('PROMOTION_ANGEL'),gc.getInfoTypeForString('PROMOTION_DEMON'),gc.getInfoTypeForString('PROMOTION_ELEMENTAL'),gc.getInfoTypeForString('PROMOTION_UNDEAD')]:
							if pUnit.getLevel() < cf.getNumSupplimentalManaPlayer(pCity.getOwner(), gc.getInfoTypeForString('BONUS_MANA_FORCE')) + 3*pCity.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_FORCE')):
								return True
				#The Ring of Warding spell-building prevents hostile summons from entering/attacking the city

					if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_RING_OF_WARDING_LESSER')):
						if pUnit.getSummoner() != -1 or pUnit.isPermanentSummon() or pUnit.getDuration() > 0:
							if pUnit.getLevel() < cf.getNumSupplimentalManaPlayer(pCity.getOwner(), gc.getInfoTypeForString('BONUS_MANA_FORCE')) +  2*pCity.getNumBonuses(gc.getInfoTypeForString('BONUS_MANA_FORCE')):
								return True
				#The Ring of Warding spell-building prevents hostile undead from entering/attacking the city

					if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TOMB_OF_ARAWN')):
						if pUnit.getRace() == gc.getInfoTypeForString('PROMOTION_UNDEAD'):
							return True

		if pPlot.isPythonActive():
			if pUnit.isAutomated() or not pUnit.isHuman():
				if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_HALLOWED_GROUND'):
					if pUnit.getRace() in [gc.getInfoTypeForString('PROMOTION_DEMON'),gc.getInfoTypeForString('PROMOTION_UNDEAD')]:
						return False
				iImprovement = pPlot.getImprovementType()
				if iImprovement != -1:
					if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_TARCHS_TOWER'):
						if not pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING2')):
							return True
					elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_MAELSTROM'):
						if not pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_AIR')):
							return True
					elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_MIRROR_OF_HEAVEN'):
						if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRE')):
							return True
						elif pUnit.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_SHADOWRIDER'):
							return True
					elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WHISPERING_WOOD'):
						if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEASIL_CHARM')):
							pass
						elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOWWALK')):
							pass
						elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GREY')):
							pass
						elif pUnit.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_AURIC'):
							pass
						else:
							return True
		return False

	def cannotHandleAction(self,argsList):
		pPlot = argsList[0]
		iAction = argsList[1]
		bTestVisible = argsList[2]
		return False

	def canBuild(self,argsList):
		iX, iY, iBuild, iPlayer = argsList
		pPlot = CyMap().plot(iX, iY)
		pPlayer = gc.getPlayer(iPlayer)
		iImprovement = pPlot.getImprovementType()
		iImprovementNew = gc.getBuildInfo(iBuild).getImprovement()
		iBonus = pPlot.getBonusType(pPlot.getTeam())
		#I don't want mana nodes blocked by farms, mines, etc

		if iBuild == gc.getInfoTypeForString('BUILD_GRAVEYARD'):
			if pPlayer.getStateReligion() != gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL'):
				return 0
		elif iBuild == gc.getInfoTypeForString('BUILD_FARM'):
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')):
				return 0
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_GRIGORI'):
				return 0
		elif iBuild == gc.getInfoTypeForString('BUILD_HOMESTEAD'):
			if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_GRIGORI'):
				return 0
		elif iBuild == gc.getInfoTypeForString('BUILD_CITADEL_OF_LIGHT'):
			if pPlayer.getStateReligion() != gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
				return 0
			if iImprovement != gc.getInfoTypeForString('IMPROVEMENT_CITADEL'):
				return 0
		elif iBuild == gc.getInfoTypeForString('BUILD_LUMBERMILL'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
				return 0
		elif iBuild == gc.getInfoTypeForString('BUILD_REMOVE_FOREST'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
				if iImprovement != gc.getInfoTypeForString('IMPROVEMENT_SMOKE'):
					return 0
		elif iBuild == gc.getInfoTypeForString('BUILD_MANA_ICE'):
			if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
				iAuricPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
				if iAuricPlayer != -1:
					pAuricPlayer = gc.getPlayer(iAuricPlayer)
					if pAuricPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AURIC')) > 0:
						if gc.getTeam(pPlayer.getTeam()).isAtWar(pAuricPlayer.getTeam()):
							return 0

		if iImprovementNew > -1:
			if iImprovement == iImprovementNew:
				return 0
			if iBonus != -1:
				if gc.getBonusInfo(iBonus).isMana():
					iBonusNew = gc.getImprovementInfo(iImprovementNew).getBonusConvert()
					if iBonusNew == -1:
						return 0
			if pPlot.isOwned():
				if pPlot.getTeam() == pPlayer.getTeam():
					if iImprovement != -1:
						if iImprovement == gc.getImprovementInfo(iImprovementNew).getImprovementPillage():
							return 1
					if pPlot.isPeak():
						if iBuild in [gc.getInfoTypeForString('BUILD_MINE'), gc.getInfoTypeForString('BUILD_QUARRY')]:
							if iImprovement == -1:
								if pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_ARETE')):
									return 1
							if iBonus > -1:
								if gc.getImprovementInfo(iImprovementNew).isImprovementBonusTrade(iBonus):
									return 1
			return -1
		if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')):
			if iBuild == gc.getInfoTypeForString('BUILD_MANA_SUN'):
				if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_SUN_MANA')):
					return 0
		elif pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')):
			if iBuild == gc.getInfoTypeForString('BUILD_MANA_CHAOS'):
				if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_CHAOS_MANA')):
					return 0
			elif iBuild == gc.getInfoTypeForString('BUILD_MANA_DEATH'):
				if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DEATH_MANA')):
					return 0
			elif iBuild == gc.getInfoTypeForString('BUILD_MANA_DIMENSIONAL'):
				if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DIMENSIONAL_MANA')):
					return 0
			elif iBuild == gc.getInfoTypeForString('BUILD_MANA_ENTROPY'):
				if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_ENTROPY_MANA')):
					return 0
			elif iBuild == gc.getInfoTypeForString('BUILD_MANA_SHADOW'):
				if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_SHADOW_MANA')):
					return 0
			elif iBuild == gc.getInfoTypeForString('BUILD_PLANTATION'):
				if iBonus == gc.getInfoTypeForString('BONUS_DESERT_ROSE'):
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DESERT_ROSE')):
						return 0
				elif iBonus == gc.getInfoTypeForString('BONUS_GULAGARM'):
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_GULAGARM')):
						return 0
				elif iBonus == gc.getInfoTypeForString('BONUS_RAZORWEED'):
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_RAZORWEED')):
						return 0
				elif iBonus == gc.getInfoTypeForString('BONUS_SHEUT_STONE'):
					if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_SHEUT_STONE')):
						return 0
		if not pPlayer.isHuman():
			iCiv = pPlayer.getCivilizationType()
			if iCiv in [gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'), gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')]:
				if iBuild in [gc.getInfoTypeForString('BUILD_REMOVE_FOREST'), gc.getInfoTypeForString('BUILD_LUMBERMILL')]:
					return 0
			elif iCiv == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				if iBuild == gc.getInfoTypeForString('BUILD_MANA_LIFE'):
					if pPlayer.getArcaneTowerVictoryFlag() != 1:
						return 0
			elif iCiv == gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
				if iBuild in [gc.getInfoTypeForString('BUILD_MANA_CHAOS'), gc.getInfoTypeForString('BUILD_MANA_DEATH'), gc.getInfoTypeForString('BUILD_MANA_DIMENSIONAL'), gc.getInfoTypeForString('BUILD_MANA_ENTROPY')]:
					if pPlayer.getArcaneTowerVictoryFlag() != 3:
						return 0

		return -1# Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can

	def cannotFoundCity(self,argsList):
		iPlayer, iPlotX, iPlotY = argsList
		return False

	def cannotSelectionListMove(self,argsList):
		pPlot = argsList[0]
		bAlt = argsList[1]
		bShift = argsList[2]
		bCtrl = argsList[3]
		return False

	def cannotSelectionListGameNetMessage(self,argsList):
		eMessage = argsList[0]
		iData2 = argsList[1]
		iData3 = argsList[2]
		iData4 = argsList[3]
		iFlags = argsList[4]
		bAlt = argsList[5]
		bShift = argsList[6]
		return False

	def cannotDoControl(self,argsList):
		eControl = argsList[0]
		return False

	def canResearch(self,argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		return False

	def cannotResearch(self,argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		pPlayer = gc.getPlayer(ePlayer)
		iCiv = pPlayer.getCivilizationType()
		eTeam = gc.getTeam(pPlayer.getTeam())

		if eTech == gc.getInfoTypeForString('TECH_ORDERS_FROM_HEAVEN'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_5):
				return True
		elif eTech == gc.getInfoTypeForString('TECH_HONOR'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_0):
				return True
		elif eTech == gc.getInfoTypeForString('TECH_WAY_OF_THE_EARTHMOTHER'):
			if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_12')):
				return True
		elif eTech == gc.getInfoTypeForString('TECH_WAY_OF_THE_FORESTS'):
			if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_13')):
				return True
		elif eTech == gc.getInfoTypeForString('TECH_MESSAGE_FROM_THE_DEEP'):
			if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_10')):
				return True
		elif eTech == gc.getInfoTypeForString('TECH_DECEPTION'):
			if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_16')):
				return True
		elif eTech == gc.getInfoTypeForString('TECH_CORRUPTION_OF_SPIRIT'):
			if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_21')):
				return True

		if CyGame().getWBMapScript():
			bBlock = sf.cannotResearch(ePlayer, eTech, bTrade)
			if bBlock:
				return True

		return False

	def canDoCivic(self,argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
		return False

	def cannotDoCivic(self,argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]

		infoCivic =  gc.getCivicInfo(eCivic)
		iCivicOption = infoCivic.getCivicOptionType()

		pPlayer = gc.getPlayer(ePlayer)
		eTeam = gc.getTeam(pPlayer.getTeam())


		if eCivic == gc.getInfoTypeForString('CIVIC_ARETE'):
			if pPlayer.getStateReligion() not in [gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'), gc.getInfoTypeForString('RELIGION_RINGGIVER')]:
				return True
		if eCivic == gc.getInfoTypeForString('CIVIC_GUARDIAN_OF_NATURE'):
			if pPlayer.getStateReligion() not in [gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'), gc.getInfoTypeForString('RELIGION_UNBLEMISHED')]:
				return True
		if eCivic == gc.getInfoTypeForString('CIVIC_SOCIAL_ORDER'):
			if pPlayer.getStateReligion() not in [gc.getInfoTypeForString('RELIGION_THE_ORDER'), gc.getInfoTypeForString('RELIGION_ANOINTED')]:
				return True
		
		if eCivic == gc.getInfoTypeForString('CIVIC_SLAVERY'):
			if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_BAN_SLAVERY')):
				if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')):
					return True

		elif eCivic in [gc.getInfoTypeForString('CIVIC_NO_MEMBERSHIP'), gc.getInfoTypeForString('CIVIC_UNDERCOUNCIL'), gc.getInfoTypeForString('CIVIC_OVERCOUNCIL')]:
			if CyGame().getWBMapScript():
				if sf.cannotDoCivic(ePlayer, eCivic):
					return True
			if eCivic == gc.getInfoTypeForString('CIVIC_UNDERCOUNCIL'):
				if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN') or not CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS')):
					return True
			elif eCivic == gc.getInfoTypeForString('CIVIC_OVERCOUNCIL'):
				if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS') or not CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')):
					return True
		return False

	def canTrain(self,argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		return False

	def cannotTrain(self,argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)
		iCiv = pPlayer.getCivilizationType()
		info = gc.getUnitInfo(eUnit)
		eUnitClass = info.getUnitClassType()
		eTeam = gc.getTeam(pPlayer.getTeam())
		iCiv = pPlayer.getCivilizationType()
		iStateReligion = pPlayer.getStateReligion()
		iUnitReligion = info.getReligionType()

		if not pPlayer.isHuman():
			if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_AI_NO_BUILDING_PREREQS')):#I don't want to let Ai players ignore the alignment, religion, civic etc restrictions that apply to temples and thus priests of various religions. This is a simpler way of checling that than applying each bHostile check for ach unit type
				iBuilding = info.getPrereqBuilding()
				if iBuilding != -1:
					if pCity.getNumBuilding(iBuilding) == 0:
						infoBuilding = gc.getBuildingInfo(iBuilding)
						if infoBuilding.getReligionType() == iUnitReligion:
							if self.cannotConstruct([pCity,iBuilding, False, False, True]):
								return True

		if eUnitClass == gc.getInfoTypeForString('UNITCLASS_ADVENTURER'):
			if pPlayer.isUnitClassMaxedOut(eUnitClass,0):
				return True
			iCount = pPlayer.getUnitClassCount(eUnitClass) 
			#iCount = pPlayer.getUnitClassCountPlusMaking(eUnitClass)
			# if pPlayer.isUnitClassMaxedOut(eUnitClass, iCount):
				# return True
			iHero = gc.getInfoTypeForString('PROMOTION_HERO')
			iAdventurer = gc.getInfoTypeForString('PROMOTION_ADVENTURER')
			for loopUnit in PyPlayer(ePlayer).getUnitList():
				if loopUnit.getUnitClassType() == eUnitClass:continue
				if loopUnit.isHasPromotion(iHero) and loopUnit.isHasPromotion(iAdventurer):
					iCount += 1
					if pPlayer.isUnitClassMaxedOut(eUnitClass, iCount):
						return True
						
		if iUnitReligion not in [-1, iStateReligion]:
			if not isLimitedUnitClass(eUnitClass):#this exempts heroes (world units) and high priests (national units)
				iDivine = gc.getInfoTypeForString('PROMOTION_DIVINE')
				iDivine2 = gc.getInfoTypeForString('PROMOTION_DIVINE2')
				if info.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_DISCIPLE') and info.getFreePromotions(iDivine) and not info.getFreePromotions(iDivine2):#narrows it down to priests, not disciples or religious champions
					#if pPlayer.getUnitClassCountPlusMaking(eUnitClass) > pPlayer.getHasReligionCount(iUnitReligion):
					iBuilding = info.getPrereqBuilding()
					if iBuilding > -1:
						iNumTemples = 7
						# iNumTemples = pPlayer.countNumBuildings(iBuilding)
						if pPlayer.getUnitClassCount(eUnitClass) >= iNumTemples:
							return True
						elif pPlayer.getUnitClassCountPlusMaking(eUnitClass) > iNumTemples:
							return True
						# elif eUnitClass == gc.getInfoTypeForString('UNITCLASS_PRIEST_FOXMEN'):
							# iNumVagrant = pPlayer.getUnitClassCountPlusMaking(eUnitClass)
							# iFoxmen = gc.getInfoTypeForString('RELIGION_FOXMEN')
							# for loopUnit in PyPlayer(ePlayer).getUnitList():
								# if loopUnit.getUnitClassType() == eUnitClass:continue
								# if loopUnit.getReligion() == iFoxmen and loopUnit.isHasPromotion(iDivine) and not loopUnit.isHasPromotion(iDivine2):
									# iNumVagrant += 1
									# if iNumVagrant > iNumTemples:
										# return True

		if info.getSpecialUnitType() == gc.getInfoTypeForString('SPECIALUNIT_DRAGON'):
			if not gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_STIR_FROM_SLUMBER')) > 0:
				return True
			if eUnit == gc.getInfoTypeForString('UNIT_DRIFA'):
				if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
					return True

		if pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_CRUSADE')):
			if eUnit in [gc.getInfoTypeForString('UNIT_SETTLER'), gc.getInfoTypeForString('UNIT_WORKER'), gc.getInfoTypeForString('UNIT_WORKBOAT')]:
				return True

		if eUnit == gc.getInfoTypeForString('UNIT_CHAINBREAKER'):
			if pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_SLAVERY')):
				return True


		if eUnitClass == gc.getInfoTypeForString('UNITCLASS_NIGHTWATCH'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
				return False
			if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_ENLIST_THE_NIGHTWATCH')):
				if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')):
					return False
			return True

		elif eUnitClass == gc.getInfoTypeForString('UNITCLASS_RADIANT_GUARD'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
				return False
			if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_ENLIST_THE_GUARD')):
				if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')):
					return False
			return True

		elif eUnit == gc.getInfoTypeForString('UNIT_PYRE_ZOMBIE'):
			if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
				return True
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
				return True
			if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')):
				if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DEATH_MANA')):
					return True


		elif eUnit == gc.getInfoTypeForString('UNIT_LICH'):
			if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
				return True
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
				return True
			if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')):
				if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DEATH_MANA')):
					return True
			pPlot = pCity.plot()
			if pPlot.isOwned():
				if gc.getPlayer(pPlot.getOwner()).countNumBuildings(gc.getInfoTypeForString('BUILDING_SOUL_SHROUD')):
					return True

		elif eUnit == gc.getInfoTypeForString('UNIT_DRACOLICH'):
			if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
				return True
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
				return True
			if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')):
				if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DEATH_MANA')):
					return True
			pPlot = pCity.plot()
			if pPlot.isOwned():
				if gc.getPlayer(pPlot.getOwner()).countNumBuildings(gc.getInfoTypeForString('BUILDING_SOUL_SHROUD')):
					return True

		elif eUnit == gc.getInfoTypeForString('UNIT_DRAGON_SCALED'):
			if iStateReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):#Can gain Thalatth the Blue Dragon
				return True


		elif eUnit == gc.getInfoTypeForString('UNIT_SUCCUBUS'):
			if iCiv != gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				return True

		elif eUnit == gc.getInfoTypeForString('UNIT_LUONNOTAR'):
			if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_7')):
				return True
			if pPlayer.getStateReligion() != -1:
				return True

		elif eUnit == gc.getInfoTypeForString('UNIT_DUIN'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_DUIN):
				return True
			iLeader = gc.getInfoTypeForString('LEADER_DUIN')
			if pPlayer.getLeaderType() != iLeader:
				if cf.getLeader(iLeader) != -1:
					return True

		elif eUnit == gc.getInfoTypeForString('UNIT_GIBBON'):
			#Sometimes the shapeshift/assume true form abilities are letting the the unit be built again.
			for iPlayer2  in xrange(gc.getMAX_PLAYERS()):
				pPlayer2 = gc.getPlayer(iPlayer2)
				(pUnit, iter) = pPlayer2.firstUnit(False)
				while(pUnit):
					if not pUnit.isDead(): #is the unit alive and valid?
						if pUnit.getScenarioCounter() == eUnit:
							return True
					(pUnit, iter) = pPlayer2.nextUnit(iter, False)


		if info.getFreePromotions(gc.getInfoTypeForString('PROMOTION_UNDEAD')):
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
				return True
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL'):
				return True
			if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TOMB_OF_ARAWN')):
				return True
			if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_SOUL_SHROUD')):
				return True
			if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')):
				if CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DEATH_MANA')):
					return True


		if info.getReligionType() == gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ACHERON):
				return True
			if not pPlayer.isHuman():
				return not cf.isHasDragon(pPlayer)

		if not pPlayer.isHuman():
			if eUnit == gc.getInfoTypeForString('UNIT_WORKBOAT'):
				if pPlayer.getUnitClassCount(eUnit) > 3:
					return True



		if CyGame().getWBMapScript():
			bBlock = sf.cannotTrain(pCity, eUnit, bContinue, bTestVisible, bIgnoreCost, bIgnoreUpgrades)
			if bBlock:
				return True

		return False

	def canConstruct(self,argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		return False

	def cannotConstruct(self,argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		info = gc.getBuildingInfo(eBuilding)
		iBuildingClass = info.getBuildingClassType()
		eTeam = gc.getTeam(pPlayer.getTeam())

		if eBuilding == gc.getInfoTypeForString('BUILDING_CHANCEL_OF_GUARDIANS'):
			iX = pCity.getX()
			iY = pCity.getY()
			for iiX in xrange(iX-2, iX+3, 1):
				for iiY in xrange(iY-2, iY+3, 1):
					pLoopPlot = CyMap().plot(iiX,iiY)
					if pLoopPlot.isNone():continue
					if pLoopPlot.isWithinCultureRange(iPlayer):
						iImprovement = pLoopPlot.getImprovementType()
						if iImprovement != -1:
							if gc.getImprovementInfo(iImprovement).isUnique():
								return False
			return True
			
		if info.getSpecialBuildingType() == gc.getInfoTypeForString('SPECIALBUILDING_TEMPLE'):
			iStateReligion = pPlayer.getStateReligion()
			iAlignment = pPlayer.getAlignment()
			iLeader = pPlayer.getLeaderType()
			iGood = gc.getInfoTypeForString('ALIGNMENT_GOOD')
			iEvil = gc.getInfoTypeForString('ALIGNMENT_EVIL')

			iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN') or pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')) or iAlignment == iGood
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
						
			iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS') or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_PACIFISM')) or iAlignment == iGood
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
						
			iTempleFriendly = gc.getInfoTypeForString('BUILDING_ARTIFICERY')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_ARTIFICERY_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RINGGIVER') or iAlignment == iGood or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_ARETE'))
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
						
			iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ORDER') or pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RINGGIVER') or iAlignment == iGood
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
						
			iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED_HOSTILE')
			bFriendly = pPlayer.getStateReligion() in [gc.getInfoTypeForString('RELIGION_UNBLEMISHED'),gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')] or iAlignment == iGood
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
						
			iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH') or (iAlignment != iEvil and pPlayer.getStateReligion() != gc.getInfoTypeForString('RELIGION_FOXMEN'))
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
						
			iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS') or iAlignment != iGood
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
			
			iTempleFriendly = gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY') or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_CONSUMPTION')) or pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_MERCANTILISM')) or iAlignment != iGood
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True

			iTempleFriendly = gc.getInfoTypeForString('BUILDING_ARENA')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_ARENA_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD') or pPlayer.isAnarchy() or iAlignment == iEvil or gc.getTeam(pPlayer.getTeam()).getAtWarCount(True) > 1
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
			iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_ANOINTED_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_ANOINTED') or iAlignment == iEvil
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
						
			iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL') or pPlayer.getCivilizationType == gc.getInfoTypeForString('CIVILIZATION_INFERNAL') or iAlignment == iEvil
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
						
			iTempleFriendly = gc.getInfoTypeForString('BUILDING_TOPHET')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_TOPHET_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_EMBER_LEGION')  or pPlayer.getCivilizationType == gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS') or iAlignment == iEvil
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
						
			iTempleFriendly = gc.getInfoTypeForString('BUILDING_INTERSTICE')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_INTERSTICE_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COVEN') or (iAlignment == iEvil and pCity.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_CALABIM'))
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
						
			iTempleFriendly = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_WHITE_HAND') or pPlayer.getCivilizationType == gc.getInfoTypeForString('CIVILIZATION_ILLIANS')

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
			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True

			iTempleFriendly = gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE')
			iTempleHostile = gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE_HOSTILE')
			bFriendly = pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS') or pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')) or iAlignment == iEvil

			if eBuilding == iTempleFriendly:
				if pCity.getNumBuilding(iTempleHostile):
					return True
				if not bFriendly:
					return True
			elif eBuilding == iTempleHostile:
				if pCity.getNumBuilding(iTempleFriendly):
					return True
				if bFriendly:
					return True
					
					
					
					
		if eBuilding == gc.getInfoTypeForString('BUILDING_TOMB_OF_ARAWN'):
			if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
				if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
					return True
				
		if eBuilding == gc.getInfoTypeForString('BUILDING_SANGUINE_FOUNTAIN'):
			if eTeam.getAtWarCount(False) < 1:
				return True

		if pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_CRUSADE')):
			if eBuilding in [	gc.getInfoTypeForString('BUILDING_ELDER_COUNCIL'),
								gc.getInfoTypeForString('BUILDING_MARKET'),
								gc.getInfoTypeForString('BUILDING_MONUMENT'),
								gc.getInfoTypeForString('BUILDING_MONEYCHANGER'),
								gc.getInfoTypeForString('BUILDING_THEATRE'),
								gc.getInfoTypeForString('BUILDING_AQUEDUCT'),
								gc.getInfoTypeForString('BUILDING_PUBLIC_BATHS'),
								gc.getInfoTypeForString('BUILDING_HERBALIST'),
								gc.getInfoTypeForString('BUILDING_CARNIVAL'),
								gc.getInfoTypeForString('BUILDING_COURTHOUSE'),
								gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE'),
								gc.getInfoTypeForString('BUILDING_GRANARY'),
								gc.getInfoTypeForString('BUILDING_SMOKEHOUSE'),
								gc.getInfoTypeForString('BUILDING_LIBRARY'),
								gc.getInfoTypeForString('BUILDING_HARBOR'),
								gc.getInfoTypeForString('BUILDING_ALCHEMY_LAB'),
								gc.getInfoTypeForString('BUILDING_BREWERY'),
								gc.getInfoTypeForString('BUILDING_BREEDING_PIT')
								]:
				return True
		if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD'):
			if eBuilding in [	gc.getInfoTypeForString('BUILDING_ELDER_COUNCIL'),
								gc.getInfoTypeForString('BUILDING_CHANCEL_OF_GUARDIANS'),
								gc.getInfoTypeForString('BUILDING_COUNCIL_OF_ANCIENTS'),
								gc.getInfoTypeForString('BUILDING_COURTHOUSE'),
								gc.getInfoTypeForString('BUILDING_COMMAND_POST')
								]:
				return True

		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')):
			if eBuilding in [	gc.getInfoTypeForString('BUILDING_AQUEDUCT'),
						gc.getInfoTypeForString('BUILDING_HERBALIST'),
						gc.getInfoTypeForString('BUILDING_GRANARY'),
						gc.getInfoTypeForString('BUILDING_SMOKEHOUSE'),
						gc.getInfoTypeForString('BUILDING_BREEDING_PIT')
						]:
				return True

		listAltars =[	gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR'),
				gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_ANOINTED'),
				gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_BLESSED'),
				gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_CONSECRATED'),
				gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_DIVINE'),
				gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_EXALTED'),
				gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_FINAL')
				]

		if eBuilding in listAltars:
			if eBuilding == gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_FINAL'):
				if pPlayer.getStateReligion() != -1:
					return True
##			if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
##				return True
			for iAltar in listAltars[listAltars.index(eBuilding):]:
				if pPlayer.countNumBuildings(iAltar) > 0:
					return True

		elif eBuilding == gc.getInfoTypeForString('BUILDING_GRAND_MENAGERIE'):
			listCages = [	'BUILDING_LION_CAGE',
							'BUILDING_WOLF_PEN',
							'BUILDING_DANCING_BEAR',
							'BUILDING_AVIARY',
							'BUILDING_TIGER_CAGE',
							'BUILDING_HYENA_CAGE',
							'BUILDING_PANTHER_CAGE',
							'BUILDING_DEER_CAGE',
							'BUILDING_GORILLA_CAGE',
							'BUILDING_BABOON_CAGE',
							'BUILDING_SPIDER_PEN',
							'BUILDING_SCORPION_PEN',
							'BUILDING_ELEPHANT_PEN',
							'BUILDING_GRIFFON_CAGE',
							'BUILDING_GIANT_CAGE',
							'BUILDING_HUMAN_CAGE',
							'BUILDING_ELF_CAGE',
							'BUILDING_ORC_CAGE',
							'BUILDING_DWARF_CAGE',
							'BUILDING_LAMIA_CAGE',
							'BUILDING_CENTAUR_CAGE',
							'BUILDING_MUSTEVAL_CAGE',
							'BUILDING_FROSTLING_CAGE',
							'BUILDING_SATYR_CAGE',
							'BUILDING_LIZARDMAN_CAGE',
							'BUILDING_TORTOISE_TANK',
							'BUILDING_SEA_SERPENT_TANK'
							]

			iNumCages = 0
			for sCage in listCages:
				if pCity.getNumRealBuilding(gc.getInfoTypeForString(sCage)):
					iNumCages += 1
			if iNumCages < 7:
				return True

		elif eBuilding == gc.getInfoTypeForString('BUILDING_CROWN_OF_AKHARIEN'):
			if CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_CROWN_OF_AKHARIEN'), 0):
				return True

		elif eBuilding == gc.getInfoTypeForString('BUILDING_HERON_THRONE'):
			if CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_HERON_THRONE'), 0):
				return True

		elif eBuilding == gc.getInfoTypeForString('BUILDING_EYES_AND_EARS_NETWORK'):
			if not pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')):
				return True
##			if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')):
##				return True


		elif eBuilding == gc.getInfoTypeForString('BUILDING_MERCURIAN_GATE'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_HYBOREM_OR_BASIUM):
				return True
			iAV = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
			if pPlayer.getStateReligion() == iAV:
				return True

			iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
			if pPlayer.getCivilizationType() == iInfernal:
				return True

			iBasium = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
			if iBasium != -1:
				pBasium = gc.getPlayer(iBasium)
				if pBasium.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_BASIUM')) > 0:
					return True

			if not pPlayer.isHuman():
				if eTeam.getAtWarCount(False) > 0:
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							iLoopTeam = pLoopPlayer.getTeam()
							if eTeam.isAtWar(iLoopTeam):
								if pLoopPlayer.getStateReligion() == iAV:
									return False
								if pLoopPlayer.getCivilizationType() == iInfernal:
									return False
				return True


		elif eBuilding == gc.getInfoTypeForString('BUILDING_PLANAR_GATE'):
			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED')):
				return True

		elif eBuilding == gc.getInfoTypeForString('BUILDING_SHRINE_OF_THE_CHAMPION'):
			iHero = cf.getHero(pPlayer)
			if iHero == -1:
				return True
			if not CyGame().isUnitClassMaxedOut(iHero, 0):
				return True
			if pPlayer.getUnitClassCount(iHero) > 0:
				return True
			for iPlayer2  in xrange(gc.getMAX_PLAYERS()):
				pPlayer2 = gc.getPlayer(iPlayer2)
				if pPlayer2.getUnitClassCount(iHero) > 0:
					return True

		elif eBuilding == gc.getInfoTypeForString('BUILDING_SMUGGLERS_PORT'):
			if not PyPlayer( pCity.getOwner() ).isVotePassed(gc.getInfoTypeForString( "VOTE_SMUGGLING_RING" ) ) :
				return True

		iReligion = gc.getBuildingInfo(eBuilding).getReligionType()
		if iReligion != -1:

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
					return True



### Start AI restrictions ###
		if not pPlayer.isHuman():


			if eBuilding == gc.getInfoTypeForString('BUILDING_PROPHECY_OF_RAGNAROK'):
				if pPlayer.getAlignment() != gc.getInfoTypeForString('ALIGNMENT_EVIL'):
					return True
				if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
					if pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_SLAVERY')):
						return True

			elif eBuilding == gc.getInfoTypeForString('BUILDING_INFERNAL_GRIMOIRE'):
				if pPlayer.getAlignment() != gc.getInfoTypeForString('ALIGNMENT_EVIL'):
					return True

			elif eBuilding == gc.getInfoTypeForString('BUILDING_MERCURIAN_GATE'):
				if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
					return True
				if pCity.isCapital():
					if pPlayer.getNumCities() > 1:
						return True
				else:
					if pCity.isHolyCity():
						return True
					if pCity.getAltarLevel() > 0:
						return True

			elif eBuilding == gc.getInfoTypeForString('BUILDING_PLANAR_GATE'):
				if pPlayer.isStrike():
					return True

			elif eBuilding == gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND'):
				if pPlayer.getStateReligion() != gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
					return True

			elif eBuilding == gc.getInfoTypeForString('BUILDING_CRUCIBLE'):
				if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_ARCANE')):
					return True
				if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_SUMMONER')):
					return True
				if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_SUNDERED')):
					return True
				if pPlayer.getCivilizationType() in [	gc.getInfoTypeForString('CIVILIZATION_AMURITES'),
									gc.getInfoTypeForString('CIVILIZATION_INFERNAL'),
									gc.getInfoTypeForString('CIVILIZATION_ILLIANS'),
									gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'),
									gc.getInfoTypeForString('CIVILIZATION_SHEAIM')
									]:
					return True
				if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_MASTERY')) > 0:
					return True
				if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_DIVINATION')) + pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_ALTERATION')) + pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_NECROMANCY')) + pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_THE_ELEMENTS')) > 2:
					return True

### End AI restrictions ###
		if CyGame().getWBMapScript():
			bBlock = sf.cannotConstruct(pCity, eBuilding, bContinue, bTestVisible, bIgnoreCost)
			if bBlock:
				return True

		return False

	def canCreate(self,argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		return False

	def cannotCreate(self,argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()
		eTeam = gc.getTeam(iTeam)
		iCiv = pPlayer.getCivilizationType()
		iStateReligion = pPlayer.getStateReligion()
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if eProject == gc.getInfoTypeForString('PROJECT_RITES_OF_OGHMA'):
			if not iStateReligion == gc.getInfoTypeForString('RELIGION_LAERAN_CORD'):
				return True

		if PyHelpers.PyGame().doesBuildingExist(gc.getInfoTypeForString('BUILDING_CRUCIBLE')):
			if eProject not in [gc.getInfoTypeForString('PROJECT_PACT_OF_THE_NILHORN'),gc.getInfoTypeForString('PROJECT_BANE_DIVINE'),gc.getInfoTypeForString('PROJECT_PURGE_THE_UNFAITHFUL')]:
				return True

		if gc.getProjectInfo(eProject).getMaxGlobalInstances() != 1:
			for pyCity in PyPlayer(iPlayer).getCityList():
				pCity2 = pyCity.GetCy()
				if pCity2.getID() != pCity.getID():
					if pCity2.isProductionProject():
						if eProject == pCity2.getProductionProject():
							return True

		if eProject == gc.getInfoTypeForString('PROJECT_STIR_FROM_SLUMBER'):
			if not pCity.isHasReligion(gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON')):
				if pPlayer.getCivilizationType() not in [ gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'), gc.getInfoTypeForString('CIVILIZATION_SHEAIM')]:
					return True
			iNumWyrmholds = 0
			listWyrmholds = [	'IMPROVEMENT_WYRMHOLD_FEATHERED',
								'IMPROVEMENT_WYRMHOLD_BLOOD',
								'IMPROVEMENT_WYRMHOLD_SIEGE',
								'IMPROVEMENT_WYRMHOLD_GOLD',
								'IMPROVEMENT_WYRMHOLD_GRAVE',
								'IMPROVEMENT_WYRMHOLD_OBSIDIAN',
								'IMPROVEMENT_WYRMHOLD_FANG',
								'IMPROVEMENT_WYRMHOLD_RUNE',
								'IMPROVEMENT_WYRMHOLD_PIT',
								'IMPROVEMENT_WYRMHOLD_FURNACE',
								'IMPROVEMENT_WYRMHOLD_ELDER',
								'IMPROVEMENT_WYRMHOLD_WINTER',
								'IMPROVEMENT_WYRMHOLD_SHIELD',
								'IMPROVEMENT_WYRMHOLD_CORAL',
								'IMPROVEMENT_WYRMHOLD_VAULT',
								'IMPROVEMENT_WYRMHOLD_SEED',
								'IMPROVEMENT_WYRMHOLD_SHADOW',
								'IMPROVEMENT_WYRMHOLD_SHIMMERING',
								'IMPROVEMENT_WYRMHOLD_DAWN',
								'IMPROVEMENT_WYRMHOLD_SCALED'
								]
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_OMNISCIENCE')):
				listWyrmholds.append('IMPROVEMENT_WYRMHOLD_SPIRE')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_MALEVOLENT_DESIGNS')) and eTeam.isBuildingClassMaxedOut(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_NECROMANCY'),0):
				if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_SIDAR') and pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_SOUL_SHROUD')) < 1:
					listWyrmholds.append('IMPROVEMENT_WYRMHOLD_DRACOLICH')
			for sWyrmhold in listWyrmholds:
				iWyrmhold = gc.getInfoTypeForString(sWyrmhold)
				infoWyrmhold = gc.getImprovementInfo(iWyrmhold)
				iBonus = infoWyrmhold.getBonusConvert()
				if iBonus != -1:
					if cf.getNumBonusEffective(iPlayer, iBonus) < 1:
						continue
				if cf.findImprovement(iWyrmhold) != -1:
					continue
				iDragon = infoWyrmhold.getSpawnUnitType()
				if iDragon !=-1:
					if bPlayer.isUnitClassMaxedOut(gc.getUnitInfo(iDragon).getUnitClassType(), 1):continue
					iNumWyrmholds += 1
					return False
			if iNumWyrmholds < 1:
				return True

		if eProject == gc.getInfoTypeForString('PROJECT_GLORY_EVERLASTING'):
			if not pPlayer.isHuman():
				if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
					return True

		elif eProject == gc.getInfoTypeForString('PROJECT_GENESIS'):
			if iCiv in [gc.getInfoTypeForString('CIVILIZATION_INFERNAL'), gc.getInfoTypeForString('CIVILIZATION_ILLIANS')]:
				return True

		elif eProject == gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_HYBOREM_OR_BASIUM):
				return True
			if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')) < 1:
				return True
			if iStateReligion != gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				if not pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_SACRIFICE_THE_WEAK')):
					return True
			if iCiv in [gc.getInfoTypeForString('CIVILIZATION_INFERNAL'), gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')]:
				return True
			if pCity.isHasReligion(gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')):

				if not pPlayer.isHuman():
					if iCiv != gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
						if not eTeam.isAtWar(gc.getBARBARIAN_TEAM()):
							if eTeam.getAtWarCount(False) < 2:
								return True

				lDemonLords = [	gc.getInfoTypeForString('LEADER_HYBOREM'),
								gc.getInfoTypeForString('LEADER_JUDECCA'),
								gc.getInfoTypeForString('LEADER_SALLOS'),
								gc.getInfoTypeForString('LEADER_OUZZA'),
								gc.getInfoTypeForString('LEADER_MERESIN'),
								gc.getInfoTypeForString('LEADER_STATIUS'),
								gc.getInfoTypeForString('LEADER_LETHE')
								]
				for iLeader in lDemonLords:

					if not CyGame().isLeaderEverActive(iLeader):
						return False

					iDemonPlayer = cf.getLeader(iLeader)
					if iDemonPlayer != -1:
						pDemonPlayer = gc.getPlayer(iDemonPlayer)
##						if pDemonPlayer.isAlive():
##							continue

						iHero = cf.getHero(pDemonPlayer)
						if pDemonPlayer.getUnitClassCount(iHero) > 0:
							continue

						iUnit = gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_INFERNAL')).getCivilizationUnits(iHero)

						iSluagh = gc.getInfoTypeForString('UNIT_SLUAGH')
						lBoundProm = [	gc.getInfoTypeForString('PROMOTION_NETHERBIND'),
										gc.getInfoTypeForString('PROMOTION_CAPTUS_CAVEAE_ANGELORUM'),
										gc.getInfoTypeForString('PROMOTION_SOUL_FORGED'),
										gc.getInfoTypeForString('PROMOTION_INCARCERATUS_JUDICII')
										]

						for pSluagh in PyPlayer(gc.getBARBARIAN_PLAYER()).getUnitList():
##						pNetherworld = CyMap().plot(0, 0)
##						for i in xrange(pNetherworld.getNumUnits()):
##							pSluagh = pNetherworld.getUnit(i)
							if pSluagh.getScenarioCounter() == iUnit:
								if pSluagh.getUnitType() == iSluagh:
									for iProm in lBoundProm:
										if pSluagh.isHasPromotion(iProm):
											break
									else:
										return False
			return True

		elif eProject == gc.getInfoTypeForString('PROJECT_PURGE_THE_UNFAITHFUL'):
			if pPlayer.isHuman():
				if iStateReligion != -1:
					for pyCity in PyPlayer(iPlayer).getCityList():
						pCity2 = pyCity.GetCy()
						for iTarget in xrange(gc.getNumReligionInfos()):
							if iStateReligion != iTarget:
								if pCity2.isHasReligion(iTarget) and not pCity2.isHolyCityByType(iTarget):
									return False
			return True

		elif eProject == gc.getInfoTypeForString('PROJECT_MANIFEST_TRISTAN'):
			if not iStateReligion == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS'):
				return True
			if not pCity.isHasReligion(gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS')):
				return True
			if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
				return True

		elif eProject == gc.getInfoTypeForString('PROJECT_BIRTHRIGHT_REGAINED'):
			if not pPlayer.isFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL):
				return True

		elif eProject == gc.getInfoTypeForString('PROJECT_THE_WHITE_HAND'):
			if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_17')):
				return True
			if not pPlayer.isHuman():
				if iCiv not in [gc.getInfoTypeForString('CIVILIZATION_ILLIANS'), gc.getInfoTypeForString('CIVILIZATION_DOVIELLO')]:
					return True

		elif eProject == gc.getInfoTypeForString('PROJECT_THE_DEEPENING'):
			if not iStateReligion == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
				return True

		elif eProject in [gc.getInfoTypeForString('PROJECT_ASCENSION'), gc.getInfoTypeForString('PROJECT_THE_DRAW')]:
			if iStateReligion == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
				if CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('UNITCLASS_AURIC'), 0):
					iAuricPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
					if iAuricPlayer != -1:
						pAuricPlayer = gc.getPlayer(iAuricPlayer)
						if pAuricPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AURIC')) > 0:
							return False
			return True

##Since The Deepening now requires Samhain, I don't want to block it
##		if eProject == gc.getInfoTypeForString('PROJECT_SAMHAIN'):
##			if not pPlayer.isHuman():
##				if pPlayer.getNumCities() <= 3:#I think this may be backwards.
##					return True

		elif eProject == gc.getInfoTypeForString('PROJECT_THE_DRAW'):
			if not pPlayer.isHuman():
				if not pPlayer.isHasTech(gc.getInfoTypeForString('TECH_OMNISCIENCE')):
					return True

		return False

	def canMaintain(self,argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]
		return False

	def cannotMaintain(self,argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]
		return False

	def AI_chooseTech(self,argsList):
		ePlayer = argsList[0]
		bFree = argsList[1]
		pPlayer = gc.getPlayer(ePlayer)

		return TechTypes.NO_TECH

	def AI_chooseProduction(self,argsList):
		pCity = argsList[0]
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)
		pPlot = pCity.plot()

		## AI catches for buildings and projects that have python-only effects
		if not pPlayer.isHuman():

			if pPlayer.isBarbarian():
				if not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ACHERON):

					iBuilding = gc.getInfoTypeForString('BUILDING_WYRMHOLD')
					if pCity.canConstruct(iBuilding, True, False, False):
						pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iBuilding,-1, False, False, False, False)
						return 1

					iUnit = gc.getInfoTypeForString('UNIT_ACHERON')
					if pCity.canTrain(iUnit, True, False):

						pCity.pushOrder(OrderTypes.ORDER_TRAIN, iUnit, -1, False, False, False, False)
						return 1
						# if pPlayer.getNumCities() == 0:

							# pCity.pushOrder(OrderTypes.ORDER_TRAIN, gc.getInfoTypeForString('UNIT_ACHERON'), -1, False, False, False, False)
							# return 1

						# pBones = cf.findImprovement(gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES'))
						# if pBones != -1:
							# if pCity == CyMap().findCity(pBones.getX(), pBones.getY(), ePlayer, TeamTypes.NO_TEAM, True, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, pPlayer.getCity(-1)):

								# pCity.pushOrder(OrderTypes.ORDER_TRAIN, gc.getInfoTypeForString('UNIT_ACHERON'), -1, False, False, False, False)
								# return 1




			iCivType = pPlayer.getCivilizationType()
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_TOLERANT')):
				iCivType = pCity.getCivilizationType()


			## Illians - make sure we build our best projects
			if iCivType == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):
					if pCity.canConstruct(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND'), True, False, False):
						iBadTileCount = 0
						for iiX in xrange(pCity.getX()-1, pCity.getX()+2, 1):
							for iiY in xrange(pCity.getY()-1, pCity.getY()+2, 1):
								pNearbyPlot = CyMap().plot(iiX,iiY)
								if (not pNearbyPlot.isWater()):
									if (pNearbyPlot.getYield(YieldTypes.YIELD_FOOD) < 2):
										iBadTileCount += 1
						if (iBadTileCount >= 4):
							pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND'),-1, False, False, False, False)
							return 1

					if pCity.findYieldRateRank(YieldTypes.YIELD_PRODUCTION) < 3:
						iProject = gc.getInfoTypeForString('PROJECT_THE_WHITE_HAND')
						if pCity.canCreate(iProject, True, True):
							pCity.pushOrder(OrderTypes.ORDER_CREATE,iProject,-1, False, False, False, False)
							return 1
						iProject = gc.getInfoTypeForString('PROJECT_ASCENSION')
						if pCity.canCreate(iProject, True, True):
							pCity.pushOrder(OrderTypes.ORDER_CREATE,iProject,-1, False, False, False, False)
							return 1


			## Sidar should build Tomb of Arawn to protect from Undead
			if iCivType == gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
				if pCity.canConstruct(gc.getInfoTypeForString('BUILDING_TOMB_OF_ARAWN'), True, False, False):
					pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,gc.getInfoTypeForString('BUILDING_TOMB_OF_ARAWN'),-1, False, False, False, False)
					return 1

				if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
					if pCity.canConstruct(gc.getInfoTypeForString('BUILDING_SOUL_SHROUD'), True, False, False):
						pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,gc.getInfoTypeForString('BUILDING_SOUL_SHROUD'),-1, False, False, False, False)
						return 1

			## Clan should build Warrens
			if iCivType == gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS'):
				if pCity.getCultureLevel() > 1 and pCity.getPopulation() > 3:
					iBuilding = gc.getInfoTypeForString('BUILDING_WARRENS')
					if pCity.canConstruct(iBuilding, True, False, False):
						pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iBuilding,-1, False, False, False, False)
						return 1

			## Sheaim should build Planar Gates
			elif iCivType == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
				if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_MAGE_GUILD')) > 0:
					iBuilding = gc.getInfoTypeForString('BUILDING_PLANAR_GATE')
					if pCity.canConstruct(iBuilding, True, False, False):
						pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iBuilding,-1, False, False, False, False)
						return 1
					elif pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
						iBuilding = gc.getInfoTypeForString('BUILDING_PROPHECY_OF_RAGNAROK')
						if pCity.canConstruct(iBuilding, True, False, False):
							pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iBuilding,-1, False, False, False, False)
							return 1


			## Sheaim should build Chancels
			elif iCivType == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
				iBuilding = gc.getInfoTypeForString('BUILDING_CHANCEL_OF_GUARDIANS')
				if pCity.canConstruct(iBuilding, True, False, False):
					pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iBuilding,-1, False, False, False, False)
					return 1
				
		if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL'):
			iBuilding = gc.getInfoTypeForString('BUILDING_RELIQUARY')
			if pCity.canConstruct(iBuilding, True, False, False):
				pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iBuilding,-1, False, False, False, False)
				return 1
##
##			if pCity.canTrain(gc.getInfoTypeForString('UNIT_HAWK'), True, False):
##				if pPlot.countNumAirUnits(pPlayer.getTeam()) == 0:
##					pCity.pushOrder(OrderTypes.ORDER_TRAIN, gc.getInfoTypeForString('UNIT_HAWK'), -1, False, False, False, False)
##					return 1

		return False

	def AI_unitUpdate(self,argsList):
		pUnit = argsList[0]
		pPlot = pUnit.plot()
		iUnitType = pUnit.getUnitType()
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		if pPlayer.isBarbarian():
			if iUnitType == gc.getInfoTypeForString('UNIT_GIANT_SPIDER'):
				iX = pUnit.getX()
				iY = pUnit.getY()
				for iDirection in range(DirectionTypes.NUM_DIRECTION_TYPES):
					pLoopPlot= plotDirection(iX, iY, DirectionTypes(iDirection))
					if not pLoopPlot.isNone():
						for i in range(pLoopPlot.getNumUnits()):
							if pLoopPlot.getUnit(i).getOwner() != iPlayer:
								return 0
				pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
				return 1

		if iUnitType == gc.getInfoTypeForString('UNIT_ACHERON'):
			if pPlot.isVisibleEnemyUnit(iPlayer):
				pUnit.cast(gc.getInfoTypeForString('SPELL_BREATH_FIRE'))

		# iImprovement = pPlot.getImprovementType()
		# if iImprovement != -1:
			# if (iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BARROW') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_RUINS') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE')):
				# if not pUnit.isAnimal():
					# if pPlot.getNumUnits() - pPlot.getNumAnimalUnits() == 1:
						# pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
						# return 1
			# if (iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BEAR_DEN') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_LION_DEN')):
				# if pUnit.isAnimal():
					# if pPlot.getNumAnimalUnits() == 1:
						# pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
						# return 1
			# if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_GOBLIN_FORT'):
				# if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ARCHER'):
					# pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
					# return 1
				# if not pUnit.isAnimal():
					# if pPlot.getNumUnits() - pPlot.getNumAnimalUnits() <= 2:
						# pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
						# return 1

		return False

	def AI_doWar(self,argsList):
		eTeam = argsList[0]
		return False

	def AI_doDiplo(self,argsList):
		ePlayer = argsList[0]
		return False

	def calculateScore(self,argsList):
		ePlayer = argsList[0]
		bFinal = argsList[1]
		bVictory = argsList[2]

		iPopulationScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getPopScore(), CyGame().getInitPopulation(), CyGame().getMaxPopulation(), gc.getDefineINT("SCORE_POPULATION_FACTOR"), True, bFinal, bVictory)
		iLandScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getLandScore(), CyGame().getInitLand(), CyGame().getMaxLand(), gc.getDefineINT("SCORE_LAND_FACTOR"), True, bFinal, bVictory)
		iTechScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getTechScore(), CyGame().getInitTech(), CyGame().getMaxTech(), gc.getDefineINT("SCORE_TECH_FACTOR"), True, bFinal, bVictory)
		iWondersScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getWondersScore(), CyGame().getInitWonders(), CyGame().getMaxWonders(), gc.getDefineINT("SCORE_WONDER_FACTOR"), False, bFinal, bVictory)
		return int(iPopulationScore + iLandScore + iWondersScore + iTechScore)

	def doHolyCity(self):
		return False

	def doHolyCityTech(self,argsList):
		eTeam = argsList[0]
		ePlayer = argsList[1]
		eTech = argsList[2]
		bFirst = argsList[3]
		return False

	def doGold(self,argsList):
		ePlayer = argsList[0]
		return False

	def doResearch(self,argsList):
		ePlayer = argsList[0]
		return False

	def doGoody(self,argsList):
		ePlayer = argsList[0]
		pPlot = argsList[1]
		pUnit = argsList[2]
		return False

	def doGrowth(self,argsList):
		pCity = argsList[0]
		return False

	def doProduction(self,argsList):
		pCity = argsList[0]
		return False

	def doCulture(self,argsList):
		pCity = argsList[0]
		pPlayer = gc.getPlayer(pCity.getOwner())
##		if pPlayer.isBarbarian():
##			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_THE_DRAGONS_HOARD')) == 0:
##				return 1
		return False

	def doPlotCulture(self,argsList):
		pCity = argsList[0]
		bUpdate = argsList[1]
		ePlayer = argsList[2]
		iCultureRate = argsList[3]
		return False

	def doReligion(self,argsList):
		pCity = argsList[0]
		return False

	def cannotSpreadReligion(self,argsList):
		iOwner, iUnitID, iReligion, iX, iY = argsList[0]
		return False

	def doGreatPeople(self,argsList):
		pCity = argsList[0]
		return False

	def doMeltdown(self,argsList):
		pCity = argsList[0]
		return False

	def doReviveActivePlayer(self,argsList):
		"allows you to perform an action after an AIAutoPlay"
		iPlayer = argsList[0]
		return False

	def doPillageGold(self, argsList):
		"controls the gold result of pillaging"
		pPlot = argsList[0]
		pUnit = argsList[1]
		iPillageGold = CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 1")
		iPillageGold += CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 2")
		iPillageGold += (pUnit.getPillageChange() * iPillageGold) / 100
		return iPillageGold

	def doCityCaptureGold(self, argsList):
		"controls the gold result of capturing a city"
		pOldCity = argsList[0]
		iCaptureGold = gc.getDefineINT("BASE_CAPTURE_GOLD")
		iCaptureGold += (pOldCity.getPopulation() * gc.getDefineINT("CAPTURE_GOLD_PER_POPULATION"))
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND1"), "Capture Gold 1")
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND2"), "Capture Gold 2")
		if gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS") > 0:
			iCaptureGold *= cyIntRange((CyGame().getGameTurn() - pOldCity.getGameTurnAcquired()), 0, gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS"))
			iCaptureGold /= gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS")
		return iCaptureGold

	def citiesDestroyFeatures(self,argsList):
		iX, iY= argsList
		pPlot = CyMap().plot(iX,iY)
		if pPlot.isOwned():
			iCiv = gc.getPlayer(pPlot.getOwner()).getCivilizationType()
			iFeature = pPlot.getFeatureType()
			if iCiv in [gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'), gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')]:
				if iFeature in [gc.getInfoTypeForString('FEATURE_FOREST_NEW'), gc.getInfoTypeForString('FEATURE_FOREST'), gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT')]:
					return False
			elif iCiv == gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
				if iFeature == gc.getInfoTypeForString('FEATURE_FOREST_NEW'):
					return False
			elif iCiv == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
				if iFeature in [gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'), gc.getInfoTypeForString('FEATURE_OASIS')]:
					return False
			elif iCiv == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				if iFeature in [gc.getInfoTypeForString('FEATURE_OBSIDIAN_PLAINS'), gc.getInfoTypeForString('FEATURE_TORMENTED_SOULS')]:
					return False
			elif iCiv == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):
				if iFeature == gc.getInfoTypeForString('FEATURE_BLIZZARD'):
					return False

		return True

	def canFoundCitiesOnWater(self,argsList):
		iX, iY= argsList
		return False

	def doCombat(self,argsList):
		pSelectionGroup, pDestPlot = argsList
		return False

	def getConscriptUnitType(self, argsList):
		iPlayer = argsList[0]
		iConscriptUnitType = -1 #return this with the value of the UNIT TYPE you want to be conscripted, -1 uses default system
		return iConscriptUnitType

	def getCityFoundValue(self, argsList):
		iPlayer, iPlotX, iPlotY = argsList
		iFoundValue = -1 # Any value besides -1 will be used
		return iFoundValue

	def canPickPlot(self, argsList):
		pPlot = argsList[0]
		return True

	def getUnitCostMod(self, argsList):
		iPlayer, iUnit = argsList
		iCostMod = -1 # Any value > 0 will be used
		return iCostMod

	def getBuildingCostMod(self, argsList):
		iPlayer, iCityID, iBuilding = argsList
		iCostMod = -1 # Any value > 0 will be used
		pPlayer = gc.getPlayer(iPlayer)
		pCity = pPlayer.getCity(iCityID)
		iCostMod = 100

		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_THE_ORDER') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_COURTHOUSE'),
								gc.getInfoTypeForString('BUILDING_TRAINING_YARD'),
								gc.getInfoTypeForString('BUILDING_COMMAND_POST'),
								gc.getInfoTypeForString('BUILDING_PALACE_BANNOR')]:
				iCostMod /= 2

		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_THE_EMPYREAN') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_DESERT_SHRINE'),
								gc.getInfoTypeForString('BUILDING_LIGHTHOUSE'),
								gc.getInfoTypeForString('BUILDING_TOWER_OF_DIVINATION'),
								gc.getInfoTypeForString('BUILDING_PALACE_MALAKIM')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_WALLS'),
								gc.getInfoTypeForString('BUILDING_DWARVEN_SMITHY'),
								gc.getInfoTypeForString('BUILDING_FORGE'),
								gc.getInfoTypeForString('BUILDING_TOWER_OF_THE_ELEMENTS'),
								gc.getInfoTypeForString('BUILDING_PALACE_LUCHUIRP'),
								gc.getInfoTypeForString('BUILDING_PALACE_KHAZAD')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED'),
								gc.getInfoTypeForString('BUILDING_HUNTING_LODGE'),
								gc.getInfoTypeForString('BUILDING_HERBALIST'),
								gc.getInfoTypeForString('BUILDING_SCION_OF_YGGDRASIL'),
								gc.getInfoTypeForString('BUILDING_PALACE_LJOSALFAR')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_HARBOR'),
								gc.getInfoTypeForString('BUILDING_HARBOR_LANUN'),
								gc.getInfoTypeForString('BUILDING_LIGHTHOUSE'),
								gc.getInfoTypeForString('BUILDING_GREAT_LIGHTHOUSE'),
								gc.getInfoTypeForString('BUILDING_PALACE_LANUN'),
								gc.getInfoTypeForString('BUILDING_PALACE_BALSERAPHS')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_HUNTING_LODGE'),
								gc.getInfoTypeForString('BUILDING_GOVERNORS_MANOR'),
								gc.getInfoTypeForString('BUILDING_PALACE_SVARTALFAR'),
								gc.getInfoTypeForString('BUILDING_EYES_AND_EARS_NETWORK')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_MAGE_GUILD'),
								gc.getInfoTypeForString('BUILDING_PLANAR_GATE'),
								gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED'),
								gc.getInfoTypeForString('BUILDING_TOWER_OF_NECROMANCY'),
								gc.getInfoTypeForString('BUILDING_PALACE_INFERNAL'),
								gc.getInfoTypeForString('BUILDING_INFERNAL_GRIMOIRE')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_WHITE_HAND') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_SMOKEHOUSE'),
								gc.getInfoTypeForString('BUILDING_TOWER_OF_THE_ELEMENTS'),
								gc.getInfoTypeForString('BUILDING_PALACE_ILLIANS')]:
				iCostMod /= 2

		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_MATRONAE') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_DWARVEN_SMITHY'),
								gc.getInfoTypeForString('BUILDING_FORGE'),
								gc.getInfoTypeForString('BUILDING_SHIPYARD'),
								gc.getInfoTypeForString('BUILDING_FANE_OF_FATE'),
								gc.getInfoTypeForString('BUILDING_DOCKS_OF_DREAMS'),
								gc.getInfoTypeForString('BUILDING_FOUNDRY_OF_VENGEANCE')]:
				iCostMod /= 2

		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_UNBLEMISHED') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_HERBALIST'),
								gc.getInfoTypeForString('BUILDING_INFIRMARY'),
								# gc.getInfoTypeForString('BUILDING_TEMPLE_UNBLEMISHED'),
								gc.getInfoTypeForString('BUILDING_AQUAE_SUCELLUS'),
								gc.getInfoTypeForString('BUILDING_SCION_OF_YGGDRASIL')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_CHANCEL_OF_GUARDIANS'),
								gc.getInfoTypeForString('BUILDING_PALACE_ELOHIM'),
								gc.getInfoTypeForString('BUILDING_SHRINE_OF_SIRONA')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_LAERAN_CORD') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_MAGE_GUILD'),
								gc.getInfoTypeForString('BUILDING_LIBRARY'),
								gc.getInfoTypeForString('BUILDING_ACADEMY'),
								gc.getInfoTypeForString('BUILDING_GREAT_LIBRARY'),
								gc.getInfoTypeForString('BUILDING_PALACE_AMURITES'),
								gc.getInfoTypeForString('BUILDING_CROWN_OF_AKHARIEN')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_FOXMEN') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_CARNIVAL'),
								gc.getInfoTypeForString('BUILDING_STABLE'),
								gc.getInfoTypeForString('BUILDING_ADVENTURERS_GUILD'),
								gc.getInfoTypeForString('BUILDING_HUNTING_LODGE'),
								gc.getInfoTypeForString('BUILDING_TAVERN'),
								gc.getInfoTypeForString('BUILDING_TAVERN_GRIGORI'),
								gc.getInfoTypeForString('BUILDING_INN'),
								gc.getInfoTypeForString('BUILDING_TOWER_OF_THE_ELEMENTS'),
								gc.getInfoTypeForString('BUILDING_SLYPH_SEARCH'),
								gc.getInfoTypeForString('BUILDING_PALACE_HIPPUS')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_MONEYCHANGER'),
								gc.getInfoTypeForString('BUILDING_TAX_OFFICE'),
								gc.getInfoTypeForString('BUILDING_PALACE_BALSERAPHS'),
								gc.getInfoTypeForString('BUILDING_GUILD_OF_THE_NINE'),
								gc.getInfoTypeForString('BUILDING_SMUGGLERS_PORT'),
								gc.getInfoTypeForString('BUILDING_MARKET'),
								gc.getInfoTypeForString('BUILDING_BAZAAR_OF_MAMMON')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_COVEN') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_OBSIDIAN_GATE'),
								gc.getInfoTypeForString('BUILDING_PLANAR_GATE'),
								gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED'),
								gc.getInfoTypeForString('BUILDING_PROPHECY_OF_RAGNAROK'),
								gc.getInfoTypeForString('BUILDING_PALACE_SHEAIM'),
								gc.getInfoTypeForString('BUILDING_THE_NEXUS')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_ANOINTED') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_HUNTING_LODGE'),
								gc.getInfoTypeForString('BUILDING_GOVERNORS_MANOR'),
								gc.getInfoTypeForString('BUILDING_DUNGEON'),
								gc.getInfoTypeForString('BUILDING_PALACE_CALABIM'),
								gc.getInfoTypeForString('BUILDING_PILLAR_OF_CHAINS'),
								gc.getInfoTypeForString('BUILDING_SCHOOL_OF_SADISM')]:
				iCostMod /= 2


		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_HOUSE_OF_PLENTY') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_CARNIVAL'),
								gc.getInfoTypeForString('BUILDING_TAVERN'),
								gc.getInfoTypeForString('BUILDING_TAVERN_GRIGORI'),
								gc.getInfoTypeForString('BUILDING_INN'),
								gc.getInfoTypeForString('BUILDING_TOWER_OF_DIVINATION'),
								gc.getInfoTypeForString('BUILDING_MUSEUM_OF_MAPONOS'),
								gc.getInfoTypeForString('BUILDING_PALACE_KURIOTATES')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_EMBER_LEGION') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_FORGE'),
								gc.getInfoTypeForString('BUILDING_FOUNDRY_OF_VENGEANCE'),
								# gc.getInfoTypeForString('BUILDING_TOPHET'),
								gc.getInfoTypeForString('BUILDING_TOWER_OF_THE_ELEMENTS'),
								gc.getInfoTypeForString('BUILDING_MUSEUM_OF_MAPONOS'),
								gc.getInfoTypeForString('BUILDING_PALACE_CLAN_OF_EMBERS'),
								gc.getInfoTypeForString('BUILDING_WYRMHOLD')]:
				iCostMod /= 2

		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_TOMB_OF_ARAWN'),
								gc.getInfoTypeForString('BUILDING_FANE_OF_FATE'),
								gc.getInfoTypeForString('BUILDING_COUNCIL_OF_ANCIENTS'),
								gc.getInfoTypeForString('BUILDING_SOUL_SHROUD'),
								gc.getInfoTypeForString('BUILDING_PALACE_SIDAR')]:
				iCostMod /= 2
		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_TRAINING_YARD'),
								gc.getInfoTypeForString('BUILDING_HUNTING_LODGE'),
								gc.getInfoTypeForString('BUILDING_RIDE_OF_THE_NINE_KINGS'),
								gc.getInfoTypeForString('BUILDING_FORM_OF_THE_TITAN'),
								gc.getInfoTypeForString('BUILDING_HIPPODROME'),
								gc.getInfoTypeForString('BUILDING_PALACE_DOVIELLO'),
								gc.getInfoTypeForString('BUILDING_SANGUINE_FOUNTAIN')]:
				iCostMod /= 2

		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_RINGGIVER') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_GUILD_OF_HAMMERS'),
								gc.getInfoTypeForString('BUILDING_SCULPTORS_STUDIO'),
								gc.getInfoTypeForString('BUILDING_FORM_OF_THE_TITAN'),
								gc.getInfoTypeForString('BUILDING_ADULARIA_CHAMBER'),
								gc.getInfoTypeForString('BUILDING_BLASTING_WORKSHOP'),
								gc.getInfoTypeForString('BUILDING_GOLEM_TRACKS'),
								gc.getInfoTypeForString('BUILDING_PALLENS_ENGINE'),
								gc.getInfoTypeForString('BUILDING_PALACE_LUCHUIRP')]:
				iCostMod /= 2

		if pCity.isHasReligion( gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON') ):
			if iBuilding in [	gc.getInfoTypeForString('BUILDING_BONE_PALACE'),
								gc.getInfoTypeForString('BUILDING_PALACE_KURIOTATES'),
								gc.getInfoTypeForString('BUILDING_PALACE_SHEAIM')]:
				iCostMod /= 2




		if iBuilding == gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE'):
			if PyPlayer(iPlayer).isVotePassed( gc.getInfoTypeForString( "VOTE_GAMBLING_RING" ) ) :
				iCostMod /= 2

		if iBuilding == gc.getInfoTypeForString('BUILDING_MERCURIAN_GATE'):
			iAV = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
			iCostMod -= gc.getGame().calculateReligionPercent(iAV)

			iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
			iEvil = gc.getInfoTypeForString('ALIGNMENT_EVIL')
			lMana = [	gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
					gc.getInfoTypeForString('BONUS_MANA_DEATH'),
					gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'),
					gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),]
			iTeam = pPlayer.getTeam()
			eTeam = gc.getTeam(iTeam)
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive():
					iLoopTeam = pLoopPlayer.getTeam()
					if eTeam.isAtWar(iLoopTeam):
						if pLoopPlayer.getCivilizationType() == iInfernal:
							iCostMod -= 10
						elif pLoopPlayer.getStateReligion() == iAV:
							iCostMod -= 5
						elif pLoopPlayer.getAlignment() == iEvil:
							iCostMod -= 2
						for iMana in lMana:
							iCostMod -= pLoopPlayer.getNumAvailableBonuses(iMana)
					elif iTeam == iLoopTeam or eTeam.isVassal(iTeam):
						if pLoopPlayer.getCivilizationType() == iInfernal:
							iCostMod += 10
						elif pLoopPlayer.getStateReligion() == iAV:
							iCostMod += 5
						elif pLoopPlayer.getAlignment() == iEvil:
							iCostMod += 2
						for iMana in lMana:
							iCostMod += pLoopPlayer.getNumAvailableBonuses(iMana)
			iCostMod = max(5, iCostMod)
		return iCostMod

	def canUpgradeAnywhere(self, argsList):
		pUnit = argsList
		bCanUpgradeAnywhere = 0
		return bCanUpgradeAnywhere

	def getWidgetHelp(self, argsList):
		eWidgetType, iData1, iData2, bOption = argsList
## Religion Screen ##
		if eWidgetType == WidgetTypes.WIDGET_HELP_RELIGION:
			if iData1 == -1:
				return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
## Platy WorldBuilder ##
		elif eWidgetType == WidgetTypes.WIDGET_PYTHON:
			if iData1 == 1027:
				return CyTranslator().getText("TXT_KEY_WB_PLOT_DATA",())
			elif iData1 == 1028:
				return gc.getGameOptionInfo(iData2).getHelp()
			elif iData1 == 1029:
				if iData2 == 0:
					sText = CyTranslator().getText("TXT_KEY_WB_PYTHON", ())
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onFirstContact"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onChangeWar"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onVassalState"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCityAcquired"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCityBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCultureExpansion"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onGoldenAge"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onEndGoldenAge"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onGreatPersonBorn"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onPlayerChangeStateReligion"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionFounded"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionSpread"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionRemove"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationFounded"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationSpread"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationRemove"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitCreated"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitLost"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitPromoted"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onBuildingBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onProjectBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onTechAcquired"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onImprovementBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onImprovementDestroyed"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onRouteBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onPlotRevealed"
					return sText
				elif iData2 == 1:
					return CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA",())
				elif iData2 == 2:
					return CyTranslator().getText("TXT_KEY_WB_TEAM_DATA",())
				elif iData2 == 3:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH",())
				elif iData2 == 4:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT",())
				elif iData2 == 5:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ())
				elif iData2 == 6:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION",())
				elif iData2 == 7:
					return CyTranslator().getText("TXT_KEY_WB_CITY_DATA2",())
				elif iData2 == 8:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING",())
				elif iData2 == 9:
					return CvModName.getName() + '\nVersion: ' + CvModName.getVersion() + "\nPlaty Builder\nVersion: 4.17b"
				elif iData2 == 10:
					return CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS",())
				elif iData2 == 11:
					return CyTranslator().getText("TXT_KEY_WB_RIVER_PLACEMENT",())
				elif iData2 == 12:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT",())
				elif iData2 == 13:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS",())
				elif iData2 == 14:
					return CyTranslator().getText("TXT_KEY_WB_PLOT_TYPE",())
				elif iData2 == 15:
					return CyTranslator().getText("TXT_KEY_CONCEPT_TERRAIN",())
				elif iData2 == 16:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_ROUTE",())
				elif iData2 == 17:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_FEATURE",())
				elif iData2 == 18:
					return CyTranslator().getText("TXT_KEY_MISSION_BUILD_CITY",())
				elif iData2 == 19:
					return CyTranslator().getText("TXT_KEY_WB_ADD_BUILDINGS",())
				elif iData2 == 20:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION",())
				elif iData2 == 21:
					return CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS",())
				elif iData2 == 22:
					return CyTranslator().getText("TXT_KEY_ESPIONAGE_CULTURE",())
				elif iData2 == 23:
					return CyTranslator().getText("TXT_KEY_PITBOSS_GAME_OPTIONS",())
				elif iData2 == 24:
					return CyTranslator().getText("TXT_KEY_WB_SENSIBILITY",())
				elif iData2 == 27:
					return CyTranslator().getText("TXT_KEY_WB_ADD_UNITS",())
				elif iData2 == 28:
					return CyTranslator().getText("TXT_KEY_WB_TERRITORY",())
				elif iData2 == 29:
					return CyTranslator().getText("TXT_KEY_WB_ERASE_ALL_PLOTS",())
				elif iData2 == 30:
					return CyTranslator().getText("TXT_KEY_WB_REPEATABLE",())
				elif iData2 == 31:
					return CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ())
				elif iData2 == 32:
					return CyTranslator().getText("TXT_KEY_WB_STARTING_PLOT", ())
				elif iData2 == 33:
					return CyTranslator().getText("TXT_KEY_INFO_SCREEN", ())
				elif iData2 == 34:
					return CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ())
#Magister Start
				elif iData2 == 35:
					return CyTranslator().getText("TXT_KEY_WB_REAL",())
#Magister Stop
			elif iData1 > 1029 and iData1 < 1040:
				if iData1 %2:
					return "-"
				return "+"
			elif iData1 == 1041:
				return CyTranslator().getText("TXT_KEY_WB_KILL",())
			elif iData1 == 1042:
				return CyTranslator().getText("TXT_KEY_MISSION_SKIP",())
			elif iData1 == 1043:
				if iData2 == 0:
					return CyTranslator().getText("TXT_KEY_WB_DONE",())
				elif iData2 == 1:
					return CyTranslator().getText("TXT_KEY_WB_FORTIFY",())
				elif iData2 == 2:
					return CyTranslator().getText("TXT_KEY_WB_WAIT",())
			elif iData1 == 6782:
				return CyGameTextMgr().parseCorporationInfo(iData2, False)
			elif iData1 == 6785:
				return CyGameTextMgr().getProjectHelp(iData2, False, CyCity())
			elif iData1 == 6787:
				return gc.getProcessInfo(iData2).getDescription()
			elif iData1 == 6788:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return gc.getRouteInfo(iData2).getDescription()
## City Hover Text ##
			elif iData1 > 7199 and iData1 < 7300:
				iPlayer = iData1 - 7200
				pPlayer = gc.getPlayer(iPlayer)
				pCity = pPlayer.getCity(iData2)
				if CyGame().GetWorldBuilderMode():
					sText = "<font=3>"
					if pCity.isCapital():
						sText += CyTranslator().getText("[ICON_STAR]", ())
					elif pCity.isGovernmentCenter():
						sText += CyTranslator().getText("[ICON_SILVER_STAR]", ())
					sText += u"%s: %d<font=2>" %(pCity.getName(), pCity.getPopulation())
					sTemp = ""
					if pCity.isConnectedToCapital(iPlayer):
						sTemp += CyTranslator().getText("[ICON_TRADE]", ())
					for i in xrange(gc.getNumReligionInfos()):
						if pCity.isHolyCityByType(i):
							sTemp += u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
						elif pCity.isHasReligion(i):
							sTemp += u"%c" %(gc.getReligionInfo(i).getChar())

					for i in xrange(gc.getNumCorporationInfos()):
						if pCity.isHeadquartersByType(i):
							sTemp += u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
						elif pCity.isHasCorporation(i):
							sTemp += u"%c" %(gc.getCorporationInfo(i).getChar())
					if len(sTemp) > 0:
						sText += "\n" + sTemp

					iMaxDefense = pCity.getTotalDefense(False)
					if iMaxDefense > 0:
						sText += u"\n%s: " %(CyTranslator().getText("[ICON_DEFENSE]", ()))
						iCurrent = pCity.getDefenseModifier(False)
						if iCurrent != iMaxDefense:
							sText += u"%d/" %(iCurrent)
						sText += u"%d%%" %(iMaxDefense)

					sText += u"\n%s: %d/%d" %(CyTranslator().getText("[ICON_FOOD]", ()), pCity.getFood(), pCity.growthThreshold())
					iFoodGrowth = pCity.foodDifference(True)
					if iFoodGrowth != 0:
						sText += u" %+d" %(iFoodGrowth)

					if pCity.isProduction():
						sText += u"\n%s:" %(CyTranslator().getText("[ICON_PRODUCTION]", ()))
						if not pCity.isProductionProcess():
							sText += u" %d/%d" %(pCity.getProduction(), pCity.getProductionNeeded())
							iProduction = pCity.getCurrentProductionDifference(False, True)
							if iProduction != 0:
								sText += u" %+d" %(iProduction)
						sText += u" (%s)" %(pCity.getProductionName())

					iGPRate = pCity.getGreatPeopleRate()
					iProgress = pCity.getGreatPeopleProgress()
					if iGPRate > 0 or iProgress > 0:
						sText += u"\n%s: %d/%d %+d" %(CyTranslator().getText("[ICON_GREATPEOPLE]", ()), iProgress, pPlayer.greatPeopleThreshold(False), iGPRate)

					sText += u"\n%s: %d/%d (%s)" %(CyTranslator().getText("[ICON_CULTURE]", ()), pCity.getCulture(iPlayer), pCity.getCultureThreshold(), gc.getCultureLevelInfo(pCity.getCultureLevel()).getDescription())

					lTemp = []
					for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
						iAmount = pCity.getCommerceRateTimes100(i)
						if iAmount <= 0: continue
						sTemp = u"%d.%02d%c" %(pCity.getCommerceRate(i), pCity.getCommerceRateTimes100(i)%100, gc.getCommerceInfo(i).getChar())
						lTemp.append(sTemp)
					if len(lTemp) > 0:
						sText += "\n"
						for i in xrange(len(lTemp)):
							sText += lTemp[i]
							if i < len(lTemp) - 1:
								sText += ", "

					iMaintenance = pCity.getMaintenanceTimes100()
					if iMaintenance != 0:
						sText += "\n" + CyTranslator().getText("[COLOR_WARNING_TEXT]", ()) + CyTranslator().getText("INTERFACE_CITY_MAINTENANCE", ()) + " </color>"
						sText += u"-%d.%02d%c" %(iMaintenance/100, iMaintenance%100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

#Magister Start
					iRevIndex = pCity.getRevolutionIndex()
					if iRevIndex != 0:
						sText += "\n" + CyTranslator().getText("TXT_KEY_WB_REV_INDEX", (iRevIndex,))

					sText += "\n" + "X: " + str(pCity.getX()) + ", Y: " + str(pCity.getY())
					sText += "\n" + CyTranslator().getText("TXT_KEY_WB_AREA_ID", ()) + ": " + str(pCity.plot().getArea())
#Magister Stop

					lBuildings = []
					lWonders = []
					for i in xrange(gc.getNumBuildingInfos()):
						if pCity.isHasBuilding(i):
							Info = gc.getBuildingInfo(i)
							if isLimitedWonderClass(Info.getBuildingClassType()):
								lWonders.append(Info.getDescription())
							else:
								lBuildings.append(Info.getDescription())
					if len(lBuildings) > 0:
						lBuildings.sort()
						sText += "\n" + CyTranslator().getText("[COLOR_BUILDING_TEXT]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()) + ": </color>"
						for i in xrange(len(lBuildings)):
							sText += lBuildings[i]
							if i < len(lBuildings) - 1:
								sText += ", "
					if len(lWonders) > 0:
						lWonders.sort()
						sText += "\n" + CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()) + ": </color>"
						for i in xrange(len(lWonders)):
							sText += lWonders[i]
							if i < len(lWonders) - 1:
								sText += ", "
					sText += "</font>"
					return sText
## Religion Widget Text##
			elif iData1 == 7869:
				return CyGameTextMgr().parseReligionInfo(iData2, False)
## Building Widget Text##
			elif iData1 == 7870:
				return CyGameTextMgr().getBuildingHelp(iData2, False, False, False, None)
## Tech Widget Text##
			elif iData1 == 7871:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return CyGameTextMgr().getTechHelp(iData2, False, False, False, False, -1)
## Civilization Widget Text##
			elif iData1 == 7872:
				iCiv = iData2 % 10000
				return CyGameTextMgr().parseCivInfos(iCiv, False)
## Promotion Widget Text##
			elif iData1 == 7873:
				return CyGameTextMgr().getPromotionHelp(iData2, False)
## Feature Widget Text##
			elif iData1 == 7874:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				iFeature = iData2 % 10000
				return CyGameTextMgr().getFeatureHelp(iFeature, False)
## Terrain Widget Text##
			elif iData1 == 7875:
				return CyGameTextMgr().getTerrainHelp(iData2, False)
## Leader Widget Text##
			elif iData1 == 7876:
				iLeader = iData2 % 10000
				return CyGameTextMgr().parseLeaderTraits(iLeader, -1, False, False)
## Improvement Widget Text##
			elif iData1 == 7877:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return CyGameTextMgr().getImprovementHelp(iData2, False)
## Bonus Widget Text##
			elif iData1 == 7878:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return CyGameTextMgr().getBonusHelp(iData2, False)
## Specialist Widget Text##
			elif iData1 == 7879:
				return CyGameTextMgr().getSpecialistHelp(iData2, False)
## Yield Text##
			elif iData1 == 7880:
				return gc.getYieldInfo(iData2).getDescription()
## Commerce Text##
			elif iData1 == 7881:
				return gc.getCommerceInfo(iData2).getDescription()
## Build Text##
			elif iData1 == 7882:
				return gc.getBuildInfo(iData2).getDescription()
## Corporation Screen ##
			elif iData1 == 8201:
				return CyGameTextMgr().parseCorporationInfo(iData2, False)
## Military Screen ##
			elif iData1 == 8202:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_PEDIA_ALL_UNITS", ())
				return CyGameTextMgr().getUnitHelp(iData2, False, False, False, None)
			elif iData1 > 8299 and iData1 < 8400:
				iPlayer = iData1 - 8300
				pUnit = gc.getPlayer(iPlayer).getUnit(iData2)
				if pUnit != -1:
					sText = CyGameTextMgr().getSpecificUnitHelp(pUnit, True, False)
					if CyGame().GetWorldBuilderMode():
#Magister Start
						i = pUnit.getScenarioCounter()
						if -1 < i < gc.getNumUnitInfos():
							if i != pUnit.getUnitType():
								sText += "\n" + CyTranslator().getText("TXT_KEY_WB_SCENARIO_COUNTER_UNIT", ()) + ": " + gc.getUnitInfo(i).getDescription()

						if pUnit.isHasCasted():
							sText += "\n" + CyTranslator().getText("TXT_KEY_UNIT_HAS_CASTED", ())

						i = pUnit.getSummoner()
						if i > 0:
							pPlayer = gc.getPlayer(pUnit.getOwner())
							pSummoner = pPlayer.getUnit(i)
							if not pSummoner.isNone():
								sText += "\n" + CyTranslator().getText("TXT_KEY_WB_SUMMONER", ()) + ": " + pSummoner.getName()
								sText += "\n" + CyTranslator().getText("TXT_KEY_WB_SUMMONER", ()) + " ID: " + str(i)

						if pUnit.isPermanentSummon():
							sText += "\n" + CyTranslator().getText("TXT_KEY_WB_IS_PERMANENT_SUMMON", ())

						i = pUnit.getDuration()
						if i > 0:
							sText += "\n" + CyTranslator().getText("TXT_KEY_WB_DURATION", ()) + ": " + str(i)

						i = pUnit.getImmobileTimer()
						if i > 0:
							sText += "\n" + CyTranslator().getText("TXT_KEY_WB_IMMOBILE_TIMER", ()) + ": " + str(i)

						i = pUnit.getFortifyTurns()
						if i > 0:
							sText += "\n" + CyTranslator().getText("TXT_KEY_WB_FORTIFY_TURNS", ()) + ": " + str(i)
#Magister Stop
						sText += "\n" + CyTranslator().getText("TXT_KEY_WB_UNIT", ()) + " ID: " + str(iData2)
						sText += "\n" + CyTranslator().getText("TXT_KEY_WB_GROUP", ()) + " ID: " + str(pUnit.getGroupID())
						sText += "\n" + "X: " + str(pUnit.getX()) + ", Y: " + str(pUnit.getY())
						sText += "\n" + CyTranslator().getText("TXT_KEY_WB_AREA_ID", ()) + ": " + str(pUnit.plot().getArea())
					return sText
## Civics Screen ##
			elif iData1 == 8205 or iData1 == 8206:
				sText = CyGameTextMgr().parseCivicInfo(iData2, False, True, False)
				if gc.getCivicInfo(iData2).getUpkeep() > -1:
					sText += "\n" + gc.getUpkeepInfo(gc.getCivicInfo(iData2).getUpkeep()).getDescription()
				else:
					sText += "\n" + CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
				return sText
#Magister Start
			elif iData1 == 9000:
				return CyGameTextMgr().parseTraits(iData2, CivilizationTypes.NO_CIVILIZATION, False )
			elif iData1 == 9001:
				return CyGameTextMgr().getSpellHelp(iData2, False)
			elif iData1 == 9002:
				return CyTranslator().getText("TXT_KEY_WB_TOGGLE",()) + CyTranslator().getText("TXT_KEY_WB_HAS_CAST",())
			elif iData1 == 9003:
				if iData2 == 0:
					return CyTranslator().getText("TXT_KEY_WB_CAN_CAST",())
				elif iData2 == 1:
					return CyTranslator().getText("TXT_KEY_WB_HAS_CAST",())
#Magister Stop
## Ultrapack ##
		return u""

	def getUpgradePriceOverride(self, argsList):
		iPlayer, iUnitID, iUnitTypeUpgrade = argsList
		return -1	# Any value 0 or above will be used

	def getExperienceNeeded(self, argsList):
		# use this function to set how much experience a unit needs
		iLevel, iOwner = argsList
		# regular epic game experience
		iExperienceNeeded = iLevel * iLevel + 1
		iModifier = gc.getPlayer(iOwner).getLevelExperienceModifier()
		if 0 != iModifier:
			iExperienceNeeded += (iExperienceNeeded * iModifier + 99) / 100  # ROUND UP
		return iExperienceNeeded

##--------	Unofficial Bug Fix: Added by Denev 2009/12/31
	# TODO: This should not be a callback, but an event
	def applyBuildEffects(self, argsList):
		pUnit, pCity = argsList
		iUnit = pUnit.getUnitType()

		iWeaponTier = gc.getUnitInfo(pUnit.getUnitType()).getWeaponTier()
		if iWeaponTier >= 3 and pCity.hasBonus(gc.getInfoTypeForString ('BONUS_MITHRIL')):
			pUnit.setHasPromotion(gc.getInfoTypeForString ('PROMOTION_MITHRIL_WEAPONS'), True)
		elif iWeaponTier >= 2 and pCity.hasBonus(gc.getInfoTypeForString ('BONUS_IRON')):
			pUnit.setHasPromotion(gc.getInfoTypeForString ('PROMOTION_IRON_WEAPONS'), True)
		elif iWeaponTier >= 1 and pCity.hasBonus(gc.getInfoTypeForString ('BONUS_COPPER')):
			pUnit.setHasPromotion(gc.getInfoTypeForString ('PROMOTION_BRONZE_WEAPONS'), True)

		iRace = pUnit.getRace()
		if -1 < iRace < gc.getNumPromotionInfos():
			if pUnit.isAlive() and not iRace in [gc.getInfoTypeForString('PROMOTION_CENTAUR'),gc.getInfoTypeForString('PROMOTION_SERPENTINE'),gc.getInfoTypeForString('PROMOTION_MUSTEVAL')]:
##			if pUnit.isAlive():#I don't want Angels or especially Manes to be given living races. Statius's manes could return as manes when they die
				if not gc.getUnitInfo(iUnit).getFreePromotions(iRace):
		##			iPlayer = pUnit.getOwner()
					iPlayer = pCity.getOwner()
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_TOLERANT')):
						iCiv = pPlayer.getCivilizationType()
						infoCiv = gc.getCivilizationInfo(iCiv)
						iDefaultRace = infoCiv.getDefaultRace()


						iKuriotates = gc.getInfoTypeForString('CIVILIZATION_KURIOTATES')
						if iCiv == iKuriotates:
							if iUnit in [	gc.getInfoTypeForString('UNIT_ADEPT'),
										gc.getInfoTypeForString('UNIT_MAGE'),
										gc.getInfoTypeForString('UNIT_ARCHMAGE')]:
								iDefaultRace = gc.getInfoTypeForString('PROMOTION_SERPENTINE')
							elif iUnit in [	gc.getInfoTypeForString('UNIT_ASSASSIN'),
											gc.getInfoTypeForString('UNIT_BEASTMASTER'),
											gc.getInfoTypeForString('UNIT_HUNTER'),
											gc.getInfoTypeForString('UNIT_RANGER'),
											gc.getInfoTypeForString('UNIT_SCOUT'),
											gc.getInfoTypeForString('UNIT_SHADOW')
											]:
								iDefaultRace = gc.getInfoTypeForString('PROMOTION_MUSTEVAL')


						if iDefaultRace !=-1 and iRace == iDefaultRace:
							if not isWorldUnitClass(pUnit.getUnitClassType()):
								listRaces = [-1]
								jCult = pCity.calculateCulturePercent(iPlayer)
								if jCult < 100:
									pUnit.setHasPromotion(iDefaultRace, False)
									listCivType = [iCiv]
									for jPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
										jCult = pCity.calculateCulturePercent(jPlayer)
										if jCult > 0:
											pjPlayer = gc.getPlayer(jPlayer)
											jCiv = pjPlayer.getCivilizationType()
											jCivInfo = gc.getCivilizationInfo(jCiv)
											jRace = jCivInfo.getDefaultRace()
											for i in xrange(jCult):
												listRaces.append(jRace)
									jCiv = listCivType.pop(CyGame().getSorenRandNum(len(listCivType), "Racial Diversity-applyBuildEffects"))
									if jCiv != -1:
										jCivInfo = gc.getCivilizationInfo(jCiv)
										jRace = jCivInfo.getDefaultRace()

										if jCiv == iKuriotates:
											if iUnit in [	gc.getInfoTypeForString('UNIT_ADEPT'),
														gc.getInfoTypeForString('UNIT_MAGE'),
														gc.getInfoTypeForString('UNIT_ARCHMAGE')]:
												jRace = gc.getInfoTypeForString('PROMOTION_SERPENTINE')
											elif iUnit in [	gc.getInfoTypeForString('UNIT_ASSASSIN'),
															gc.getInfoTypeForString('UNIT_BEASTMASTER'),
															gc.getInfoTypeForString('UNIT_HUNTER'),
															gc.getInfoTypeForString('UNIT_RANGER'),
															gc.getInfoTypeForString('UNIT_SCOUT'),
															gc.getInfoTypeForString('UNIT_SHADOW')
															]:
												jRace = gc.getInfoTypeForString('PROMOTION_MUSTEVAL')


										if jRace != -1:
											pUnit.setHasPromotion(jRace, True)

##						if iDefaultRace !=-1 and iRace == iDefaultRace:
##							if not isWorldUnitClass(pUnit.getUnitClassType()):
##								jCult = pCity.calculateCulturePercent(iPlayer)
##								if jCult < 100:
##									pUnit.setHasPromotion(iDefaultRace, False)
##									listRaces = [-1]
##									for jPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
##										jCult = pCity.calculateCulturePercent(jPlayer)
##										if jCult > 0:
##											pjPlayer = gc.getPlayer(jPlayer)
##											jCiv = pjPlayer.getCivilizationType()
##											jCivInfo = gc.getCivilizationInfo(jCiv)
##											jRace = jCivInfo.getDefaultRace()
##											for i in xrange(jCult):
##												listRaces.append(jRace)
##									iRace = listRaces.pop(CyGame().getSorenRandNum(len(listRaces), "Racial Diversity-applyBuildEffects"))
##									if iRace != -1:
##										pUnit.setHasPromotion(iRace, True)

		if iRace == gc.getInfoTypeForString('PROMOTION_DWARF'):
			pUnit.changeExperience(pCity.getNumBonuses(gc.getInfoTypeForString ('BONUS_ALE')), -1, False, False, False)

		elif iRace == gc.getInfoTypeForString('PROMOTION_DEMON'):
			if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')) > 0:
				pUnit.changeExperience(2, -1, False, False, False)

		elif iRace == gc.getInfoTypeForString('PROMOTION_GOLEM'):
			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_ADULARIA_CHAMBER')) > 0:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STEALTH'), True)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN'), True)
			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_BLASTING_WORKSHOP')) > 0:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE2'), True)
##			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_DWARVEN_SMITHY')) > 0:
##				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), True)
			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_GOLEM_TRACKS')) > 0:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOBILITY2'), True)
			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_PALLENS_ENGINE')) > 0:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PERFECT_SIGHT'), True)
			if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TOWER_OF_ALTERATION')) > 0:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), True)


		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_CHANCEL_OF_GUARDIANS')) > 0:
			if not pUnit.noDefensiveBonus() and pUnit.baseCombatStrDefense() > 0:
				if CyGame().getSorenRandNum(100, "Chancel of Guardians") < 20:
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEFENSIVE'), True)
					
		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TOPHET')) > 0:
			if CyGame().getSorenRandNum(100, "Tophet") < 20:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE_RESISTANCE'), True)



		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS_HOSTILE')) > 0:
			if pUnit.isAlive():
				if not isWorldUnitClass(pUnit.getUnitClassType()):
					if CyGame().getSorenRandNum(100, "Asylum") < 10:
						pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)


	def AI_MageTurn(self, argsList):
		"""
			Returns 0 if we couldn't find anything to do.
			Returns 1 if we did something, or pushed some mission, or are out of moves
		"""
		pUnit = argsList[0] # type: CyUnit
		pUnitPlot = pUnit.plot()
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iCiv = pPlayer.getCivilizationType()

		if pUnit.getUnitAIType() == gc.getInfoTypeForString('UNITAI_TERRAFORMER'):
			# LFGR_TODO: Automated units may attack (probably while moving)

			# TERRAFORMING 03/2021 lfgr: Refactored and tweaked

			# Useful constants
			eSpellSpring = gc.getInfoTypeForString('SPELL_SPRING')
			eSpellSpringG = gc.getInfoTypeForString('SPELL_SPRING_GREATER')
			eSpellVitalize = gc.getInfoTypeForString('SPELL_VITALIZE')
			eSpellScorch = gc.getInfoTypeForString('SPELL_SCORCH')
			eSpellScorchG = gc.getInfoTypeForString('SPELL_SCORCH_GREATER')
			eSpellSanctify = gc.getInfoTypeForString('SPELL_SANCTIFY')
			eSpellSanctifyG = gc.getInfoTypeForString('SPELL_SANCTIFY_GREATER')
			eSpellBloom = gc.getInfoTypeForString('SPELL_BLOOM')
			eSpellBloom2 = gc.getInfoTypeForString('SPELL_BLOOM2')
			eSpellBloom3 = gc.getInfoTypeForString('SPELL_BLOOM3')
			eSpellBloomG = gc.getInfoTypeForString('SPELL_BLOOM_GREATER')
			eSpellBloom2G = gc.getInfoTypeForString('SPELL_BLOOM2_GREATER')
			eSpellBloom3G = gc.getInfoTypeForString('SPELL_BLOOM3_GREATER')

			eDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
			eMarsh = gc.getInfoTypeForString('TERRAIN_MARSH')
			eGrass = gc.getInfoTypeForString('TERRAIN_GRASS')
			ePlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
			eSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
			eTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
			eFlood = gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')
			eSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
			eBloomForest = gc.getSpellInfo( eSpellBloom ).getCreateFeatureType()
			assert eBloomForest != -1
			eBloomForest2 = gc.getSpellInfo( eSpellBloom2 ).getCreateFeatureType()
			assert eBloomForest2 != -1
			eBloomForest3 = gc.getSpellInfo( eSpellBloom3 ).getCreateFeatureType()
			assert eBloomForest3 != -1

			bIllians = iCiv == gc.getInfoTypeForString( "CIVILIZATION_ILLIANS" )
			bInfernal = iCiv == gc.getInfoTypeForString( "CIVILIZATION_INFERNAL" )
			bFoL = pPlayer.getStateReligion() == gc.getInfoTypeForString( "RELIGION_FELLOWSHIP_OF_LEAVES" )
			bMaintainBloomForest = gc.getCivilizationInfo( iCiv ).isMaintainFeatures( eBloomForest )

			# Catch leftover priests
			if not pPlayer.isHuman() :
				if pUnit.isHasPromotion( gc.getInfoTypeForString( "PROMOTION_MEDIC2" ) ) :
					pUnit.setUnitAIType(gc.getInfoTypeForString('UNITAI_MEDIC'))
					return 0

			# Can cast cache
			# LFGR_TODO: This really should be cached in the DLL anyway
			debCanCastWCP = {} # type: Dict[int, bool]
			for eSpell in ( eSpellSpringG,eSpellSpring, eSpellVitalize, eSpellScorchG, eSpellScorch, eSpellSanctifyG, eSpellSanctify, eSpellBloom3G, eSpellBloom2G, eSpellBloomG, eSpellBloom3, eSpellBloom2, eSpellBloom) :
				debCanCastWCP[eSpell] = pUnit.canCastWithCurrentPromotions( eSpell )

			def iterSpellsForPlot( pPlot ) :
				# type: (CyPlot) -> Iterator[int]
				if pPlot.getOwner() == iPlayer:
					eTerrain = pPlot.getTerrainType()
					eFeature = pPlot.getFeatureType()
					eImprovement = pPlot.getImprovementType()
					eBonus = pPlot.getBonusType(-1)

					lBloomableImp =[	-1,
										gc.getInfoTypeForString('IMPROVEMENT_CAMP'),
										gc.getInfoTypeForString('IMPROVEMENT_LUMBERMILL'),
										gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES'),
										gc.getInfoTypeForString('IMPROVEMENT_YGGDRASIL'),
										gc.getInfoTypeForString('IMPROVEMENT_TOMB_OF_SUCELLUS'),
										gc.getInfoTypeForString('IMPROVEMENT_MANA_NATURE'),
										gc.getInfoTypeForString('IMPROVEMENT_MANA_CREATION'),
										gc.getInfoTypeForString('IMPROVEMENT_MANA_LIFE')
										]
					lBloomableBoni =[	-1,
										gc.getInfoTypeForString('BONUS_MANA_NATURE'),
										gc.getInfoTypeForString('BONUS_MANA_LIFE'),
										gc.getInfoTypeForString('BONUS_MANA_CREATION'),
										gc.getInfoTypeForString('BONUS_DEER'),
										gc.getInfoTypeForString('BONUS_FUR'),
										gc.getInfoTypeForString('BONUS_FRUIT_OF_YGGDRASIL'),
										gc.getInfoTypeForString('BONUS_IVORY')]

					if eImprovement == eSmoke or ( eTerrain == eDesert and eFeature != eFlood ) :
						yield eSpellSpringG
						yield eSpellSpring
					if eTerrain in (eDesert, eMarsh, ePlains, eTundra) or ( eTerrain == eSnow and not bIllians ) :
						yield eSpellVitalize
					if eTerrain == eMarsh or ( eTerrain == eSnow and not bIllians ) :
						yield eSpellScorchG
						yield eSpellScorch
					if pPlot.getPlotCounter() >= 10 and not bInfernal :
						yield eSpellSanctifyG
						yield eSpellSanctify


					if eFeature == -1 and pPlot.canHaveFeature( eBloomForest ) :
						if bMaintainBloomForest or ( eImprovement in lBloomableImp and eBonus in lBloomableBoni):
							yield eSpellBloomG # Can't bloom over improvements and don't want to bloom over boni or grass
							yield eSpellBloom # Can't bloom over improvements and don't want to bloom over boni or grass

					if eFeature in [gc.getInfoTypeForString('FEATURE_FOREST_NEW'),gc.getInfoTypeForString('FEATURE_FOREST_BURNT')]:
						if bMaintainBloomForest or ( eImprovement in lBloomableImp and eBonus in lBloomableBoni):

							yield eSpellBloom2G # Can't bloom over improvements and don't want to bloom over boni or grass
							yield eSpellBloom2 # Can't bloom over improvements and don't want to bloom over boni or grass

					if eFeature in [gc.getInfoTypeForString('FEATURE_FOREST'),gc.getInfoTypeForString('FEATURE_JUNGLE')]:
						if bMaintainBloomForest or ( eImprovement in lBloomableImp and eBonus in lBloomableBoni):

							yield eSpellBloom3G # Can't bloom over improvements and don't want to bloom over boni or grass
							yield eSpellBloom3 # Can't bloom over improvements and don't want to bloom over boni or grass


			def hasSpellForPlot( pPlot ) :
				for eSpell in iterSpellsForPlot( pPlot ) :
					if debCanCastWCP[eSpell] :
						return True
				return False
			
			# Try casting a spell!
			for eSpell in iterSpellsForPlot( pUnitPlot ) :
				if pUnit.canCast( eSpell, False ) :
					pUnit.cast( eSpell )

			if not pUnit.canMove() :
				pUnit.getGroup().pushMission( MissionTypes.MISSION_SKIP, -1, -1, 0, False,
					False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit )
				return 1

			TERRAFORM_SEARCH_DISTANCE = 3

			for iDist in range( 1, TERRAFORM_SEARCH_DISTANCE ) :
				lPlots = list( PyHelpers.PyPlot( pUnitPlot ).iterPlotsAtDistance( iDist ) )
				CvUtil.shuffleSequence( lPlots )
				for pPlot in lPlots :
					if pPlot.getOwner() != iPlayer : continue
					if pPlot.isImpassable() : continue
					if not pUnit.generatePath( pPlot, 0, False, None ) : continue
					if pPlot.isVisibleEnemyUnit( iPlayer ) : continue

					if hasSpellForPlot( pPlot ) :
						pUnit.getGroup().pushMission( MissionTypes.MISSION_MOVE_TO, pPlot.getX(), pPlot.getY(), 0, False,
							False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit )
						return 1

			# Nothing to do, lets move on to another City!
			iBestCount = 0
			pBestCity = None
			for pyCity in PyPlayer( iPlayer ).iterCities() :
				if pUnit.generatePath( pyCity.plot(), 0, True, None ) :
					iCount = 0 # Count number of terraformable plots
					# LFGR_TODO: Should create and expose CyCity.getNumCityPlots() (using ::calculateNumCityPlots())
					for iI in range( 1, pyCity.getNumCityPlots() ) :
						pPlot = pyCity.getCityIndexPlot( iI )
						if pPlot.isNone() : continue
						if pPlot.getOwner() != iPlayer : continue
						if pPlot.isImpassable() : continue
						if not pUnit.generatePath( pPlot, 0, False, None ) : continue
						if pPlot.isVisibleEnemyUnit( iPlayer ) : continue

						if hasSpellForPlot( pPlot ) :
							iCount += 1

					if iCount > 0 :
						if not pyCity.isSettlement() :
							iCount += 1000 # Always prefer non-settlements
						if iCount > iBestCount :
							pBestCity = pyCity
							iBestCount = iCount

			if pBestCity is not None :
				pCPlot = pBestCity.plot()
				iCX = pCPlot.getX()
				iCY = pCPlot.getY()
				if iCX != pUnit.getX() or iCY != pUnit.getY() :
					pUnit.getGroup().pushMission( MissionTypes.MISSION_MOVE_TO, iCX, iCY, 0, False, False,
						MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit )
					return 1

		return 0


	def AI_Mage_UPGRADE_MANA(self, argsList):
		pUnit = argsList[0]

#-----------------------------------
#UNITAI_MANA_UPGRADE
#Terraformer looks around for mana, changes UNITAI if he doesn't find some
#
# 1) Look for non raw mana and upgrade
# 2) Look for raw mana, decide how to upgrade, and do it!
# 3) Look for mana to dispel, and do it!
#-----------------------------------

		pPlot = pUnit.plot()
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		eTeam = gc.getTeam(pPlayer.getTeam())
		iX = pUnit.getX()
		iY = pUnit.getY()


		iRawMana = gc.getInfoTypeForString('BONUSCLASS_RAWMANA')
		iMana = gc.getInfoTypeForString('BONUSCLASS_MANA')
		lManasAlteration = [	gc.getInfoTypeForString('BONUS_MANA_BODY'),
					gc.getInfoTypeForString('BONUS_MANA_LIFE'),
					gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'),
					gc.getInfoTypeForString('BONUS_MANA_NATURE'),
					gc.getInfoTypeForString('BONUS_MANA_NATURE'),
					gc.getInfoTypeForString('BONUS_MANA_FORCE')
					]
		lManasDivination = [	gc.getInfoTypeForString('BONUS_MANA_LAW'),
					gc.getInfoTypeForString('BONUS_MANA_SUN'),
					gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
					gc.getInfoTypeForString('BONUS_MANA_MIND'),
					gc.getInfoTypeForString('BONUS_MANA_CREATION')
					]
		lManasElementalism = [	gc.getInfoTypeForString('BONUS_MANA_EARTH'),
					gc.getInfoTypeForString('BONUS_MANA_FIRE'),
					gc.getInfoTypeForString('BONUS_MANA_AIR'),
					gc.getInfoTypeForString('BONUS_MANA_WATER'),
					gc.getInfoTypeForString('BONUS_MANA_ICE')
					]
		lManasNecromancy = [	gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
					gc.getInfoTypeForString('BONUS_MANA_DEATH'),
					gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
					gc.getInfoTypeForString('BONUS_MANA_SHADOW'),
					gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')
					]
#Look for Mana to Dispel
		searchdistance=15

		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC2')):
			for isearch in range(1,searchdistance+1,1):
				for iiY in range(iY-isearch, iY+isearch, 1):
					for iiX in range(iX-isearch, iX+isearch, 1):
						pPlot2 = CyMap().plot(iiX,iiY)
						if pPlot2.isNone():continue
						if pPlot2.isImpassable():continue
						if pPlot2.isVisibleEnemyUnit(iPlayer):continue
						if pPlot2.getOwner() != iPlayer:continue
						iBonus = pPlot2.getBonusType(TeamTypes.NO_TEAM)
						if iBonus != -1:
							if gc.getBonusInfo(iBonus).getBonusClassType() == iMana:
								bDispel = True
								if pPlayer.getArcaneTowerVictoryFlag() == 0:
									if CyGame().getSorenRandNum(50, "Don't have to Dispel all the Time"):
										bDispel = False
								if pPlayer.getArcaneTowerVictoryFlag() == 1:
									if iBonus in lManasAlteration:
										if pPlayer.getNumAvailableBonuses(iBonus) == 1:
											bDispel = False
								if pPlayer.getArcaneTowerVictoryFlag() == 2:
									if iBonus in lManasDivination:
										if pPlayer.getNumAvailableBonuses(iBonus) == 1:
											bDispel = False
								if pPlayer.getArcaneTowerVictoryFlag() == 3:
									if iBonus in lManasNecromancy:
										if pPlayer.getNumAvailableBonuses(iBonus) == 1:
											bDispel = False
								if pPlayer.getArcaneTowerVictoryFlag() == 4:
									if iBonus in lManasElementalism:
										if pPlayer.getNumAvailableBonuses(iBonus) == 1:
											bDispel = False
								if bDispel:
									if pUnit.atPlot(pPlot2):
										if pUnit.canCast(gc.getInfoTypeForString('SPELL_DISPEL_MAGIC'),False):
											pUnit.cast(gc.getInfoTypeForString('SPELL_DISPEL_MAGIC'))
											return 1
									else:
#										CyInterface().addImmediateMessage('Searching for stuff to Dispel', "AS2D_NEW_ERA")
										pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
										return 1

#Dispel more if we seek Tower Victory Condition
			if pPlayer.getArcaneTowerVictoryFlag() > 0:
				iBestCount=0
				pBestCity=0
				for icity in range(pPlayer.getNumCities()):
					pCity = pPlayer.getCity(icity)
					if not pCity.isNone():
						iCount = 0
						for iI in range(1, 21):
							pPlot2 = pCity.getCityIndexPlot(iI)
							if pPlot2.isNone():continue
							if pPlot2.isImpassable():continue
							if pPlot2.isVisibleEnemyUnit(iPlayer):continue
							if pPlot2.getOwner() != iPlayer:continue
							iBonus = pPlot2.getBonusType(TeamTypes.NO_TEAM)
							if iBonus != -1:
								if gc.getBonusInfo(iBonus).getBonusClassType() in [iMana, iRawMana]:
									iCount += 1

						if iCount > iBestCount:
							pBestCity=pCity
							iBestCount=iCount
				if pBestCity != 0:
					pCPlot = pBestCity.plot()
					CX = pCPlot.getX()
					CY = pCPlot.getY()
					pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, CX, CY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
					return 1

#found no mana, return 2 so UNITAI is reset

		return 2

#returns the current flag for Tower Victory
	def AI_TowerMastery(self, argsList):
		ePlayer = argsList[0]
		flag = argsList[1]

		pPlayer = gc.getPlayer(ePlayer)
		eTeam = gc.getTeam(pPlayer.getTeam())

#		CyInterface().addImmediateMessage('This is AI_TowerMastery ', "AS2D_NEW_ERA")
#		CyInterface().addImmediateMessage('Flag is '+str(pPlayer.getArcaneTowerVictoryFlag()), "AS2D_NEW_ERA")

		if flag == 0:
#			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')) == False :
#				return 0
#			if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'))==0:
#				return 0

			iRawMana = gc.getInfoTypeForString('BONUSCLASS_RAWMANA')
			iMana = gc.getInfoTypeForString('BONUSCLASS_MANA')

			possiblemana=0
			for i in range (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.getOwner() == ePlayer:
					iBonus = pPlot.getBonusType(TeamTypes.NO_TEAM)
					if iBonus != -1:
						if gc.getBonusInfo(iBonus).getBonusClassType() in [iMana, iRawMana]:
							possiblemana += 1

			if possiblemana < 5:
				return 0

			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ALTERATION')):
				if eTeam.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_ALTERATION')) == 0:
					return 1

			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_DIVINATION')):
				if eTeam.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_DIVINATION')) == 0:
					return 2

			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_NECROMANCY')):
				if eTeam.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_NECROMANCY')) == 0:
					if not pPlayer.isCivic(CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_OVERCOUNCIL')):
						return 3

			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ELEMENTALISM')):
				if eTeam.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_THE_ELEMENTS')) == 0:
					return 4

		if flag==1:
			if eTeam.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_ALTERATION')) > 0:
				return 0
			else:
				return 1

		if flag==2:
			if eTeam.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_DIVINATION')) > 0:
				return 0
			else:
				return 2

		if flag==3:
			if eTeam.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_NECROMANCY')) > 0:
				return 0
			else:
				return 3

		if flag==4:
			if eTeam.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_THE_ELEMENTS')) > 0:
				return 0
			else:
				return 4

		return 0



