## Save-load diagnostics for corrupt CvUnit records.
##
## This module must remain compatible with Civ4's embedded Python 2.4.

from CvPythonExtensions import *
import BugCore
import BugPath
import BugUtil
import codecs
import os
import time
import traceback


gc = CyGlobalContext()
SaveDiagnosticsOpt = BugCore.game.SaveDiagnostics

LOG_PREFIX = "save-load-"
LOG_SUFFIX = ".log"


def _resolveLogDirectory():
	value = SaveDiagnosticsOpt.getLogDirectory()
	if not value or value == "Default":
		return BugPath.findOrMakeDir("SaveDiagnostics")

	value = os.path.expandvars(value)
	if not os.path.isabs(value):
		value = os.path.join(BugPath.getRootDir(), value)
	if not os.path.isdir(value):
		os.makedirs(value)
	return value


def _removeOldLogs(logDirectory, maxFiles):
	if maxFiles < 1:
		return

	files = []
	for name in os.listdir(logDirectory):
		if name.startswith(LOG_PREFIX) and name.endswith(LOG_SUFFIX):
			path = os.path.join(logDirectory, name)
			if os.path.isfile(path):
				files.append((os.path.getmtime(path), path))
	files.sort()

	while len(files) >= maxFiles:
		unusedMtime, path = files.pop(0)
		try:
			os.remove(path)
		except:
			BugUtil.warn("SaveDiagnostics - cannot remove old log %s", path)


def _write(logFile, message):
	logFile.write(unicode(message))
	logFile.write(u"\r\n")


def onLoadGame():
	if not SaveDiagnosticsOpt.isEnabled():
		return None

	logDirectory = _resolveLogDirectory()
	if not logDirectory:
		BugUtil.error("SaveDiagnostics - no writable log directory")
		return None

	maxFiles = SaveDiagnosticsOpt.getMaxFiles()
	_removeOldLogs(logDirectory, maxFiles)

	now = time.strftime("%Y%m%d-%H%M%S")
	turn = gc.getGame().getGameTurn()
	fileName = "%s%s-turn-%04d-pid-%d%s" % (
		LOG_PREFIX,
		now,
		turn,
		os.getpid(),
		LOG_SUFFIX,
	)
	logPath = os.path.join(logDirectory, fileName)
	logFile = codecs.open(logPath, "w", "utf-8")

	badUnits = 0
	unitCount = 0
	try:
		_write(
			logFile,
			"FFH2_SAVE_DIAG_BEGIN timestamp=%s turn=%d numUnitInfos=%d mapWidth=%d mapHeight=%d"
			% (
				now,
				turn,
				gc.getNumUnitInfos(),
				gc.getMap().getGridWidth(),
				gc.getMap().getGridHeight(),
			),
		)

		for playerID in xrange(gc.getMAX_PLAYERS()):
			player = gc.getPlayer(playerID)
			unit, iterator = player.firstUnit(False)
			while unit:
				try:
					unitID = unit.getID()
					unitType = unit.getUnitType()
					x = unit.getX()
					y = unit.getY()
					_write(
						logFile,
						"FFH2_SAVE_DIAG_UNIT owner=%d id=%d type=%d x=%d y=%d"
						% (playerID, unitID, unitType, x, y),
					)
					unitCount += 1
					if unitType < 0 or unitType >= gc.getNumUnitInfos():
						badUnits += 1
						_write(
							logFile,
							"FFH2_SAVE_DIAG_BAD_UNIT owner=%d id=%d type=%d x=%d y=%d"
							% (playerID, unitID, unitType, x, y),
						)
				except:
					_write(
						logFile,
						"FFH2_SAVE_DIAG_UNIT_EXCEPTION owner=%d" % playerID,
					)
					traceback.print_exc(file=logFile)
				unit, iterator = player.nextUnit(iterator, False)

		_write(
			logFile,
			"FFH2_SAVE_DIAG_SUMMARY units=%d badUnits=%d" % (unitCount, badUnits),
		)

		pauseSeconds = SaveDiagnosticsOpt.getPauseSeconds()
		if pauseSeconds > 0:
			_write(
				logFile,
				"FFH2_SAVE_DIAG_PAUSE_BEGIN seconds=%d" % pauseSeconds,
			)
			logFile.flush()
			time.sleep(pauseSeconds)
			_write(logFile, "FFH2_SAVE_DIAG_PAUSE_END")

		_write(logFile, "FFH2_SAVE_DIAG_END")
	finally:
		logFile.close()

	BugUtil.info(
		"SaveDiagnostics - wrote %s (units=%d, bad=%d)",
		logPath,
		unitCount,
		badUnits,
	)
	return logPath
