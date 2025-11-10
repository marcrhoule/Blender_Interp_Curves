"""
Interpolation Functions Library
All 140+ interpolation functions in one place
Edit this file to add new functions!

Functions ending with ↺ return to the start value (0→peak→0 curves)
"""

import math

# Simple noise function for organic effects
def noise(t):
    """Simple pseudo-random noise based on sine"""
    return math.sin(t * 12.9898) * 0.5 + 0.5

# Helper functions that are reused
def ease_in_quad(t): 
    return t**2

def ease_out_quad(t): 
    return 1 - (1 - t)**2

def ease_in_cubic(t): 
    return t**3

def ease_out_sine(t): 
    return math.sin((t*math.pi)/2)

def bounce_out(t):
    n1, d1 = 7.5625, 2.75
    if t < 1/d1: 
        return n1*t*t
    elif t < 2/d1: 
        return n1*(t-1.5/d1)**2 + 0.75
    elif t < 2.5/d1: 
        return n1*(t-2.25/d1)**2 + 0.9375
    else: 
        return n1*(t-2.625/d1)**2 + 0.984375

def elastic_out(t): 
    return 2**(-10*t)*math.sin((t*10 - 0.75)*2*math.pi/3)+1

def smoothstep(t): 
    return 3*t**2 - 2*t**3

# All interpolation functions organized by category
INTERPOLATION_FUNCTIONS = {
    # === SMOOTH & CLASSIC (15) ===
    "Linear": lambda t: t,
    "Ease In Quad": lambda t: t**2,
    "Ease Out Quad": lambda t: 1 - (1 - t)**2,
    "Ease InOut Quad": lambda t: 2*t*t if t<0.5 else 1-((-2*t+2)**2)/2,
    "Ease In Cubic": lambda t: t**3,
    "Ease Out Cubic": lambda t: 1 - (1 - t)**3,
    "Ease InOut Cubic": lambda t: 4*t**3 if t<0.5 else 1-((-2*t+2)**3)/2,
    "Ease In Quart": lambda t: t**4,
    "Ease Out Quart": lambda t: 1 - (1 - t)**4,
    "Ease InOut Quart": lambda t: 8*t**4 if t<0.5 else 1-((-2*t+2)**4)/2,
    "Ease In Sine": lambda t: 1 - math.cos((t*math.pi)/2),
    "Ease Out Sine": lambda t: math.sin((t*math.pi)/2),
    "Ease InOut Sine": lambda t: -(math.cos(math.pi*t)-1)/2,
    "Smoothstep": lambda t: 3*t**2 - 2*t**3,
    "Smoother Step": lambda t: t**3 * (t * (t * 6 - 15) + 10),
    
    # === ELASTIC & SPRINGY (12) ===
    "Elastic Out": lambda t: 2**(-10*t)*math.sin((t*10 - 0.75)*2*math.pi/3)+1,
    "Elastic In": lambda t: -2**(10*(t-1))*math.sin((t*10 - 10.75)*2*math.pi/3),
    "Elastic InOut": lambda t: (-2**(10*(2*t-1))*math.sin((20*t-11.125)*math.pi/3))/2 if t<0.5 else (2**(-10*(2*t-1))*math.sin((20*t-11.125)*math.pi/3))/2+1,
    "Rubberband": lambda t: 1 - math.cos(t*math.pi/2)*math.exp(-t*5),
    "Spring Damped": lambda t: 1 - math.exp(-6*t)*math.cos(12*math.pi*t),
    "Underdamped Spring": lambda t: 1 - math.exp(-3*t)*(math.cos(10*math.pi*t)+0.5*math.sin(10*math.pi*t)),
    "Jelly Wobble": lambda t: math.sin(t**2*10*math.pi)*math.exp(-5*t)*(1-t) + t,
    "Twang": lambda t: (1-t)**2 * math.sin(t*20*math.pi) * 0.3 + t,
    "Vibrato": lambda t: t + 0.1*math.sin(50*math.pi*t)*math.exp(-8*t),
    "String Pluck ↺": lambda t: math.sin(math.pi*t)*math.exp(-4*t**0.5),
    "Suspension": lambda t: t - 0.15*math.sin(2*math.pi*t)*math.exp(-3*t),
    "Springboard": lambda t: 1 - (1-t)*math.cos(15*math.pi*t)*math.exp(-5*t),
    
    # === BOUNCY & OVERSHOOT (12) ===
    "Back Out": lambda t: 1 + 2.70158*(t-1)**3 + 1.70158*(t-1)**2,
    "Bounce Out": bounce_out,
    "Overshoot": lambda t: t**3 - t*math.sin(t*math.pi),
    "Recoil": lambda t: 1 - math.exp(-6*t)*math.cos(8*math.pi*t),
    "Basketball Bounce ↺": lambda t: abs(math.sin(t*math.pi*4))*(1-t)**1.5,
    "Trampolining ↺": lambda t: abs(math.sin(t*math.pi*2.5))*math.exp(-t*2),
    "Pogo Stick": lambda t: 1 - abs(math.cos(t*math.pi*3))*(1-t)**2,
    "Boing": lambda t: 1 - (1-t)**2 * abs(math.cos(t*math.pi*7)),
    "Rubber Ball": lambda t: t + abs(math.sin(t*math.pi*6))*(1-t)**2*0.5,
    "Yo-Yo": lambda t: t - 0.5*math.sin(t*math.pi*4)*(1-t),
    "Slingshot": lambda t: t**2 * (3 - 2*t) + math.sin(t*math.pi*2)*0.1*(1-t),
    "Catapult": lambda t: t if t<0.7 else 0.7 + (t-0.7)*10 - 2*(t-0.7)**2,
    
    # === EXPONENTIAL & POWER (10) ===
    "Ease In Expo": lambda t: 0 if t==0 else 2**(10*(t-1)),
    "Ease Out Expo": lambda t: 1 if t==1 else 1 - 2**(-10*t),
    "Ease InOut Expo": lambda t: (2**(20*t-10))/2 if t<0.5 else (2-2**(-20*t+10))/2,
    "Ease In Circ": lambda t: 1 - math.sqrt(1 - t**2),
    "Ease Out Circ": lambda t: math.sqrt(1 - (t-1)**2),
    "Ease InOut Circ": lambda t: (1 - math.sqrt(1 - (2*t)**2))/2 if t<0.5 else (math.sqrt(1 - (-2*t+2)**2)+1)/2,
    "Rocket Launch": lambda t: t**3 * math.exp(t*2),
    "Parachute": lambda t: 1 - math.exp(-t*5),
    "Gravity Fall": lambda t: 1 - (1-t)**2,
    "Terminal Velocity": lambda t: 1 - math.exp(-t*3),
    
    # === RHYTHMIC & WAVES (12) ===
    "Sine Wave ↺": lambda t: 0.5*(1 - math.cos(2*math.pi*t)),
    "Pulse ↺": lambda t: math.sin(8*math.pi*t)**2,
    "Heartbeat ↺": lambda t: abs(math.sin(t*math.pi*2))**8 * (1 + math.sin(t*math.pi*4)*0.3),
    "Breath ↺": lambda t: (math.sin(t*math.pi*2) + 1) / 2,
    "Wave Crash": lambda t: math.sin(t*math.pi*0.5)**2 + 0.3*abs(math.sin(t*math.pi*8))*(1-t),
    "Ripple": lambda t: t + math.sin(t*math.pi*8)*0.1*(1-t),
    "Oscillate": lambda t: t + 0.1*math.sin(8*math.pi*t),
    "Flutter": lambda t: t + math.sin(t*math.pi*20)*0.05*math.sin(t*math.pi),
    "Shimmer": lambda t: t + math.sin(t*math.pi*15)*0.03*(math.sin(t*math.pi*3)+1),
    "Tremolo": lambda t: t * (1 + 0.1*math.sin(t*math.pi*30)),
    "Warble": lambda t: t + 0.08*math.sin(t**2*50),
    "Gallop": lambda t: t + 0.15*abs(math.sin(t*math.pi*3))*math.sin(t*math.pi*9),
    
    # === ORGANIC & NATURAL (10) ===
    "Leaf Fall": lambda t: t + 0.1*math.sin(t*math.pi*3)*math.cos(t*math.pi*5),
    "Butterfly": lambda t: t + 0.15*math.sin(t*math.pi*6)*math.sin(t*math.pi*2),
    "Seaweed Sway": lambda t: t + 0.1*math.sin(t*math.pi*2)*math.cos(t*math.pi*1.3),
    "Bird Hop": lambda t: t + abs(math.sin(t*math.pi*4))*0.2*(1-abs(2*t-1)),
    "Fish Swim": lambda t: t + 0.15*math.sin(t*math.pi*8)*math.exp(-t*2),
    "Snake Slither": lambda t: t + 0.1*math.sin(t*math.pi*10)*math.sin(t*math.pi*3),
    "Jellyfish": lambda t: t + 0.2*math.sin(t*math.pi*4)**2*math.cos(t*math.pi*2),
    "Muscle Twitch": lambda t: t + 0.1*abs(math.sin(t*math.pi*25))*math.exp(-t*8),
    "Growing Vine": lambda t: t**1.5 + 0.05*math.sin(t*math.pi*20)*(1-t),
    "Melting": lambda t: t**0.5 + (t**3)*0.5,
    
    # === GLITCHY & DIGITAL (10) ===
    "Stutter": lambda t: math.floor(t*10)/10,
    "Pixelate": lambda t: math.floor(t*20)/20,
    "Bit Crush": lambda t: round(t*8)/8,
    "Glitch": lambda t: t + 0.05*math.floor(10*t)/10,
    "Static": lambda t: t + (noise(t*50)-0.5)*0.1,
    "Screen Tear": lambda t: t if t<0.5 else 0.5 + (t-0.5)*1.2,
    "Lag Spike": lambda t: t*0.9 if t<0.8 else 0.72 + (t-0.8)*5,
    "Frame Drop": lambda t: t - 0.05*math.floor(t*15),
    "Digital Noise": lambda t: t + (math.sin(t*1000)**2 - 0.5)*0.05,
    "Packet Loss": lambda t: t * (1 + 0.1*math.floor(math.sin(t*50))),
    
    # === EXTREME & WILD (10) ===
    "Explosion": lambda t: t**5 * (10 - 9*t),
    "Implosion": lambda t: 1 - (1-t)**5 * (10 - 9*(1-t)),
    "Quantum Tunnel": lambda t: abs(math.sin(1/(t+0.01)))*0.3 + t*0.7,
    "Wormhole": lambda t: t + math.sin(50*t)*math.cos(30*t)*0.1*(1-abs(2*t-1)),
    "Black Hole": lambda t: 1 - math.exp(-t*5)*math.cos(t*20*math.pi),
    "Time Warp": lambda t: t + 0.3*math.sin(t*math.pi)*math.sin(1/(t+0.1)),
    "Chaos Theory": lambda t: t + math.sin(10*t)*math.cos(7*t)*math.sin(13*t)*0.1,
    "Fractal": lambda t: t + 0.05*math.sin(t) + 0.025*math.sin(2*t) + 0.0125*math.sin(4*t),
    "Lightning": lambda t: t + abs(noise(t*20)-0.5)*0.3*math.exp(-t*5),
    "Earthquake": lambda t: t + (noise(t*15)-0.5)*0.15*abs(math.sin(t*math.pi*3)),
    
    # === MECHANICAL & ROBOTIC (9) ===
    "Gear Turn": lambda t: math.floor(t*8)/8 + (t*8 - math.floor(t*8))**2 * 0.125,
    "Piston": lambda t: (math.floor(t*4)/4 + smoothstep((t*4)%1)*0.25),
    "Ratchet": lambda t: t + abs(math.sin(t*math.pi*10))*0.05 if t%0.1<0.05 else t,
    "Conveyor Belt": lambda t: t + 0.02*math.sin(t*math.pi*20),
    "Pneumatic": lambda t: smoothstep(t) + 0.1*math.exp(-t*10)*math.sin(t*50*math.pi),
    "Hydraulic": lambda t: t**2 * (3-2*t) * (1 + 0.05*math.sin(t*math.pi*15)),
    "Motor Spin-Up": lambda t: 1 - math.exp(-t*5) * (1 + 0.1*math.sin(t*30*math.pi)),
    "Clutch Engage": lambda t: 0 if t<0.3 else (t-0.3)/0.7,
    "Brake": lambda t: t if t<0.7 else 0.7 + (t-0.7)*0.3,
    
    # === COMPLEX STORIES (40) ===
    "Balloon Rise Fall ↺": lambda t: math.sin(t*math.pi*0.5)**2 * (1 + 0.1*math.sin(t*math.pi*4)) if t<0.8 else (1-(t-0.8)*5)**2 if (1-(t-0.8)*5)>0 else 0,
    "Rocket Launch Crash ↺": lambda t: t**2*3 if t<0.6 else 1.8 - (t-0.6)**2*11,
    "Jump and Land ↺": lambda t: (-4*(t-0.5)**2 + 1) * 1.2 if t>0 else 0,
    "Throw and Catch ↺": lambda t: (-16*(t-0.5)**2 + 4) * 0.25 + 0.05*math.sin(t*math.pi*15)*(1-abs(2*t-1)),
    "Toss Up Drop ↺": lambda t: t*2 if t<0.5 else 2*(1-t),
    "Peak and Plummet ↺": lambda t: smoothstep(t*2) if t<0.5 else 1-(t-0.5)*2,
    "Climb and Slide ↺": lambda t: t**0.5 if t<0.7 else 0.7**0.5 * (1-(t-0.7)*3),
    "Inflate Deflate ↺": lambda t: math.sin(t*math.pi)**2,
    "Swell and Pop ↺": lambda t: (1-math.cos(t*math.pi*1.2))/2 if t<0.8 else 0.1*math.exp(-(t-0.8)*20),
    "Rise Hover Fall ↺": lambda t: smoothstep(t*2.5) if t<0.4 else (1 if t<0.7 else 1-(t-0.7)**2*10),
    "Ocean Wave ↺": lambda t: 0.5*math.sin(t*math.pi*2) + 0.3*math.sin(t*math.pi*5) + 0.5,
    "Tide In Out ↺": lambda t: 0.5 - 0.5*math.cos(t*math.pi*2) + 0.1*math.sin(t*math.pi*8),
    "Breathing Cycle ↺": lambda t: 0.4 + 0.4*math.sin(t*math.pi*2) + 0.2*math.sin(t*math.pi*4),
    "Circadian Rhythm ↺": lambda t: 0.5 + 0.5*math.sin(t*math.pi*2 - math.pi/2) + 0.1*noise(t*3),
    "Seasons Cycle ↺": lambda t: 0.5 - 0.5*math.cos(t*math.pi*2) + 0.15*math.sin(t*math.pi*8),
    "Day Night ↺": lambda t: 0.5 + 0.5*math.sin(t*math.pi*2) if t<0.5 else 0.5 - 0.5*math.sin((t-0.5)*math.pi*2),
    "Lunar Cycle ↺": lambda t: abs(math.sin(t*math.pi)) * (1 + 0.1*noise(t*10)),
    "Pulse Wave ↺": lambda t: 1 if (t*8)%1 < 0.3 else 0.2,
    "Wind Up Release": lambda t: t**4 if t<0.7 else 1 + (t-0.7)**2*3,
    "Charge Discharge": lambda t: t**3 if t<0.6 else 1 - (t-0.6)**0.5,
    "Tension Snap": lambda t: t*0.2 if t<0.8 else 0.16 + (t-0.8)*4,
    "Compress Explode ↺": lambda t: -t**2*0.3 if t<0.5 else (t-0.5)**2*4,
    "Inhale Exhale ↺": lambda t: smoothstep(t*2) if t<0.5 else smoothstep(2-t*2),
    "Squeeze Release ↺": lambda t: 1-t if t<0.5 else (t-0.5)*2,
    "Build Crescendo": lambda t: (t**2 if t<0.7 else 0.49 + (t-0.7)**3*5),
    "Anticipation Strike": lambda t: -0.2*(1-t)**2 if t<0.3 else ((t-0.3)/0.7)**2,
    "Recoil Forward": lambda t: -0.3*smoothstep((1-t)*2) if t<0.2 else ((t-0.2)/0.8),
    "Flower Bloom": lambda t: (t**0.5) * (1 + 0.05*math.sin(t*math.pi*10)),
    "Seed Sprout": lambda t: 0 if t<0.2 else ((t-0.2)/0.8)**2,
    "Tree Sway ↺": lambda t: 0.5 + 0.5*math.sin(t*math.pi*3) * math.cos(t*math.pi*1.7),
    "Butterfly Flutter": lambda t: 0.5 + 0.5*math.sin(t*math.pi*8) + 0.2*abs(math.sin(t*math.pi*2)),
    "Bird Take Off": lambda t: (1-math.exp(-t*5)) * (1 + 0.3*abs(math.sin(t*math.pi*15))),
    "Firefly Blink ↺": lambda t: math.exp(-((t*10-5)**2)/2) + 0.3*math.exp(-((t*10-2)**2)/1),
    "Spider Drop ↺": lambda t: 0 if t<0.3 else smoothstep((t-0.3)*2.5) if t<0.6 else (0.75 - (t-0.6)*math.sin((t-0.6)*40)),
    "Frog Jump ↺": lambda t: (-4*(t-0.3)**2 + 0.36)*5 if 0.2<t<0.5 else 0,
    "Joy to Sad": lambda t: 1 - t**2,
    "Surprise Shock ↺": lambda t: 0 if t<0.3 else (math.exp(-(t-0.3)*10) if t<0.5 else 0.5*math.exp(-(t-0.5)*3)),
    "Anticipation Peak": lambda t: t**3*2 if t<0.5 else 2 - (1-t)**2*2,
    "Calm to Panic": lambda t: t + (t**2)*2 + abs(math.sin(t*math.pi*20))*t**2,
    "Meditation Wave ↺": lambda t: 0.5 + 0.3*math.sin(t*math.pi*2) * math.exp(-t*0.5),
    "Laughter Fit": lambda t: abs(math.sin(t*math.pi*12)) * (1-math.exp(-t*3)),
}

# Category definitions for color coding and organization
CATEGORIES = {
    "SMOOTH & CLASSIC": ["Linear", "Ease In Quad", "Ease Out Quad", "Ease InOut Quad", "Ease In Cubic", 
                 "Ease Out Cubic", "Ease InOut Cubic", "Ease In Quart", "Ease Out Quart", 
                 "Ease InOut Quart", "Ease In Sine", "Ease Out Sine", "Ease InOut Sine", 
                 "Smoothstep", "Smoother Step"],
    "ELASTIC & SPRINGY": ["Elastic Out", "Elastic In", "Elastic InOut", "Rubberband", "Spring Damped",
                 "Underdamped Spring", "Jelly Wobble", "Twang", "Vibrato", "String Pluck ↺",
                 "Suspension", "Springboard"],
    "BOUNCY & OVERSHOOT": ["Back Out", "Bounce Out", "Overshoot", "Recoil", "Basketball Bounce ↺",
                 "Trampolining ↺", "Pogo Stick", "Boing", "Rubber Ball", "Yo-Yo",
                 "Slingshot", "Catapult"],
    "EXPONENTIAL & POWER": ["Ease In Expo", "Ease Out Expo", "Ease InOut Expo", "Ease In Circ",
                 "Ease Out Circ", "Ease InOut Circ", "Rocket Launch", "Parachute",
                 "Gravity Fall", "Terminal Velocity"],
    "RHYTHMIC & WAVES": ["Sine Wave ↺", "Pulse ↺", "Heartbeat ↺", "Breath ↺", "Wave Crash", "Ripple",
                 "Oscillate", "Flutter", "Shimmer", "Tremolo", "Warble", "Gallop"],
    "ORGANIC & NATURAL": ["Leaf Fall", "Butterfly", "Seaweed Sway", "Bird Hop", "Fish Swim",
                 "Snake Slither", "Jellyfish", "Muscle Twitch", "Growing Vine", "Melting"],
    "GLITCHY & DIGITAL": ["Stutter", "Pixelate", "Bit Crush", "Glitch", "Static",
                 "Screen Tear", "Lag Spike", "Frame Drop", "Digital Noise", "Packet Loss"],
    "EXTREME & WILD": ["Explosion", "Implosion", "Quantum Tunnel", "Wormhole", "Black Hole",
                 "Time Warp", "Chaos Theory", "Fractal", "Lightning", "Earthquake"],
    "MECHANICAL & ROBOTIC": ["Gear Turn", "Piston", "Ratchet", "Conveyor Belt", "Pneumatic",
                 "Hydraulic", "Motor Spin-Up", "Clutch Engage", "Brake"],
    "COMPLEX STORIES": ["Balloon Rise Fall ↺", "Rocket Launch Crash ↺", "Jump and Land ↺", "Throw and Catch ↺", 
                 "Toss Up Drop ↺", "Peak and Plummet ↺", "Climb and Slide ↺", "Inflate Deflate ↺", 
                 "Swell and Pop ↺", "Rise Hover Fall ↺",
                 "Ocean Wave ↺", "Tide In Out ↺", "Breathing Cycle ↺", "Circadian Rhythm ↺", 
                 "Seasons Cycle ↺", "Day Night ↺", "Lunar Cycle ↺", "Pulse Wave ↺",
                 "Wind Up Release", "Charge Discharge", "Tension Snap", "Compress Explode ↺",
                 "Inhale Exhale ↺", "Squeeze Release ↺", "Build Crescendo", "Anticipation Strike",
                 "Recoil Forward",
                 "Flower Bloom", "Seed Sprout", "Tree Sway ↺", "Butterfly Flutter",
                 "Bird Take Off", "Firefly Blink ↺", "Spider Drop ↺", "Frog Jump ↺",
                 "Joy to Sad", "Surprise Shock ↺", "Anticipation Peak", "Calm to Panic",
                 "Meditation Wave ↺", "Laughter Fit"],
}
