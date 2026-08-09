# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005

#
# Sevopedia 2.3
#   sevotastic.blogspot.com
#   sevotastic@yahoo.com
#
# additional work by Gaurav, Progor, Ket, Vovan, Fitchn, LunarMongoose, lfgr
# see ReadMe for details
#

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import SevoScreenEnums
import string

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaReligion:

	def __init__(self, main):
		self.iReligion = -1
		self.top = main


	def initPositions( self ) :
##--------	BUGFfH: Modified by Denev 2009/10/08
		"""
		self.X_MAIN_PANE = self.top.X_PEDIA_PAGE
		self.Y_MAIN_PANE = self.top.Y_PEDIA_PAGE
		self.W_MAIN_PANE = 200

		self.X_REQUIRES = self.X_MAIN_PANE + self.W_MAIN_PANE + 10
		self.Y_REQUIRES = self.Y_MAIN_PANE
		self.W_REQUIRES = self.top.R_PEDIA_PAGE - self.X_REQUIRES
		self.H_REQUIRES = 110

		self.X_SPECIAL = self.X_MAIN_PANE + self.W_MAIN_PANE + 10
		self.Y_SPECIAL = self.Y_REQUIRES + self.H_REQUIRES + 10
		self.W_SPECIAL = self.top.R_PEDIA_PAGE - self.X_SPECIAL
		self.H_SPECIAL = 150

		self.H_MAIN_PANE = self.Y_SPECIAL + self.H_SPECIAL - self.Y_MAIN_PANE

		self.W_ICON = 150
		self.H_ICON = 150
		self.X_ICON = self.X_MAIN_PANE + (self.W_MAIN_PANE - self.W_ICON) / 2
		self.Y_ICON = self.Y_MAIN_PANE + (self.H_MAIN_PANE - self.H_ICON) / 2
		self.ICON_SIZE = 64

		self.X_TEXT = self.X_MAIN_PANE
		self.Y_TEXT = self.Y_SPECIAL + self.H_SPECIAL + 10
		self.W_TEXT = self.top.R_PEDIA_PAGE - self.X_TEXT
		self.H_TEXT = self.top.B_PEDIA_PAGE - self.Y_TEXT
		"""
		X_MERGIN = self.top.X_MERGIN
		Y_MERGIN = self.top.Y_MERGIN

		self.X_MAIN_PANE = self.top.X_PEDIA_PAGE
		self.Y_MAIN_PANE = self.top.Y_PEDIA_PAGE
		self.W_MAIN_PANE = 200
		self.H_MAIN_PANE = 116

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_MAIN_PANE + (self.W_MAIN_PANE - self.W_ICON) / 2
		self.Y_ICON = self.Y_MAIN_PANE + (self.H_MAIN_PANE - self.H_ICON) / 2
		self.ICON_SIZE = 64

		self.X_REQUIRES = self.X_MAIN_PANE
		self.Y_REQUIRES = self.Y_MAIN_PANE + self.H_MAIN_PANE + Y_MERGIN
		self.W_REQUIRES = self.W_MAIN_PANE
		self.H_REQUIRES = 110

		self.X_SPECIAL = self.X_MAIN_PANE + self.W_MAIN_PANE + X_MERGIN
		self.Y_SPECIAL = self.Y_MAIN_PANE - 10
		self.W_SPECIAL = self.top.R_PEDIA_PAGE - self.X_SPECIAL
		self.H_SPECIAL = self.Y_REQUIRES + self.H_REQUIRES - self.Y_SPECIAL

		self.X_UNITS = self.X_REQUIRES
		self.Y_UNITS = self.Y_REQUIRES + self.H_REQUIRES + Y_MERGIN
		self.W_UNITS = self.top.W_PEDIA_PAGE
		self.H_UNITS = 110

		self.X_OTHERS = self.X_UNITS
		self.Y_OTHERS = self.Y_UNITS + self.H_UNITS + Y_MERGIN
		self.W_OTHERS = (self.top.W_PEDIA_PAGE - X_MERGIN) / 2
		self.H_OTHERS = 110

		self.X_NO_STATE = self.X_OTHERS + self.W_OTHERS + X_MERGIN
		self.Y_NO_STATE = self.Y_OTHERS
		self.W_NO_STATE = self.top.R_PEDIA_PAGE - self.X_NO_STATE
		self.H_NO_STATE = self.H_OTHERS

		self.X_TEXT = self.X_OTHERS
		self.Y_TEXT = self.Y_OTHERS + self.H_OTHERS + Y_MERGIN
		self.W_TEXT = self.top.W_PEDIA_PAGE
		self.H_TEXT = self.top.B_PEDIA_PAGE - self.Y_TEXT
##--------	BUGFfH: End Modify



	def interfaceScreen(self, iReligion):
		self.initPositions()

		self.iReligion = iReligion
		screen = self.top.getScreen()

##--------	BUGFfH: Added by Denev 2009/08/16
		# Header...
		szHeader = u"<font=4b>" + gc.getReligionInfo(self.iReligion).getDescription() + u"</font>"
		szHeaderId = "PediaMainHeader"
		screen.setText(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
##--------	BUGFfH: End Add

		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.X_MAIN_PANE, self.Y_MAIN_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getReligionInfo(self.iReligion).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placeSpecial()
		self.placeRequires()
		self.placeText()
##--------	BUGFfH: Added by Denev 2009/09/30
		self.placeUnits()
		self.placeOthers()
		self.placeNoStates()

	def placeUnits(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_UNITS_ENABLED", ()), "", false, true, self.X_UNITS, self.Y_UNITS, self.W_UNITS, self.H_UNITS, PanelStyles.PANEL_STYLE_BLUE50 )

		screen.attachLabel(panelName, "", "  ")

		liUnit = []
		for iLoopUnit in range(gc.getNumUnitInfos()):
			if gc.getUnitInfo(iLoopUnit).getStateReligion() == self.iReligion:
				bHero = isWorldUnitClass(gc.getUnitInfo(iLoopUnit).getUnitClassType())
				liUnit.append((bHero, iLoopUnit))
		liUnit.sort(reverse=true)

		bPreviousType = None
		for bHero, iUnit in liUnit:
			if bPreviousType not in (bHero, None):
				screen.attachLabel(panelName, "", " <font=4>/</font> ")
			szButton = gc.getUnitInfo(iUnit).getButton()
			if self.top.iActivePlayer != PlayerTypes.NO_PLAYER:
				szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(iUnit)
			screen.attachImageButton( panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False )
			bPreviousType = bHero

	def placeOthers(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_OTHERS_ENABLED", ()), "", false, true, self.X_OTHERS, self.Y_OTHERS, self.W_OTHERS, self.H_OTHERS, PanelStyles.PANEL_STYLE_BLUE50 )

		screen.attachLabel(panelName, "", "  ")

		for iLoopTech in range(gc.getNumTechInfos()):
			if gc.getTechInfo(iLoopTech).getPrereqReligion() == self.iReligion:
				screen.attachImageButton( panelName, "", gc.getTechInfo(iLoopTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech, 1, False )

		for iLoopBuilding in range(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(iLoopBuilding).getStateReligion() == self.iReligion:
				screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		for iLoopCivic in range(gc.getNumCivicInfos()):
			if gc.getCivicInfo(iLoopCivic).getPrereqReligion() == self.iReligion:
				screen.attachImageButton( panelName, "", gc.getCivicInfo(iLoopCivic).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iLoopCivic, 1, False )

		for iLoopFeature in range(gc.getNumFeatureInfos()):
			if gc.getFeatureInfo(iLoopFeature).getPrereqStateReligion() == self.iReligion:
				screen.attachImageButton( panelName, "", gc.getFeatureInfo(iLoopFeature).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, iLoopFeature, 1, False )

		for iLoopSpell in range(gc.getNumSpellInfos()):
			if gc.getSpellInfo(iLoopSpell).getStateReligionPrereq() == self.iReligion:
				screen.attachImageButton( panelName, "", gc.getSpellInfo(iLoopSpell).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPELL, iLoopSpell, 1, False )

		for iLoopPromotion in range(gc.getNumPromotionInfos()):
			if gc.getPromotionInfo(iLoopPromotion).getStateReligionPrereq() == self.iReligion:
				screen.attachImageButton( panelName, "", gc.getPromotionInfo(iLoopPromotion).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iLoopPromotion, 1, False )

	def placeNoStates(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_ENABLED_WITHOUT_STATE", ()), "", false, true, self.X_NO_STATE, self.Y_NO_STATE, self.W_NO_STATE, self.H_NO_STATE, PanelStyles.PANEL_STYLE_BLUE50 )

		screen.attachLabel(panelName, "", "  ")

		for iLoopUnit in range(gc.getNumUnitInfos()):
			if gc.getUnitInfo(iLoopUnit).getPrereqReligion() == self.iReligion\
			and gc.getUnitInfo(iLoopUnit).getStateReligion() == ReligionTypes.NO_RELIGION:
				szButton = gc.getUnitInfo(iLoopUnit).getButton()
				if self.top.iActivePlayer != PlayerTypes.NO_PLAYER:
					szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(iLoopUnit)
				screen.attachImageButton( panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iLoopUnit, 1, False )

		for iLoopBuilding in range(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(iLoopBuilding).getPrereqReligion() == self.iReligion\
			and gc.getBuildingInfo(iLoopBuilding).getStateReligion() == ReligionTypes.NO_RELIGION:
				screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		for iLoopSpell in range(gc.getNumSpellInfos()):
			if gc.getSpellInfo(iLoopSpell).getReligionPrereq() == self.iReligion\
			and gc.getSpellInfo(iLoopSpell).getStateReligionPrereq() == ReligionTypes.NO_RELIGION:
				screen.attachImageButton( panelName, "", gc.getSpellInfo(iLoopSpell).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPELL, iLoopSpell, 1, False )
##--------	BUGFfH: End Add



	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
##--------	BUGFfH: Modified by Denev 2009/10/07
#		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_FOUNDED_BY_FIRST", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
##--------	BUGFfH: End Modify
		screen.attachLabel(panelName, "", "  ")
		iTech = gc.getReligionInfo(self.iReligion).getTechPrereq()

		if iTech > -1 and iTech < gc.getNumTechInfos() and iTech != gc.getInfoTypeForString('TECH_NEVER'):
			screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_BROTHERHOOD_OF_WARDENS') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_SHRINE_OF_SIRONA')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_HOUSE_OF_PLENTY') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_MUSEUM_OF_MAPONOS')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_RINGGIVER') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_GUILD_OF_HAMMERS')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_UNBLEMISHED') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_AQUAE_SUCELLUS')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_ETERNAL_CABAL') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_TOMB_OF_ARAWN')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_FOXMEN') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_SLYPH_SEARCH')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_CHILDREN_OF_THE_ONE') :
			iLoopUnit = gc.getInfoTypeForString('UNIT_LUONNOTAR')
			screen.attachImageButton( panelName, "", gc.getUnitInfo(iLoopUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iLoopUnit, 1, False )

			iLoopBuilding = gc.getInfoTypeForString('BUILDING_UNHARMED_MARTYRS')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_GREY_COUNCIL') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_TEMPORENCE')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_LAERAN_CORD') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_GREAT_LIBRARY')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_WHITE_HAND') :
			iLoopProject = gc.getInfoTypeForString('PROJECT_THE_WHITE_HAND')
			screen.attachImageButton( panelName, "", gc.getProjectInfo(iLoopProject).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, iLoopProject, 1, False )

			iLoopBuilding = gc.getInfoTypeForString('BUILDING_NEW_MULYR')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_STEWARDS_OF_INEQUITY') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_BAZAAR_OF_MAMMON')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_SONS_OF_DISCORD') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_SANGUINE_FOUNTAIN')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_ANOINTED') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_SCHOOL_OF_SADISM')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

			iLoopSpell= gc.getInfoTypeForString('SPELL_SPREAD_THE_ANOINTED')
			screen.attachImageButton( panelName, "", gc.getSpellInfo(iLoopSpell).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPELL, iLoopSpell, 1, False )


		if self.iReligion == gc.getInfoTypeForString('RELIGION_EMBER_LEGION') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_ETERNAL_FLAME')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_COVEN') :
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_PROPHECY_OF_RAGNAROK')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_CULT_OF_THE_DRAGON') :
			iLoopProject = gc.getInfoTypeForString('PROJECT_STIR_FROM_SLUMBER')
			screen.attachImageButton( panelName, "", gc.getProjectInfo(iLoopProject).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, iLoopProject, 1, False )

			iLoopBuilding = gc.getInfoTypeForString('BUILDING_WYRMHOLD')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )

		if self.iReligion == gc.getInfoTypeForString('RELIGION_MATRONAE') :
			iLoopProject = gc.getInfoTypeForString('PROJECT_BANE_DIVINE')
			screen.attachImageButton( panelName, "", gc.getProjectInfo(iLoopProject).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, iLoopProject, 1, False )

			iLoopSpell= gc.getInfoTypeForString('SPELL_RETRIEVE_CORUNDUM_ARDENS')
			screen.attachImageButton( panelName, "", gc.getSpellInfo(iLoopSpell).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPELL, iLoopSpell, 1, False )
			iLoopSpell= gc.getInfoTypeForString('SPELL_RETRIEVE_OPALUM_MORTIS')
			screen.attachImageButton( panelName, "", gc.getSpellInfo(iLoopSpell).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPELL, iLoopSpell, 1, False )
			iLoopSpell= gc.getInfoTypeForString('SPELL_RETRIEVE_BERYLLUM_ABYSSI')
			screen.attachImageButton( panelName, "", gc.getSpellInfo(iLoopSpell).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPELL, iLoopSpell, 1, False )

			iLoopBuilding = gc.getInfoTypeForString('BUILDING_FANE_OF_FATE')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_DOCKS_OF_DREAMS')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_FOUNDRY_OF_VENGEANCE')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )
			iLoopBuilding = gc.getInfoTypeForString('BUILDING_CATHEDRAL_OF_VIGILANCE')
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iLoopBuilding, 1, False )



	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_EFFECTS", ()), "", True, False, self.X_SPECIAL, self.Y_SPECIAL, self.W_SPECIAL, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		listName = self.top.getNextWidgetName()
		screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(listName, False)
		szSpecialText = CyGameTextMgr().parseReligionInfo(self.iReligion, True)
##--------	BUGFfH: Modified by Denev 2009/10/08
		"""
		splitText = string.split( szSpecialText, "\n" )
		for special in splitText:
			if len( special ) != 0:
				screen.appendListBoxString( listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		"""
		szSpecialText = szSpecialText.strip("\n")	#Trim empty line
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL + 5, self.Y_SPECIAL + 30, self.W_SPECIAL - 5, self.H_SPECIAL - 32, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
##--------	BUGFfH: End Modify



	def placeText(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", True, True, self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = gc.getReligionInfo(self.iReligion).getCivilopedia()
		screen.attachMultilineText( panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
