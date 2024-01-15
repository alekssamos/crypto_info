import config
import braille
import scriptHandler
import os
import json
import time
import wx
import threading
import sys

import globalPluginHandler
import gui
import globalVars
import speech
import api
import textInfos
import tones
import ui
import addonHandler
import languageHandler
from logHandler import log
from . import parsers
from .crypto_infoFrame import crypto_infoFrame


addonHandler.initTranslation()

if "crypto_info" not in config.conf: config.conf["crypto_info"]={}

parsers_classes = parsers.Base.__subclasses__()
parsers_classes_names = [l.__name__ for l in parsers_classes]
parsers_names = [l.name for l in parsers_classes]

def parseData(classname):
	ps = getattr(parsers, classname)()
	headers, content = ps.get_info(False)
	if classname == "Investing":
		l = []
		for c in content:
			l.append((
				str(c[0]), #name
				str(c[2]), #price
				ps.toStr(c[6]), #ch 24h
				ps.toStr(c[3]) #capitalization
			))

		return l

	return content

def _speakData(classname, position):
	ui.message(_("Data is being received... Wait..."))
	try:
		data = parseData(classname)[position]
		speech.cancelSpeech()
		msg = ""
		cols = [_("Name"), _("Price"), _("changes"), _("Capitalization")]
		lines = []
		# if len(cols) != len(data): raise ValueError("")
		# for i in range(0, len(cols)):
			# lines.append(cols[i]+": "+data[i])
		lines.append(data[0])
		lines.append(cols[1]+": "+data[1])
		lines.append(cols[2]+": "+data[2])
		lines.append(cols[3]+": "+data[3])
		msg = ",\n".join(lines)
		ui.message(msg)
	except:
		speech.cancelSpeech()
		ui.message(_('An error occurred while retrieving the data. '
		'Check the connection and try again after a while.') + resp)

def speakData(classname, position):
	threading.Thread(target=_speakData, args=[parsers_classes_names[0], position]).start()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.crypto_infoMainDialogItem = gui.mainFrame.sysTrayIcon.toolsMenu.Append(wx.ID_ANY,
			_("crypto info"))
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU, self.onSettings, self.crypto_infoMainDialogItem)

	def terminate(self):
		try:
			gui.mainFrame.sysTrayIcon.toolsMenu.RemoveItem(
				self.crypto_infoMainDialogItem)
		except:
			pass

	def onSettings(self, evt):
		gui.mainFrame.prePopup()
		d = crypto_infoFrameDialog(gui.mainFrame)
		d.Show()
		gui.mainFrame.postPopup()
		d.postInit()

	def script_position1(self, gesture): speakData(parsers_classes_names[0], 1)
	def script_position2(self, gesture): speakData(parsers_classes_names[0], 2)
	def script_position3(self, gesture): speakData(parsers_classes_names[0], 3)
	def script_position4(self, gesture): speakData(parsers_classes_names[0], 4)
	def script_position5(self, gesture): speakData(parsers_classes_names[0], 5)
	def script_position6(self, gesture): speakData(parsers_classes_names[0], 6)
	def script_position7(self, gesture): speakData(parsers_classes_names[0], 7)
	def script_position8(self, gesture): speakData(parsers_classes_names[0], 8)
	def script_position9(self, gesture): speakData(parsers_classes_names[0], 9)
	def script_position0(self, gesture): speakData(parsers_classes_names[0], 0)
	def script_onSettings(self, gesture): self.onSettings(None)

	script_position1.__doc__ = _("Position #")+"1"
	script_position1.category = "Crypto info"
	script_position2.__doc__ = _("Position #")+"2"
	script_position2.category = "Crypto info"
	script_position3.__doc__ = _("Position #")+"3"
	script_position3.category = "Crypto info"
	script_position4.__doc__ = _("Position #")+"4"
	script_position4.category = "Crypto info"
	script_position5.__doc__ = _("Position #")+"5"
	script_position5.category = "Crypto info"
	script_position6.__doc__ = _("Position #")+"6"
	script_position6.category = "Crypto info"
	script_position7.__doc__ = _("Position #")+"7"
	script_position7.category = "Crypto info"
	script_position8.__doc__ = _("Position #")+"8"
	script_position8.category = "Crypto info"
	script_position9.__doc__ = _("Position #")+"9"
	script_position9.category = "Crypto info"
	script_position0.__doc__ = _("Position #")+"0"
	script_position0.category = "Crypto info"
	script_onSettings.__doc__ = _("Open crypto info window")
	script_onSettings.category = "Crypto info"
	__gestures = {
		"kb:NVDA+Alt+K": "onSettings",
		"kb:NVDA+Alt+1": "position1",
		"kb:NVDA+Alt+2": "position2",
		"kb:NVDA+Alt+3": "position3",
		"kb:NVDA+Alt+4": "position4",
		"kb:NVDA+Alt+5": "position5",
		"kb:NVDA+Alt+6": "position6",
		"kb:NVDA+Alt+7": "position7",
		"kb:NVDA+Alt+8": "position8",
		"kb:NVDA+Alt+9": "position9",
		"kb:NVDA+Alt+0": "position0",
	}


class crypto_infoFrameDialog(crypto_infoFrame):
	def update_crypto_list_ctrl(self, classname):
		ui.message(_("Data is being received... Wait..."))
		data = parseData(classname)
		index=0
		self.crypto_list_ctrl.DeleteAllItems()
		for d in data:
			self.crypto_list_ctrl.InsertItem(index, d[0])
			self.crypto_list_ctrl.SetItem(index, 1, d[1])
			self.crypto_list_ctrl.SetItem(index, 2, d[2])
			self.crypto_list_ctrl.SetItem(index, 3, d[3])
			index=index+1

	def onrefresh(self, evt):
		threading.Thread(target=self.update_crypto_list_ctrl, args=[parsers_classes_names[0]]).start()

	def postInit(self):
		self.onrefresh(None)

	def onok(self, evt):
		self.Close()

	def oncancel(self, evt):
		self.Close()
