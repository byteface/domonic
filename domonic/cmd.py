"""
    domonic.cmd
    ====================================
    - call cmd commands from python 3
"""
import subprocess
import os

from domonic.javascript import window

# create a mapping of equivelent commands to call on terminal if user OS is not windows
equivelents_map = {
    "dir": "ls",
    "move": "mv",
    "copy": "cp",
    "erase": "rm",
    "comp": "diff",
    # "type_":"cat",
    # "open":"open",
    # "edit":"vim",
    # "view":"less",
    # "search":"grep",
    # "replace":"sed"
}


class CmdException(Exception):
    """ raised if cmd throws an exception """

    def __init__(self, error, message: str = "An error message was recieved from cmd"):
        print(error, message)
        self.message = message
        super().__init__(self.message)


class Cmdcommand():
    """ wrapper class for all cmd commands """

    @staticmethod
    def run(cmd: str) -> str:
        """[runs any command on the cmd]

        Args:
            cmd (str): The command you want to run on cmd

        Returns:
            str: the response as a string
        """
        returned_output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return returned_output.decode("utf-8")

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.params = ''.join([each.__str__() for each in args])
        self.result = ""

        if not hasattr(self, 'first_run'):
            self.first_run = True
        else:
            self.first_run = False

        # TODO - call terminal equiv command if not on windows
        # from sys import platform
        # if platform == "linux" or platform == "linux2":
        #     print("This is linux")
        # elif platform == "darwin":
        #    print("This is mac")
        # elif platform == "win32":
        #    print("This is windows")

        self.run_command()

    def __call__(self, *args, **kwargs):
        self.run_command()
        return self.result

    def run_command(self):
        if hasattr(self, 'wait'):
            self.has_wait = True
            if self.first_run is True:
                self.first_run = False
                return
        else:
            self.has_wait = False

        if hasattr(self, 'iterable'):
            if self.first_run is True:
                self.first_run = False
                return

        try:
            cmd = f"{self.name} {self.params}"
            cmd = cmd.strip()

            '''
            # TODO - after doing all this. think i may have decided to go for 2 base commands instead
            # one iterable and one normal. its still hidden from user as just a different inhereted command
            # but would keep both simpler and can have more types. so will have to refactor all this again
            # for now this behaves how i want despite the _new_ hack and double call on this command
            '''
            if self.has_wait is not True:
                returned_output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                self.result = returned_output.decode("utf-8")
            else:
                self.result = 'PING FAIL'

                def kill_switch(proc):
                    proc.kill()
                    return

                # try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                intId = window.setInterval(3000, kill_switch, proc)
                self.result = proc.stdout.readlines()
                window.clearInterval(intId)
                # except subprocess.TimeoutExpired as e:
                # self.result = returned_output.decode("utf-8")
                # print('process ran too long')

        except subprocess.CalledProcessError as e:
            print(e.output)
            self.result = e.output
            raise CmdException(e, self.result)

        return

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        if hasattr(instance, 'iterable'):
            is_iterable = instance.iterable
            if is_iterable:
                return instance

        return str(instance.result)

    def __str__(self):
        return str(self.result)

    def __getitem__(self, index):
        return self.result.splitlines()[index]

    # def __repr__(self):
    #     return f"{self.__class__.__name__}({self.params})"

    def __iter__(self):
        return iter(self.result.splitlines())

    # def __add__(self, other):
    #     return str(self.result) + str(other)

    # def __radd__(self, other):
    #     return str(other) + str(self.result)

    # def __call__(self, *args, **kwargs):
    #     self.run_command()
    #     return self.result

    # def __getattr__(self, attr):
    #     if attr in equivelents_map:
    #         return Cmdcommand(equivelents_map[attr], *self.args, **self.kwargs)

    # def __del__(self):
    #     os.chdir("..")
    #     return


class cd(Cmdcommand):
    """
    NOTE - 'cd' does not run on cmd
    - cd is pointless as session opens and closes
    - so is overridden to change dirs via pure python
    """
    def run_command(self):
        os.chdir(self.params)


# tested --
dir = type('dir', (Cmdcommand,), {'name': 'dir', 'iterable': True})  #: list directory content
erase = type('erase', (Cmdcommand,), {'name': 'erase'})
# del = type('del', (command,), {'name': 'del'})
mkdir = type('mkdir', (Cmdcommand,), {'name': 'mkdir'})  #: create a new directory
rmdir = type('rmdir', (Cmdcommand,), {'name': 'rmdir'})  #: delete directory
copy = type('copy', (Cmdcommand,), {'name': 'copy'})  #: copy files

fsutil = type('fsutil', (Cmdcommand,), {'name': 'fsutil'})
fc = type('fc', (Cmdcommand,), {'name': 'fc'})  # compare files and display the differences


class touch(Cmdcommand):
    def run_command(self):
        self.iterable = True
        try:
            cmd = f"fsutil file createnew {self.params} 0"
            Cmdcommand.run(cmd)
        except Exception as e:
            # print('failed to touch:', e)
            self.result = ''


getmac = type('getmac', (Cmdcommand,), {'name': 'getmac'})  #: display MAC address
ipconfig = type('ipconfig', (Cmdcommand,), {'name': 'ipconfig'})  #: display IP network settings
shutdown = type('shutdown', (Cmdcommand,), {'name': 'shutdown'})  #: shutdown the computer. (/s), triggers a restart (/r), or logs the user out (/l).
# date = type('date', (Cmdcommand,), {'name': 'date'})  #: show/set date - TODO seemed to hang. needs a param
echo = type('echo', (Cmdcommand,), {'name': 'echo'})  #: text output
hostname = type('hostname', (Cmdcommand,), {'name': 'hostname'})  #: display host name
# time = type('time', (Cmdcommand,), {'name': 'time'})  #: display/edit the system time - TODO seemed to hang
ver = type('ver', (Cmdcommand,), {'name': 'ver'})  #: display operating system version - TODO seemed to hang
# netstat = type('netstat', (Cmdcommand,), {'name': 'netstat'})  #: display TCP/IP connections and status
ping = type('ping', (Cmdcommand,), {'name': 'ping'})  #: pings the network
# ping = type('ping', (Cmdcommand,), {'name': 'ping', 'wait': True, 'iterable': True})  # < TODO - need to stream feedback

move = type('move', (Cmdcommand,), {'name': 'move'})  #: move/rename files
rename = type('rename', (Cmdcommand,), {'name': 'rename'})  #: rename files
replace = type('replace', (Cmdcommand,), {'name': 'replace'})  #: replace files

systeminfo = type('systeminfo', (Cmdcommand,), {'name': 'systeminfo'})  #: displays computer-specific properties and configurations

attrib = type('attrib', (Cmdcommand,), {'name': 'attrib'})  #: display file attributes
# tree = type('tree', (Cmdcommand,), {'name': 'tree'})  #: display folder structure graphically - TODO - return not utf-8
type_ = type('type_', (Cmdcommand,), {'name': 'type'})  #: display content of text files
comp = type('comp', (Cmdcommand,), {'name': 'comp'})  #: compare file contents

chkdsk = type('chkdsk', (Cmdcommand,), {'name': 'chkdsk'})  #: check volumes
driverquery = type('driverquery', (Cmdcommand,), {'name': 'driverquery'})  #: display installed devices and their properties
vol = type('vol', (Cmdcommand,), {'name': 'vol'})  #: show volume description and serial numbers of the HDDs
gpresult = type('gpresult', (Cmdcommand,), {'name': 'gpresult'})  #: display group policies

# ssh = type('ssh', (Cmdcommand,), {'name': 'ssh'})

chdir = type('chdir', (Cmdcommand,), {'name': 'chdir'})  # : show current dir or can switch dir
# clip = type('clip', (Cmdcommand,), {'name': 'clip'})  # : Forwards the result of a command to the clipboard

# find = type('find', (Cmdcommand,), {'name': 'find'})
whoami = type('whoami', (Cmdcommand,), {'name': 'whoami'})  #: information about the current user. /GROUP parameter

logoff = type('logoff', (Cmdcommand,), {'name': 'logoff'})  #: Logs the user out of Windows.
mrinfo = type('mrinfo', (Cmdcommand,), {'name': 'mrinfo'})  #: Provides information on the router
tasklist = type('tasklist', (Cmdcommand,), {'name': 'tasklist'})  #: Lists all running processes

# cmd = type('cmd', (Cmdcommand,), {'name': 'cmd'})  #: start command prompt - NOTE hangs
title = type('title', (Cmdcommand,), {'name': 'title'})  #: Changes the title of the command prompt
tzutil = type('tzutil', (Cmdcommand,), {'name': 'tzutil'})  #: Displays the currently set time zone (/g) or changes it (/s)

# bitsadmin = type('bitsadmin', (Cmdcommand,), {'name': 'bitsadmin'})  #: Allows you to run commands on a remote computer
# chcp = type('chcp', (Cmdcommand,), {'name': 'chcp'})  #: Change the locale of the command prompt
# cls = type('cls', (Cmdcommand,), {'name': 'cls'})  #: Clears the screen
# deluser = type('deluser', (Cmdcommand,), {'name': 'deluser'})  #: Deletes a user
# dir = type('dir', (Cmdcommand,), {'name': 'dir'})  #: Displays the contents of a directory
# dlls = type('dlls', (Cmdcommand,), {'name': 'dlls'})  #: Lists the DLLs loaded by an executable
# echo_ = type('echo_', (Cmdcommand,), {'name': 'echo_'})  #: text output
# echo = type('echo', (Cmdcommand,), {'name': 'echo'})  #: text output
# ed = type('ed', (Cmdcommand,), {'name': 'ed'})  #: Edit a file
# edlin = type('edlin', (Cmdcommand,), {'name': 'edlin'})  #: Edit a file
# exit = type('exit', (Cmdcommand,), {'name': 'exit'})  #: Exits the command prompt
# find = type('find', (Cmdcommand,), {'name': 'find'})  #: Find a file or folder
# findstr = type('findstr', (Cmdcommand,), {'name': 'findstr'})  #: Find a string in files or folders
# format = type('format', (Cmdcommand,), {'name': 'format'})  #: Format a file
# gpedit = type('gpedit', (Cmdcommand,), {'name': 'gpedit'})  #: Edit the Group Policy
# help = type('help', (Cmdcommand,), {'name': 'help'})  #: Displays help files
# help_ = type('help_', (Cmdcommand,), {'name': 'help_'})  #: Displays help files
# help_ctx = type('help_ctx', (Cmdcommand,), {'name': 'help_ctx'})  #: Displays help files
# help_nt = type('help_nt', (Cmdcommand,), {'name': 'help_nt'})  #: Displays help files


# WINDOWS COMMANDS
'''
bitsadmin	Creates and monitors downloads and uploads
chcp	Changes the current code page
choice	Creates a selection list
clip	Forwards the result of a command to the clipboard.
color	Changes the background
command	Starts CMD.COM.	32-bit/DOS
date	Displays the current date and allows you to change it.
debug	Starts debug
doskey	Creates macros, recalls commands, and edits command input
dosshell	Opens the DOS shell
edit	Starts the MS-DOS editor
edlin	Creates and edits text files within the command prompt
fasthelp	Displays helpful information about commands
fastopen	Writes the position of a program into a specified list
find	Searches through a file or multiple files for a particular character sequence.
findstr	Finds character sequences in one or multiple files.
forcedos	Starts a program in the MS-DOS partial system
graftabl	Enables the option to use extended characters of a specific code page in graphics mode.	32-bit/DOS
graphics	Starts a program that can print graphics.	32-bit/DOS
help	Displays help text for a specific command (you can also use the /? command)
kb16	Changes the country settings of the keyboard for DOS programs
keyb	Changes the country settings of the keyboard for DOS programs
lpq	Displays the status of a printer queue for computers that use a “line Printer Daemon” (LPD)
lpr	Sends a file to a computer that uses a line printer daemon (LPD).
md	Creates a new directory on the specified path.
more	Outputs the content of a file (for example, a text file) by the page.
msg	Sends a message to another user.
nlsfunc	Provides country-specific information for language support.	32-bit/DOS
ntbackup	Runs backup services directly from the command line or as part of batch or script files.	XP
path	Creates and displays the path for searching executable files
pause	Pauses execution in batch files and scripts.
popd	Changes to the folder saved by the pushd command.
print	Prints a text file.
prompt	Changes the display of the command prompt
pushd	Saves a specific path into a script or batch file.
qbasic	Starts qbasic, a program environment based on the BASIC programming language
rd	Deletes a directory.
rem	Writes comments in batch and script files that aren’t taken into account when executing
runas	Allows a user to run commands with the rights of another user.
scandisk	Starts Microsoft ScanDisk. The program searches data carriers for errors
schtasks	Sets the execution of specified programs and commands for a specified point in time.
set	Displays environmental variables of CMD.EXE and lets you configure them
shift	Moves variables within batch files and scripts
sort	Lists out data (from a file or command) and outputs it again sorted
start	Opens a new command prompt window in which you can run a specific program or command
subst	Assigns a drive letter to a path to create a virtual drive
taskkill	Ends one or more running tasks.
time	Displays the current time and allows it to be changed.
timeout	Stops a process for a specified time.
Files
CMD command	Description	Windows version
append	Sets the path in which files will be searched for.	32-bit/DOS
assoc	Changes the program that’s linked with a particular file ending.
attrib	Changes attributes of specified files. With the parameter +R you can protect a file from changes
cipher	Displays and changes the encryption status of files and directories on NTFS partitions.
comp	Compares the content of two files or two file sets.
compact	Displays and changes the compression status of files and directories on NTFS partitions.
copy	Copies a file or multiple files to another location.
cscript	Runs scripts over the Microsoft Script Host.
del	Deletes a file or multiple files.
deltree	Deletes a directory as well as all subdirectories and files within
diantz	Compresses files without any loss (command has the same function as makecab)
diskcomp	Compares the content of two disks (not 10)/DOS
diskcopy	Copies the content of a disk to another (not 10)/DOS
endlocal	Ends the valid range of changes to batch files or scripts.
erase	Function is the same as del
exe2bin	Converts an EXE file to a BIN file.	32-bit
expand	Extracts files and folders stored in CAB files (not 64-bit XP)/DOS
extrac32	Extracts files and folders stored in CAB files.
fc	Compares two individual files or two sets of files with one another and displays the differences
forfiles	Selects one or more files and runs a command that refers to these files.
ftype	Specifies a program for opening a specific file type.
goto	Skips the execution within a batch program to a specific line (marker)
if	Represents a conditional statement and executes expressions within batch files only under certain conditions.
makecab	Compresses files without loss in CAB format (you can also use the diantz command).
mklink	Creates a symbolic link to a file. With /D you can also create connections to directories.
move	Moves a file or multiple files from one directory to another.
openfiles	Displays and separates open system files and folders.
recover	Restores readable files that were on a defective data drive.
ren	Changes the name of a particular file.
rename	Function is the same as ren
replace	Replaces the selected file or files with one or more other files.
robocopy	Allows so-called robust file copying.
rsm	Manages media on removable storage devices.
setlocal	Limits the valid range of changes to batch files or scripts.
share	Installs file sharing and file locking.	32-bit/DOS
sxstrace	Starts the WinSxs Tracing Utility, a tool for programming diagnostics.
takeown	Restores administrator access rights to a file that have been lost when reassigning a user.
undelete	Undoes the deletion of a file
verify	When enabled, checks whether files are written correctly on a data drive.
where	Finds files that match a particular search topic.
xcopy	Copies files and entire directory structures.
System
CMD command	Description	Windows version
at	Starts commands and programs at a particular time.
auditpol	Displays current monitoring policies.
backup	Creates backups of files. These can be recovered with restore (replaced by msbackup)
bcdboot	Creates and repairs start files
bcdedit	Allows users to make changes to start configuration data storage
bdehdcfg	Prepares a hard drive for BitLocker Drive Encryption.
bootcfg	Creates, edits, or displays the content of boot.ini
bootsect	Modifies the master boot code sot that it’s compatible with the Windows Boot Manager or NT Loader
cacls	Edits and displays the access control list.
chkdsk	Checks and repairs (with the parameter /R) a data drive
chkntfs	Changes or displays the data driver check at startup.
cmdkey	Can display (/list), create (/add), or delete (/delete) login information.
convert	Converts partitions from FAT/FAT32 to NTFS.
ctty	Changes the standard input and output for the system
dblspace	Creates or configures compresses drives (a newer version of the command is called drvspace)
defrag	Defragments all or only specified drives. Use /U to observe the progress.
diskpart	Manages, creates, and deletes partitions from the hard drive.
diskperf	Allows users to remotely control the disk performance counter.
diskraid	Manages RAID systems.
dism	Manages and integrates Windows images
dispdiag	Creates a file in the current directory in which you’ll find information about your display.
dosx	Starts the DOS Protected Mode Interface
driverquery	Creates a list with all installed drivers.
drvspace	Creates or configures compressed drives.
emm386	Provides DOS with more than 640 KB of RAM
esentutl	Manages databases within the extensible storage engine.
eventcreate	Creates an entry (ID and message) in an event log.
eventtriggers	Configures and displays event trigger.	XP
fdisk	Creates, deletes, and manages partitions on the hard drive.
fltmc	Allows users to manage and display filter drivers.
fondue	Installs additional Windows features.
format	Formats a drive to the file system specified by the user
hwrcomp	Compiles self-created dictionaries for handwriting recognition
hwrreg	Installs a compiled dictionary for handwriting recognition
icacls	Edits and displays the access control list.
ktmutil	Starts the kernel transaction manager.
label	Changes or deletes a drive’s label
lh	Loads a program into the high memory area (UMB) – has the same function as loadhigh
licensingdiag	Creates an XML and a CAB file that contain information on the Windows product licence
loadfix	Ensures that a program is loaded and executed above the first 64 KB of RAM.	32-bit/DOS
loadhigh	Has the same function as lh
lock	Locks a drive so that only a user-selected program can access it directly.	98/95
lodctr	Updates all registry entries that have to do with performance indicators
logman	Creates and manages event trace sessions and performance logs.
manage-bde	Configures drive encryption with BitLocker.
mem	Displays information about the RAM and indicates which programs are currently loaded in it.	32-bit/DOS
memmaker	Optimises the RAM
mode	Configures system devices – primarily on the COM or LPT port
mofcomp	Analyses files in managed object format (MOF) and adds the classes and instances to the WMI repository
mountvol	Creates and deletes mount points for drives and displays them.
msav	Starts Microsoft Antivirus
msbackup	Starts Microsoft Backup (replaces backup and restores)
mscdex	Loads the CD-ROM support for MS-DOS
msd	Starts the program Microsoft Diagnostics, with which system information can be displayed
msiexec	Starts the Windows installer
muiunattend	Starts an automatic setup process for the multilingual user interface (MUI)
netcfg	Installs the minimal operating system Microsoft Windows PE.
ocsetup	Installs additional Windows functions.	8/7/Vista
pentnt	Recognises floating point division errors
pkgmgr	Installs, uninstalls, and configures packages and functions for Windows.
pnpunattend	Automates the installation of device drivers
pnputil	Installs plug-and-play devices from the command prompt.
power	Uses the IDLE status of a processor to reduce energy consumption
powercfg	Allows the user to change the computer’s energy options and control energy conservation plans.
pwlauncher	Configures the startup options for Windows To Go with which you can boot Windows from a USB drive
qprocess	Provides information on running processes.
query	Displays the status of a particular service.
quser	Provides information on the currently logged-in users.
reagentc	Configures the Windows recovery environment
recimg	Creates a user-defined Windows image to restore the system.	8
reg	Manages the registry of the command prompt.
regini	Changes registry authorisations.
register-cimprovider	Registers a common information model provider (CIM provider) in Windows
regsvr32	Registers a DLL file in the registry.
relog	Creates new performance indicator protocols from the data in the existing protocols.
repair-bde	Repairs and decrypts defective drives that are encrypted with BitLocker.
reset	Resets a session. You can also use the rwinsta command.
restore	Restores backups that were created with the backup command (replaced by msbackup)
rwinsta	Command has the same function as reset.
sc	Manages services by connecting to the Service Controller.
scanreg	Repairs the registry and allows a backup to be created of it.	98/95
sdbinst	Applies user-defined database files (SDB).
secedit	Analyses the security settings by comparing the current configurations with templates.
setver	Sets a version number of MS-DOS that’s forwarded to a program
setx	Creates or changes environmental variable in the user of system environment.
sfc	Checks all important and protected system files.
smartdrv	Starts and manages the hard drive cache program SMARTDrive
sys	Copies system files from MS-DOS and the command interpreter to another hard drive. This makes it bootable
systeminfo	Displays information about the Windows installation, including all installed service packages.
tpmvscmgr	Creates and deletes TPM virtual smart cards.
tracerpt	Processes logs or real-time data generated during the tracing of computer programs.
typeperf	Displays performance counter data or writes it into a file.
unformat	Undoes the drive formatting done by the format command
unlock	Unlocks a drive that was locked with the lock command.	98/95
unlodctr	Deletes names as well as descriptions for extensible performance counters in the Windows registry.
vaultcmd	Creates, deletes, and displays saved registration information
vol	Displays the label and serial number of a drive
vsafe	Starts the antivirus software VSafe
vssadmin	Manages the volume shadow copy services that can be used to store different versions (snapshots) of drives.
wbadmin	Creates backups of the operating system and delivers information to the created backup copies.
wevtutil	Manages event logs and event log files.
winmgmt	Manages WMI repositories. Backups (/backup) are possible with the command, for example
winsat	Evaluates various system factors – for example, processor performance or graphical capabilities.
wmic	Starts the Windows Management Instrumentation in the command prompt.
xwizard	Registers Windows data in the form of XML files
Network
CMD command	Description	Windows version
arp	Displays and edits entries in the Address Resolution Protocol cache
atmadm	Displays information on asynchronous transfer mode (ATM).	XP
certreq	Manages and creates certificate registration requirements for certification authorities.
certutil	Manages services related to certificate authentication.
change	Changes the settings of a terminal server and can be used together with the parameters logon, port, or user
checknetisolation	Checks the network capability of apps from the Windows Store
chglogon	Enables, disables, or adjusts logins for terminal server sessions.
chgport	Displays or changes the COM pin assignment of terminal servers for DOS compatibility.
chgusr	Changes the installation mode of a terminal server.
cmstp	Installs or uninstalls profiles for the connection manager.
djoin	Creates a new computer account in the Active Directory Domain Services (AD DS).
finger	Provides information about users on remote devices using the Finger service.
ftp	Transfers data to an FTP server or from this to a PC.
gpresult	Displays information on the Group Policy.
gpupdate	Updates information on the Group Policy.
interlnk	Connects two computers via serial or parallel connection to share files or printers
intersvr	Starts an interlnk server and transfers data from one computer to another via serial or parallel connection
ipxroute	Changes and displays information on the IPX routing tables.	XP
irftp	Transfers files via infrared connection, if one is available.
iscsicli	Manages iSCSI, which enables connections via the SCSI protocol.
klist	Displays all tickets authenticated by the Kerberos service. Also enables the command to delete tickets (purge)
ksetup	Configures a connection to a Kerberos server
mount	Enables network sharing under the Network File System. (To use the command, enable NFS services)
nbtstat	Displays statistics and information on the TCP/IP connections on remote computers
net	Configures and displays network settings
net1	Configures and displays network settings
netsh	Starts the network shell, which allows for network settings to be changed on local and remote computers.
netstat	Displays statistics and information on TCP/IP connections on the local computer
nfsadmin	Manages NFS servers and clients (to be able to use the command, you first have to enable NFS services in Windows)
nltest	Displays information related to secure channels in the Active Directory Domain Services (AD DS) and tests the connections
nslookup	Sends a DNS query to a specific IP or host name on the preconfigured DNS server. You can also specify another DNS server
ntsd	Runs debugging.	XP
pathping	Provides information on forwarding and package loss when sending over a network and also specifies the latency.
qappsrv	Displays all available remote computers in the network.
qwinsta	Displays information on the open remote desktop sessions.
rasautou	Manages autodial addresses.
rasdial	Starts and ends network connections for Microsoft clients.
rcp	Copies files from a Windows computer to a server that’s running a RSDH daemon, and vice versa
rdpsign	Signs a remote desktop protocol file (RDP file)/7
rexec	Runs commands on a remote computer that’s running a Rexec daemon.	Vista/XP
route	Displays routing tables and makes it possible to change, add, or delete entries
rpcinfo	Sends a remote procedure call (RPC) to an RPC server.
rpcping	Sends a ping via remote procedure call (RPC) and checks whether a connection is possible.
rsh	Runs commands on remote computers that are running the Unix program Remote Shell (RSH)
setspn	Creates, deletes, and changes SPNs.
shadow	Monitors a session on a remote computer.
showmount	Provides information on NFS file systems (to use the command, you first have to activate NFS services in Windows)
tcmsetup	Enables or disables a client for the Telephony Application Programming Interface (TAPI)
telnet	Enables communication with another computer that also uses the telnet protocol
tftp	Enables a file exchange between the local computer and a server that supports the Trivial File Transfer Protocol (TFTP).
tlntadmn	Manages a telnet server on a local or remote computer
tracert	Tracks a data package on the way through the network to a server.
tscon	Connects the current local user session with a session on a remote computer.
tsdiscon	Ends the connection between a local user session and a session on a remote computer.XP
tskill	Ends a process on a remote computer.
tsshutdn	Shuts down or restarts a remote terminal server.
umount	Removes mounted network file system drives.
w32tm	Manages the Windows time service that synchronises dates and times on all computers that share an AD DS domain.
waitfor	Sends or waits on a single.
wecutil	Creates and managements subscriptions for events.
winrm	Manages secure connections between local and remote computers via the WS management protocol.
winrs	Enables access to the command line of a remote computer via a secure connection to implement changes.
wsmanhttpconfig	Manages functions of the Windows Remote Management (winrm).
'''
