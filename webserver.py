from flask import Flask, jsonify, render_template
from flask_cors import CORS
from gpiozero import DistanceSensor, PWMLED
from threading import Thread
from time import sleep

app = Flask(__name__)
CORS(app)

sensor = DistanceSensor(echo=24, trigger=23)
led = PWMLED(17)
distance = 0
brightness = 0

def update_distance():
    global distance, brightness
    while True:
        distance = round(sensor.distance * 100, 2)
        brightness = adjust_led_brightness(distance, brightness)
        sleep(1)

def adjust_led_brightness(distance, brightness):
    if distance < 5:
        brightness = 0
    elif distance < 10:
        brightness = 0.2
    elif distance < 15:
        brightness = 0.4
    elif distance < 20:
        brightness = 0.6
    elif distance < 25:
        brightness = 0.8
    led.value = brightness
    return brightness

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_distance_value', methods=['GET'])
def get_distance_value():
    return jsonify(distance=distance, brightness=brightness)

if __name__ == '__main__':
    thread = Thread(target=update_distance)
    thread.daemon = True
    thread.start()
    
    app.run(host='0.0.0.0', port=80, debug=False)
