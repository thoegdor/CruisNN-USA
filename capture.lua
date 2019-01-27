map_address = 0x04714C -- reads progress of the map

function read_progress()
  return mainmemory.readfloat(map_address, true)
end

state = 0
end_state = 2400000
test_state = 500000
recording_frame = 1
skip_frames = 44

--testing
ruN = "run_54"

dir = "" --update
os.execute("mkdir "..dir..ruN)

local steering_file = io.open()

local save_state_file = ""

-- start game
savestate.load(save_state_file)

while state < end_state do  
	
	for f=1,skip_frames do
		
		joypad.set({["P1 Z"] = true})
		emu.frameadvance()
		
	end 
	
	-- start cap --
	--client.screenshot()
	  
	steering_value = joypad.get()["P1 X Axis"]
	steering_file:write(steering_value .. '\n')
	-- end cap --
	
	-- start again -- 
	recording_frame = recording_frame + 1
	state = read_progress()

end

steering_file:close()
