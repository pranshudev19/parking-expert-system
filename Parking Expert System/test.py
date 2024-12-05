from datetime import datetime

class ParkingExpertSystemWithUser:
    def __init__(self):
        # Knowledge Base: The parking blocks layout
        self.parking_blocks = {
            'block_1': {'type': 'motorcycle', 'status': 'free'},
            'block_2': {'type': 'car', 'status': 'free'},
            'block_3': {'type': 'truck', 'status': 'occupied'},
            'block_4': {'type': 'car', 'status': 'free'},
            'block_5': {'type': 'truck', 'status': 'free'},
            'block_6': {'type': 'motorcycle', 'status': 'occupied'},
        }
        # Store assigned blocks with user name, vehicle type, and entry time
        self.assigned_blocks = {}
        # Parking fee rate per hour
        self.fee_rate_per_hour = 10.0

    # Inference Engine: Infers suitable parking blocks based on the vehicle type
    def infer_parking(self, vehicle_type):
        suitable_blocks = [block for block, info in self.parking_blocks.items() 
                           if info['type'] == vehicle_type and info['status'] == 'free']
        return suitable_blocks

    # Forward Chaining: Applies inference rules to find and assign parking
    def suggest_parking(self, user_name, vehicle_type):
        suitable_blocks = self.infer_parking(vehicle_type)
        
        # If there are free blocks, assign the first one
        if suitable_blocks:
            block_choice = suitable_blocks[0]  # Automatically select first free block
            self.parking_blocks[block_choice]['status'] = 'occupied'
            entry_time = datetime.now()  # Record the time the vehicle is parked
            self.assigned_blocks[user_name] = {'block': block_choice, 'vehicle_type': vehicle_type, 'entry_time': entry_time}
            print(f"{user_name}'s {vehicle_type} has been parked in {block_choice} at {entry_time}.")
            self.explain_reasoning(block_choice, vehicle_type)  # Explain decision
        else:
            print(f"No free parking blocks available for {vehicle_type}.")

    # Explanation Module: Explains why a block was chosen
    def explain_reasoning(self, block, vehicle_type):
        print(f"Block {block} was chosen because it is free and suitable for a {vehicle_type}.")

    # Free a parking block when a user exits and calculate the fee
    def free_parking(self, user_name):
        if user_name in self.assigned_blocks:
            block_info = self.assigned_blocks[user_name]
            block_to_free = block_info['block']
            vehicle_type = block_info['vehicle_type']
            entry_time = block_info['entry_time']
            exit_time = datetime.now()  # Record the time the vehicle exits
            duration_hours = (exit_time - entry_time).total_seconds() / 3600  # Convert to hours
            total_fee = round(self.fee_rate_per_hour * duration_hours, 2)  # Calculate the fee
            
            # Update the block status to free
            self.parking_blocks[block_to_free]['status'] = 'free'
            print(f"{user_name}'s {vehicle_type} has left {block_to_free}. The block is now free.")
            print(f"Parking Duration: {duration_hours:.2f} hours")
            print(f"Total Fee: Rs.{total_fee}")
            
            # Remove the user from the assigned blocks
            del self.assigned_blocks[user_name]
        else:
            print(f"No vehicle found for user: {user_name}")

# Main program loop for interacting with the expert system
expert_system = ParkingExpertSystemWithUser()

# Sample Interaction: Park vehicles, exit, and calculate parking fees
while True:
    action = input("Enter 'park' to park a vehicle, 'exit' to exit a vehicle, or 'quit' to quit: ").lower()
    
    if action == 'park':
        user_name = input("Enter your name: ").capitalize()
        vehicle_type = input("Enter vehicle type (motorcycle, car, truck): ").lower()
        if vehicle_type in ['motorcycle', 'car', 'truck']:
            expert_system.suggest_parking(user_name, vehicle_type)
        else:
            print("Invalid vehicle type entered.")
    
    elif action == 'exit':
        user_name = input("Enter your name: ").capitalize()
        expert_system.free_parking(user_name)
    
    elif action == 'quit':
        break
    
    else:
        print("Invalid action entered.")
