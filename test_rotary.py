import rotary_encoder

A_PIN = 5  # use wiring pin numbers here
B_PIN = 4
encoder = rotary_encoder.RotaryEncoder(A_PIN, B_PIN)

while 1:
  delta = encoder.get_delta() # returns 0,1,or -1
  if delta!=0:
    print delta
