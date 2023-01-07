# generate a list of randomized mac addresses to use as replacement fields when scrubbing capture data
# in shell
# user@machine$ printf '02:00:00:%02X:%02X:%02X\n' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256))
# 02:00:00:AD:DB:62

printf '02:00:00:%02X:%02X:%02X\n' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256))

# In python
# In [29]: "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
#     ...: random.randint(0, 255),
#     ...: random.randint(0, 255))
# Out[29]: '02:00:00:b0:65:c6'
# 
# In [30]: "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
#     ...: random.randint(0, 255),
#     ...: random.randint(0, 255))
# Out[30]: '02:00:00:fa:a2:99'
# 
# In [31]: "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
#     ...: random.randint(0, 255),
#     ...: random.randint(0, 255))
# Out[31]: '02:00:00:cb:6b:77'

# in python using faker
# In [15]: from faker import Faker
# 
# In [16]: myfake = Faker()
# 
# n [33]: [myfake.mac_address() for x in range(5)]
# Out[33]:
# ['c2:c2:c4:16:26:36',
#  '49:c0:d3:f7:dd:0e',
#  'ef:21:77:74:8d:6d',
#  'b7:8f:46:a1:d2:d7',
#  'b1:7e:5a:74:f1:59']
