# MagisterModMod Events

from CvPythonExtensions import *

import PyHelpers
import CustomFunctions
cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
game = gc.getGame()

localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
def onCombatWithdrawal(argsList):
	"""Fired when an attacker withdraws from combat after doing maximum damage."""
	pAttacker, pDefender = argsList


	if gc.getInfoTypeForString('UNIT_RUNEWYN') in [pAttacker.getUnitType(), pDefender.getUnitType()]:
		pCaster = pAttacker
		pOpponent = pDefender
		if gc.getInfoTypeForString('UNIT_RUNEWYN') == pDefender.getUnitType():
			pCaster = pDefender
			pOpponent = pAttacker
		iX = pOpponent.getX()
		iY = pOpponent.getY()
		iPlayerCaster = pCaster.getOwner()
		pPlayerCaster = gc.getPlayer(iPlayerCaster)
		sNameCaster = "<color=%d,%d,%d,%d>%s</color>" %(pPlayerCaster.getPlayerTextColorR(), pPlayerCaster.getPlayerTextColorG(), pPlayerCaster.getPlayerTextColorB(), pPlayerCaster.getPlayerTextColorA(), pCaster.getName() )
		sNamePlayerCaster = pPlayerCaster.getName()
		iPlayerOpponent = pOpponent.getOwner()
		pPlayerOpponent = gc.getPlayer(iPlayerOpponent)
		sNameOpponent = "<color=%d,%d,%d,%d>%s</color>" %(pPlayerOpponent.getPlayerTextColorR(), pPlayerOpponent.getPlayerTextColorG(), pPlayerOpponent.getPlayerTextColorB(), pPlayerOpponent.getPlayerTextColorA(), pOpponent.getName() )
		sNamePlayerOpponent = pPlayerOpponent.getName()
		pPlot = pOpponent.plot()

		iWard = gc.getInfoTypeForString('IMPROVEMENT_RING_OF_WARDING')
		if pPlot.getImprovementType() == iWard:

			pPlot.setMinLevel(0)
			iReal = pPlot.getRealImprovementType()
			if iReal == iWard:
				pPlot.setImprovementType(-1)
			else:
				pPlot.setImprovementType(iReal)

		if pPlot.isCity():
			pCity = pPlot.getPlotCity()
			if pCaster.getTeam() != pCity.getTeam():
				iPlayerCity = pCity.getOwner()
				pPlayerCity = gc.getPlayer(iPlayerCity)
				sNameCity = "<color=%d,%d,%d,%d>%s</color>" %(pPlayerCity.getPlayerTextColorR(), pPlayerCity.getPlayerTextColorG(), pPlayerCity.getPlayerTextColorB(), pPlayerCity.getPlayerTextColorA(), pCity.getName() )
				sNamePlayerCity = pPlayerCity.getName()
				iX = pPlot.getX()
				iY = pPlot.getY()
				for i in xrange(gc.getNumBuildingInfos()):
					if pCity.getNumRealBuilding(i) > 0:
						if gc.getBuildingInfo(i).isRequiresCaster():
							pCity.setNumRealBuilding(i, 0)
							info = gc.getBuildingInfo(i)
							sDescription = info.getDescription()
							sButton = info.getButton()
							CyInterface().addMessage(iPlayerCaster, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_BUILDING_GOOD", (sNameCaster, sDescription, sNamePlayerCity, sNameCity, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_GREEN'), iX, iY, True, True)
							CyInterface().addMessage(iPlayerCity, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_BUILDING_BAD", (sNamePlayerCaster, sNameCaster, sDescription, sNameCity, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_RED'), iX, iY, True, True)

		for iProm in xrange(gc.getNumPromotionInfos()):
			info = gc.getPromotionInfo(iProm)
			#Remove Spell buffs from opponent's owner's units
			if info.isDispellable():
				sButton = info.getButton()
				sDescription = info.getDescription()
				for iUnit in xrange(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(iUnit)
					if pUnit.isHasPromotion(iProm):
						if pUnit.getOwner() == iPlayerOpponent:
							if pUnit.isImmuneToMagic():continue #Avatars are immune
							pUnit.setHasPromotion(iProm, False)
							pPlayerU = gc.getPlayer(pUnit.getOwner())
							sNameOpponentUnit = "<color=%d,%d,%d,%d>%s</color>" %(pPlayerU.getPlayerTextColorR(), pPlayerU.getPlayerTextColorG(), pPlayerU.getPlayerTextColorB(), pPlayerU.getPlayerTextColorA(), pUnit.getName() )
							CyInterface().addMessage(iPlayerCaster, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_PROMOTION_GOOD", (sNameCaster, sDescription, sNamePlayerOpponent, sNameOpponentUnit, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_GREEN'), iX, iY, True, True)
							CyInterface().addMessage(iPlayerOpponent, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_PROMOTION_BAD", (sNamePlayerCaster, sNameCaster, sDescription, sNameOpponentUnit, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_RED'), iX, iY, True, True)
			#Remove Spell sphere promotions from opponent
			if pOpponent.isHasPromotion(iProm):
				if not pOpponent.isImmuneToMagic(): #Avatars are immune
					iBonus = info.getBonusPrereq()
					if iBonus != -1:
						if gc.getBonusInfo(iBonus).isMana():
							pOpponent.setHasPromotion(iProm, False)
							sDescription = info.getDescription()
							sButton = info.getButton()
							CyInterface().addMessage(iPlayerCaster, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_PROMOTION_GOOD", (sNameCaster, sDescription, sNamePlayerOpponent, sNameOpponent, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_GREEN'), iX, iY, True, True)
							CyInterface().addMessage(iPlayerOpponent, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_PROMOTION_BAD", (sNamePlayerCaster, sNameCaster, sDescription, sNameOpponent, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_RED'), iX, iY, True, True)




	pWinner = pDefender
	pLoser = pAttacker

	iPlayerW = pWinner.getOwner()
	playerX = PyPlayer(iPlayerW)

	iTypeWinner = pWinner.getUnitType()
	unitX = PyInfo.UnitInfo(iTypeWinner)

	iPlayerL = pLoser.getOwner()
	playerY = PyPlayer(iPlayerL)

	iTypeLoser = pLoser.getUnitType()
	unitY = PyInfo.UnitInfo(iTypeLoser)

	iUnitCombatLoser = pLoser.getUnitCombatType()

	pPlayerW = gc.getPlayer(iPlayerW)
	pPlayerL = gc.getPlayer(iPlayerL)

	if CyGame().getSorenRandNum(100,"Scavage Recreater") < 10:
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SCAVENGER')):
			cf.scavenge(pWinner, pLoser)

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
								gc.getInfoTypeForString('PROMOTION_TARGET_WEAKEST')
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
				iProm = listProms[CyGame().getSorenRandNum(len(listProms), "Mimic" + str(pWinner.getName()) + ' slayer of '+ str(pLoser.getName()))]
				infoProm = gc.getPromotionInfo(iProm)
				pWinner.setHasPromotion(iProm, True)
				CyInterface().addMessage(iPlayerW,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PROMOTION_STOLEN", (infoProm.getDescription(),)),'',1,infoProm.getButton(),ColorTypes(8),pWinner.getX(),pWinner.getY(),True,True)
				CyInterface().addMessage(iPlayerL,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PROMOTION_STOLEN", (infoProm.getDescription(),)),'',1,infoProm.getButton(),ColorTypes(7),pWinner.getX(),pWinner.getY(),True,True)
			if iCount >= 20:
				if pPlayerW.isHuman():
					t = "TROPHY_FEAT_MIMIC_20"
					if not CyGame().isHasTrophy(t):
						CyGame().changeTrophyValue(t, 1)

	iX = pWinner.getX()
	iY = pWinner.getY()

	if pLoser.isAlive():
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


		if pLoser.isHasPromotion(iWerewolf):
			if pWinner.isAlive() and pWinner.getDamage() > 0:
				if not pWinner.getUnitCombatType() in [gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'),gc.getInfoTypeForString('UNITCOMBAT_BEAST')]:
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
							if CyGame().getSorenRandNum(200, "Spread Lycanthropy"  + str(pWinner.getName()) + ' slayer of '+ str(pLoser.getName())) < iChance:
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
				if not iUnitCombatLoser in [gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'),gc.getInfoTypeForString('UNITCOMBAT_BEAST')]:
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
							if CyGame().getSorenRandNum(300, "Spread Lycanthropy "  + str(pWinner.getName()) + ' slayer of '+ str(pLoser.getName())) < iChance:
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








##	CyInterface().addImmediateMessage( str("%s withdraws from %s" % ( pAttacker.getName(), pDefender.getName() ) ), "" )

def onCombatRetreat(argsList):
	"""Fired when an attacker retreats from combat, escaping death."""
	pAttacker, pDefender = argsList


	if gc.getInfoTypeForString('UNIT_RUNEWYN') in [pAttacker.getUnitType(), pDefender.getUnitType()]:
		pCaster = pAttacker
		pOpponent = pDefender
		if gc.getInfoTypeForString('UNIT_RUNEWYN') == pDefender.getUnitType():
			pCaster = pDefender
			pOpponent = pAttacker
		iX = pOpponent.getX()
		iY = pOpponent.getY()
		iPlayerCaster = pCaster.getOwner()
		pPlayerCaster = gc.getPlayer(iPlayerCaster)
		sNameCaster = "<color=%d,%d,%d,%d>%s</color>" %(pPlayerCaster.getPlayerTextColorR(), pPlayerCaster.getPlayerTextColorG(), pPlayerCaster.getPlayerTextColorB(), pPlayerCaster.getPlayerTextColorA(), pCaster.getName() )
		sNamePlayerCaster = pPlayerCaster.getName()
		iPlayerOpponent = pOpponent.getOwner()
		pPlayerOpponent = gc.getPlayer(iPlayerOpponent)
		sNameOpponent = "<color=%d,%d,%d,%d>%s</color>" %(pPlayerOpponent.getPlayerTextColorR(), pPlayerOpponent.getPlayerTextColorG(), pPlayerOpponent.getPlayerTextColorB(), pPlayerOpponent.getPlayerTextColorA(), pOpponent.getName() )
		sNamePlayerOpponent = pPlayerOpponent.getName()
		pPlot = pOpponent.plot()

		iWard = gc.getInfoTypeForString('IMPROVEMENT_RING_OF_WARDING')
		if pPlot.getImprovementType() == iWard:

			pPlot.setMinLevel(0)
			iReal = pPlot.getRealImprovementType()
			if iReal == iWard:
				pPlot.setImprovementType(-1)
			else:
				pPlot.setImprovementType(iReal)

		if pPlot.isCity():
			pCity = pPlot.getPlotCity()
			if pCaster.getTeam() != pCity.getTeam():
				iPlayerCity = pCity.getOwner()
				pPlayerCity = gc.getPlayer(iPlayerCity)
				sNameCity = "<color=%d,%d,%d,%d>%s</color>" %(pPlayerCity.getPlayerTextColorR(), pPlayerCity.getPlayerTextColorG(), pPlayerCity.getPlayerTextColorB(), pPlayerCity.getPlayerTextColorA(), pCity.getName() )
				sNamePlayerCity = pPlayerCity.getName()
				iX = pPlot.getX()
				iY = pPlot.getY()
				for i in xrange(gc.getNumBuildingInfos()):
					if pCity.getNumRealBuilding(i) > 0:
						if gc.getBuildingInfo(i).isRequiresCaster():
							pCity.setNumRealBuilding(i, 0)
							info = gc.getBuildingInfo(i)
							sDescription = info.getDescription()
							sButton = info.getButton()
							CyInterface().addMessage(iPlayerCaster, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_BUILDING_GOOD", (sNameCaster, sDescription, sNamePlayerCity, sNameCity, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_GREEN'), iX, iY, True, True)
							CyInterface().addMessage(iPlayerCity, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_BUILDING_BAD", (sNamePlayerCaster, sNameCaster, sDescription, sNameCity, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_RED'), iX, iY, True, True)

		for iProm in xrange(gc.getNumPromotionInfos()):
			info = gc.getPromotionInfo(iProm)
			#Remove Spell buffs from opponent's owner's units
			if info.isDispellable():
				sButton = info.getButton()
				sDescription = info.getDescription()
				for iUnit in xrange(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(iUnit)
					if pUnit.isHasPromotion(iProm):
						if pUnit.getOwner() == iPlayerOpponent:
							if pUnit.isImmuneToMagic():continue #Avatars are immune
							pUnit.setHasPromotion(iProm, False)
							pPlayerU = gc.getPlayer(pUnit.getOwner())
							sNameOpponentUnit = "<color=%d,%d,%d,%d>%s</color>" %(pPlayerU.getPlayerTextColorR(), pPlayerU.getPlayerTextColorG(), pPlayerU.getPlayerTextColorB(), pPlayerU.getPlayerTextColorA(), pUnit.getName() )
							CyInterface().addMessage(iPlayerCaster, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_PROMOTION_GOOD", (sNameCaster, sDescription, sNamePlayerOpponent, sNameOpponentUnit, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_GREEN'), iX, iY, True, True)
							CyInterface().addMessage(iPlayerOpponent, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_PROMOTION_BAD", (sNamePlayerCaster, sNameCaster, sDescription, sNameOpponentUnit, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_RED'), iX, iY, True, True)
			#Remove Spell sphere promotions from opponent
			if pOpponent.isHasPromotion(iProm):
				if not pOpponent.isImmuneToMagic(): #Avatars are immune
					iBonus = info.getBonusPrereq()
					if iBonus != -1:
						if gc.getBonusInfo(iBonus).isMana():
							pOpponent.setHasPromotion(iProm, False)
							sDescription = info.getDescription()
							sButton = info.getButton()
							CyInterface().addMessage(iPlayerCaster, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_PROMOTION_GOOD", (sNameCaster, sDescription, sNamePlayerOpponent, sNameOpponent, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_GREEN'), iX, iY, True, True)
							CyInterface().addMessage(iPlayerOpponent, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_PROMOTION_BAD", (sNamePlayerCaster, sNameCaster, sDescription, sNameOpponent, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_RED'), iX, iY, True, True)




	pWinner = pDefender
	pLoser = pAttacker

	iPlayerW = pWinner.getOwner()
	playerX = PyPlayer(iPlayerW)

	iTypeWinner = pWinner.getUnitType()
	unitX = PyInfo.UnitInfo(iTypeWinner)

	iPlayerL = pLoser.getOwner()
	playerY = PyPlayer(iPlayerL)

	iTypeLoser = pLoser.getUnitType()
	unitY = PyInfo.UnitInfo(iTypeLoser)

	iUnitCombatLoser = pLoser.getUnitCombatType()

	pPlayerW = gc.getPlayer(iPlayerW)
	pPlayerL = gc.getPlayer(iPlayerL)

	if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SCAVENGER')):
		if CyGame().getSorenRandNum(100,"Scavage Recreater") < 10:
			cf.scavenge(pWinner, pLoser)

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
							gc.getInfoTypeForString('PROMOTION_TARGET_WEAKEST')
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
			iProm = listProms[CyGame().getSorenRandNum(len(listProms), "Mimic" + str(pWinner.getName()) + ' slayer of '+ str(pLoser.getName()))]
			infoProm = gc.getPromotionInfo(iProm)
			pWinner.setHasPromotion(iProm, True)
			CyInterface().addMessage(iPlayerW,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PROMOTION_STOLEN", (infoProm.getDescription(),)),'',1,infoProm.getButton(),ColorTypes(8),pWinner.getX(),pWinner.getY(),True,True)
			CyInterface().addMessage(iPlayerL,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PROMOTION_STOLEN", (infoProm.getDescription(),)),'',1,infoProm.getButton(),ColorTypes(7),pWinner.getX(),pWinner.getY(),True,True)
		if iCount >= 20:
			if pPlayerW.isHuman():
				t = "TROPHY_FEAT_MIMIC_20"
				if not CyGame().isHasTrophy(t):
					CyGame().changeTrophyValue(t, 1)

	iX = pWinner.getX()
	iY = pWinner.getY()

	if pLoser.isAlive():
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


		if pLoser.isHasPromotion(iWerewolf):
			if pWinner.isAlive() and pWinner.getDamage() > 0:
				if not pWinner.getUnitCombatType() in [gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'),gc.getInfoTypeForString('UNITCOMBAT_BEAST')]:
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
							if CyGame().getSorenRandNum(200, "Spread Lycanthropy"  + str(pWinner.getName()) + ' slayer of '+ str(pLoser.getName())) < iChance:
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
				if not iUnitCombatLoser in [gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'),gc.getInfoTypeForString('UNITCOMBAT_BEAST')]:
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
							if CyGame().getSorenRandNum(300, "Spread Lycanthropy "  + str(pWinner.getName()) + ' slayer of '+ str(pLoser.getName())) < iChance:
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





##	CyInterface().addImmediateMessage( str( "%s retreats from %s" % ( pAttacker.getName(), pDefender.getName() ) ), "" )

def onCombatDefenderRetreat(argsList):
	"""Fired when a defender retreats from combat, escaping death."""
	pAttacker, pDefender = argsList


	if gc.getInfoTypeForString('UNIT_RUNEWYN') in [pAttacker.getUnitType(), pDefender.getUnitType()]:
		pCaster = pAttacker
		pOpponent = pDefender
		if gc.getInfoTypeForString('UNIT_RUNEWYN') == pDefender.getUnitType():
			pCaster = pDefender
			pOpponent = pAttacker
		iX = pOpponent.getX()
		iY = pOpponent.getY()
		iPlayerCaster = pCaster.getOwner()
		pPlayerCaster = gc.getPlayer(iPlayerCaster)
		sNameCaster = "<color=%d,%d,%d,%d>%s</color>" %(pPlayerCaster.getPlayerTextColorR(), pPlayerCaster.getPlayerTextColorG(), pPlayerCaster.getPlayerTextColorB(), pPlayerCaster.getPlayerTextColorA(), pCaster.getName() )
		sNamePlayerCaster = pPlayerCaster.getName()
		iPlayerOpponent = pOpponent.getOwner()
		pPlayerOpponent = gc.getPlayer(iPlayerOpponent)
		sNameOpponent = "<color=%d,%d,%d,%d>%s</color>" %(pPlayerOpponent.getPlayerTextColorR(), pPlayerOpponent.getPlayerTextColorG(), pPlayerOpponent.getPlayerTextColorB(), pPlayerOpponent.getPlayerTextColorA(), pOpponent.getName() )
		sNamePlayerOpponent = pPlayerOpponent.getName()
		pPlot = pOpponent.plot()

		iWard = gc.getInfoTypeForString('IMPROVEMENT_RING_OF_WARDING')
		if pPlot.getImprovementType() == iWard:

			pPlot.setMinLevel(0)
			iReal = pPlot.getRealImprovementType()
			if iReal == iWard:
				pPlot.setImprovementType(-1)
			else:
				pPlot.setImprovementType(iReal)

		if pPlot.isCity():
			pCity = pPlot.getPlotCity()
			if pCaster.getTeam() != pCity.getTeam():
				iPlayerCity = pCity.getOwner()
				pPlayerCity = gc.getPlayer(iPlayerCity)
				sNameCity = "<color=%d,%d,%d,%d>%s</color>" %(pPlayerCity.getPlayerTextColorR(), pPlayerCity.getPlayerTextColorG(), pPlayerCity.getPlayerTextColorB(), pPlayerCity.getPlayerTextColorA(), pCity.getName() )
				sNamePlayerCity = pPlayerCity.getName()
				iX = pPlot.getX()
				iY = pPlot.getY()
				for i in xrange(gc.getNumBuildingInfos()):
					if pCity.getNumRealBuilding(i) > 0:
						if gc.getBuildingInfo(i).isRequiresCaster():
							pCity.setNumRealBuilding(i, 0)
							info = gc.getBuildingInfo(i)
							sDescription = info.getDescription()
							sButton = info.getButton()
							CyInterface().addMessage(iPlayerCaster, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_BUILDING_GOOD", (sNameCaster, sDescription, sNamePlayerCity, sNameCity, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_GREEN'), iX, iY, True, True)
							CyInterface().addMessage(iPlayerCity, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_BUILDING_BAD", (sNamePlayerCaster, sNameCaster, sDescription, sNameCity, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_RED'), iX, iY, True, True)

		for iProm in xrange(gc.getNumPromotionInfos()):
			info = gc.getPromotionInfo(iProm)
			#Remove Spell buffs from opponent's owner's units
			if info.isDispellable():
				sButton = info.getButton()
				sDescription = info.getDescription()
				for iUnit in xrange(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(iUnit)
					if pUnit.isHasPromotion(iProm):
						if pUnit.getOwner() == iPlayerOpponent:
							if pUnit.isImmuneToMagic():continue #Avatars are immune
							pUnit.setHasPromotion(iProm, False)
							pPlayerU = gc.getPlayer(pUnit.getOwner())
							sNameOpponentUnit = "<color=%d,%d,%d,%d>%s</color>" %(pPlayerU.getPlayerTextColorR(), pPlayerU.getPlayerTextColorG(), pPlayerU.getPlayerTextColorB(), pPlayerU.getPlayerTextColorA(), pUnit.getName() )
							CyInterface().addMessage(iPlayerCaster, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_PROMOTION_GOOD", (sNameCaster, sDescription, sNamePlayerOpponent, sNameOpponentUnit, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_GREEN'), iX, iY, True, True)
							CyInterface().addMessage(iPlayerOpponent, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_PROMOTION_BAD", (sNamePlayerCaster, sNameCaster, sDescription, sNameOpponentUnit, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_RED'), iX, iY, True, True)
			#Remove Spell sphere promotions from opponent
			if pOpponent.isHasPromotion(iProm):
				if not pOpponent.isImmuneToMagic(): #Avatars are immune
					iBonus = info.getBonusPrereq()
					if iBonus != -1:
						if gc.getBonusInfo(iBonus).isMana():
							pOpponent.setHasPromotion(iProm, False)
							sDescription = info.getDescription()
							sButton = info.getButton()
							CyInterface().addMessage(iPlayerCaster, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_PROMOTION_GOOD", (sNameCaster, sDescription, sNamePlayerOpponent, sNameOpponent, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_GREEN'), iX, iY, True, True)
							CyInterface().addMessage(iPlayerOpponent, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_NEGATUS_MYSTERIUM_PROMOTION_BAD", (sNamePlayerCaster, sNameCaster, sDescription, sNameOpponent, )), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, gc.getInfoTypeForString('COLOR_RED'), iX, iY, True, True)




	pWinner = pDefender
	pLoser = pAttacker

	iPlayerW = pWinner.getOwner()
	playerX = PyPlayer(iPlayerW)

	iTypeWinner = pWinner.getUnitType()
	unitX = PyInfo.UnitInfo(iTypeWinner)

	iPlayerL = pLoser.getOwner()
	playerY = PyPlayer(iPlayerL)

	iTypeLoser = pLoser.getUnitType()
	unitY = PyInfo.UnitInfo(iTypeLoser)

	iUnitCombatLoser = pLoser.getUnitCombatType()

	pPlayerW = gc.getPlayer(iPlayerW)
	pPlayerL = gc.getPlayer(iPlayerL)

	if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SCAVENGER')):
		if CyGame().getSorenRandNum(100,"Scavage Recreater") < 10:
			cf.scavenge(pWinner, pLoser)

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
							gc.getInfoTypeForString('PROMOTION_TARGET_WEAKEST')
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
			iProm = listProms[CyGame().getSorenRandNum(len(listProms), "Mimic" + str(pWinner.getName()) + ' slayer of '+ str(pLoser.getName()))]
			infoProm = gc.getPromotionInfo(iProm)
			pWinner.setHasPromotion(iProm, True)
			CyInterface().addMessage(iPlayerW,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PROMOTION_STOLEN", (infoProm.getDescription(),)),'',1,infoProm.getButton(),ColorTypes(8),pWinner.getX(),pWinner.getY(),True,True)
			CyInterface().addMessage(iPlayerL,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PROMOTION_STOLEN", (infoProm.getDescription(),)),'',1,infoProm.getButton(),ColorTypes(7),pWinner.getX(),pWinner.getY(),True,True)
		if iCount >= 20:
			if pPlayerW.isHuman():
				t = "TROPHY_FEAT_MIMIC_20"
				if not CyGame().isHasTrophy(t):
					CyGame().changeTrophyValue(t, 1)

	iX = pWinner.getX()
	iY = pWinner.getY()

	if pLoser.isAlive():
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


		if pLoser.isHasPromotion(iWerewolf):
			if pWinner.isAlive() and pWinner.getDamage() > 0:
				if not pWinner.getUnitCombatType() in [gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'),gc.getInfoTypeForString('UNITCOMBAT_BEAST')]:
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
							if CyGame().getSorenRandNum(200, "Spread Lycanthropy"  + str(pWinner.getName()) + ' slayer of '+ str(pLoser.getName())) < iChance:
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
				if not iUnitCombatLoser in [gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'),gc.getInfoTypeForString('UNITCOMBAT_BEAST')]:
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
							if CyGame().getSorenRandNum(300, "Spread Lycanthropy "  + str(pWinner.getName()) + ' slayer of '+ str(pLoser.getName())) < iChance:
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






##	CyInterface().addImmediateMessage( str( "defender %s retreats from %s" % ( pDefender.getName(), pAttacker.getName() ) ), "" )
