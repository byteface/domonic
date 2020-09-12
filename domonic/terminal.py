"""
    domonic.terminal
    ====================================
    - call command line functions in python 3
"""
import subprocess
import os

from domonic.javascript import window


class TerminalException(Exception):
    """ raised if the terminal throws an exception """

    def __init__(self, error, message="An error message was recieved from terminal"):
        print(error, message)
        self.message = message
        super().__init__(self.message)


class command():
    """ wrapper class for all terminal commands """

    @staticmethod
    def run(cmd):
        """run

        runs any command on the terminal

        Args:
            cmd (str): The command you want to run on the terminal

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
            raise TerminalException(e, self.result)

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


class cd(command):
    """
    NOTE - 'cd' does not run on terminal
    - cd is pointless as session opens and closes
    - so is overridden to change dirs via pure python
    """
    def run_command(self):
        os.chdir(self.params)


# tested --
ls = type('ls', (command,), {'name': 'ls', 'iterable': True})
rm = type('rm', (command,), {'name': 'rm'})
ln = type('ln', (command,), {'name': 'ln'})
mkdir = type('mkdir', (command,), {'name': 'mkdir'})
rmdir = type('rmdir', (command,), {'name': 'rmdir'})
touch = type('touch', (command,), {'name': 'touch'})
df = type('df', (command,), {'name': 'df', 'iterable': True})
du = type('du', (command,), {'name': 'du', 'iterable': True})
ps = type('ps', (command,), {'name': 'ps', 'iterable': True})
cat = type('cat', (command,), {'name': 'cat', 'iterable': True})
# --

mv = type('mv', (command,), {'name': 'mv'})
cp = type('cp', (command,), {'name': 'cp'})
rm = type('rm', (command,), {'name': 'rm'})
chmod = type('chmod', (command,), {'name': 'chmod'})
chown = type('chown', (command,), {'name': 'chown'})

users = type('users', (command,), {'name': 'users', 'iterable': True})
useradd = type('useradd', (command,), {'name': 'useradd'})
userdel = type('userdel', (command,), {'name': 'userdel'})
groups = type('groups', (command,), {'name': 'groups'})
groupadd = type('groupadd', (command,), {'name': 'groupadd'})
groupdel = type('groupdel', (command,), {'name': 'groupdel'})

uniq = type('uniq', (command,), {'name': 'uniq'})
sort = type('sort', (command,), {'name': 'sort'})
diff = type('diff', (command,), {'name': 'diff'})
# cmp = type('cmp', (command,), {'name': 'cmp'})

ssh = type('ssh', (command,), {'name': 'ssh'})
scp = type('scp', (command,), {'name': 'scp'})

more = type('more', (command,), {'name': 'more'})
less = type('less', (command,), {'name': 'less'})
# vi = type('vi', (command,), {'name': 'vi'})
# emacs = type('emacs', (command,), {'name': 'emacs'})
head = type('head', (command,), {'name': 'head', 'iterable': True})
tail = type('tail', (command,), {'name': 'tail', 'iterable': True})

uptime = type('uptime', (command,), {'name': 'uptime'})
bash = type('bash', (command,), {'name': 'bash'})
shutdown = type('shutdown', (command,), {'name': 'shutdown'})
reboot = type('reboot', (command,), {'name': 'reboot'})
# open = type('open', (command,), {'name': 'open'})
killall = type('killall', (command,), {'name': 'killall'})
mkfile = type('mkfile', (command,), {'name': 'mkfile'})
ifconfig = type('ifconfig', (command,), {'name': 'ifconfig', 'iterable': True})
ipconfig = type('ipconfig', (command,), {'name': 'ipconfig', 'iterable': True})
finger = type('finger', (command,), {'name': 'finger'})
passwd = type('passwd', (command,), {'name': 'passwd'})
whoami = type('whoami', (command,), {'name': 'whoami'})
# help = type('help', (command,), {'name': 'help'})


class history(command):
    def run_command(self):
        self.iterable = True
        try:
            # history is empty for non interactive sessions so read file
            from os.path import join, expanduser
            with open(join(expanduser('~'), '.bash_history'), 'r') as f:
                self.result = ''.join(f.readlines())
        except Exception as e:
            print('failed to get history:', e)
            self.result = ''


ping = type('ping', (command,), {'name': 'ping', 'wait': True, 'iterable': True})  # < TODO - need to stream feedback
man = type('man', (command,), {'name': 'man'})
find = type('find', (command,), {'name': 'find'})
awk = type('awk', (command,), {'name': 'awk'})
grep = type('grep', (command,), {'name': 'grep'})
cut = type('cut', (command,), {'name': 'cut'})
sed = type('sed', (command,), {'name': 'sed'})
apt = type('apt', (command,), {'name': 'apt'})
gunzip = type('gunzip', (command,), {'name': 'gunzip'})
tar = type('tar', (command,), {'name': 'tar'})
gzip = type('gzip', (command,), {'name': 'gzip'})
cron = type('cron', (command,), {'name': 'cron'})
crontab = type('crontab', (command,), {'name': 'crontab'})
xargs = type('xargs', (command,), {'name': 'xargs'})
nautilus = type('nautilus', (command,), {'name': 'nautilus'})  # Linux only?
date = type('date', (command,), {'name': 'date'})
cal = type('cal', (command,), {'name': 'cal'})
bc = type('bc', (command,), {'name': 'bc'})

rsync = type('rsync', (command,), {'name': 'rsync'})

# https://github.com/agarrharr/awesome-cli-apps
# - NOTE - these ones may need installing if you haven't already
git = type('git', (command,), {'name': 'git'})
wget = type('wget', (command,), {'name': 'wget'})
nmap = type('nmap', (command,), {'name': 'nmap'})
nohup = type('nohup', (command,), {'name': 'nohup'})
python = type('python', (command,), {'name': 'python'})
npm = type('npm', (command,), {'name': 'npm'})
cowsay = type('cowsay', (command,), {'name': 'cowsay'})
pip = type('pip', (command,), {'name': 'pip'})  # TODO - change to 'python3 -m pip'? # TODO - both iterable and not
say = type('say', (command,), {'name': 'say'})  # Mac only?
gcc = type('gcc', (command,), {'name': 'gcc'})
jq = type('jq', (command,), {'name': 'jq'})
curl = type('curl', (command,), {'name': 'curl'})
ffmpeg = type('ffmpeg', (command,), {'name': 'ffmpeg'})
convert = type('convert', (command,), {'name': 'convert'})  # imagemagik
figlet = type('figlet', (command,), {'name': 'figlet'})
banner = type('banner', (command,), {'name': 'banner'})
# imagemagik
# asciiview
# toilet
# figlet
# youtube-dl = type('youtube-dl', (command,), {'name': 'youtube-dl'}) # TODO - illegal chars
# tree = type('tree', (command,), {'name': 'tree'})
# vim = type('vim', (command,), {'name': 'vim'})
# mail = type('mail', (command,), {'name': 'mail'})
# vncserver = type('vncserver', (command,), {'name': 'vncserver'})
# tmux

# https://en.wikipedia.org/wiki/List_of_Unix_commands
# admin = type('admin', (command,), {'name': 'admin'})
ar = type('ar', (command,), {'name': 'ar'})
asa = type('asa', (command,), {'name': 'asa'})
at = type('at', (command,), {'name': 'at'})
basename = type('basename', (command,), {'name': 'basename'})
batch = type('batch', (command,), {'name': 'batch'})
bg = type('bg', (command,), {'name': 'bg'})
cc = type('cc', (command,), {'name': 'cc'})
cflow = type('cflow', (command,), {'name': 'cflow'})
chgrp = type('chgrp', (command,), {'name': 'chgrp'})
cksum = type('cksum', (command,), {'name': 'cksum'})
comm = type('comm', (command,), {'name': 'comm'})
compress = type('compress', (command,), {'name': 'compress'})
csplit = type('csplit', (command,), {'name': 'csplit'})
ctags = type('ctags', (command,), {'name': 'ctags'})
cxref = type('cxref', (command,), {'name': 'cxref'})
dd = type('dd', (command,), {'name': 'dd'})
delta = type('delta', (command,), {'name': 'delta'})
dirname = type('dirname', (command,), {'name': 'dirname'})
ed = type('ed', (command,), {'name': 'ed'})
env = type('env', (command,), {'name': 'env'})
ex = type('ex', (command,), {'name': 'ex'})
expand = type('expand', (command,), {'name': 'expand'})
expr = type('expr', (command,), {'name': 'expr'})
fc = type('fc', (command,), {'name': 'fc'})
fg = type('fg', (command,), {'name': 'fg'})
file = type('file', (command,), {'name': 'file'})
fold = type('fold', (command,), {'name': 'fold'})
fort77 = type('fort77', (command,), {'name': 'fort77'})
fuser = type('fuser', (command,), {'name': 'fuser'})
gencat = type('gencat', (command,), {'name': 'gencat'})
get = type('get', (command,), {'name': 'get'})
getconf = type('getconf', (command,), {'name': 'getconf'})
getopts = type('getopts', (command,), {'name': 'getopts'})
iconv = type('iconv', (command,), {'name': 'iconv'})
# id = type('id', (command,), {'name': 'id'})
ipcrm = type('ipcrm', (command,), {'name': 'ipcrm'})
ipcs = type('ipcs', (command,), {'name': 'ipcs'})
join = type('join', (command,), {'name': 'join'})
lex = type('lex', (command,), {'name': 'lex'})
link = type('link', (command,), {'name': 'link'})
locale = type('locale', (command,), {'name': 'locale'})
localedef = type('localedef', (command,), {'name': 'localedef'})
logger = type('logger', (command,), {'name': 'logger'})
logname = type('logname', (command,), {'name': 'logname'})
lp = type('lp', (command,), {'name': 'lp'})
m4 = type('m4', (command,), {'name': 'm4'})
mailx = type('mailx', (command,), {'name': 'mailx'})
make = type('make', (command,), {'name': 'make'})
mesg = type('mesg', (command,), {'name': 'mesg'})
mkdir = type('mkdir', (command,), {'name': 'mkdir'})
mkfifo = type('mkfifo', (command,), {'name': 'mkfifo'})
more = type('more', (command,), {'name': 'more'})
newgrp = type('newgrp', (command,), {'name': 'newgrp'})
nice = type('nice', (command,), {'name': 'nice'})
nl = type('nl', (command,), {'name': 'nl'})
nm = type('nm', (command,), {'name': 'nm'})
od = type('od', (command,), {'name': 'od'})
paste = type('paste', (command,), {'name': 'paste'})
patch = type('patch', (command,), {'name': 'patch'})
pathchk = type('pathchk', (command,), {'name': 'pathchk'})
pax = type('pax', (command,), {'name': 'pax'})
pr = type('pr', (command,), {'name': 'pr'})
prs = type('prs', (command,), {'name': 'prs'})
qalter = type('qalter', (command,), {'name': 'qalter'})
qdel = type('qdel', (command,), {'name': 'qdel'})
qhold = type('qhold', (command,), {'name': 'qhold'})
qmove = type('qmove', (command,), {'name': 'qmove'})
qmsg = type('qmsg', (command,), {'name': 'qmsg'})
qrerun = type('qrerun', (command,), {'name': 'qrerun'})
qrls = type('qrls', (command,), {'name': 'qrls'})
qselect = type('qselect', (command,), {'name': 'qselect'})
qsig = type('qsig', (command,), {'name': 'qsig'})
qstat = type('qstat', (command,), {'name': 'qstat'})
qsub = type('qsub', (command,), {'name': 'qsub'})
read = type('read', (command,), {'name': 'read'})
renice = type('renice', (command,), {'name': 'renice'})
rmdel = type('rmdel', (command,), {'name': 'rmdel'})
sact = type('sact', (command,), {'name': 'sact'})
sccs = type('sccs', (command,), {'name': 'sccs'})
sed = type('sed', (command,), {'name': 'sed'})
sh = type('sh', (command,), {'name': 'sh'})
sleep = type('sleep', (command,), {'name': 'sleep'})
split = type('split', (command,), {'name': 'split'})
strings = type('strings', (command,), {'name': 'strings'})
strip = type('strip', (command,), {'name': 'strip'})
stty = type('stty', (command,), {'name': 'stty'})
tabs = type('tabs', (command,), {'name': 'tabs'})
talk = type('talk', (command,), {'name': 'talk'})
tee = type('tee', (command,), {'name': 'tee'})
test = type('test', (command,), {'name': 'test'})
time = type('time', (command,), {'name': 'time'})
tput = type('tput', (command,), {'name': 'tput'})
tr = type('tr', (command,), {'name': 'tr'})
true = type('true', (command,), {'name': 'true'})
tsort = type('tsort', (command,), {'name': 'tsort'})
tty = type('tty', (command,), {'name': 'tty'})
uname = type('uname', (command,), {'name': 'uname'})
uncompress = type('uncompress', (command,), {'name': 'uncompress'})
unexpand = type('unexpand', (command,), {'name': 'unexpand'})
unget = type('unget', (command,), {'name': 'unget'})
unlink = type('unlink', (command,), {'name': 'unlink'})
uucp = type('uucp', (command,), {'name': 'uucp'})
uudecode = type('uudecode', (command,), {'name': 'uudecode'})
uuencode = type('uuencode', (command,), {'name': 'uuencode'})
uustat = type('uustat', (command,), {'name': 'uustat'})
uux = type('uux', (command,), {'name': 'uux'})
val = type('val', (command,), {'name': 'val'})
wc = type('wc', (command,), {'name': 'wc'})  # < TODO - stream. plus figure out piping
what = type('what', (command,), {'name': 'what'})
who = type('who', (command,), {'name': 'who'})
write = type('write', (command,), {'name': 'write'})
yacc = type('yacc', (command,), {'name': 'yacc'})
zcat = type('zcat', (command,), {'name': 'zcat'})

# bash builtins
alias = type('alias', (command,), {'name': 'alias'})
bg = type('bg', (command,), {'name': 'bg'})
bind = type('bind', (command,), {'name': 'bind'})
# break = type('break', (command,), {'name': 'break'})
builtin = type('builtin', (command,), {'name': 'builtin'})
caller = type('caller', (command,), {'name': 'caller'})
# command = type('command', (command,), {'name': 'command'})
compgen = type('compgen', (command,), {'name': 'compgen'})
complete = type('complete', (command,), {'name': 'complete'})
compopt = type('compopt', (command,), {'name': 'compopt'})
# continue = type('continue', (command,), {'name': 'continue'})
declare = type('declare', (command,), {'name': 'declare'})
dirs = type('dirs', (command,), {'name': 'dirs'})
disown = type('disown', (command,), {'name': 'disown'})
echo = type('echo', (command,), {'name': 'echo'})
enable = type('enable', (command,), {'name': 'enable'})
# eval = type('eval', (command,), {'name': 'eval'})
# exec = type('exec', (command,), {'name': 'exec'})
exit = type('exit', (command,), {'name': 'exit'})
export = type('export', (command,), {'name': 'export'})
# false = type('false', (command,), {'name': 'false'})
fc = type('fc', (command,), {'name': 'fc'})
fg = type('fg', (command,), {'name': 'fg'})
getopts = type('getopts', (command,), {'name': 'getopts'})
# hash = type('hash', (command,), {'name': 'hash'})
# help = type('help', (command,), {'name': 'help'})

jobs = type('jobs', (command,), {'name': 'jobs'})
kill = type('kill', (command,), {'name': 'kill'})
let = type('let', (command,), {'name': 'let'})
local = type('local', (command,), {'name': 'local'})
logout = type('logout', (command,), {'name': 'logout'})
mapfile = type('mapfile', (command,), {'name': 'mapfile'})
popd = type('popd', (command,), {'name': 'popd'})
printf = type('printf', (command,), {'name': 'printf'})
pushd = type('pushd', (command,), {'name': 'pushd'})
pwd = type('pwd', (command,), {'name': 'pwd'})
read = type('read', (command,), {'name': 'read'})
readarray = type('readarray', (command,), {'name': 'readarray'})
readonly = type('readonly', (command,), {'name': 'readonly'})
# return = type('return', (command,), {'name': 'return'})
# set = type('set', (command,), {'name': 'set'})
shift = type('shift', (command,), {'name': 'shift'})
shopt = type('shopt', (command,), {'name': 'shopt'})
source = type('source', (command,), {'name': 'source'})
suspend = type('suspend', (command,), {'name': 'suspend'})
# test = type('test', (command,), {'name': 'test'})
times = type('times', (command,), {'name': 'times'})
trap = type('trap', (command,), {'name': 'trap'})
# true = type('true', (command,), {'name': 'true'})
# type = type('type', (command,), {'name': 'type'})
typeset = type('typeset', (command,), {'name': 'typeset'})
ulimit = type('ulimit', (command,), {'name': 'ulimit'})
umask = type('umask', (command,), {'name': 'umask'})
unalias = type('unalias', (command,), {'name': 'unalias'})
unset = type('unset', (command,), {'name': 'unset'})
wait = type('wait', (command,), {'name': 'wait'})

# https://ss64.com/bash/
# PIPE etc?
