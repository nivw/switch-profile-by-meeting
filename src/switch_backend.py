#!/usr/bin/run-standalone.sh python2.5

# Import global modules
import sys, traceback, gobject, dbus, dbus.mainloop.glib ,os , subprocess 
import time, sqlite3,mafw
sys.path.insert(0, '/usr/lib/switchProfByMeeting')
import debug
debug = debug.debug

sys.path.insert(0, '/home/user')
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

class backend:
	def __init__( self ):
		#debug( 'init' )
		self.bus = dbus.SessionBus()
		self.sleep_duration = 10000
		self.timeout_id = None
		self.loop = None
		
		try:
			self.profiled_object = self.bus.get_object( 'com.nokia.profiled', '/com/nokia/profiled' )
			self.calender_object = self.bus.get_object( 'com.nokia.calendar', '/com/nokia/calendar' )
			self.calender_object.connect_to_signal( 'dbChange', \
			self.calender_changed, dbus_interface = 'com.nokia.calendar' )
			self.mafw_object = self.bus.get_object( \
			'com.nokia.mafw.renderer.Mafw-Gst-Renderer-Plugin.gstrenderer' \
			,'/com/nokia/mafw/renderer/gstrenderer' )
		except dbus.DBusException:
			traceback.print_exc()
			sys.exit(1)

		self.start()

	def set_profile( self, prof ):
		debug ('in set_profile with '+prof)
		#save speaker volume as profile change effects it
		volume_level = self.mafw_object.get_extension_property( 'volume' \
		, dbus_interface = 'com.nokia.mafw.extension')[1]
		self.profiled_object.set_profile(prof, dbus_interface='com.nokia.profiled')
		#restore volume level due to profile change
		retcode = subprocess.call("dbus-send --type=method_call \
		--dest=com.nokia.mafw.renderer.Mafw-Gst-Renderer-Plugin.gstrenderer \
		/com/nokia/mafw/renderer/gstrenderer \
		com.nokia.mafw.extension.set_extension_property \
		string:volume variant:uint32:%d"%volume_level, shell=True)
		if retcode != 0:
			raise SystemExit('got error code '+str(retcode)+' when setting volume')

	def is_meeting_now( self ):
		cal_db = sqlite3.connect(os.path.expanduser("~/.calendar/calendardb"))
		query = "SELECT Summary FROM Components WHERE ComponentType='1' \
		AND AllDay='0' AND strftime('%s','now') >= DateStart AND \
		strftime('%s','now') < DateEnd limit 1"
		ans = cal_db.execute(query).fetchone()
		debug( 'is_meeting_now returns: '+str(ans) )
		return ans

	def when_next_meeting( self ):
		cal_db = sqlite3.connect(os.path.expanduser("~/.calendar/calendardb"))	
		query = "SELECT DateStart FROM Components WHERE ComponentType='1' \
		and AllDay='0' and strftime('%s','now') < DateStart AND \
		DateStart < DateEnd ORDER BY DateStart limit 1"
	#here is the place to make sure the meeting is leagal non zero duration and event 
		ans = cal_db.execute(query).fetchone()
		if ans != None:
			next_timeout = ans [0]
		else:
			next_timeout = None
		debug( 'when_next_meeting returns: '+str(next_timeout) )
		return next_timeout
		
	def when_end_of_meeting( self ):
		cal_db = sqlite3.connect(os.path.expanduser("~/.calendar/calendardb"))	
		query = "SELECT DateEnd FROM Components WHERE ComponentType='1' \
		and AllDay='0' and strftime('%s','now') < DateEnd and \
		DateStart < DateEnd ORDER BY DateEnd limit 1"
		#I also need to adress overlapping meetings that the other finishes later
		next_timeout = cal_db.execute(query).fetchone() [0]
		debug( 'when_end_of_meeting returns: ' +str(next_timeout) )
		return next_timeout
		
	def calc_next_duration( self, next_meeting_time ):
		if next_meeting_time != None:
			self.sleep_duration = int ((next_meeting_time - time.time())*1000)
		else:
			self.sleep_duration = 5000
		debug("calc_next_duration returns: "+str(self.sleep_duration))
			
	def set_timer( self, current_profile ):
		if current_profile == 'general' :
			self.calc_next_duration( self.when_next_meeting() )
		else :
			self.calc_next_duration( self.when_end_of_meeting() )
			
	def calender_changed( self, arg1 , arg2 ):
		debug('calender_changed called with arg1: '+arg1+' arg2: '+arg2 )
		self.remove_timeout()
		self.update_profile()
		self.mainloop()
		debug ('end of calender_changed')
		
	def timer_callback( self ):
		debug('timer_callback timeout_id: '+str(self.timeout_id))
		self.remove_timeout()
		self.update_profile()
		self.mainloop()
		#commented by merlin 1991 advice self.mainloop()
		debug('end of timer_callback')
			
	def remove_timeout( self ):
		debug ( 'remove timeout called' )
		if self.timeout_id != None:
			gobject.source_remove(self.timeout_id)
			debug( 'removed timeout: '+str(self.timeout_id) )

	def update_profile( self ):
		debug ( 'begining of update_profile' )
		if self.is_meeting_now() :
			self.set_profile( 'silent' )
			self.set_timer( 'silent' )
		else:
			self.set_profile( 'general' )
			self.set_timer( 'general' )
			
	def mainloop( self ):
		debug('going to run loop with sleep_duration: '+str(self.sleep_duration))
		self.timeout_id = gobject.timeout_add(self.sleep_duration, self.timer_callback )
		debug( ' new timeou_id is: '+str(self.timeout_id) )

		if self.loop == None :
			self.loop = gobject.MainLoop()
			self.loop.run()
			debug('new loop started')
		debug ('end of mainloop')
		
	def start ( self ):
		''' update the profile and set a timer loop'''
		debug( 'starting' )
		self.update_profile()
		self.mainloop()
		
	def stop_mainloop( self ):
		''' stop nain loop'''
		debug( 'stopping main loop' )
		if self.loop != None and self.loop.is_running():
			self.loop.quit()
		
	def status( self ):
		'''check the status of the switch backend'''
		if self.loop != None:
			status = self.loop.is_running()
		else:
			status = None
		debug( 'status is: '+status)
		return status

if __name__ == "__main__":
	backend = backend()
