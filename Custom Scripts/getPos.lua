-- This script is intended to be mapped to the F7 hotkey when the client boots using hubstartup.txt.

LoadLibrary("LocalPlayer")
LoadLibrary("Person")

-- This script is intended for NPC creation, finding coordinates, or general debugging.
-- It serves no value to a normal end user.

function getPositionThread()
	
	while ( true ) do
	
		if ( Debug.KeyIsPressed( KEY_F3 ) ) then
			LocalPerson = LocalPlayer.GetPerson()
			print("Your position is: ", Person.GetPosition(LocalPerson))
		end
		
		Sleep( 0.0 )
		
	end
end

PositionMonitorThreadId = SpawnFunction( getPositionThread )
