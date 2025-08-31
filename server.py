from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from rpi5_ws2812.ws2812 import Color, WS2812SpiDriver
import time
import random
import assets

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
BACKGROUD_COLOR = Color(0,0,0)
LED_COUNT = 64  
BRIGHTNESS = 0.015
position = [Point(0,0)]
cookie = Point(0,0)
score = 0
strip = WS2812SpiDriver(spi_bus=0, spi_device=0, led_count=LED_COUNT).get_strip()

def reset(): 
    global position, score
    position = [Point(0,0)]
    score = 0

def isIllegal():
    for i in range(len(position)):
        for ii in range(len(position)):
            if i != ii:
                if position[i].x == position[ii].x and position[i].y == position[ii].y:
                    return True
    return False

def set_pixel(x, y, color):
    if ((y % 2) == 0) :
        index = (7 - y) * 8 + (7 - x)  
    else :
        index = (7 - y) * 8 + x
    strip.set_pixel_color(index, color)
    strip.set_brightness(BRIGHTNESS)
    strip.show()

def show_board():
    global position, cookie, score
    if isIllegal():
        assets.show_skull(set_pixel)
        time.sleep(5)
        reset()
        show_board()
        return 0

    if score == 63: 
        assets.show_trophy(set_pixel)
        time.sleep(5)
        reset()
        show_board()
        return 0

    used = [[True]*8 for _ in range(8)]

    used[cookie.y][cookie.x] = False
    set_pixel(cookie.x, cookie.y, Color(0,255,0))

    for i in range(score):
        used[position[-i - 1].y][position[-i - 1].x] = False
        set_pixel(position[-i - 1].x, position[-i - 1].y, Color(255,0,0))

    for i in range(8):
        for ii in range(8):
            if used[ii][i] == True:
                set_pixel(i, ii, BACKGROUD_COLOR)

def make_cookie():
    global position, cookie, score 
    score += 1

    if score == 63:
        return 0;

    flag = True

    while flag:
        cookie.x = random.randint(0,7)
        cookie.y = random.randint(0,7)
        flag = False

        for i in range(score):
            if position[-i - 1].x == cookie.x and position[-i - 1].y == cookie.y:
                flag = True

    set_pixel(cookie.x, cookie.y, Color(0,255,0))

def cookie_or_pop():
    if position[-1].x == cookie.x and position[-1].y == cookie.y:
        make_cookie()
    else :
        position.pop(0)
    show_board()

for i in range(8):
    for ii in range(8):
        set_pixel(i, ii, Color(0,0,0))

@app.get("/ON")
async def root():
    global position, cookie
    for i in range(8):
        for ii in range(8):
            set_pixel(i, ii, BACKGROUD_COLOR)
        time.sleep(0.100)        
    set_pixel(position[-1].x, position[-1].y, Color(255,0,0))
    make_cookie()
    return JSONResponse(content={"ok": True})

@app.get("/OFF")
async def root():
    global position,score
    for i in range(8):
        for ii in range(8):
            set_pixel(i, ii, Color(0,0,0))
        time.sleep(0.100)   
    reset()
    return JSONResponse(content={"ok": True})


@app.get("/up")
async def up():
    global position, score
    if position[-1].y != 0:
        position.append(Point(position[-1].x, position[-1].y - 1))
        cookie_or_pop()
    return JSONResponse(content={"ok": True})


@app.get("/down")
async def down():
    global position, score
    if position[-1].y != 7:
        position.append(Point(position[-1].x, position[-1].y + 1))
        cookie_or_pop()
    return JSONResponse(content={"ok": True})


@app.get("/left")
async def left():
    global position, score
    if position[-1].x != 0:
        position.append(Point(position[-1].x - 1, position[-1].y))
        cookie_or_pop()
    return JSONResponse(content={"ok": True})


@app.get("/right")
async def right():
    global position, score
    if position[-1].x != 7:
        position.append(Point(position[-1].x + 1, position[-1].y))
        cookie_or_pop()
    return JSONResponse(content={"ok": True})

@app.post("/set")
async def root(request: Request):
    reset()
    data = await request.json()
    for i in range(8):
        for ii in range(8):
            r, g, b = data[ii][i]
            set_pixel(i, ii, Color(r,g,b))
        time.sleep(0.100)
    return JSONResponse(content={"ok": True})