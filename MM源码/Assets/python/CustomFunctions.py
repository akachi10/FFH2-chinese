## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import FfHDefines # lfgr 04/2021

# globals
gc = CyGlobalContext()
ffhDefines = FfHDefines.getInstance() # lfgr 04/2021
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

class CustomFunctions:

	# Set up containers for cached data.
	def __init__(self):
		self.__siIgnoreFire = set()

	@property
	def siIgnoreFire(self):
		# Cached data is initialized the first time that it is read. This prevents assertions while the game is loading.
		if len(self.__siIgnoreFire) > 0:
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_ANOINTED'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_BLESSED'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_CONSECRATED'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_DIVINE'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_EXALTED'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_FINAL'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_DEMONIC_CITIZENS'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_DWARVEN_VAULT'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_DWARVEN_VAULT_ABUNDANT'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_DWARVEN_VAULT_EMPTY'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_DWARVEN_VAULT_FULL'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_DWARVEN_VAULT_LOW'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_DWARVEN_VAULT_OVERFLOWING'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_DWARVEN_VAULT_STOCKED'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_TOWER_OF_ALTERATION'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_TOWER_OF_DIVINATION'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_TOWER_OF_MASTERY'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_TOWER_OF_NECROMANCY'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_TOWER_OF_THE_ELEMENTS'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_PLANAR_GATE'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_CHANCEL_OF_GUARDIANS'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_TEMPLE_BROTHERHOOD'))
			self.__siIgnoreFire.add(gc.getInfoTypeForString('BUILDING_APHOTIC_THRONE'))

		return self.__siIgnoreFire

	def addBonus(self, iBonus, iNum, sIcon):
		listPlots = []
		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.canHaveBonus(gc.getInfoTypeForString(iBonus),True) and pPlot.getBonusType(-1) == -1 and not pPlot.isCity():
				listPlots.append(pPlot)
		iCount = 0
		while iCount < iNum and len(listPlots) > 0:
			iCount += 1
			pPlot = listPlots.pop(CyGame().getSorenRandNum(len(listPlots), "Add Bonus"))
			pPlot.setBonusType(gc.getInfoTypeForString(iBonus))
			if sIcon != -1:
				iActivePlayer = CyGame().getActivePlayer()
				CyInterface().addMessage(iActivePlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RESOURCE_DISCOVERED",()),'AS2D_DISCOVERBONUS',1,sIcon,ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)

	def addBonusWithinBorders(self, iBonus, iNum, sIcon, iPlayer):
		listPlots = []
		for i in PyPlayer(iPlayer).getPlotIDList():
			pPlot = CyMap().plotByIndex(i)
			if pPlot.canHaveBonus(gc.getInfoTypeForString(iBonus),True) and pPlot.getBonusType(-1) == -1 and not pPlot.isCity():
				listPlots.append(pPlot)
		iCount = 0
		while iCount < iNum and len(listPlots) > 0:
			iCount += 1
			pPlot = listPlots.pop(CyGame().getSorenRandNum(len(listPlots), "Add Bonus"))
			pPlot.setBonusType(gc.getInfoTypeForString(iBonus))
			if sIcon != -1:
				iActivePlayer = CyGame().getActivePlayer()
				CyInterface().addMessage(iActivePlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RESOURCE_DISCOVERED",()),'AS2D_DISCOVERBONUS',1,sIcon,ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)

	def addPopup(self, szText, sDDS):
		szTitle = CyGameTextMgr().getTimeStr(CyGame().getGameTurn(), False)
		popup = PyPopup.PyPopup(-1)
		popup.addDDS(sDDS, 0, 0, 128, 384)
		popup.addSeparator()
		popup.setHeaderString(szTitle)
		popup.setBodyString(szText)
		popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

	def addPlayerPopup(self, szText, iPlayer):
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(szText)
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_CLOSE", ()), "")
		popupInfo.addPopup(iPlayer)

	def addUnit(self, iUnit, iPlayer=gc.getBARBARIAN_PLAYER()):
		pBestPlot = -1
		iBestPlot = -1
		iUnitInfo = gc.getUnitInfo(iUnit)
		bSea = iUnitInfo.getDomainType() == gc.getInfoTypeForString('DOMAIN_SEA') or iUnitInfo.getFreePromotions(gc.getInfoTypeForString('PROMOTION_WATER_WALKING'))
		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iPlot = -1
			if pPlot.getNumUnits() == 0:
				if not pPlot.isCity():
					if not pPlot.isImpassable() or iUnitInfo.isCanMoveImpassable():
						if (pPlot.isWater() and bSea) or (not pPlot.isWater() and not bSea):
							iPlot = CyGame().getSorenRandNum(500, "Add Unit")
							iPlot += pPlot.area().getNumTiles() * 10
							if pPlot.isOwned():
								iPlot /= 2
								if pPlot.getOwner() == iPlayer:
									iPlot += 200
							if iPlot > iBestPlot:
								iBestPlot = iPlot
								pBestPlot = pPlot
		if iBestPlot != -1:
			bPlayer = gc.getPlayer(iPlayer)
			newUnit = bPlayer.initUnit(iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			return newUnit

	def addLair(self, iImprovement, bSea=False, bPeak=False):
		pBestPlot = -1
		iBestPlot = -1
		info = gc.getImprovementInfo(iImprovement)
		iBonus = info.getBonusConvert()
		#bPeak = info.isRequiresPeak()#Not exposed to python
		bPeak = iImprovement == gc.getInfoTypeForString('IMPROVEMENT_WYRMHOLD_FANG')
		bSea = info.isWater()
		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iPlot = -1
			if pPlot.getNumUnits() == 0:
				if not pPlot.isCity():
					if pPlot.isPeak() == bPeak:
						if pPlot.isWater() == bSea:
							iPlot = CyGame().getSorenRandNum(500, "Add Improvement")
							iPlot += pPlot.area().getNumTiles() * 10
							if pPlot.isOwned():
								iPlot /= 5
								if pPlot.getOwner() == gc.getBARBARIAN_PLAYER():
									iPlot += 200
							if pPlot.getBonusType(-1) == iBonus:
								iPlot += 500
									
							if iPlot > iBestPlot:
								iBestPlot = iPlot
								pBestPlot = pPlot
		if iBestPlot != -1:
			pBestPlot.setImprovementType(iImprovement)
			return pBestPlot

	def getNameWithColorScheme(self, pUnit, bInvisible=False):
		if pUnit == -1:
			return ''
		if pUnit.isNone():
			return ''
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_SLUAGH'):
			return ''
		if bInvisible:
			return CyTranslator().getText("TXT_KEY_UNKNOWN", ())
		pPlayer = gc.getPlayer(pUnit.getOwner())
		if pPlayer == -1:
			return ''
		if pUnit.isHiddenNationality():
			pPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		return "<color=%d,%d,%d,%d>%s</color>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), pUnit.getName() )

	def addUnitFixed(self, pCaster, iUnit):
		pPlot = pCaster.plot()
		pNewPlot = self.findClearPlot(-1, pPlot)
		if pNewPlot != -1:
			pPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
			newUnit = pPlayer.initUnit(iUnit, pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			return newUnit
		return -1

	def doCrusade(self, iPlayer):
		iCrusadeChance = gc.getDefineINT('CRUSADE_SPAWN_CHANCE')
		iDemagog = gc.getInfoTypeForString('UNIT_DEMAGOG')
		iEnclave = gc.getInfoTypeForString('IMPROVEMENT_ENCLAVE')
		iTown = gc.getInfoTypeForString('IMPROVEMENT_TOWN')
		iVillage = gc.getInfoTypeForString('IMPROVEMENT_VILLAGE')
		pPlayer = gc.getPlayer(iPlayer)
		iReligion = pPlayer.getStateReligion()
		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getImprovementType() in [iTown, iEnclave]:
				if pPlot.getOwner() == iPlayer :
##--------		Unofficial Bug Fix: Added by Denev		--------##
# To prevent spawning demagog in the same tile with his enemy unit.
					if not pPlot.isVisibleEnemyUnit(iPlayer):
##--------		Unofficial Bug Fix: End Add				--------##
						if CyGame().getSorenRandNum(100, "Crusade") < iCrusadeChance:
							newUnit = pPlayer.initUnit(iDemagog, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
							pCity = CyMap().findCity(pPlot.getX(), pPlot.getY(), iPlayer, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, pPlayer.getCity(-1))
							if not pCity.isNone():
								pCity.applyBuildEffects(newUnit)
							newUnit.setReligion(iReligion)
							pPlot.setImprovementType(iVillage)

	def doFear(self, pVictim, pPlot, pCaster, bResistable=True):
		if pVictim.getDuration() > 0:
			return False
		if bResistable:
			if pVictim.isImmuneToFear():
				return False
			if pCaster != -1:
				if CyGame().getSorenRandNum(100, "Resist Fear") < pVictim.getResistChance(pCaster, gc.getInfoTypeForString('SPELL_ROAR')):
					return False
		iX = pVictim.getX()
		iY = pVictim.getY()
		pBestPlot = -1
		iBestPlot = 0
		if pVictim == -1:
			return False
		iPlayer = pVictim.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isNone():
			return False
		iTeam = pPlayer.getTeam()
		eTeam = gc.getTeam(iTeam)
		

		for iDirection in xrange(DirectionTypes.NUM_DIRECTION_TYPES):
			pLoopPlot = plotDirection(iX, iY, DirectionTypes(iDirection))
			if not pLoopPlot.isNone():
				if not pLoopPlot.isVisibleEnemyUnit(pVictim.getOwner()):
					if pVictim.canMoveOrAttackInto(pLoopPlot, False):
						if abs(pLoopPlot.getX() - pPlot.getX()) > 1 or abs(pLoopPlot.getY() - pPlot.getY()) > 1:
							iRnd = CyGame().getSorenRandNum(500, "Fear")
							
							if pPlot.isOwned():
								if pPlot.getOwner() == iPlayer:
									iRnd += 200
								elif pPlot.getTeam() == iTeam:
									iRnd += 100
								elif eTeam.isAtWar(pPlot.getTeam()):
									iRnd -= 200
								if pCaster != -1:
									if pPlot.getOwner() == pCaster.getOwner():
										iRnd -= 200
									elif pPlot.getTeam() == pCaster.getTeam():
										iRnd += 100

							if iRnd > iBestPlot:
								iBestPlot = iRnd
								pBestPlot = pLoopPlot
		if pBestPlot != -1:
			pVictim.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True)
			return True
		return False

	# lfgr 08/2019: utility function
	def filterBarbarianUnitSpawnList( self, lList ) :
		"""
		Takes a list that has elements of the form "UnitType" or ("UnitType", "TechType").
		Removes all elements with a tech the barbarians don't have, converts the other
		("UnitType", "TechType") elements from tuples to simple "UnitType" strings.
		"""
		pBarbPlayer = gc.getPlayer( gc.getBARBARIAN_PLAYER() )
		for item in lList :
			if isinstance( item, str ) :
				yield item
			else :
				sUnit, sTech = item
				if pBarbPlayer.isHasTech( gc.getInfoTypeForString( sTech ) ) :
					yield sUnit

	# lfgr 08/2019: Added tech prereqs
	def exploreLairBigBad(self, pCaster):
		iPlayer = pCaster.getOwner()
		pPlot = pCaster.plot()
		iPlayer = pCaster.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		CvUtil.pyPrint( "exploreLairBigBad" )

		lList = ['UNIT_DJINN']
		
		lPromoList = [	'PROMOTION_MUTATED',
						'PROMOTION_CANNIBALIZE',
						'PROMOTION_MOBILITY1',
						'PROMOTION_STRONG',
						'PROMOTION_BLITZ',
						'PROMOTION_COMMAND1',
						'PROMOTION_HEROIC_STRENGTH',
						'PROMOTION_HEROIC_DEFENSE',
						'PROMOTION_MAGIC_IMMUNE',
						'PROMOTION_STONESKIN',
						'PROMOTION_VALOR',
						'PROMOTION_VILE_TOUCH'
						]
		lHenchmanList = [	'UNIT_AZER',
							'UNIT_GRIFFON'
							]
		if not self.grace():
			lList += [	'UNIT_AIR_ELEMENTAL',
						'UNIT_RUNEWYN',
						'UNIT_AZER',
						'UNIT_MANTICORE'
						]
		if not pPlot.isWater():


			lList += [	'UNIT_ASSASSIN',
						'UNIT_OGRE',
						'UNIT_GIANT_SPIDER',
						'UNIT_HILL_GIANT',
						'UNIT_SPECTRE',
						'UNIT_SCORPION'
						]
			lHenchmanList += [	'UNIT_AXEMAN',
								'UNIT_WOLF',
								'UNIT_CHAOS_MARAUDER',
								'UNIT_WOLF_RIDER',
								'UNIT_MISTFORM',
								'UNIT_LION',
								'UNIT_TIGER',
								'UNIT_BABY_SPIDER',
								'UNIT_FAWN',
								'UNIT_SCORPION'
								]
			if not self.grace():
				lList += [	'UNIT_EARTH_ELEMENTAL',
							'UNIT_FIRE_ELEMENTAL',
							'UNIT_GARGOYLE',
							'UNIT_BRUJAH',
							'UNIT_MYCONID',
							'UNIT_EIDOLON',
							'UNIT_LICH',
							'UNIT_OGRE_WARCHIEF',
							'UNIT_SATYR',
							'UNIT_WEREWOLF'
							]
				lPromoList += [	'PROMOTION_FIRE2',
								'PROMOTION_AIR2',
								'PROMOTION_HERO',
								'PROMOTION_MARKSMAN',
								'PROMOTION_SHADOWWALK'
								]
				lHenchmanList += ['UNIT_OGRE']
				if pPlot.getFeatureType() in [gc.getInfoTypeForString('FEATURE_FOREST'), gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT')]:
					lList += ['UNIT_TREANT']
			iTerrain = pPlot.getTerrainType()
			if iTerrain == gc.getInfoTypeForString('TERRAIN_SNOW'):
				lList += ['UNIT_HOLLOW_MAN']
				lHenchmanList += [	'UNIT_FROSTLING_ARCHER',
									'UNIT_FROSTLING_WOLF_RIDER',
									'UNIT_POLAR_BEAR',
									'UNIT_HOLLOW_MAN'
									]
			elif iTerrain in [gc.getInfoTypeForString('TERRAIN_WASTELAND'), gc.getInfoTypeForString('TERRAIN_GLACIER')]:
				lList += [	'UNIT_HOLLOW_MAN',
							'UNIT_NIVE',
							'UNIT_TAR_DEMON'
							]
				lHenchmanList += [	'UNIT_FROSTLING_ARCHER',
							'UNIT_FROSTLING_WOLF_RIDER',
							'UNIT_NIVE',
							'UNIT_HOLLOW_MAN'
							]
			iImprovement = pPlot.getImprovementType()
			if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BARROW'):
				lPromoList += ['PROMOTION_DEATH2']
				lHenchmanList += [	'UNIT_SKELETON',
									'UNIT_PYRE_ZOMBIE']
				if not self.grace():
					lList += ['UNIT_WRAITH']

			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_PYRE_OF_THE_SERAPHIC'):
				lPromoList += [	'PROMOTION_FIRE1',
								'PROMOTION_FIRE2',
								'PROMOTION_FIRE3',
								'PROMOTION_FIRE3',
								'PROMOTION_ORC'
								]
				lHenchmanList += [	'UNIT_FIREBALL',
									'UNIT_PRIEST_EMBER_LEGION',
									'UNIT_AZER',
									'UNIT_PYRE_ZOMBIE',
									'UNIT_SERAPH'
									]
				if not self.grace():
					lList += [	'UNIT_SERAPH',
								'UNIT_SERAPH',
								'UNIT_SERAPH',
								'UNIT_SERAPH',
								'UNIT_IFRIT',
								'UNIT_BALOR',
								'UNIT_BALOR',
								'UNIT_PRIEST_EMBER_LEGION',
								'UNIT_FIRE_ELEMENTAL'
								]

			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER'):

				lPromoList += [	'PROMOTION_ROTTING_FLESH',
								'PROMOTION_DEATH1',
								'PROMOTION_DEATH2',
								'PROMOTION_DISEASED',
								'PROMOTION_GALLOWBLIGHT'
								]
				lHenchmanList += [	'UNIT_ROTTING_WOLF',
									'UNIT_ROTTING_TROLL',
									'UNIT_SKELETON',
									'UNIT_SPECTRE',
									'UNIT_PYRE_ZOMBIE']
				if not self.grace():
					lList += [	'UNIT_ROTTING_WOLF',
								'UNIT_LICH',
								'UNIT_ROTTING_WOLF',
								'UNIT_DISEASED_CORPSE',
								'UNIT_ROTTING_TROLL'
								]


			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_GRIGI_ABATTOIR'):
				lPromoList += [	'PROMOTION_BODY1',
								'PROMOTION_BODY2',
								'PROMOTION_BODY3',
								'PROMOTION_MUTATED',
								'PROMOTION_CRAZED',
								'PROMOTION_BURNING_BLOOD'
								]
				lHenchmanList += [	'UNIT_GRIFFON',
									'UNIT_FREAK',
									'UNIT_PEGASUS',
									'UNIT_SABERTOOTH',
									'UNIT_CENTAUR',
									'UNIT_LIZARDMAN',
									'UNIT_COLUBRA',
									'UNIT_ADEPT_LAMIA',
									'UNIT_MUSTEVAL_SCOUT',
									'UNIT_MUSTEVAL_HUNTER',
									'UNIT_HILL_GIANT',
									'UNIT_MANTICORE',
									'UNIT_FLESH_GOLEM']
				if not self.grace():
					lList += [	'UNIT_MAGE_LAMIA',
								'UNIT_ARCHMAGE_LAMIA',
								'UNIT_COLUBRA',
								'UNIT_CENTAUR_CHARGER',
								'UNIT_CENTAUR_ARCHER',
								'UNIT_CENTAUR_LANCER',
								'UNIT_MINOTAUR',
								'UNIT_MUSTEVAL_BEASTMASTER',
								'UNIT_MUSTEVAL_ASSASSIN',
								'UNIT_MUSTEVAL_RANGER',
								'UNIT_SPIDERKIN',
								'UNIT_LIZARDMAN_DRUID',
								'UNIT_LIZARDMAN_ASSASSIN',
								'UNIT_LIZARDMAN_RANGER',
								'UNIT_LIZARDMAN_BEASTMASTER',
								'UNIT_MANTICORE'
								]


			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS'):
				lPromoList += [	'PROMOTION_ICE1',
								'PROMOTION_ICE2',
								'PROMOTION_ICE3'
								]
				lHenchmanList += [	'UNIT_HOLLOW_MAN',
									'UNIT_NIVE',
									'UNIT_ICE_ELEMENTAL',
									'UNIT_ICE_GOLEM']
				if not self.grace():
					lList += [	'UNIT_HOLLOW_MAN',
								'UNIT_NIVE',
								'UNIT_FROST_GIANT'
								]
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_PALUS'):
				lPromoList += [	'PROMOTION_MIND2',
								'PROMOTION_MIND3',
								'PROMOTION_MAGIC_IMMUNE',
								'PROMOTION_GUARDSMAN'
								]
				lHenchmanList += [	'UNIT_IRON_GOLEM',
									'UNIT_WOOD_GOLEM'
									]
				if not self.grace():
					lList += [	'UNIT_NULLSTONE_GOLEM',
								'UNIT_CLOCKWORK_GOLEM',
								'UNIT_IRON_GOLEM'
								]
			elif iImprovement == gc.getInfoTypeForString('IMPROVEMENT_RUINS'):
				lPromoList += ['PROMOTION_POISONED_BLADE']
				lHenchmanList += [	'UNIT_LIZARDMAN',
									'UNIT_GORILLA'
									]
				if not self.grace():
					lList += ['UNIT_MANTICORE']
			else:#It is possible for another
				if self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_WHISPERING_WOOD')):
					lPromoList += ['PROMOTION_SHADOW2']
					lHenchmanList += [	'UNIT_SPECTRE',
								'UNIT_MISTFORM']
					if not self.grace():
						lList += ['UNIT_WRAITH']
				if self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_BARROW')):
					lPromoList += ['PROMOTION_DEATH2']
					lHenchmanList += [	'UNIT_SKELETON',
								'UNIT_PYRE_ZOMBIE']
					if not self.grace():
						lList += ['UNIT_WRAITH']
				elif self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS')):
					lPromoList += [	'PROMOTION_ICE1',
									'PROMOTION_ICE2',
									'PROMOTION_ICE3'
									]
					lHenchmanList += [	'UNIT_HOLLOW_MAN',
										'UNIT_HOLLOW_MAN',
										'UNIT_NIVE',
										'UNIT_ICE_ELEMENTAL',
										'UNIT_ICE_GOLEM',
										'UNIT_TAR_DEMON'
										]
					if not self.grace():
						lList += [	'UNIT_NIVE',
									'UNIT_FROST_GIANT',
									'UNIT_TAR_DEMON'
									]

				elif self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_SOULEN_ARCHWAY')):
					lPromoList += [	'PROMOTION_DIMENSIONAL1',
									'PROMOTION_DIMENSIONAL2',
									'PROMOTION_EARTH1',
									'PROMOTION_EARTH2',
									'PROMOTION_ENCHANTMENT1',
									'PROMOTION_ENCHANTMENT2',
									'PROMOTION_PERFECT_SIGHT',
									'PROMOTION_SPIRIT_GUIDE',
									'PROMOTION_AFFINITY_EARTH',
									'PROMOTION_AFFINITY_SPIRIT',
									'PROMOTION_AFFINITY_DIMENSIONAL',
									'PROMOTION_SUNDERED',
									'PROMOTION_SUMMONER']
					lHenchmanList += [	'UNIT_MOBIUS_WITCH',
										'UNIT_DWARVEN_SOLDIER_RUNES',
										'UNIT_DWARVEN_SLINGER',
										'UNIT_EMRYS',
										'UNIT_SHADE',
										'UNIT_IMP']
					lList += [	'UNIT_IMP',
								'UNIT_MOBIUS_WITCH']
					if not self.grace():
						lList += [	'UNIT_MOBIUS_WITCH',
									'UNIT_EMRYS',
									'UNIT_MANTICORE']


				elif self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_ABADDONS_PIT')):
					lPromoList += [	'PROMOTION_ENTROPY1',
									'PROMOTION_ENTROPY2',
									'PROMOTION_ENTROPY3',
									'PROMOTION_EARTH1',
									'PROMOTION_EARTH2',
									'PROMOTION_EARTH3',
									'PROMOTION_MOUNTAINEER',
									'PROMOTION_RUSTED',
									'PROMOTION_AFFINITY_ENTROPY',
									'PROMOTION_PACT_WITH_JUDECCA',
									'PROMOTION_DWARF_SLAYING']
					lHenchmanList += [	'UNIT_DWARVEN_SOLDIER_RUNES',
										'UNIT_DWARVEN_SOLDIER_RUNES',
										'UNIT_DWARVEN_SLINGER',
										'UNIT_SCORPION',
										'UNIT_PARAMANDER',
										'UNIT_IMP']
					lList += [	'UNIT_IMP',
								'UNIT_DWARVEN_SOLDIER_RUNES']
					if not self.grace():
						lList += [	'UNIT_BALOR',
									'UNIT_DWARVEN_SOLDIER_RUNES',
									'UNIT_DWARVEN_DRUID',
									'UNIT_PARAMANDER',
									'UNIT_HORNGUARD',
									'UNIT_MANTICORE']


				elif self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_GRAVE_OF_ASMODAY')):
					lPromoList += [	'PROMOTION_ENTROPY1',
									'PROMOTION_ENTROPY2',
									'PROMOTION_ENTROPY3',
									'PROMOTION_VILE_TOUCH',
									'PROMOTION_RUSTED',
									'PROMOTION_AFFINITY_ENTROPY',
									'PROMOTION_PACT_WITH_SALLOS',
									'PROMOTION_ELF_SLAYING']
					lHenchmanList += [	'UNIT_IMP',
										'UNIT_HELLHOUND',
										'UNIT_SUCCUBUS',
										'UNIT_MANES',
										'UNIT_SKELETON',
										'UNIT_SPECTRE',
										'UNIT_DROWN',
										'UNIT_SCORPION',
										'UNIT_MOBIUS_WITCH']
					lList += [	'UNIT_MOBIUS_WITCH',
								'UNIT_SPECTRE']
					if not self.grace():
						lList += [	'UNIT_BALOR',
									'UNIT_SUCCUBUS',
									'UNIT_BEAST_OF_AGARES',
									'UNIT_EIDOLON']

				elif self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_CLOCKWORK_CITY')):
					lPromoList += [	
									'PROMOTION_ENCHANTMENT1',
									'PROMOTION_ENCHANTMENT2',
									'PROMOTION_ENCHANTMENT3',
									'PROMOTION_ENCHANTED_BLADE',
									'PROMOTION_GOLEM',
									'PROMOTION_GOLEM',
									'PROMOTION_GOLEM',
									'PROMOTION_GOLEM',
									'PROMOTION_GOLEM']
					lHenchmanList += [	'UNIT_IRON_GOLEM',
										'UNIT_WOOD_GOLEM',
										'UNIT_MUD_GOLEM']
					if not self.grace():
						lList += [	'UNIT_NULLSTONE_GOLEM',
									'UNIT_CLOCKWORK_GOLEM',
									'UNIT_IRON_GOLEM',
									'UNIT_GARGOYLE',
									'UNIT_AUTOMATON',
									'UNIT_PRIEST_RINGGIVER'
									'UNIT_HIGH_PRIEST_RINGGIVER']


				elif self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_PALUS')):
					lPromoList += [	'PROMOTION_MIND2',
									'PROMOTION_MIND3',
									'PROMOTION_MAGIC_IMMUNE',
									'PROMOTION_GUARDSMAN']
					lHenchmanList += [	'UNIT_IRON_GOLEM',
										'UNIT_WOOD_GOLEM']
					if not self.grace():
						lList += [	'UNIT_NULLSTONE_GOLEM',
									'UNIT_CLOCKWORK_GOLEM',
									'UNIT_IRON_GOLEM']
				elif self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_RUINS')):
					lPromoList += ['PROMOTION_POISONED_BLADE']
					lHenchmanList += [	'UNIT_LIZARDMAN',
										'UNIT_GORILLA']
					if not self.grace():
						lList += ['UNIT_MANTICORE']
			if CyGame().getGlobalCounter() > 40:
				lList += [	'UNIT_PIT_BEAST',
							'UNIT_DEATH_KNIGHT',
							'UNIT_BALOR']
				lPromoList += [	'PROMOTION_FEAR',
								'PROMOTION_UNHOLY_TAINT']
				lHenchmanList += [	'UNIT_IMP',
							'UNIT_HELLHOUND']
		if pPlot.isWater():
			lList += [	'UNIT_SEA_SERPENT',
						'UNIT_STYGIAN_GUARD',
						'UNIT_PIRATE']
			lHenchmanList += ['UNIT_DROWN']
			if not self.grace():
				lList += [	'UNIT_WATER_ELEMENTAL',
						'UNIT_KRAKEN']
				if self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE')):
					lList += ['UNIT_KRAKEN']
					if CyGame().getUnitCreatedCount(gc.getInfoTypeForString('UNIT_LEVIATHAN')) == 0:
						lList += ['UNIT_LEVIATHAN']
		sMonster = lList.pop(CyGame().getSorenRandNum(len(lList), "Pick Monster"))
		sHenchman = lHenchmanList.pop(CyGame().getSorenRandNum(len(lHenchmanList), "Pick Henchman"))
		sPromo = lPromoList.pop(CyGame().getSorenRandNum(len(lPromoList), "Pick Promotion"))
		iUnit = gc.getInfoTypeForString(sMonster)
		iHenchman = gc.getInfoTypeForString(sHenchman)
##		pPlot2 = self.findClearPlot(-1, pPlot)
##		if pPlot2 != -1:
##			for i in xrange(pPlot.getNumUnits(), -1, -1):
##				pUnit = pPlot.getUnit(i)
##				pUnit.setXY(pPlot2.getX(), pPlot2.getY(), True, True, True)
##		else:
##			pCaster.kill(True,0)
		for i in xrange(pPlot.getNumUnits(), -1, -1):
			pUnit = pPlot.getUnit(i)
			if not pUnit.isBarbarian():
				if not pUnit.jumpToNearestValidPlot():
					CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_DEATH", (pUnit.getName(),)),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)

		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
##		newUnit = self.addUnitFixed(pCaster,iUnit)#I think this is obsolete code from base FfH2, which would create an extra boss unit without HN or UNITAI_LAIRGUARDIAN
		iHN = gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY')
		iExile = gc.getInfoTypeForString('PROMOTION_EXILE')
		iX = pPlot.getX()
		iY = pPlot.getY()
		newUnit = bPlayer.initUnit(iUnit, iX, iY, UnitAITypes.UNITAI_LAIRGUARDIAN, DirectionTypes.DIRECTION_SOUTH)
		if newUnit != -1:
			newUnit.setHasPromotion(gc.getInfoTypeForString(sPromo), True)
			newUnit.setHasPromotion(iExile, True)
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAIR_GUARDIAN'), True)
			newUnit.setName(self.MarnokNameGenerator(newUnit))
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_BIGBAD",()),'',1,gc.getUnitInfo(iUnit).getButton(),ColorTypes(7), iX, iY,True,True)
			for i in xrange (CyGame().getSorenRandNum(5, "Pick Henchmen")):
				newUnit2 = bPlayer.initUnit(iHenchman, iX, iY, UnitAITypes.UNITAI_ANIMAL, DirectionTypes.DIRECTION_SOUTH)
				newUnit2.setHasPromotion(iHN , True)
				newUnit2.setHasPromotion(iExile, True)
		return 0

	def exploreLairBad(self, pCaster):
		iPlayer = pCaster.getOwner()
		pPlot = pCaster.plot()
		pPlayer = gc.getPlayer(pCaster.getOwner())
		iHN = gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY')
		iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
		lList = ['COLLAPSE']
		info = gc.getUnitInfo(pCaster.getUnitType())
		if not info.isObject() and info.getTier() + pCaster.getLevel() < 4:
			lList += ['DEATH']

		if self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_GRAVE_OF_ASMODAY')) or self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_TAPESTRY_HOUSE')):
			lList += ['SPAWN_SUCCUBUS']

		if pCaster.isAlive() and not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DRAGON')):
			if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMUNE_DISEASE')):
				if not (pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MEDIC2')) or pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_LIFE'))):
					if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DISEASED')):
						lList += ['DISEASED']
					if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PLAGUED')):
						lList += ['PLAGUED']
					if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_WITHERED')):
						lList += ['WITHERED']
				if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED')):
					lList += ['POISONED']
			if not pCaster.isOnlyDefensive():
				if not (pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT3'))or pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AFFINITY_SPIRIT'))):
					if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENRAGED')):
						lList += ['ENRAGED']
					if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED')):
						lList += ['CRAZED']
					if not (pPlayer.getCivilizationType() == iMercurians or pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_EXORCIST')) or pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON_SLAYING')) or pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BLESSED')) or pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_POSSESSED'))):
						lList += ['DEMONIC_POSSESSION']

		if pCaster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_MELEE') or pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS')) or pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')) or pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MITHRIL_WEAPONS')):
			lList += ['RUSTED']
		if pPlot.isWater():
			lList += ['SPAWN_DROWN', 'SPAWN_SEA_SERPENT']
		else:
			lList += ['SPAWN_SPIDER', 'SPAWN_SPECTRE']

		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_GOBLIN_FORT'):
			lList += ['SPAWN_SCORPION_BAD', 'SPAWN_SCORPION_BAD', 'SPAWN_SCORPION_BAD']
		sGoody = lList.pop(CyGame().getSorenRandNum(len(lList), "Pick Goody"))
		if sGoody == 'DEATH':
			pCaster.kill(True,0)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_DEATH", (pCaster.getName(),)),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
			return 0
		elif sGoody == 'COLLAPSE':
			pCaster.doDamageNoCaster(50, 90, gc.getInfoTypeForString('DAMAGE_PHYSICAL'), False)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_COLLAPSE", ()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'CRAZED':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_CRAZED", ()),'',1,'Art/Interface/Buttons/Promotions/Crazed.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
			return 80
		elif sGoody == 'DEMONIC_POSSESSION':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENRAGED'), True)
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POSSESSED'), True)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_POSSESSED", ()),'',1,'Art/Interface/Buttons/Units/UCDemon.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
			return 80
		elif sGoody == 'DISEASED':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DISEASED'), True)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_DISEASED", ()),'',1,'Art/Interface/Buttons/Promotions/Diseased.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
			return 80
		elif sGoody == 'ENRAGED':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENRAGED'), True)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_ENRAGED", ()),'',1,'Art/Interface/Buttons/Promotions/Enraged.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
			return 80
		elif sGoody == 'PLAGUED':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PLAGUED'), True)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_PLAGUED", ()),'',1,'Art/Interface/Buttons/Promotions/Plagued.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
			return 80
		elif sGoody == 'POISONED':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED'), True)
			pCaster.doDamageNoCaster(25, 90, gc.getInfoTypeForString('DAMAGE_POISON'), False)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_POISONED", ()),'',1,'Art/Interface/Buttons/Promotions/Poisoned.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
			return 80
		elif sGoody == 'WITHERED':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WITHERED'), True)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_WITHERED", ()),'',1,'Art/Interface/Buttons/Promotions/Withered.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
			return 80
		elif sGoody == 'RUSTED':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RUSTED'), True)
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), False)
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS'), False)
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MITHRIL_WEAPONS'), False)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_RUSTED", ()),'',1,'Art/Interface/Buttons/Promotions/Rusted.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
			return 80
		elif sGoody == 'SPAWN_DROWN':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_SPAWN_DROWN'), pCaster)
			return 50
		elif sGoody == 'SPAWN_SCORPION_BAD':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_SPAWN_SCORPION_BAD'), pCaster)
			return 50
		elif sGoody == 'SPAWN_SEA_SERPENT':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_SPAWN_SEA_SERPENT'), pCaster)
			return 50
		elif sGoody == 'SPAWN_SPECTRE':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_GRAVE_SPECTRE'), pCaster)
			return 50
		elif sGoody == 'SPAWN_SUCCUBUS':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_GRAVE_SUCCUBUS'), pCaster)
			return 50
		elif sGoody == 'SPAWN_SPIDER':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_SPAWN_SPIDER'), pCaster)
			return 50
		return 100

	def exploreLairNeutral(self, pCaster):
		iPlayer = pCaster.getOwner()
		pPlot = pCaster.plot()
		pPlayer = gc.getPlayer(pCaster.getOwner())
		lList = ['NOTHING']
		if not pPlot.isWater():
			lList += ['SPAWN_SKELETON', 'SPAWN_LIZARDMAN', 'SPAWN_SPIDER', 'PORTAL', 'DEPTHS', 'DWARF_VS_LIZARDMEN', 'CAGE']
			if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
				lList += ['SPAWN_FROSTLING']
			iImp = pPlot.getImprovementType()
			if iImp == gc.getInfoTypeForString('IMPROVEMENT_BARROW'):
				lList += ['SPAWN_SKELETON', 'SPAWN_SKELETON']
			elif iImp == gc.getInfoTypeForString('IMPROVEMENT_RUINS'):
				lList += ['SPAWN_LIZARDMAN', 'SPAWN_LIZARDMAN']
			elif iImp == gc.getInfoTypeForString('IMPROVEMENT_GOBLIN_FORT'):
				lList += ['SPAWN_SCORPION', 'SPAWN_SCORPION', 'SPAWN_SCORPION']



		if pPlot.isWater():
			lList += ['SPAWN_DROWN']
		if pCaster.isAlive():
			if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MUTATED')):
				lList += ['MUTATED']
		sGoody = lList.pop(CyGame().getSorenRandNum(len(lList), "Pick Goody"))
		if sGoody == 'CAGE':
			pPlotCage = self.findClearPlotImprovement(pPlot)
			if pPlotCage != -1:
				pPlotCage.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_CAGE'))
				for i in xrange(pPlot.getNumUnits(), -1, -1):
					pUnit = pPlot.getUnit(i)
					pUnit.setXY(pPlotCage.getX(), pPlotCage.getY(), False, True, True)
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_CAGE",()),'',1,'Art/Interface/Buttons/Improvements/Cage.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)
			return 0
		elif sGoody == 'DEPTHS':
			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(), 'EVENTTRIGGER_EXPLORE_LAIR_DEPTHS')
			pPlayer.initTriggeredData(iEvent, True, -1, pCaster.getX(), pCaster.getY(), pCaster.getOwner(), -1, -1, -1, pCaster.getID(), -1)
			return 100
		elif sGoody == 'DWARF_VS_LIZARDMEN':
			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(), 'EVENTTRIGGER_EXPLORE_LAIR_DWARF_VS_LIZARDMEN')
			pPlayer.initTriggeredData(iEvent, True, -1, pCaster.getX(), pCaster.getY(), pCaster.getOwner(), -1, -1, -1, pCaster.getID(), -1)
			return 100
		elif sGoody == 'MUTATED':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MUTATED'), True)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_MUTATED",()),'',1,'Art/Interface/Buttons/Promotions/Mutated.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)
			return 50
		elif sGoody == 'NOTHING':
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_NOTHING",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'SPAWN_DROWN':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_SPAWN_DROWN'), pCaster)
			return 50
		elif sGoody == 'SPAWN_FROSTLING':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_SPAWN_FROSTLING'), pCaster)
			return 50
		elif sGoody == 'SPAWN_LIZARDMAN':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_SPAWN_LIZARDMAN'), pCaster)
			return 50
		elif sGoody == 'SPAWN_SCORPION':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_SPAWN_SCORPION'), pCaster)
			return 50
		elif sGoody == 'SPAWN_SKELETON':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_SPAWN_SKELETON'), pCaster)
			return 50
		elif sGoody == 'SPAWN_SPIDER':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_SPAWN_SPIDER'), pCaster)
			return 50
		return 100

	def exploreLairGood(self, pCaster):
		iPlayer = pCaster.getOwner()
		pPlot = pCaster.plot()
		pPlayer = gc.getPlayer(pCaster.getOwner())
		iTeam = pPlayer.getTeam()
		eTeam = gc.getTeam(pPlayer.getTeam())
		iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
		iSidar = gc.getInfoTypeForString('CIVILIZATION_SIDAR')
		iCiv = pPlayer.getCivilizationType()
		bInfernal = iCiv == iInfernal
		bMercurians = iCiv == iMercurians
		bSidar = iCiv == iSidar

		bMystic = eTeam.isHasTech(gc.getInfoTypeForString('TECH_PRIESTHOOD'))
		bPriest = eTeam.isHasTech(gc.getInfoTypeForString('TECH_RELIGIOUS_LAW'))
		bFanatic = eTeam.isHasTech(gc.getInfoTypeForString('TECH_THEOLOGY'))

		lList = ['HIGH_GOLD', 'TREASURE', 'EXPERIENCE']
		if pCaster.isAlive():
			if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT_GUIDE')):
				lList += ['SPIRIT_GUIDE']
		if not pPlot.isWater():
			lList += ['ITEM_HEALING_SALVE', 'SUPPLIES']
			if bMystic or bPriest or bFanatic:
				if not bInfernal:
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_0')):#iEmpyrean
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')):
							lList += ['PRISONER_DISCIPLE_EMPYREAN']
							if bPriest:
								lList += ['PRISONER_PRIEST_EMPYREAN_EMPYREAN']
							if bFanatic:
								lList += ['PRISONER_RADIANT_GUARD_EMPYREAN']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_1')):#iBrotherhood
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS')):
							lList += ['PRISONER_DISCIPLE_SIRONA']
							if bPriest:
								lList += ['PRISONER_PRIEST_SIRONA']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_2')):#iRinggiver
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_RINGGIVER')):
							lList += ['PRISONER_DISCIPLE_RINGGIVER']
							if bPriest:
								lList += ['PRISONER_PRIEST_RINGGIVER']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_3')):#iUnblemished
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_UNBLEMISHED')):
							lList += ['PRISONER_DISCIPLE_UNBLEMISHED']
							if bPriest:
								lList += ['PRISONER_DRUID']
							if bFanatic:
								lList += ['PRISONER_HOSPITALLER']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_4')):#iPlenty
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_HOUSE_OF_PLENTY')):
							lList += ['PRISONER_DISCIPLE_PLENTY']
							if bPriest:
								lList += ['PRISONER_PRIEST_PLENTY']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_5')):#iOrder
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_THE_ORDER')):
							lList += ['PRISONER_DISCIPLE_ORDER']
							if bPriest:
								lList += ['PRISONER_PRIEST_ORDER']
							if bFanatic:
								lList += ['PRISONER_CRUSADER_ORDER']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_6')):#iMatronae
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_MATRONAE')):
							if bPriest:
								lList += ['PRISONER_APOSTATE']
							if bFanatic:
								lList += ['PRISONER_WITCH_HUNTER']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_7')):#iOne
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE')):
							if pPlayer.getStateReligion() == -1:
								if bPriest:
									lList += ['PRISONER_LUONNOTAR']

				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_8')):#iEternalCabal
					if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL')):
						lList += ['PRISONER_DISCIPLE_ARAWN']
						if bPriest:
							lList += ['PRISONER_PRIEST_ARAWN']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_9')):#iLaeran
					if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_LAERAN_CORD')):
						lList += ['PRISONER_DISCIPLE_LAERAN']
						if bPriest:
							lList += ['PRISONER_PRIEST_LAERAN']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_10')):#iUndertow
					if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS')):
						if not bMercurians:
							lList += ['PRISONER_DISCIPLE_OVERLORDS']
							if bPriest:
								lList += ['PRISONER_PRIEST_OVERLORDS']
							if bFanatic:
								lList += ['PRISONER_STYGIAN_GUARD_OVERLORDS']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_11')):#iGrey
					if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_GREY_COUNCIL')):
						lList += ['PRISONER_DISCIPLE_GREY']
						if bPriest:
							lList += ['PRISONER_PRIEST_GREY']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_12')):#iRunes
					if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH')):
						if not bInfernal:
							lList += ['PRISONER_DISCIPLE_RUNES']
							if bPriest:
								lList += ['PRISONER_PRIEST_RUNES']
						if bFanatic:
							lList += ['PRISONER_PARAMANDER_RUNES']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_13')):#iLeaves
					if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')):
						lList += ['PRISONER_DISCIPLE_LEAVES']
						if bPriest:
							lList += ['PRISONER_PRIEST_LEAVES']
						if bFanatic:
							lList += ['PRISONER_SATYR_LEAVES']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_14')):#iFoxmen
					if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_FOXMEN')):
						lList += ['PRISONER_DISCIPLE_FOXMEN']
						if bPriest:
							lList += ['PRISONER_PRIEST_FOXMEN']
				if not bMercurians:
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_15')):#iDragonCult
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON')):
							lList += ['PRISONER_PRIEST_DRAGON']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_16')):#iEsus
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS')):
							if bPriest:
								lList += ['PRISONER_PRIEST_ESUS']
							if bFanatic:
								lList += ['PRISONER_NIGHTWATCH_ESUS']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_17')):#iHand
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_WHITE_HAND')):
							lList += ['PRISONER_DISCIPLE_HAND']
							if bPriest:
								lList += ['PRISONER_PRIEST_HAND']
							if bFanatic:
								if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
									lList += ['PRISONER_HOLLOW_MAN']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_18')):#iStewards
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY')):
							lList += ['PRISONER_DISCIPLE_STEWARD']
							if bPriest:
								lList += ['PRISONER_PRIEST_STEWARD']
							if bFanatic:
								lList += ['PRISONER_CONDOTTIERO']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_19')):#iDiscord
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD')):
							lList += ['PRISONER_DISCIPLE_DISCORD']
							if bFanatic:
								lList += ['PRISONER_PRIEST_DISCORD']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_20')):#iAnointed
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_ANOINTED')):
							lList += ['PRISONER_DISCIPLE_ANOINTED']
							if bPriest:
								lList += ['PRISONER_PRIEST_ANOINTED']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_21')):#iVeil
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')):
							lList += ['PRISONER_DISCIPLE_ASHEN']
							if bPriest:
								lList += ['PRISONER_PRIEST_ASHEN']
							if bFanatic:
								if not bSidar:
									lList += ['PRISONER_DISEASED_CORPSE_ASHEN']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_22')):#iLegion
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_EMBER_LEGION')):
							lList += ['PRISONER_DISCIPLE_EMBER_LEGION']
							if bPriest:
								lList += ['PRISONER_PRIEST_EMBER_LEGION']
							if bFanatic:
								lList += ['PRISONER_SALAMANDER']
					if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_23')):#Coven
						if CyGame().isReligionFounded(gc.getInfoTypeForString('RELIGION_COVEN')):
							lList += ['PRISONER_DISCIPLE_COVEN']
							if bPriest:
								lList += ['PRISONER_MOBIUS_WITCH']
							if bFanatic:
								lList += ['PRISONER_CHAINBREAKER']


		iCombat = pCaster.getUnitCombatType()
		if iCombat == gc.getInfoTypeForString('UNITCOMBAT_MELEE'):
			if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTED_BLADE')):
				lList += ['ENCHANTED_BLADE']
		elif iCombat == gc.getInfoTypeForString('UNITCOMBAT_ADEPT'):
			if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELLSTAFF')):
				lList += ['SPELLSTAFF']
		elif iCombat == gc.getInfoTypeForString('UNITCOMBAT_RECON'):
			if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE')):
				lList += ['POISONED_BLADE']
		elif iCombat == gc.getInfoTypeForString('UNITCOMBAT_ARCHER'):
			if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FLAMING_ARROWS')):
				lList += ['FLAMING_ARROWS']
		elif iCombat == gc.getInfoTypeForString('UNITCOMBAT_DISCIPLE'):
			if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHIELD_OF_FAITH')):
				lList += ['SHIELD_OF_FAITH']
		if gc.getUnitInfo(pCaster.getUnitType()).getWeaponTier() >= 1:
			if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MITHRIL_WEAPONS')):
				if gc.getUnitInfo(pCaster.getUnitType()).getWeaponTier() >= 3 and eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
					lList += ['MITHRIL_WEAPONS']
				if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')):
					if gc.getUnitInfo(pCaster.getUnitType()).getWeaponTier() >= 2 and eTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
						lList += ['IRON_WEAPONS']
					if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS')):
						lList += ['BRONZE_WEAPONS']
		sGoody = lList.pop(CyGame().getSorenRandNum(len(lList), "Pick Goody"))
		if sGoody == 'HIGH_GOLD':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_HIGH_GOLD'), pCaster)
			return 90
		elif sGoody == 'SUPPLIES':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_SUPPLIES'), pCaster)
			return 100
		elif sGoody == 'TREASURE':
			self.placeTreasure(iPlayer, gc.getInfoTypeForString('EQUIPMENT_TREASURE'))
			return 80
		elif sGoody == 'EXPERIENCE':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_EXPERIENCE'), pCaster)
			return 100
		elif sGoody == 'SPIRIT_GUIDE':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT_GUIDE'), True)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_SPIRIT_GUIDE",()),'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Promotions/SpiritGuide.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 80
		elif sGoody == 'ITEM_HEALING_SALVE':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_HEALING_SALVE'), pCaster)
			return 100
		elif sGoody == 'ITEM_POTION_OF_INVISIBILITY':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_POTION_OF_INVISIBILITY'), pCaster)
			return 100
		elif sGoody == 'ITEM_POTION_OF_RESTORATION':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_POTION_OF_RESTORATION'), pCaster)
			return 100
		elif sGoody == 'ENCHANTED_BLADE':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTED_BLADE'), True)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_ENCHANTED_BLADE",()),'',1,'Art/Interface/Buttons/Promotions/EnchantedBlade.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'SPELLSTAFF':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELLSTAFF'), True)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_SPELLSTAFF",()),'',1,'Art/Interface/Buttons/Promotions/Spellstaff.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'POISONED_BLADE':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE'), True)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_POISONED_BLADE",()),'',1,'Art/Interface/Buttons/Promotions/PoisonedBlade.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'FLAMING_ARROWS':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FLAMING_ARROWS'), True)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_FLAMING_ARROWS",()),'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Promotions/FlamingArrows.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_EMPYREAN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_EMPYREAN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_EMPYREAN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_EMPYREAN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_RADIANT_GUARD_EMPYREAN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_RADIANT_GUARD_EMPYREAN'), pCaster)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_SIRONA':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_SIRONA'), pCaster)
		elif sGoody == 'PRISONER_PRIEST_SIRONA':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_SIRONA'), pCaster)
			return 100
			
			
		elif sGoody == 'PRISONER_DISCIPLE_RINGGIVER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_RINGGIVER'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_RINGGIVER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_RINGGIVER'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_UNBLEMISHED':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_UNBLEMISHED'), pCaster)
			return 100
		elif sGoody == 'PRISONER_DRUID':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DRUID'), pCaster)
			return 100
		elif sGoody == 'PRISONER_HOSPITALLER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_HOSPITALLER'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_PLENTY':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_PLENTY'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_PLENTY':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_PLENTY'), pCaster)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_ORDER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_ORDER'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_ORDER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_ORDER'), pCaster)
			return 100
		elif sGoody == 'PRISONER_CRUSADER_ORDER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_CRUSADER_ORDER'), pCaster)
			return 100


		elif sGoody == 'PRISONER_LUONNOTAR':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_LUONNOTAR'), pCaster)
			return 120

		elif sGoody == 'PRISONER_APOSTATE':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_APOSTATE'), pCaster)
			return 120
		elif sGoody == 'PRISONER_WITCH_HUNTER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_WITCH_HUNTER'), pCaster)
			return 120

		elif sGoody == 'PRISONER_DISCIPLE_ARAWN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_ARAWN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_ARAWN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_ARAWN'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_LAERAN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_LAERAN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_LAERAN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_LAERAN'), pCaster)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_OVERLORDS':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_OVERLORDS'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_OVERLORDS':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_OVERLORDS'), pCaster)
			return 100
		elif sGoody == 'PRISONER_STYGIAN_GUARD_OVERLORDS':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_STYGIAN_GUARD_OVERLORDS'), pCaster)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_GREY':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_GREY'), pCaster)
			return 200
		elif sGoody == 'PRISONER_PRIEST_GREY':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_GREY'), pCaster)
			return 200

		elif sGoody == 'PRISONER_DISCIPLE_RUNES':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_RUNES'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_RUNES':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_RUNES'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PARAMANDER_RUNES':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PARAMANDER_RUNES'), pCaster)
			return 100



		elif sGoody == 'PRISONER_DISCIPLE_LEAVES':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_LEAVES'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_LEAVES':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_LEAVES'), pCaster)
			return 100
		elif sGoody == 'PRISONER_SATYR_LEAVES':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_SATYR_LEAVES'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_FOXMEN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_FOXMEN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_FOXMEN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_FOXMEN'), pCaster)
			return 100

		elif sGoody == 'PRISONER_PRIEST_DRAGON':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DRAGON_FANATIC'), pCaster)
			return 120

		elif sGoody == 'PRISONER_NIGHTWATCH_ESUS':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_NIGHTWATCH'), pCaster)
			return 200
		elif sGoody == 'PRISONER_PRIEST_ESUS':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_ESUS'), pCaster)
			return 200

		elif sGoody == 'PRISONER_DISCIPLE_HAND':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_HAND'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_HAND':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_OF_WINTER'), pCaster)
			return 100
		elif sGoody == 'PRISONER_HOLLOW_MAN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_HOLLOW_MAN'), pCaster)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_STEWARD':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_STEWARD'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_STEWARD':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_STEWARD'), pCaster)
			return 100
		elif sGoody == 'PRISONER_CONDOTTIERO':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_CONDOTTIERO'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_DISCORD':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_DISCORD'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_DISCORD':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_DISCORD'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_ANOINTED':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_ANOINTED'), pCaster)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_ASHEN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_ASHEN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_ASHEN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_ASHEN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_DISEASED_CORPSE_ASHEN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISEASED_CORPSE_ASHEN'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_EMBER_LEGION':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_EMBER_LEGION'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_EMBER_LEGION':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_EMBER_LEGION'), pCaster)
			return 100
		elif sGoody == 'PRISONER_SALAMANDER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_SALAMANDER'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_COVEN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_COVEN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_MOBIUS_WITCH':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_MOBIUS_WITCH'), pCaster)
			return 100
		elif sGoody == 'PRISONER_CHAINBREAKER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_CHAINBREAKER'), pCaster)
			return 100


		elif sGoody == 'SHIELD_OF_FAITH':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHIELD_OF_FAITH'), True)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_SHIELD_OF_FAITH",()),'',1,'Art/Interface/Buttons/Promotions/ShieldOfFaith.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'BRONZE_WEAPONS':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_BRONZE_WEAPONS",()),'',1,'Art/Interface/Buttons/Promotions/BronzeWeapons.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			if pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RUSTED')):
				pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RUSTED'), False)
			return 100
		elif sGoody == 'IRON_WEAPONS':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS'), True)
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), False)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_IRON_WEAPONS",()),'',1,'Art/Interface/Buttons/Promotions/IronWeapons.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			if pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RUSTED')):
				pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RUSTED'), False)
			return 100
		elif sGoody == 'MITHRIL_WEAPONS':
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MITHRIL_WEAPONS'), True)
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS'), False)
			pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), False)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_MITHRIL_WEAPONS",()),'',1,'Art/Interface/Buttons/Promotions/MithrilWeapons.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			if pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RUSTED')):
				pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RUSTED'), False)
			return 100
		return 100

	def exploreLairBigGood(self, pCaster):
		iPlayer = pCaster.getOwner()
		pPlot = pCaster.plot()
		pPlayer = gc.getPlayer(pCaster.getOwner())
		eTeam = gc.getTeam(pPlayer.getTeam())
		lList = ['TREASURE_VAULT', 'GOLDEN_AGE']


		if pCaster.area().getNumImprovements(gc.getInfoTypeForString('IMPROVEMENT_PORTAL')) < 2:
			lList += ['PORTAL']
		if pPlayer.canReceiveGoody(pPlot, gc.getInfoTypeForString('GOODY_GRAVE_TECH'), pCaster):
			lList += ['TECH']
		if not pPlot.isWater():
			lList += ['ITEM_DEASIL_CHARM','ITEM_JADE_TORC', 'ITEM_TIMOR_MASK', 'PRISONER_SHADE', 'PRISONER_ADVENTURER', 'PRISONER_ARTIST', 'PRISONER_GREAT_GENERAL', 'PRISONER_ENGINEER', 'PRISONER_MERCHANT', 'PRISONER_PROPHET', 'PRISONER_SCIENTIST']
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL')):
				if not (CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_UROR_BAND'), 0) or CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('UNITCLASS_OS_GABELLA'), 0)):
					lList += ['ITEM_UROR_BAND']
			if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_ROD_OF_WINDS'), 0):
				lList += ['ITEM_ROD_OF_WINDS']



			if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_KANNAS_WHIP'), 0):
				if self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_TAPESTRY_HOUSE')):
					lList += ['ITEM_KANNAS_WHIP']
			if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_SHIELD_OF_BALANCE'), 0):
				lList += ['ITEM_SHIELD_OF_BALANCE']
			if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_SEVEN_LEAGUE_BOOTS'), 0):
				lList += ['ITEM_SEVEN_LEAGUE_BOOTS']
			if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_SAWOL_CAVEA'), 0):
				lList += ['ITEM_SAWOL_CAVEA']
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_WAY_OF_THE_FORESTS')):
				if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_TANELYN'), 0):
					lList += ['ITEM_TANELYN']
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_DECEPTION')):
				if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_APHELION_AMULET'), 0):
					lList += ['ITEM_APHELION_AMULET']
				if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_UMBRA_CLOAK'), 0):
					lList += ['ITEM_UMBRA_CLOAK']
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_WAY_OF_THE_WISE')):
				if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_PELIANS_PALLIUM'), 0):
					lList += ['ITEM_PELIANS_PALLIUM']
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ALTERATION')):
				if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_MIRROR_OF_WISHES'), 0):
					lList += ['ITEM_MIRROR_OF_WISHES']
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_RELIGIOUS_LAW')):
				if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_METRONOME'), 0):
					lList += ['ITEM_METRONOME']
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_WRITING')) and eTeam.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):
				if not ( CyGame().isBuildingClassMaxedOut(gc.getInfoTypeForString('BUILDINGCLASS_CROWN_OF_AKHARIEN'), 0) or CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_CROWN_OF_AKHARIEN'), 0)):
					lList += ['ITEM_CROWN_OF_AKHARIEN']

			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_CODE_OF_LAWS')) or self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_TEMPLE_OF_ATONEMENT')):
				if not ( CyGame().isBuildingClassMaxedOut(gc.getInfoTypeForString('BUILDINGCLASS_HERON_THRONE'), 0) or CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_HERON_THRONE'), 0)):
					lList += ['ITEM_HERON_THRONE']


			if self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_WHISPERING_WOOD')) or self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL')):

				if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_STARLIGHT_AMULET'), 0):
					lList += ['ITEM_STARLIGHT_AMULET']
				if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_RESOUNDING_SHIELD'), 0):
					lList += ['ITEM_RESOUNDING_SHIELD']
				if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_MIST'), 0):
					lList += ['ITEM_MIST']

				lList += ['PRISONER_SHADE','ITEM_DEASIL_CHARM',]
				if not CyGame().isUnitEverActive(gc.getInfoTypeForString('UNIT_RATHUS')):
					if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_NETHER_BLADE'), 0):
						lList += ['ITEM_PROMOTION_NETHER_BLADE']

				if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_HEARTSTONE'), 0):
						lList += ['ITEM_PROMOTION_HEARTSTONE']

				if pCaster.getLevel() > 7:
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_FANATICISM')):
						if CyGame().getUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_GYRA')) == 0:
							lList += ['PRISONER_GYRA']

			if pPlot.getBonusType(-1) == -1:
				lList += ['BONUS_MANA']
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_MINING')):
					lList += ['BONUS_COPPER', 'BONUS_GEMS', 'BONUS_GOLD']
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_SMELTING')):
					lList += ['BONUS_IRON']
		iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
		iSidar = gc.getInfoTypeForString('CIVILIZATION_SIDAR')
		iCiv = pPlayer.getCivilizationType()
		bInfernal = iCiv == iInfernal
		bMercurians = iCiv == iMercurians
		bSidar = iCiv == iSidar

		bMystic = eTeam.isHasTech(gc.getInfoTypeForString('TECH_MYSTICISM'))
		bPriest = eTeam.isHasTech(gc.getInfoTypeForString('TECH_PRIESTHOOD'))
		bFanatic = eTeam.isHasTech(gc.getInfoTypeForString('TECH_FANATICISM'))

		if bMystic or bPriest or bFanatic:
			if not bInfernal:
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_0')):#iEmpyrean
					lList += ['PRISONER_DISCIPLE_EMPYREAN']
					if bPriest:
						lList += ['PRISONER_PRIEST_EMPYREAN_EMPYREAN']
					if bFanatic:
						lList += ['PRISONER_RADIANT_GUARD_EMPYREAN']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_1')):#iBrotherhood
					lList += ['PRISONER_DISCIPLE_SIRONA']
					if bPriest:
						lList += ['PRISONER_PRIEST_SIRONA']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_2')):#iRinggiver
					lList += ['PRISONER_DISCIPLE_RINGGIVER']
					if bPriest:
						lList += ['PRISONER_PRIEST_RINGGIVER']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_3')):#iUnblemished
					lList += ['PRISONER_DISCIPLE_UNBLEMISHED']
					if bPriest:
						lList += ['PRISONER_DRUID']
					if bFanatic:
						lList += ['PRISONER_HOSPITALLER']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_4')):#iPlenty
					lList += ['PRISONER_DISCIPLE_PLENTY']
					if bPriest:
						lList += ['PRISONER_PRIEST_PLENTY']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_5')):#iOrder
					lList += ['PRISONER_DISCIPLE_ORDER']
					if bPriest:
						lList += ['PRISONER_PRIEST_ORDER']
					if bFanatic:
						lList += ['PRISONER_CRUSADER_ORDER']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_6')):#iMatronae
					if bPriest:
						lList += ['PRISONER_APOSTATE']
					if bFanatic:
						lList += ['PRISONER_WITCH_HUNTER']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_7')):#iOne
					if pPlayer.getStateReligion() == -1:
						if bPriest:
							lList += ['PRISONER_LUONNOTAR']

			if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_8')):#iEternalCabal
				lList += ['PRISONER_DISCIPLE_ARAWN']
				if bPriest:
					lList += ['PRISONER_PRIEST_ARAWN']
			if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_9')):#iLaeran
				lList += ['PRISONER_DISCIPLE_LAERAN']
				if bPriest:
					lList += ['PRISONER_PRIEST_LAERAN']
			if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_10')):#iUndertow
				if not bMercurians:
					lList += ['PRISONER_DISCIPLE_OVERLORDS']
					if bPriest:
						lList += ['PRISONER_PRIEST_OVERLORDS']
					if bFanatic:
						lList += ['PRISONER_STYGIAN_GUARD_OVERLORDS']
			if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_11')):#iGrey
				lList += ['PRISONER_DISCIPLE_GREY']
				if bPriest:
					lList += ['PRISONER_PRIEST_GREY']
			if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_12')):#iRunes
				if not bInfernal:
					lList += ['PRISONER_DISCIPLE_RUNES']
					if bPriest:
						lList += ['PRISONER_PRIEST_RUNES']
				if bFanatic:
					lList += ['PRISONER_PARAMANDER_RUNES']
			if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_13')):#iLeaves
				lList += ['PRISONER_DISCIPLE_LEAVES']
				if bPriest:
					lList += ['PRISONER_PRIEST_LEAVES']
				if bFanatic:
					lList += ['PRISONER_SATYR_LEAVES']
			if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_14')):#iFoxmen
				lList += ['PRISONER_PRIEST_FOXMEN']
				if bPriest:
					lList += ['PRISONER_PRIEST_FOXMEN']
			if not bMercurians:
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_15')):#iDragonCult
					lList += ['PRISONER_PRIEST_DRAGON']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_16')):#iEsus
					if bPriest:
						lList += ['PRISONER_PRIEST_ESUS']
					if bFanatic:
						lList += ['PRISONER_NIGHTWATCH_ESUS']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_17')):#iHand
					lList += ['PRISONER_DISCIPLE_HAND']
					if bPriest:
						lList += ['PRISONER_PRIEST_HAND']
					if bFanatic:
						if not bSidar:
							lList += ['PRISONER_HOLLOW_MAN']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_18')):#iStewards
					lList += ['PRISONER_DISCIPLE_STEWARD']
					if bPriest:
						lList += ['PRISONER_PRIEST_STEWARD']
					if bFanatic:
						if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
							lList += ['PRISONER_CONDOTTIERO']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_19')):#iDiscord
					lList += ['PRISONER_DISCIPLE_DISCORD']
					if bFanatic:
						lList += ['PRISONER_PRIEST_DISCORD']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_20')):#iAnointed
					lList += ['PRISONER_DISCIPLE_ANOINTED']
					if bPriest:
						lList += ['PRISONER_PRIEST_ANOINTED']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_21')):#iVeil
					lList += ['PRISONER_DISCIPLE_ASHEN']
					if bPriest:
						lList += ['PRISONER_PRIEST_ASHEN']
					if bFanatic:
						if not bSidar:
							lList += ['PRISONER_DISEASED_CORPSE_ASHEN']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_22')):#iLegion
					lList += ['PRISONER_DISCIPLE_EMBER_LEGION']
					if bPriest:
						lList += ['PRISONER_PRIEST_EMBER_LEGION']
					if bFanatic:
						lList += ['PRISONER_SALAMANDER']
				if not gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_RELIGION_23')):#Coven
					lList += ['PRISONER_DISCIPLE_COVEN']
					if bPriest:
						lList += ['PRISONER_MOBIUS_WITCH']
					if bFanatic:
						lList += ['PRISONER_CHAINBREAKER']


		if pPlot.isWater():
			lList += ['PRISONER_SEA_SERPENT']
			if pPlot.getBonusType(-1) == -1:
				lList += ['BONUS_CLAM', 'BONUS_CRAB', 'BONUS_FISH']
			if self.isNearImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE')):
				if not (CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_SPEAR_OF_MAJOSI'), 0) or CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('UNITCLASS_TRENTON'), 0)):
					lList += ['ITEM_MAJOSI']


				if pCaster.getLevel() > 3:
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_FANATICISM')):
						if CyGame().getUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_CONDATIS')) == 0:
							lList += ['PRISONER_CONDATIS']
			if pPlot.getPlotCounter() > 50:
				if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('EQUIPMENTCLASS_BONE_CIRCLET'), 0):
					lList += ['ITEM_BONE_CIRCLET']


		if not self.grace():
			lList += ['PRISONER_ANGEL', 'PRISONER_MONK', 'PRISONER_ASSASSIN', 'PRISONER_CHAMPION', 'PRISONER_MAGE']

		sGoody = lList.pop(CyGame().getSorenRandNum(len(lList), "Pick Goody"))
		if sGoody == 'ITEM_MAJOSI':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_SPEAR_OF_MAJOSI'), pCaster)
			return 100
		elif sGoody == 'ITEM_KANNAS_WHIP':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_KANNAS_WHIP'), pCaster)
			return 100
		elif sGoody == 'ITEM_SHIELD_OF_BALANCE':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_SHIELD_OF_BALANCE'), pCaster)
			return 100
		elif sGoody == 'ITEM_SEVEN_LEAGUE_BOOTS':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_SEVEN_LEAGUE_BOOTS'), pCaster)
			return 100

		elif sGoody == 'ITEM_SAWOL_CAVEA':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_SAWOL_CAVEA'), pCaster)
			return 100




		elif sGoody == 'ITEM_BONE_CIRCLET':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_BONE_CIRCLET'), pCaster)
			return 100
		elif sGoody == 'ITEM_TANELYN':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_TANELYN'), pCaster)
			return 100
		elif sGoody == 'ITEM_APHELION_AMULET':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_APHELION_AMULET'), pCaster)
			return 100
		elif sGoody == 'ITEM_MIRROR_OF_WISHES':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_MIRROR_OF_WISHES'), pCaster)
			return 100
		elif sGoody == 'ITEM_UMBRA_CLOAK':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_UMBRA_CLOAK'), pCaster)
			return 100
		elif sGoody == 'ITEM_METRONOME':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_METRONOME'), pCaster)
			return 100
		elif sGoody == 'ITEM_MIST':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_MIST'), pCaster)
			return 100
		elif sGoody == 'ITEM_STARLIGHT_AMULET':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_STARLIGHT_AMULET'), pCaster)
			return 100
		elif sGoody == 'ITEM_RESOUNDING_SHIELD':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_RESOUNDING_SHIELD'), pCaster)
			return 100
		elif sGoody == 'ITEM_PELIANS_PALLIUM':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_PELIANS_PALLIUM'), pCaster)
			return 100
		elif sGoody == 'ITEM_CROWN_OF_AKHARIEN':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_CROWN_OF_AKHARIEN'), pCaster)
			return 100
		elif sGoody == 'ITEM_HERON_THRONE':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_HERON_THRONE'), pCaster)
			return 100
		elif sGoody == 'ITEM_UROR_BAND':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_UROR_BAND'), pCaster)
			return 100



		elif sGoody == 'TREASURE_VAULT':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_TREASURE_VAULT'), pCaster)
			return 100
		elif sGoody == 'BONUS_CLAM':
			pPlot.setBonusType(gc.getInfoTypeForString('BONUS_CLAM'))
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_CLAM",()),'',1,'Art/Interface/Buttons/WorldBuilder/Clam.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'BONUS_COPPER':
			pPlot.setBonusType(gc.getInfoTypeForString('BONUS_COPPER'))
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_COPPER",()),'',1,'Art/Interface/Buttons/WorldBuilder/Copper.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'BONUS_CRAB':
			pPlot.setBonusType(gc.getInfoTypeForString('BONUS_CRAB'))
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_CRAB",()),'',1,'Art/Interface/Buttons/WorldBuilder/Crab.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'BONUS_FISH':
			pPlot.setBonusType(gc.getInfoTypeForString('BONUS_FISH'))
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_FISH",()),'',1,'Art/Interface/Buttons/WorldBuilder/Fish.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'BONUS_GOLD':
			pPlot.setBonusType(gc.getInfoTypeForString('BONUS_GOLD'))
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_GOLD",()),'',1,'Art/Interface/Buttons/WorldBuilder/Gold.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'BONUS_GEMS':
			pPlot.setBonusType(gc.getInfoTypeForString('BONUS_GEMS'))
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_GEMS",()),'',1,'Art/Interface/Buttons/WorldBuilder/Gems.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'BONUS_IRON':
			pPlot.setBonusType(gc.getInfoTypeForString('BONUS_IRON'))
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_IRON",()),'',1,'Art/Interface/Buttons/WorldBuilder/Iron.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'BONUS_MANA':
			pPlot.setBonusType(gc.getInfoTypeForString('BONUS_MANA'))
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_MANA",()),'',1,'Art/Interface/Buttons/WorldBuilder/mana_button.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'GOLDEN_AGE':
			pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength())
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_GOLDEN_AGE",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			return 100
		elif sGoody == 'ITEM_JADE_TORC':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_JADE_TORC'), pCaster)
			return 100
		elif sGoody == 'ITEM_DEASIL_CHARM':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_DEASIL_CHARM'), pCaster)
			return 100
		elif sGoody == 'ITEM_ROD_OF_WINDS':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_ROD_OF_WINDS'), pCaster)
			return 100
		elif sGoody == 'ITEM_TIMOR_MASK':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_TIMOR_MASK'), pCaster)
			return 100
		elif sGoody == 'PRISONER_ADVENTURER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_ADVENTURER'), pCaster)
			return 100
		elif sGoody == 'PRISONER_SHADE':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_SHADE'), pCaster)
			return 100
		elif sGoody == 'PRISONER_ANGEL':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_ANGEL'), pCaster)
			return 100
		elif sGoody == 'PRISONER_ARTIST':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_ARTIST'), pCaster)
			return 100
		elif sGoody == 'PRISONER_ASSASSIN':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_ASSASSIN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_CHAMPION':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_CHAMPION'), pCaster)
			return 100
		elif sGoody == 'PRISONER_GREAT_GENERAL':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_GREAT_GENERAL'), pCaster)
			return 100
		elif sGoody == 'PRISONER_ENGINEER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_ENGINEER'), pCaster)
			return 100
		elif sGoody == 'PRISONER_MAGE':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_MAGE'), pCaster)
			return 100
		elif sGoody == 'PRISONER_MERCHANT':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_MERCHANT'), pCaster)
			return 100
		elif sGoody == 'PRISONER_MONK':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_MONK'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PROPHET':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PROPHET'), pCaster)
			return 100
		elif sGoody == 'PRISONER_SEA_SERPENT':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_SEA_SERPENT'), pCaster)
			return 100
		elif sGoody == 'PRISONER_SCIENTIST':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_SCIENTIST'), pCaster)
			return 100
		elif sGoody == 'TECH':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_GRAVE_TECH'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_EMPYREAN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_EMPYREAN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_EMPYREAN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_EMPYREAN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_RADIANT_GUARD_EMPYREAN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_RADIANT_GUARD_EMPYREAN'), pCaster)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_SIRONA':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_SIRONA'), pCaster)
		elif sGoody == 'PRISONER_PRIEST_SIRONA':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_SIRONA'), pCaster)
			return 100
			
			
		elif sGoody == 'PRISONER_DISCIPLE_RINGGIVER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_RINGGIVER'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_RINGGIVER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_RINGGIVER'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_UNBLEMISHED':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_UNBLEMISHED'), pCaster)
			return 100
		elif sGoody == 'PRISONER_DRUID':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DRUID'), pCaster)
			return 100
		elif sGoody == 'PRISONER_HOSPITALLER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_HOSPITALLER'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_PLENTY':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_PLENTY'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_PLENTY':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_PLENTY'), pCaster)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_ORDER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_ORDER'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_ORDER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_ORDER'), pCaster)
			return 100
		elif sGoody == 'PRISONER_CRUSADER_ORDER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_CRUSADER_ORDER'), pCaster)
			return 100


		elif sGoody == 'PRISONER_LUONNOTAR':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_LUONNOTAR'), pCaster)
			return 120

		elif sGoody == 'PRISONER_APOSTATE':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_APOSTATE'), pCaster)
			return 120
		elif sGoody == 'PRISONER_WITCH_HUNTER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_WITCH_HUNTER'), pCaster)
			return 120

		elif sGoody == 'PRISONER_DISCIPLE_ARAWN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_ARAWN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_ARAWN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_ARAWN'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_LAERAN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_LAERAN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_LAERAN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_LAERAN'), pCaster)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_OVERLORDS':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_OVERLORDS'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_OVERLORDS':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_OVERLORDS'), pCaster)
			return 100
		elif sGoody == 'PRISONER_STYGIAN_GUARD_OVERLORDS':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_STYGIAN_GUARD_OVERLORDS'), pCaster)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_GREY':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_GREY'), pCaster)
			return 200
		elif sGoody == 'PRISONER_PRIEST_GREY':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_GREY'), pCaster)
			return 200

		elif sGoody == 'PRISONER_DISCIPLE_RUNES':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_RUNES'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_RUNES':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_RUNES'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PARAMANDER_RUNES':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PARAMANDER_RUNES'), pCaster)
			return 100



		elif sGoody == 'PRISONER_DISCIPLE_LEAVES':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_LEAVES'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_LEAVES':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_LEAVES'), pCaster)
			return 100
		elif sGoody == 'PRISONER_SATYR_LEAVES':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_SATYR_LEAVES'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_FOXMEN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_FOXMEN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_FOXMEN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_FOXMEN'), pCaster)
			return 100

		elif sGoody == 'PRISONER_PRIEST_DRAGON':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DRAGON_FANATIC'), pCaster)
			return 120

		elif sGoody == 'PRISONER_NIGHTWATCH_ESUS':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_NIGHTWATCH'), pCaster)
			return 200
		elif sGoody == 'PRISONER_PRIEST_ESUS':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_ESUS'), pCaster)
			return 200

		elif sGoody == 'PRISONER_DISCIPLE_HAND':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_HAND'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_HAND':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_OF_WINTER'), pCaster)
			return 100
		elif sGoody == 'PRISONER_HOLLOW_MAN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_HOLLOW_MAN'), pCaster)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_STEWARD':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_STEWARD'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_STEWARD':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_STEWARD'), pCaster)
			return 100
		elif sGoody == 'PRISONER_CONDOTTIERO':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_CONDOTTIERO'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_DISCORD':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_DISCORD'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_DISCORD':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_DISCORD'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_ANOINTED':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_ANOINTED'), pCaster)
			return 100


		elif sGoody == 'PRISONER_DISCIPLE_ASHEN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_ASHEN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_ASHEN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_ASHEN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_DISEASED_CORPSE_ASHEN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISEASED_CORPSE_ASHEN'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_EMBER_LEGION':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_EMBER_LEGION'), pCaster)
			return 100
		elif sGoody == 'PRISONER_PRIEST_EMBER_LEGION':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_PRIEST_EMBER_LEGION'), pCaster)
			return 100
		elif sGoody == 'PRISONER_SALAMANDER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_SALAMANDER'), pCaster)
			return 100

		elif sGoody == 'PRISONER_DISCIPLE_COVEN':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_COVEN'), pCaster)
			return 100
		elif sGoody == 'PRISONER_MOBIUS_WITCH':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_MOBIUS_WITCH'), pCaster)
			return 100
		elif sGoody == 'PRISONER_CHAINBREAKER':
			pPlayer.receiveGoody(pPlot,gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_PRISONER_CHAINBREAKER'), pCaster)
			return 100



		elif sGoody == 'PRISONER_GYRA':
			pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GYRA'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_SOUTH)
			return 1200

		elif sGoody == 'PRISONER_CONDATIS':
			pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CONDATIS'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_SOUTH)
			return 1200

		elif sGoody == 'PORTAL':
			pPlotPortal = self.findClearPlotImprovement(pPlot)
			if pPlotPortal != -1:
				iBestValue = 0
				pBestPlot = -1
				for i in xrange (CyMap().numPlots()):
					iValue = 0
					pPlot2 = CyMap().plotByIndex(i)
##					if pPlot2.at(0, 0):continue#I do not want any portal on the plot reserved for Sluaghs
					if pPlot2.isPeak():continue
					if pPlot2.getBonusType(-1) != -1:continue#I'm tired of portals making resources, especially mana, inaccessible
					if pPlotPortal.isWater() == pPlot2.isWater():
						if pPlot2.getNumUnits() == 0:
							iValue = CyGame().getSorenRandNum(1000, "Portal")
							if not pPlot2.isOwned():
								iValue += 100
							iDistance = CyMap().calculatePathDistance(pPlotPortal,pPlot2)
							if iDistance == -1:
								iValue += 500
							else:
								iValue += 10 * iDistance
							if iValue > iBestValue:
								iBestValue = iValue
								pBestPlot = pPlot2
				if pBestPlot != -1:
					pCaster.setXY(pPlotPortal.getX(), pPlotPortal.getY(), False, True, True)
					CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_PORTAL",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlotPortal.getX(),pPlotPortal.getY(),True,True)
					pPlotPortal.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_PORTAL'))
					pPlotPortal.setPortalExitX(pBestPlot.getX())
					pPlotPortal.setPortalExitY(pBestPlot.getY())
					pBestPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_PORTAL'))
					pBestPlot.setPortalExitX(pPlotPortal.getX())
					pBestPlot.setPortalExitY(pPlotPortal.getY())
				return 100
		return 0

	def formEmpire(self, iCiv, iLeader, iTeam, pCity, iAlignment, pFromPlayer):
		iPlayer = pFromPlayer.initNewEmpire(iLeader, iCiv)
		if iPlayer != PlayerTypes.NO_PLAYER:
			pPlot = pCity.plot()
			for i in xrange(pPlot.getNumUnits(), -1, -1):
				pUnit = pPlot.getUnit(i)
				pUnit.jumpToNearestValidPlot()
			pPlayer = gc.getPlayer(iPlayer)
			if iTeam != TeamTypes.NO_TEAM:
				if iTeam < pPlayer.getTeam():
					gc.getTeam(iTeam).addTeam(pPlayer.getTeam())
				else:
					gc.getTeam(pPlayer.getTeam()).addTeam(iTeam)
			pPlayer.acquireCity(pCity, False, True)
			pCity = pPlot.getPlotCity()
			pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
			pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
			pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
			pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
			pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WORKER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if iAlignment != -1:
				pPlayer.setAlignment(iAlignment)
		return pPlayer

	def grace(self):
		iGrace = 20 * (int(CyGame().getGameSpeedType()) + 1)
		iDiff = gc.getNumHandicapInfos() + 1 - int(gc.getGame().getHandicapType())
		iGrace *= iDiff
		iGrace += CyGame().getSorenRandNum(iGrace, "grace")
		if iGrace > CyGame().getGameTurn():
			return True
		return False

	def doCityFire(self, pCity):
		iCount = 0

		for iBuilding in range(gc.getNumBuildingInfos()):
			kBuilding = gc.getBuildingInfo(iBuilding)
			# Evaluate getNumRealBuilding first, no need to check conditions for buildings that are not present.
			if pCity.getNumRealBuilding(iBuilding) > 0 and iBuilding not in self.siIgnoreFire and \
					not kBuilding.isRequiresCaster() and \
					kBuilding.getBuildingClassType() != gc.getInfoTypeForString('BUILDINGCLASS_PALACE') and \
					kBuilding.getConquestProbability() != 100:
##--------		Unofficial Bug Fix: Modified by Denev	--------##
#				if CyGame().getSorenRandNum(100, "City Fire") <= 10:
				if CyGame().getSorenRandNum(100, "City Fire") < 10:
##--------		Unofficial Bug Fix: End Modify			--------##
					pCity.setNumRealBuilding(iBuilding, 0)
					CyInterface().addMessage(pCity.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_CITY_FIRE",(kBuilding.getDescription(), )),'',1,kBuilding.getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
					iCount += 1

		if iCount == 0:
			CyInterface().addMessage(pCity.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_CITY_FIRE_NO_DAMAGE",()),'AS2D_SPELL_FIRE_ELEMENTAL',1,'Art/Interface/Buttons/Fire.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

#Magister
	def isNearImprovement(self, pPlot, iImprovement):
		if pPlot.getImprovementType() == iImprovement:
			return True
		iX = pPlot.getX()
		iY = pPlot.getY()
		for iDirection in xrange(DirectionTypes.NUM_DIRECTION_TYPES):
			pAdjacentPlot = plotDirection(iX, iY, DirectionTypes(iDirection))
			if not pAdjacentPlot.isNone():
				if pPlot.getImprovementType() == iImprovement:
					return True
		return False


	def doHellTerrain(self):
		iEvil = gc.getInfoTypeForString('ALIGNMENT_EVIL')
		iNeutral = gc.getInfoTypeForString('ALIGNMENT_NEUTRAL')
		iBarb = gc.getBARBARIAN_PLAYER()
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
		iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
		iBarb = gc.getInfoTypeForString('CIVILIZATION_BARBARIAN')
		iAshenVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
		iBurningSands = gc.getInfoTypeForString('TERRAIN_BURNING_SANDS')
		iGlac = gc.getInfoTypeForString('TERRAIN_GLACIER')
		iBliz = gc.getInfoTypeForString('FEATURE_BLIZZARD')
		iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')

		iBForest = gc.getInfoTypeForString('FEATURE_FOREST_BURNT')
		iObsidian = gc.getInfoTypeForString('FEATURE_OBSIDIAN_PLAINS')
		iFlood = gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')
		iScrub = gc.getInfoTypeForString('FEATURE_SCRUB')
		iTormentedSouls = gc.getInfoTypeForString('FEATURE_TORMENTED_SOULS')

		iHallowed=gc.getInfoTypeForString('FEATURE_HALLOWED_GROUND')
		iFarm = gc.getInfoTypeForString('IMPROVEMENT_FARM')
		iSnakePillar = gc.getInfoTypeForString('IMPROVEMENT_SNAKE_PILLAR')
		iHellfire = gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE')
		iNecrototem = gc.getInfoTypeForString('IMPROVEMENT_NECROTOTEM')
		iPortal = gc.getInfoTypeForString('IMPROVEMENT_PORTAL')


		iGulagarm = gc.getInfoTypeForString('BONUS_GULAGARM')
		iToad = gc.getInfoTypeForString('BONUS_TOAD')
		iGrapes= gc.getInfoTypeForString('BONUS_GRAPES_OF_WRATH')
		iSheutStone = gc.getInfoTypeForString('BONUS_SHEUT_STONE')
		iRazorweed = gc.getInfoTypeForString('BONUS_RAZORWEED')
		iWine= gc.getInfoTypeForString('BONUS_WINE')
		iMarble = gc.getInfoTypeForString('BONUS_MARBLE')
		iNightmare = gc.getInfoTypeForString('BONUS_NIGHTMARE')


		lMeats = [gc.getInfoTypeForString('BONUS_SHEEP'), gc.getInfoTypeForString('BONUS_PIG')]
		lMounts = [gc.getInfoTypeForString('BONUS_HORSE'), gc.getInfoTypeForString('BONUS_COW'), gc.getInfoTypeForString('BONUS_DEER')]
		lFibers = [gc.getInfoTypeForString('BONUS_COTTON'), gc.getInfoTypeForString('BONUS_SILK')]
		lTropicals = [gc.getInfoTypeForString('BONUS_BANANA'), gc.getInfoTypeForString('BONUS_SUGAR')]
		lCereals = [gc.getInfoTypeForString('BONUS_CORN'), gc.getInfoTypeForString('BONUS_RICE'), gc.getInfoTypeForString('BONUS_WHEAT')]
		lForests = [gc.getInfoTypeForString('FEATURE_FOREST'), gc.getInfoTypeForString('FEATURE_JUNGLE'), gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT'), gc.getInfoTypeForString('FEATURE_FOREST_NEW')]
		lDesertFeatures = [iScrub, iFlood]

		iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
		iFlamesSpreadChance = gc.getDefineINT('FLAMES_SPREAD_CHANCE')
		iPlotCounterUp = 50
		iCount = CyGame().getGlobalCounter()
		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iFeature = pPlot.getFeatureType()
			if iFeature == iHallowed:
				pPlot.changePlotCounter(-100)
				continue
			elif iFeature == iTormentedSouls:
				pPlot.changePlotCounter(100)
				continue
			iImprovement = pPlot.getImprovementType()
			iPlotCount = pPlot.getPlotCounter()
			bSpread = False
			bUntouched = True
			iRecover = 0
			if iImprovement in [iHellfire, iNecrototem]:
				pPlot.changePlotCounter(100)
				bUntouched = False
			elif pPlot.isOwned():
				pPlayer = gc.getPlayer(pPlot.getOwner())
				iAlignment = pPlayer.getAlignment()
				if pPlayer.getCivilizationType() == iMercurians:
					iRecover = -4
					bUntouched = True
					bSpread = False
				elif pPlayer.getCivilizationType() == iInfernal:
					pPlot.changePlotCounter(13)
					bUntouched = False
					bSpread = True
				elif pPlayer.getStateReligion() == iAshenVeil:
					if iCount > 10:
						bSpread = True
				elif iAlignment == iEvil:
					if iCount > 25:
						bSpread = True
						iRecover = -1
				elif iAlignment == iNeutral:
					if iCount > 50:
						bSpread = True
						iRecover = -2
				else:
					if iCount > 90:
						bSpread = True
						iRecover = -3
			else:
				if pPlot.isPeak() and iCount > 75:
					bSpread = True
					iRecover = -1
				elif pPlot.isWater() and iCount > 50:
					bSpread = True
					iRecover = -1
				elif iCount > 30:
					bSpread = True
					iRecover = -1
			if bSpread:
				if iImprovement == iPortal:
					pAdjacentPlot = CyMap().plot(pPlot.getPortalExitX(),pPlot.getPortalExitY())
					if not pAdjacentPlot.isNone():
						if not pAdjacentPlot.getFeatureType() == iHallowed:
							if pAdjacentPlot.getPlotCounter() > 100-iCount:
								change = 8*pAdjacentPlot.getPlotCounter()//(120-iCount)
								if pPlot.isPeak() or pPlot.isWater():
									change //= 2
								pPlot.changePlotCounter(change)
								bUntouched = False
				iX = pPlot.getX()
				iY = pPlot.getY()

				for iDirection in xrange(DirectionTypes.NUM_DIRECTION_TYPES):
					pAdjacentPlot = plotDirection(iX, iY, DirectionTypes(iDirection))
					if not pAdjacentPlot.isNone():
						if not pAdjacentPlot.getFeatureType() == iHallowed:
							if pAdjacentPlot.getPlotCounter() > 100-iCount:
								change = 1 + pAdjacentPlot.getPlotCounter()//(120-iCount)
								if pPlot.isPeak() or pPlot.isWater():
									change //= 2
								pPlot.changePlotCounter(change)
								bUntouched = False
			if bUntouched and iPlotCount:
				pPlot.changePlotCounter(iRecover)
			iPlotCount = pPlot.getPlotCounter()
			if iPlotCount > iPlotCounterUp:
				if iFeature in lForests:
					iRandom = CyGame().getSorenRandNum(15, "Hell Terrain Burnt Forest")
					if iRandom < 10:
						pPlot.setFeatureType(iBForest, 0)

				elif iFeature in lDesertFeatures:
					pPlot.setFeatureType(iObsidian, 0)
				iBonus = pPlot.getBonusType(-1)
				if iBonus != -1:
					if iBonus == iWine:
						pPlot.setBonusType(iGrapes)
					elif iBonus == iMarble:
						pPlot.setBonusType(iSheutStone)
					elif iBonus in lMeats:
						pPlot.setBonusType(iToad)
					elif iBonus in lMounts:
						pPlot.setBonusType(iNightmare)
					elif iBonus in lFibers:
						pPlot.setBonusType(iRazorweed)
					elif iBonus in lTropicals:
						pPlot.setBonusType(iGulagarm)
					elif iBonus in lCereals:
						pPlot.setBonusType(-1)
						pPlot.setImprovementType(iSnakePillar)
			if iPlotCount < iPlotCounterUp:
				if iFeature == iObsidian:
					if pPlot.isFreshWater():
						pPlot.setFeatureType(iFlood, 0)
					else:
						pPlot.setFeatureType(iScrub, 0)
				if iImprovement == iSnakePillar:
					pPlot.setImprovementType(iFarm)
					pPlot.setBonusType(lCereals[CyGame().getSorenRandNum(len(lCereals), "Hell Convert Bonus")])
				iBonus = pPlot.getBonusType(-1)
				if iBonus != -1:
					if iBonus == iGrapes:
						pPlot.setBonusType(iWine)
					elif iBonus == iSheutStone:
						pPlot.setBonusType(iMarble)
					elif iBonus == iToad:
						pPlot.setBonusType(lMeats[CyGame().getSorenRandNum(len(lMeats), "Hell Convert Bonus")])
					elif iBonus == iNightmare:
						pPlot.setBonusType(lMounts[CyGame().getSorenRandNum(len(lMounts), "Hell Convert Bonus")])
					elif iBonus == iRazorweed:
						pPlot.setBonusType(lFibers[CyGame().getSorenRandNum(len(lFibers), "Hell Convert Bonus")])
					elif iBonus == iGulagarm:
						pPlot.setBonusType(lTropicals[CyGame().getSorenRandNum(len(lTropicals), "Hell Convert Bonus")])
			if pPlot.isCity():
				if iFeature == iFlames:
					pPlot.setFeatureType(-1,-1)
				if iImprovement == iSmoke:
					pPlot.setImprovementType(-1)
			elif iFeature == -1:
				if not pPlot.isPeak():
					iTerrain = pPlot.getTerrainType()
					if iTerrain == iBurningSands:
						if CyGame().getSorenRandNum(10, "Flames") < iFlamesSpreadChance/10:
							pPlot.setFeatureType(iFlames, 0)
					elif iTerrain == iGlac:
						if CyGame().getSorenRandNum(10, "Blizzard") < iFlamesSpreadChance/100:
							pPlot.setFeatureType(iBliz, 0)
				if iImprovement == iSmoke:
					pPlot.setImprovementType(-1)
			elif iFeature == iFlood:
				if iImprovement == iSmoke:
					pPlot.setImprovementType(-1)


	def doCitiesTurn(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()
		eTeam = gc.getTeam(iTeam)
		iCiv = pPlayer.getCivilizationType()
		iStateReligion = pPlayer.getStateReligion()




		iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
		iCalabim = gc.getInfoTypeForString('CIVILIZATION_CALABIM')
		iIllians = gc.getInfoTypeForString('CIVILIZATION_ILLIANS')

		iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
		iEmpyrean = gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')
		iOverlords = gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS')
		iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
		iDragonCult = gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON')
		iHand = gc.getInfoTypeForString('RELIGION_WHITE_HAND')
		iOne = gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE')

		iHouseRel = gc.getInfoTypeForString('RELIGION_HOUSE_OF_PLENTY')

		iAbundance = gc.getInfoTypeForString('BUILDING_ABUNDANCE')
		iFertility = gc.getInfoTypeForString('BUILDING_FERTILITY')
		iHospitality = gc.getInfoTypeForString('BUILDING_HOSPITALITY')


		iCrucible = gc.getInfoTypeForString('BUILDING_CRUCIBLE')
		iComplacency = gc.getInfoTypeForString('BUILDING_TOWER_OF_COMPLACENCY')
		iUnyielding = gc.getInfoTypeForString('BUILDING_UNYIELDING_ORDER')
		iUnyieldingG = gc.getInfoTypeForString('BUILDING_UNYIELDING_ORDER_GREATER')


		iChains = gc.getInfoTypeForString('BUILDING_PILLAR_OF_CHAINS')
		iTowerElements = gc.getInfoTypeForString('BUILDING_TOWER_OF_THE_ELEMENTS')
		iMartyrs = gc.getInfoTypeForString('BUILDING_UNHARMED_MARTYRS')

		iSmugglersPort = gc.getInfoTypeForString('BUILDING_SMUGGLERS_PORT')
		iHallMirrors = gc.getInfoTypeForString('BUILDING_HALL_OF_MIRRORS')
		iPaganTemple = gc.getInfoTypeForString('BUILDING_PAGAN_TEMPLE')
		iAqueduct = gc.getInfoTypeForString('BUILDING_AQUEDUCT')

		iFreshWater = gc.getInfoTypeForString('FEATURE_FRESH_WATER')

		iTolerant = gc.getInfoTypeForString('TRAIT_TOLERANT')
		iSummoner = gc.getInfoTypeForString('TRAIT_SUMMONER')
		iFallow = gc.getInfoTypeForString('TRAIT_FALLOW')

		bAuricAlive = False
		bAuricRevolt = False
		iAuricLeader = gc.getInfoTypeForString('LEADER_AURIC')
		iAuricPlayer = self.getLeader(iAuricLeader)
		if iAuricPlayer != -1:
			pAuricPlayer = gc.getPlayer(iAuricPlayer)
			if pAuricPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AURIC')) > 0:
				bAuricAlive = True
				if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_DRAW')) > 0:
					if not pPlayer.getLeaderType() == iAuricLeader:
						if eTeam.isAtWar(pAuricPlayer.getTeam()):
							bAuricRevolt = True

		iTempleHand = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_HAND')
		iNewMulyr = gc.getInfoTypeForString('BUILDING_NEW_MULYR')
		iSnowRange = 0
		if bAuricAlive:
			if pPlayer.countNumBuildings(iTempleHand) > 0:
				if iStateReligion == iHand:
					iSnowRange += 1
				for sRitual in [	'PROJECT_SAMHAIN',
									'PROJECT_THE_WHITE_HAND',
									'PROJECT_THE_DEEPENING',
									'PROJECT_THE_DRAW',
									'PROJECT_ASCENSION'
									]:
					if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString(sRitual)) > 0:
						iSnowRange += 1
				iManaIce = gc.getInfoTypeForString('BONUS_MANA_ICE')
				iManaFire = gc.getInfoTypeForString('BONUS_MANA_FIRE')
				iManaNature = gc.getInfoTypeForString('BONUS_MANA_NATURE')

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

		iChancel = gc.getInfoTypeForString('BUILDING_CHANCEL_OF_GUARDIANS')
		if pPlayer.countNumBuildings(iChancel) > 0:
			bNoPlotCounter = gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_PLOT_COUNTER)

			iWarden = gc.getInfoTypeForString('UNIT_TOMB_WARDEN')

			iObsidian = gc.getInfoTypeForString('FEATURE_OBSIDIAN_PLAINS')
			iFlood = gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')
			iScrub = gc.getInfoTypeForString('FEATURE_SCRUB')

			iTormentedSouls = gc.getInfoTypeForString('FEATURE_TORMENTED_SOULS')
			iHallowedGround = gc.getInfoTypeForString('FEATURE_HALLOWED_GROUND')


			iHellfire = gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE')
			iNecrototem = gc.getInfoTypeForString('IMPROVEMENT_NECROTOTEM')
			iPortal = gc.getInfoTypeForString('IMPROVEMENT_PORTAL')
			iPit = gc.getInfoTypeForString('IMPROVEMENT_PIT')
			iRuin = gc.getInfoTypeForString('IMPROVEMENT_CITY_RUINS')
			iGrave = gc.getInfoTypeForString('IMPROVEMENT_GRAVEYARD')
			iSnakePillar = gc.getInfoTypeForString('IMPROVEMENT_SNAKE_PILLAR')
			iFarm = gc.getInfoTypeForString('IMPROVEMENT_FARM')

			iManaSpirit = gc.getInfoTypeForString('BONUS_MANA_SPIRIT')
			iGrapes= gc.getInfoTypeForString('BONUS_GRAPES_OF_WRATH')
			iWine= gc.getInfoTypeForString('BONUS_WINE')
			iSheutStone = gc.getInfoTypeForString('BONUS_SHEUT_STONE')
			iMarble = gc.getInfoTypeForString('BONUS_MARBLE')
			iToad = gc.getInfoTypeForString('BONUS_TOAD')
			iNightmare = gc.getInfoTypeForString('BONUS_NIGHTMARE')
			iRazorweed = gc.getInfoTypeForString('BONUS_RAZORWEED')
			iGulagarm = gc.getInfoTypeForString('BONUS_GULAGARM')
			lCereals = [	gc.getInfoTypeForString('BONUS_CORN'),
					gc.getInfoTypeForString('BONUS_RICE'),
					gc.getInfoTypeForString('BONUS_WHEAT')
					]
			lMeats = [	gc.getInfoTypeForString('BONUS_SHEEP'),
					gc.getInfoTypeForString('BONUS_PIG')
					]
			lMounts = [	gc.getInfoTypeForString('BONUS_HORSE'),
					gc.getInfoTypeForString('BONUS_COW'),
					gc.getInfoTypeForString('BONUS_DEER')
					]
			lFibers = [	gc.getInfoTypeForString('BONUS_COTTON'),
					gc.getInfoTypeForString('BONUS_SILK')
					]
			lTropicals = [	gc.getInfoTypeForString('BONUS_BANANA'),
					gc.getInfoTypeForString('BONUS_SUGAR')
					]

		iPlanarGate = gc.getInfoTypeForString('BUILDING_PLANAR_GATE')
		iNumPlanerGate = pPlayer.countNumBuildings(iPlanarGate)
		if iNumPlanerGate > 0:
			iManaDimensional = gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')
			iAC = CyGame().getGlobalCounter()

			iPlanarGateClosed = gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED')
			iNumPlanerGateClosed = pPlayer.countNumBuildings(iPlanarGateClosed)

			iMaxNumCreature = (iNumPlanerGate+iNumPlanerGateClosed)*max(1, iAC/25)
			iGateChance = gc.getDefineINT('PLANAR_GATE_CHANCE')*max(1, iAC/5)

			lRemoveChaos = [	gc.getInfoTypeForString('PROMOTION_REBEL'),
								gc.getInfoTypeForString('PROMOTION_ENRAGED'),
								gc.getInfoTypeForString('PROMOTION_CRAZED')
								]

			listStringCreatures =	[
										'UNIT_CHAOS_MARAUDER',
										'UNIT_COLUBRA',
										'UNIT_MINOTAUR',
										'UNIT_MANTICORE',
										'UNIT_MOBIUS_WITCH',
										'UNIT_REVELERS',
										'UNIT_SUCCUBUS',
										'UNIT_TAR_DEMON',
										'UNIT_IMP',
										'UNIT_SALAMANDER',
										'UNIT_STYGIAN_GUARD',
										'UNIT_BALOR',
										'UNIT_SPECTRE',
										'UNIT_MISTFORM',
										'UNIT_DYBBUK'
									]
			listGateCreatures = []
			for sUnit in listStringCreatures:
				iUnit = gc.getInfoTypeForString(sUnit)
				infoUnit = gc.getUnitInfo(iUnit)
				iTech = infoUnit.getPrereqAndTech()
				if iTech != -1:
					if not eTeam.isHasTech(iTech):
						continue
				iBuilding = infoUnit.getPrereqBuilding()
				if iBuilding != -1:
					if pPlayer.countNumBuildings(iBuilding) == 0:
						continue
				if pPlayer.getUnitClassCount(infoUnit.getUnitClassType()) < iMaxNumCreature:
					if not pPlayer.isUnitClassMaxedOut(infoUnit.getUnitClassType(), 0):
						listGateCreatures.append(iUnit)

		if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_SHRINE_OF_SIRONA')) > 0:
			for pTeammate in self.getTeammates(pPlayer):
				pTeammate.setFeatAccomplished(FeatTypes.FEAT_HEAL_UNIT_PER_TURN, True)
##
##		if pPlayer.isFullMember(gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')):
##			bNetwork = False
##			if CyGame().getBuildingClassCreatedCount(gc.getInfoTypeForString('BUILDINGCLASS_EYES_AND_EARS_NETWORK')) > 0:
##				iNetwork = gc.getInfoTypeForString('BUILDING_EYES_AND_EARS_NETWORK')
##				for pTeammate in self.getTeammates(pPlayer):
##
##					if pTeammate.countNumBuildings(iNetwork) > 0:#This is more efficient than checking what city has the wonder
##						bNetwork = True
##						break
##			if bNetwork:
##
##				listTeams = []
##				iNumLivingTeams = 0
##				for iTeam2 in xrange(gc.getMAX_TEAMS()):
##					if iTeam != iTeam2:
##						eTeam2 = gc.getTeam(iTeam2)
##						if eTeam2.isAlive():
##							if eTeam.isHasMet(iTeam2):
##								iNumLivingTeams += 1
##								if not eTeam.isAtWar(iTeam2):
##									listTeams.append(gc.getTeam(iTeam2))
##				if len(listTeams) > iNumLivingTeams//4:
##					for iTech in xrange(gc.getNumTechInfos()):
##						if pPlayer.canResearch(iTech, False):
##							iCount = 0
##							for i in xrange(len(listTeams)):
##								if listTeams[i].isHasTech(iTech):
##									iCount += 1
##							if iCount > iNumLivingTeams//4:
##								eTeam.setHasTech(iTech, True, iPlayer, False, True)
##								pCity = pPlayer.getCapitalCity()#This is more efficient than checking what city has the wonder
##								szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_EYES_AND_EARS_NETWORK_FREE_TECH",(PyInfo.TechnologyInfo(iTech).getDescription(),))
##								CyInterface().addMessage(iPlayer,True,25,szBuffer,'AS2D_TECH_DING',1,'Art/Interface/Buttons/Buildings/Eyesandearsnetwork.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

		
		for pyCity in PyPlayer(iPlayer).getCityList():
			pCity = pyCity.GetCy()
			pPlot = pCity.plot()
			iX = pCity.getX()
			iY = pCity.getY()

			if pPlayer.hasTrait(iFallow):
				pCity.setNumRealBuilding(iFertility, 0)
				pCity.setNumRealBuilding(iAbundance, 0)
				pCity.setNumRealBuilding(iHospitality, 0)
				
			if pPlayer.isCivic(gc.getInfoTypeForString('CIVIC_SACRIFICE_THE_WEAK')):
				pCity.setNumRealBuilding(iHospitality, 0)

			if pPlayer.hasTrait(iTolerant):
				if not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
					iDominantCiv = iCiv
					iMostCivCulture = 0
					for iCiv2 in xrange(gc.getNumCivilizationInfos()):
						if (iCiv2 == iInfernal and iCiv == iMercurians) or (iCiv2 == iMercurians and iCiv == iInfernal):
							continue
						iCivCult = 0
						for jPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
							if gc.getPlayer(jPlayer).getCivilizationType() == iCiv2:
								iCivCult += pCity.getCulture(jPlayer)
						if iCiv == iCiv2:
							iCivCult /= 4
						if iCivCult > iMostCivCulture:
							iMostCivCulture = iCivCult
							iDominantCiv = iCiv2
					if iDominantCiv != pCity.getCivilizationType():
						pCity.setCivilizationType(iDominantCiv)
						CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)


			if pCity.getNumBuilding(iCrucible) > 0:
				self.doEffectCrucible(pCity)


			if pCity.getNumBuilding(iComplacency) > 0 or pCity.getNumBuilding(iUnyielding) > 0 or pCity.getNumBuilding(iUnyieldingG) > 0:
				iChange = -9
				pTimer = pCity.getHurryAngerTimer()
				if pTimer < 9:
					iChange = 0 - pTimer
				pCity.changeHurryAngerTimer(iChange)
				pCity.setOccupationTimer(0)
				CyGame().changeCrime(-5)
				if pCity.getRevolutionIndex() > 0:
					pCity.setRevolutionIndex(0)

			elif pCity.getNumBuilding(iChains):
				pCity.setOccupationTimer(0)
				CyGame().changeCrime(-5)
				if pCity.getRevolutionIndex() > 0:
					pCity.setRevolutionIndex(0)
			else:
				if pCity.isHasReligion(iDragonCult):
					iRnd = CyGame().getSorenRandNum(100, "Dragon Cult Revolt")
					if 1 < iRnd < 3:
						if self.isHasDragon(pPlayer):
							iRnd *= -1
						else:
							CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DRAGON_CULT_REVOLT", ()),'',1,'Art/Interface/Buttons/Units/Acheron.dds',ColorTypes(7),iX,iY,True,True)
						pCity.changeOccupationTimer(iRnd)
						pCity.changeHurryAngerTimer(iRnd)
				if pCity.isHasReligion(iEmpyrean):
					if iCiv == iCalabim:
						iRnd = CyGame().getSorenRandNum(100, "Empyrean vs Vampire revolt")
						if 1 < iRnd < 4:
							pCity.changeOccupationTimer(iRnd)
							pCity.changeHurryAngerTimer(iRnd)
							pCity.setRevolutionIndex(pCity.getRevolutionIndex() + iRnd)
							CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EMPYREAN_REVOLT", (pCity.getName(),)),'',1,'Art/Interface/Buttons/Units/Priest Empyrean.dds',ColorTypes(7),iX,iY,True,True)
				if pCity.isHasReligion(iOne):
					iRnd = CyGame().getSorenRandNum(75, "Monotheist  Revolt")
					if pCity.getNumRealBuilding(iMartyrs) > 0:
						iRnd *= 2
					if 1 < iRnd < 5:
						for iTarget in xrange(gc.getNumReligionInfos()):
							if iTarget != iOne and pCity.isHasReligion(iTarget):
								if self.removeReligion(iTarget, pCity):
									CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_Monotheist _REVOLT", ()),'',1,'Art/Interface/Buttons/Units/Inquisitor Grigori.dds',ColorTypes(7),iX,iY,True,True)
									iRnd += 1
									if iStateReligion == iTarget:
										pCity.changeOccupationTimer(iRnd)
										pCity.changeHurryAngerTimer(iRnd)
						if pCity.getNumBuilding(iPaganTemple):
							pCity.setNumRealBuilding(iPaganTemple, 0)
							iRnd += 1
						if iRnd >= 1:
							pCity.changeHurryAngerTimer(iRnd)

				if pCity.isHasReligion(iHand):
					if bAuricRevolt:
						if CyGame().getSorenRandNum(100, "Auric Revolt") < 15:
							pCity.changeOccupationTimer(3)
							pCity.changeHurryAngerTimer(1)
							CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_AURIC_REVOLT", ()),'',1,'Art/Interface/Buttons/Units/Auric Ascended.dds',ColorTypes(7),iX,iY,True,True)

			if pCity.getNumRealBuilding(iHallMirrors) > 0:
				lUnit = []
				for iDirection in xrange(DirectionTypes.NUM_DIRECTION_TYPES):
					pLoopPlot = plotDirection(iX, iY, DirectionTypes(iDirection))
					if not pLoopPlot.isNone():
						if pLoopPlot.isVisibleOtherUnit(iPlayer):
							for i in xrange(pLoopPlot.getNumUnits()):
								pUnit = pLoopPlot.getUnit(i)
								if pUnit.baseCombatStrDefense() > 0:
									if not pUnit.isImmortal():
										if iTeam != pUnit.getTeam():
											if eTeam.isAtWar(pUnit.getTeam()) or pUnit.isHiddenNationality():
												lUnit.append(pUnit)

				if len(lUnit) > 0:
					pUnit = lUnit.pop(CyGame().getSorenRandNum(len(lUnit), "Create Illusion - Hall of Mirrors"))
					newUnit = pPlayer.initUnit(pUnit.getUnitType(), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION'), True)
					newUnit.setMadeAttack(True)
					newUnit.setHasCasted(True)
					newUnit.setScenarioCounter(-1)
					for iProm in xrange(gc.getNumPromotionInfos()):
						if gc.getPromotionInfo(iProm).isEquipment():
							newUnit.setHasPromotion(iProm, False)

	##--------		Unofficial Bug Fix: Modified by Denev	--------##
	# Copy not only unit type, but also unit artstyle.
					newUnit.setUnitArtStyleType(pUnit.getUnitArtStyleType())
	##--------		Unofficial Bug Fix: End Modify			--------##

					if pPlayer.hasTrait(iSummoner):
						newUnit.setDuration(5)
					else:
						newUnit.setDuration(3)

					gc.getGame().decrementUnitClassCreatedCount(newUnit.getUnitClassType())
					gc.getGame().decrementUnitCreatedCount(newUnit.getUnitType())


			if pCity.getNumRealBuilding(iSmugglersPort) > 0:
				for iiX in xrange(iX-3, iX+4, 1):
					for iiY in xrange(iY-3, iY+4, 1):
						pLoopPlot = CyMap().plot(iiX,iiY)
						if not pLoopPlot.isNone():
							if pLoopPlot.isWater():
								if pLoopPlot.isVisibleOtherUnit(iPlayer):
									for i in xrange(pLoopPlot.getNumUnits()):
										pUnit = pLoopPlot.getUnit(i)
										if iTeam != pUnit.getTeam():
											pUnit.setBlockading(False)

			if pCity.getNumRealBuilding(iTempleHand) > 0 or pCity.getNumRealBuilding(iNewMulyr) > 0:
				if iSnowRange > 0:#There is no use wasting resources when nothing would get done
					iSnowOdds = iSnowRange//2
					iSnowOdds += self.getNumBonusEffective(iPlayer, iManaIce, -1)
					iSnowOdds += max(0, pCity.getNumBonuses(iManaIce))
					iSnowOdds -= max(0, pCity.getNumBonuses(iManaFire))
					iSnowOdds -= max(0, pCity.getNumBonuses(iManaNature))
					if iCiv == iIllians:
						iSnowOdds += 1
					if iSnowOdds > 1:#There is no use wasting resources when nothing would get done
						for iiX in xrange(iX-iSnowRange, iX+iSnowRange+1, 1):
							for iiY in xrange(iY-iSnowRange, iY+iSnowRange+1, 1):
								pLoopPlot = CyMap().plot(iiX,iiY)
								if not pLoopPlot.isNone():
									if not pLoopPlot.isWater():
										if pLoopPlot.isWithinCultureRange(iPlayer):
											if pLoopPlot.getImprovementType() == iSmoke:
												pLoopPlot.setImprovementType(-1)
											iDistance = CyMap().calculatePathDistance(pLoopPlot, pPlot)
											if iSnowOdds > iDistance > -1:
												iTimer = CyGame().getSorenRandNum(iSnowOdds - iDistance, "Temple of the Hand Snowfall")
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


			if pCity.getNumRealBuilding(iChancel) > 0:
				iRange = 2
				for iiX in xrange(iX-iRange, iX+iRange+1, 1):
					for iiY in xrange(iY-iRange, iY+iRange+1, 1):
						pLoopPlot = CyMap().plot(iiX,iiY)
						if not pLoopPlot.isNone():
							if pLoopPlot.isWithinCultureRange(iPlayer):
								if bNoPlotCounter:
									iTerrainNew = gc.getTerrainInfo(pLoopPlot.getTerrainType()).getTerrainDown()
									if iTerrainNew > -1:
										pLoopPlot.setTerrainType(iTerrainNew, True, True)
								elif pLoopPlot.getPlotCounter() > 0:
									pLoopPlot.changePlotCounter(pLoopPlot.getPlotCounter() * -1)
								iFeature = pLoopPlot.getFeatureType()
								if iFeature != -1:
									if iFeature == iTormentedSouls:
										pLoopPlot.setFeatureType(-1, -1)
									elif iFeature == iObsidian:
										if pLoopPlot.isFreshWater():
											pLoopPlot.setFeatureType(iFlood, 0)
										else:
											pLoopPlot.setFeatureType(iScrub, 0)
								iBonus = pLoopPlot.getBonusType(-1)
								if iBonus != -1:
									if iBonus == iGrapes:
										pLoopPlot.setBonusType(iWine)
									elif iBonus == iSheutStone:
										pLoopPlot.setBonusType(iMarble)
									elif iBonus == iToad:
										pLoopPlot.setBonusType(lMeats[CyGame().getSorenRandNum(len(lMeats), "Hell Convert Bonus")])
									elif iBonus == iNightmare:
										pLoopPlot.setBonusType(lMounts[CyGame().getSorenRandNum(len(lMounts), "Hell Convert Bonus")])
									elif iBonus == iRazorweed:
										pLoopPlot.setBonusType(lFibers[CyGame().getSorenRandNum(len(lFibers), "Hell Convert Bonus")])
									elif iBonus == iGulagarm:
										pLoopPlot.setBonusType(lTropicals[CyGame().getSorenRandNum(len(lTropicals), "Hell Convert Bonus")])
								iImp = pLoopPlot.getImprovementType()
								if iImp != -1:
									if iImp in [iHellfire, iPit]:
										pLoopPlot.setImprovementType(-1)
										CyGame().changeGlobalCounter(-2)
									elif iImp == iRuin:
										pLoopPlot.setImprovementType(-1)
										CyGame().changeGlobalCounter(-1)
									elif iImp == iGrave:
										if iFeature != iHallowedGround:
											pLoopPlot.setTempFeatureType(iHallowedGround, 0, 1)
											CyGame().changeGlobalCounter(-1)

##													newUnit = pPlayer.initUnit(iWarden, iiX, iiY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
####													newUnit.setPermanentSummon(True)
##													newUnit.setDuration(1)
##													pCity.applyBuildEffects(newUnit)

										elif pLoopPlot.getTempFeatureTimer() > 0:
											pLoopPlot.changeTempFeatureTimer(1)

									elif iImp == iSnakePillar:
										pLoopPlot.setImprovementType(iFarm)
										pLoopPlot.setBonusType(lCereals[CyGame().getSorenRandNum(len(lCereals), "Hell Convert Bonus")])

			# if pCity.getNumRealBuilding(iTowerElements) > 0:
				# iElemental = gc.getInfoTypeForString('PROMOTION_ELEMENTAL')
				# iLairGuardian = gc.getInfoTypeForString('PROMOTION_LAIR_GUARDIAN')

				# for i in xrange(pPlot.getNumUnits()):
					# pUnit = pPlot.getUnit(i)
					# if pUnit.isHasPromotion(iLairGuardian) and pUnit.isHasPromotion(iElemental):
						# if pUnit.getOwner() == pCity.getOwner():
							# break
				# else:
					# lList = []
					# for i in xrange(pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_AIR'))):
						# lList += ['UNIT_AIR_ELEMENTAL']
						# if i%2:
							# lList += ['UNIT_LIGHTNING_ELEMENTAL']
					# for i in xrange(pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_EARTH'))):
						# lList += ['UNIT_EARTH_ELEMENTAL']
					# for i in xrange(pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_FIRE'))):
						# lList += ['UNIT_FIRE_ELEMENTAL']
						# if i%3:
							# lList += ['UNIT_AZER']
					# for i in xrange(pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_ICE'))):
						# lList += ['UNIT_ICE_ELEMENTAL']
					# for i in xrange(pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_WATER'))):
						# lList += ['UNIT_WATER_ELEMENTAL']
					# for i in xrange(pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'))/8):
						# lList += ['UNIT_DJINN']
					# if len(lList) > 0:
						# iUnit = gc.getInfoTypeForString(lList.pop(CyGame().getSorenRandNum(len(lList), "Pick Elemental")))
						# newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
						# newUnit.setHasPromotion(iLairGuardian, True)
						# newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEFENSIVE'), True)
						# newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GUARDSMAN'), True)
						# pCity.applyBuildEffects(newUnit)
						# CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TOWER_ELEMENTS",(newUnit.getName(),pCity.getName())),'AS2D_DISCOVERBONUS',1,gc.getUnitInfo(newUnit.getUnitType()).getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)


			if pCity.getNumRealBuilding(iPlanarGate) > 0:

				if pCity.getNumBonuses(iManaDimensional) < 1:
					pCity.setNumRealBuilding(iPlanarGate, 0)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_PLANAR_GATE_CLOSED'), 1)

				elif CyGame().getSorenRandNum(1000, "Planar Gate") < iGateChance:
					listUnits = []
					for iUnit in listGateCreatures:
						infoUnit = gc.getUnitInfo(iUnit)
						iBuilding = infoUnit.getPrereqBuilding()
						if iBuilding != -1:
							if pCity.getNumBuilding(iBuilding) < 1:
								continue
						if pPlayer.getUnitClassCount(infoUnit.getUnitClassType()) < iMaxNumCreature:
							listUnits.append(iUnit)
					if len(listUnits) > 0:
						iUnit = listUnits.pop(CyGame().getSorenRandNum(len(listUnits), "Planar Gate"))
						newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PLANAR_GATE",(newUnit.getName(),pCity.getName())),'AS2D_DISCOVERBONUS',1,gc.getUnitInfo(newUnit.getUnitType()).getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
						pCity.applyBuildEffects(newUnit)
						iDuration = 1+CyGame().getSorenRandNum(iAC*gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getVictoryDelayPercent() / 50, "Planar Gate Duration")
						if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_SUMMONER')):
							iDuration += 1
						newUnit.setDuration(iDuration)
						newUnit.changeExperience(CyGame().getSorenRandNum(iAC//4, "Planar Gate XP"), -1, False, False, False)
						for iProm in lRemoveChaos:
							newUnit.setHasPromotion(iProm, False)

			if iCiv == iInfernal:
				if pCity.isHasReligion(iOrder):
					self.removeReligion(iOrder, pCity)
				if pCity.isHasReligion(iEmpyrean):
					self.removeReligion(iEmpyrean, pCity)
				if not pCity.isHasReligion(iVeil):
					pCity.setHasReligion(iVeil, True, True, True)
			elif iCiv == iMercurians:
				if pCity.isHasReligion(iOverlords):
					self.removeReligion(iOverlords, pCity)
				if pCity.isHasReligion(iVeil):
					self.removeReligion(iVeil, pCity)

			if pCity.getNumBuilding(iAqueduct) > 0:
				if not pPlot.isFreshWater():
					pPlot.setFeatureType(iFreshWater, 0)
			elif pPlot.getFeatureType() == iFreshWater:
				pPlot.setFeatureType(-1,-1)



	def doAvatarDefection(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iLeader = pPlayer.getLeaderType()
		dLeaders = {
				gc.getInfoTypeForString('LEADER_BARBARIAN')	:	'UNITCLASS_ORTHUS'	,
				gc.getInfoTypeForString('LEADER_BASIUM')	:	'UNITCLASS_BASIUM'	,
				gc.getInfoTypeForString('LEADER_AURIC')		:	'UNITCLASS_AURIC'	,
				gc.getInfoTypeForString('LEADER_ANAGANTIOS')	:	'UNITCLASS_ANAGANTIOS'	,
				gc.getInfoTypeForString('LEADER_DUMANNIOS')	:	'UNITCLASS_DUMANNIOS'	,
				gc.getInfoTypeForString('LEADER_RIUROS')	:	'UNITCLASS_RIUROS'	,
				gc.getInfoTypeForString('LEADER_HYBOREM')	:	'UNITCLASS_HYBOREM'	,
				gc.getInfoTypeForString('LEADER_JUDECCA')	:	'UNITCLASS_JUDECCA'	,
				gc.getInfoTypeForString('LEADER_LETHE')		:	'UNITCLASS_LETHE'	,
				gc.getInfoTypeForString('LEADER_MERESIN')	:	'UNITCLASS_MERESIN'	,
				gc.getInfoTypeForString('LEADER_OUZZA')		:	'UNITCLASS_OUZZA'	,
				gc.getInfoTypeForString('LEADER_SALLOS')	:	'UNITCLASS_SALLOS'	,
				gc.getInfoTypeForString('LEADER_STATIUS')	:	'UNITCLASS_STATIUS'	,
				gc.getInfoTypeForString('LEADER_GOSEA')		:	'UNITCLASS_GOSEA'	,
				gc.getInfoTypeForString('LEADER_DUIN')		:	'UNITCLASS_DUIN'	,
				gc.getInfoTypeForString('LEADER_CARDITH')	:	'UNITCLASS_EURABATRES'	,
				}
		if iLeader in dLeaders:
			iAvatar = gc.getInfoTypeForString(dLeaders[iLeader])
			if CyGame().getUnitClassCreatedCount(iAvatar) > 0:
				if pPlayer.getUnitClassCount(iAvatar) == 0:
					iIllusion = gc.getInfoTypeForString('PROMOTION_ILLUSION')
					iDark = gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION')
					for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
						if iPlayer2 != iPlayer:
							pPlayer2 = gc.getPlayer(iPlayer2)
							if pPlayer2.getLeaderType() != iLeader:
								if pPlayer2.getUnitClassCount(iAvatar) > 0:
									for pUnit in PyPlayer(iPlayer2).getUnitList():
										if pUnit.getUnitClassType() == iAvatar:
											pUnit.setAvatarOfCivLeader(False)
											if pUnit.getDuration() != 0 or pUnit.isHasPromotion(iIllusion) or pUnit.isHasPromotion(iDark):
												pass
											else:
												pPlot = pUnit.plot()
												if pPlayer.getNumCities() > 0:
													pCity = pPlayer.getCapitalCity()
													if pCity.isNone():
														pCity = CyMap().findCity(pUnit.getX(), pUnit.getY(), iPlayer, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION,pPlayer.getCity(-1))
														if pCity.isNone():
															pCity = pPlayer.firstCity(False)[0]
													pPlot = pCity.plot()
												elif pPlayer.getNumUnits() > 0:
													pPlot = pPlayer.firstUnit(False)[0].plot()
												if not pPlot.isNone():
													if not pPlot.isVisibleEnemyUnit(iPlayer):
														CyInterface().addMessage(iPlayer2, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_AVATAR_DEFECT_SELF", (pUnit.getName(),)), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, pUnit.getButton(), gc.getInfoTypeForString('COLOR_RED'), pUnit.getX(), pUnit.getY(), True, True)
														newUnit = pPlayer.initUnit(pUnit.getUnitType(), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_SOUTH)
														bImmortal = pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMORTAL'))
														self.makeMortal(pUnit)
														newUnit.convert(pUnit)
														newUnit.setAvatarOfCivLeader(True)
														newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REBEL'), False)
														newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LOYALTY'), True)
														if bImmortal:
															newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMORTAL'), True)
														break

	def doEffectCrucible(self, pCity):
		iNum = (CyGame().getGameTurn() - pCity.getBuildingOriginalTime(gc.getInfoTypeForString('BUILDING_CRUCIBLE'))) #The Age of the Crucible
		iNum *= 100/gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getVictoryDelayPercent() #Adjust by game speed
		iNum = CyGame().getSorenRandNum(iNum, "Crucible Potency")
		iNum /= 7
##		iNum = 1000#For testing
		if iNum < 1:
			return False

		lMatronae = [gc.getInfoTypeForString('UNIT_MORRIGAN'), gc.getInfoTypeForString('UNIT_CLIODNA'), gc.getInfoTypeForString('UNIT_SARABRIDE'), gc.getInfoTypeForString('UNIT_BASIUM_ANIMANS')]

		iDeath = gc.getInfoTypeForString('BONUS_MANA_DEATH')
		iFire = gc.getInfoTypeForString('BONUS_MANA_FIRE')
		iWater = gc.getInfoTypeForString('BONUS_MANA_WATER')
		iLife = gc.getInfoTypeForString('BONUS_MANA_LIFE')
		iFaneOfFate = gc.getInfoTypeForString('BUILDING_FANE_OF_FATE')
		iFoundryOfVengeance = gc.getInfoTypeForString('BUILDING_FOUNDRY_OF_VENGEANCE')
		iDocksOfDreams = gc.getInfoTypeForString('BUILDING_DOCKS_OF_DREAMS')
		iCathedralOfVigilance = gc.getInfoTypeForString('BUILDING_CATHEDRAL_OF_VIGILANCE')


		CyGame().changeGlobalCounter(-iNum/2)
		iRed = gc.getInfoTypeForString('COLOR_RED')
		listMana = []
		for iLoopBonus in xrange(gc.getNumBonusInfos()):
			if gc.getBonusInfo(iLoopBonus).isMana():
				listMana.append(iLoopBonus)

		if iDeath in listMana and PyHelpers.PyGame().doesBuildingExist(iFaneOfFate):
			listMana.remove(iDeath)
		if iFire in listMana and PyHelpers.PyGame().doesBuildingExist(iFoundryOfVengeance):
			listMana.remove(iFire)
		if iWater in listMana and PyHelpers.PyGame().doesBuildingExist(iDocksOfDreams):
			listMana.remove(iWater)
		if iLife in listMana and PyHelpers.PyGame().doesBuildingExist(iCathedralOfVigilance):
			listMana.remove(iLife)

		listPlotsMana = []
		listCities = []
		for i in xrange(CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.isNone():
				continue
			if pPlot.getBonusType(-1) in listMana:
				listPlotsMana.append(pPlot)
			elif pPlot.isCity():
				pLoopCity = pPlot.getPlotCity()
				if pLoopCity.isProductionProject():
					listCities.append(pLoopCity)
					continue
				for iLoopBonus in listMana:
					if pLoopCity.getFreeBonus(iLoopBonus) > 0:
						listCities.append(pLoopCity)
						break
		while len(listPlotsMana) > 0:
			pPlot = listPlotsMana.pop(CyGame().getSorenRandNum(len(listPlotsMana), "Crucible - Pick Mana Plot"))
			iBonus = pPlot.getBonusType(-1)
			sButton = gc.getBonusInfo(iBonus).getButton()
			sDescription = gc.getBonusInfo(iBonus).getDescription()
			iX = pPlot.getX()
			iY = pPlot.getY()
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isHuman():
					if pLoopPlayer.isAlive():
						CyInterface().addMessage(iLoopPlayer, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_CRUCIBLE_DRAIN_MANA", (sDescription,)), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, iRed, iX, iY, True, True)
			CyCamera().JustLookAtPlot(pPlot)
			pPlot.setBonusType(-1)
			pPlot.setRealBonusType(iBonus)
##			iImp = pPlot.getImprovementType()
##			if iImp != -1:
##				infoImp = gc.getImprovementInfo(iImp)
##				if infoImp.isPermanent() and not infoImp.isUnique():#Is a Mana Node
##					pPlot.setImprovementType(-1)
##					pPlot.setRealImprovementType(iImp)
			iNum -= 1
			if iNum < 1:
				return False
		while len(listCities) > 0:
			pCity = listCities.pop(CyGame().getSorenRandNum(len(listCities), "Crucible - Pick City"))
			# if pCity.isProductionProject():
				# iHinder = min(pCity.getProduction(),iNum)
				# pCity.changeProduction(-iHinder)
				# infoP = gc.getProjectInfo(pCity.getProductionProject())
				# CyInterface().addMessage(pCity.getOwner(), True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_CRUCIBLE_HINDER_PROJECT", (infoP.getDescription(),iHinder,)), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, infoP.getButton(), iRed, pCity.getX(), pCity.getY(), True, True)
			listCityMana = []
			for iLoopBonus in listMana:

				# if iLoopBonus == iDeath and pCity.getNumBuilding(iFaneOfFate) > 0:
					# continue
				# if iLoopBonus == iFire and pCity.getNumBuilding(iFoundryOfVengeance) > 0:
					# continue
				# if iLoopBonus == iWater and pCity.getNumBuilding(iDocksOfDreams) > 0:
					# continue


				for i in range(pCity.getFreeBonus(iLoopBonus)):
					listCityMana.append(iLoopBonus)
			while len(listCityMana) > 0:
				iMana = listCityMana.pop(CyGame().getSorenRandNum(len(listCityMana), "Crucible - Pick City Mana Type"))
				sButton = gc.getBonusInfo(iMana).getButton()
				sDescription = gc.getBonusInfo(iMana).getDescription()
				CyInterface().addMessage(pCity.getOwner(), True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_CRUCIBLE_DRAIN_MANA", (sDescription + ' in ' + pCity.getName(),)), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, iRed, pCity.getX(), pCity.getY(), True, True)
				pCity.changeFreeBonus(iMana, -1)
				iNum -= 1
				if iNum < 1:
					return False
		listMagicTiers = [
			#Affinity Magic
			[
				'PROMOTION_AFFINITY_AIR',
				'PROMOTION_AFFINITY_BODY',
				'PROMOTION_AFFINITY_CHAOS',
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
				],
			#Archmage level Magic
			[
				'PROMOTION_AIR3',
				'PROMOTION_BODY3',
				'PROMOTION_CHAOS3',
				'PROMOTION_DEATH3',
				'PROMOTION_DEATH_ARAWN3',
				'PROMOTION_DIMENSIONAL3',
				'PROMOTION_EARTH3',
				'PROMOTION_ENCHANTMENT3',
				'PROMOTION_ENTROPY3',
				'PROMOTION_FIRE3',
				'PROMOTION_FORCE3',
				'PROMOTION_ICE3',
				'PROMOTION_LAW3',
				'PROMOTION_LIFE3',
				'PROMOTION_METAMAGIC3',
				'PROMOTION_MIND3',
				'PROMOTION_NATURE3',
				'PROMOTION_SHADOW3',
				'PROMOTION_SPIRIT3',
				'PROMOTION_SUN3',
				'PROMOTION_WATER3',
				'PROMOTION_CHANNELING4',
				'PROMOTION_CHANNELING3',#The Tower of Mastery could keep adding this back, so including it on the list actually slows the death of magic
				'PROMOTION_TWINCAST'
				],
			#Mage level Magic
			[
				'PROMOTION_AIR2',
				'PROMOTION_BODY2',
				'PROMOTION_CHAOS2',
				'PROMOTION_DEATH2',
				'PROMOTION_DEATH_ARAWN2',
				'PROMOTION_DIMENSIONAL2',
				'PROMOTION_EARTH2',
				'PROMOTION_ENCHANTMENT2',
				'PROMOTION_ENTROPY2',
				'PROMOTION_FIRE2',
				'PROMOTION_FORCE2',
				'PROMOTION_ICE2',
				'PROMOTION_LAW2',
				'PROMOTION_LIFE2',
				'PROMOTION_METAMAGIC2',
				'PROMOTION_MIND2',
				'PROMOTION_NATURE2',
				'PROMOTION_SHADOW2',
				'PROMOTION_SPIRIT2',
				'PROMOTION_SUN2',
				'PROMOTION_WATER2',
				'PROMOTION_CHANNELING2',
				'PROMOTION_EXTENSION2',
				'PROMOTION_UNHOLY_TAINT'
				],
			#Adept level Magic
			[
				'PROMOTION_AIR1',
				'PROMOTION_BODY1',
				'PROMOTION_CHAOS1',
				'PROMOTION_AFFINITY_CREATION',
				'PROMOTION_DEATH1',
				'PROMOTION_DEATH_ARAWN1',
				'PROMOTION_DIMENSIONAL1',
				'PROMOTION_EARTH1',
				'PROMOTION_ENCHANTMENT1',
				'PROMOTION_ENTROPY1',
				'PROMOTION_FIRE1',
				'PROMOTION_FORCE1',
				'PROMOTION_ICE1',
				'PROMOTION_LAW1',
				'PROMOTION_LIFE1',
				'PROMOTION_METAMAGIC1',
				'PROMOTION_MIND1',
				'PROMOTION_NATURE1',
				'PROMOTION_SHADOW1',
				'PROMOTION_SPIRIT1',
				'PROMOTION_SUN1',
				'PROMOTION_WATER1',
				'PROMOTION_ARCANE',
				'PROMOTION_CHANNELING1',
				'PROMOTION_DIVINE',
				'PROMOTION_EXTENSION1'
				'PROMOTION_ILLUSIONIST',
				'PROMOTION_SUMMONER',
				'PROMOTION_SUNDERED'
				],
			#Spell Buffs
			[
				'PROMOTION_BLIND',
				'PROMOTION_BLUR',
				'PROMOTION_BURNING_BLOOD',
				'PROMOTION_CHARMED',
				'PROMOTION_COURAGE',
				'PROMOTION_CROWN_OF_BRILLANCE',
				'PROMOTION_DANCE_OF_BLADES',
				'PROMOTION_ENCHANTED_BLADE',
				'PROMOTION_FAIR_WINDS',
				'PROMOTION_FLAMING_ARROWS',
				'PROMOTION_HASTED',
				'PROMOTION_HERALDS_BLESSING',
				'PROMOTION_HIDDEN',
				'PROMOTION_IMMORTAL',
				'PROMOTION_MUTATED',
				'PROMOTION_REGENERATION',
				'PROMOTION_SLOW',
				'PROMOTION_SHADOWWALK',
				'PROMOTION_SHIELD_OF_FAITH',
				'PROMOTION_STONESKIN',
				'PROMOTION_TEMPERANCE',
				'PROMOTION_WATER_WALKING',
				'PROMOTION_WATER_WALKING_TEMP',
				'PROMOTION_WITHERED'
			],
			#Magic dependent races
			[
##				'PROMOTION_ANGEL',
##				'PROMOTION_AVATAR',
##				'PROMOTION_DEMON',
				'PROMOTION_GOLEM',
				'PROMOTION_ILLUSION',
				'PROMOTION_ELEMENTAL'
				'PROMOTION_UNDEAD',
				'PROMOTION_VAMPIRE'
				],
			#Construct level Magic
			[
				'PROMOTION_ATHAME',
				'PROMOTION_BLACK_MIRROR',
				'PROMOTION_CROWN_OF_AKHARIEN',
				'PROMOTION_CROWN_OF_COMMAND',
				'PROMOTION_DRAGONS_HOARD',
				'PROMOTION_EMPTY_BIER',
				'PROMOTION_GELA',
				'PROMOTION_GOLDEN_HAMMER',
				'PROMOTION_HEALING_SALVE',
				'PROMOTION_HEARTSTONE',
				'PROMOTION_INFERNAL_GRIMOIRE',
				'PROMOTION_JADE_TORC',
				'PROMOTION_KANNAS_WHIP',
				'PROMOTION_ANGELORUM_CAVEA',
				'PROMOTION_SAWOL_CAVEA',
				'PROMOTION_MATRON_ESSENDI',
				'PROMOTION_MOKKAS_CAULDRON',
				'PROMOTION_MASK_OF_ESUS',
				'PROMOTION_NETHER_BLADE',
				'PROMOTION_ORTHUSS_AXE',
				'PROMOTION_PIECES_OF_BARNAXUS',
				'PROMOTION_PIECES_OF_MITHRIL_GOLEM',
				'PROMOTION_POTION_OF_INVISIBILITY',
				'PROMOTION_POTION_OF_RESTORATION',
				'PROMOTION_ROD_OF_WINDS',
				'PROMOTION_SCORCHED_STAFF',
				'PROMOTION_SHIELD_OF_BALANCE',
				'PROMOTION_SEVEN_LEAGUE_BOOTS',
				'PROMOTION_SPEAR_OF_MAJOSI',
				'PROMOTION_SPELLSTAFF',
				'PROMOTION_STAFF_OF_SOULS',
				'PROMOTION_TIMOR_MASK',
				'PROMOTION_WAR'
				]
			]
		listUnits = PyHelpers.PyGame().getAllUnitList()
		for listMagic in listMagicTiers:
			while len(listMagic) > 0:
				iProm = gc.getInfoTypeForString(listMagic.pop(CyGame().getSorenRandNum(len(listMagic), "Crucible - Pick Promotion")))
				infoP = gc.getPromotionInfo(iProm)
				sNamePromotion = infoP.getDescription()
				sButton = infoP.getButton()
				for pUnit in listUnits:
					if pUnit.getUnitType() in lMatronae:continue

					if pUnit.isHasPromotion(iProm):
						sNameUnit = pUnit.getName()
						if infoP.isRace():
							CyInterface().addMessage(pUnit.getOwner(), True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_CRUCIBLE_KILL", (sNameUnit,)), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, iRed, pUnit.getX(), pUnit.getY(), True, True)
							pUnit.kill()
						else:
							pUnit.setHasPromotion(iProm, False)
							CyInterface().addMessage(pUnit.getOwner(), True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_CRUCIBLE_REMOVE_PROMOTION", (sNameUnit, sNamePromotion,)), '', InterfaceMessageTypes.MESSAGE_TYPE_INFO, sButton, iRed, pUnit.getX(), pUnit.getY(), True, True)
						iNum -= 1
						if iNum < 1:
							return False
		if iNum > 0:
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive():
					pLoopPlayer.changeDisableSpellcasting(2)
		return False



	def getNumTeamImprovements(self, pPlayer, iImprovement):
		iNum = 0
##		iImprovement = gc.getInfoTypeForString(sImprovement)
		for pTeammate in self.getTeammates(pPlayer):
			iNum += pTeammate.getImprovementCount(iImprovement)
		return iNum



	def chooseRandomAvailibleMana(self, pUnit, listMana = []):
		if len(listMana) == 0:
			for iLoopBonus in xrange(gc.getNumBonusInfos()):
				if gc.getBonusInfo(iLoopBonus).isMana():
					listMana.append(iLoopBonus)

		listManaSupply = []
		for iMana in listMana:
			for i in range(self.getNumBonusEffective(pUnit.getOwner(), iMana, pUnit)):
				listManaSupply.append(iMana)
		if len(listManaSupply) < 1:
			return -1
		return listManaSupply.pop(CyGame().getSorenRandNum(len(listManaSupply), "Random Mana"))

	def getNumBonusEffective(self, iPlayer, iBonus, unit=-1):
		return gc.getPlayer(iPlayer).getNumAvailableBonuses(iBonus) + self.getNumSupplimentalMana(iPlayer, iBonus, unit)

	def getNumSupplimentalMana(self, iPlayer, iBonus, unit=-1):
		iNum = 0
		if gc.getBonusInfo(iBonus).isMana():
			if PyHelpers.PyGame().doesBuildingExist(gc.getInfoTypeForString('BUILDING_CRUCIBLE')):

				if gc.getInfoTypeForString('BONUS_MANA_DEATH'):
					if not PyHelpers.PyGame().doesBuildingExist(gc.getInfoTypeForString('BUILDING_FANE_OF_FATE')):
						return 0
				elif gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					if not PyHelpers.PyGame().doesBuildingExist(gc.getInfoTypeForString('UNIT_FOUNDRY_OF_VENGEANCE')):
						return 0
				elif gc.getInfoTypeForString('BONUS_MANA_WATER'):
					if not PyHelpers.PyGame().doesBuildingExist(gc.getInfoTypeForString('UNIT_DOCKS_OF_DREAMS')):
						return 0
				elif gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					if not PyHelpers.PyGame().doesBuildingExist(gc.getInfoTypeForString('UNIT_CATHEDRAL_OF_VENGEANCE')):
						return 0
				else:
					return 0
			iNum += self.getNumSupplimentalManaPlayer(iPlayer, iBonus)
			if unit != -1:
				iNum += self.getNumSupplimentalManaUnit(iBonus, unit)
		return iNum


	def getNumSupplimentalManaUnit(self, iBonus, unit):
		iNum = 0

		iPrereq = gc.getUnitInfo(unit.getUnitType()).getPrereqAndBonus()
		if iPrereq == iBonus:
			iNum += 3
		elif iPrereq != -1 and unit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_ADEPT'):
			iNum = -21
			return iNum

		pPlot = unit.plot()
		pArea = unit.area()
		iTeam = unit.getTeam()
		if iBonus == pPlot.getBonusType(iTeam):
			iNum += 7

		for iProm in xrange(gc.getNumPromotionInfos()):
			if unit.isHasPromotion(iProm):
				if gc.getPromotionInfo(iProm).getBonusPrereq() == iBonus:
					iNum += abs(gc.getPromotionInfo(iProm).getAIWeight()//50)

		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ADVENTURER')):
			if iBonus == gc.getInfoTypeForString('BONUS_MANA_AIR'):
				iNum += 1


		iRace = unit.getRace()
		if iRace != -1:
			if iRace == gc.getInfoTypeForString('PROMOTION_ELF'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_NATURE'):
					iNum += 1
			elif iRace == gc.getInfoTypeForString('PROMOTION_DWARF'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_EARTH'):
					iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_AIR'):
					iNum -= 1
			elif iRace == gc.getInfoTypeForString('PROMOTION_UNDEAD'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH'):
					iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					iNum -= 3
			elif iRace == gc.getInfoTypeForString('PROMOTION_DEMON'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
					iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SUN'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LAW'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
					iNum -= 1
			elif iRace == gc.getInfoTypeForString('PROMOTION_ANGEL'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_BODY'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ICE'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_MIND'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SHADOW'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH'):
					iNum -= 1



		iRel = unit.getReligion()
		if iRel != -1:
			if iRel == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_LAW'):
					iNum += 3
				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FORCE'):
					# iNum += 1
				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					# iNum += 1
				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
					# iNum += 1

				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
					iNum -= 7
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_NATURE'):
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_SUN'):
					iNum += 3

				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					# iNum += 1
				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					# iNum += 1
				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					# iNum += 1
				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
					# iNum += 1


				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SHADOW'):
					iNum -= 7

				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LAW'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_BODY'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ICE'):
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_EARTH'):
					iNum += 3
				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
					# iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_AIR'):
					iNum -= 7
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_MIND'):
					iNum -= 3

			elif iRel == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_NATURE'):
					iNum += 3
				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					# iNum += 1
				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_AIR'):
					# iNum += 1
				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					# iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ICE'):
					iNum -= 7
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					iNum -= 3

			elif iRel == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_WATER'):
					iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_MIND'):
					iNum += 2
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
					iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH'):
					iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					iNum -= 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SUN'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LAW'):
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_SHADOW'):
					iNum += 3
				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_MIND'):
					# iNum += 1
				# elif iBonus == gc.getInfoTypeForString('BONUS_MANA_BODY'):
					# iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SUN'):
					iNum -= 7
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LAW'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
					iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_MIND'):
					iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'):
					iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_BODY'):
					iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
					iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					iNum += 1

				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					iNum -= 7
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LAW'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
					iNum -= 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON'):
				pPlayer = gc.getPlayer(unit.getOwner())
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_BODY'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_BLOOD')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_CORAL')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SUN'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_DAWN')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FORCE'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_ELDER')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_AIR'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_FEATHERED')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ACHERON')):
						iNum += 6
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_GRAVE')):
						iNum += 3
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRACOLICH')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_GOLD')):
						iNum += 3
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_EURABATRES')):
						iNum += 7
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_OBSIDIAN')):
						iNum += 3
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ABASHI')):
						iNum += 6
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_PIT')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_RUNE')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_WATER'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_SCALED')):
						iNum += 3
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_THALATTH')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_NATURE'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_SEED')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SHADOW'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_SHADOW')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LAW'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_SHIELD')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_SHIMMERING')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_SIEGE')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_SPIRE')):
						iNum += 3
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_MIND'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_VAULT_WYRM')):
						iNum += 3
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_THALATTH')):
						iNum += 2
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ICE'):
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRAGON_WINTER')):
						iNum += 3
					if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DRIFA')):
						iNum += 4


			elif iRel == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_ICE'):
					iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_WATER'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_EARTH'):
					# iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_NATURE'):
					iNum -= 2
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_MATRONAE'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					iNum += 3
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_WATER'):
					iNum += 3
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH'):
					iNum += 3
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					iNum += 1

			elif iRel == gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_FORCE'):
					iNum += 3
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					iNum += 2
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
					iNum += 1
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					iNum += 1
			elif iRel == gc.getInfoTypeForString('RELIGION_UNBLEMISHED'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
					# iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					# iNum += 1
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_NATURE'):
					iNum += 1


			elif iRel == gc.getInfoTypeForString('RELIGION_LAERAN_CORD'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'):
					iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					# iNum += 1

			elif iRel == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
					iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_FORCE'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_WATER'):
					# iNum += 1
			elif iRel == gc.getInfoTypeForString('RELIGION_FOXMEN'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_AIR'):
					iNum += 3
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_EARTH'):
					iNum -= 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					# iNum += 1
			elif iRel == gc.getInfoTypeForString('RELIGION_COVEN'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'):
					iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
					# iNum -= 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					# iNum -= 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
					# iNum += 1
			elif iRel == gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_MIND'):
					iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'):
					# iNum -= 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_BODY'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_SHADOW'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_FORCE'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'):
					# iNum += 1
			elif iRel == gc.getInfoTypeForString('RELIGION_ANOINTED'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_BODY'):
					iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH'):
					# iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_SHADOW'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
					# iNum += 1



			elif iRel == gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
					iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH'):
					# iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_BODY'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_AIR'):
					# iNum += 1
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_LAW'):
					iNum -= 3
			elif iRel == gc.getInfoTypeForString('RELIGION_EMBER_LEGION'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
					# iNum += 2
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_LAW'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
					# iNum += 1
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_WATER'):
					iNum -= 3
			elif iRel == gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH'):
					iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_WATER'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_ICE'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
					# iNum += 1
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					iNum += 1
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					iNum -= 3
			elif iRel == gc.getInfoTypeForString('RELIGION_RINGGIVER'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
					iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_EARTH'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
					# iNum -= 3
			elif iRel == gc.getInfoTypeForString('RELIGION_HOUSE_OF_PLENTY'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					iNum += 3
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
					# iNum += 1
				# if iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
					# iNum += 1
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
					iNum -= 3

		else:
			iAlignment = self.getUnitAlignment(unit)
			if iAlignment == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SUN'),
								gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'),
								gc.getInfoTypeForString('BONUS_MANA_LAW'),
								gc.getInfoTypeForString('BONUS_MANA_CREATION'),
								gc.getInfoTypeForString('BONUS_MANA_LIFE')]:
					iNum += 1
				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
								gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
								gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_ICE'),
								gc.getInfoTypeForString('BONUS_MANA_SHADOW'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'),
								gc.getInfoTypeForString('BONUS_MANA_DEATH'),
								gc.getInfoTypeForString('BONUS_MANA_FORCE')]:
					iNum -= 1

			elif iAlignment == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
								gc.getInfoTypeForString('BONUS_MANA_DEATH'),
								gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_ICE'),
								gc.getInfoTypeForString('BONUS_MANA_SHADOW'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')]:
					iNum += 1
				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SUN'),
									gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
									gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'),
									gc.getInfoTypeForString('BONUS_MANA_LAW'),
									gc.getInfoTypeForString('BONUS_MANA_LIFE'),
									gc.getInfoTypeForString('BONUS_MANA_FORCE')]:
					iNum -= 1



		return iNum

	def getNumSupplimentalManaPlayer(self, iPlayer, iBonus):
		iNum = 0
		pPlayer = gc.getPlayer(iPlayer)
		if gc.getBonusInfo(iBonus).isMana():
			iRel = pPlayer.getStateReligion()
			if iRel == gc.getInfoTypeForString('RELIGION_MATRONAE'):
				if iBonus in [gc.getInfoTypeForString('BONUS_MANA_DEATH'),gc.getInfoTypeForString('BONUS_MANA_FIRE'),gc.getInfoTypeForString('BONUS_MANA_WATER')]:
					return 21

			if PyHelpers.PyGame().doesBuildingExist(gc.getInfoTypeForString('BUILDING_CRUCIBLE')):
				return 0

			if pPlayer.isBarbarian():
				return CyMap().getNumBonuses(iBonus)

			iOvercouncil = gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')
			iUndercouncil = gc.getInfoTypeForString('DIPLOVOTE_UNDERCOUNCIL')
			if pPlayer.isFullMember(iOvercouncil):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH') and CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DEATH_MANA')):
					return -pPlayer.getNumAvailableBonuses(iBonus)
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL') and CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_DIMENSIONAL_MANA')):
					return -pPlayer.getNumAvailableBonuses(iBonus)
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY') and CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_ENTROPY_MANA')):
					return -pPlayer.getNumAvailableBonuses(iBonus)
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS') and CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_CHAOS_MANA')):
					return -pPlayer.getNumAvailableBonuses(iBonus)
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SHADOW') and CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_SHADOW_MANA')):
					return -pPlayer.getNumAvailableBonuses(iBonus)
				else:
					for jPlayer in xrange(gc.getMAX_PLAYERS()):
						if iPlayer != jPlayer:
							pPlayer2 = gc.getPlayer(jPlayer)
							if pPlayer2.isFullMember(iOvercouncil):
								if pPlayer2.isAlive():
									iPatron = self.getPatronSphere(pPlayer2)
									if iBonus == iPatron:
										iNum += 1

			elif pPlayer.isFullMember(iUndercouncil):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_SUN') and CyGame().isVotePassed(gc.getInfoTypeForString('VOTE_NO_SUN_MANA')):
					return -pPlayer.getNumAvailableBonuses(iBonus)
				else:
					for jPlayer in xrange(gc.getMAX_PLAYERS()):
						if iPlayer != jPlayer:
							pPlayer2 = gc.getPlayer(jPlayer)
							if pPlayer2.isFullMember(iUndercouncil):
								if pPlayer2.isAlive():
									iPatron = self.getPatronSphere(pPlayer2)
									if iBonus == iPatron:
										iNum += 1

			iPatron = self.getPatronSphere(pPlayer)
			if iBonus == iPatron:
				iNum += 1
			if iBonus == self.getOppositeSphere(iPatron):
				iNum -= 2

			iLeader = pPlayer.getLeaderType()
			if iLeader == gc.getInfoTypeForString('LEADER_ALEXIS'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
								gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_DEATH')]:
					iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SUN'):
					iNum -= 1
			elif iLeader == gc.getInfoTypeForString('LEADER_AMELANCHIER'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_NATURE'),
								gc.getInfoTypeForString('BONUS_MANA_AIR'),
								gc.getInfoTypeForString('BONUS_MANA_LIFE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_ANAGANTIOS'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ICE'),
								gc.getInfoTypeForString('BONUS_MANA_LAW')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_ARENDEL'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_NATURE'),
								gc.getInfoTypeForString('BONUS_MANA_CREATION'),
								gc.getInfoTypeForString('BONUS_MANA_LIFE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_ARTURUS'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_EARTH'),
								gc.getInfoTypeForString('BONUS_MANA_LAW'),
								gc.getInfoTypeForString('BONUS_MANA_ICE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_AURIC'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'),
								gc.getInfoTypeForString('BONUS_MANA_ICE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_AVERAX'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'),
								gc.getInfoTypeForString('BONUS_MANA_MIND')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_BASIUM'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
					iNum += 2
			elif iLeader == gc.getInfoTypeForString('LEADER_BEERI'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'),
								gc.getInfoTypeForString('BONUS_MANA_EARTH')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_BRAEDEN'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ICE'),
								gc.getInfoTypeForString('BONUS_MANA_WATER')]:
					iNum += 2
			elif iLeader == gc.getInfoTypeForString('LEADER_CAPRIA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_LAW'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_LIFE'),
								gc.getInfoTypeForString('BONUS_MANA_CHAOS')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_CARDITH'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_CREATION'),
								gc.getInfoTypeForString('BONUS_MANA_LIFE'),
								gc.getInfoTypeForString('BONUS_MANA_NATURE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_CASSIEL'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_CREATION'),
								gc.getInfoTypeForString('BONUS_MANA_LIFE'),
								gc.getInfoTypeForString('BONUS_MANA_FORCE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_CHARADON'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
								gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_ICE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_DAIN'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_SUN')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_DECIUS'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_LAW'),
								gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_SUN'),
								gc.getInfoTypeForString('BONUS_MANA_MIND')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_DUIN'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_DUMANNIOS'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ICE'),
								gc.getInfoTypeForString('BONUS_MANA_MIND')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_EINION'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
								gc.getInfoTypeForString('BONUS_MANA_SUN'),
								gc.getInfoTypeForString('BONUS_MANA_METAMAGIC')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_ETHNE'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE')]:
					iNum += 1

			elif iLeader == gc.getInfoTypeForString('LEADER_FAERYL'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SHADOW'),
								gc.getInfoTypeForString('BONUS_MANA_NATURE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_FALAMAR'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_AIR'),
								gc.getInfoTypeForString('BONUS_MANA_CREATION'),
								gc.getInfoTypeForString('BONUS_MANA_WATER')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_FLAUROS'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_SHADOW')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_FURIA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_DEATH')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_GARRIM'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_GOSEA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'),
								gc.getInfoTypeForString('BONUS_MANA_SPIRIT')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_HANNAH'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_WATER'),
								gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
								gc.getInfoTypeForString('BONUS_MANA_DEATH')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_HAFGAN'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_HYBOREM'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
								gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_JONAS'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_JUDECCA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
								gc.getInfoTypeForString('BONUS_MANA_EARTH')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_KANE'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SUN'),
								gc.getInfoTypeForString('BONUS_MANA_BODY')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_KANDROS'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_LAW'),
								gc.getInfoTypeForString('BONUS_MANA_EARTH')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_KEELYN'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_KOUN'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_LAW'),
								gc.getInfoTypeForString('BONUS_MANA_MIND')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_LETHE'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
								gc.getInfoTypeForString('BONUS_MANA_ENTROPY')]:
					iNum += 1
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_CHAOS')]:
					iNum -= 1
			elif iLeader == gc.getInfoTypeForString('LEADER_MALCHAVIC'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_FORCE'),
								gc.getInfoTypeForString('BONUS_MANA_MIND')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_MAHALA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
								gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_MAHON'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
								gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_DEATH')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_MELISANDRE'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'):
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_MERESIN'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_ENTROPY')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_OS-GABELLA'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'):
					iNum += 3
			elif iLeader == gc.getInfoTypeForString('LEADER_OSTANES'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_AIR'):
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_OUZZA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_ENTROPY')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_PERPENTACH'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'),
								gc.getInfoTypeForString('BONUS_MANA_MIND')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_RHOANNA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_LAW')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_RIUROS'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ICE'),
								gc.getInfoTypeForString('BONUS_MANA_AIR')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_RIVANNA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SHADOW'),
								gc.getInfoTypeForString('BONUS_MANA_DEATH')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_SABATHIEL'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_LAW'),
								gc.getInfoTypeForString('BONUS_MANA_FORCE'),
								gc.getInfoTypeForString('BONUS_MANA_LIFE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_SALLOS'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ENTROPY')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_SANDALPHON'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
								gc.getInfoTypeForString('BONUS_MANA_SHADOW')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_SHEELBA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_LAW')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_SHEKINAH'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'),
								gc.getInfoTypeForString('BONUS_MANA_SHADOW')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_STATIUS'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
								gc.getInfoTypeForString('BONUS_MANA_ENTROPY')]:
					iNum += 1
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_BODY')]:
					iNum -= 1
			elif iLeader == gc.getInfoTypeForString('LEADER_TASUNKE'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_BODY')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_TEBRYN'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'),
								gc.getInfoTypeForString('BONUS_MANA_DEATH'),
								gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_TETHIRA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_LAW'),
								gc.getInfoTypeForString('BONUS_MANA_SPIRIT')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_THESSA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_DEATH'),
								gc.getInfoTypeForString('BONUS_MANA_NATURE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_THESSALONICA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_FORCE'),
								gc.getInfoTypeForString('BONUS_MANA_SPIRIT')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_TYA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'),
								gc.getInfoTypeForString('BONUS_MANA_ENTROPY')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_ULDANOR'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_MIND'):
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_VALLEDIA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'),
								gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_SHADOW')]:
					iNum += 1
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SUN'):
					iNum -= 1
			elif iLeader == gc.getInfoTypeForString('LEADER_VARN'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_SUN'):
					iNum += 2
				elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SHADOW'):
					iNum -= 2
			elif iLeader == gc.getInfoTypeForString('LEADER_VOLANNA'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SHADOW'),
								gc.getInfoTypeForString('BONUS_MANA_ICE')]:
					iNum += 1
			elif iLeader == gc.getInfoTypeForString('LEADER_WEEVIL'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_MIND'):
					iNum += 1


			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
					return -pPlayer.getNumAvailableBonuses(iBonus)


			if iRel == -1:
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_FORCE'):
					iNum += 1
			elif iRel == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_LAW'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_FORCE'),
								gc.getInfoTypeForString('BONUS_MANA_LIFE'),
								gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT')]:
					iNum += 1

				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
									gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
									gc.getInfoTypeForString('BONUS_MANA_DEATH'),
									gc.getInfoTypeForString('BONUS_MANA_CREATION'),
									gc.getInfoTypeForString('BONUS_MANA_NATURE'),
									gc.getInfoTypeForString('BONUS_MANA_SPIRIT')]:
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SUN'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
								gc.getInfoTypeForString('BONUS_MANA_LIFE'),
								gc.getInfoTypeForString('BONUS_MANA_CREATION')]:
					iNum += 1

				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
									gc.getInfoTypeForString('BONUS_MANA_SHADOW'),
									gc.getInfoTypeForString('BONUS_MANA_BODY'),
									gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'),
									gc.getInfoTypeForString('BONUS_MANA_ICE')]:
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_EARTH'),
								gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'),
								gc.getInfoTypeForString('BONUS_MANA_ICE'),
								gc.getInfoTypeForString('BONUS_MANA_BODY')]:
					iNum += 1

				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
									gc.getInfoTypeForString('BONUS_MANA_AIR'),
									gc.getInfoTypeForString('BONUS_MANA_MIND')]:
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_NATURE'),
								gc.getInfoTypeForString('BONUS_MANA_LIFE'),
								gc.getInfoTypeForString('BONUS_MANA_AIR'),
								gc.getInfoTypeForString('BONUS_MANA_CREATION')]:
					iNum += 1

				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ICE'),
									gc.getInfoTypeForString('BONUS_MANA_FIRE'),
									gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
									gc.getInfoTypeForString('BONUS_MANA_LAW')]:
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_WATER'),
								gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
								gc.getInfoTypeForString('BONUS_MANA_BODY')]:
					iNum += 1

				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SUN'),
									gc.getInfoTypeForString('BONUS_MANA_FIRE'),
									gc.getInfoTypeForString('BONUS_MANA_LAW'),
									gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT')]:
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SHADOW'),
								gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')]:
					iNum += 1

				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SUN'),
									gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
									gc.getInfoTypeForString('BONUS_MANA_LAW'),
									gc.getInfoTypeForString('BONUS_MANA_FIRE')]:
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
								gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'),
								gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE')]:
					iNum += 1

				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_CREATION'),
									gc.getInfoTypeForString('BONUS_MANA_LAW'),
									gc.getInfoTypeForString('BONUS_MANA_LIFE'),
									gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
									gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT')]:
					iNum -= 1

			elif iRel == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ICE'),
								gc.getInfoTypeForString('BONUS_MANA_WATER'),
								gc.getInfoTypeForString('BONUS_MANA_LAW'),
								gc.getInfoTypeForString('BONUS_MANA_METAMAGIC')]:
					iNum += 1

				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_FIRE'),
									gc.getInfoTypeForString('BONUS_MANA_NATURE'),
									gc.getInfoTypeForString('BONUS_MANA_LIFE')]:
					iNum -= 1


			iAlignment = pPlayer.getAlignment()
			if iAlignment == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SUN'),
								gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'),
								gc.getInfoTypeForString('BONUS_MANA_LAW'),
								gc.getInfoTypeForString('BONUS_MANA_CREATION'),
								gc.getInfoTypeForString('BONUS_MANA_LIFE')]:
					iNum += 1
				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
								gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
								gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_ICE'),
								gc.getInfoTypeForString('BONUS_MANA_SHADOW'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'),
								gc.getInfoTypeForString('BONUS_MANA_DEATH'),
								gc.getInfoTypeForString('BONUS_MANA_FORCE')]:
					iNum -= 1

			elif iAlignment == gc.getInfoTypeForString('ALIGNMENT_NEUTRAL'):
				if iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
					iNum -= 1
				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_FORCE'),
									gc.getInfoTypeForString('BONUS_MANA_NATURE'),
									gc.getInfoTypeForString('BONUS_MANA_AIR'),
									gc.getInfoTypeForString('BONUS_MANA_EARTH'),
									gc.getInfoTypeForString('BONUS_MANA_WATER'),
									gc.getInfoTypeForString('BONUS_MANA_DEATH'),
									gc.getInfoTypeForString('BONUS_MANA_METAMAGIC')]:
					iNum += 1
			elif iAlignment == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
				if iBonus in [	gc.getInfoTypeForString('BONUS_MANA_ENTROPY'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_BODY'),
								gc.getInfoTypeForString('BONUS_MANA_CHAOS'),
								gc.getInfoTypeForString('BONUS_MANA_DEATH'),
								gc.getInfoTypeForString('BONUS_MANA_MIND'),
								gc.getInfoTypeForString('BONUS_MANA_ICE'),
								gc.getInfoTypeForString('BONUS_MANA_SHADOW'),
								gc.getInfoTypeForString('BONUS_MANA_FIRE'),
								gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')]:
					iNum += 1
				elif iBonus in [	gc.getInfoTypeForString('BONUS_MANA_SUN'),
									gc.getInfoTypeForString('BONUS_MANA_SPIRIT'),
									gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'),
									gc.getInfoTypeForString('BONUS_MANA_LAW'),
									gc.getInfoTypeForString('BONUS_MANA_LIFE'),
									gc.getInfoTypeForString('BONUS_MANA_FORCE')]:
					iNum -= 1

		return iNum

	def doTurnKhazad(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.getNumCities() > 0:
			# lfgr 04/2021: Simplified
			iNewVault = ffhDefines.getKhazadVault( pPlayer )
			for pyCity in PyPlayer(iPlayer).getCityList():
				pCity = pyCity.GetCy()
				for eVault, _ in ffhDefines.getKhazadVaultsWithMinGold() :
					pCity.setNumRealBuilding( eVault, 0)
				pCity.setNumRealBuilding(iNewVault, 1)




	def doTurnLuchuirp(self, iPlayer):
		iBarnaxus = gc.getInfoTypeForString('UNITCLASS_BARNAXUS')
		if gc.getPlayer(iPlayer).getUnitClassCount(iBarnaxus) > 0:
			iGolem = gc.getInfoTypeForString('PROMOTION_GOLEM')
			pBarnaxus = -1
			bEmp1 = False
			bEmp2 = False
			bEmp3 = False
			bEmp4 = False
			bEmp5 = False
			iCombat1 = gc.getInfoTypeForString('PROMOTION_COMBAT1')
			iCombat2 = gc.getInfoTypeForString('PROMOTION_COMBAT2')
			iCombat3 = gc.getInfoTypeForString('PROMOTION_COMBAT3')
			iCombat4 = gc.getInfoTypeForString('PROMOTION_COMBAT4')
			iCombat5 = gc.getInfoTypeForString('PROMOTION_COMBAT5')
			iEmpower1 = gc.getInfoTypeForString('PROMOTION_EMPOWER1')
			iEmpower2 = gc.getInfoTypeForString('PROMOTION_EMPOWER2')
			iEmpower3 = gc.getInfoTypeForString('PROMOTION_EMPOWER3')
			iEmpower4 = gc.getInfoTypeForString('PROMOTION_EMPOWER4')
			iEmpower5 = gc.getInfoTypeForString('PROMOTION_EMPOWER5')

			lGolems = []
			py = PyPlayer(iPlayer)
			for pUnit in py.getUnitList():
				if pUnit.getUnitClassType() == iBarnaxus :
					pBarnaxus = pUnit
				elif pUnit.isHasPromotion(iGolem):
					lGolems.append(pUnit)
			if pBarnaxus != -1 :
				bEmp1 = bool(pBarnaxus.isHasPromotion(iCombat1))
				bEmp2 = bool(pBarnaxus.isHasPromotion(iCombat2))
				bEmp3 = bool(pBarnaxus.isHasPromotion(iCombat3))
				bEmp4 = bool(pBarnaxus.isHasPromotion(iCombat4))
				bEmp5 = bool(pBarnaxus.isHasPromotion(iCombat5))
			for pUnit in lGolems:
				pUnit.setHasPromotion(iEmpower1, bEmp1)
				pUnit.setHasPromotion(iEmpower2, bEmp2)
				pUnit.setHasPromotion(iEmpower3, bEmp3)
				pUnit.setHasPromotion(iEmpower4, bEmp4)
				pUnit.setHasPromotion(iEmpower5, bEmp5)


	def findClearPlot(self, pUnit=-1, plot=-1):
		BestPlot = -1
		iBestPlot = 0
		if pUnit != -1:
			iX = pUnit.getX()
			iY = pUnit.getY()
			iOwner = pUnit.getOwner()
			for iiX in xrange(iX-1, iX+2, 1):
				for iiY in xrange(iY-1, iY+2, 1):
					pPlot = CyMap().plot(iiX,iiY)
					if not pPlot.isNone():
						iCurrentPlot = 0
						if not pPlot.at(iX,iY):
							if pPlot.getNumUnits() == 0:
								if pUnit.canMoveOrAttackInto(pPlot, False):
									iCurrentPlot += 5
							for i in xrange(pPlot.getNumUnits()):
								if pPlot.getUnit(i).getOwner() == iOwner:
									if pUnit.canMoveOrAttackInto(pPlot, False):
										iCurrentPlot += 15
							if pPlot.isCity():
								if pPlot.getPlotCity().getOwner() == iOwner:
									iCurrentPlot += 50
						if iCurrentPlot >= 1:
							iCurrentPlot += CyGame().getSorenRandNum(5, "FindClearPlot")
							if iCurrentPlot >= iBestPlot:
								BestPlot = pPlot
								iBestPlot = iCurrentPlot
			return BestPlot

		iX = plot.getX()
		iY = plot.getY()
		for iiX in xrange(iX-1, iX+2, 1):
			for iiY in xrange(iY-1, iY+2, 1):
				iCurrentPlot = 0
				pPlot = CyMap().plot(iiX,iiY)
				if not pPlot.isNone():
					if pPlot.getNumUnits() == 0:
						if pPlot.isWater() == plot.isWater() and not pPlot.isPeak() and not pPlot.isCity() and not pPlot.isImpassable():
							iCurrentPlot += 5
					if iCurrentPlot >= 1:
						iCurrentPlot += CyGame().getSorenRandNum(5, "FindClearPlot")
						if iCurrentPlot >= iBestPlot:
							BestPlot = pPlot
							iBestPlot = iCurrentPlot
		return BestPlot




	def findClearPlotImprovement(self, plot):
		for r in xrange(0,5,1):
			iX = plot.getX()
			iY = plot.getY()
			for iiX in xrange(iX-r, iX+1+r, 1):
				for iiY in xrange(iY-r, iY+1+r, 1):
					pPlot = CyMap().plot(iiX,iiY)
					if pPlot.isNone():
						continue
					if pPlot.isCity():
						continue
					if pPlot.isWater():
						continue
					if pPlot.isImpassable():
						continue
					if pPlot.getBonusType(-1) != -1:
						continue
					if pPlot.getImprovementType() == -1:
						return pPlot
					if not gc.getImprovementInfo(pPlot.getImprovementType()).isPermanent():
						return pPlot
		return -1


	def getUnitAlignment(self, pUnit, bCheckPromotions = True):
		if pUnit.getRace() == gc.getInfoTypeForString('PROMOTION_ANGEL'):
			return gc.getInfoTypeForString('ALIGNMENT_GOOD')
		elif pUnit.getRace() in [gc.getInfoTypeForString('PROMOTION_DEMON'), gc.getInfoTypeForString('PROMOTION_UNDEAD')]:
			return gc.getInfoTypeForString('ALIGNMENT_EVIL')
		iReligion = pUnit.getReligion()
		iAlignment = gc.getInfoTypeForString('ALIGNMENT_NEUTRAL')
		if iReligion in [gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE'),gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL'),gc.getInfoTypeForString('RELIGION_GREY_COUNCIL')]:
			return -1
		elif iReligion == gc.getInfoTypeForString('RELIGION_MATRONAE'):
			if PyHelpers.PyGame().doesBuildingExist(gc.getInfoTypeForString('BUILDING_CATHEDRAL_OF_VIGILANCE')):
				return gc.getInfoTypeForString('ALIGNMENT_GOOD')
			return -1
		elif iReligion in [
							gc.getInfoTypeForString('RELIGION_COVEN'),
							gc.getInfoTypeForString('RELIGION_EMBER_LEGION'),
							gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'),
							gc.getInfoTypeForString('RELIGION_ANOINTED'),
							gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD'),
							gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY'),
							gc.getInfoTypeForString('RELIGION_WHITE_HAND'),
							gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'),
							gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS')
							]:
			iAlignment = gc.getInfoTypeForString('ALIGNMENT_EVIL')
		elif iReligion in [
							gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'),
							gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS'),
							gc.getInfoTypeForString('RELIGION_RINGGIVER'),
							gc.getInfoTypeForString('RELIGION_UNBLEMISHED'),
							gc.getInfoTypeForString('RELIGION_HOUSE_OF_PLENTY'),
							gc.getInfoTypeForString('RELIGION_THE_ORDER'),
							gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH')
							]:
			iAlignment = gc.getInfoTypeForString('ALIGNMENT_GOOD')
		elif iReligion == gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON'):
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
									gc.getInfoTypeForString('UNITCLASS_VAULT_WYRM'),
									gc.getInfoTypeForString('UNITCLASS_DRAGON_WINTER'),
									gc.getInfoTypeForString('UNITCLASS_DRACOLICH'),
								]
			listNeutralDragons = [
									gc.getInfoTypeForString('UNITCLASS_DRAGON_ELDER'),
									gc.getInfoTypeForString('UNITCLASS_DRAGON_FANG'),
									gc.getInfoTypeForString('UNITCLASS_DRAGON_FEATHERED'),
									gc.getInfoTypeForString('UNITCLASS_DRAGON_SCALED'),
									gc.getInfoTypeForString('UNITCLASS_DRAGON_SEED'),
									gc.getInfoTypeForString('UNITCLASS_DRAGON_GRAVE'),
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
			pPlayer = gc.getPlayer(pUnit.getOwner())
			eTeam = gc.getTeam(pUnit.getTeam())
			if pUnit.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
				iCountGood += 3
			elif pUnit.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
				iCountEvil += 2
			if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
				iCountGood += 2
			elif pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
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

			iAlignment = gc.getInfoTypeForString('ALIGNMENT_NEUTRAL')
			if iCountGood > iCountEvil + iCountNeutral:
				iAlignment = gc.getInfoTypeForString('ALIGNMENT_GOOD')
			if iCountEvil > iCountNeutral:
				iAlignment = gc.getInfoTypeForString('ALIGNMENT_EVIL')
		if bCheckPromotions:
			lEvilProms = [
							'PROMOTION_UNHOLY_TAINT',
							'PROMOTION_VAMPIRE',
							'PROMOTION_POSSESSED',
							'PROMOTION_CIRCLE_OF_GAELAN',

							'PROMOTION_INFERNAL_GRIMOIRE',
							'PROMOTION_KANNAS_WHIP',

							'PROMOTION_AFFINITY_DEATH',
							'PROMOTION_DEATH1',
							'PROMOTION_DEATH2',
							'PROMOTION_DEATH3',

							'PROMOTION_CHAOS2',
							'PROMOTION_DIMENSIONAL2',
							'PROMOTION_ENTROPY2',

							'PROMOTION_BODY3',
							'PROMOTION_CHAOS3',
							'PROMOTION_DIMENSIONAL3',
							'PROMOTION_FIRE3',
							'PROMOTION_ICE3',
							'PROMOTION_ENTROPY3',
							'PROMOTION_MIND3',
							'PROMOTION_SHADOW3',

							'PROMOTION_PACT_WITH_HYBOREM',
							'PROMOTION_PACT_WITH_JUDECCA',
							'PROMOTION_PACT_WITH_LETHE',
							'PROMOTION_PACT_WITH_MERESIN',
							'PROMOTION_PACT_WITH_OUZZA',
							'PROMOTION_PACT_WITH_SALLOS',
							'PROMOTION_PACT_WITH_STATIUS',

							'PROMOTION_PACT_WITH_WINTER',
							'PROMOTION_OCCISOR'

					]
			for sProm in lEvilProms:
				if pUnit.isHasPromotion(gc.getInfoTypeForString(sProm)):
					return gc.getInfoTypeForString('ALIGNMENT_EVIL')

		return iAlignment

	def findAfterlife(self, unit):
		if unit.isAlive():
			for iProm in [gc.getInfoTypeForString('PROMOTION_CAPTUS_CAVEAE_ANGELORUM'),gc.getInfoTypeForString('PROMOTION_NETHERBIND'),gc.getInfoTypeForString('PROMOTION_INCARCERATUS_JUDICII')]:
				if unit.isHasPromotion(iProm):
					return -1
			if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GREY')):
				if unit.getLevel() > 6:
					return -1
				elif CyGame().getSorenRandNum(100, "Grey claimed by Laroth") > 15*unit.getLevel():
					return -1

			# if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GALLOWBLIGHT')):
				# return gc.getInfoTypeForString('UNIT_SKELETON')
			iAlignment = self.getUnitAlignment(unit)
			if iAlignment == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
				return gc.getInfoTypeForString('UNIT_MANES')
			elif iAlignment != -1:
				iBasiumPlayer = self.getLeader(gc.getInfoTypeForString('LEADER_BASIUM'))
				if iBasiumPlayer != -1:
					iAngel = gc.getInfoTypeForString('UNIT_ANGEL')
					if unit.getOwner() == iBasiumPlayer:
						return iAngel
					elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HERALDS_BLESSING')):
						return iAngel
					elif unit.getReligion() in [gc.getInfoTypeForString('RELIGION_THE_ORDER'), gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'), gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH')]:
						return iAngel
					elif unit.getTeam() == gc.getPlayer(iBasiumPlayer).getTeam():
						if CyGame().getSorenRandNum(10, "Mercurian Team unit becomes Angel") < 3:
							return iAngel
		return -1

	def doAfterlife(self, pUnit):
		iAfterlife = self.findAfterlife(pUnit)
		if iAfterlife != -1:
			iAngel = gc.getInfoTypeForString('UNIT_ANGEL')
			iManes = gc.getInfoTypeForString('UNIT_MANES')
			iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
			iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
			iXP = pUnit.getExperience()
			pPlot = pUnit.plot()
			iPlayer = pUnit.getOwner()
			iReligion= pUnit.getReligion()
			if iAfterlife == iAngel:
				self.giftUnit(iAngel, iMercurians, iXP, pPlot, iPlayer, iReligion)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HERALDS_BLESSING'), False)
			elif iAfterlife == iManes:


				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_HYBOREM')):
					iPactPlayer = self.getLeader(gc.getInfoTypeForString('LEADER_HYBOREM'))
					if iPactPlayer != -1:
						self.giftUnitToPlayer(iManes, iPactPlayer, iXP, pPlot, iPlayer,iReligion)

				elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_JUDECCA')):
					iPactPlayer = self.getLeader(gc.getInfoTypeForString('LEADER_JUDECCA'))
					if iPactPlayer != -1:
						self.giftUnitToPlayer(iManes, iPactPlayer, iXP, pPlot, iPlayer,iReligion)

				elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_LETHE')):
					iPactPlayer = self.getLeader(gc.getInfoTypeForString('LEADER_LETHE'))
					if iPactPlayer != -1:
						self.giftUnitToPlayer(iManes, iPactPlayer, iXP, pPlot, iPlayer,iReligion)

				elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_MERESIN')):
					iPactPlayer = self.getLeader(gc.getInfoTypeForString('LEADER_MERESIN'))
					if iPactPlayer != -1:
						self.giftUnitToPlayer(iManes, iPactPlayer, iXP, pPlot, iPlayer,iReligion)

				elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_OUZZA')):
					iPactPlayer = self.getLeader(gc.getInfoTypeForString('LEADER_OUZZA'))
					if iPactPlayer != -1:
						self.giftUnitToPlayer(iManes, iPactPlayer, iXP, pPlot, iPlayer,iReligion)

				elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_SALLOS')):
					iPactPlayer = self.getLeader(gc.getInfoTypeForString('LEADER_SALLOS'))
					if iPactPlayer != -1:
						self.giftUnitToPlayer(iManes, iPactPlayer, iXP, pPlot, iPlayer,iReligion)

				elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_STATIUS')):
					iPactPlayer = self.getLeader(gc.getInfoTypeForString('LEADER_STATIUS'))
					if iPactPlayer != -1:
						self.giftUnitToPlayer(iManes, iPactPlayer, iXP, pPlot, iPlayer,iReligion)

				elif gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_ASCENSION')) > 0:
					if iReligion == gc.getInfoTypeForString('RELIGION_WHITE_HAND') or pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PACT_WITH_WINTER')):
						iAuricPlayer = self.getLeader(gc.getInfoTypeForString('LEADER_AURIC'))
						if iAuricPlayer != -1:
							pAuricPlayer = gc.getPlayer(iAuricPlayer)
							if pAuricPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')):
								self.giftUnitToPlayer(iManes, iAuricPlayer, iXP, pPlot, iPlayer,iReligion)
								return
				else:
					self.giftUnit(iManes, iInfernal, iXP, pPlot, iPlayer, iReligion)

	def genesis(self, iPlayer):
		bAllowBloomAllImprovements = gc.getPlayer(iPlayer).getCivilizationType() in [gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'), gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'), gc.getInfoTypeForString('CIVILIZATION_KURIOTATES')]

		if not bAllowBloomAllImprovements:
			lBloomableImprovements = [	-1,
							gc.getInfoTypeForString('IMPROVEMENT_CAMP'),
							gc.getInfoTypeForString('IMPROVEMENT_LUMBERMILL'),
							gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES'),
							gc.getInfoTypeForString('IMPROVEMENT_YGGDRASIL'),
							gc.getInfoTypeForString('IMPROVEMENT_TOMB_OF_SUCELLUS'),
							gc.getInfoTypeForString('IMPROVEMENT_MANA_NATURE'),
							gc.getInfoTypeForString('IMPROVEMENT_MANA_CREATION')
							]

		iForestNew = gc.getInfoTypeForString('FEATURE_FOREST_NEW')
		dFeatures = {	gc.getInfoTypeForString('FEATURE_FOREST')		:	gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT'),
				iForestNew						:	gc.getInfoTypeForString('FEATURE_FOREST'),
				gc.getInfoTypeForString('FEATURE_FOREST_BURNT')		:	gc.getInfoTypeForString('FEATURE_FOREST'),
				gc.getInfoTypeForString('FEATURE_SCRUB')		:	iForestNew,
				gc.getInfoTypeForString('FEATURE_BLIZZARD')		:	-1,
				gc.getInfoTypeForString('FEATURE_ICE')			:	-1
				}

		dTerrains = {	gc.getInfoTypeForString('TERRAIN_SNOW')			:	gc.getInfoTypeForString('TERRAIN_TUNDRA'),
				gc.getInfoTypeForString('TERRAIN_TUNDRA')		:	gc.getInfoTypeForString('TERRAIN_PLAINS'),
				gc.getInfoTypeForString('TERRAIN_DESERT')		:	gc.getInfoTypeForString('TERRAIN_PLAINS'),
				gc.getInfoTypeForString('TERRAIN_PLAINS')		:	gc.getInfoTypeForString('TERRAIN_GRASS'),
				gc.getInfoTypeForString('TERRAIN_MARSH')		:	gc.getInfoTypeForString('TERRAIN_GRASS'),


				gc.getInfoTypeForString('TERRAIN_GLACIER')		:	gc.getInfoTypeForString('TERRAIN_TUNDRA'),
				gc.getInfoTypeForString('TERRAIN_WASTELAND')		:	gc.getInfoTypeForString('TERRAIN_PLAINS'),
				gc.getInfoTypeForString('TERRAIN_BURNING_SANDS')	:	gc.getInfoTypeForString('TERRAIN_PLAINS'),
				gc.getInfoTypeForString('TERRAIN_FIELDS_OF_PERDITION')	:	gc.getInfoTypeForString('TERRAIN_GRASS'),
				gc.getInfoTypeForString('TERRAIN_MARSH')		:	gc.getInfoTypeForString('TERRAIN_GRASS'),
				gc.getInfoTypeForString('TERRAIN_SHALLOWS')		:	gc.getInfoTypeForString('TERRAIN_GRASS')
				}

		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getOwner() == iPlayer:
				pPlot.changePlotCounter(-100)
				if not pPlot.isWater():
					iTerrain = pPlot.getTerrainType()
					if iTerrain in dTerrains:
						pPlot.setTerrainType(dTerrains[iTerrain],True,True)
					if not pPlot.isPeak():
						iFeature = pPlot.getFeatureType()
						if iFeature == -1:
							if bAllowBloomAllImprovements or pPlot.getImprovementType() in lBloomableImprovements:
								if pPlot.canHaveFeature(iForestNew):
									pPlot.setFeatureType(iForestNew, 0)
						elif iFeature in dFeatures:
							iFeatureNew = dFeatures[iFeature]
							pPlot.setFeatureType(iFeatureNew, 0)

	def getAshenVeilCities(self, iCasterPlayer, iCasterID, iNum):
		pCasterPlayer = gc.getPlayer(iCasterPlayer)
		pCaster = pCasterPlayer.getUnit(iCasterID)
		iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
		ltVeilCities = []
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			pTargetPlayer = gc.getPlayer(iPlayer)
			if not pTargetPlayer.isAlive():
				continue

			if pTargetPlayer.getTeam() == pCasterPlayer.getTeam():
				continue

			if (gc.getTeam(pCasterPlayer.getTeam()).isVassal(pTargetPlayer.getTeam())):
				continue

			iBaseModifier = 100
			if pTargetPlayer.getStateReligion() == iVeil:
				iBaseModifier -= 20
			if pTargetPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
				iBaseModifier -= 10

			for pyCity in PyPlayer(iPlayer).getCityList():
				pTargetCity = pyCity.GetCy()
		
				if pTargetCity.isHasReligion(iVeil) and not pTargetCity.isCapital():
					iValue = pTargetCity.getPopulation() * 100
					iValue += pTargetCity.getCulture(iPlayer) / 3
					iValue += pTargetCity.getNumBuildings() * 10
					iValue += pTargetCity.getNumWorldWonders() * 100
					iValue += pTargetCity.countNumImprovedPlots()
					iModifier = iBaseModifier
					pCasterCapital = pCasterPlayer.getCapitalCity()
					if not pCasterCapital.isNone() and pTargetCity.area() is pCasterCapital.area():
						iModifier += 10
					if pTargetCity.area().getCitiesPerPlayer(iCasterPlayer) > 0:
						iModifier += 10
					if pCasterPlayer.getNumCities() > 0:
						iMinDistance = -1
						
						for pyCity in PyPlayer(iCasterPlayer).getCityList():
							pLoopCity = pyCity.GetCy()
							if pLoopCity is pTargetCity:
								continue
							iDistance = stepDistance(pLoopCity.getX(), pLoopCity.getY(), pTargetCity.getX(), pTargetCity.getY())
							if iMinDistance == -1 or iMinDistance > iDistance:
								iMinDistance = iDistance
								
					if iMinDistance != -1:
							iModifier -= iMinDistance
					iModifier = max(0, iModifier)
					iValue *= iModifier
					iValue //= 100
					ltVeilCities.append((iValue, pTargetCity))

		ltVeilCities.sort()
		ltVeilCities.reverse()
		lpVeilCities = []
		if len(ltVeilCities) > 0:
			ltVeilCities = ltVeilCities[0:min(iNum, len(ltVeilCities))]
			lpVeilCities = [pCity for iValue, pCity in ltVeilCities]
		return lpVeilCities
##--------		Tweaked Hyborem: End Modify			--------##


	def getInfernalIngress(self,iRitualistPlayer):
		eRitualistTeam = gc.getTeam(gc.getPlayer(iRitualistPlayer).getTeam())
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
		iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
		iLair = gc.getInfoTypeForString('BUILDING_WYRMHOLD')
		iBestValue = 0
		pBestCity = -1
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			if iPlayer != iRitualistPlayer:
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive() and pPlayer.getCivilizationType() != iInfernal:
					for pyCity in PyPlayer(iPlayer).getCityList():
						pCity = pyCity.GetCy()
						if pCity.isHasReligion(iVeil) and not pCity.isCapital() and pCity.getNumRealBuilding(iLair) < 1:
							iValue = pCity.getPopulation() * 100
							iValue += pCity.getCulture(iPlayer) / 3
							iValue += pCity.getNumBuildings() * 10
							iValue += pCity.getNumWorldWonders() * 200
							iValue += pCity.countNumImprovedPlots()
							iValue += pCity.isHolyCity() * 100
							iValue -= pPlayer.AI_getAttitude(iRitualistPlayer)
							iTeam = pPlayer.getTeam()
							iValue += eRitualistTeam.getWarWeariness(iTeam)
							if eRitualistTeam.isAtWar(iTeam):
								iValue *= 100
							if pPlayer.getStateReligion() == iVeil:
								iValue /= 2000
							if iValue > iBestValue:
								pBestCity = pCity
								iBestValue = iValue
								
		return pBestCity


	def getAshenVeilCity(self, iNum):
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
		iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
		iBestValue1 = 0
		iBestValue2 = 0
		iBestValue3 = 0
		pBestCity1 = -1
		pBestCity2 = -1
		pBestCity3 = -1
		for iPlayer in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if (pPlayer.isAlive() and pPlayer.getCivilizationType() != iInfernal):
				for pyCity in PyPlayer(iPlayer).getCityList():
					pCity = pyCity.GetCy()
					if (pCity.isHasReligion(iVeil) and pCity.isCapital() == False):
						bValid = True
						iValue = pCity.getPopulation() * 100
						iValue += pCity.getCulture(iPlayer) / 3
						iValue += pCity.getNumBuildings() * 10
						iValue += pCity.getNumWorldWonders() * 100
						iValue += pCity.countNumImprovedPlots()
						if iValue > iBestValue1:
							iBestValue3 = iBestValue2
							pBestCity3 = pBestCity2
							iBestValue2 = iBestValue1
							pBestCity2 = pBestCity1
							iBestValue1 = iValue
							pBestCity1 = pCity
							bValid = False
						if (bValid and iValue > iBestValue2):
							iBestValue3 = iBestValue2
							pBestCity3 = pBestCity2
							iBestValue2 = iValue
							pBestCity2 = pCity
							bValid = False
						if (bValid and iValue > iBestValue3):
							iBestValue3 = iValue
							pBestCity3 = pCity
		if iNum == 1:
			return pBestCity1
		if iNum == 2:
			return pBestCity2
		if iNum == 3:
			return pBestCity3
		return -1


	def getCivilization(self, iCiv):
		i = -1
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.getCivilizationType() == iCiv:
				i = iPlayer
				if pPlayer.isAlive():
					return i
		return i

	def getHero(self, pPlayer):
		iHero = -1
		iCiv = pPlayer.getCivilizationType()
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
			if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_HYBOREM'):
				iHero = gc.getInfoTypeForString('UNITCLASS_HYBOREM')
			elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_LETHE'):
				iHero = gc.getInfoTypeForString('UNITCLASS_LETHE')
			elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_JUDECCA'):
				iHero = gc.getInfoTypeForString('UNITCLASS_JUDECCA')
			elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_OUZZA'):
				iHero = gc.getInfoTypeForString('UNITCLASS_OUZZA')
			elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MERESIN'):
				iHero = gc.getInfoTypeForString('UNITCLASS_MERESIN')
			elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SALLOS'):
				iHero = gc.getInfoTypeForString('UNITCLASS_SALLOS')
			elif pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_STATIUS'):
				iHero = gc.getInfoTypeForString('UNITCLASS_STATIUS')
		else:
			iHeroUnit = gc.getCivilizationInfo(iCiv).getHero()
			if iHeroUnit != -1:
				iHero = gc.getUnitInfo(iHeroUnit).getUnitClassType()
		return iHero

	def getLeader(self, iLeader):
		iLeaderPlayer = -1
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.getLeaderType() == iLeader:
				iLeaderPlayer = iPlayer
				if pPlayer.isAlive():
					return iLeaderPlayer
		return iLeaderPlayer


	def getPatronSphere(self, pPlayer):
		if not pPlayer.isBarbarian():
			iCiv = pPlayer.getCivilizationType()
			if iCiv not in [-1, gc.getInfoTypeForString('CIVILIZATION_BARBARIAN')]:
				infoC =  gc.getCivilizationInfo(pPlayer.getCivilizationType())
				if infoC != -1:
					iPalace = infoC.getCivilizationBuildings(gc.getInfoTypeForString('BUILDINGCLASS_PALACE'))
					if iPalace != -1:
						return gc.getBuildingInfo(iPalace).getFreeBonus()
		return -1

	def getOppositeSphere(self,iBonus):
		if iBonus == gc.getInfoTypeForString('BONUS_MANA_AIR'):
			return gc.getInfoTypeForString('BONUS_MANA_EARTH')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_BODY'):
			return gc.getInfoTypeForString('BONUS_MANA_SPIRIT')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CREATION'):
			return gc.getInfoTypeForString('BONUS_MANA_ENTROPY')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
			return gc.getInfoTypeForString('BONUS_MANA_LAW')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH'):
			return gc.getInfoTypeForString('BONUS_MANA_LIFE')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL'):
			return gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_EARTH'):
			return gc.getInfoTypeForString('BONUS_MANA_AIR')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
			return gc.getInfoTypeForString('BONUS_MANA_DIMENSIONAL')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
			return gc.getInfoTypeForString('BONUS_MANA_CREATION')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
			return gc.getInfoTypeForString('BONUS_MANA_WATER')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_FORCE'):
			return -1
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_ICE'):
			return gc.getInfoTypeForString('BONUS_MANA_NATURE')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
			return gc.getInfoTypeForString('BONUS_MANA_DEATH')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_LAW'):
			return gc.getInfoTypeForString('BONUS_MANA_CHAOS')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'):
			return gc.getInfoTypeForString('BONUS_MANA_MIND')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_MIND'):
			return gc.getInfoTypeForString('BONUS_MANA_METAMAGIC')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_NATURE'):
			return gc.getInfoTypeForString('BONUS_MANA_ICE')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SHADOW'):
			return gc.getInfoTypeForString('BONUS_MANA_SUN')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
			return gc.getInfoTypeForString('BONUS_MANA_BODY')
		elif iBonus == gc.getInfoTypeForString('BONUS_MANA_SUN'):
			return gc.getInfoTypeForString('BONUS_MANA_SHADOW')

	def getOpenPlayer(self):
		i = -1
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if i == -1 and not pPlayer.isEverAlive():
				i = iPlayer
		return i

	def getUnholyVersion(self, pUnit):
##		iUnit = -1
		iUnit = gc.getInfoTypeForString('UNIT_SKELETON')
		iUnitCombat = pUnit.getUnitCombatType()
		iTier = gc.getUnitInfo(pUnit.getUnitType()).getTier()
		if iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_ADEPT'):
			if iTier == 2:
				iUnit = gc.getInfoTypeForString('UNIT_IMP')
			elif iTier == 3:
				iUnit = gc.getInfoTypeForString('UNIT_MAGE')
			elif iTier == 4:
				iUnit = gc.getInfoTypeForString('UNIT_ARCHMAGE')
		elif iUnitCombat in [gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'), gc.getInfoTypeForString('UNITCOMBAT_BEAST')]:
			if iTier == 1:
				iUnit = -1
			elif iTier == 2:
				iUnit = gc.getInfoTypeForString('UNIT_HELLHOUND')
			elif iTier == 3:
				iUnit = gc.getInfoTypeForString('UNIT_PIT_BEAST')
			elif iTier == 4:
				iUnit = gc.getInfoTypeForString('UNIT_BEAST_OF_AGARES')
		elif iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_GUN'):
			iUnit = gc.getInfoTypeForString('UNIT_ARQUEBUS')
		elif iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_ARCHER'):
			if iTier == 2:
				iUnit = gc.getInfoTypeForString('UNIT_ARCHER')
			elif iTier == 3:
				iUnit = gc.getInfoTypeForString('UNIT_LONGBOWMAN')
			elif iTier == 4:
				iUnit = gc.getInfoTypeForString('UNIT_CROSSBOWMAN')
		elif iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_DISCIPLE'):
			if iTier == 2:
				iUnit = gc.getInfoTypeForString('UNIT_IMP')
			elif iTier == 3:
				iUnit = gc.getInfoTypeForString('UNIT_IMP')
			elif iTier == 4:
				iUnit = gc.getInfoTypeForString('UNIT_EIDOLON')
		elif iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_MELEE'):
			if iTier == 1:
				iUnit = gc.getInfoTypeForString('UNIT_SKELETON')
			elif iTier == 2:
				iUnit = gc.getInfoTypeForString('UNIT_DISEASED_CORPSE')
			elif iTier == 3:
				iUnit = gc.getInfoTypeForString('UNIT_CHAMPION')
			elif iTier == 4:
				iUnit = gc.getInfoTypeForString('UNIT_PHALANX')
		elif iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_MOUNTED'):
			if iTier == 2:
				iUnit = gc.getInfoTypeForString('UNIT_HORSEMAN')
			elif iTier == 3:
				iUnit = gc.getInfoTypeForString('UNIT_CHARIOT')
			elif iTier == 4:
				iUnit = gc.getInfoTypeForString('UNIT_DEATH_KNIGHT')
		elif iUnitCombat == gc.getInfoTypeForString('UNITCOMBAT_RECON'):
			if iTier == 1:
				iUnit = gc.getInfoTypeForString('UNIT_SCOUT')
			elif iTier == 2:
				iUnit = gc.getInfoTypeForString('UNIT_HELLHOUND')
			elif iTier == 3:
				iUnit = gc.getInfoTypeForString('UNIT_ASSASSIN')
			elif iTier == 4:
				iUnit = gc.getInfoTypeForString('UNIT_BEASTMASTER')
		return iUnit

	def getUnitPlayerID(self, pUnit):
		pPlayer = gc.getPlayer(pUnit.getOwner())
		iID = pUnit.getID()
		iUnitID = -1
		for iUnit in xrange(pPlayer.getNumUnits()):
			pLoopUnit = pPlayer.getUnit(iUnit)
			if pLoopUnit.getID() == iID:
				iUnitID = iUnit
		return iUnitID

	def giftUnit(self, iUnit, iCivilization, iXP = 0, pFromPlot = -1, iFromPlayer = -1, iReligion = -1):

		iAngel = gc.getInfoTypeForString('UNIT_ANGEL')
		iManes = gc.getInfoTypeForString('UNIT_MANES')
		if iUnit == iAngel:
			iChance = 50 - (CyGame().countCivPlayersAlive() * 3)
			iChance += iXP
			if iChance < 5:
				iChance = 5
			elif iChance > 95:
				iChance = 95
			if CyGame().getSorenRandNum(100, "Gift Unit") > iChance:
				iUnit = -1
		elif iUnit == iManes:
			iChance = 100 - (CyGame().countCivPlayersAlive() * 3)
			iChance += iXP
			if iChance < 5:
				iChance = 5
			elif iChance > 95:
				iChance = 95
			if CyGame().getSorenRandNum(100, "Gift Unit") > iChance:
				iUnit = -1

		if iUnit != -1:
			playerList = list()
			for iPlayer in xrange(gc.getMAX_PLAYERS()):#I decided to make this give units to only one random eligible player, not all of them
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive():
					if pPlayer.getCivilizationType() == iCivilization:
						playerList.append(iPlayer)

			while len(playerList) > 0:
				iPlayer = playerList.pop(CyGame().getSorenRandNum(len(playerList), "Gift Unit-pick player"))
				pPlayer = gc.getPlayer(iPlayer)
				iTeam = pPlayer.getTeam()

				listPlots = PyPlayer(iPlayer).getCityPlotList()
				if len(listPlots) < 1 or gc.getUnitInfo(iUnit).getWeaponTier() > 2:
					listPlots += PyPlayer(iPlayer).getActAsCityPlotList()

					if gc.getTeam(iTeam).getNumMembers() > 1:
						for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
							pLoopPlayer = gc.getPlayer(iLoopPlayer)
							if iTeam == pLoopPlayer.getTeam():
								if pLoopPlayer.isAlive():
									listPlots += PyPlayer(iLoopPlayer).getActAsCityPlotList()

				if len(listPlots) > 0:
					pPlot = listPlots.pop(CyGame().getSorenRandNum(len(listPlots), "Gift Unit-pick plot"))


					if pPlot.isWater():
						unitInfo = gc.getUnitInfo(iUnit)
						if not (unitInfo.getDomainType() == DomainTypes.DOMAIN_SEA or unitInfo.getFreePromotions(gc.getInfoTypeForString('PROMOTION_FLYING')) or unitInfo.getFreePromotions(gc.getInfoTypeForString('PROMOTION_WATER_WALKING')) or unitInfo.getFreePromotions(gc.getInfoTypeForString('PROMOTION_WATER_WALKING_TEMP'))):

							if len(listPlots) > 0:
								pPlot = listPlots.pop(CyGame().getSorenRandNum(len(listPlots), "Gift Unit-pick plot"))
							else:
								continue

					newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

					if pPlot.isCity():
						pCity = pPlot.getPlotCity()
						pCity.applyBuildEffects(newUnit)

					newUnit.changeExperience(iXP, -1, False, False, False)
					if newUnit.experienceNeeded() < iXP:
						newUnit.setPromotionReady(True)
					newUnit.setWeapons()

					if iReligion != -1:
						newUnit.setReligion(iReligion)
						iProm = -1
						if iReligion == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
							iProm = gc.getInfoTypeForString('PROMOTION_COMMAND1')
						elif iReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
							iProm = gc.getInfoTypeForString('PROMOTION_PERFECT_SIGHT')
						elif iReligion == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
							iProm = gc.getInfoTypeForString('PROMOTION_GUERILLA2')
						elif iReligion == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
							iProm = gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL')
						elif iReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
							iProm = gc.getInfoTypeForString('PROMOTION_AMPHIBIOUS')
						elif iReligion == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
							iProm = gc.getInfoTypeForString('PROMOTION_STEALTH')
						elif iReligion == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
							iProm = gc.getInfoTypeForString('PROMOTION_STIGMATA')
						elif iReligion == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
							iProm = gc.getInfoTypeForString('PROMOTION_IMMUNE_COLD')
						elif iReligion == gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON'):
							iProm = gc.getInfoTypeForString('PROMOTION_SCOURGE')
						elif iReligion == gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE'):
							iProm = gc.getInfoTypeForString('PROMOTION_MAGIC_IMMUNE')
						if iProm != -1:
							newUnit.setHasPromotion(iProm,True)

					if pPlayer.isHuman():
						if iUnit == iManes:
							CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ADD_MANES",()),'AS2D_UNIT_FALLS',1,'Art/Interface/Buttons/Promotions/Demon.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
						elif iUnit == iAngel:
							CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ADD_ANGEL",()),'AS2D_UNIT_FALLS',1,'Art/Interface/Buttons/Promotions/Angel.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
					elif iUnit == iManes and pPlot.isCity():
						pCity = pPlot.getPlotCity()
						if CyGame().getSorenRandNum(100, "Manes") < (100 - (pCity.getPopulation() * 5)):
							if newUnit.canCast(gc.getInfoTypeForString('SPELL_ADD_TO_CITY'), False):
									newUnit.cast(gc.getInfoTypeForString('SPELL_ADD_TO_CITY'))
					if pFromPlot != -1 and iFromPlayer != -1:
						if gc.getPlayer(iFromPlayer).isHuman():
							sPlayer = "<color=%d,%d,%d,%d>%s</color>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), pPlayer.getName() )
							if iUnit == iManes:
								CyInterface().addMessage(iFromPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_AFTERLIFE_PLAYER",( sPlayer,)),'AS2D_UNIT_FALLS',1,'Art/Interface/Buttons/Promotions/Demon.dds',ColorTypes(7),pFromPlot.getX(),pFromPlot.getY(),True,True)
							elif iUnit == iAngel:
								CyInterface().addMessage(iFromPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_AFTERLIFE_PLAYER",( sPlayer,)),'AS2D_UNIT_FALLS',1,'Art/Interface/Buttons/Promotions/Angel.dds',ColorTypes(7),pFromPlot.getX(),pFromPlot.getY(),True,True)
					break

	def giftUnitToPlayer(self, iUnit, iPlayer, iXP = 0, pFromPlot = -1, iFromPlayer = -1, iReligion = -1):
		if iPlayer != -1:
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isAlive():

				listPlots = PyPlayer(iPlayer).getActAsCityPlotList()
				if len(listPlots) > 0:
					pPlot = listPlots.pop(CyGame().getSorenRandNum(len(listPlots), "Gift Unit-pick plot"))

					iAngel = gc.getInfoTypeForString('UNIT_ANGEL')
					iManes = gc.getInfoTypeForString('UNIT_MANES')

					if iUnit in [iAngel, iManes]:
						iChance = 4000//(pPlayer.getNumUnits()+1)
						iChance += iXP
						if iChance < 5:
							iChance = 5
						if iChance > 95:
							iChance = 95
						if CyGame().getSorenRandNum(100, "Gift Unit to player") > iChance:
							iUnit = -1
					if iUnit != -1:
						newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

						if pPlot.isCity():
							pCity = pPlot.getPlotCity()
							pCity.applyBuildEffects(newUnit)

						newUnit.changeExperience(iXP, -1, False, False, False)
						if newUnit.experienceNeeded() < iXP:
							newUnit.setPromotionReady(True)
						newUnit.setWeapons()

						if iReligion != -1:
							newUnit.setReligion(iReligion)
							iProm = -1
							if iReligion == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
								iProm = gc.getInfoTypeForString('PROMOTION_COMMAND1')
							elif iReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
								iProm = gc.getInfoTypeForString('PROMOTION_PERFECT_SIGHT')
							elif iReligion == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
								iProm = gc.getInfoTypeForString('PROMOTION_GUERILLA2')
							elif iReligion == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
								iProm = gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL')
							elif iReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
								iProm = gc.getInfoTypeForString('PROMOTION_AMPHIBIOUS')
							elif iReligion == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
								iProm = gc.getInfoTypeForString('PROMOTION_STEALTH')
							elif iReligion == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
								iProm = gc.getInfoTypeForString('PROMOTION_STIGMATA')
							elif iReligion == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
								iProm = gc.getInfoTypeForString('PROMOTION_IMMUNE_COLD')
							elif iReligion == gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON'):
								iProm = gc.getInfoTypeForString('PROMOTION_SCOURGE')
							elif iReligion == gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE'):
								iProm = gc.getInfoTypeForString('PROMOTION_MAGIC_IMMUNE')
							if iProm != -1:
								newUnit.setHasPromotion(iProm,True)

						if pPlayer.isHuman():
							if iUnit == iManes:
								CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ADD_MANES",()),'AS2D_UNIT_FALLS',1,'Art/Interface/Buttons/Promotions/Demon.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
							elif iUnit == iAngel:
								CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ADD_ANGEL",()),'AS2D_UNIT_FALLS',1,'Art/Interface/Buttons/Promotions/Angel.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
						elif iUnit == iManes and pPlot.isCity():
							pCity = pPlot.getPlotCity()
							if CyGame().getSorenRandNum(100, "Manes") < (100 - (pCity.getPopulation() * 5)):
								if newUnit.canCast(gc.getInfoTypeForString('SPELL_ADD_TO_CITY'), False):
									newUnit.cast(gc.getInfoTypeForString('SPELL_ADD_TO_CITY'))
						if pFromPlot != -1 and iFromPlayer != -1:
							if gc.getPlayer(iFromPlayer).isHuman():
								if iUnit == iManes:
									CyInterface().addMessage(iFromPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_FALLS",()),'AS2D_UNIT_FALLS',1,'Art/Interface/Buttons/Promotions/Demon.dds',ColorTypes(7),pFromPlot.getX(),pFromPlot.getY(),True,True)
								elif iUnit == iAngel:
									CyInterface().addMessage(iFromPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_RISES",()),'AS2D_UNIT_FALLS',1,'Art/Interface/Buttons/Promotions/Angel.dds',ColorTypes(7),pFromPlot.getX(),pFromPlot.getY(),True,True)

	def placeTreasure(self, iPlayer, iUnit):
		pPlayer = gc.getPlayer(iPlayer)
		pBestPlot = -1
		iBestPlot = -1
		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iPlot = -1

			if not pPlot.isWater():
				if pPlot.getNumUnits() == 0:
					if not pPlot.isCity():
						if not pPlot.isImpassable():
							iPlot = CyGame().getSorenRandNum(1000, "Add Unit")
							if pPlot.area().getNumTiles() < 8:
								iPlot += 1000
							if not pPlot.isOwned():
								iPlot += 1000
							if iPlot > iBestPlot:
								iBestPlot = iPlot
								pBestPlot = pPlot
		if iBestPlot != -1:
			newUnit = pPlayer.initUnit(iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_TREASURE",()),'',1,'Art/Interface/Buttons/Equipment/Treasure.dds',ColorTypes(8),newUnit.getX(),newUnit.getY(),True,True)
			CyCamera().JustLookAtPlot(pBestPlot)

	def removeAffinities(self, pCaster, bPreserveSpells=False):
		for sProm in [
						'PROMOTION_CHANNELING1',
						'PROMOTION_CHANNELING2',
						'PROMOTION_CHANNELING3',

						'PROMOTION_MASTERY',
						'PROMOTION_ARCANE',
						'PROMOTION_SUMMONER',
						'PROMOTION_SUNDERED',

						'PROMOTION_AFFINITY_AIR',
						'PROMOTION_AFFINITY_BODY',
						'PROMOTION_AFFINITY_CHAOS',
						'PROMOTION_AFFINITY_CREATION',
						'PROMOTION_AFFINITY_DEATH_ARAWN',
						'PROMOTION_AFFINITY_DEATH',
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
			if iProm > -1:
				if pCaster.isHasPromotion(iProm):
					pCaster.setHasPromotion(iProm, False)
					if bPreserveSpells:
						info = gc.getPromotionInfo(iProm)
						iBonus = info.getBonusPrereq()
						if iBonus != -1:
							if gc.getBonusInfo(iBonus).isMana():

								iSpell2 = info.getPrereqPromotion()#Normal Mage tier spell
								if iSpell2 != -1:
									iMana = gc.getPromotionInfo(iSpell2).getBonusPrereq()
									if iMana != -1:
										pCaster.setHasPromotion(iSpell2, True)
										info = gc.getPromotionInfo(iSpell2)
										iSpell1 = info.getPrereqPromotion()#Normal Mage tier spell
										if iSpell1 != -1:
											iMana = gc.getPromotionInfo(iSpell1).getBonusPrereq()
											if iMana != -1:
												pCaster.setHasPromotion(iSpell1, True)



	def removeReligion(self, iReligion, pCity):
		if pCity.isHolyCityByType(iReligion):
			return False
		pCity.setHasReligion(iReligion, False, True, True)
		for i in xrange(gc.getNumBuildingInfos()):
			if pCity.getNumBuilding(i) > 0:
				info = gc.getBuildingInfo(i)
				if info.getPrereqReligion() == iReligion:
					if not isWorldWonderClass(info.getBuildingClassType()):
						pCity.setNumRealBuilding(i, 0)
		return True

	def restoreTraits(self,pPlayer):
		pLeader = gc.getLeaderHeadInfo(pPlayer.getLeaderType())
		pCivilization = gc.getCivilizationInfo(pPlayer.getCivilizationType())
		iTrait = pCivilization.getCivTrait()
		if iTrait != -1:
			pPlayer.setHasTrait(iTrait, True)
		for iTrait in xrange(gc.getNumTraitInfos()):
			if pLeader.hasTrait(iTrait):
				pPlayer.setHasTrait(iTrait, True)


	def makeMortal(self, pUnit):
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMORTAL'), False)
		while pUnit.isImmortal():
			pUnit.changeImmortal(-1)

	def showUniqueImprovements(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()
		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getImprovementType() != -1:
				iImprovement = gc.getImprovementInfo(pPlot.getImprovementType())
				if iImprovement.isUnique():
					CyEngine().addSign(pPlot,iPlayer, CvUtil.convertToStr(iImprovement.getDescription()))

	def findImprovement(self, iImprovementType):
		for i in xrange (CyMap().getNumAreas()):
			pArea = CyMap().getArea(i)
			if pArea.getNumImprovements(iImprovementType) > 0:
				break
		else:
			return -1

		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getImprovementType() == iImprovementType:
				return pPlot
		return -1


	def findImprovements(self, iImprovementType):
		listImprovements = []
		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getImprovementType() == iImprovementType:
				listImprovements.append(pPlot)
		return listImprovements

	def isHasDragon(self,pPlayer):
		eTeamP = gc.getTeam(pPlayer.getTeam())
		for sDragon in [	'UNITCLASS_EURABATRES',
							'UNITCLASS_DRIFA',
							'UNITCLASS_ACHERON',
							'UNITCLASS_ABASHI',
							'UNITCLASS_THALATTH',
							'UNITCLASS_DRACOLICH',
							'UNITCLASS_DRAGON_BLOOD',
							'UNITCLASS_DRAGON_CORAL',
							'UNITCLASS_DRAGON_DAWN',
							'UNITCLASS_DRAGON_ELDER',
							'UNITCLASS_DRAGON_FANG',
							'UNITCLASS_DRAGON_FEATHERED',
							'UNITCLASS_DRAGON_FURNACE',
							'UNITCLASS_DRAGON_GRAVE',
							'UNITCLASS_DRAGON_GOLD',
							'UNITCLASS_DRAGON_OBSIDIAN',
							'UNITCLASS_DRAGON_PIT',
							'UNITCLASS_DRAGON_RUNE',
							'UNITCLASS_DRAGON_SCALED',
							'UNITCLASS_DRAGON_SEED',
							'UNITCLASS_DRAGON_SHADOW',
							'UNITCLASS_DRAGON_SHIELD',
							'UNITCLASS_DRAGON_SHIMMERING',
							'UNITCLASS_DRAGON_SIEGE',
							'UNITCLASS_DRAGON_SPIRE',
							'UNITCLASS_VAULT_WYRM',
							'UNITCLASS_DRAGON_WINTER']:
			if eTeamP.getUnitClassCount(gc.getInfoTypeForString(sDragon)) > 0:
				return True
		if pPlayer.isBarbarian():
			if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('UNITCLASS_ACHERON'), 0):
				return True
		elif pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
			if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('UNITCLASS_EURABATRES'), 0):
				return True
		elif pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
			if not CyGame().isUnitClassMaxedOut(gc.getInfoTypeForString('UNITCLASS_ABASHI'), 0):
				return True
		return False

	def showMana(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()

		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iBonus = pPlot.getBonusType(-1)
			if iBonus != -1:
				infoB = gc.getBonusInfo(iBonus)
				if infoB.isMana():
					pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
					CyEngine().addSign(pPlot,iPlayer, CvUtil.convertToStr(infoB.getDescription()))
			elif pPlot.isCity():
				pCity = pPlot.getPlotCity()
				for j in xrange(gc.getNumBuildingInfos()):
					if pCity.getNumRealBuilding(j) > 0:
						iBuild = gc.getBuildingInfo(j)
						if not iBuild.isNeverCapture():
							if iBuild.getFreeBonus() != -1:
								iBonus = iBuild.getFreeBonus()
								infoB = gc.getBonusInfo(iBonus)
								if infoB.isMana():
									pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
									CyEngine().addSign(pPlot,iPlayer, CvUtil.convertToStr(infoB.getDescription()))

	def listSummons(self, pUnit, iSummonType = -1):
		summonerID = pUnit.getID()
		pPlayer = gc.getPlayer(pUnit.getOwner())
		lUnit = []
		(loopUnit, iter) = pPlayer.firstUnit(False)
		while(loopUnit):
			if not loopUnit.isDead(): #is the unit alive and valid?
				if loopUnit.getSummoner() == summonerID:#is it a summon of pUnit?
					if iSummonType == -1 or loopUnit.getUnitType() == iSummonType:#is it a specified type of summon?
						lUnit.append(loopUnit) #add unit instance to list
			(loopUnit, iter) = pPlayer.nextUnit(iter, False)
		return lUnit

	def getSummonPerks(self, pSummoner):
		lPerks = []
		for iProm in xrange(gc.getNumPromotionInfos()):
			if pSummoner.isHasPromotion(iProm):
				iPerk = gc.getPromotionInfo(iProm).getPromotionSummonPerk()
				if iPerk != -1:
					lPerks.append(iPerk)
		return lPerks

	def grantSummonPerks(self, pSummon, pSummoner):
		lPerks = self.getSummonPerks(pSummoner)
		for iProm in lPerks:
			pSummon.setHasPromotion(iProm, True)

	def getTeammates(self, pPlayer):
		iTeam = pPlayer.getTeam()
		iNum = gc.getTeam(iTeam).getNumMembers()
		listTeammates = []
		if iNum == 1:
			listTeammates = [pPlayer]
		else:
			iCount = 0
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive():
					if pLoopPlayer.getTeam() == iTeam:
						listTeammates.append(pLoopPlayer)
						iCount +=1
						if iCount == iNum:
							break
		return listTeammates

	def sluagh(self, unit):
		if unit.isMechUnit():
			return
		if unit.getSummoner() != -1:
			return
		if unit.isPermanentSummon():
			return
		if unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'):
			return
		if unit.getRace() in [gc.getInfoTypeForString('PROMOTION_GOLEM'),gc.getInfoTypeForString('PROMOTION_UNDEAD'),gc.getInfoTypeForString('PROMOTION_PUPPET'),gc.getInfoTypeForString('PROMOTION_ELEMENTAL')]:
			return
		iIllusion = gc.getInfoTypeForString('PROMOTION_ILLUSION')
		iReflection = gc.getInfoTypeForString('PROMOTION_DARK_REFLECTION')
		if unit.getRace() in [iIllusion,iReflection]:
			unit.setAvatarOfCivLeader(False)
			self.makeMortal(unit)
			return
		iUnit = unit.getUnitType()
		if iUnit == gc.getInfoTypeForString('UNIT_SEVERED_SOUL'):
			return
		iSluagh = gc.getInfoTypeForString('UNIT_SLUAGH')
		if iUnit == iSluagh:
			return
		iPlayer = unit.getOwner()
		iReligion = unit.getReligion()
		pPlot = unit.plot()
		if pPlot.isCity():
			if iUnit == gc.getInfoTypeForString('UNIT_SETTLER'):
				if iReligion != -1:
					pCity = pPlot.getPlotCity()
					if iPlayer == pCity.getOwner():
						pCity.setHasReligion(iReligion, True, False, False)
		if unit.baseCombatStr() < 1:
			return
		pPlayer = gc.getPlayer(iPlayer)
		if unit.isImmortal() and not pPlayer.getCapitalCity().isNone():
			return
		if pPlot.isOwned():
			if gc.getPlayer(pPlot.getOwner()).countNumBuildings(gc.getInfoTypeForString('BUILDING_SOUL_FORGE')) > 0:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SOUL_FORGED'), True)
			if gc.getPlayer(pPlot.getOwner()).countNumBuildings(gc.getInfoTypeForString('BUILDING_SOUL_SHROUD')) > 0:
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NETHERBIND'), True)
		sUnitName = unit.getNameNoDesc()
		if len(sUnitName) == 0:
			sUnitName = unit.getName()
		iAdventurer = gc.getInfoTypeForString('PROMOTION_ADVENTURER')
		iChangeling = gc.getInfoTypeForString('PROMOTION_CHANGELING')
		iWerewolf = gc.getInfoTypeForString('PROMOTION_WEREWOLF')
		if -1 < unit.getScenarioCounter() < gc.getNumUnitInfos():#Important for Werewolves and Gibbon
			if unit.isHasPromotion(iAdventurer) or unit.isHasPromotion(iChangeling) or unit.isHasPromotion(iWerewolf):
				iUnit = unit.getScenarioCounter()
		unitInfo = gc.getUnitInfo(iUnit)
		if unit.isHasPromotion(iWerewolf):
			if not unitInfo.getFreePromotions(iWerewolf):
				unit.setHasPromotion(iWerewolf, False)
		unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CANNOT_CAST'), False)
		if isWorldUnitClass(unitInfo.getUnitClassType()):
			if unit.getUnitType() == gc.getInfoTypeForString('UNIT_AURIC_ASCENDED'):
				pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_FALLOW'),False)
				iDC = gc.getInfoTypeForString('BUILDING_DEMONIC_CITIZENS')
				for pyCity in PyPlayer(iPlayer).getCityList():
					loopCity = pyCity.GetCy()
					loopCity.setNumRealBuilding(iDC, 0)
				iManes = gc.getInfoTypeForString('UNIT_MANES')
				iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
				for loopUnit in PyPlayer(iPlayer).getUnitList():
					if loopUnit.getUnitType() == iManes:
						self.giftUnit(iManes, iInfernal, loopUnit.getExperience(), loopUnit.plot(), iPlayer,loopUnit.getReligion())
						loopUnit.kill(False, PlayerTypes.NO_PLAYER)
			if unit.getUnitType() == iUnit:
				unitID = unit.getID()
				for i in xrange(pPlot.getNumUnits()):
					pLoopUnit = pPlot.getUnit(i)
					if iPlayer == pLoopUnit.getOwner():
						if not pLoopUnit.isDelayedDeath():
							if pLoopUnit.getScenarioCounter() == iUnit:
								if pLoopUnit.getUnitType() != iUnit:
									if pLoopUnit.getID() != unitID:
										if pLoopUnit.getRace() not in [iIllusion, iReflection]:
											iSluagh = -1
											return
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				if iLoopPlayer != iPlayer:
					for loopUnit in PyPlayer(iPlayer).getUnitList():
						if loopUnit.getUnitType() == iUnit or loopUnit.getScenarioCounter() == iUnit:
							if pLoopUnit.getRace() not in [iIllusion, iReflection]:
								return
		# elif unit.getRace() == gc.getInfoTypeForString('PROMOTION_DRAGON'):#Treating Dragon as a race means a Dracolich can't be both a dragon and undead and that Pit Dragons cannot be dragons and demonic
		elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DRAGON')):
			pass
		elif unit.getRace() in [gc.getInfoTypeForString('PROMOTION_ANGEL'),gc.getInfoTypeForString('PROMOTION_DEMON')]:
			return
		elif unit.isHasPromotion(iChangeling):
			unitID = unit.getID()
			for i in xrange(pPlot.getNumUnits()):
				pLoopUnit = pPlot.getUnit(i)
				if not pLoopUnit.isHasPromotion(iChangeling):
					if pLoopUnit.getID() != unitID:
						if iPlayer == pLoopUnit.getOwner():
							if pLoopUnit.getRace() not in [iIllusion, iReflection]:
								iSluagh = -1
								return
								break
		elif unit.isHasPromotion(iAdventurer):
			for i in xrange(pPlot.getNumUnits()):
				pLoopUnit = pPlot.getUnit(i)
				# if pLoopUnit.isHasPromotion(iAdventurer):continue
				if pLoopUnit.getNameNoDesc() == sUnitName:
					if not pLoopUnit.isDelayedDeath():
						if iPlayer == pLoopUnit.getOwner():
							if pLoopUnit.getRace() not in [iIllusion, iReflection]:
								iSluagh = -1
								return
								break
		elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO')):
			pass
		elif unit.getLevel() > 15:
			pass
		elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_NETHERBIND')):
			pass
		elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CAPTUS_CAVEAE_ANGELORUM')):
			pass
		else:
			iSluagh = -1
			return
		if iSluagh != -1:
##			iX = 0
##			iY = 0
##			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_GRAVEYARD'):
##				iX = pPlot.getX()
##				iY = pPlot.getY()

			iX = pPlot.getX()
			iY = pPlot.getY()
			pPlot2 = self.findClearPlot(-1, pPlot)
			if pPlot2 != -1:
				iX = pPlot2.getX()
				iY = pPlot2.getY()
			else:
				pWell = self.findImprovement(gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL'))
				if pWell != -1:
					iX = pWell.getX()
					iY = pWell.getY()
					
			## if newUnit.getRace() == gc.getInfoTypeForString('PROMOTION_DRAGON'):#Treating Dragon as a race means a Dracolich can't be both a dragon and undead and that Pit Dragons cannot be dragons and demonic
			if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DRAGON')):
				pPlot2 = self.findClearPlotImprovement(pPlot)
				iX = pPlot2.getX()
				iY = pPlot2.getY()
				# newUnit.setXY(pPlot.getX(), pPlot.getY(), False, True, True)
				infoUnit = gc.getUnitInfo(iUnit)
				iBonus = infoUnit.getPrereqAndBonus()
				pPlot2.setBonusType(iBonus)
				pPlot2.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES'))



			bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
			newUnit= bPlayer.initUnit(iSluagh, iX,iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setLevel(unit.getLevel())
			newUnit.setExperience(unit.getExperience(), -1)
			newUnit.setReligion(iReligion)
			newUnit.setScenarioCounter(iUnit)
			newUnit.setName(sUnitName + "'s Sluagh")
			for iCount in xrange(gc.getNumPromotionInfos()):
				if unit.isHasPromotion(iCount) and not gc.getPromotionInfo(iCount).isEquipment():
					newUnit.setHasPromotion(iCount, True)
			if isWorldUnitClass(unitInfo.getUnitClassType()):
				newUnit.setDuration(0)

			# if newUnit.getRace() == gc.getInfoTypeForString('PROMOTION_DRAGON'):#Treating Dragon as a race means a Dracolich can't be both a dragon and undead and that Pit Dragons cannot be dragons and demonic
			# if newUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DRAGON')):
				# pPlot = self.findClearPlotImprovement(pPlot)
				# newUnit.setXY(pPlot.getX(), pPlot.getY(), False, True, True)
				# pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES'))
				# infoUnit = gc.getUnitInfo(iUnit)
				# iBonus = infoUnit.getPrereqAndBonus()
				# pPlot.setBonusType(iBonus)

			if newUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CASSWALLAWN')):
				sName = newUnit.getName()[:newUnit.getName().find(" the Casswallawn")]
				newUnit.setName(sName)
				iGastrius = gc.getInfoTypeForString('UNIT_GASTRIUS')
				infoUnit = gc.getUnitInfo(newUnit.getUnitType())
				infoUnitG = gc.getUnitInfo(iGastrius)

				lChanneling = [gc.getInfoTypeForString('PROMOTION_CASSWALLAWN'), gc.getInfoTypeForString('PROMOTION_CHANNELING1'), gc.getInfoTypeForString('PROMOTION_CHANNELING2'), gc.getInfoTypeForString('PROMOTION_CHANNELING3'), gc.getInfoTypeForString('PROMOTION_CHANNELING4')]

				for iProm in xrange(gc.getNumPromotionInfos()):
					if not infoUnit.getFreePromotions(iProm):
						if infoUnitG.getFreePromotions(iProm):
							newUnit.setHasPromotion(iProm, False)
						else:
							infoProm = gc.getPromotionInfo(iProm)
							iBonus = infoProm.getBonusPrereq()
							if iBonus != -1:
								if gc.getBonusInfo(iBonus).isMana():
									newUnit.setHasPromotion(iProm, False)
									if newUnit.canAcquirePromotion(iProm):
										newUnit.setHasPromotion(iProm, True)

				iX = newUnit.getX()
				iY = newUnit.getY()
				iGastrius = gc.getInfoTypeForString('UNIT_GASTRIUS')
				pCaveOfAncestors = self.findImprovement(gc.getInfoTypeForString('IMPROVEMENT_CAVE_OF_ANCESTORS'))
				if pCaveOfAncestors != -1:
					iX = pCaveOfAncestors.getX()
					iY = pCaveOfAncestors.getY()
					newUnitG = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(gc.getInfoTypeForString('UNIT_SLUAGH'), iX, iY, UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_SOUTH)
					newUnitG.setScenarioCounter(iGastrius)
					infoU = gc.getUnitInfo(iGastrius)
					newUnitG.setName(CyTranslator().getText('TXT_KEY_UNIT_GASTRIUS', ()) +"'s Sluagh")
					for iProm in xrange(gc.getNumPromotionInfos()):
						if infoU.getFreePromotions(iProm):
							newUnit.setHasPromotion(iProm, True)
				else:
					newUnitG = pPlayer.initUnit(iGastrius, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnitG.finishMoves()

		return

	def scavenge(self, pWinner, pLoser, bKill = True):
		iPlayer = pWinner.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iTier = gc.getUnitInfo(pWinner.getUnitType()).getWeaponTier()
		iBronze = gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS')
		iIron = gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
		iMithril = gc.getInfoTypeForString('PROMOTION_MITHRIL_WEAPONS')
		iRust = gc.getInfoTypeForString('PROMOTION_RUSTED')
		iEnchant = gc.getInfoTypeForString('PROMOTION_ENCHANTED_BLADE')
		iPoisonBlade = gc.getInfoTypeForString('PROMOTION_POISONED_BLADE')
		if bKill:
			iX = pLoser.getX()
			iY = pLoser.getY()
			pCity = CyMap().findCity(iX,iY, iPlayer, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, pPlayer.getCity(-1))
			if pCity.isNone():
				pCity = pPlayer.getCapitalCity()
			if not pCity.isNone():
				iDistance = CyMap().calculatePathDistance(pWinner.plot(),pCity.plot())
				if iDistance != -1:
					iBooty = pLoser.getExperience()//(iDistance + 2)
					if iBooty > 0:
						if pLoser.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'):
							if not pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL')) and not pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')):
								pCity.changeFood(iBooty)
								szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_SCAVAGE_FOOD", (iBooty, pCity.getName(),))
								CyInterface().addMessage(iPlayer,True,25,szBuffer,'',1,gc.getUnitInfo(pLoser.getUnitType()).getButton(),ColorTypes(8),iX,iY,True,True)
						elif pCity.isProduction():
							pCity.changeProduction(iBooty)
							szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_SCAVAGE_PRODUCTION", (iBooty, pCity.getName(), pCity.getProductionName()))
							CyInterface().addMessage(iPlayer,True,25,szBuffer,'',1,gc.getUnitInfo(pLoser.getUnitType()).getButton(),ColorTypes(8),iX,iY,True,True)
#I think this may be causing the duplication of equipment, when a dying unit drops the equipment even though it should have been removed here
		if not pLoser.isDelayedDeath():
			for iProm in xrange(gc.getNumPromotionInfos()):
				if gc.getPromotionInfo(iProm).isEquipment():
					if pLoser.isHasPromotion(iProm):
						if not pWinner.isHasPromotion(iProm):
							pLoser.setHasPromotion(iProm, False)
							pWinner.setHasPromotion(iProm, True)

		if pLoser.isHasPromotion(iBronze) == pWinner.isHasPromotion(iBronze) and pLoser.isHasPromotion(iIron) == pWinner.isHasPromotion(iIron) and pLoser.isHasPromotion(iMithril) == pWinner.isHasPromotion(iMithril):
			if pWinner.isHasPromotion(iRust) and not pLoser.isHasPromotion(iRust):
				pWinner.setHasPromotion(iRust, False)
			if pLoser.isHasPromotion(iEnchant) and not pWinner.isHasPromotion(iEnchant):
				pWinner.setHasPromotion(iEnchant, True)
			if pLoser.isHasPromotion(iPoisonBlade) and not pWinner.isHasPromotion(iPoisonBlade):
				pWinner.setHasPromotion(iPoisonBlade, True)
		elif not pWinner.isHasPromotion(iMithril):
			if pLoser.isHasPromotion(iMithril) and iTier >= 3:
				pWinner.setHasPromotion(iMithril, True)
				pWinner.setHasPromotion(iIron, False)
				pWinner.setHasPromotion(iBronze, False)
				pLoser.setHasPromotion(iMithril, False)
				pWinner.setHasPromotion(iRust, pLoser.isHasPromotion(iRust))
				pWinner.setHasPromotion(iEnchant, pLoser.isHasPromotion(iEnchant))
				pWinner.setHasPromotion(iPoisonBlade, pLoser.isHasPromotion(iPoisonBlade))
			elif not pWinner.isHasPromotion(iIron):
				if pLoser.isHasPromotion(iIron) and iTier >= 2:
					pWinner.setHasPromotion(iIron, True)
					pWinner.setHasPromotion(iBronze, False)
					pLoser.setHasPromotion(iIron, False)
					pWinner.setHasPromotion(iRust, pLoser.isHasPromotion(iRust))
					pWinner.setHasPromotion(iEnchant, pLoser.isHasPromotion(iEnchant))
					pWinner.setHasPromotion(iPoisonBlade, pLoser.isHasPromotion(iPoisonBlade))
				elif not pWinner.isHasPromotion(iBronze) and iTier >= 1:
					if pLoser.isHasPromotion(iBronze):
						pWinner.setHasPromotion(iBronze, True)
						pLoser.setHasPromotion(iBronze, False)
						pWinner.setHasPromotion(iRust, pLoser.isHasPromotion(iRust))
						pWinner.setHasPromotion(iEnchant, pLoser.isHasPromotion(iEnchant))
						pWinner.setHasPromotion(iPoisonBlade, pLoser.isHasPromotion(iPoisonBlade))

	# lfgr 03/2021: For spell help texts
	def canStartWar( self, iPlayer, iPlayer2 ) :
		# type: (int, int) -> bool
		iTeam = gc.getPlayer(iPlayer).getTeam()
		iTeam2 = gc.getPlayer(iPlayer2).getTeam()
		pTeam = gc.getTeam(iTeam)
		pTeam2 = gc.getTeam(iTeam2)
		return ( pTeam.isAlive() and pTeam2.isAlive()
				and iTeam != iTeam2 and not pTeam.isAtWar(iTeam2)
				and pTeam.isHasMet(iTeam2) and not pTeam.isPermanentWarPeace(iTeam2) )


	# lfgr 03/2021: refactored
	def startWar(self, iPlayer, iPlayer2, iWarPlan):
		if self.canStartWar( iPlayer, iPlayer2 ) :
			pTeam = gc.getTeam( gc.getPlayer(iPlayer).getTeam() )
			iTeam2 = gc.getPlayer(iPlayer2).getTeam()
			pTeam.declareWar(iTeam2, False, iWarPlan)

	def warScript(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		eTeam = gc.getTeam(pPlayer.getTeam())
		if not eTeam.isAVassal():
			iCiv = pPlayer.getCivilizationType()
			iDoviello = gc.getInfoTypeForString('CIVILIZATION_DOVIELLO')
			iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
			iLjosalfar = gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR')
			iSvartalfar = gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')
			iEvil = gc.getInfoTypeForString('ALIGNMENT_EVIL')
			iMastery = gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_MASTERY')
			iAltarDivine = gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_DIVINE')
			iAltarExalted = gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_EXALTED')
			iAltarFinal = gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_FINAL')

			iCrucible = gc.getInfoTypeForString('BUILDING_CRUCIBLE')
			iArcane = gc.getInfoTypeForString('TRAIT_ARCANE')
			iSummoner = gc.getInfoTypeForString('TRAIT_SUMMONER')
			iVictoryMastery = gc.getInfoTypeForString('VICTORY_TOWER_OF_MASTERY')
			bVictoryMaster = gc.getGame().isVictoryValid(iVictoryMastery)
			iVictoryAltar = gc.getInfoTypeForString('VICTORY_ALTAR_OF_THE_LUONNOTAR')
			bVictoryAltar = gc.getGame().isVictoryValid(iVictoryAltar)
 
 
			iEnemy = -1
			for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
				pPlayer2 = gc.getPlayer(iPlayer2)
				if pPlayer2.isAlive():
					iTeam2 = pPlayer2.getTeam()
					if eTeam.isAtWar(iTeam2):
						if CyGame().getSorenRandNum(100, "War Script") < 5:
							self.dogpile(iPlayer, iPlayer2)
					if self.warScriptAllow(iPlayer, iPlayer2):

						if pPlayer2.getBuildingClassMaking(iCrucible) > 0:
							if eTeam.getAtWarCount(True) == 0:
								self.startWar(iPlayer, iPlayer2, WarPlanTypes.WARPLAN_TOTAL)
								
						if bVictoryAltar:
							if pPlayer2.getBuildingClassMaking(iAltarFinal) > 0:
								if eTeam.getAtWarCount(True) == 0:
									self.startWar(iPlayer, iPlayer2, WarPlanTypes.WARPLAN_TOTAL)
									
						if bVictoryMaster:
							if pPlayer2.getBuildingClassMaking(iMastery) > 0:
								if eTeam.getAtWarCount(True) == 0:
									self.startWar(iPlayer, iPlayer2, WarPlanTypes.WARPLAN_TOTAL)
									
						iCiv2 = pPlayer2.getCivilizationType()
						if CyGame().getGlobalCounter() > 20:
							if (iCiv == iSvartalfar and iCiv2 == iLjosalfar) or (iCiv2 == iSvartalfar and iCiv == iLjosalfar):
								if CyGame().getPlayerRank(iPlayer) > CyGame().getPlayerRank(iPlayer2):
									self.startWar(iPlayer, iPlayer2, WarPlanTypes.WARPLAN_TOTAL)
						if pPlayer.getAlignment() == iEvil:
							if CyGame().getGlobalCounter() > 40 or iCiv in [iInfernal, iDoviello]:
								if eTeam.getAtWarCount(True) == 0 and CyGame().getPlayerRank(iPlayer2) > CyGame().getPlayerRank(iPlayer):
									if iEnemy == -1 or CyGame().getPlayerRank(iPlayer2) > CyGame().getPlayerRank(iEnemy):
										iEnemy = iPlayer2
							if pPlayer2.getNumBuilding(iAltarDivine) > 0 or pPlayer2.getNumBuilding(iAltarExalted) > 0:
								if eTeam.getAtWarCount(True) == 0:
									self.startWar(iPlayer, iPlayer2, WarPlanTypes.WARPLAN_TOTAL)
			if iEnemy != -1:
				if CyGame().getPlayerRank(iPlayer) > CyGame().getPlayerRank(iEnemy):
					self.startWar(iPlayer, iEnemy, WarPlanTypes.WARPLAN_LIMITED)

	def warScriptAllow(self, iPlayer, iPlayer2):
		if iPlayer == gc.getBARBARIAN_PLAYER():
			return False
		pPlayer = gc.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()
		eTeam = gc.getTeam(iTeam)
		pPlayer2 = gc.getPlayer(iPlayer2)
		iTeam2 = pPlayer2.getTeam()
		if not eTeam.isHasMet(iTeam2):
			return False
		if eTeam.AI_getAtPeaceCounter(iTeam2) < 20:
			return False
#		if pPlayer.AI_getAttitude(iPlayer2) <= gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getDeclareWarRefuseAttitudeThreshold():
#			return False
		if eTeam.isAtWar(iTeam2):
			return False
		if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
			if pPlayer2.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				return False
		return True

	def dogpile(self, iPlayer, iVictim):
		pPlayer = gc.getPlayer(iPlayer)
		iBal = gc.getInfoTypeForString('CIVILIZATION_BALSERAPHS')
		for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
			pPlayer2 = gc.getPlayer(iPlayer2)
			iChance = -1
			if pPlayer2.isAlive():
				if self.dogPileAllow(iPlayer, iPlayer2) and self.warScriptAllow(iPlayer2, iVictim):
					iChance = pPlayer2.AI_getAttitude(iPlayer) * 5
					if iChance > 0:
						iChance -= (pPlayer2.AI_getAttitude(iVictim) * 10) - 20
						if not CyGame().isOption(gc.getInfoTypeForString('GAMEOPTION_AGGRESSIVE_AI')):
							iChance -= 100
						if iChance > 0:
							iChance += (CyGame().getGlobalCounter() / 4)
							if pPlayer2.getCivilizationType() == iBal:
								iChance = CyGame().getSorenRandNum(50, "Dogpile")
							if CyGame().getSorenRandNum(100, "Dogpile") < iChance:
								self.startWar(iPlayer2, iVictim, WarPlanTypes.WARPLAN_DOGPILE)

	def dogPileAllow(self, iPlayer, iPlayer2):
		pPlayer = gc.getPlayer(iPlayer)
		pPlayer2 = gc.getPlayer(iPlayer2)
		if pPlayer2.isHuman():
			return False
		if iPlayer == iPlayer2:
			return False
		iTeam = gc.getPlayer(iPlayer).getTeam()
		iTeam2 = gc.getPlayer(iPlayer2).getTeam()
		if iTeam == iTeam2:
			return False
		if pPlayer2.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
			return False
		if pPlayer2.getStateReligion() == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS'):
			return False
		if gc.getTeam(iTeam2).isAVassal():
			return False
		return True

	def warn(self, iPlayer, szText, pPlot):
		pPlayer = gc.getPlayer(iPlayer)
		for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
			pPlayer2 = gc.getPlayer(iPlayer2)
			if pPlayer2.isAlive() and iPlayer != iPlayer2:
				if pPlayer2.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
					popupInfo.setText(szText)
					popupInfo.setOnClickedPythonCallback("selectWarn")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_MAIN_MENU_OK",()), "")
					popupInfo.addPopup(iPlayer2)
				if pPlot != -1:
					CyInterface().addMessage(iPlayer2,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ALTAR_OF_THE_LUONNOTAR",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/Buildings/AltaroftheLuonnotar.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)

	def MarnokNameGenerator(self, unit):
		pPlayer = gc.getPlayer(unit.getOwner())
		pCiv = pPlayer.getCivilizationType()
		iReligion = unit.getReligion()
		if iReligion == -1:
			iReligion = pPlayer.getStateReligion()
		iAlign = pPlayer.getAlignment()

		iUnitType = unit.getUnitType()
		iAlternateType = unit.getScenarioCounter()
		if -1 < iAlternateType < gc.getNumUnitInfos():
			iUnitType = iAlternateType

		lPre=["ta","go","da","bar","arc","ken","an","ad","mi","kon","kar","mar","wal","he", "ha", "re", "ar", "bal", "bel", "bo", "bri", "car","dag","dan","ma","ja","co","be","ga","qui","sa"]
		lMid=["ad","z","the","and","tha","ent","ion","tio","for","tis","oft","che","gan","an","en","wen","on","d","n","g","t","ow","dal"]
		lEnd=["ar","sta","na","is","el","es","ie","us","un","th", "er","on","an","re","in","ed","nd","at","en","le","man","ck","ton","nok","git","us","or","a","da","u","cha","ir"]

		lEpithet=["red","blue","black","grey","white","strong","brave","old","young","great","slayer","hunter","seeker"]
		lNoun=["spirit","soul","boon","born","staff","rod","shield","autumn","winter","spring","summer","wit","horn","tusk","glory","claw","tooth","head","heart", "blood","breath", "blade", "hand", "lover","bringer","maker","taker","river","stream","moon","star","face","foot","half","one","hundred","thousand"]
		lSchema=["CPME","CPMESCPME","CPESCPE","CPE","CPMME","CPMDCME","CPMAME","KCPMESCUM","CPMME[ the ]CX", "CPMESCXN", "CPMME[ of ]CPMME", "CNNSCXN"]

		if iAlign == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
			lNoun += ["fear","terror","reign","brood","snare","war","strife","pain","hate","evil","hell","misery","murder","anger","fury","rage","spawn","sly","blood","bone","scythe","slave","bound","ooze","scum"]
			lEpithet = ["dark","black","white","cruel","foul"]
		if iReligion != -1:
			if iReligion == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				lEpithet += ["fallen","diseased","infernal","profane","corrupt"]
				lSchema += ["CPME[ the ]CX"]
			elif iReligion == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
				lEpithet += ["hidden","dark"]
				lNoun += ["cloak","shadow","mask"]
				lSchema += ["CPME","CPMME"]
			elif iReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
				lPre += ["cth","cht","shu","az","ts","dag","hy","gla","gh","rh","x","ll"]
				lMid += ["ul","tha","on","ug","st","oi"]
				lEnd += ["hu","on", "ha","ua","oa","uth","oth","ath","thua", "thoa","ur","ll","og","hua"]
				lEpithet += ["nameless","webbed","deep","watery"]
				lNoun += ["tentacle","wind","wave","sea","ocean","dark","crab","abyss","island"]
				lSchema += ["CPMME","CPDMME","CPAMAME","CPMAME","CPAMAMEDCPAMAE"]
			elif iReligion == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
				lPre += ["ki","ky","yv"]
				lMid += ["th","ri"]
				lEnd += ["ra","el","ain"]
				lEpithet += ["green"]
				lNoun += ["tree","bush","wood","berry","elm","willow","oak","leaf","flower","blossom"]
				lSchema += ["CPESCN","CPMESCNN","CPMESCXN"]
			elif iReligion == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
				lPre += ["bam","ar","khel","ki"]
				lMid += ["th","b","en"]
				lEnd += ["ur","dain","ain","don"]
				lEpithet += ["deep","guard","miner"]
				lNoun += ["rune","flint","slate","stone","rock","iron","copper","mithril","thane","umber"]
				lSchema += ["CPME","CPMME"]
			elif iReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
				lEpithet += ["radiant","holy"]
				lNoun += ["honor"]
			elif iReligion == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
				lPre += ["ph","v","j"]
				lMid += ["an","al","un"]
				lEnd += ["uel","in","il"]
				lEpithet += ["confessor","crusader", "faithful","obedient","good"]
				lNoun += ["order", "faith", "heaven","law"]
				lSchema += ["CPESCPME","CPMESCPE","CPMESCPME", "CPESCPE"]
			elif iReligion == gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE'):
				lEpithet += ["Elder","Wise"]

		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_COURAGE')):
			lEpithet += ["Brave"]
		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VALOR')):
			lEpithet += ["Brave","Valiant"]
		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF')):
			lEpithet += ["Delver"]
			lSchema += ["CPME[ the ]CX"]

		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENRAGED')):
			# I have left this as a copy of the Barbarian, see how it goes, this might do the trick. I plan to use it when there is a chance a unit will go Barbarian anyway.
			lPre += ["gru","bra","no","os","dir","ka","z"]
			lMid += ["g","ck","gg","sh","b","bh","aa"]
			lEnd += ["al","e","ek","esh","ol","olg","alg"]
			lNoun += ["death", "hate", "rage", "mad","insane","berserk"]
			lEpithet += ["smasher", "breaker", "mangle","monger"]

		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED')):
			# might want to tone this down, because I plan to use it as possession/driven to madness, less than madcap zaniness.
			lPre += ["mad","pim","zi","zo","fli","mum","dum","odd","slur"]
			lMid += ["bl","pl","gg","ug","bl","b","zz","abb","odd"]
			lEnd += ["ad","ap","izzle","onk","ing","er","po","eep","oggle","y"]

		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRE')):
			lPre += ["dra","al","nos","vam","vla","tep","bat","bar","cor","lil","ray","zar","stra","le"]
			lMid += ["cul","u","car","fer","pir","or","na","ov","sta"]
			lEnd += ["a","d","u","e","es","y","bas","vin","ith","ne","ak","ich","hd","t"]

		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON')):
			lPre += ["aa","ab","adr","ah","al","de","ba","cro","da","be","eu","el","ha","ib","me","she","sth","z"]
			lMid += ["rax","lia","ri","al","as","b","bh","aa","al","ze","phi","sto","phe","cc","ee"]
			lEnd += ["tor","tan","ept","lu","res","ah","mon","gon","bul","gul","lis","les","uz"]
			lSchema = ["CPMMME","CPMACME", "CPKMAUAPUE", "CPMMME[ the ]CNX"]

		if iUnitType == gc.getInfoTypeForString('UNIT_HILL_GIANT'):
			lPre += ["gor","gra","gar","gi","gol"]
			lMid += ["gan","li","ri","go"]
			lEnd += ["tus","tan","ath","tha"]
			lSchema +=["CXNSCNN","CPESCNE", "CPMME[ the ]CX"]
			lEpithet += ["large","huge","collossal","brutal","basher","smasher","crasher","crusher"]
			lNoun += ["fist","tor","hill","brute","stomp"]

		elif iUnitType == gc.getInfoTypeForString('UNIT_LIZARDMAN'):
			lPre += ["ss","s","th","sth","hss"]
			lEnd += ["ess","iss","ath","tha"]
			lEpithet += ["cold"]
			lNoun += ["hiss","tongue","slither","scale","tail","ruin"]
			lSchema += ["CPAECPAE","CPAKECPAU","CPAMMAE"]
		elif iUnitType == gc.getInfoTypeForString('UNIT_FIRE_ELEMENTAL') or unit.getUnitType() == gc.getInfoTypeForString('UNIT_AZER'):
			lPre += ["ss","cra","th","sth","hss","roa"]
			lMid += ["ss","ck","rr","oa","iss","tt"]
			lEnd += ["le","iss","st","r","er"]
			lNoun += ["hot", "burn","scald","roast","flame","scorch","char","sear","singe","fire","spit"]
			lSchema = ["CNN","CNX","CPME","CPME[ the ]CNX","CPMME","CNNSCPME"]
		elif iUnitType == gc.getInfoTypeForString('UNIT_WATER_ELEMENTAL'):
			lPre += ["who","spl","dr","sl","spr","sw","b"]
			lMid += ["o","a","i","ub","ib"]
			lEnd += ["sh","p","ter","ble"]
			lNoun += ["wave","lap","sea","lake","water","tide","surf","spray","wet","damp","soak","gurgle","bubble"]
			lSchema = ["CNN","CNX","CPME","CPME[ the ]CNX","CPMME","CNNSCPME"]
		elif iUnitType == gc.getInfoTypeForString('UNIT_AIR_ELEMENTAL'):
			lPre += ["ff","ph","th","ff","ph","th"]
			lMid += ["oo","aa","ee","ah","oh"]
			lEnd += ["ff","ph","th","ff","ph","th"]
			lNoun += ["wind","air","zephyr","breeze","gust","blast","blow"]
			lSchema = ["CNN","CNX","CPME","CPME[ the ]CNX","CPMME","CNNSCPME"]
		elif iUnitType == gc.getInfoTypeForString('UNIT_EARTH_ELEMENTAL'):
			lPre += ["gra","gro","kro","ff","ph","th"]
			lMid += ["o","a","u"]
			lEnd += ["ck","g","k"]
			lNoun += ["rock","stone","boulder","slate","granite","rumble","quake"]
			lSchema = ["CNN","CNX","CPME","CPME[ the ]CNX","CPMME","CNNSCPME"]

		# SEA BASED
		# Check for ships - special schemas
		if unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_NAVAL'):
			lEnd += ["ton","town","port"]
			lNoun += ["lady","jolly","keel","bow","stern", "mast","sail","deck","hull","reef","wave"]
			lEpithet += ["sea", "red", "blue","grand","barnacle","gull"]
			lSchema = ["[The ]CNN", "[The ]CXN", "[The ]CNX","[The ]CNSCN", "[The ]CNSCX","CPME['s ]CN","[The ]CPME", "[The ]CNX","CNX","CN['s ]CN"]

		# # #
		# Pick a Schema
		sSchema = lSchema.pop(CyGame().getSorenRandNum(len(lSchema), "Name Gen"))
		sFull = ""
		sKeep = ""
		iUpper = 0
		iKeep = 0
		iSkip = 0

		# Run through each character in schema to generate name
		for iCount in xrange (0,len(sSchema)):
			sAdd=""
			iDone = 0
			sAction = sSchema[iCount]
			if iSkip == 1:
				if sAction == "]":
					iSkip = 0
				else:
					sAdd = sAction
					iDone = 1
			else:					# MAIN SECTION
				if sAction == "P":	# Pre	: beginnings of names
					sAdd = lPre.pop(CyGame().getSorenRandNum(len(lPre), "Name Gen"))
					iDone = 1
				elif sAction == "M":	# Mid	: middle syllables
					sAdd = lMid.pop(CyGame().getSorenRandNum(len(lMid), "Name Gen"))
					iDone = 1
				elif sAction == "E":	# End	: end of names
					sAdd = lEnd.pop(CyGame().getSorenRandNum(len(lEnd), "Name Gen"))
					iDone = 1
				elif sAction == "X":	# Epithet	: epithet word part
					#epithets ("e" was taken!)
					sAdd = lEpithet.pop(CyGame().getSorenRandNum(len(lEpithet), "Name Gen"))
					iDone = 1
				elif sAction == "N":	# Noun	: noun word part
					#noun
					sAdd = lNoun.pop(CyGame().getSorenRandNum(len(lNoun), "Name Gen"))
					iDone = 1
				elif sAction == "S":	# Space	: a space character. (Introduced before [ ] was possible )
					sAdd = " "
					iDone = 1
				elif sAction == "D":	# Dash	: a - character. Thought to be common and useful enough to warrant inclusion : Introduced before [-] was possible
					sAdd = "-"
					iDone = 1
				elif sAction == "A":	# '		: a ' character - as for -, introduced early
					sAdd = "'"
					iDone = 1
				elif sAction == "C":	# Caps	: capitalizes first letter of next phrase generated. No effect on non-letters.
					iUpper = 1
				elif sAction == "K":	# Keep	: stores the next phrase generated for re-use with U
					iKeep = 1
				elif sAction == "U":	# Use	: re-uses a stored phrase.
					sAdd = sKeep
					iDone = 1
				elif sAction == "[":	# Print	: anything between [] is added to the final phrase "as is". Useful for [ the ] and [ of ] among others.
					iSkip = 1
			# capitalizes phrase once.
			if iUpper == 1 and iDone == 1:
				sAdd = sAdd.capitalize()
				iUpper = 0
			# stores the next phrase generated.
			if iKeep == 1 and iDone == 1:
				sKeep = sAdd
				iKeep = 0
			# only adds the phrase if a new bit was actally created.
			if iDone == 1:
				sFull += sAdd

		# trim name length
		if len(sFull) > 25:
			sFull = sFull[:25]
		#CyInterface().addMessage(pCaster.getOwner(),True,25,"NAME : "+sFull,'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Spells/Rob Grave.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)

		return sFull





