"""
not a script

method 1 - oneliner
In [25]: print('{}.{}.{}.{}'.format(*__import__('random').sample(range(0,255),4)))
119.10.191.132

In [26]: print('{}.{}.{}.{}'.format(*__import__('random').sample(range(0,255),4)))
71.38.150.182

In [27]: print('{}.{}.{}.{}'.format(*__import__('random').sample(range(0,255),4)))
90.166.194.180


method 2 - using faker
In [15]: from faker import Faker

In [16]: myfake = Faker()

In [21]: ip_addr = myfake.ipv4()

In [22]: print(ip_addr)
209.176.68.198

or generate a bunch of them

In [28]: [myfake.ipv4() for x in range(10)]
Out[28]:
['186.119.51.191',
 '89.21.194.211',
 '138.190.151.33',
 '161.73.46.16',
 '99.71.198.73',
 '91.11.208.174',
 '109.211.20.243',
 '130.137.122.80',
 '186.169.38.89',
 '194.169.98.125']

"""
