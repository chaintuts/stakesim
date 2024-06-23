## General
____________

### Author
* Josh McIntyre

### Website
* jmcintyre.net

### Overview
* StakeSim is a tool for visualizing Proof-of-Stake algorithms with microprocessors

## Development
________________

### Git Workflow
* development for bugfixes and new features

### Building
* make build
Build the application
* make clean
Clean the build directory

### Features
* Generate entropy for default of 3 nodes
* Combines entropy using a commit -> reveal scheme with a toy hash
* Select nodes using combined entropy and weighted selection based on stake
* Display simulation data via character screen
* Display simulation data via serial

### Requirements
* Requires CircuitPython

### Platforms
* Adafruit M4 microcontrollers (ItsyBitsy M4, Grand Central M4, Metro M4)

## Usage
____________

### Code Installation
* Connect your microprocessor to PC via USB
* Copy the source Python files and libraries to the `CircuitPython` directory

### Peripheral Installation
* Wire up the desired output - currently supports a character LCD with I2C backpack, or output to PC via USB cable (no accessories needed)

### General usage
* Once the code is loaded, restart the board to automatically run a new simulation

### Run unit tests
* Run `python -m pytest <test file>`