import os
import threading
import time

from global_vars import *
from UserInterface.generate_ui import *
from UserInterface.update_ui import *
from UserInterface.parse_excel_ngio import *



gv = global_vars()
pe = parse_excel(gv)
gu = generate_ui(gv)
ui = update_ui(gv)

# parse excel config file
pe.parse_excel()


# generate UI
gu.generate_ui()