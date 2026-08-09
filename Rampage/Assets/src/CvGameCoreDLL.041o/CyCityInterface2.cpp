#include "CvGameCoreDLL.h"
#include "CyCity.h"
#include "CyPlot.h"
#include "CyArea.h"
#include "CvInfos.h"

//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>

//
// published python interface for CyCity
//

void CyCityPythonInterface2(python::class_<CyCity>& x)
{
	OutputDebugString("Python Extension Module - CyCityPythonInterface2\n");

	x
		.def("getOccupationTimer", &CyCity::getOccupationTimer, "int () - total # of turns remaining on occupation timer")
		.def("isOccupation", &CyCity::isOccupation, "bool () - is the city under occupation?")
		.def("setOccupationTimer", &CyCity::setOccupationTimer, "void (iNewValue) - set the Occupation Timer to iNewValue")
		.def("changeOccupationTimer", &CyCity::changeOccupationTimer, "void (iChange) - adjusts the Occupation Timer by iChange")
		.def("getCultureUpdateTimer", &CyCity::getCultureUpdateTimer, "int () - Culture Update Timer")
		.def("changeCultureUpdateTimer", &CyCity::changeCultureUpdateTimer, "void (iChange) - adjusts the Culture Update Timer by iChange")
		.def("isNeverLost", &CyCity::isNeverLost, "bool ()")
		.def("setNeverLost", &CyCity::setNeverLost, "void (iNewValue)")
		.def("isBombarded", &CyCity::isBombarded, "bool ()")
		.def("setBombarded", &CyCity::setBombarded, "void (iNewValue)")
		.def("isDrafted", &CyCity::isDrafted, "bool ()")
		.def("setDrafted", &CyCity::setDrafted, "void (iNewValue)")
		.def("isAirliftTargeted", &CyCity::isAirliftTargeted, "bool ()")
		.def("setAirliftTargeted", &CyCity::setAirliftTargeted, "void (iNewValue)")
		.def("isCitizensAutomated", &CyCity::isCitizensAutomated, "bool () - are citizens under automation?")
		.def("setCitizensAutomated", &CyCity::setCitizensAutomated, "void (bool bNewValue) - set city animation bNewValue")
		.def("isProductionAutomated", &CyCity::isProductionAutomated, "bool () - is production under automation?")
		.def("setProductionAutomated", &CyCity::setProductionAutomated, "void (bool bNewValue) - set city production automation to bNewValue")
		.def("isWallOverride", &CyCity::isWallOverride, "bool isWallOverride()")
		.def("setWallOverride", &CyCity::setWallOverride, "setWallOverride(bool bOverride)")
		.def("setCitySizeBoost", &CyCity::setCitySizeBoost, "setCitySizeBoost(int iBoost)")
		.def("isPlundered", &CyCity::isPlundered, "bool ()")
		.def("setPlundered", &CyCity::setPlundered, "void (iNewValue)")
		.def("getOwner", &CyCity::getOwner, "int /*PlayerTypes*/ ()")
		.def("getTeam", &CyCity::getTeam, "int /*TeamTypes*/ ()")
		.def("getPreviousOwner", &CyCity::getPreviousOwner, "int /*PlayerTypes*/ ()")
		.def("getOriginalOwner", &CyCity::getOriginalOwner, "int /*PlayerTypes*/ ()")
		.def("getCultureLevel", &CyCity::getCultureLevel, "int /*CultureLevelTypes*/ ()")
		.def("getCultureThreshold", &CyCity::getCultureThreshold)
		.def("getSeaPlotYield", &CyCity::getSeaPlotYield, "int (int /*YieldTypes*/) - total YieldType for water plots")
		.def("getRiverPlotYield", &CyCity::getRiverPlotYield, "int (int /*YieldTypes*/) - total YieldType for river plots")

		.def("getBaseYieldRate", &CyCity::getBaseYieldRate, "int (int /*YieldTypes*/) - base rate for YieldType")
		.def("setBaseYieldRate", &CyCity::setBaseYieldRate, "int (int /*YieldTypes*/, int iNewValue) - sets the base rate for YieldType")
		.def("changeBaseYieldRate", &CyCity::changeBaseYieldRate, "int (int /*YieldTypes*/, int iChange) - changes the base rate for YieldType")

		.def("getBaseYieldRateModifier", &CyCity::getBaseYieldRateModifier)
		.def("getYieldRate", &CyCity::getYieldRate, "int (int /*YieldTypes*/) - total value of YieldType")
		.def("getYieldRateModifier", &CyCity::getYieldRateModifier, "int (int /*YieldTypes*/) - yield rate modifier for YieldType")
		.def("getTradeYield", &CyCity::getTradeYield, "int (int /*YieldTypes*/) - trade adjustment to YieldType")
		.def("totalTradeModifier", &CyCity::totalTradeModifier, "int () - total trade adjustment")

		.def("calculateTradeProfit", &CyCity::calculateTradeProfit, "int (CyCity) - returns the trade profit created by CyCity")
		.def("calculateTradeYield", &CyCity::calculateTradeYield, "int (YieldType, int iTradeProfit) - calculates Trade Yield")

		.def("getExtraSpecialistYield", &CyCity::getExtraSpecialistYield, "int (int /*YieldTypes*/ eIndex)")
		.def("getExtraSpecialistYieldOfType", &CyCity::getExtraSpecialistYieldOfType, "int (int /*YieldTypes*/ eIndex, int /*SpecialistTypes*/ eSpecialist)")

		.def("getCommerceRate", &CyCity::getCommerceRate, "int (int /*CommerceTypes*/) - total Commerce rate")
		.def("getCommerceRateTimes100", &CyCity::getCommerceRateTimes100, "int (int /*CommerceTypes*/) - total Commerce rate")
		.def("getCommerceFromPercent", &CyCity::getCommerceFromPercent, "int (int /*CommerceTypes*/, int iYieldRate)")
		.def("getBaseCommerceRate", &CyCity::getBaseCommerceRate, "int (int /*CommerceTypes*/)")
		.def("getBaseCommerceRateTimes100", &CyCity::getBaseCommerceRateTimes100, "int (int /*CommerceTypes*/)")
		.def("getTotalCommerceRateModifier", &CyCity::getTotalCommerceRateModifier, "int (int /*CommerceTypes*/)")
		.def("getProductionToCommerceModifier", &CyCity::getProductionToCommerceModifier, "int (int /*CommerceTypes*/) - value of production to commerce modifier")
		.def("getBuildingCommerce", &CyCity::getBuildingCommerce, "int (int /*CommerceTypes*/) - total effect of cities buildings on CommerceTypes")
		.def("getBuildingCommerceByBuilding", &CyCity::getBuildingCommerceByBuilding, "int (int /*CommerceTypes*/, BuildingTypes) - total value of CommerceType from BuildingTypes")
		.def("getSpecialistCommerce", &CyCity::getSpecialistCommerce, "int (int /*CommerceTypes*/) - value of CommerceType adjustment from Specialists")
		.def("changeSpecialistCommerce", &CyCity::changeSpecialistCommerce, "void (int /*CommerceTypes*/, iChange) - adjusts Specialist contribution to CommerceType by iChange")
		.def("getReligionCommerce", &CyCity::getReligionCommerce, "int (int /*CommerceTypes*/) - effect on CommerceType by Religions")
		.def("getReligionCommerceByReligion", &CyCity::getReligionCommerceByReligion, "int (int /*CommerceTypes*/, ReligionType) - CommerceType effect from ReligionType")
		.def("getCorporationCommerce", &CyCity::getCorporationCommerce, "int (int /*CommerceTypes*/) - effect on CommerceType by Corporation")
		.def("getCorporationCommerceByCorporation", &CyCity::getCorporationCommerceByCorporation, "int (int /*CommerceTypes*/, CorporationType) - CommerceType effect from CorporationType")
		.def("getCorporationYield", &CyCity::getCorporationYield, "int (int /*CommerceTypes*/) - effect on YieldTypes by Corporation")
		.def("getCorporationYieldByCorporation", &CyCity::getCorporationYieldByCorporation, "int (int /*YieldTypes*/, CorporationType) - YieldTypes effect from CorporationType")
		.def("getCommerceRateModifier", &CyCity::getCommerceRateModifier, "int (int /*CommerceTypes*/) - indicates the total rate modifier on CommerceType")
		.def("getCommerceHappinessPer", &CyCity::getCommerceHappinessPer, "int (int /*CommerceTypes*/) - happiness from each level of entertainment")
		.def("getCommerceHappinessByType", &CyCity::getCommerceHappinessByType, "int (int /*CommerceTypes*/) - happiness from CommerceType")
		.def("getCommerceHappiness", &CyCity::getCommerceHappiness, "int () - happiness from all CommerceTypes")
		.def("getDomainFreeExperience", &CyCity::getDomainFreeExperience, "int (int /*DomainTypes*/)")
		.def("getDomainProductionModifier", &CyCity::getDomainProductionModifier, "int (int /*DomainTypes*/)")
		.def("getCulture", &CyCity::getCulture, "int /*PlayerTypes*/ ()")
		.def("getCultureTimes100", &CyCity::getCultureTimes100, "int /*PlayerTypes*/ ()")
		.def("countTotalCultureTimes100", &CyCity::countTotalCultureTimes100, "int ()")
		.def("findHighestCulture", &CyCity::findHighestCulture, "PlayerTypes ()")
		.def("calculateCulturePercent", &CyCity::calculateCulturePercent, "int (int eIndex)")
		.def("calculateTeamCulturePercent", &CyCity::calculateTeamCulturePercent, "int /*TeamTypes*/ ()")
		.def("setCulture", &CyCity::setCulture, "void (int PlayerTypes eIndex`, bool bPlots)")
		.def("setCultureTimes100", &CyCity::setCultureTimes100, "void (int PlayerTypes eIndex, int iNewValue, bool bPlots)")
		.def("changeCulture", &CyCity::changeCulture, "void (int PlayerTypes eIndex, int iChange, bool bPlots)")
		.def("changeCultureTimes100", &CyCity::changeCultureTimes100, "void (int PlayerTypes eIndex, int iChange, bool bPlots)")

		.def("isTradeRoute", &CyCity::isTradeRoute, "bool ()")
		.def("isEverOwned", &CyCity::isEverOwned, "bool ()")

		.def("isRevealed", &CyCity::isRevealed, "bool (int /*TeamTypes*/ eIndex, bool bDebug)")
		.def("setRevealed", &CyCity::setRevealed, "void (int /*TeamTypes*/ eIndex, bool bNewValue)")
		.def("getEspionageVisibility", &CyCity::getEspionageVisibility, "bool (int /*TeamTypes*/ eIndex)")
		.def("getName", &CyCity::getName, "string () - city name")
		.def("getNameForm", &CyCity::getNameForm, "string () - city name")
		.def("getNameKey", &CyCity::getNameKey, "string () - city name")
		.def("setName", &CyCity::setName, "void (TCHAR szNewValue, bool bFound) - sets the name to szNewValue")
		.def("isNoBonus", &CyCity::isNoBonus, "bool (int eIndex)")
		.def("changeNoBonusCount", &CyCity::changeNoBonusCount, "void (int eIndex, int iChange)")
		.def("getFreeBonus", &CyCity::getFreeBonus, "int (int eIndex)")
		.def("changeFreeBonus", &CyCity::changeFreeBonus, "void (int eIndex, int iChange)")
		.def("getNumBonuses", &CyCity::getNumBonuses, "int (PlayerID)")
		.def("hasBonus", &CyCity::hasBonus, "bool - (BonusID) - is BonusID connected to the city?")
		.def("getBuildingProduction", &CyCity::getBuildingProduction, "int (BuildingID) - current production towards BuildingID")
		.def("setBuildingProduction", &CyCity::setBuildingProduction, "void (BuildingID, iNewValue) - set progress towards BuildingID as iNewValue")
		.def("changeBuildingProduction", &CyCity::changeBuildingProduction, "void (BuildingID, iChange) - adjusts progress towards BuildingID by iChange")
		.def("getBuildingProductionTime", &CyCity::getBuildingProductionTime, "int (int eIndex)")
		.def("setBuildingProductionTime", &CyCity::setBuildingProductionTime, "int (int eIndex, int iNewValue)")
		.def("changeBuildingProductionTime", &CyCity::changeBuildingProductionTime, "int (int eIndex, int iChange)")
		.def("getBuildingOriginalOwner", &CyCity::getBuildingOriginalOwner, "int (BuildingType) - index of original building owner")
		.def("getBuildingOriginalTime", &CyCity::getBuildingOriginalTime, "int (BuildingType) - original build date")
		.def("getUnitProduction", &CyCity::getUnitProduction, "int (UnitID) - gets current production towards UnitID")
		.def("setUnitProduction", &CyCity::setUnitProduction, "void (UnitID, iNewValue) - sets production towards UnitID as iNewValue")
		.def("changeUnitProduction", &CyCity::changeUnitProduction, "void (UnitID, iChange) - adjusts production towards UnitID by iChange")
		.def("getGreatPeopleUnitRate", &CyCity::getGreatPeopleUnitRate, "int (int /*UnitTypes*/ iIndex)")
		.def("getGreatPeopleUnitProgress", &CyCity::getGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex)")
		.def("setGreatPeopleUnitProgress", &CyCity::setGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex, int iNewValue)")
		.def("changeGreatPeopleUnitProgress", &CyCity::changeGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex, int iChange)")
		.def("getSpecialistCount", &CyCity::getSpecialistCount, "int (int /*SpecialistTypes*/ eIndex)")
		.def("alterSpecialistCount", &CyCity::alterSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, int iChange)")
		.def("getMaxSpecialistCount", &CyCity::getMaxSpecialistCount, "int (int /*SpecialistTypes*/ eIndex)")
		.def("isSpecialistValid", &CyCity::isSpecialistValid, "bool (int /*SpecialistTypes*/ eIndex, int iExtra)")
		.def("getForceSpecialistCount", &CyCity::getForceSpecialistCount, "int (int /*SpecialistTypes*/ eIndex)")
		.def("isSpecialistForced", &CyCity::isSpecialistForced, "bool ()")
		.def("setForceSpecialistCount", &CyCity::setForceSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, int iNewValue")
		.def("changeForceSpecialistCount", &CyCity::changeForceSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, int iChange")
		.def("getFreeSpecialistCount", &CyCity::getFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex")
		.def("setFreeSpecialistCount", &CyCity::setFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, iNewValue")
		.def("changeFreeSpecialistCount", &CyCity::changeFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, iChange")
		.def("getAddedFreeSpecialistCount", &CyCity::getAddedFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex")
		.def("getImprovementFreeSpecialists", &CyCity::getImprovementFreeSpecialists, "int (ImprovementID)")
		.def("changeImprovementFreeSpecialists", &CyCity::changeImprovementFreeSpecialists, "void (ImprovementID, iChange) - adjust ImprovementID free specialists by iChange")
		.def("getReligionInfluence", &CyCity::getReligionInfluence, "int (ReligionID) - value of influence from ReligionID")
		.def("changeReligionInfluence", &CyCity::changeReligionInfluence, "void (ReligionID, iChange) - adjust ReligionID influence by iChange")

		.def("getCurrentStateReligionHappiness", &CyCity::getCurrentStateReligionHappiness, "int ()")
		.def("getStateReligionHappiness", &CyCity::getStateReligionHappiness, "int (int /*ReligionTypes*/ ReligionID)")
		.def("changeStateReligionHappiness", &CyCity::changeStateReligionHappiness, "void (int /*ReligionTypes*/ ReligionID, iChange)")

		.def("getUnitCombatFreeExperience", &CyCity::getUnitCombatFreeExperience, "int (int /*UnitCombatTypes*/ eIndex)")
		.def("getFreePromotionCount", &CyCity::getFreePromotionCount, "int (int /*PromotionTypes*/ eIndex)")
		.def("isFreePromotion", &CyCity::isFreePromotion, "bool (int /*PromotionTypes*/ eIndex)")
		.def("getSpecialistFreeExperience", &CyCity::getSpecialistFreeExperience, "int ()")
		.def("getEspionageDefenseModifier", &CyCity::getEspionageDefenseModifier, "int ()")

		.def("isWorkingPlotByIndex", &CyCity::isWorkingPlotByIndex, "bool (iIndex) - true if a worker is working this city's plot iIndex")
		.def("isWorkingPlot", &CyCity::isWorkingPlot, "bool (iIndex) - true if a worker is working this city's pPlot")
		.def("alterWorkingPlot", &CyCity::alterWorkingPlot, "void (iIndex)")
		.def("getNumRealBuilding", &CyCity::getNumRealBuilding, "int (BuildingID) - get # real building of this type")
		.def("setNumRealBuilding", &CyCity::setNumRealBuilding, "(BuildingID, iNum) - Sets number of buildings in this city of BuildingID type")
		.def("getNumFreeBuilding", &CyCity::getNumFreeBuilding, "int (BuildingID) - # of free Building ID (ie: from a Wonder)")
		.def("isHasReligion", &CyCity::isHasReligion, "bool (ReligionID) - does city have ReligionID?")
		.def("setHasReligion", &CyCity::setHasReligion, "void (ReligionID, bool bNewValue, bool bAnnounce, bool bArrows) - religion begins to spread")
		.def("isHasCorporation", &CyCity::isHasCorporation, "bool (CorporationID) - does city have CorporationID?")
		.def("setHasCorporation", &CyCity::setHasCorporation, "void (CorporationID, bool bNewValue, bool bAnnounce, bool bArrows) - corporation begins to spread")
		.def("isActiveCorporation", &CyCity::isActiveCorporation, "bool (CorporationID) - does city have active CorporationID?")
		.def("getTradeCity", &CyCity::getTradeCity, python::return_value_policy<python::manage_new_object>(), "CyCity (int iIndex) - remove SpecialistType[iIndex]")
		.def("getTradeRoutes", &CyCity::getTradeRoutes, "int ()")

		.def("clearOrderQueue", &CyCity::clearOrderQueue, "void ()")
		.def("pushOrder", &CyCity::pushOrder, "void (OrderTypes eOrder, int iData1, int iData2, bool bSave, bool bPop, bool bAppend, bool bForce)")
		.def("popOrder", &CyCity::popOrder, "int (int iNum, bool bFinish, bool bChoose)")
		.def("getOrderQueueLength", &CyCity::getOrderQueueLength, "void ()")
		.def("getOrderFromQueue", &CyCity::getOrderFromQueue, python::return_value_policy<python::manage_new_object>(), "OrderData* (int iIndex)")

		.def("setWallOverridePoints", &CyCity::setWallOverridePoints, "setWallOverridePoints(const python::tuple& kPoints)")
		.def("getWallOverridePoints", &CyCity::getWallOverridePoints, "python::tuple getWallOverridePoints()")

		.def("AI_avoidGrowth", &CyCity::AI_avoidGrowth, "bool ()")
		.def("AI_isEmphasize", &CyCity::AI_isEmphasize, "bool (int iEmphasizeType)")
		.def("AI_countBestBuilds", &CyCity::AI_countBestBuilds, "int (CyArea* pArea)")
		.def("AI_cityValue", &CyCity::AI_cityValue, "int ()")

		.def("getScriptData", &CyCity::getScriptData, "str () - Get stored custom data (via pickle)")
		.def("setScriptData", &CyCity::setScriptData, "void (str) - Set stored custom data (via pickle)")

		.def("visiblePopulation", &CyCity::visiblePopulation, "int ()")

		.def("getBuildingYieldChange", &CyCity::getBuildingYieldChange, "int (int /*BuildingClassTypes*/ eBuildingClass, int /*YieldTypes*/ eYield)")
		.def("setBuildingYieldChange", &CyCity::setBuildingYieldChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int /*YieldTypes*/ eYield, int iChange)")
		.def("getBuildingCommerceChange", &CyCity::getBuildingCommerceChange, "int (int /*BuildingClassTypes*/ eBuildingClass, int /*CommerceTypes*/ eCommerce)")
		.def("setBuildingCommerceChange", &CyCity::setBuildingCommerceChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int /*CommerceTypes*/ eCommerce, int iChange)")
		.def("getBuildingHappyChange", &CyCity::getBuildingHappyChange, "int (int /*BuildingClassTypes*/ eBuildingClass)")
		.def("setBuildingHappyChange", &CyCity::setBuildingHappyChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int iChange)")
		.def("getBuildingHealthChange", &CyCity::getBuildingHealthChange, "int (int /*BuildingClassTypes*/ eBuildingClass)")
		.def("setBuildingHealthChange", &CyCity::setBuildingHealthChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int iChange)")

		.def("getLiberationPlayer", &CyCity::getLiberationPlayer, "int ()")
		.def("liberate", &CyCity::liberate, "void ()")

//FfH: Added by Kael 10/18/2007
		.def("applyBuildEffects", &CyCity::applyBuildEffects, "void (CyUnit* pUnit)")
		.def("changeCrime", &CyCity::changeCrime, "void (int iChange) - changes the Crime Rate for this city")
		.def("getCrime", &CyCity::getCrime, "int () - crime rate")
		.def("isHasBuildingClass", &CyCity::isHasBuildingClass, "bool (int /*BuildingClassTypes*/ iIndex) - has building class")
		.def("isSettlement", &CyCity::isSettlement, "bool () - is settlement")
		.def("setCivilizationType", &CyCity::setCivilizationType, "void (int iNewValue) - sets the Civilization Type of this city")
		.def("setPlotRadius", &CyCity::setPlotRadius, "void (int iNewValue) - sets the Plot Radius of this city")
		.def("setSettlement", &CyCity::setSettlement, "void (bool bNewValue) - sets city as a Settlement or not")
//FfH: End Add

/*************************************************************************************************/
/**	BETTER AI (New Functions Definition) Sephi                                 					**/
/**																								**/
/**						                                            							**/
/*************************************************************************************************/
        .def("AI_neededPermDefense", &CyCity::AI_neededPermDefense, "int (int flag)")
        .def("AI_neededPatrol", &CyCity::AI_neededPatrol, "int (int flag)")
		.def("AI_stopGrowth", &CyCity::AI_stopGrowth, "bool ()")
		.def("AI_neededSeaWorkers", &CyCity::AI_neededSeaWorkers, "int ()")
		.def("AI_neededCityDefenseProduction", &CyCity::AI_neededCityDefenseProduction, "int (int)")
		.def("AI_neededCityPatrolProduction", &CyCity::AI_neededCityPatrolProduction, "int (int)")
/*************************************************************************************************/
/**	END	                                        												**/
/*************************************************************************************************/
		;
}
