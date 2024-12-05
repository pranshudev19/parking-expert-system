from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

class ParkingExpertSystemWithUser:
    def __init__(self):
        # Parking block layout
        self.parking_blocks = {
            'block_1': {'type': 'motorcycle', 'status': 'free'},
            'block_2': {'type': 'car', 'status': 'free'},
            'block_3': {'type': 'truck', 'status': 'occupied'},
            'block_4': {'type': 'car', 'status': 'free'},
            'block_5': {'type': 'truck', 'status': 'free'},
            'block_6': {'type': 'motorcycle', 'status': 'occupied'},
        }
        self.assigned_blocks = {}
        self.reserved_blocks = {}
        self.fee_rate_per_hour = 10.0

    def infer_parking(self, vehicle_type):
        suitable_blocks = [block for block, info in self.parking_blocks.items() 
                           if info['type'] == vehicle_type and info['status'] == 'free']
        return suitable_blocks

    def suggest_parking(self, user_name, vehicle_type):
        suitable_blocks = self.infer_parking(vehicle_type)
        if suitable_blocks:
            block_choice = suitable_blocks[0]
            self.parking_blocks[block_choice]['status'] = 'occupied'
            entry_time = datetime.now()
            self.assigned_blocks[user_name] = {'block': block_choice, 'vehicle_type': vehicle_type, 'entry_time': entry_time}
            return f"{user_name}'s {vehicle_type} has been parked in {block_choice} at {entry_time}."
        else:
            return f"No free parking blocks available for {vehicle_type}."

    def free_parking(self, user_name):
        if user_name in self.assigned_blocks:
            block_info = self.assigned_blocks[user_name]
            block_to_free = block_info['block']
            vehicle_type = block_info['vehicle_type']
            entry_time = block_info['entry_time']
            exit_time = datetime.now()
            duration_hours = (exit_time - entry_time).total_seconds() / 3600
            total_fee = round(self.fee_rate_per_hour * duration_hours, 2)
            self.parking_blocks[block_to_free]['status'] = 'free'
            del self.assigned_blocks[user_name]
            return f"{user_name}'s {vehicle_type} has left {block_to_free}. Total Fee: Rs.{total_fee}"
        else:
            return f"No vehicle found for user: {user_name}"

    def reserve_block(self, block, user_name):
        if self.parking_blocks[block]['status'] == 'free':
            self.parking_blocks[block]['status'] = 'reserved'
            self.reserved_blocks[user_name] = block
            return f"Block {block} reserved successfully by {user_name}."
        else:
            return f"Block {block} is not available for reservation."

expert_system = ParkingExpertSystemWithUser()

# Index Page
@app.route('/')
def index():
    return render_template('index.html')

# Reserve Page (Grid of Parking Blocks)
@app.route('/reserve')
def reserve():
    blocks = expert_system.parking_blocks
    return render_template('grid.html', blocks=blocks, selected_block=None)

# Select a Parking Block to Reserve
@app.route('/select_block', methods=['POST'])
def select_block():
    block = request.form['block']
    user_name = "User"  # You can modify this to get actual user input
    message = expert_system.reserve_block(block, user_name)
    return render_template('result.html', message=message)

# Park a Vehicle
@app.route('/park', methods=['POST'])
def park_vehicle():
    user_name = request.form['name'].capitalize()
    vehicle_type = request.form['vehicle'].lower()
    message = expert_system.suggest_parking(user_name, vehicle_type)
    return render_template('result.html', message=message)

# Exit a Vehicle
@app.route('/exit', methods=['POST'])
def exit_vehicle():
    user_name = request.form['exit_name'].capitalize()
    message = expert_system.free_parking(user_name)
    return render_template('result.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
