from xml.sax.saxutils import escape

player = None
b_g = None
walls =[]
start_time=None
key1=None
key2=None
key3=None
cover=None
escape_open=None
boy=None
mode=None


PIXEL_PER_METER = (10.0 / 0.5)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 9.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1.0