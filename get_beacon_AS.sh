HOST='mybox'
for x in `rita show-beacons ${HOST}|grep -v Source |awk -F, '{if ($1 > .8) print $3}'`
do
    echo "$x: $(whois -h whois.cymru.com " -v $x"| grep -v BGP)"
done
