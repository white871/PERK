bash bash_tlv 

( speaker-test -t sine -f 1000 )& pid=$! ; sleep 0.2s ; kill -9 $pid
( speaker-test -t sine -f 1500 )& pid=$! ; sleep 0.2s ; kill -9 $pid

source home/perk/pyperk/bin/activate; python home/perk/transliteration.py