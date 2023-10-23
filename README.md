# Fargo Engineering NGIO prototype software

## Environment Setup

#### Create a virtual environment - Windows
* First make sure you have python installed, ideally from python.org, and installed on your PATH
* Open the Folder in VS code containing the python code with *main.py* at the root level.
* On Windows, run in terminal **python -m venv ./venv**  You should see a venv folder appear in your source directory.
* To activate the venv, run **venv/Scripts/activate**
* Once this is activated (you should see (venv) in front of your command line), install the python dependencies
* **pip install -r requirements.txt** from the root directory should install all required pip libraries

#### Create a virtual environment - Linux
* First make sure you have python installed, if not you can run *sudo apt-get install python* from a terminal to install.
* you can also install VS code with **sudo apt-get install code** on linux.
* Open the Folder in vs code containing the python code with *main.py* at the root level.
* On Windows, run in terminal **python -m venv ./venv** You should see a venv folder appear in your source directory.
* To activate the venv, run **venv/bin/activate** NOTE THE DIFFERENCE FROM WINDOWS
* Once this is activated (you should see (venv) in front of your command line), install the python dependencies
* **pip install -r requirements.txt** from the root directory should install all required pip libraries

## Usage

#### Select your EtherCAT Network Adapter
* Look at line 17-18 in fei_ethercat.py and make sure the adapter_name matches the adapter you are using.
* To determine your adapter name, run the file find_adapters.py, which will print out all your network adapters ID's
* If you are on a Raspberry Pi or linux, the adapter should be as simple as 'eth0'
* It is a little more complicated on windows, the adapter format should be similar to : '\Device\NPF_{DEADBEEF-DEAD-BEEF-DEAD-BEEEEEEEEF}'
* *Make sure to format your string with double backslashes in python*
* Simply use that string as the adapter name in fei_ethercat, and you should be good to go.

#### Starting the UI
* To start the UI, run *main.py*
* If you receive an error, make sure the board is powered up and the ethernet cable is plugged into the correct port(bottom)
* You should see the Slave name appear in the command line and the UI should open

#### Using the UI
* The UI Has Four Text Inputs, One Dropdown and one button.
* For this revision, the python is talking to one slot board at a time, which is determined by the slot number that is entered.
* Functionality is determined by the selected slot_type.

#### Setting Slot Type
* Enter the number of the slot you would like to set in the first box (i.e 1)
* Enter the number corresponding to the slot type you would like to set in the last text box.
* From the dropdown, select *SetSlotType* as your command.
* Press the submit button, and you should see your slot board change led matching the new slot type:
* Slot types and their number are as follows:

| ID | SlotType |
| -- | -------- |
| 0  | Invalid  | 
| 1  |DigitalOut|
| 2  |DigitalIn | 
| 3  |AnalogIn  | 
| 4  |AnalogOut |
| 5  | PWM In   |
| 6  | Freq Out |

#### DigitalOutput
* Enter the desired Slot number 
* Simply enter 0 for LOW or 1 for HIGH in Data1 text box
* Set slottype to 1, and select *SetSlotType* command from dropdown.
* Click submit to set slot state
* Slot LED should turn RED

#### DigitalInput 
* Enter the desired Slot number
* Set the threshold value (in Volts) in the Data1 text box
* Enter slottype as 2, and select *SetSlotType* command from dropdown.
* Click submit to set slot state
* If the input voltage is higher than the set threshold, you should see HIGH in blue text, or LOW if lower than the threshold.
* Slot LED should turn WHITE

#### AnalogInput
* Enter the desired Slot Number
* Enter slottype as 3, and select *SetSlotType* command from dropdown.
* Click submit to set slot state
* You should be able to view your input voltage in blue text at the bottom of the UI
* Slot LED should turn PURPLE

#### AnalogOutput
* Enter the desired Slot Number
* Set your output value (from 0-4096, where 12v is the maximum output) in Data 1 text box.
* Enter slottype as 4, and select *SetSlotType* command from dropdown.
* Click submit to set slot state
* Slot LED should turn ORANGE

#### PWM IN
* Enter the desired Slot Number
* Enter slottype as 5, and select *SetSlotType* command from dropdown.
* Click submit to set slot state
* You should see the reported Duty Cycle in blue text

#### FREQUENCY OUT
* Enter the desired Slot Number
* Enter slottype as 6, and select *SetSlotType* command from dropdown.
* Enter the frequency value in Data1
* enter the duty cycle in Data2 (being a value from 0 - 4096, 4096 being always off, 0 being always on)
* Click submit to set slot state

#### Setting relays
* Enter the desired Slot Number 
* Select *Set Relays* from the dropdown
* Enter a value from 0 - 3 in the slot type box, and click submit to set the relay state
* states are described here:
| Val | RelayState   |
| --- | ----------   |
| 0   |Both OFF      | 
| 1   |RelayPin HIGH |
| 2   |Bypass HIGH   | 
| 3   |Both ACTIVE   | 


#### Uploading new firmware.
* Enter the number of the slot you wish to update
* Select *SetBLEState* from the dropdown
* Enter 1 for BLE on or 0 for BLE off in the slot type box
* Click submit to set slot state
* if BLE is active, Slot LED should be flashing BLUE
* Set the path to the bin file in slot_program.py 
* run slot_program.py to detect BLE slots and update firmware OTA