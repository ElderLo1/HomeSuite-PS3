LoadLibrary("Osk")

function entryComplete()
	OskText = Osk.GetText()
	if (OskText == nil) then
		print("No IP or domain was entered! The override will not proceed.")
	else
		print("Overriding MUIS to " + OskText + "...")
		Debug.System("muisOverride " + OskText + "")
		Sleep(0.5)
		Debug.System("logoff")
	end
end

function OverrideThread()
	
	print("Script hooked into F11!")
	while ( true ) do
	
		if ( Debug.KeyIsPressed( KEY_F11 ) ) then
			print("Gonna try to open up the OSK...")
			if (Osk.IsAvailable() == true) then
				print("Looks like it worked! :D")
				Osk.Open(entryComplete, "Enter MUIS IP/Domain", "muis.cdevc.homeps3.online.scee.com", 50, CharacterSet.Default, false)
			else
				print("OSK could not be opened at this time... :(")
			end
		end
		
		Sleep( 0.0 )
		
	end
end

MUISOVERRIDEMonitorThreadId = SpawnFunction( OverrideThread )
