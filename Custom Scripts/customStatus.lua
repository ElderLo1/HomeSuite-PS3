-- This script is intended to be mapped to the F7 hotkey when the client boots using hubstartup.txt.

LoadLibrary("LocalPlayer")
LoadLibrary("Person")
LoadLibrary("Osk")

function entryComplete()
	OskText = Osk.GetText()
	LocalPerson = LocalPlayer.GetPerson()
	if (OskText == nil) then
		Person.SetCurrentStatusText(LocalPerson, "")
	else
		Person.SetCurrentStatusText(LocalPerson, OskText)
	end
end

function setStatusThread()
	
	while ( true ) do
	
		if ( Debug.KeyIsPressed( KEY_F7 ) ) then
			print("Gonna try to open up the OSK...")
			if (Osk.IsAvailable() == true) then
				print("Looks like it worked! :D")
				Osk.Open(entryComplete, "What do you want your status to be?", "... has a new status!", 35, CharacterSet.Default, false)
			else
				print("OSK could not be opened at this time... :(")
			end
		end
		
		Sleep( 0.0 )
		
	end
end

StatusMonitorThreadId = SpawnFunction( setStatusThread )
