# -*- coding: utf-8 -*-
"""
    domonic.terminal
    ~~~~~
    - call command line functions in python 3
"""


class command():

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        self.params = ''.join([each.__str__() for each in args])
        # self.attributes = ''.join([ ''' %s="%s"''' % (key.split('_',1)[1], value) for key, value in kwargs.items()])

        import subprocess
        cmd = f"{self.name} {self.params}"
        cmd = cmd.strip()

        # print('running: ', cmd)

        returned_output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        # print(returned_output.decode("utf-8"))
        self.result = returned_output.decode("utf-8")

    def __str__(self):
        # return f"{self.name} {self.params}"
        return self.result

    # def __repr__(self):
    #     return f"<{self.name}{self.attributes}>{self.content}</{self.name}>"

    # def __repr__(self):
        # return repr([self.args])
        # return repr(self.result)

    def __getitem__(self, index):
        # return self.args[index]
        return self.result.splitlines()[index]

    # def __setitem__(self,key,value):
        # self.args[key] = value
        # print( self.args[key] )
        # return self.result


ls = type('ls', (command,), {'name': 'ls'})
cd = type('cd', (command,), {'name': 'cd'})
rm = type('rm', (command,), {'name': 'rm'})
ln = type('ln', (command,), {'name': 'ln'})
mkdir = type('mkdir', (command,), {'name': 'mkdir'})
rmdir = type('rmdir', (command,), {'name': 'rmdir'})
touch = type('touch', (command,), {'name': 'touch'})

df = type('df', (command,), {'name': 'df'})
du = type('du', (command,), {'name': 'du'})
ps = type('ps', (command,), {'name': 'ps'})

cat = type('cat', (command,), {'name': 'cat'})
mv = type('mv', (command,), {'name': 'mv'})
cp = type('cp', (command,), {'name': 'cp'})
rm = type('rm', (command,), {'name': 'rm'})

chmod = type('chmod', (command,), {'name': 'chmod'})
chown = type('chown', (command,), {'name': 'chown'})

users = type('users', (command,), {'name': 'users'})
useradd = type('useradd', (command,), {'name': 'useradd'})
userdel = type('userdel', (command,), {'name': 'userdel'})
groups = type('groups', (command,), {'name': 'groups'})
groupadd = type('groupadd', (command,), {'name': 'groupadd'})
groupdel = type('groupdel', (command,), {'name': 'groupdel'})

uniq = type('uniq', (command,), {'name': 'uniq'})
sort = type('sort', (command,), {'name': 'sort'})
dif = type('dif', (command,), {'name': 'dif'})
# cmp = type('cmp', (command,), {'name': 'cmp'})


ssh = type('ssh', (command,), {'name': 'ssh'})
scp = type('scp', (command,), {'name': 'scp'})

more = type('more', (command,), {'name': 'more'})
less = type('less', (command,), {'name': 'less'})
# vi = type('vi', (command,), {'name': 'vi'})
# emacs = type('emacs', (command,), {'name': 'emacs'})
head = type('head', (command,), {'name': 'head'})
tail = type('tail', (command,), {'name': 'tail'})

uptime = type('uptime', (command,), {'name': 'uptime'})
bash = type('bash', (command,), {'name': 'bash'})

'''
def Atag(self,*args,**kwargs):
    tag.__init__(self,*args,**kwargs)
    URL.__init__(self, url=kwargs['_href'])

def __update__(self):
    URL.__update__(self)
    tag.__init__(self,_href=self.href)
    
a = type('a', (tag, Element, URL), {'name': 'a', '__init__':Atag, '__update__':__update__})
'''

# class ls():
#     def __init__(self,content=""):
#         self.content = content
#     def __str__(self):
        # return f"<!-- {self.content} -->"


# help = type('help', (command,), {'name': 'help'})

ping = type('ping', (command,), {'name': 'ping'}) # < TODO - need to stream feedback
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
nautilus = type('nautilus', (command,), {'name': 'nautilus'}) # Linux only?
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
pip = type('pip', (command,), {'name': 'pip'})  # TODO - change to 'python3 -m pip'?
say = type('say', (command,), {'name': 'say'})  # Mac only?
gcc = type('gcc', (command,), {'name': 'gcc'})
jq = type('jq', (command,), {'name': 'jq'})
curl = type('curl', (command,), {'name': 'curl'})
ffmpeg = type('ffmpeg', (command,), {'name': 'ffmpeg'})
convert = type('convert', (command,), {'name': 'convert'})  # imagemagik
figlet = type('figlet', (command,), {'name': 'figlet'})
banner = type('banner', (command,), {'name': 'banner'})  # imagemagik
# youtube-dl = type('youtube-dl', (command,), {'name': 'youtube-dl'}) # TODO - illegal chars
# tree = type('tree', (command,), {'name': 'tree'})
# vim = type('vim', (command,), {'name': 'vim'})
# mail = type('mail', (command,), {'name': 'mail'})


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
command = type('command', (command,), {'name': 'command'})
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
find = type('find', (command,), {'name': 'find'})
fold = type('fold', (command,), {'name': 'fold'})
fort77 = type('fort77', (command,), {'name': 'fort77'})
fuser = type('fuser', (command,), {'name': 'fuser'})
gencat = type('gencat', (command,), {'name': 'gencat'})
get = type('get', (command,), {'name': 'get'})
getconf = type('getconf', (command,), {'name': 'getconf'})
getopts = type('getopts', (command,), {'name': 'getopts'})
head = type('head', (command,), {'name': 'head'})
iconv = type('iconv', (command,), {'name': 'iconv'})
# id = type('id', (command,), {'name': 'id'})
ipcrm = type('ipcrm', (command,), {'name': 'ipcrm'})
ipcs = type('ipcs', (command,), {'name': 'ipcs'})
jobs = type('jobs', (command,), {'name': 'jobs'})
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
man = type('man', (command,), {'name': 'man'})
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
rmdir = type('rmdir', (command,), {'name': 'rmdir'})
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
tail = type('tail', (command,), {'name': 'tail'})
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
command = type('command', (command,), {'name': 'command'})
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
history = type('history', (command,), {'name': 'history'}) # < TODO - NOT WORKING. try with stream method after doing 'ping'
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
