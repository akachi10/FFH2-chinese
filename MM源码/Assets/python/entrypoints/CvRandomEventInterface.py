# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
#
# CvRandomEventInterface.py
#
# These functions are App Entry Points from C++
# WARNING: These function names should not be changed
# WARNING: These functions can not be placed into a class
#
# No other modules should import this
#
import CvUtil
from CvPythonExtensions import *
import CustomFunctions
import PyHelpers

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer

def canTriggerAeronsChosen(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	if pUnit.getLevel() < 5:
		return False
	iMarksman = gc.getInfoTypeForString('PROMOTION_MARKSMAN')
	iAeronsChosen = gc.getInfoTypeForString('PROMOTION_OCCISOR')
	if pUnit.isHasPromotion(iAeronsChosen):
		return False
	if pUnit.getDuration():
		return False
	if pUnit.getSummoner() != -1:
		return False
	if not (pUnit.isHasPromotion(iMarksman) or pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRE')) or pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BURNING_BLOOD')) or pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENRAGED'))):
		return False
	if pUnit.getRace() in [gc.getInfoTypeForString('PROMOTION_ILLUSION'), gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION'), gc.getInfoTypeForString('PROMOTION_PUPPET')]:
		return False
	if cf.getNumBonusEffective(iPlayer, gc.getInfoTypeForString('BONUS_MANA_BODY'), pUnit) < 2:
		return False
	if gc.getInfoTypeForString('ALIGNMENT_GOOD') in [pPlayer.getAlignment(), cf.getUnitAlignment(pUnit)]:
		return False
	(pUnit2, iter) = pPlayer.firstUnit(False)
	while(pUnit2):
		if not pUnit2.isDead(): #is the unit alive and valid?
			if pUnit2.isHasPromotion(iMarksman) or pUnit2.isHasPromotion(iAeronsChosen):
				if pUnit.getLevel() < pUnit2.getLevel():
					return False
		(pUnit2, iter) = pPlayer.nextUnit(iter, False)
	return True
	
	

def canTriggerAmuriteTrialUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if pUnit.isHiddenNationality():
		return False
	return True

def applyAmuriteTrial1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iPlayer2 = cf.getCivilization(gc.getInfoTypeForString('CIVILIZATION_AMURITES'))
	if iPlayer2 != -1:
		pPlayer2 = gc.getPlayer(iPlayer2)
		pCity = pPlayer2.getCapitalCity()
		pUnit.setXY(pCity.getX(), pCity.getY(), False, True, True)

def doArmageddonApocalypse(argsList):
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
	iPercent = gc.getDefineINT('APOCALYPSE_KILL_CHANCE')
	pPlayer = gc.getPlayer(iPlayer)
	iBound = gc.getInfoTypeForString('PROMOTION_BOUND_BY_COMPACT')


	if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')) == False:
		for pyCity in PyPlayer(iPlayer).getCityList():
			pCity = pyCity.GetCy()
			iPop = pCity.getPopulation()
			iPop = int(iPop / 2)
			if iPop == 0:
				iPop = 1
			CvUtil.pyPrint('ARMAGEDDON! Setting %s to %d population' %(pyCity.getName(), iPop))
			pCity.setPopulation(iPop)
	pyPlayer = PyPlayer(iPlayer)
	apUnitList = pyPlayer.getUnitList()
	for pUnit in apUnitList:
		if pUnit.isAlive():
			if (CyGame().getSorenRandNum(100, "Apocalypse") < iPercent):
				pUnit.kill(False, PlayerTypes.NO_PLAYER)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_APOCALYPSE_KILLED", ()),'',1,'Art/Interface/Buttons/Apocalypse.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
		elif pUnit.isHasPromotion(iBound):
			pUnit.setHasPromotion(iBound, False)

	for i in xrange (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		pPlot.changePlotCounter(100)

	if pPlayer.isHuman():
		t = "TROPHY_FEAT_APOCALYPSE"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def doArmageddonArs(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_ARS')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doArmageddonBlight(argsList):
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
	pPlayer = gc.getPlayer(iPlayer)

	py = PyPlayer(iPlayer)
	if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
		for pyCity in py.getCityList():
			pCity = pyCity.GetCy()
			i = CyGame().getSorenRandNum(15, "Blight")
			i += pCity.getPopulation()
			i += pCity.getFeatureBadHealth()
			i -= pCity.getFeatureGoodHealth()
			i -= pCity.totalGoodBuildingHealth()
			if i > 0:
				pCity.changeEspionageHealthCounter(i)

	iDeath = gc.getInfoTypeForString('DAMAGE_DEATH')
	for pUnit in py.getUnitList():
		if pUnit.isAlive():
			pUnit.doDamageNoCaster(25, 100, iDeath, False)


def doArmageddonBuboes(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_BUBOES')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doArmageddonHellfire(argsList):
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
	if iPlayer == 0:
		iChampion = gc.getInfoTypeForString('UNIT_SECT_OF_FLIES')
		iDemon = gc.getInfoTypeForString('PROMOTION_DEMON')
		iHellfire = gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE')
		iHellfireChance = gc.getDefineINT('HELLFIRE_CHANCE')
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
		for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
			pPlayer2 = gc.getPlayer(iPlayer2)
			if pPlayer2.isAlive():
				if pPlayer2.isBarbarian() or pPlayer2.getCivilizationType() == iInfernal:
					for i in xrange (CyMap().numPlots()):
						pPlot = CyMap().plotByIndex(i)
						if not pPlot.isWater():
							if pPlot.getNumUnits() == 0:
								if not pPlot.isCity():
									if pPlot.isFlatlands() and not pPlot.isImpassable():
										if pPlot.getBonusType(-1) == -1:
											if CyGame().getSorenRandNum(3000, "Hellfire") < iHellfireChance:
												iImprovement = pPlot.getImprovementType()
												bValid = True
												if iImprovement != -1 :
													if gc.getImprovementInfo(iImprovement).isPermanent():
														bValid = False
												if bValid :
													if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS):
														pPlot.setOwner(iPlayer2)
													pPlot.setImprovementType(iHellfire)
													newUnit = pPlayer2.initUnit(iChampion, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
													newUnit.setHasPromotion(iDemon, True)

def doArmageddonPestilence(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iDeath = gc.getInfoTypeForString('DAMAGE_DEATH')
	
	if not pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')):
		for pyCity in PyPlayer(iPlayer).getCityList() :
			pCity = pyCity.GetCy()
			i = CyGame().getSorenRandNum(9, "Pestilence")
			i += (pCity.getPopulation() / 4)
			i -= pCity.totalGoodBuildingHealth()
			pCity.changeEspionageHealthCounter(i)
	py = PyPlayer(iPlayer)
	for pUnit in py.getUnitList():
		if pUnit.isAlive():
			pUnit.doDamageNoCaster(25, 100, iDeath, False)

def doArmageddonStephanos(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_STEPHANOS')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doArmageddonApophis(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_APOPHIS')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doArmageddonWrath(argsList):
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
	iEnraged = gc.getInfoTypeForString('PROMOTION_ENRAGED')

	iPossessed = gc.getInfoTypeForString('PROMOTION_POSSESSED')
	iSpirit = gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT')
	iSpirit3 = gc.getInfoTypeForString('PROMOTION_SPIRIT3')
	iExorcist = gc.getInfoTypeForString('PROMOTION_EXORCIST')
	iBlessed = gc.getInfoTypeForString('PROMOTION_BLESSED')

	iUnit = gc.getInfoTypeForString('UNIT_WRATH')
	iLand = gc.getInfoTypeForString('DOMAIN_LAND')
	iWrathConvertChance = gc.getDefineINT('WRATH_CONVERT_CHANCE')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)
	pPlayer = gc.getPlayer(iPlayer)

	for pUnit in PyPlayer(iPlayer).getUnitList():
		if not (pUnit.isOnlyDefensive() or pUnit.isHasPromotion(iSpirit) or pUnit.isHasPromotion(iSpirit3)):
			if pUnit.getDomainType() == iLand:
				if pUnit.isAlive():
					if CyGame().getSorenRandNum(100, "Wrath") < iWrathConvertChance:
						if not isWorldUnitClass(pUnit.getUnitClassType()):
							pUnit.setHasPromotion(iEnraged, True)
							if not (pUnit.isHasPromotion(iBlessed) or pUnit.isHasPromotion(iExorcist)) and CyGame().getSorenRandNum(100, "Wrath") < iWrathConvertChance:
								pUnit.setHasPromotion(iPossessed, True)
							CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WRATH_ENRAGED", ()),'',1,'Art/Interface/Buttons/Promotions/Enraged.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
							


def doArmageddonYersinia(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_YERSINIA')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doAzer(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not pPlot.isNone():
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_AZER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doBanditNietz3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CONDOTTIERO'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	# newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HORSEMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setName("Nietz the Bandit Lord")
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOBILITY1'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BOUNTY_HUNTER'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDO'), True)
	newUnit.setReligion(-1)

def helpBanditNietz3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_BANDIT_NIETZ_3_HELP", ())
	return szHelp

def doCalabimSanctuary1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iPlayer2 = cf.getCivilization(gc.getInfoTypeForString('CIVILIZATION_CALABIM'))
	if iPlayer2 != -1:
		pPlayer2 = gc.getPlayer(iPlayer2)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-4)

def canTriggerCityFeud(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.isCapital():
		return False
	return True

def doCityFeudArson(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCapitalCity()
	cf.doCityFire(pCity)

def doCityFeudStart1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCapitalCity = pPlayer.getCapitalCity()
	pCapitalCity.changeHappinessTimer(5)

def doCityFeudStart3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCapitalCity = pPlayer.getCapitalCity()
	pCapitalCity.changeOccupationTimer(5)

def helpCityFeudStart1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCapitalCity()
	szHelp = localText.getText("TXT_KEY_EVENT_CITY_FEUD_START_1_HELP", (pCity.getName(), ))
	return szHelp

def helpCityFeudStart3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCapitalCity()
	szHelp = localText.getText("TXT_KEY_EVENT_CITY_FEUD_START_3_HELP", (pCity.getName(), ))
	return szHelp

def canTriggerCitySplit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.isCapital():
		return False
	if pPlayer.getOpenPlayer() == -1:
		return False
	if CyGame().getWBMapScript():
		return False
	if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_BARBARIAN')):
		return False
	iKoun = gc.getInfoTypeForString('LEADER_KOUN')
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iPlayer)
		if pLoopPlayer.getLeaderType() == iKoun:
			return False
	return True

def doCitySplit1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pSplitPlayer = cf.formEmpire(pPlayer.getCivilizationType(), gc.getInfoTypeForString('LEADER_KOUN'), TeamTypes.NO_TEAM, pCity, pPlayer.getAlignment(), pPlayer)
	pSplitPlayer.setParent(kTriggeredData.ePlayer)

def doSoverignCity1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	cf.formEmpire(pPlayer.getCivilizationType(), gc.getInfoTypeForString('LEADER_KOUN'), pPlayer.getTeam(), pCity, pPlayer.getAlignment(), pPlayer)

def doDissent1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if gc.getGame().getSorenRandNum(100, "Dissent 1") < 50:
		pCity.changeOccupationTimer(2)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISSENT_1", ()),'',1,'Art/Interface/Buttons/Actions/Pillage.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)

def helpDissent1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DISSENT_1_HELP", ())
	return szHelp

def doDissent2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if gc.getGame().getSorenRandNum(100, "Dissent 2") < 50:
		pCity.changeOccupationTimer(4)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISSENT_2_BAD", ()),'',1,'Art/Interface/Buttons/Actions/Pillage.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
	else:
		pCity.changeHappinessTimer(5)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISSENT_2_GOOD", ()),'',1,'Art/Interface/Buttons/General/happy_person.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

def helpDissent2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DISSENT_2_HELP", ())
	return szHelp

def canApplyDissent4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_SOCIAL_ORDER')):
		return False
	return True

def applyExploreLairDepths1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iRnd = CyGame().getSorenRandNum(100, "Explore Lair")
	if iRnd < 50:
		cf.exploreLairBigBad(pUnit)
	if iRnd >= 50:
		cf.exploreLairBigGood(pUnit)

def applyExploreLairDwarfVsLizardmen1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	iTeam = bPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)

	bBronze = False
	bPoison = False
	if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
		bBronze = True
	if eTeam.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')):
		bPoison = True
	pPlot = pUnit.plot()
	pNewPlot = cf.findClearPlot(-1, pPlot)
	if pNewPlot != -1:
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIZARDMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIZARDMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit3 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIZARDMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bPoison:
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE'), True)
			newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE'), True)
			newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE'), True)
		newUnit4 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit4.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
		newUnit5 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit5.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
		if bBronze:
			newUnit4.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)
			newUnit5.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)

def applyExploreLairDwarfVsLizardmen2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	iTeam = bPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	bBronze = False
	bPoison = False
	if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
		bBronze = True
	if eTeam.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')):
		bPoison = True
	pPlot = pUnit.plot()
	pNewPlot = cf.findClearPlot(-1, pPlot)
	if pNewPlot != -1:
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIZARDMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIZARDMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bPoison:
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE'), True)
			newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE'), True)
		newUnit3 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
		newUnit4 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit4.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
		newUnit5 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit5.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
		if bBronze:
			newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)
			newUnit4.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)
			newUnit5.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)

def applyExploreLairPortal1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iBestValue = 0
	pBestPlot = -1
	for i in range (CyMap().numPlots()):
		iValue = 0
		pPlot = CyMap().plotByIndex(i)
		if not pPlot.isWater():
			if not pPlot.isPeak():
				if pPlot.getNumUnits() == 0:
					iValue = CyGame().getSorenRandNum(1000, "Portal")
					if not pPlot.isOwned():
						iValue += 1000
					if iValue > iBestValue:
						iBestValue = iValue
						pBestPlot = pPlot
	if pBestPlot != -1:
		pUnit.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_PORTAL",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pBestPlot.getX(),pBestPlot.getY(),True,True)

def doFlareDimensionalNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL1'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_DEFILE",point.x,point.y,point.z)

	pPlot = cf.findClearPlot(-1, pPlot)
	if pPlot != -1:
		pPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		lList = [	'UNIT_AIR_ELEMENTAL',
					'UNIT_EARTH_ELEMENTAL',
					'UNIT_FIRE_ELEMENTAL',
					'UNIT_WATER_ELEMENTAL',
					'UNIT_ICE_ELEMENTAL',
					'UNIT_LIGHTNING_ELEMENTAL',
					'UNIT_BALOR',
					'UNIT_DJINN',
					'UNIT_SPIDERKIN',
					'UNIT_WRAITH',
					'UNIT_CHAOS_MARAUDER',
					'UNIT_AUREALIS',
					'UNIT_FROST_GIANT',
					'UNIT_SUCCUBUS',
					'UNIT_REVELERS',
					'UNIT_MANTICORE',
					'UNIT_MOBIUS_WITCH',
					'UNIT_COLUBRA',
					'UNIT_TAR_DEMON',
					'UNIT_CHAOS_MARAUDER',
					'UNIT_AZER',
					# 'UNIT_AQUILAN',
					'UNIT_IMP'
					]
		iUnit = gc.getInfoTypeForString(lList[CyGame().getSorenRandNum(len(lList), "Pick Elemental")-1])
		newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_LAIRGUARDIAN, DirectionTypes.DIRECTION_SOUTH)

def doFlareEntropyNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	pPlot.setTempFeatureType(gc.getInfoTypeForString('FEATURE_TORMENTED_SOULS'), 0, CyGame().getSorenRandNum(7, "Flare Entropy Node"))
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL1'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_DEFILE",point.x,point.y,point.z)
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if not pPlot.isNone():
				pPlot.changePlotCounter(100)
	CyGame().changeGlobalCounter(2)

def doFlareFireNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_ARTILLERY_SHELL_EXPLODE'),point)
	CyAudioGame().Play3DSound("AS3D_UN_GRENADE_EXPLODE",point.x,point.y,point.z)
	iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
	iForest = gc.getInfoTypeForString('FEATURE_FOREST')
	iJungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if not pPlot.isNone():
				if pPlot.getFeatureType() in [iForest, iJungle]:
					pPlot.setFeatureType(iFlames, 0)
					if pPlot.isOwned():
						CyInterface().addMessage(pPlot.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_FLAMES", ()),'',1,'Art/Interface/Buttons/Fire.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)

def doFlareIceNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_ICE_SUMMON'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_CONTAGION",point.x,point.y,point.z)
	iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
	iGlacier = gc.getInfoTypeForString('TERRAIN_GLACIER')
	iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
	iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
	iWaste = gc.getInfoTypeForString('TERRAIN_WASTELAND')
	for iX in xrange(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in xrange(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pLoopPlot = CyMap().plot(iX,iY)
			if not pLoopPlot.isNone():
				if not pLoopPlot.isWater():
					iTerrain = pLoopPlot.getTerrainType()
					if not (iTerrain == iGlacier or iTerrain == iSnow or iTerrain == iWaste or iTerrain == iTundra):
						pLoopPlot.setTerrainType(iTundra, True, True)
				if pLoopPlot.getFeatureType() == iFlames:
					pLoopPlot.setFeatureType(-1, -1)
	pPlot.setTerrainType(iSnow, True, True)
	pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_BLIZZARD'), 1)


def doFlareLifeNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	iHallowed = gc.getInfoTypeForString('FEATURE_HALLOWED_GROUND')
	if pPlot.getFeatureType() == iHallowed:
		if pPlot.getTempFeatureTimer() > 0:
			pPlot.changeTempFeatureTimer(CyGame().getSorenRandNum(7, "Flare Life Node"))
	else:
		pPlot.setTempFeatureType(iHallowed, 0, 1+ CyGame().getSorenRandNum(7, "Flare Life Node"))
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL1'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_SANCTIFY",point.x,point.y,point.z)
	for iX in range(kTriggeredData.iPlotX-2, kTriggeredData.iPlotX+3, 1):
		for iY in range(kTriggeredData.iPlotY-2, kTriggeredData.iPlotY+3, 1):
			pPlot = CyMap().plot(iX,iY)
			if not pPlot.isNone():
				pPlot.changePlotCounter(-100)
	CyGame().changeGlobalCounter(-2)

def doFlareNatureNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_BLOOM'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_BLOOM",point.x,point.y,point.z)
	iForestNew = gc.getInfoTypeForString('FEATURE_FOREST_NEW')
	iLjos = gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR')
	iSvart = gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')
	iKurio = gc.getInfoTypeForString('CIVILIZATION_KURIOTATES')
	if pPlot.canHaveFeature(iForestNew): #This checks for valid terrain and whether there is already a feature on the tile
		pPlot.setFeatureType(iForestNew, 0)
	for iX in xrange(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in xrange(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if not pPlot.isNone():
				if pPlot.canHaveFeature(iForestNew): #This checks for valid terrain and whether there is already a feature on the tile
					if pPlot.getImprovementType() == -1:
						pPlot.setFeatureType(iForestNew, 0)
					elif pPlot.isOwned():
						if gc.getPlayer(pPlot.getOwner()).getCivilizationType() in [iLjos, iSvart, iKurio]:
							pPlot.setFeatureType(iForestNew, 0)

def doFlareWaterNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPRING'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_SPRING",point.x,point.y,point.z)
	iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
	iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
	iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
	iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if not pPlot.isNone():
				if pPlot.getTerrainType() == iDesert:
					pPlot.setTerrainType(iPlains,True,True)
				if pPlot.getFeatureType() == iFlames:
					pPlot.setFeatureType(-1, -1)
				if pPlot.getImprovementType() == iSmoke:
					pPlot.setImprovementType(-1)

def canTriggerPlotEmpty(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone():
		return False
	if pPlot.getNumUnits() > 0:
		return False
	return True

def canTriggerFoodSicknessUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if not pUnit.isAlive():
		return False
	return True

def doFoodSickness(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iDmg = pUnit.getDamage() + 20
	if iDmg > 99:
		iDmg = 99
	pUnit.setDamage(iDmg, PlayerTypes.NO_PLAYER)
	pUnit.changeImmobileTimer(2)

def doFrostling(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not pPlot.isNone():
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_FROSTLING'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doGodslayer(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	cf.placeTreasure(iPlayer, gc.getInfoTypeForString('EQUIPMENT_GODSLAYER'))

def doGovernorAssassination(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	bMatch = False
	iCivic = pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_GOVERNMENT'))
	if iCivic != gc.getInfoTypeForString('CIVIC_DESPOTISM'):
		if iCivic == gc.getInfoTypeForString('CIVIC_GOD_KING'):
			bMatch = True
		if iCivic == gc.getInfoTypeForString('CIVIC_ARISTOCRACY'):
			if iEvent == gc.getInfoTypeForString('EVENT_GOVERNOR_ASSASSINATION_1'):
				bMatch = True
		if iCivic == gc.getInfoTypeForString('CIVIC_CITY_STATES') or iCivic == gc.getInfoTypeForString('CIVIC_REPUBLIC'):
			if iEvent == gc.getInfoTypeForString('EVENT_GOVERNOR_ASSASSINATION_3'):
				bMatch = True
		if iCivic == gc.getInfoTypeForString('CIVIC_THEOCRACY'):
			if iEvent == gc.getInfoTypeForString('EVENT_GOVERNOR_ASSASSINATION_4'):
				bMatch = True
		if bMatch:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PEOPLE_APPROVE", ()),'',1,'Art/Interface/Buttons/General/happy_person.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
			pCity.changeHappinessTimer(3)
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_JUDGEMENT_WRONG", ()),'',1,'Art/Interface/Buttons/General/unhealthy_person.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
			pCity.changeHurryAngerTimer(3)

def doGuildOfTheNineMerc41(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)

	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WOODSMAN1'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)

	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LONGBOWMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEXTEROUS'), True)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)

	newUnit3 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RANGER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)
	newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SINISTER'), True)
	newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)

def canTriggerGuildOfTheNineMerc5(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if not pCity.isCoastal(10):
		return False
	return True

def doGuildOfTheNineMerc51(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AMPHIBIOUS'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)

	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_BOARDING_PARTY'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)

	newUnit3 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIVATEER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)
	newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)

def doGuildOfTheNineMerc61(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MIMIC'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MUTATED'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)

	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_TASKMASTER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)

	newUnit3 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HUNTER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setUnitArtStyleType(gc.getInfoTypeForString('UNIT_ARTSTYLE_BALSERAPHS'))
	newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)

def doGuildOfTheNineMerc71(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CROSSBOWMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEFENSIVE'), True)

	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)

	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)

	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)
	newUnit3 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DWARVEN_CANNON'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)
	
def doGuildOfTheNineMerc81(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LONGBOWMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), True)

	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)

	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_OGRE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)
	newUnit3 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIZARDMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)

def doGreatBeastGurid(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_GURID')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doGreatBeastXien(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_XIEN')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doGreatBeastLeviathan(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_LEVIATHAN')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		pBestPlot = -1
		iBestPlot = -1
		for i in range (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iPlot = -1
			if pPlot.isWater():
				if pPlot.getNumUnits() == 0:
					iPlot = CyGame().getSorenRandNum(500, "Leviathan")
					iPlot += (pPlot.area().getNumTiles() * 10)
			if iPlot > iBestPlot:
				iBestPlot = iPlot
				pBestPlot = pPlot
		if iBestPlot != -1:
			bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
			newUnit = bPlayer.initUnit(iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doGreatBeastMargalard(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_MARGALARD')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def applyHyboremsWhisper1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = cf.getAshenVeilCity(1)
	pPlayer.acquireCity(pCity,False,False)

def helpHyboremsWhisper1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pCity = cf.getAshenVeilCity(1)
	szHelp = localText.getText("TXT_KEY_EVENT_HYBOREMS_WHISPER_HELP", (pCity.getName(), ))
	return szHelp

def applyHyboremsWhisper2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = cf.getAshenVeilCity(2)
	pPlayer.acquireCity(pCity,False,False)

def helpHyboremsWhisper2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pCity = cf.getAshenVeilCity(2)
	szHelp = localText.getText("TXT_KEY_EVENT_HYBOREMS_WHISPER_HELP", (pCity.getName(), ))
	return szHelp

def applyHyboremsWhisper3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = cf.getAshenVeilCity(3)
	pPlayer.acquireCity(pCity,False,False)

def helpHyboremsWhisper3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pCity = cf.getAshenVeilCity(3)
	szHelp = localText.getText("TXT_KEY_EVENT_HYBOREMS_WHISPER_HELP", (pCity.getName(), ))
	return szHelp

def applyIronOrb3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	szBuffer = localText.getText("TXT_KEY_EVENT_IRON_ORB_3_RESULT", ())
	pPlayer.chooseTech(1, szBuffer, True)

def doJudgementRight(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_JUDGEMENT_RIGHT", ()),'',1,'Art/Interface/Buttons/General/happy_person.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
	pCity.changeHappinessTimer(10)

def doJudgementWrong(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_JUDGEMENT_WRONG", ()),'',1,'Art/Interface/Buttons/General/unhealthy_person.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
	pCity.changeCrime(3)

def doLetumFrigus3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_AGGRESSIVE'),True)

def helpLetumFrigus3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_LETUM_FRIGUS_3_HELP", ())
	return szHelp

def canTriggerLunaticCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	iReligion = pPlayer.getStateReligion()
	iTemple = -1
	if iReligion == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
		iTemple = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER')
	if iReligion == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
		iTemple = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_LEAVES')
	if iReligion == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
		iTemple = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')
	if iReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
		iTemple = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS')
	if iReligion == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
		iTemple = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH')
	if iReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
		iTemple = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN')
	if iTemple == -1:
		return False
	if pCity.getNumRealBuilding(iTemple) == 0:
		return False
	return True

def doMachineParts1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CLOCKWORK_GOLEM'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)

def doMachineParts2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CLOCKWORK_GOLEM'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), True)

def applyMalakimPilgrimage1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iPlayer2 = cf.getCivilization(gc.getInfoTypeForString('CIVILIZATION_MALAKIM'))
	if iPlayer2 != -1:
		pPlayer2 = gc.getPlayer(iPlayer2)
		pCity = pPlayer2.getCapitalCity()
		pUnit.setXY(pCity.getX(), pCity.getY(), False, True, True)

def doMarketTheft2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iRnd = gc.getGame().getSorenRandNum(21, "Market Theft 2") - 10
	pCity.changeCrime(iRnd)

def helpMarketTheft2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	szHelp = localText.getText("TXT_KEY_EVENT_MARKET_THEFT_2_HELP", ())
	return szHelp

def canTriggerMerchantKeep(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_MERCHANT')) == 0:
		return False
	return True

def doMistforms(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	iMistform = gc.getInfoTypeForString('UNIT_MISTFORM')
	newUnit1 = bPlayer.initUnit(iMistform, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(iMistform, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(iMistform, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)


def canTriggerMushrooms(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	return not pPlot.isCity()
	
def doMushrooms(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.setBonusType(gc.getInfoTypeForString('BONUS_MUSHROOMS'))

def canTriggerMutateUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	iMutated = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_MUTATED')
	if pUnit.isHasPromotion(iMutated):
		return False
	return True

def canApplyNoOrder(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
		return False
	return True

def doOrderVsVeil1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	if not pCity.isHolyCityByType(iVeil):
		if gc.getGame().getSorenRandNum(100, "Order vs Veil 1") < 50:
			pCity.setHasReligion(iVeil, False, False, False)
	for pyCity in PyPlayer(iPlayer).getCityList():
		loopCity = pyCity.GetCy()
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHurryAngerTimer(5)
			

def doOrderVsVeil2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	if not pCity.isHolyCityByType(iOrder):
		if gc.getGame().getSorenRandNum(100, "Order vs Veil 2") < 50:
			pCity.setHasReligion(iOrder, False, False, False)
	for pyCity in PyPlayer(iPlayer).getCityList():
		loopCity = pyCity.GetCy()
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHurryAngerTimer(5)

def doOrderVsVeil3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(3)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	if not pCity.isHolyCityByType(iVeil):
		if gc.getGame().getSorenRandNum(100, "Order vs Veil 3") < 25:
			pCity.setHasReligion(iVeil, False, False, False)
	if not pCity.isHolyCityByType(iOrder):
		if gc.getGame().getSorenRandNum(100, "Order vs Veil 3") < 25:
			pCity.setHasReligion(iOrder, False, False, False)
	if gc.getGame().getSorenRandNum(100, "Order vs Veil 3") < 50:
		pCity.changePopulation(-1)

def canApplyOrderVsVeil4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_DUNGEON')) == 0:
		return False
	return True

def helpOrderVsVeil1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_1_HELP", ())
	return szHelp

def helpOrderVsVeil2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_2_HELP", ())
	return szHelp

def helpOrderVsVeil3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_3_HELP", ())
	return szHelp

def doOrderVsVeilTemple1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL'), 0)
	if not pCity.isHolyCityByType(iVeil):
		if gc.getGame().getSorenRandNum(100, "Order vs Veil Temple 1") < 50:
			pCity.setHasReligion(iVeil, False, False, False)
	for pyCity in PyPlayer(iPlayer).getCityList():
		loopCity = pyCity.GetCy()
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHurryAngerTimer(5)

def doOrderVsVeilTemple2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	if gc.getGame().getSorenRandNum(100, "Order vs Veil Temple 2") < 50:
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL'), 0)
	if not pCity.isHolyCityByType(iVeil):
		if gc.getGame().getSorenRandNum(100, "Order vs Veil Temple 2") < 50:
			pCity.setHasReligion(iVeil, False, False, False)
	if gc.getGame().getSorenRandNum(100, "Order vs Veil Temple 2") < 50:
		pCity.changePopulation(-1)

def doOrderVsVeilTemple3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(3)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	for pyCity in PyPlayer(iPlayer).getCityList():
		loopCity = pyCity.GetCy()
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHurryAngerTimer(5)

def helpOrderVsVeilTemple1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_TEMPLE_1_HELP", ())
	return szHelp

def helpOrderVsVeilTemple2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_TEMPLE_2_HELP", ())
	return szHelp

def helpOrderVsVeilTemple3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_TEMPLE_3_HELP", ())
	return szHelp

def canTriggerParith(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	if CyGame().getTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH") != 1:
		return False
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
		return False
	return True

def applyParithYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = player.getUnit(kTriggeredData.iUnitId)
	CyGame().setTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH", pUnit.getUnitType())

def canTriggerPenguins(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not pPlot.isAdjacentToWater():
		return False
	if pPlot.isPeak():
		return False
	return True

def doPenguins(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.setBonusType(gc.getInfoTypeForString('BONUS_PENGUINS'))

def canTriggerPickAlignment(argsList):
	kTriggeredData = argsList[0]
	if CyGame().getWBMapScript():
		return False
	return True

def doPickAlignment1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_GOOD'))

def doPickAlignment2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_NEUTRAL'))

def doPickAlignment3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))

def doPigGiant3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pPlot = cf.findClearPlot(-1, pCity.plot())
	if pPlot != -1:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_HILL_GIANT'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDO'), True)

def applyPronCapria(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_CAPRIA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_CAPRIA_POPUP",()), iPlayer)

def canTriggerPronCapria(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_CAPRIA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronEthne(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_ETHNE'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_ETHNE_POPUP",()), iPlayer)

def canTriggerPronEthne(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_ETHNE'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronArendel(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_ARENDEL'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_ARENDEL_POPUP",()), iPlayer)

def canTriggerPronArendel(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_ARENDEL'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronThessa(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_THESSA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_THESSA_POPUP",()), iPlayer)

def canTriggerPronThessa(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_THESSA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronHannah(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_HANNAH'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_HANNAH_POPUP",()), iPlayer)

def canTriggerPronHannah(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_HANNAH'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronRhoanna(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_RHOANNA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_RHOANNA_POPUP",()), iPlayer)

def canTriggerPronRhoanna(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_RHOANNA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronValledia(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_VALLEDIA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_VALLEDIA_POPUP",()), iPlayer)

def canTriggerPronValledia(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_VALLEDIA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronMahala(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_MAHALA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_MAHALA_POPUP",()), iPlayer)

def canTriggerPronMahala(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_MAHALA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronKeelyn(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_KEELYN'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_KEELYN_POPUP",()), iPlayer)

def canTriggerPronKeelyn(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_KEELYN'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronSheelba(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_SHEELBA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_SHEELBA_POPUP",()), iPlayer)

def canTriggerPronSheelba(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_SHEELBA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronFaeryl(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_FAERYL'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_FAERYL_POPUP",()), iPlayer)

def canTriggerPronFaeryl(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_FAERYL'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronAlexis(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_ALEXIS'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_ALEXIS_POPUP",()), iPlayer)

def canTriggerPronAlexis(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_ALEXIS'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def canTriggerUniqueFeatureAifonIsle(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureBradelinesWell(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureBrokenSepulcher(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def doFreeBarbatos(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_BARBATOS')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def canTriggerUniqueFeatureGuardian(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_GUARDIAN')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureLetumFrigus(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureLetumFrigusIllians(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeaturePyreOfTheSeraphic(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_PYRE_OF_THE_SERAPHIC')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerSageKeep(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_SCIENTIST')) == 0:
		return False
	return True

def doSailorsDirge(argsList):
	kTriggeredData = argsList[0]
	eUnit = gc.getInfoTypeForString('UNIT_SAILORS_DIRGE')
	eIce = gc.getInfoTypeForString('FEATURE_ICE')
	if CyGame().getUnitCreatedCount(eUnit) == 0:
		pBestPlot = -1
		iBestPlot = -1
		for i in range (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iPlot = -1
			if pPlot.isWater() and pPlot.getFeatureType() != eIce:
				if pPlot.getNumUnits() == 0:
					iPlot = CyGame().getSorenRandNum(500, "Sailors Dirge")
					iPlot = iPlot + (pPlot.area().getNumTiles() * 10)
					if pPlot.isOwned():
						iPlot = iPlot / 2
					if iPlot > iBestPlot:
						iBestPlot = iPlot
						pBestPlot = pPlot
		if iBestPlot != -1:
			bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
			newUnit = bPlayer.initUnit(eUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

			lUndead = [	gc.getInfoTypeForString('UNIT_SKELETON'),
						gc.getInfoTypeForString('UNIT_SKELETON'),
						gc.getInfoTypeForString('UNIT_SKELETON'),
						gc.getInfoTypeForString('UNIT_SKELETON'),
						gc.getInfoTypeForString('UNIT_SKELETON'),
						gc.getInfoTypeForString('UNIT_SKELETON'),
						gc.getInfoTypeForString('UNIT_SKELETON'),
						gc.getInfoTypeForString('UNIT_SKELETON'),
						gc.getInfoTypeForString('UNIT_SKELETON'),
						gc.getInfoTypeForString('UNIT_SKELETON'),
						gc.getInfoTypeForString('UNIT_SKELETON'),
						gc.getInfoTypeForString('UNIT_SPECTRE'),
						gc.getInfoTypeForString('UNIT_SPECTRE'),
						gc.getInfoTypeForString('UNIT_SPECTRE'),
						gc.getInfoTypeForString('UNIT_SPECTRE'),
						gc.getInfoTypeForString('UNIT_SPECTRE'),
						gc.getInfoTypeForString('UNIT_SPECTRE'),
						gc.getInfoTypeForString('UNIT_SPECTRE'),
						gc.getInfoTypeForString('UNIT_SPECTRE'),
						gc.getInfoTypeForString('UNIT_SPECTRE'),
						gc.getInfoTypeForString('UNIT_DROWN'),
						gc.getInfoTypeForString('UNIT_DROWN'),
						gc.getInfoTypeForString('UNIT_DROWN'),
						gc.getInfoTypeForString('UNIT_DROWN'),
						gc.getInfoTypeForString('UNIT_DROWN'),
						gc.getInfoTypeForString('UNIT_DROWN'),
						gc.getInfoTypeForString('UNIT_DROWN'),
						gc.getInfoTypeForString('UNIT_DROWN'),
						gc.getInfoTypeForString('UNIT_DROWN'),
						gc.getInfoTypeForString('UNIT_DISEASED_CORPSE'),
						gc.getInfoTypeForString('UNIT_DISEASED_CORPSE'),
						gc.getInfoTypeForString('UNIT_DISEASED_CORPSE'),
						gc.getInfoTypeForString('UNIT_DISEASED_CORPSE'),
						gc.getInfoTypeForString('UNIT_HOLLOW_MAN'),
						gc.getInfoTypeForString('UNIT_HOLLOW_MAN'),
						gc.getInfoTypeForString('UNIT_HOLLOW_MAN')
						]

			iSkeleton = gc.getInfoTypeForString('UNIT_SKELETON')
			iBoarding = gc.getInfoTypeForString('PROMOTION_BOARDING')
			for i in range(4):
				iUnit = lUndead.pop(CyGame().getSorenRandNum(len(lUndead), "Crew Sailors Dirge"))
				newUnit = bPlayer.initUnit(iUnit , newUnit.getX(), newUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setHasPromotion(iBoarding, True)

def doSailorsDirgeDefeated(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	cf.placeTreasure(iPlayer, gc.getInfoTypeForString('EQUIPMENT_TREASURE'))

def applyShrineCamulos2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if CyGame().getSorenRandNum(100, "Shrine Camulos") < 10:
		pPlot = cf.findClearPlot(-1, pCity.plot())
		if pPlot != -1:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SHRINE_CAMULOS",()),'',1,'Art/Interface/Buttons/Units/Pit Beast.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
			bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
			newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_PIT_BEAST'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.attack(pCity.plot(), False)

def doSignAeron(argsList):
	kTriggeredData = argsList[0]
	CyGame().changeGlobalCounter(3)

def doSacredGrove(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_LEAVES')) > 0:
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_LEAVES'), 1)

def doSignAmathaon(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iCreation = gc.getInfoTypeForString('BONUS_MANA_CREATION')
	if pPlayer.getNumAvailableBonuses(iCreation) < 2 and not pPlot.isCity() and pPlot.getBonusType(-1) == -1:
		pPlot.setBonusType(iCreation)
	else:
		iTurns = 7 + gc.getGame().getSorenRand().get(100, "Amathaon")* gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getVictoryDelayPercent() / 50
		pPlot.setTempImprovementType(gc.getInfoTypeForString('IMPROVEMENT_MANA_CREATION'), iTurns)
		pPlot.changeTempBonusTimer(iTurns)

def doSignArawn(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iGrave = gc.getInfoTypeForString('IMPROVEMENT_GRAVEYARD')
	iHallowed = gc.getInfoTypeForString('FEATURE_HALLOWED_GROUND')
	iCount = pPlayer.getImprovementCount(iGrave)
	if iCount > 0:
		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.isOwned():
				if pPlot.getOwner() == iPlayer:
					if pPlot.getImprovementType() == iGrave:
						if pPlot.getFeatureType() == iHallowed:
							if pPlot.getTempFeatureTimer() > 0:
								pPlot.changeTempFeatureTimer(CyGame().getSorenRandNum(10, "Sign Arawn Gyra hallows grave"))
						else:
							pPlot.setTempFeatureType(iHallowed, 0, 1 + CyGame().getSorenRandNum(10, "Sign Arawn Gyra hallows grave"))
						iCount-= 1
						if iCount < 1:
							break

def doSignBhall(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
	iGrass = gc.getInfoTypeForString('TERRAIN_GRASS')
	iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
	iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
	iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
	for i in xrange (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.isOwned():
			if pPlot.getOwner() == iPlayer:
				if pPlot.getFeatureType() == -1:
					if pPlot.getImprovementType() == -1:
						if not pPlot.isWater():
							if CyGame().getSorenRandNum(100, "SignBhall") < 10:
								iTerrain = pPlot.getTerrainType()
								if iTerrain == iSnow:
									pPlot.setTempTerrainType(iTundra, CyGame().getSorenRandNum(10, "Tundra") + 10)
								elif iTerrain == iTundra:
									pPlot.setTempTerrainType(iGrass, CyGame().getSorenRandNum(10, "Grass") + 10)
								elif iTerrain == iGrass:
									pPlot.setTempTerrainType(iPlains, CyGame().getSorenRandNum(10, "Plains") + 10)
								elif iTerrain == iPlains:
									pPlot.setTempTerrainType(iDesert, CyGame().getSorenRandNum(10, "Desert") + 10)

def doSignCamulos(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iLoopPlayer)
		if loopPlayer.isAlive():
			if loopPlayer.getTeam() != pPlayer.getTeam():
				loopPlayer.AI_changeAttitudeExtra(iPlayer, -1)
				pPlayer.AI_changeAttitudeExtra(iLoopPlayer, -1)

def doSignDagda(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iLoopPlayer)
		if loopPlayer.isAlive():
			if loopPlayer.getTeam() != pPlayer.getTeam():
				loopPlayer.AI_changeAttitudeExtra(iPlayer, 1)
				pPlayer.AI_changeAttitudeExtra(iLoopPlayer, 1)

def doSignEsus(argsList):
	kTriggeredData = argsList[0]
	CyGame().changeCrime(15)

def doSignLugus(argsList):
	kTriggeredData = argsList[0]
	CyGame().changeCrime(-15)

def doSignMulcarn(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
	iGrass = gc.getInfoTypeForString('TERRAIN_GRASS')
	iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
	iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
	iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.isOwned():
			if pPlot.getOwner() == iPlayer:
				if pPlot.getFeatureType() == -1:
					if pPlot.getImprovementType() == -1:
						if not pPlot.isWater():
							if CyGame().getSorenRandNum(100, "SignMulcarn") < 10:
								iTerrain = pPlot.getTerrainType()
								if iTerrain == iTundra:
									pPlot.setTempTerrainType(iSnow, CyGame().getSorenRandNum(10, "Snow") + 10)
								elif iTerrain == iGrass:
									pPlot.setTempTerrainType(iTundra, CyGame().getSorenRandNum(10, "Tundra") + 10)
								elif iTerrain == iPlains:
									pPlot.setTempTerrainType(iTundra, CyGame().getSorenRandNum(10, "Tundra") + 10)
								elif iTerrain == iDesert:
									pPlot.setTempTerrainType(iPlains, CyGame().getSorenRandNum(10, "Plains") + 10)

def doSignSirona(argsList):
	kTriggeredData = argsList[0]
	CyGame().changeGlobalCounter(-3)

def doSignSucellus(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iDiseased = gc.getInfoTypeForString('PROMOTION_DISEASED')
	apUnitList = PyPlayer(iPlayer).getUnitList()
	for pUnit in apUnitList:
		if pUnit.isHasPromotion(iDiseased):
			pUnit.setHasPromotion(iDiseased, False)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POOL_OF_TEARS_DISEASED",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Spells/Curedisease.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
		if pUnit.getDamage() > 0:
			pUnit.setDamage(pUnit.getDamage() / 2, PlayerTypes.NO_PLAYER)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_HEALED",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Spells/Heal.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)

def doSignTali(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
	iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
	iSpring = gc.getInfoTypeForString('EFFECT_SPRING')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.isOwned():
			if pPlot.getOwner() == iPlayer:
				if pPlot.getFeatureType() == iFlames:
					point = pPlot.getPoint()
					CyEngine().triggerEffect(iSpring,point)
					CyAudioGame().Play3DSound("AS3D_SPELL_SPRING",point.x,point.y,point.z)
					pPlot.setFeatureType(-1, 0)
				if pPlot.getImprovementType() == iSmoke:
					point = pPlot.getPoint()
					CyEngine().triggerEffect(iSpring,point)
					CyAudioGame().Play3DSound("AS3D_SPELL_SPRING",point.x,point.y,point.z)
					pPlot.setImprovementType(-1)

def canTriggerSmugglers(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_SMUGGLERS_PORT')) > 0:
		return False
	if not pCity.isCoastal(10):
		return False
	return True

def doSpiderMine3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_GIANT_SPIDER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)

def applyTreasure1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	cf.placeTreasure(iPlayer, gc.getInfoTypeForString('EQUIPMENT_TREASURE'))

def canTriggerSwitchCivs(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if not pPlayer.isHuman():
		return False
	if CyGame().getRankPlayer(0) != kTriggeredData.ePlayer:
		return False
	if CyGame().getGameTurn() < 20:
		return False
	if gc.getTeam(otherPlayer.getTeam()).isAVassal():
		return False
	if CyGame().getWBMapScript():
		return False
	return True

def doSwitchCivs2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iNewPlayer = kTriggeredData.eOtherPlayer
	iOldPlayer = kTriggeredData.ePlayer
	CyGame().reassignPlayerAdvanced(iOldPlayer, iNewPlayer, -1)

def canTriggerTraitor(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.happyLevel() - pCity.unhappyLevel(0) < 0:
		return False
	return True

def doVeilVsOrderTemple1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER'), 0)
	if not pCity.isHolyCityByType(iOrder):
		if gc.getGame().getSorenRandNum(100, "Veil vs Order Temple 1") < 50:
			pCity.setHasReligion(iOrder, False, False, False)
	for pyCity in PyPlayer(iPlayer).getCityList():
		loopCity = pyCity.GetCy()
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHurryAngerTimer(5)

def doVeilVsOrderTemple2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	if gc.getGame().getSorenRandNum(100, "Veil Vs Order Temple 2") < 50:
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER'), 0)
	if not pCity.isHolyCityByType(iOrder):
		if gc.getGame().getSorenRandNum(100, "Veil Vs Order Temple 2") < 50:
			pCity.setHasReligion(iOrder, False, False, False)
	if gc.getGame().getSorenRandNum(100, "Veil Vs Order Temple 2") < 50:
		pCity.changePopulation(-1)

def doVeilVsOrderTemple3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(3)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	for pyCity in PyPlayer(iPlayer).getCityList():
		loopCity = pyCity.GetCy()
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHurryAngerTimer(5)

def helpVeilVsOrderTemple1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_VEIL_VS_ORDER_TEMPLE_1_HELP", ())
	return szHelp

def helpVeilVsOrderTemple2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_VEIL_VS_ORDER_TEMPLE_2_HELP", ())
	return szHelp

def helpVeilVsOrderTemple3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_VEIL_VS_ORDER_TEMPLE_3_HELP", ())
	return szHelp

def doSlaveEscape(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.kill(False, -1)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SLAVE_ESCAPE", ()),'',1,'Art/Interface/Buttons/Units/Slave.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)

def canTriggerSlaveRevoltUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	pPlot = pUnit.plot()
	if pPlot.getNumUnits() != 1:
		return False
	return True

def doSlaveRevolt(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iRace = pUnit.getRace()
	plot = pUnit.plot()
	iX = pUnit.getX()
	iY = pUnit.getY()
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SLAVE_REVOLT", ()),'',1,'Art/Interface/Buttons/Units/Slave.dds',ColorTypes(8),iX,iY,True,True)
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	iUnit = gc.getInfoTypeForString('UNIT_WARRIOR')
	pCity = CyMap().findCity(iX, iY, pUnit.getOwner(), TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, pPlayer.getCity(-1))
	if not pCity.isNone():
		iUnit = pCity.getConscriptUnit()
	if iUnit == -1:
		iUnit = gc.getInfoTypeForString('UNIT_WARRIOR')
		
	if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_COVEN')):
		if pUnit.getReligion() == gc.getInfoTypeForString('RELIGION_COVEN'):
			iUnit = gc.getInfoTypeForString('UNIT_CHAINBREAKER')
	pPlot2 = cf.findClearPlot(-1, plot)
	if pPlot2 != -1:
		pNewUnit = bPlayer.initUnit(iUnit, pPlot2.getX(), pPlot2.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		pNewUnit.convert(pUnit)

# lfgr
# REPLACE
# \Qdef canApplyTrait\E([^(]*)\Q(argsList):\E\r\n\t\QiEvent = argsList[0]\E\r\n\t\QkTriggeredData = argsList[1]\E\r\n\t\QpPlayer = gc.getPlayer(kTriggeredData.ePlayer)\E\r\n\t\Qif gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('\E([^']*)\Q'):\E\r\n\t\t\Qreturn False\E\r\n\t\Qreturn True\E
# WITH
# def canApplyTrait\1\(argsList\):\r\n\tiEvent = argsList[0]\r\n\tkTriggeredData = argsList[1]\r\n\tpPlayer = gc.getPlayer\(kTriggeredData.ePlayer\)\r\n\tif gc.getLeaderHeadInfo\(pPlayer.getLeaderType\(\)\).getPermanentTrait\(\) == gc.getInfoTypeForString\('\2'\):\r\n\t\treturn False\r\n\treturn True\r\n\r\n# lfgr: adaptive event help\r\ndef helpTrait\1\(argsList\) :\r\n\treturn CyGameTextMgr\(\).parseTraits\( gc.getInfoTypeForString\('\2'\), CivilizationTypes.NO_CIVILIZATION, False \)\r\n# lfgr end
# lfgr end

def canApplyTraitAggressive(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_AGGRESSIVE'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitAggressive(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_AGGRESSIVE'), CivilizationTypes.NO_CIVILIZATION, False )
# lfgr end

def doTraitAggressive(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_AGGRESSIVE'),True)

def canApplyTraitArcane(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_ARCANE'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitArcane(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_ARCANE'), CivilizationTypes.NO_CIVILIZATION, False )
# lfgr end

def doTraitArcane(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_ARCANE'),True)

def canApplyTraitCharismatic(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_CHARISMATIC'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitCharismatic(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_CHARISMATIC'), CivilizationTypes.NO_CIVILIZATION, False )
# lfgr end

def doTraitCharismatic(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_CHARISMATIC'),True)

def canApplyTraitCreative(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_CREATIVE'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitCreative(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_CREATIVE'), CivilizationTypes.NO_CIVILIZATION, False )
# lfgr end

def doTraitCreative(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_CREATIVE'),True)

def canApplyTraitExpansive(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_EXPANSIVE'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitExpansive(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_EXPANSIVE'), CivilizationTypes.NO_CIVILIZATION, False )
# lfgr end

def doTraitExpansive(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_EXPANSIVE'),True)

def canApplyTraitFinancial(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_FINANCIAL'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitFinancial(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_FINANCIAL'), CivilizationTypes.NO_CIVILIZATION, False )
# lfgr end

def doTraitFinancial(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_FINANCIAL'),True)

def canApplyTraitIndustrious(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_INDUSTRIOUS'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitIndustrious(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_INDUSTRIOUS'), CivilizationTypes.NO_CIVILIZATION, False )
# lfgr end

def doTraitIndustrious(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait, False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_INDUSTRIOUS'),True)

def doTraitInsane(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCivilization = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iTraitCount = 0
	for i in xrange(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(i) and i != gc.getInfoTypeForString('TRAIT_INSANE'):
			if gc.getTraitInfo(i).isSelectable():
				if i != pCivilization.getCivTrait():
					pPlayer.setHasTrait(i, False)
					iTraitCount += 1

	Traits = [ 'TRAIT_AGGRESSIVE','TRAIT_ARCANE','TRAIT_CHARISMATIC','TRAIT_CREATIVE','TRAIT_EXPANSIVE','TRAIT_FINANCIAL','TRAIT_INDUSTRIOUS','TRAIT_ORGANIZED','TRAIT_PHILOSOPHICAL','TRAIT_RAIDERS','TRAIT_SPIRITUAL' ]

	if iTraitCount > 0:
		iRnd1 = CyGame().getSorenRandNum(len(Traits), "Insane Trait 1")
		pPlayer.setHasTrait(gc.getInfoTypeForString(Traits[iRnd1]),True)
	if iTraitCount > 1:
		iRnd2 = CyGame().getSorenRandNum(len(Traits), "Insane Trait 2")
		while iRnd2 == iRnd1:
			iRnd2 = CyGame().getSorenRandNum(len(Traits), "Insane Trait 2 - retry")
		pPlayer.setHasTrait(gc.getInfoTypeForString(Traits[iRnd2]),True)
	if iTraitCount > 2:
		iRnd3 = CyGame().getSorenRandNum(len(Traits), "Insane Trait 3")
		while iRnd3 == iRnd1 or iRnd3 == iRnd2:
			iRnd3 = CyGame().getSorenRandNum(len(Traits), "Insane Trait 3 - retry")
		pPlayer.setHasTrait(gc.getInfoTypeForString(Traits[iRnd3]),True)


	iRnd = (CyGame().getSorenRandNum(6, "Insane Attitude Change") - 3)
	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iLoopPlayer)
		if loopPlayer.isAlive():
			if loopPlayer.getTeam() != pPlayer.getTeam():
				pPlayer.AI_changeAttitudeExtra(iLoopPlayer, iRnd)



def canApplyTraitOrganized(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_ORGANIZED'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitOrganized(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_ORGANIZED'), CivilizationTypes.NO_CIVILIZATION, False )
# lfgr end

def doTraitOrganized(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait, False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_ORGANIZED'),True)

def canApplyTraitPhilosophical(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_PHILOSOPHICAL'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitPhilosophical(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_PHILOSOPHICAL'), CivilizationTypes.NO_CIVILIZATION, False )
# lfgr end

def doTraitPhilosophical(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait, False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_PHILOSOPHICAL'),True)

def canApplyTraitRaiders(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_RAIDERS'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitRaiders(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_RAIDERS'), CivilizationTypes.NO_CIVILIZATION, False )
# lfgr end

def doTraitRaiders(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait, False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_RAIDERS'),True)

def canApplyTraitSpiritual(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_SPIRITUAL'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitSpiritual(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_SPIRITUAL'), CivilizationTypes.NO_CIVILIZATION, False )
# lfgr end

def doTraitSpiritual(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait, False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_SPIRITUAL'),True)

def doVolcanoCreation(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

	iImprovement = pPlot.getImprovementType()
	if iImprovement != -1 :
		while gc.getImprovementInfo(iImprovement).isUnique():
			pPlot = cf.findClearPlotImprovement(pPlot)
			if pPlot != -1:
				iImprovement = pPlot.getImprovementType()

	pPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
	pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_VOLCANO'), 0)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_ARTILLERY_SHELL_EXPLODE'),point)
	CyAudioGame().Play3DSound("AS3D_UN_GRENADE_EXPLODE",point.x,point.y,point.z)
# FlavourMod: Idea nicked from Rystic's TweakMod by Jean Elcard 11/08/2009
	iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
	iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
	sFlammables = ['FOREST', 'FOREST_NEW', 'FOREST_ANCIENT', 'JUNGLE', 'SCRUB']
	iFlammables = [gc.getInfoTypeForString('FEATURE_' + sFeature) for sFeature in sFlammables]
	for iDirection in range(DirectionTypes.NUM_DIRECTION_TYPES):
		pAdjacentPlot = plotDirection(pPlot.getX(), pPlot.getY(), DirectionTypes(iDirection))
		iImprovement = pAdjacentPlot.getImprovementType()
		if iImprovement != -1:
			if gc.getImprovementInfo(iImprovement).isUnique():
				continue
		if pAdjacentPlot.getFeatureType() in iFlammables:
			iRandom = CyGame().getSorenRandNum(100, "FlavourMod: doVolcanoCreation")
			if iRandom < 30:
				pAdjacentPlot.setFeatureType(iFlames, -1)
			elif iRandom < 60:
				pAdjacentPlot.setImprovementType(iSmoke)
# FlavourMod: End Pilferage

def canTriggerWarGamesUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if pUnit.getExperience() < 2:
		return False
	if not pUnit.isAlive():
		return False
	if pUnit.isOnlyDefensive():
		return False
	if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO')):
		return False
	if isWorldUnitClass(pUnit.getUnitClassType()):
		return False
	return True

def applyWBFallOfCuantineRosier1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyGame().setTrophyValue("TROPHY_WB_FALL_OF_CUANTINE_ROSIER_ALLY", 0)

def applyWBFallOfCuantineRosier2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyGame().setTrophyValue("TROPHY_WB_FALL_OF_CUANTINE_ROSIER_ALLY", 1)

def applyWBFallOfCuantineFleeCalabim(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyGame().setTrophyValue("TROPHY_WB_CIV_DECIUS", gc.getInfoTypeForString('CIVILIZATION_CALABIM'))

def applyWBFallOfCuantineFleeMalakim(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyGame().setTrophyValue("TROPHY_WB_CIV_DECIUS", gc.getInfoTypeForString('CIVILIZATION_MALAKIM'))

def applyWBGiftOfKylorinMeshabberRight(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = CyMap().plot(19,16)
	pPlot.setPythonActive(False)
	pPlot = CyMap().plot(20,16)
	pUnit = pPlot.getUnit(0)
	pUnit.kill(True, 0)
	cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_MESHABBER_RIGHT",()),'art/interface/popups/Tya.dds')

def applyWBGiftOfKylorinMeshabberWrong(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot1 = CyMap().plot(19,16)
	pPlot1.setPythonActive(False)
	pPlot2 = CyMap().plot(20,16)
	pUnit = pPlot2.getUnit(0)
	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), False)
	pUnit.attack(pPlot1, False)
	cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_MESHABBER_WRONG",()),'art/interface/popups/Tya.dds')

def applyWBGiftOfKylorinSecretDoorYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = CyMap().plot(23,6)
	pPlot.setPythonActive(False)
	pPlot = CyMap().plot(23,5)
	pPlot.setFeatureType(-1, -1)
	pPlot.setMinLevel(0)
	pPlot.setMoveDisabledAI(False)
	pPlot.setMoveDisabledHuman(False)
			

def applyWBLordOfTheBalorsTemptJudeccaYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	enemyTeam = otherPlayer.getTeam()
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(enemyTeam, False)
	eTeam.setPermanentWarPeace(6, False)
	eTeam.makePeace(6)
	eTeam.declareWar(enemyTeam, True, WarPlanTypes.WARPLAN_TOTAL)
	eTeam.setPermanentWarPeace(enemyTeam, True)
	eTeam.setPermanentWarPeace(6, True)

	otherPlayer.AI_changeAttitudeExtra(iPlayer,-6)

	eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), 1)

	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_JUDECCA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,6)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-6)

def applyWBLordOfTheBalorsTemptSallosYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(7, False)
	eTeam.makePeace(7)
	eTeam.setPermanentWarPeace(7, True)

	eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), 1)


	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_SALLOS'))
	if iLeader != -1:
		cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_SUCCUBUS'), iLeader, 0, pPlayer.getCapitalCity().plot(), iPlayer,-1)
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,6)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-6)

def applyWBLordOfTheBalorsTemptOuzzaYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(8, False)
	eTeam.makePeace(8)
	eTeam.setPermanentWarPeace(8, True)

	eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), 1)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_OUZZA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,6)
	for pyCity in PyPlayer(iPlayer).getCityList():
		pCity = pyCity.GetCy()
		if pCity.getPopulation() > 1:
			pCity.changePopulation(-1)
			cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_MANES'), iLeader, pCity.getPopulation(), pCity.plot(), iPlayer,pPlayer.getStateReligion())

	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-6)

def applyWBLordOfTheBalorsTemptMeresinYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(9, False)
	eTeam.makePeace(9)
	eTeam.setPermanentWarPeace(9, True)

	eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), 1)

	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_MERESIN'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,6)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-6)

def applyWBLordOfTheBalorsTemptStatiusYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(10, False)
	eTeam.makePeace(10)
	eTeam.setPermanentWarPeace(10, True)
	pPlayer2 = gc.getPlayer(10)
	pPlayer2.acquireCity(pCity,False,False)

	eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), 1)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_STATIUS'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,6)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-6)

def applyWBLordOfTheBalorsTemptLetheYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(11, False)
	eTeam.makePeace(11)
	eTeam.setPermanentWarPeace(11, True)

	eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), 1)

	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_LETHE'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,6)
		cf.giftUnitToPlayer(gc.getInfoTypeForString('UNIT_MANES'), iLeader, pUnit.getExperience(), pUnit.plot(), iPlayer, pUnit.getReligion())
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_VARN'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-6)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-6)
	pUnit.kill(True, 0)

def applyWBSplinteredCourtDefeatedAmelanchier3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iLjosalfarTeam = -1
	iDovielloTeam = -1
	iSvartalfarTeam = -1
	CyGame().setTrophyValue("TROPHY_WB_CIV_AMELANCHIER", gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'))
	for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
				iDovielloTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				iLjosalfarTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				iSvartalfarTeam = pLoopPlayer.getTeam()
	if iDovielloTeam != -1 and iLjosalfarTeam != -1 and iSvartalfarTeam != -1:
		eTeam = gc.getTeam(iDovielloTeam)
		if eTeam.isAtWar(iSvartalfarTeam):
			eTeam.makePeace(iSvartalfarTeam)
		if not eTeam.isAtWar(iLjosalfarTeam):
			eTeam.declareWar(iLjosalfarTeam, False, WarPlanTypes.WARPLAN_LIMITED)

def applyWBSplinteredCourtDefeatedThessa3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iLjosalfarTeam = -1
	iCalabimTeam = -1
	iSvartalfarTeam = -1
	CyGame().setTrophyValue("TROPHY_WB_CIV_THESSA", gc.getInfoTypeForString('CIVILIZATION_CALABIM'))
	for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				iCalabimTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				iLjosalfarTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				iSvartalfarTeam = pLoopPlayer.getTeam()
	if iCalabimTeam != -1 and iLjosalfarTeam != -1 and iSvartalfarTeam != -1:
		eTeam = gc.getTeam(iCalabimTeam)
		if eTeam.isAtWar(iSvartalfarTeam):
			eTeam.makePeace(iSvartalfarTeam)
		if not eTeam.isAtWar(iLjosalfarTeam):
			eTeam.declareWar(iLjosalfarTeam, False, WarPlanTypes.WARPLAN_LIMITED)

def applyWBSplinteredCourtDefeatedRivanna3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iLjosalfarTeam = -1
	iCalabimTeam = -1
	iSvartalfarTeam = -1
	CyGame().setTrophyValue("TROPHY_WB_CIV_RIVANNA", gc.getInfoTypeForString('CIVILIZATION_CALABIM'))
	for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				iCalabimTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				iLjosalfarTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				iSvartalfarTeam = pLoopPlayer.getTeam()
	if iCalabimTeam != -1 and iLjosalfarTeam != -1 and iSvartalfarTeam != -1:
		eTeam = gc.getTeam(iCalabimTeam)
		if eTeam.isAtWar(iLjosalfarTeam):
			eTeam.makePeace(iLjosalfarTeam)
		if not eTeam.isAtWar(iSvartalfarTeam):
			eTeam.declareWar(iSvartalfarTeam, False, WarPlanTypes.WARPLAN_LIMITED)

def applyWBSplinteredCourtDefeatedVolanna3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iLjosalfarTeam = -1
	iDovielloTeam = -1
	iSvartalfarTeam = -1
	CyGame().setTrophyValue("TROPHY_WB_CIV_VOLANNA", gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'))
	for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
				iDovielloTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				iLjosalfarTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				iSvartalfarTeam = pLoopPlayer.getTeam()
	if iDovielloTeam != -1 and iLjosalfarTeam != -1 and iSvartalfarTeam != -1:
		eTeam = gc.getTeam(iDovielloTeam)
		if eTeam.isAtWar(iLjosalfarTeam):
			eTeam.makePeace(iLjosalfarTeam)
		if not eTeam.isAtWar(iSvartalfarTeam):
			eTeam.declareWar(iSvartalfarTeam, False, WarPlanTypes.WARPLAN_LIMITED)

def applyWBSplinteredCourtParithYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	CyGame().setTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH", 1)

def canDoWBTheBlackTowerPickCivBannor(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	if CyGame().isHasTrophy("TROPHY_WB_THE_RADIANT_GUARD_CAPRIA_ALLY"):
		return True
	return False

def applyWBTheBlackTowerPickCivBannor(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_BANNOR'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def applyWBTheBlackTowerPickCivHippus(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_HIPPUS'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def applyWBTheBlackTowerPickCivLanun(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_LANUN'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def canDoWBTheBlackTowerPickCivLjosalfar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	if CyGame().isHasTrophy("TROPHY_WB_THE_SPLINTERED_COURT_LJOSALFAR"):
		return True
	return False

def applyWBTheBlackTowerPickCivLjosalfar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def canDoWBTheBlackTowerPickCivLuchuirp(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	if CyGame().isHasTrophy("TROPHY_WB_THE_MOMUS_BEERI_ALLY"):
		return True
	return False

def applyWBTheBlackTowerPickCivLuchuirp(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def canDoWBTheBlackTowerPickCivSvartalfar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	if CyGame().isHasTrophy("TROPHY_WB_THE_SPLINTERED_COURT_SVARTALFAR"):
		return True
	return False

def applyWBTheBlackTowerPickCivSvartalfar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def canDoWBTheBlackTowerPickCivGrigori(argsList):
	return True
##	iEvent = argsList[0]
##	kTriggeredData = argsList[1]
##	if CyGame().isHasTrophy("TROPHY_WB_THE_SPLINTERED_COURT_SVARTALFAR"):
##		return True
##	return False

def applyWBTheBlackTowerPickCivGrigori(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_GRIGORI'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def applyWBTheMomusBeerisOfferYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	gc.getGame().changeTrophyValue("TROPHY_WB_THE_MOMUS_BEERI_ALLY", 1)
	eTeam = gc.getTeam(0) #Falamar
	eTeam7 = gc.getTeam(7) #Beeri
	eTeam.setPermanentWarPeace(1, False)
	eTeam.setPermanentWarPeace(7, False)
	eTeam.declareWar(1, True, WarPlanTypes.WARPLAN_TOTAL)
	eTeam7.declareWar(1, True, WarPlanTypes.WARPLAN_TOTAL)
	eTeam.makePeace(7)
	eTeam.setPermanentWarPeace(1, True)
	eTeam.setPermanentWarPeace(7, True)

def applyWBTheRadiantGuardChooseSidesBasium(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	gc.getGame().setTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_HYBOREM_ALLY", 0)
	gc.getGame().setTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_BASIUM_ALLY", 1)

def applyWBTheRadiantGuardChooseSidesHyborem(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer

	gc.getGame().setTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_HYBOREM_ALLY", 1)
	gc.getGame().setTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_BASIUM_ALLY", 0)
	pPlayerFalamar = gc.getPlayer(0)
	pPlayerBasium = gc.getPlayer(1) #Basium
	pCity = pPlayer.getCapitalCity()

	for pLoopUnit in PyPlayer(iPlayer).getUnitList():
		if gc.getUnitInfo(pLoopUnit.getUnitType()).getReligionType() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
			szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_ABANDON", (pLoopUnit.getName(), ))
			CyInterface().addMessage(0,True,25,szBuffer,'',1,gc.getUnitInfo(pLoopUnit.getUnitType()).getButton(),ColorTypes(7),pLoopUnit.getX(),pLoopUnit.getY(),True,True)
			newUnit = pPlayerBasium.initUnit(pLoopUnit.getUnitType(), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			newUnit.convert(pLoopUnit)

	eTeam = gc.getTeam(0) #Falamar
	eTeam.setPermanentWarPeace(1, False)
	eTeam.setPermanentWarPeace(2, False)
	eTeam.declareWar(1, True, WarPlanTypes.WARPLAN_TOTAL)
	eTeam.makePeace(2)
	eTeam.setPermanentWarPeace(1, True)
	eTeam.setPermanentWarPeace(2, True)

def doWerewolf1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pPlot = cf.findClearPlot(-1, pCity.plot())
	if pPlot != -1:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		bPlayer.initUnit(gc.getInfoTypeForString('UNIT_WEREWOLF'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WEREWOLF_RELEASED", ()),'',1,'Art/Interface/Buttons/Units/Werewolf.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)

def doWerewolf3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WEREWOLF_KILLED", ()),'',1,'Art/Interface/Buttons/Units/Werewolf.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)


######## MARATHON ###########

def canTriggerMarathon(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	team = gc.getTeam(player.getTeam())

	if team.AI_getAtWarCounter(otherPlayer.getTeam()) == 1:
		for loopUnit in PyPlayer(kTriggeredData.eOtherPlayer).getUnitList():
			plot = loopUnit.plot()
			if not plot.isNone():
				if plot.getOwner() == kTriggeredData.ePlayer:
					return True
					
	return False

######## WEDDING FEUD ###########

def doWeddingFeud2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	for pyCity in PyPlayer(kTriggeredData.ePlayer).getCityList():
		loopCity = pyCity.GetCy()
		if loopCity.isHasReligion(kTriggeredData.eReligion):
			loopCity.changeHappinessTimer(30)
	return 1

def getHelpWeddingFeud2(argsList):
	iEvent = argsList[0]
	event = gc.getEventInfo(iEvent)
	kTriggeredData = argsList[1]
	religion = gc.getReligionInfo(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_2_HELP", (gc.getDefineINT("TEMP_HAPPY"), 30, religion.getChar()))

	return szHelp

def canDoWeddingFeud3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.getGold() - 10 * player.getNumCities() < 0:
		return False

	return True

def doWeddingFeud3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	player = gc.getPlayer(kTriggeredData.ePlayer)

	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iLoopPlayer)
		if loopPlayer.isAlive() and loopPlayer.getStateReligion() == player.getStateReligion():
			loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
			player.AI_changeAttitudeExtra(iLoopPlayer, 1)

	if gc.getTeam(destPlayer.getTeam()).canDeclareWar(player.getTeam()):
		if destPlayer.isHuman():
			# this works only because it's a single-player only event
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setText(localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_OTHER_3", (gc.getReligionInfo(kTriggeredData.eReligion).getAdjectiveKey(), player.getCivilizationShortDescriptionKey())))
			popupInfo.setData1(kTriggeredData.eOtherPlayer)
			popupInfo.setData2(kTriggeredData.ePlayer)
			popupInfo.setPythonModule("CvRandomEventInterface")
			popupInfo.setOnClickedPythonCallback("weddingFeud3Callback")
			popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
			popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
			popupInfo.addPopup(kTriggeredData.eOtherPlayer)
		else:
			gc.getTeam(destPlayer.getTeam()).declareWar(player.getTeam(), False, WarPlanTypes.WARPLAN_LIMITED)

	return 1


def weddingFeud3Callback(argsList):
	iButton = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	szText = argsList[4]
	bOption1 = argsList[5]
	bOption2 = argsList[6]

	if iButton == 0:
		destPlayer = gc.getPlayer(iData1)
		player = gc.getPlayer(iData2)
		gc.getTeam(destPlayer.getTeam()).declareWar(player.getTeam(), False, WarPlanTypes.WARPLAN_LIMITED)

	return 0

def getHelpWeddingFeud3(argsList):
	iEvent = argsList[0]
	event = gc.getEventInfo(iEvent)
	kTriggeredData = argsList[1]
	religion = gc.getReligionInfo(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_3_HELP", (1, religion.getChar()))

	return szHelp


######## BABY BOOM ###########

def canTriggerBabyBoom(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	team = gc.getTeam(player.getTeam())

	if team.getAtWarCount(True) > 0:
		return False

	for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
		if iLoopTeam != player.getTeam():
			if team.AI_getAtPeaceCounter(iLoopTeam) == 1:
				return True

	return False


######## LOOTERS ###########

def getHelpLooters3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	city = otherPlayer.getCity(kTriggeredData.iOtherPlayerCityId)

	szHelp = localText.getText("TXT_KEY_EVENT_LOOTERS_3_HELP", (1, 2, city.getNameKey()))

	return szHelp

def canApplyLooters3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	city = otherPlayer.getCity(kTriggeredData.iOtherPlayerCityId)

	iNumBuildings = 0
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			iNumBuildings += 1

	return (iNumBuildings > 0)


def applyLooters3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	city = otherPlayer.getCity(kTriggeredData.iOtherPlayerCityId)

	iNumBuildings = gc.getGame().getSorenRandNum(2, "Looters event number of buildings destroyed")
	iNumBuildingsDestroyed = 0

	listBuildings = []
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listBuildings.append(iBuilding)

	for i in range(iNumBuildings+1):
		if len(listBuildings) > 0:
			iBuilding = listBuildings[gc.getGame().getSorenRandNum(len(listBuildings), "Looters event building destroyed")]
			szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
			CyInterface().addMessage(kTriggeredData.eOtherPlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), gc.getInfoTypeForString("COLOR_RED"), city.getX(), city.getY(), True, True)
			city.setNumRealBuilding(iBuilding, 0)
			iNumBuildingsDestroyed += 1
			listBuildings.remove(iBuilding)

	if iNumBuildingsDestroyed > 0:
		szBuffer = localText.getText("TXT_KEY_EVENT_NUM_BUILDINGS_DESTROYED", (iNumBuildingsDestroyed, gc.getPlayer(kTriggeredData.eOtherPlayer).getCivilizationAdjectiveKey(), city.getNameKey()))
		CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, None, gc.getInfoTypeForString("COLOR_WHITE"), -1, -1, True, True)


######## BROTHERS IN NEED ###########

def canTriggerBrothersInNeed(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	if not player.canTradeNetworkWith(kTriggeredData.eOtherPlayer):
		return False

	listResources = []
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER'))
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_IRON'))
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_HORSE'))
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_IVORY'))

#FfH: Modified by Kael 10/01/2007
#	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_OIL'))
#	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_URANIUM'))
#FfH: End Modify

	bFound = False
	for iResource in listResources:
		if (player.getNumTradeableBonuses(iResource) > 1 and otherPlayer.getNumAvailableBonuses(iResource) <= 0):
			bFound = True
			break

	if not bFound:
		return False

	for iTeam in range(gc.getMAX_CIV_TEAMS()):
		if iTeam != player.getTeam() and iTeam != otherPlayer.getTeam() and gc.getTeam(iTeam).isAlive():
			if gc.getTeam(iTeam).isAtWar(otherPlayer.getTeam()) and not gc.getTeam(iTeam).isAtWar(player.getTeam()):
				return True

	return False

def canDoBrothersInNeed1(argsList):
	kTriggeredData = argsList[1]
	newArgs = (kTriggeredData, )

	return canTriggerBrothersInNeed(newArgs)


######## HURRICANE ###########

def canTriggerHurricaneCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]

	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)

	if city.isNone():
		return False

	if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return False

	if city.plot().getLatitude() <= 0:
		return False

	if city.getPopulation() < 2:
		return False

	return True

def canApplyHurricane1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)

	listBuildings = []
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listBuildings.append(iBuilding)

	return (len(listBuildings) > 0)

def canApplyHurricane2(argsList):
	return (not canApplyHurricane1(argsList))


def applyHurricane1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)

	listCheapBuildings = []
	listExpensiveBuildings = []
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listCheapBuildings.append(iBuilding)
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() > 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listExpensiveBuildings.append(iBuilding)

	if len(listCheapBuildings) > 0:
		iBuilding = listCheapBuildings[gc.getGame().getSorenRandNum(len(listCheapBuildings), "Hurricane event cheap building destroyed")]
		szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
		CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), gc.getInfoTypeForString("COLOR_RED"), city.getX(), city.getY(), True, True)
		city.setNumRealBuilding(iBuilding, 0)

	if len(listExpensiveBuildings) > 0:
		iBuilding = listExpensiveBuildings[gc.getGame().getSorenRandNum(len(listExpensiveBuildings), "Hurricane event expensive building destroyed")]
		szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
		CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), gc.getInfoTypeForString("COLOR_RED"), city.getX(), city.getY(), True, True)
		city.setNumRealBuilding(iBuilding, 0)


######## CYCLONE ###########

def canTriggerCycloneCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]

	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)

	if city.isNone():
		return False

	if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return False

	if city.plot().getLatitude() >= 0:
		return False

	return True


######## MONSOON ###########

def canTriggerMonsoonCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]

	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)

	if city.isNone():
		return False

	if city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return False

	iJungleType = CvUtil.findInfoTypeNum(gc.getFeatureInfo, gc.getNumFeatureInfos(),'FEATURE_JUNGLE')

	for iDX in range(-3, 4):
		for iDY in range(-3, 4):
			pLoopPlot = plotXY(city.getX(), city.getY(), iDX, iDY)
			if not pLoopPlot.isNone() and pLoopPlot.getFeatureType() == iJungleType:
				return True

	return False


######## VOLCANO ###########

def getHelpVolcano1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_VOLCANO_1_HELP", ())

	return szHelp

def canApplyVolcano1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	iNumImprovements = 0
	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			loopPlot = plotXY(kTriggeredData.iPlotX, kTriggeredData.iPlotY, iDX, iDY)
			if not loopPlot.isNone():
				if (iDX != 0 or iDY != 0):
					if loopPlot.getImprovementType() != -1:
							iNumImprovements += 1

	return (iNumImprovements > 0)

def applyVolcano1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	listPlots = []
	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			loopPlot = plotXY(kTriggeredData.iPlotX, kTriggeredData.iPlotY, iDX, iDY)
			if not loopPlot.isNone():
				if (iDX != 0 or iDY != 0):
					if loopPlot.getImprovementType() != -1:
							listPlots.append(loopPlot)

	listRuins = []
	listRuins.append(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_COTTAGE'))
	listRuins.append(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_HAMLET'))
	listRuins.append(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_VILLAGE'))
	listRuins.append(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_TOWN'))

	iRuins = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_CITY_RUINS')

	for i in range(3):
		if len(listPlots) > 0:
			plot = listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Volcano event improvement destroyed")]
			iImprovement = plot.getImprovementType()
			szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getImprovementInfo(iImprovement).getTextKey(), ))
			CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getImprovementInfo(iImprovement).getButton(), gc.getInfoTypeForString("COLOR_RED"), plot.getX(), plot.getY(), True, True)
			if iImprovement in listRuins:
				plot.setImprovementType(iRuins)
			else:
				plot.setImprovementType(-1)
			listPlots.remove(plot)

			if i == 1 and gc.getGame().getSorenRandNum(100, "Volcano event num improvements destroyed") < 50:
				break


######## DUSTBOWL ###########

def canTriggerDustbowlCont(argsList):
	kTriggeredData = argsList[0]

	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)

	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

	if (kOrigTriggeredData == None):
		return False

	iFarmType = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_FARM')
	iPlainsType = CvUtil.findInfoTypeNum(gc.getTerrainInfo,gc.getNumTerrainInfos(),'TERRAIN_PLAINS')

	map = gc.getMap()
	iBestValue = map.getGridWidth() + map.getGridHeight()
	bestPlot = None
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == kTriggeredData.ePlayer and plot.getImprovementType() == iFarmType and plot.getTerrainType() == iPlainsType):
			iValue = plotDistance(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY, plot.getX(), plot.getY())
			if iValue < iBestValue:
				iBestValue = iValue
				bestPlot = plot

	if bestPlot != None:
		kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
		kActualTriggeredDataObject.iPlotX = bestPlot.getX()
		kActualTriggeredDataObject.iPlotY = bestPlot.getY()
	else:
		player.resetEventOccured(trigger.getPrereqEvent(0))
		return False

	return True

def getHelpDustBowl2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_DUSTBOWL_2_HELP", ())

	return szHelp


######## CHAMPION ###########

def canTriggerChampion(argsList):
	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	team = gc.getTeam(player.getTeam())

	if team.getAtWarCount(True) > 0:
		return False

	return True

def canTriggerChampionUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]

	player = gc.getPlayer(ePlayer)
	unit = player.getUnit(iUnit)

	if unit.isNone():
		return False

	if unit.getDamage() > 0:
		return False

	if unit.getDuration() > 0:
		return False

	if unit.getExperience() < 3:
		return False

#FfH: Modified by Kael 09/26/2007
#	iLeadership = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_LEADERSHIP')
	iLeadership = gc.getInfoTypeForString('PROMOTION_HERO')
#FfH: End Modify

	if unit.isHasPromotion(iLeadership):
		return False

	return True

def applyChampion(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)

#FfH: Modified by Kael 10/01/2007
#	iLeadership = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_LEADERSHIP')
	iLeadership = gc.getInfoTypeForString('PROMOTION_HERO')
#FfH: End Modify

	unit.setHasPromotion(iLeadership, True)

def getHelpChampion(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)

#FfH: Modified by Kael 09/26/2007
#	iLeadership = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_LEADERSHIP')
	iLeadership = gc.getInfoTypeForString('PROMOTION_HERO')
#FfH: End Modify

	szHelp = localText.getText("TXT_KEY_EVENT_CHAMPION_HELP", (unit.getNameKey(), gc.getPromotionInfo(iLeadership).getTextKey()))

	return szHelp


######## ANTELOPE ###########

def canTriggerAntelope(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	iDeer = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_DEER')
	iHappyBonuses = 0
	bDeer = False
	for i in xrange(gc.getNumBonusInfos()):
		bonus = gc.getBonusInfo(i)
		iNum = player.getNumAvailableBonuses(i)
		if iNum > 0 :
			if bonus.getHappiness() > 0:
				iHappyBonuses += 1
				if iHappyBonuses > 5:
					return False
			if i == iDeer:
				return False

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not plot.canHaveBonus(iDeer, False):
		return False

	return True

def doAntelope2(argsList):
#	Need this because camps are not normally allowed unless there is already deer.
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

	if not plot.isNone():
		plot.setImprovementType(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_CAMP'))

	return 1

def getHelpAntelope2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	iCamp = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_CAMP')
	szHelp = localText.getText("TXT_KEY_EVENT_IMPROVEMENT_GROWTH", ( gc.getImprovementInfo(iCamp).getTextKey(), ))

	return szHelp


######## WHALEOFATHING ###########

def canTriggerWhaleOfAThing(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	iWhale = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_WHALE')
	iHappyBonuses = 0
	bWhale = False
	for i in range(gc.getNumBonusInfos()):
		bonus = gc.getBonusInfo(i)
		iNum = player.getNumAvailableBonuses(i)
		if iNum > 0 :
			if bonus.getHappiness() > 0:
				iHappyBonuses += 1
				if iHappyBonuses > 5:
					return False
			if i == iWhale:
				return False

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not plot.canHaveBonus(iWhale, False):
		return False

	return True

######## ANCIENT OLYMPICS ###########

def doAncientOlympics2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	map = gc.getMap()

	for j in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(j)
		if j != kTriggeredData.ePlayer and loopPlayer.isAlive() and not loopPlayer.isMinorCiv():

			for i in range(map.numPlots()):
				plot = map.plotByIndex(i)
				if not plot.isWater() and plot.getOwner() == kTriggeredData.ePlayer and plot.isAdjacentPlayer(j, True):
					loopPlayer.AI_changeMemoryCount(kTriggeredData.ePlayer, MemoryTypes.MEMORY_EVENT_GOOD_TO_US, 1)
					break

	return 1

def getHelpModernOlympics(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_SOLO_FLIGHT_HELP_1", (1, ))

	return szHelp


######## HEROIC_GESTURE ###########

def canTriggerHeroicGesture(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	if not gc.getTeam(destPlayer.getTeam()).canChangeWarPeace(player.getTeam()):
		return False

	if gc.getTeam(destPlayer.getTeam()).AI_getWarSuccess(player.getTeam()) <= 0:
		return False

	if gc.getTeam(player.getTeam()).AI_getWarSuccess(destPlayer.getTeam()) <= 0:
		return False

	return True

def doHeroicGesture2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if destPlayer.isHuman():
		# this works only because it's a single-player only event
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(localText.getText("TXT_KEY_EVENT_HEROIC_GESTURE_OTHER_3", (player.getCivilizationAdjectiveKey(), )))
		popupInfo.setData1(kTriggeredData.eOtherPlayer)
		popupInfo.setData2(kTriggeredData.ePlayer)
		popupInfo.setPythonModule("CvRandomEventInterface")
		popupInfo.setOnClickedPythonCallback("heroicGesture2Callback")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
		popupInfo.addPopup(kTriggeredData.eOtherPlayer)
	else:
		destPlayer.forcePeace(kTriggeredData.ePlayer)
		destPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
		player.AI_changeAttitudeExtra(kTriggeredData.eOtherPlayer, 1)

	return

def heroicGesture2Callback(argsList):
	iButton = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	szText = argsList[4]
	bOption1 = argsList[5]
	bOption2 = argsList[6]

	if iButton == 0:
		destPlayer = gc.getPlayer(iData1)
		player = gc.getPlayer(iData2)
		destPlayer.forcePeace(iData2)
		destPlayer.AI_changeAttitudeExtra(iData2, 1)
		player.AI_changeAttitudeExtra(iData1, 1)

	return 0

def getHelpHeroicGesture2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	# Get help text
	szHelp = localText.getText("TXT_KEY_EVENT_ATTITUDE_GOOD", (1, destPlayer.getNameKey()));

	return szHelp


######## GREAT_MEDIATOR ###########

def canTriggerGreatMediator(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	if not gc.getTeam(player.getTeam()).canChangeWarPeace(destPlayer.getTeam()):
		return False

	if gc.getTeam(player.getTeam()).AI_getAtWarCounter(destPlayer.getTeam()) < 10:
		return False

	return True

def doGreatMediator2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if destPlayer.isHuman():
		# this works only because it's a single-player only event
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(localText.getText("TXT_KEY_EVENT_GREAT_MEDIATOR_OTHER_3", (player.getCivilizationAdjectiveKey(), )))
		popupInfo.setData1(kTriggeredData.eOtherPlayer)
		popupInfo.setData2(kTriggeredData.ePlayer)
		popupInfo.setPythonModule("CvRandomEventInterface")
		popupInfo.setOnClickedPythonCallback("greatMediator2Callback")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
		popupInfo.addPopup(kTriggeredData.eOtherPlayer)
	else:
		gc.getTeam(player.getTeam()).makePeace(destPlayer.getTeam())
		destPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
		player.AI_changeAttitudeExtra(kTriggeredData.eOtherPlayer, 1)

	return

def greatMediator2Callback(argsList):
	iButton = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	szText = argsList[4]
	bOption1 = argsList[5]
	bOption2 = argsList[6]

	if iButton == 0:
		destPlayer = gc.getPlayer(iData1)
		player = gc.getPlayer(iData2)
		gc.getTeam(destPlayer.getTeam()).makePeace(player.getTeam())
		destPlayer.AI_changeAttitudeExtra(iData2, 1)
		player.AI_changeAttitudeExtra(iData1, 1)

	return 0

def getHelpGreatMediator2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	# Get help text
	szHelp = localText.getText("TXT_KEY_EVENT_ATTITUDE_GOOD", (1, destPlayer.getNameKey()));

	return szHelp


######## ANCIENT_TEXTS ###########

def doAncientTexts2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:
			loopTeam = gc.getTeam(loopPlayer.getTeam())
			if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
				loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)

	return

def getHelpAncientTexts2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_SOLO_FLIGHT_HELP_1", (1, ))

	return szHelp


######## LITERACY ###########

def canTriggerLiteracy(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	iLibrary = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_LIBRARY')
	if player.getNumCities() > player.getBuildingClassCount(iLibrary):
		return False

	return True

######## ESTEEMEED_PLAYWRIGHT ###########

def canTriggerEsteemedPlaywright(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	# If source civ is operating this Civic, disallow the event to trigger.
	if player.isCivic(CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_SLAVERY')):
		return False

	return True


######## EXPERIENCED_CAPTAIN ###########

def canTriggerExperiencedCaptain(argsList):
	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)

	if unit.isNone():
		return False

	if unit.getExperience() < 7:
		return False

	return True


######## Great Beast ########

def doGreatBeast3(argsList):
	kTriggeredData = argsList[1]

	for pyCity in PyPlayer(kTriggeredData.ePlayer).getCityList():
		loopCity = pyCity.GetCy()
		if loopCity.isHasReligion(kTriggeredData.eReligion):
			loopCity.changeHappinessTimer(40)

def getHelpGreatBeast3(argsList):
	kTriggeredData = argsList[1]
	religion = gc.getReligionInfo(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_GREAT_BEAST_3_HELP", (gc.getDefineINT("TEMP_HAPPY"), 40, religion.getChar()))

	return szHelp


####### Controversial Philosopher ######

def canTriggerControversialPhilosopherCity(argsList):
	ePlayer = argsList[1]
	iCity = argsList[2]

	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)

	if city.isNone():
		return False
	if not city.isCapital():
		return False
	if city.getCommerceRateTimes100(CommerceTypes.COMMERCE_RESEARCH) < 3500:
		return False

	return True

####### Spy Discovered #######


def canDoSpyDiscovered3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.getNumCities() < 4:
		return False

	if player.getCapitalCity().isNone():
		return False

	return True



def canCondemnLuonnotar(argsList):
	if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_7')):
		return False
	if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE')):
		return False
	return True


def doGiggles(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_BALOR'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setName("Giggles, Prince of Hell")
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOBILITY'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUMMONER'), True)

def helpGiggles(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_GIGGLES_HELP", ())
	return szHelp

def doUnharmedMartyrs(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iOne = gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE')
	pCity.setHasReligion(iOne, True, True, True)
	gc.getGame().setHolyCity(iOne, pCity, True)

def doRunewyn(argsList):
	kTriggeredData = argsList[0]
	pPlot0 = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot = cf.findClearPlot(-1, pPlot0)
	if pPlot.isNone() != -1 and not pPlot.isNone():
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_RUNEWYN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)
		if newUnit.canMoveOrAttackInto(pPlot0, False):
			newUnit.attack(pPlot0, False)

def applyWBLordOfTheBalorsTemptHyboremYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(11, False)
	eTeam.makePeace(11)
	eTeam.setPermanentWarPeace(11, True)

	pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))
	pPlayer.convert(gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'))

	eTeam.changeProjectCount(gc.getInfoTypeForString('PROJECT_INFERNAL_PACT'), 1)


	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_HYBOREM'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,6)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-6)

def canDoDragonBonesFanatic(argsList):
	if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_15')):
		return False
##	if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON')):
##		return False
	return True


def canTriggerDiscoverChangeling(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if not pUnit.isAlive():
		return False
	if pUnit.isOnlyDefensive():
		return False
	if pUnit.isImmuneToMagic():
		return False
	if isLimitedUnitClass(pUnit.getUnitClassType()):
		return False
	if pUnit.isAvatarOfCivLeader():
		return False
	if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANGELING')):
		return False
	if pUnit.getUnitCombatType() in [gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'), gc.getInfoTypeForString('UNITCOMBAT_BEAST')]:
		return False
	iUnit = pUnit.getUnitType()
	info = gc.getUnitInfo(iUnit)
	if info.isAbandon():
		return False
	if info.isObject():
		return False
	if cf.findClearPlot(-1, pUnit.plot()) == -1:
		return False
	return True

def applyIgnoreChangeling(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	iRnd = CyGame().getSorenRandNum(100, "Ignored Changeling")
	if iRnd < 35:
		pPlot = pUnit.plot()
		pNewPlot = cf.findClearPlot(-1, pPlot)
		if pNewPlot != -1:
			newUnit = bPlayer.initUnit(pUnit.getUnitType(), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.convert(pUnit)
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANGELING'), True)

def helpIgnoreChangeling(argsList):
	szBuffer = CyTranslator().getText("TXT_KEY_EVENT_IGNORE_CHANGELING_INFO", ())
	return szBuffer

def applyForcePermanentAlliance(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer1 = kTriggeredData.ePlayer
	iPlayer2 = kTriggeredData.eOtherPlayer
	pPlayer1 = gc.getPlayer(iPlayer1)
	pPlayer2 = gc.getPlayer(iPlayer2)
	iTeam1 = pPlayer1.getTeam()
	iTeam2 = pPlayer2.getTeam()
	gc.getTeam(iTeam1).addTeam(iTeam2)

def canDoGovannonLegacy(argsList):
	iHero = gc.getInfoTypeForString('UNITCLASS_GOVANNON')
	if not CyGame().isUnitClassMaxedOut(iHero, 0):
		return False
	for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if pPlayer2.getUnitClassCount(iHero) > 0:
			return False

	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iProm = gc.getInfoTypeForString('PROMOTION_MAGICALLY_LIBERAL')
	(loopUnit, iter) = pPlayer.firstUnit(False)
	while(loopUnit):
		if not loopUnit.isDead(): #is the unit alive and valid?
			if loopUnit.isHasPromotion(iProm):
				return True
		(loopUnit, iter) = pPlayer.nextUnit(iter, False)
	return False

def applyOutlawGovannonsEthics(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	iProm = gc.getInfoTypeForString('PROMOTION_MAGICALLY_LIBERAL')
	for loopUnit in PyPlayer(iPlayer).getUnitList():
		if loopUnit.isHasPromotion(iProm):
			loopUnit.setHasPromotion(iProm, False)

def helpRemoveGovannonsEthics(argsList):
##	return "Removes the Govannon's Ethics promotion from all units"
	iProm = gc.getInfoTypeForString('PROMOTION_MAGICALLY_LIBERAL')
	sDescription = gc.getPromotionInfo(iProm).getDescription()
	szHelp = localText.getText("TXT_KEY_HELP_REMOVE_PROMOTION", (sDescription,))
	return szHelp

def canTriggerSlayerOfAngels(argsList):
	iCiv = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.getCivilizationType() == iCiv:
		return False
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if destPlayer.getCivilizationType() == iCiv:
		return True
	return False

def applyRacismAngel(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iCiv = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
	for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if iCiv == pPlayer2.getCivilizationType():
			pPlayer2.AI_changeAttitudeExtra(iPlayer,-5)

def canTriggerSlayerOfGolems(argsList):
	iCiv = gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP')
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.getCivilizationType() == iCiv:
		return False
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if destPlayer.getCivilizationType() == iCiv:
		return True
	return False

def applyRacismGolem(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iCiv = gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP')
	for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if iCiv == pPlayer2.getCivilizationType():
			pPlayer2.AI_changeAttitudeExtra(iPlayer,-5)

def canTriggerSlayerOfDemons(argsList):
	iCiv = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.getCivilizationType() == iCiv:
		return False
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if destPlayer.getCivilizationType() == iCiv:
		return True
	return False

def applyRacismDemon(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iCiv = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
	for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if iCiv == pPlayer2.getCivilizationType():
			pPlayer2.AI_changeAttitudeExtra(iPlayer,-5)

def canTriggerSlayerOfDwarves(argsList):
	iRace = gc.getInfoTypeForString('PROMOTION_DWARF')
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	iCiv = player.getCivilizationType()
	infoCiv = gc.getCivilizationInfo(iCiv)
	iDefaultRace = infoCiv.getDefaultRace()
	if iDefaultRace == iRace:
		return False
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	iCiv = destPlayer.getCivilizationType()
	infoCiv = gc.getCivilizationInfo(iCiv)
	iDefaultRace = infoCiv.getDefaultRace()
	if iDefaultRace == iRace:
		return True
	return False

def applyRacismDwarf(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iRace = gc.getInfoTypeForString('PROMOTION_DWARF')
	for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if pPlayer2.isAlive():
			iCiv = pPlayer2.getCivilizationType()
			if iCiv > -1:
				infoCiv = gc.getCivilizationInfo(iCiv)
				iDefaultRace = infoCiv.getDefaultRace()
				if iDefaultRace > -1:
					if iDefaultRace == iRace:
						pPlayer2.AI_changeAttitudeExtra(iPlayer,-5)

def canTriggerSlayerOfElves(argsList):
	lRaces = [gc.getInfoTypeForString('PROMOTION_ELF'), gc.getInfoTypeForString('PROMOTION_DARK_ELF')]
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	iCiv = player.getCivilizationType()
	infoCiv = gc.getCivilizationInfo(iCiv)
	iDefaultRace = infoCiv.getDefaultRace()
	if iDefaultRace in lRaces:
		return False
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	iCiv = destPlayer.getCivilizationType()
	infoCiv = gc.getCivilizationInfo(iCiv)
	iDefaultRace = infoCiv.getDefaultRace()
	if iDefaultRace in lRaces:
		return True
	return False

def applyRacismElf(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	lRaces = [gc.getInfoTypeForString('PROMOTION_ELF'), gc.getInfoTypeForString('PROMOTION_DARK_ELF')]
	for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if pPlayer2.isAlive():
			iCiv = pPlayer2.getCivilizationType()
			if iCiv > -1:
				infoCiv = gc.getCivilizationInfo(iCiv)
				iDefaultRace = infoCiv.getDefaultRace()
				if iDefaultRace > -1:
					if iDefaultRace in lRaces:
						pPlayer2.AI_changeAttitudeExtra(iPlayer,-5)

def canTriggerSlayerOfOrcs(argsList):
	iRace = gc.getInfoTypeForString('PROMOTION_ORC')
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	iCiv = player.getCivilizationType()
	infoCiv = gc.getCivilizationInfo(iCiv)
	iDefaultRace = infoCiv.getDefaultRace()
	if iDefaultRace == iRace:
		return False
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	iCiv = destPlayer.getCivilizationType()
	infoCiv = gc.getCivilizationInfo(iCiv)
	iDefaultRace = infoCiv.getDefaultRace()
	if iDefaultRace == iRace:
		return True
	return False

def applyRacismOrc(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iRace = gc.getInfoTypeForString('PROMOTION_ORC')
	for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if pPlayer2.isAlive():
			iCiv = pPlayer2.getCivilizationType()
			if iCiv > -1:
				infoCiv = gc.getCivilizationInfo(iCiv)
				iDefaultRace = infoCiv.getDefaultRace()
				if iDefaultRace > -1:
					if iDefaultRace == iRace:
						pPlayer2.AI_changeAttitudeExtra(iPlayer,-5)

def canTriggerSlayerOfWerewolves(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DUIN')) > 0:
		return False
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if destPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DUIN')) > 0:
		return True
	if destPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_GREATER_WEREWOLF')) > 2:
		return True
	if destPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_WEREWOLF')) > 6:
		return True
	if destPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RAVENOUS_WEREWOLF')) > 12:
		return True
	return False

def applyRacismWerewolf(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer

	iDuin = gc.getInfoTypeForString('UNITCLASS_DUIN')
	iGreaterWerewolf = gc.getInfoTypeForString('UNITCLASS_GREATER_WEREWOLF')
	iWerewolf = gc.getInfoTypeForString('UNITCLASS_WEREWOLF')

	for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if pPlayer2.isAlive():
			iChange = 3*pPlayer2.getUnitClassCount(iDuin) + 2*pPlayer2.getUnitClassCount(iGreaterWerewolf) + pPlayer2.getUnitClassCount(iWerewolf)
			if iChange > 0:
				pPlayer2.AI_changeAttitudeExtra(iPlayer,-iChange)

def applyGraveyard(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer

	iSidar = gc.getInfoTypeForString('CIVILIZATION_SIDAR')
	for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if pPlayer2.getCivilizationType() == iSidar:
			if pPlayer2.isAlive():
				pPlayer2.AI_changeAttitudeExtra(iPlayer,1)

def canSummonHyborem(argsList):
	return canSummonDemonLord(gc.getInfoTypeForString('LEADER_HYBOREM'))

def helpSummonHyborem(argsList):
	return helpSummonDemonLord(gc.getInfoTypeForString('LEADER_HYBOREM'), gc.getInfoTypeForString('UNIT_HYBOREM'), gc.getInfoTypeForString('PROMOTION_PACT_WITH_HYBOREM') )

def doSummonHyborem(argsList):
	iImmortal		= gc.getInfoTypeForString('PROMOTION_IMMORTAL')
	iExtension		= gc.getInfoTypeForString('PROMOTION_EXTENSION1')
	iIronWeapon		= gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
	iMobility1		= gc.getInfoTypeForString('PROMOTION_MOBILITY1')
	iSettleBonus		= gc.getInfoTypeForString('PROMOTION_STARTING_SETTLER')

	liStartingUnits = [	(1,gc.getInfoTypeForString('UNIT_HYBOREM'),[iImmortal, iIronWeapon]),
				(3,gc.getInfoTypeForString('UNIT_LONGBOWMAN'),[iMobility1]),
				(2,gc.getInfoTypeForString('UNIT_SECT_OF_FLIES'),[iMobility1, iIronWeapon]),
				(2,gc.getInfoTypeForString('UNIT_BALOR'),[iMobility1, iIronWeapon, iExtension]),
				(1,gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_VEIL'),[iMobility1, iExtension]),
				(1,gc.getInfoTypeForString('UNIT_DISCIPLE_THE_ASHEN_VEIL'),[iMobility1]),
				(2,gc.getInfoTypeForString('UNIT_HELLHOUND'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_IMP'),[iMobility1, iExtension]),
				(1,gc.getInfoTypeForString('UNIT_GREAT_GENERAL'),[iMobility1]),
				(6,gc.getInfoTypeForString('UNIT_MANES'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_WORKER'),[]),
				(1,gc.getInfoTypeForString('UNIT_SETTLER'),[iSettleBonus])]

	doSummonDemonLord(gc.getInfoTypeForString('LEADER_HYBOREM'), liStartingUnits, argsList)

def canSummonJudecca(argsList):
	return canSummonDemonLord(gc.getInfoTypeForString('LEADER_JUDECCA'))

def helpSummonJudecca(argsList):
	return helpSummonDemonLord(gc.getInfoTypeForString('LEADER_JUDECCA'), gc.getInfoTypeForString('UNIT_JUDECCA'), gc.getInfoTypeForString('PROMOTION_PACT_WITH_JUDECCA') )

def doSummonJudecca(argsList):
	iExtension		= gc.getInfoTypeForString('PROMOTION_EXTENSION1')
	iIronWeapon		= gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
	iMobility1		= gc.getInfoTypeForString('PROMOTION_MOBILITY1')
	iSettleBonus		= gc.getInfoTypeForString('PROMOTION_STARTING_SETTLER')

	liStartingUnits = [	(1,gc.getInfoTypeForString('UNIT_JUDECCA'),[]),
				(1,gc.getInfoTypeForString('UNIT_BALOR'),[iMobility1, iIronWeapon, iExtension]),
				(2,gc.getInfoTypeForString('UNIT_LONGBOWMAN'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_ARCHER'),[iMobility1]),
				(2,gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_VEIL'),[iMobility1, iExtension]),
				(1,gc.getInfoTypeForString('UNIT_DISCIPLE_THE_ASHEN_VEIL'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_MAGE'),[iMobility1, iExtension]),
				(4,gc.getInfoTypeForString('UNIT_IMP'),[iMobility1, iExtension]),
				(1,gc.getInfoTypeForString('UNIT_GREAT_GENERAL'),[iMobility1]),
				(4,gc.getInfoTypeForString('UNIT_MANES'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_WORKER'),[]),
				(1,gc.getInfoTypeForString('UNIT_SETTLER'),[iSettleBonus])]

	doSummonDemonLord(gc.getInfoTypeForString('LEADER_JUDECCA'), liStartingUnits, argsList)

def canSummonLethe(argsList):
	return canSummonDemonLord(gc.getInfoTypeForString('LEADER_LETHE'))

def helpSummonLethe(argsList):
	return helpSummonDemonLord(gc.getInfoTypeForString('LEADER_LETHE'), gc.getInfoTypeForString('UNIT_LETHE'), gc.getInfoTypeForString('PROMOTION_PACT_WITH_LETHE') )

def doSummonLethe(argsList):
	iExtension		= gc.getInfoTypeForString('PROMOTION_EXTENSION1')
	iIronWeapon		= gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
	iMobility1		= gc.getInfoTypeForString('PROMOTION_MOBILITY1')
	iSettleBonus		= gc.getInfoTypeForString('PROMOTION_STARTING_SETTLER')

	liStartingUnits = [	(1,gc.getInfoTypeForString('UNIT_LETHE'),[]),
				(2,gc.getInfoTypeForString('UNIT_LONGBOWMAN'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_ARCHER'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_SECT_OF_FLIES'),[iMobility1, iIronWeapon]),
				(2,gc.getInfoTypeForString('UNIT_ASSASSIN'),[iMobility1]),
				(2,gc.getInfoTypeForString('UNIT_HELLHOUND'),[iMobility1]),
				(2,gc.getInfoTypeForString('UNIT_COLUBRA'),[iMobility1]),
				(2,gc.getInfoTypeForString('UNIT_PRIEST_ESUS'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_DISCIPLE_THE_ASHEN_VEIL'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_BALOR'),[iMobility1, iIronWeapon, iExtension]),
				(1,gc.getInfoTypeForString('UNIT_MAGE'),[iMobility1, iExtension]),
				(2,gc.getInfoTypeForString('UNIT_IMP'),[iMobility1, iExtension]),
				(1,gc.getInfoTypeForString('UNIT_GREAT_GENERAL'),[iMobility1]),
				(4,gc.getInfoTypeForString('UNIT_MANES'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_WORKER'),[]),
				(1,gc.getInfoTypeForString('UNIT_SETTLER'),[iSettleBonus])]

	doSummonDemonLord(gc.getInfoTypeForString('LEADER_LETHE'), liStartingUnits, argsList)

def canSummonMeresin(argsList):
	return canSummonDemonLord(gc.getInfoTypeForString('LEADER_MERESIN'))

def helpSummonMeresin(argsList):
	return helpSummonDemonLord(gc.getInfoTypeForString('LEADER_MERESIN'), gc.getInfoTypeForString('UNIT_MERESIN'), gc.getInfoTypeForString('PROMOTION_PACT_WITH_MERESIN') )

def doSummonMeresin(argsList):
	iExtension		= gc.getInfoTypeForString('PROMOTION_EXTENSION1')
	iIronWeapon		= gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
	iMobility1		= gc.getInfoTypeForString('PROMOTION_MOBILITY1')
	iSettleBonus		= gc.getInfoTypeForString('PROMOTION_STARTING_SETTLER')

	liStartingUnits = [	(1,gc.getInfoTypeForString('UNIT_MERESIN'),[iIronWeapon]),
				(2,gc.getInfoTypeForString('UNIT_LONGBOWMAN'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_ARCHER'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_SECT_OF_FLIES'),[iMobility1, iIronWeapon]),
				(2,gc.getInfoTypeForString('UNIT_DISCIPLE_THE_ASHEN_VEIL'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_BALOR'),[iMobility1, iIronWeapon, iExtension]),
				(2,gc.getInfoTypeForString('UNIT_DISEASED_CORPSE'),[iMobility1, iIronWeapon]),
				(1,gc.getInfoTypeForString('UNIT_IMP'),[iMobility1, iExtension]),
				(1,gc.getInfoTypeForString('UNIT_GREAT_GENERAL'),[iMobility1]),
				(4,gc.getInfoTypeForString('UNIT_MANES'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_WORKER'),[]),
				(1,gc.getInfoTypeForString('UNIT_SETTLER'),[iSettleBonus])]

	doSummonDemonLord(gc.getInfoTypeForString('LEADER_MERESIN'), liStartingUnits, argsList)

def canSummonOuzza(argsList):
	return canSummonDemonLord(gc.getInfoTypeForString('LEADER_OUZZA'))

def helpSummonOuzza(argsList):
	return helpSummonDemonLord(gc.getInfoTypeForString('LEADER_OUZZA'), gc.getInfoTypeForString('UNIT_OUZZA'), gc.getInfoTypeForString('PROMOTION_PACT_WITH_OUZZA') )

def doSummonOuzza(argsList):
	iExtension		= gc.getInfoTypeForString('PROMOTION_EXTENSION1')
	iIronWeapon		= gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
	iMobility1		= gc.getInfoTypeForString('PROMOTION_MOBILITY1')
	iSettleBonus		= gc.getInfoTypeForString('PROMOTION_STARTING_SETTLER')

	liStartingUnits = [	(1,gc.getInfoTypeForString('UNIT_OUZZA'),[iIronWeapon]),
				(1,gc.getInfoTypeForString('UNIT_LONGBOWMAN'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_ARCHER'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_SECT_OF_FLIES'),[iMobility1, iIronWeapon]),
				(5,gc.getInfoTypeForString('UNIT_CHAOS_MARAUDER'),[iMobility1, iIronWeapon]),
				(2,gc.getInfoTypeForString('UNIT_HELLHOUND'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_DISCIPLE_THE_ASHEN_VEIL'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_BALOR'),[iMobility1, iIronWeapon, iExtension]),
				(2,gc.getInfoTypeForString('UNIT_IMP'),[iMobility1, iExtension]),
				(1,gc.getInfoTypeForString('UNIT_GREAT_GENERAL'),[iMobility1]),
				(4,gc.getInfoTypeForString('UNIT_MANES'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_WORKER'),[]),
				(1,gc.getInfoTypeForString('UNIT_SETTLER'),[iSettleBonus])]

	doSummonDemonLord(gc.getInfoTypeForString('LEADER_OUZZA'), liStartingUnits, argsList)

def canSummonSallos(argsList):
	return canSummonDemonLord(gc.getInfoTypeForString('LEADER_SALLOS'))

def helpSummonSallos(argsList):
	return helpSummonDemonLord(gc.getInfoTypeForString('LEADER_SALLOS'), gc.getInfoTypeForString('UNIT_SALLOS'), gc.getInfoTypeForString('PROMOTION_PACT_WITH_SALLOS') )

def doSummonSallos(argsList):
	iExtension		= gc.getInfoTypeForString('PROMOTION_EXTENSION1')
	iIronWeapon		= gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
	iMobility1		= gc.getInfoTypeForString('PROMOTION_MOBILITY1')
	iSettleBonus		= gc.getInfoTypeForString('PROMOTION_STARTING_SETTLER')

	liStartingUnits = [	(1,gc.getInfoTypeForString('UNIT_SALLOS'),[iIronWeapon]),
				(2,gc.getInfoTypeForString('UNIT_LONGBOWMAN'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_ARCHER'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_HELLHOUND'),[iMobility1]),
				(3,gc.getInfoTypeForString('UNIT_SUCCUBUS'),[iMobility1, iIronWeapon]),
				(1,gc.getInfoTypeForString('UNIT_BALOR'),[iMobility1, iIronWeapon, iExtension]),
				(2,gc.getInfoTypeForString('UNIT_IMP'),[iMobility1, iExtension]),
				(1,gc.getInfoTypeForString('UNIT_GREAT_GENERAL'),[iMobility1]),
				(4,gc.getInfoTypeForString('UNIT_MANES'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_WORKER'),[]),
				(1,gc.getInfoTypeForString('UNIT_SETTLER'),[iSettleBonus])]

	doSummonDemonLord(gc.getInfoTypeForString('LEADER_SALLOS'), liStartingUnits, argsList)

def canSummonStatius(argsList):
	return canSummonDemonLord(gc.getInfoTypeForString('LEADER_STATIUS'))

def helpSummonStatius(argsList):
	return helpSummonDemonLord(gc.getInfoTypeForString('LEADER_STATIUS'), gc.getInfoTypeForString('UNIT_STATIUS'), gc.getInfoTypeForString('PROMOTION_PACT_WITH_STATIUS') )

def doSummonStatius(argsList):
	iExtension		= gc.getInfoTypeForString('PROMOTION_EXTENSION1')
	iIronWeapon		= gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
	iMobility1		= gc.getInfoTypeForString('PROMOTION_MOBILITY1')
	iSettleBonus		= gc.getInfoTypeForString('PROMOTION_STARTING_SETTLER')

	liStartingUnits = [	(1,gc.getInfoTypeForString('UNIT_STATIUS'),[iIronWeapon]),
				(2,gc.getInfoTypeForString('UNIT_LONGBOWMAN'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_ARCHER'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_SECT_OF_FLIES'),[iMobility1, iIronWeapon]),
				(1,gc.getInfoTypeForString('UNIT_BALOR'),[iMobility1, iIronWeapon, iExtension]),
				(2,gc.getInfoTypeForString('UNIT_IMP'),[iMobility1, iExtension]),
				(2,gc.getInfoTypeForString('UNIT_GREAT_GENERAL'),[iMobility1]),
				(4,gc.getInfoTypeForString('UNIT_MANES'),[iMobility1]),
				(1,gc.getInfoTypeForString('UNIT_WORKER'),[]),
				(1,gc.getInfoTypeForString('UNIT_SETTLER'),[iSettleBonus])]

	doSummonDemonLord(gc.getInfoTypeForString('LEADER_STATIUS'), liStartingUnits, argsList)

def canSummonDemonLord(iLeader):
	if CyGame().isLeaderEverActive(iLeader):
		iDemonPlayer = cf.getLeader(iLeader)
		if iDemonPlayer != -1:
			pDemonPlayer = gc.getPlayer(iDemonPlayer)
##			if pDemonPlayer.isAlive():
##				return False
			iHero = cf.getHero(pDemonPlayer)
			if pDemonPlayer.getUnitClassCount(iHero) > 0:
				return False
			iUnit = gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_INFERNAL')).getCivilizationUnits(iHero)

			iSluagh = gc.getInfoTypeForString('UNIT_SLUAGH')
			lBoundProm = [	gc.getInfoTypeForString('PROMOTION_NETHERBIND'),
							gc.getInfoTypeForString('PROMOTION_CAPTUS_CAVEAE_ANGELORUM'),
							gc.getInfoTypeForString('PROMOTION_SOUL_FORGED'),
							gc.getInfoTypeForString('PROMOTION_INCARCERATUS_JUDICII')
							]

##			pNetherworld = CyMap().plot(0, 0)
##			for i in xrange(pNetherworld.getNumUnits()):
##				pSluagh = pNetherworld.getUnit(i)
			for pSluagh in PyPlayer(gc.getBARBARIAN_PLAYER()).getUnitList():
				if pSluagh.getScenarioCounter() == iUnit:
					if pSluagh.getUnitType() == iSluagh:
						for iProm in lBoundProm:
							if pSluagh.isHasPromotion(iProm):
								return False

	return True

def helpSummonDemonLord(iLeader, iUnit, iProm=-1):
	szBuffer = ''
	if iProm != -1:
		szBuffer += CyGameTextMgr().getPromotionHelp(iProm, False)

	szBuffer += "\n\nLeader:" + CyGameTextMgr().parseLeaderTraits(iLeader, -1, False, False)
	sHelp = CyGameTextMgr().getUnitHelp(iUnit, False, False, False, None)
	sText = CyTranslator().getText("TXT_KEY_REQUIRES", ())
	iStop = sHelp.find(sText)#I don't want to show Building or bonus prereqs
	if iStop != -1:
		sHelp = sHelp[:iStop]
		iStop = sHelp.rfind("\n")
		if iStop != -1:
			sHelp = sHelp[:iStop]
	iStop = sHelp.find(u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())#I don't want to show a unit's cost in hammers, especially when it is -1
	if iStop != -1:
		sHelp = sHelp[:iStop]
		iStop = sHelp.rfind("\n")
		if iStop != -1:
			sHelp = sHelp[:iStop]
	szBuffer += "\n\nAvatar Unit: " + sHelp


	return szBuffer

def doSummonDemonLord(iDemonLord, liStartingUnits, argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)



	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	sInfernal = "TXT_KEY_POPUP_CONTROL_INFERNAL"
	iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')


	iInfernalPlayer = cf.getLeader(iDemonLord)
	if iInfernalPlayer == -1:
		iInfernalPlayer = pPlayer.initNewEmpire(iDemonLord, iInfernal)
	if iInfernalPlayer != PlayerTypes.NO_PLAYER:
		pInfernalPlayer = gc.getPlayer(iInfernalPlayer)
		pBestPlot = -1
		pAshCity = pInfernalPlayer.getCapitalCity()
		if pAshCity.isNone():
			pAshCity = cf.getInfernalIngress(iPlayer)
		if pAshCity != -1:
			pBestPlot = pAshCity.plot()
			for iLoop in xrange(pBestPlot.getNumUnits(), -1, -1):
				pLoopUnit = pBestPlot.getUnit(iLoop)
				pLoopUnit.jumpToNearestValidPlot()
			pAshCity.setHasReligion(iVeil, True, True, True)
			pAshCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DEMONIC_CITIZENS'), 1)
			pAshCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL'), 1)
			pAshCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MAGE_GUILD'), 1)
			pAshCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_OBSIDIAN_GATE'), 1)
			pAshCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARCHERY_RANGE'), 1)
			pAshCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TRAINING_YARD'), 1)
			pAshCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ELDER_COUNCIL'), 1)
			pInfernalPlayer.acquireCity(pAshCity,False,False)
		if pBestPlot == -1:
			iBestPlot = -1
			for iLoop in xrange (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(iLoop)
				iPlot = -1
				if pInfernalPlayer.canFound(pPlot.getX(), pPlot.getY()):
					if pPlot.getNumUnits() == 0:
						iPlot = CyGame().getSorenRandNum(50, "Place "+ str(pInfernalPlayer.getName()))
						iPlot += 50
						iPlot += pPlot.area().getNumTiles() * 2
						iPlot += pPlot.area().getNumUnownedTiles() * 10
						if pPlot.area().getNumTiles() < 3:
							iPlot -= 500
						if pPlot.isAdjacentOwned():
							iPlot -= 200
						for jPlayer in xrange(gc.getMAX_PLAYERS()):
							lPlayer = gc.getPlayer(jPlayer)
							if lPlayer.isAlive():
								if lPlayer.getCivilizationType() == iInfernal:
									pCapital = lPlayer.getCapitalCity()
									if not pCapital.isNone():
										iDistance = CyMap().calculatePathDistance(pPlot, pCapital.plot())
										if iDistance == -1:
											iPlot += 50
										else:
											iPlot += iDistance
						iX = pPlot.getX()
						iY = pPlot.getY()
						## Check Big Fat Cross for other players, resources and terrain
						for iDirection in xrange(DirectionTypes.NUM_DIRECTION_TYPES):
							pCityPlot = plotDirection(iX, iY, DirectionTypes(iDirection))
							iPlot += (pCityPlot.getYield(YieldTypes.YIELD_PRODUCTION)-2)*20
							iPlot += (pCityPlot.getYield(YieldTypes.YIELD_COMMERCE)-2)*5
							if pPlot.isCity():
								iPlot -= 100
							if pPlot.isAdjacentOwned():
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
					pBestPlot = pPlot

		if pBestPlot != -1:
			if not pBestPlot.isCity():
				pBestPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE'))
				if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS):
					pPlot.setOwner(iInfernalPlayer)

			iFounderTeam = pPlayer.getTeam()
			pFounderTeam = gc.getTeam(iFounderTeam)

			iInfernalTeam = pInfernalPlayer.getTeam()
			pInfernalTeam = gc.getTeam(iInfernalTeam)

			iBarbTeam = gc.getBARBARIAN_TEAM()
			pBarbTeam = gc.getTeam(iBarbTeam)

			pFounderTeam.makePeace(iInfernalTeam)

			pFounderTeam.makePeace(iBarbTeam)

			pInfernalTeam.makePeace(iBarbTeam)
			pFounderTeam.makePeace(iBarbTeam)

			pFounderTeam.signOpenBorders(iBarbTeam)
			pBarbTeam.signOpenBorders(iFounderTeam)

			pInfernalTeam.signOpenBorders(iBarbTeam)
			pBarbTeam.signOpenBorders(iInfernalTeam)

			pFounderTeam.signOpenBorders(iInfernalTeam)
			pInfernalTeam.signOpenBorders(iFounderTeam)

			pFounderTeam.signDefensivePact(iInfernalTeam)
			pInfernalTeam.signDefensivePact(iFounderTeam)

			pInfernalPlayer.setLastStateReligion(iVeil)

			for iNumUnits, iUnit, liPromotions in liStartingUnits:
				for iLoop in xrange(iNumUnits):
					pNewUnit = pInfernalPlayer.initUnit(iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
					for iPromotion in liPromotions:
						pNewUnit.setHasPromotion(iPromotion, True)
					if pNewUnit.getReligion() == -1:
						pNewUnit.setReligion(iVeil)

			for iLoopTeam in xrange(gc.getMAX_TEAMS()):
				if iLoopTeam == iBarbTeam:continue
				pLoopTeam = gc.getTeam(iLoopTeam)
				if pLoopTeam.isAlive():
					if pLoopTeam.isHasMet(iFounderTeam):
						pLoopTeam.meet(iInfernalTeam, True)
					if pLoopTeam.isAtWar(iFounderTeam):
						pInfernalTeam.declareWar(iLoopTeam, False, WarPlanTypes.WARPLAN_LIMITED)

			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS):
				if not pFounderTeam.isHasEmbassy(iInfernalTeam):
					pFounderTeam.setHasEmbassy(iInfernalTeam, True)
				if not pInfernalTeam.isHasEmbassy(iFounderTeam):
					pInfernalTeam.setHasEmbassy(iFounderTeam, True)

				pInfernalTeam.setHasNonAggression(iFounderTeam, True)
				for iLoopTeam in xrange(gc.getMAX_TEAMS()):
					if iLoopTeam == iBarbTeam: continue
					if pFounderTeam.isHasPrepareWar(iLoopTeam) or pFounderTeam.isAtWar(iLoopTeam):
						pInfernalTeam.setHasPrepareWar(iLoopTeam,True)

			pInfernalTeam.changeStolenVisibilityTimer(iFounderTeam,1)
			pFounderTeam.changeStolenVisibilityTimer(iInfernalTeam,1)

			pBestPlot.setRevealed(iFounderTeam, True, False, TeamTypes.NO_TEAM)

			iBasiumPlayer = cf.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
			if iBasiumPlayer != -1:
				gc.getPlayer(iBasiumPlayer).AI_changeAttitudeExtra(iPlayer,-7)

			pInfernalPlayer.AI_changeAttitudeExtra(iPlayer, 5)
			for jPlayer in xrange(gc.getMAX_PLAYERS()):
				if jPlayer != iPlayer and jPlayer != iInfernalPlayer:
					lPlayer = gc.getPlayer(jPlayer)
					if lPlayer.isAlive():
						if lPlayer.getCivilizationType() == iInfernal:
							lPlayer.AI_changeAttitudeExtra(iPlayer,-6)

			if pPlayer.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText(sInfernal,(pInfernalPlayer.getName(),)))
				popupInfo.setData1(iPlayer)
				popupInfo.setData2(iInfernalPlayer)
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_YES", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_NO", ()), "")
				popupInfo.setOnClickedPythonCallback("reassignPlayer")
				popupInfo.addPopup(iPlayer)

def recruitMercenary(sUnitClass, iCost, kTriggeredData):
	iUnitClass = gc.getInfoTypeForString(sUnitClass)
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

	pCity = pPlot.getPlotCity()
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iGold = iCost//10
	iCiv = pPlayer.getCivilizationType()
	iPlayerC = pCity.findHighestCulture()
	if iPlayerC == -1:
		iPlayerC = iPlayer
	pPlayerC = gc.getPlayer(iPlayerC)
	iCivC = pPlayerC.getCivilizationType()
	infoCivC = gc.getCivilizationInfo(iCivC)

	iUnit = infoCivC.getCivilizationUnits(iUnitClass)
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.finishMoves()
		newUnit.setHasCasted(True)
		pCity.applyBuildEffects(newUnit)

		if iCivC != iCiv:
			infoCiv = gc.getCivilizationInfo(iCiv)
			iRace = infoCiv.getDefaultRace()
			if iRace != -1:
				if newUnit.isHasPromotion(iRace):
					newUnit.setHasPromotion(iRace, False)
			iUnitCombat = newUnit.getUnitCombatType()
			iArt = -1
			if iCivC == gc.getInfoTypeForString('CIVILIZATION_AMURITES'):
				if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_ADEPT'):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ARCANE'), True)
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_AMURITES')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_BALSERAPHS'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_BALSERAPHS')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_BANNOR'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_BANNOR')
				if iUnitCombat in [gc.getInfoTypeForString('UNITCOMBAT_ARCHER'), gc.getInfoTypeForString('UNITCOMBAT_MELEE')]:
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GUARDSMAN'), True)
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_CALABIM')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_CLAN_OF_EMBERS')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
				if iUnitCombat in [gc.getInfoTypeForString('"UNITCOMBAT_ANIMAL'), gc.getInfoTypeForString('UNITCOMBAT_BEAST'), gc.getInfoTypeForString('UNITCOMBAT_MELEE'), gc.getInfoTypeForString('UNITCOMBAT_RECON')]:
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SCAVENGER'), True)
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_DOVIELLO')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_ELOHIM')
				if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_DISCIPLE'):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOBILITY1'), True)
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ZEAL'), True)
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_GRIGORI'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_GRIGORI')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_HIPPUS'):
				iGold = 5 * iGold
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_HIPPUS')
				if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_MOUNTED'):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HORSELORD'), True)
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_ILLIANS')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_INFERNAL')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_KHAZAD'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_KHAZAD')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_KURIOTATES')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_LANUN'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_LANUN')
				if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_NAVAL'):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SEAFARING'), True)
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_LJOSALFAR')
				if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_ARCHER'):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEXTEROUS'), True)
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_LUCHUIRP')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_MALAKIM')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_MERCURIANS')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_SHEAIM')
				if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_ADEPT'):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUNDERED'), True)
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_SIDAR')
			elif iCivC == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				iArt = gc.getInfoTypeForString('UNIT_ARTSTYLE_SVARTALFAR')
				if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_RECON'):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SINISTER'), True)
			newUnit.setUnitArtStyleType(iArt)
			iRace = infoCivC.getDefaultRace()
			if iRace != -1:
				if not newUnit.isHasPromotion(iRace):
					newUnit.setHasPromotion(iRace, True)
		if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_HIPPUS'):
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MERCENARY'), True)
		elif pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGNADINE')) > 0:
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MORALE'), True)
		pPlayerC.changeGold(iGold)

def canRecruitMercenary(sUnitClass, kTriggeredData):
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iUnitClass = gc.getInfoTypeForString(sUnitClass)
	if pPlayer.isUnitClassMaxedOut(gc.getUnitInfo(iUnitClass).getUnitClassType(), 0):
		return False
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()

	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	if eTeam.isAtWar(pCity.getTeam()):
		return False
	iPlayerC = pCity.findHighestCulture()
	if iPlayerC == -1:
		iPlayerC = iPlayer
	iCivC = gc.getPlayer(iPlayerC).getCivilizationType()
	if iCivC == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
		if pPlayer.getStateReligion() != gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
			return False
	infoCiv = gc.getCivilizationInfo(iCivC)
	iUnit = infoCiv.getCivilizationUnits(iUnitClass)
	if iUnit != -1:

		if not pPlayer.isHuman():
			if eTeam.getAtWarCount(True) < 1:
				return False
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_KHAZAD'):
				if pPlayer.getGold() / pPlayer.getNumCities() < 700:
					return False
			iCount = 0
			for i in xrange(pPlot.getNumUnits(), 0, -1):
				pUnit = pPlot.getUnit(i)
				if iTeam == pUnit.getTeam():
					iCount += 1
					if iCount > 7:
						return False

		if pCity.canTrain(iUnit, True, False):
			return True
		infoUnit = gc.getUnitInfo(iUnit)

		iBuilding = infoUnit.getPrereqBuilding()
		if iBuilding != -1:
			if pCity.getNumBuilding(iBuilding) < 1:
				return False
		iReligion = infoUnit.getPrereqReligion()
		if iReligion != -1:
			if not pCity.isHasReligion(iReligion):
				return False

		return True
	return False

def helpRecruitMercenary(sUnitClass, kTriggeredData):
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iUnitClass = gc.getInfoTypeForString(sUnitClass)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iPlayerC = pCity.findHighestCulture()
	if iPlayerC == -1:
		iPlayerC = iPlayer
	iCivC = gc.getPlayer(iPlayerC).getCivilizationType()
	infoCiv = gc.getCivilizationInfo(iCivC)
	iUnit = infoCiv.getCivilizationUnits(iUnitClass)
	sDescription = "TXT_KEY_EVENT_HIRE_MERCENARY_UNIT_UNAVAILABLE"
	if iUnit != -1:
		sDescription = gc.getUnitInfo(iUnit).getDescription()
	szHelp = localText.getText("TXT_KEY_EVENT_HIRE_MERCENARY_UNIT_TYPE_HELP", (sDescription,))
	return szHelp

def recruitMercenaryAdept(argsList):
	recruitMercenary('UNITCLASS_ADEPT', 120, argsList[1])
def canRecruitMercenaryAdept(argsList):
	return canRecruitMercenary('UNITCLASS_ADEPT', argsList[1])
def helpRecruitMercenaryAdept(argsList):
	return helpRecruitMercenary('UNITCLASS_ADEPT', argsList[1])

def recruitMercenaryArcher(argsList):
	recruitMercenary('UNITCLASS_ARCHER',80, argsList[1])
def canRecruitMercenaryArcher(argsList):
	return canRecruitMercenary('UNITCLASS_ARCHER', argsList[1])
def helpRecruitMercenaryArcher(argsList):
	return helpRecruitMercenary('UNITCLASS_ARCHER', argsList[1])

def recruitMercenaryArquebus(argsList):
	recruitMercenary('UNITCLASS_ARQUEBUS',240, argsList[1])
def canRecruitMercenaryArquebus(argsList):
	return canRecruitMercenary('UNITCLASS_ARQUEBUS', argsList[1])
def helpRecruitMercenaryArquebus(argsList):
	return helpRecruitMercenary('UNITCLASS_ARQUEBUS', argsList[1])

def recruitMercenaryAssassin(argsList):
	recruitMercenary('UNITCLASS_ASSASSIN',160, argsList[1])
def canRecruitMercenaryAssassin(argsList):
	return canRecruitMercenary('UNITCLASS_ASSASSIN', argsList[1])
def helpRecruitMercenaryAssassin(argsList):
	return helpRecruitMercenary('UNITCLASS_ASSASSIN', argsList[1])

def recruitMercenaryAxeman(argsList):
	recruitMercenary('UNITCLASS_AXEMAN',80, argsList[1])
def canRecruitMercenaryAxeman(argsList):
	return canRecruitMercenary('UNITCLASS_AXEMAN', argsList[1])
def helpRecruitMercenaryAxeman(argsList):
	return helpRecruitMercenary('UNITCLASS_AXEMAN', argsList[1])

def recruitMercenaryBerserker(argsList):
	recruitMercenary('UNITCLASS_BERSERKER',320, argsList[1])
def canRecruitMercenaryBerserker(argsList):
	return canRecruitMercenary('UNITCLASS_BERSERKER', argsList[1])
def helpRecruitMercenaryBerserker(argsList):
	return helpRecruitMercenary('UNITCLASS_BERSERKER', argsList[1])

def recruitMercenaryCatapult(argsList):
	recruitMercenary('UNITCLASS_CATAPULT',120, argsList[1])
def canRecruitMercenaryCatapult(argsList):
	return canRecruitMercenary('UNITCLASS_CATAPULT', argsList[1])
def helpRecruitMercenaryCatapult(argsList):
	return helpRecruitMercenary('UNITCLASS_CATAPULT', argsList[1])

def recruitMercenaryCannon(argsList):
	recruitMercenary('UNITCLASS_CANNON',240, argsList[1])
def canRecruitMercenaryCannon(argsList):
	return canRecruitMercenary('UNITCLASS_CANNON', argsList[1])
def helpRecruitMercenaryCannon(argsList):
	return helpRecruitMercenary('UNITCLASS_CANNON', argsList[1])

def recruitMercenaryChampion(argsList):
	recruitMercenary('UNITCLASS_CHAMPION',160, argsList[1])
def canRecruitMercenaryChampion(argsList):
	return canRecruitMercenary('UNITCLASS_CHAMPION', argsList[1])
def helpRecruitMercenaryChampion(argsList):
	return helpRecruitMercenary('UNITCLASS_CHAMPION', argsList[1])

def recruitMercenaryChaos(argsList):
	recruitMercenary('UNITCLASS_CHAOS_MARAUDER',66, argsList[1])
def canRecruitMercenaryChaos(argsList):
	return canRecruitMercenary('UNITCLASS_CHAOS_MARAUDER', argsList[1])
def helpRecruitMercenaryChaos(argsList):
	return helpRecruitMercenary('UNITCLASS_CHAOS_MARAUDER', argsList[1])

def recruitMercenaryColubra(argsList):
	recruitMercenary('UNITCLASS_COLUBRA',216, argsList[1])
def canRecruitMercenaryColubra(argsList):
	return canRecruitMercenary('UNITCLASS_COLUBRA', argsList[1])
def helpRecruitMercenaryColubra(argsList):
	return helpRecruitMercenary('UNITCLASS_COLUBRA', argsList[1])

def recruitMercenaryCrossbowman(argsList):
	recruitMercenary('UNITCLASS_CROSSBOWMAN',200, argsList[1])
def canRecruitMercenaryCrossbowman(argsList):
	return canRecruitMercenary('UNITCLASS_CROSSBOWMAN', argsList[1])
def helpRecruitMercenaryCrossbowman(argsList):
	return helpRecruitMercenary('UNITCLASS_CROSSBOWMAN', argsList[1])

def recruitMercenaryHorseman(argsList):
	recruitMercenary('UNITCLASS_HORSEMAN',80, argsList[1])
def canRecruitMercenaryHorseman(argsList):
	return canRecruitMercenary('UNITCLASS_HORSEMAN', argsList[1])
def helpRecruitMercenaryHorseman(argsList):
	return helpRecruitMercenary('UNITCLASS_HORSEMAN', argsList[1])

def recruitMercenaryHorseArcher(argsList):
	recruitMercenary('UNITCLASS_HORSE_ARCHER',160, argsList[1])
def canRecruitMercenaryHorseArcher(argsList):
	return canRecruitMercenary('UNITCLASS_HORSE_ARCHER', argsList[1])
def helpRecruitMercenaryHorseArcher(argsList):
	return helpRecruitMercenary('UNITCLASS_HORSE_ARCHER', argsList[1])

def recruitMercenaryHunter(argsList):
	recruitMercenary('UNITCLASS_HUNTER',80, argsList[1])
def canRecruitMercenaryHunter(argsList):
	return canRecruitMercenary('UNITCLASS_HUNTER', argsList[1])
def helpRecruitMercenaryHunter(argsList):
	return helpRecruitMercenary('UNITCLASS_HUNTER', argsList[1])

def recruitMercenaryLongbowman(argsList):
	recruitMercenary('UNITCLASS_LONGBOWMAN',400, argsList[1])
def canRecruitMercenaryLongbowman(argsList):
	return canRecruitMercenary('UNITCLASS_LONGBOWMAN', argsList[1])
def helpRecruitMercenaryLongbowman(argsList):
	return helpRecruitMercenary('UNITCLASS_LONGBOWMAN', argsList[1])

def recruitMercenaryMage(argsList):
	recruitMercenary('UNITCLASS_MAGE',240, argsList[1])
def canRecruitMercenaryMage(argsList):
	return canRecruitMercenary('UNITCLASS_MAGE', argsList[1])
def helpRecruitMercenaryMage(argsList):
	return helpRecruitMercenary('UNITCLASS_MAGE', argsList[1])

def recruitMercenaryNightwatch(argsList):
	recruitMercenary('UNITCLASS_NIGHTWATCH',240, argsList[1])
def canRecruitMercenaryNightwatch(argsList):
	return canRecruitMercenary('UNITCLASS_NIGHTWATCH', argsList[1])
def helpRecruitMercenaryNightwatch(argsList):
	return helpRecruitMercenary('UNITCLASS_NIGHTWATCH', argsList[1])

def recruitMercenaryRanger(argsList):
	recruitMercenary('UNITCLASS_RANGER',300, argsList[1])
def canRecruitMercenaryRanger(argsList):
	return canRecruitMercenary('UNITCLASS_RANGER', argsList[1])
def helpRecruitMercenaryRanger(argsList):
	return helpRecruitMercenary('UNITCLASS_RANGER', argsList[1])

def recruitMercenaryShadow(argsList):
	recruitMercenary('UNITCLASS_SHADOW',480, argsList[1])
def canRecruitMercenaryShadow(argsList):
	return canRecruitMercenary('UNITCLASS_SHADOW', argsList[1])
def helpRecruitMercenaryShadow(argsList):
	return helpRecruitMercenary('UNITCLASS_SHADOW', argsList[1])

def recruitMercenarySuccubus(argsList):
	recruitMercenary('UNITCLASS_SUCCUBUS',169, argsList[1])
def canRecruitMercenarySuccubus(argsList):
	return canRecruitMercenary('UNITCLASS_SUCCUBUS', argsList[1])
def helpRecruitMercenarySuccubus(argsList):
	return helpRecruitMercenary('UNITCLASS_SUCCUBUS', argsList[1])

def doAngryTreants(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	iTreant = gc.getInfoTypeForString('UNIT_TREANT')
	for i in range(4):
		newUnit = bPlayer.initUnit(iTreant, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENRAGED'), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)
	pPlot.setImprovementType(-1)





