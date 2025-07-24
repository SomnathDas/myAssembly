import subprocess
import os
import signal
import time
import sys # Import sys to check OS

def kill_newest_process_by_name_no_library(process_name_pattern):
    """
    Finds and kills the newest process whose command line matches the given pattern
    without using external libraries like psutil.

    This method is platform-specific and less robust than using psutil.

    Args:
        process_name_pattern (str): The pattern to match against the process's
                                     command line (e.g., "./babyrop_level14.0").
    Returns:
        bool: True if a process was found and killed, False otherwise.
    """
    if sys.platform.startswith('win'):
        print("This function is currently implemented for Linux/macOS only.")
        print("On Windows, you would typically use 'tasklist' and 'taskkill'.")
        return False
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        try:
            # Execute 'ps aux' to list all processes
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, check=True)
            lines = result.stdout.splitlines()

            matching_processes = []
            # Skip header line
            for line in lines[1:]:
                parts = line.split(None, 10)

                if len(parts) < 11:
                    continue

                pid = int(parts[1])
                command = parts[10]

                if process_name_pattern in command:
                    # Relying on PID as a rough proxy for "newest" (higher PID usually means newer)
                    matching_processes.append({'pid': pid, 'command': command})

            if not matching_processes:
                print(f"No process found matching '{process_name_pattern}'.")
                return False

            # Sort by PID in descending order to find the "newest" (highest PID)
            matching_processes.sort(key=lambda x: x['pid'], reverse=True)
            newest_process = matching_processes[0]

            print(f"Found newest process matching '{process_name_pattern}':")
            print(f"  PID: {newest_process['pid']}")
            print(f"  Command Line: {newest_process['command']}")

            try:
                # Attempt graceful termination (SIGTERM)
                print(f"Attempting to terminate PID {newest_process['pid']} gracefully...")
                os.kill(newest_process['pid'], signal.SIGTERM)

                time.sleep(2) # Give it a moment to terminate

                try:
                    os.kill(newest_process['pid'], 0) # Signal 0 checks if the process exists
                    print(f"Process PID {newest_process['pid']} did not terminate gracefully. Killing forcefully (SIGKILL)...")
                    os.kill(newest_process['pid'], signal.SIGKILL)
                    time.sleep(1)
                    try:
                        os.kill(newest_process['pid'], 0)
                        print(f"Failed to kill process PID {newest_process['pid']}.")
                        return False
                    except OSError:
                        print(f"Successfully killed process PID {newest_process['pid']}.")
                        return True
                except OSError:
                    print(f"Successfully terminated process PID {newest_process['pid']}.")
                    return True

            except OSError as e:
                if e.errno == 3: # ESRCH (No such process)
                    print(f"Process PID {newest_process['pid']} already gone.")
                    return True
                else:
                    print(f"Error sending signal to process PID {newest_process['pid']}: {e}")
                    return False

        except subprocess.CalledProcessError as e:
            print(f"Error running 'ps aux' command: {e}")
            print(f"Stderr: {e.stderr}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
    else:
        print(f"Unsupported operating system: {sys.platform}")
        return False

# The __name__ == "__main__" block is for code that should only run when this file is executed directly.
# It will NOT run when this file is imported as a module.
if __name__ == "__main__":
    print("This file is being run directly.")
    # You can add test calls here if you want to test the function directly
    # target_process_name = "sleep 1000"
    # if kill_newest_process_by_name_no_library(target_process_name):
    #     print("Test operation completed successfully.")
    # else:
    #     print("Test operation failed or no matching process was found.")
