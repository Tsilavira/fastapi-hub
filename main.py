import os
from datetime import datetime
from multiprocessing import Process
import subprocess

INST_FOLD = "instances"
BASE_PORT = 8000

def run_project(name, port):
    print(f"Starting project {name} on port {port}")
    
    log_file = f"log.txt"
    command = f"uvicorn main:app --port {port} --host 0.0.0.0" 

    current_directory = os.getcwd()
    target_directory = os.path.join(current_directory, 'instances', name)

    restart_attempts = 0
    max_attempts = 3


    while restart_attempts < max_attempts:

        os.chdir(target_directory)

        if not os.path.exists(log_file):
            with open(log_file, 'w') as file:
                file.write("Log file created.\n")
        
        with open(log_file, "a") as log_file:

            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            log_file.write(timestamp)
            log_file.write("\n")

            try:
                subprocess.run(command, shell=True, check=True, stdout=log_file, stderr=subprocess.STDOUT)
                print(f"Project {name} on port {port} ran successfully.")
                return
            except subprocess.CalledProcessError as e:
                print(f"Error running FastAPI {name}: {e}")
                print(f"Restarting project {name} on port {port}")
                restart_attempts += 1
            except Exception as e:
                print(f"An unexpected error occurred in {name}: {e}")
                print(f"Restarting project {name} on port {port}")
                restart_attempts += 1

        current_directory = os.getcwd()
        parent_directory = os.path.dirname(current_directory)
        os.chdir(parent_directory)

    print(f"Failed to start project {name} after {max_attempts} restart attempts.")
    return


def main():
    projects = [folder_name for folder_name in os.listdir(INST_FOLD) if os.path.isdir(os.path.join(INST_FOLD, folder_name))]

    if not projects:
        print("No FastAPI projects found in the instances folder.")
        return
    
    processes = []
    port = 8000
    for name in projects:
        port = port + 1
        process = Process(target=run_project, args=(name, port,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()



if __name__ == "__main__":
    main()