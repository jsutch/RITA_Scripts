HOST='myhost'
for x in `rita show-long-connections myhost| grep -v Dest| awk -F, '{print $2}'`
> do
> echo "$x: $(whois -h whois.cymru.com " -v $x"| grep -v BGP)";
> done
