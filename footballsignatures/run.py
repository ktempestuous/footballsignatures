import subprocess
import os
import time
import platform

# Step 1: Run Scrapy Spider
def run_scrapy_spider():
    # run spider from project's root directory
    command = ['scrapy', 'crawl', 'footballsignature','-o','output_file.json']
    try:
        print("Running Scrapy spider...")
        subprocess.run(command, check=True)
        print("Scrapy spider finished.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the Scrapy spider: {e}")
        exit(1)

# Step 2: run Python plotting
def run_plotting_script():
    try:
        print("Running Python plotting scripts...")
        print("While it's running, guess who has/have the most expensive signature...")
        command = ['python', 'boxplot.py']  
        subprocess.run(command, check=True)
        command = ['python', 'barchart.py']  
        subprocess.run(command, check=True)
        command = ['python', 'heatmap_plot.py']  
        subprocess.run(command, check=True)
        print("Time's up! Plotting scripts finished.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the plotting script: {e}")
        exit(1)

# Step 3: open 'figures' directory in file explorer
def open_figures_directory():
    system = platform.system()
    if system == 'Darwin':  # macOS
        subprocess.run(['open', 'figures/'])
    elif system == 'Linux':  # Linux
        subprocess.run(['xdg-open', 'figures/'])
    elif system == 'Windows':  # Windows
        subprocess.run(['start', 'figures/'], shell=True)
    else:
        print(f"Unsupported OS: {system}")

# Main function to execute both tasks sequentially
def main():
    # Step 1: run the Scrapy spider
    run_scrapy_spider()
    
    # wait
    time.sleep(2) 
    
    # Step 2: run plotting scripts
    run_plotting_script()

    # Step 3: open figures directory
    open_figures_directory()

# run main function
if __name__ == "__main__":
    main()

