"""
Callback functions for vote system
"""

from CvPythonExtensions import *
from PyHelpers import PyGame
import PyHelpers

PyPlayer = PyHelpers.PyPlayer

gc = CyGlobalContext()


### Main callbacks

def votePrereq( argsList ) :
	print( "votePrereq()" )
	eVote, = argsList
	return eval( gc.getVoteInfo( eVote ).getPyRequirement() )

def voteAI( argsList ) :
	ePlayer, eVote, eVotePlayer, iVoteCityId, eVoteOtherPlayer, = argsList
	return eval( gc.getVoteInfo( eVote ).getPyAI() )

def voteResult( argsList ) :
	eVote, = argsList
	eval( gc.getVoteInfo( eVote ).getPyResult() )


# Fund dissidents

def canDoFundDissidents() :
	eOvercouncil = gc.getInfoTypeForString( 'DIPLOVOTE_OVERCOUNCIL' )
	for ePlayer, pyPlayer in PyGame().iterAliveCivPlayers() :
		if pyPlayer.isFullMember( eOvercouncil ) :
			return True
	return False
	

def doFundDissidents() :
	eOvercouncil = gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')
	for ePlayer, pyPlayer in PyGame().iterAliveCivPlayers() :
		if pyPlayer.isFullMember( eOvercouncil ):
			for pyCity in pyPlayer.iterCities() :
				if CyGame().getSorenRandNum(100, "Fund Dissidents") < 50:
					pyCity.changeHurryAngerTimer(1 + CyGame().getSorenRandNum(3, "Fund Dissidents"))

def voteShareMaps():

	iOvercouncil = gc.getInfoTypeForString('CIVIC_OVERCOUNCIL')
	iMembership = gc.getInfoTypeForString('CIVICOPTION_MEMBERSHIP')

	iSidar = gc.getInfoTypeForString('CIVILIZATION_SIDAR')

	lMembers = []
	for iPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			if pPlayer.getCivics(iMembership) == iOvercouncil:
				lMembers.append(pPlayer)
	for pPlayer in lMembers:
		if pPlayer.getCivilizationType() == iSidar:continue
		iTeam = pPlayer.getTeam()
		for pPlayer2 in lMembers:
			iTeam2 = pPlayer2.getTeam()
			if iTeam == iTeam2:continue
			gc.getTeam(iTeam2).changeStolenVisibilityTimer(iTeam,2)


def voteArawnAffinity():
	iOvercouncil = gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')
	iUndead = gc.getInfoTypeForString('PROMOTION_UNDEAD')
	iUndeathA = gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH')
	iArawnA = gc.getInfoTypeForString('PROMOTION_AFFINITY_DEATH_ARAWN')
	for iPlayer in xrange(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			if pPlayer.isFullMember(iOvercouncil):
				for loopUnit in PyPlayer(iPlayer).getUnitList():
					if loopUnit.getRace() == iUndead:
						loopUnit.kill(False, PlayerTypes.NO_PLAYER)
					elif loopUnit.isHasPromotion(iUndeathA):
						loopUnit.setHasPromotion(iUndeathA, False)
						loopUnit.setHasPromotion(iArawnA, True)

def voteBanSlavery():
	iOvercouncil = gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')
	iLabor = gc.getInfoTypeForString('CIVICOPTION_LABOR')
	iSlavery = gc.getInfoTypeForString('CIVIC_SLAVERY')
	iTribalism = gc.getInfoTypeForString('CIVIC_TRIBALISM')
	iSlave = gc.getInfoTypeForString('UNIT_SLAVE')
	for iPlayer in xrange(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			if pPlayer.isFullMember(iOvercouncil):
				if pPlayer.getCivics(iLabor) == iSlavery:
					pPlayer.setCivics(iLabor, iTribalism)
				for loopUnit in PyPlayer(iPlayer).getUnitList():
					if loopUnit.getUnitType() == iSlave:
						loopUnit.kill(False, PlayerTypes.NO_PLAYER)

def voteFundDissidents():
	iOvercouncil = gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')
	for iPlayer in xrange(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			if pPlayer.isFullMember(iOvercouncil):
				(loopCity, iter) = pPlayer.firstCity(False)
				while(loopCity):
					if (not loopCity.isNone() and loopCity.getOwner() == iPlayer): #only valid cities
						if CyGame().getSorenRandNum(100, "Fund Dissidents") < 50:
							loopCity.changeHurryAngerTimer(1 + CyGame().getSorenRandNum(3, "Fund Dissidents"))
					(loopCity, iter) = pPlayer.nextCity(iter, False)




					
# Setup gambling ring

def aiGamblingRing( ePlayer ) :
	pPlayer = gc.getPlayer( ePlayer )
	if pPlayer.getAlignment() != gc.getInfoTypeForString( "ALIGNMENT_EVIL" ) :
		return PlayerVoteTypes.PLAYER_VOTE_NO
	
	return PlayerVoteTypes.NO_PLAYER_VOTE


# Slave trade

def aiSlaveTrade( ePlayer ) :
	pPlayer = gc.getPlayer( ePlayer )
	if pPlayer.getAlignment() != gc.getInfoTypeForString( "ALIGNMENT_EVIL" ) :
		return PlayerVoteTypes.PLAYER_VOTE_NO
	
	return PlayerVoteTypes.NO_PLAYER_VOTE


# Setup smuggling ring

def aiSmugglingRing( ePlayer ) :
	pPlayer = gc.getPlayer( ePlayer )
	if 4 * pPlayer.countNumCoastalCities() <= pPlayer.getNumCities() :
		return PlayerVoteTypes.PLAYER_VOTE_NO
	elif 3 * pPlayer.countNumCoastalCities() <= pPlayer.getNumCities() :
		return PlayerVoteTypes.PLAYER_VOTE_ABSTAIN # LFGR_TODO: does this actually do anything?
	else :
		return PlayerVoteTypes.PLAYER_VOTE_YES
	
