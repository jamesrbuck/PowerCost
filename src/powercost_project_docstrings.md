# Project Documentation Extracted from Docstrings

## File: `powercost_project\config.py`

### 🧾 Module-level Docstring
```
This modules contains both config class: DatabaseConfig and SetupConfig.
```

### Class: `DatabaseConfig`
```
MySQL database configuration settings.
```

### Class: `SetupConfig`
```
Class to handle logging, port configuration settings.
```

### Class: `PonderosaConfig`
```
Class is the entry point into acquiring all configuration settings.  It references
SetupConfig and DatabaseConfig.
```

### Function: `as_dict`
```
It returns a dictionary of database settings for debugging
purposes for debugging purposes
```

### Function: `running_file`
```
Returns: running_file
```

### Function: `stop_file`
```
Returns: stop_file
```

### Function: `log_dir`
```
Returns: log_dir
```

### Function: `log_file`
```
Returns: log_file
```

### Function: `log_level`
```
Returns: log_level
```

### Function: `the_port`
```
Returns: port to EMU-2 device
```

### Function: `db_config`
```
Returns: database configuration settings as a dictionary.
```

## File: `powercost_project\database.py`

### 🧾 Module-level Docstring
```
Handles database activities.
```

### Class: `PonderosaDB`
```
A single class that handles database activities.
```

### Function: `__init__`
```
Initializes the database connection manager.
```

### Function: `__enter__`
```
Connect to the database when PonderosaDB class is instantiated.
```

### Function: `__exit__`
```
Automatically close connection on context exit of PonderosaDB class.
```

### Function: `connect`
```
Establish a new connection to the database.
```

### Function: `close`
```
Close the connection if it is open.
```

### Function: `insert_usage`
```
Insert an hourly usage record into the database.

Parameters:
- date_str: Date in 'YYYY-MM-DD' format
- hour_str: Time in 'HH:00:00' format
- kwh: Decimal or float kWh value
```

### Function: `__str__`
```
Return setting as a string for debugging.
```

## File: `powercost_project\main.py`

### 🧾 Module-level Docstring
```
This Python code handles the setup of the configuration (in config.py),and
database (in database.py) classes.  Most of the work is done in the run()
method.
```

### Class: `PonderosaMonitor`
```
This class encapulates most of the script's logic to isolate responsibilities,
improve code testability and enable future extensions.
```

### Function: `setup_logging`
```
Set up Python logging based on settings in INI file.
```

### Function: `setup_signal_handler`
```
Since this app runs indefinitely, setup signal handling to
report being killed from the OS.  These signals are not usually
sent in Windows.  The presence of a "stop file" triggers a
graceful shutdown.  In Windows, I have also had to use
Task Manager + Details + End Task which does not send a
"signal".  This method would be useful in Linux.
```

### Function: `check_stop_file`
```
This method checks for the existence of a file that indicates that
this daemon-like program should stop gracefully.
```

### Function: `check_already_running`
```
This method checks for the existence of a file that indicates that
this daemon-like program is already running.  It cannot run more than
one instance at a time.  The Force option was intended to be
used when the program is started by Windows Scheduled Task.  The original
intention was that Windows would start the task every Midnight and
if the application was already running, nothing would happen.
Starting of the application was changed to System Startup.  Now, I
just manually start feom a script.  Almost daemon.
```

### Function: `wait_until_top_of_hour`
```
The application will only make hourly recordsing that contain
full 60 separate minute readings.  The application will wait how many seconds
until the top of the next hour or xx:00 AM/PM before starting.
```

### Function: `start_serial`
```
Starting a serial connection (via USB on Windows) to the EMU-2.  This
startup may not work the first time so there is retry logic.
```

### Function: `read_demand`
```
Reading from the EMU-2 may not work the first time so there is retry logic.
```

### Function: `run`
```
Almost all of the logic is in this method.  Only the acquisition of the
parameters is done in main.py.
```

## File: `powercost_project\__init__.py`

### 🧾 Module-level Docstring
```
Designate this folder as a Python package.  Only main.py - Class PonderosaMonitor
is accessible from outside of the package.  Initializations are not done here.
```

## File: `powercost_project\__main__.py`

### 🧾 Module-level Docstring
```
Entry point for project.  _init__.py does not do much.  For now, this code: handles
arguments passed to the package; there is only one argument: the location of the
INI file.  This code instantiates the primary controller class PonderosaMonitor
where control is passed to the run() method to do most of the work.
```

### Function: `main`
```
Entry Point.  This is the only method and it instantiates the PonderosaMonitor
class and control passes to the run() method.
```

