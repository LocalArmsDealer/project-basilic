# Copyright (C) 2024 Alina
# Project Basilic uses the GNU Public License (GPLv3). Details are available in the LICENSE file contained in the "Project Basilic" folder.

import d_ctrl
import logging

def main():
    """Main function. Starts Project Basilic."""
    print("""
            Project Basilic  Copyright (C) 2024 Alina
            This program comes with ABSOLUTELY NO WARRANTY; for details, check the LICENSE file.
            This is free software, and you are welcome to redistribute it under certain conditions specified in the LICENSE file.
          """)
    print()
    print("Input JavaScript code to send to a connected drone, or type 'exit' to quit Project Basilic.")

    while True:
        try:
            js_input = input("Enter code to send to the drone (or 'exit' to quit): ")

            if js_input.lower() == "exit":
                print("Exiting Project Basilic...")
                break

            response = d_ctrl.send_command(js_input)
            print(f"Drone response {response} received.")
        
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")
            d_ctrl.send_command("land()")
            break

        except Exception as e:
            logging.error(f"Error: {e}")
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
