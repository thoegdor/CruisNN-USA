local use_clipboard = true -- Use the clipboard to send screenshots to the predict server.

local check_progress_every = 300 -- Check progress after this many frames to detect if we get stuck

local save_state_file = "C:\\Users\\unclebret\\Desktop\\deep_learning\\cruising_world_ai\\BizHawk-1.12.2\\N64\\State\\state_2.State"

-- start game
savestate.load(save_state_file)

local tcp = require("socket").tcp()
local success, error = tcp:connect('localhost', 36296)
if not success then
  print("Failed to connect to server:", error)
  return
end

client.setscreenshotosd(false)

client.screenshottoclipboard()

outgoing_message, outgoing_message_index = nil, nil

local receive_buffer = ""

function onexit()
  tcp:close()
end

--[[
BOX_CENTER_X, BOX_CENTER_Y = 160, 215
BOX_WIDTH, BOX_HEIGHT = 100, 4
SLIDER_WIDTH, SLIDER_HIEGHT = 4, 16
function draw_info()
  gui.drawBox(BOX_CENTER_X - BOX_WIDTH / 2, BOX_CENTER_Y - BOX_HEIGHT / 2,
              BOX_CENTER_X + BOX_WIDTH / 2, BOX_CENTER_Y + BOX_HEIGHT / 2,
              none, 0x60FFFFFF)
  gui.drawBox(BOX_CENTER_X + current_action*(BOX_WIDTH / 2) - SLIDER_WIDTH / 2, BOX_CENTER_Y - SLIDER_HIEGHT / 2,
              BOX_CENTER_X + current_action*(BOX_WIDTH / 2) + SLIDER_WIDTH / 2, BOX_CENTER_Y + SLIDER_HIEGHT / 2,
              none, 0xFFFF0000)
end
--]]

map_address = 0x04714C -- reads progress of the map

function read_progress()
  return mainmemory.readfloat(map_address, true)
end

local state = 0
local end_state = 2400000
local test_state = 500000
local recording_frame = 1
local skip_frames = 100
local action = 0

outgoing_message, outgoing_message_index = nil, nil

function request_prediction()
  
    client.screenshottoclipboard()
    outgoing_message = "PREDICTFROMCLIPBOARD\n"
	outgoing_message_index = 1
	
end

request_prediction()

while state < end_state do

	if outgoing_message ~= nil then
    local sent, error, last_byte = tcp:send(outgoing_message, outgoing_message_index)
    if sent ~= nil then
      outgoing_message = nil
      outgoing_message_index = nil
    else
      if error == "timeout" then
        outgoing_message_index = last_byte + 1
      else
        print("Send failed: ", error); break
      end
     end
	end
	
  local message, error
  message, error, receive_buffer = tcp:receive("*l", receive_buffer)
  print(message)
  --if message == nil then
  --  if error ~= "timeout" then
  --   print("Receive failed: ", error); break
  -- end
  --else
  --  action = tonumber(message)
    for i=1, 10 do
        joypad.setanalog({["P1 X Axis"] = action})
        --draw_info()
        emu.frameadvance()
      end
  --else
  --    print("Prediction error...")
  -- end
	
	-- need a state checker here
	--...
	
    request_prediction()
	state = read_progress()
end

--onexit()
--event.unregisterbyid(exit_guid)
