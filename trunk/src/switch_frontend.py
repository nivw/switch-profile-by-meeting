#!/usr/bin/env python

#import gobject
import gtk, hildon
import sys,commands
sys.path.insert(0, '/usr/lib/switchProfByMeeting')
import debug
debug = debug.debug


class frontend:
	def __init__(self):
		# Basic properties
		self.backend_started = self.status_backend()
		debug('self.backend_started is:'+str(self.backend_started))
		
		# Initialize the main window
		self.program = hildon.Program.get_instance()
		self.mainwindow = hildon.StackableWindow()
		self.program.add_window(self.mainwindow)
		self.mainwindow.connect( 'delete_event', self.quit, None)
		self.mainwindow.set_title( 'switchProfileByMeeting')
		
		# Start/stop button
		self.startstop_button = hildon.Button(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL, 'not on')
		self.startstop_button.connect('clicked', self.startstop_clicked)
		self.mainwindow.add(self.startstop_button)
		self.update_startstop_state()
		#think its allready in mainloop self.mainwindow.show_all()
		debug ('mainwindow created')

	def update_startstop_state(self):
		"""Update the start/stop button to reflect current state"""
		debug('in update_startstop_state')
		#states = [ gtk.STATE_NORMAL, gtk.STATE_ACTIVE, gtk.STATE_PRELIGHT, gtk.STATE_SELECTED,  gtk.STATE_INSENSITIVE ]
		if self.backend_started:
			self.startstop_button.set_title('Stop')
		else:
			self.startstop_button.set_title('Start')

	def startstop_clicked(self, *args):
		"""Starts or stops the backend according to current state"""
		if self.backend_started:
			self.stop_backend()
		else:
			self.start_backend()
		self.update_startstop_state()
		
#work is needed below here
	def start_backend(self):
		"""calls backend start"""
		debug('called start_backend')
		#return_tuple = commands.getstatusoutput('/etc/init.d/switch start &')
		(status, output) = commands.getstatusoutput("""sudo /etc/init.d/switch_backend start""")
		
		if status <> 0:
			print "DEBUG: backend start exit code " + str(status) + ", output: \n"
			note = hildon.hildon_note_new_information(self.mainwindow, 'switchProfByMeeting failed to start')
			response = gtk.Dialog.run(note)
			note.destroy()
			return
		self.backend_started = True
		self.update_startstop_state()

	def stop_backend(self):
		"""kills backend"""
		(status, output) = commands.getstatusoutput("""sudo /etc/init.d/switch_backend stop""")
		if status <> 0:
			print "DEBUG: backend stop exit code " + str(status) + ", output: \n"
			print return_tuple[1]
			note = hildon.hildon_note_new_information(self.mainwindow, 'switch failed to stop')
			response = gtk.Dialog.run(note)
			note.destroy()
			return
		self.backend_started = False
		self.update_startstop_state()

	def status_backend(self):
		"""is backend running?"""
		return_tuple = commands.getstatusoutput('pgrep switch_backend')
		debug ('is the backend running? '+str(return_tuple))
		if return_tuple[0] == 0:
			return True
		else:
			return False
        
	def quit(self, *args):
		"""Cleanup routines and possible pre-exit confirmations"""
		if self.backend_started:
			note = hildon.hildon_note_new_confirmation(self.mainwindow, 'switch is active, are you sure you want to quit ?')
			response = note.run()
			note.hide()
			note.destroy()
			if response != gtk.RESPONSE_OK:
				# Not ok to quit, return true to prevent window from being deleted...
				return True
			self.stop_backend()
		gtk.main_quit()

	def mainloop(self):
		"""Program entry point; draws windows and enters GTK mainloop"""
		self.mainwindow.show_all()
		gtk.main()

if __name__ == "__main__":
    f = frontend()
    f.mainloop()
