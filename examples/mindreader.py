from time import sleep
from domonic.javascript import Math
ADD = Math.round(Math.random()*5)*2
sleep(1)
print("Let's see if we can read your mind!")
sleep(2)
print("# think of any number. DONT TELL ME. and press return to proceed")
start_number = Math.random()*1000000
sleep(1)
input('ok')
print("# double it")
doubled = start_number*2
sleep(1)
input('ok')
print("# now add ", str(ADD))
added_to = doubled+ADD
sleep(1)
input('ok')
print("# halve it")
halved = added_to/2
sleep(1)
input('ok')
print("# Take away the first number you thought of")
reduced = halved - start_number
sleep(1)
input('ok')
print("# And you are left with:", reduced)



# from time import sleep
# from domonic.javascript import Math
# ADD = Math.round(Math.random()*5)*2
# start_number = Math.random()*1000000
# doubled = start_number*2
# added_to = doubled+ADD
# halved = added_to/2
# reduced = halved - start_number
# assert reduced == ADD/2
