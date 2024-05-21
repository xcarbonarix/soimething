from flask import Flask, request, jsonify
import serial
import time
import atexit

# Initialize Flask app
app = Flask(__name__)

# Setup serial connection to Arduino
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Wait for the serial connection to initialize

# Define the send_command function
def send_command(command):
    ser.write(f"{command}\n".encode())
    time.sleep(1)  # Adjust the delay as needed

# Ensure the serial connection is closed properly when the script ends
atexit.register(lambda: ser.close())

@app.route('/disease', methods=['POST'])
def receive_disease():
    data = request.get_json()
    disease = data.get('disease')
    if not disease:
        return jsonify({"error": "No disease provided"}), 400
    
    # Use the disease data to call the send_command function
    try:
        send_command(disease)
        print(f"Received disease: {disease}")
        return jsonify({"message": f"Disease {disease} received successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
