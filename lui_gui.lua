function draw_info()
	dir = "" --update
	gui.drawImage(dir,100,100,100,100)
	gui.drawEllipse(100,100,50,50)--main circle
	smaller circle
end

BOX_CENTER_X, BOX_CENTER_Y = 160, 215
BOX_WIDTH, BOX_HEIGHT = 100, 4
SLIDER_WIDTH, SLIDER_HIEGHT = 4, 16

--function draw_info()

--  gui.drawBox(BOX_CENTER_X - BOX_WIDTH / 2, BOX_CENTER_Y - BOX_HEIGHT / 2,
              --BOX_CENTER_X + BOX_WIDTH / 2, BOX_CENTER_Y + BOX_HEIGHT / 2,
              --none, 0x60FFFFFF)
 -- gui.drawBox(BOX_CENTER_X + 1*(BOX_WIDTH / 2) - SLIDER_WIDTH / 2, BOX_CENTER_Y - SLIDER_HIEGHT / 2,
--              BOX_CENTER_X + 1*(BOX_WIDTH / 2) + SLIDER_WIDTH / 2, BOX_CENTER_Y + SLIDER_HIEGHT / 2,
---              none, 0xFFFF0000)
--end


state = 0
end_state = 2400000

local save_state_file = "" --update

-- start game
savestate.load(save_state_file)

while state < end_state do  
	
	for f=1,500 do
		
		draw_info()
		joypad.set({["P1 Z"] = true})
		emu.frameadvance()
		
	end 
	
	state = state+1

end


