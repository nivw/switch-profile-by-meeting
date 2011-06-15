#!/usr/bin/env python

import hildon, gtk
import hildondesktop
import commands

class ExampleStatusPlugin(hildondesktop.StatusMenuItem):
	def __init__(self):
		hildondesktop.StatusMenuItem.__init__(self)

		self.backend_started =  self.status_backend()

		self.button_title_text = "switchProfile"
		self.button = hildon.Button(gtk.HILDON_SIZE_AUTO_WIDTH | gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL)
		self.button.set_style(hildon.BUTTON_STYLE_PICKER)
		self.button.set_alignment(0.2,0.5,1,1)
		image = gtk.image_new_from_icon_name("switchProfile", gtk.ICON_SIZE_BUTTON)
		self.button.set_image(image)
		self.button.set_image_position(gtk.POS_LEFT)
		self.button.connect("clicked", self.button_clicked_event)

		icon_theme = gtk.icon_theme_get_default()
		self.pixbuf = icon_theme.load_icon("switchProfile", 22, gtk.ICON_LOOKUP_NO_SVG)

		self.add(self.button)
		self.show_all()
		self.update_button()

	def status_backend(self):
		"""is backend running?"""
		return commands.getoutput('pgrep switch_backend')

	def button_clicked_event(self,*args):
		if self.backend_started:
			self.stop_backend()
		else:
			self.start_backend()
		self.update_button()

	def update_button(self):
		"""Update the start/stop button to reflect current state"""
		if self.backend_started:
			self.button.set_text(self.button_title_text,'Stop')
			self.set_status_area_icon(self.pixbuf)
		else:
			self.button.set_text(self.button_title_text,'Start')
			self.set_status_area_icon(None)
	
	def start_backend(self):
		"""calls backend start"""
		(exitstatus, outtext) = commands.getstatusoutput("""/etc/init.d/switch_backend start""")
		if exitstatus <> 0:
			print "DEBUG: backend start exit code " + str(status) + ", output: \n"
			note = hildon.hildon_note_new_information(self.mainwindow, 'switchProfByMeeting failed to start')
			response = gtk.Dialog.run(note)
			note.destroy()
			return
		self.backend_started = True

	def stop_backend(self):
		"""kills backend"""
		(exitstatus, outtext) = commands.getstatusoutput("""/etc/init.d/switch_backend stop""")
		if exitstatus <> 0:
			print "DEBUG: backend start exit code " + str(status) + ", output: \n"
			note = hildon.hildon_note_new_information(self.mainwindow, 'switchProfByMeeting failed to start')
			response = gtk.Dialog.run(note)
			note.destroy()
			return
		self.backend_started = False

hd_plugin_type = ExampleStatusPlugin
