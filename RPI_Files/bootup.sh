bash setup_tlv.sh

#( speaker-test -t sine -f 1000 )& pid=$! ; sleep 0.2s ; kill -9 $pid
#( speaker-test -t sine -f 1500 )& pid=$! ; sleep 0.2s ; kill -9 $pid

pyperk/bin/python transliteration.py

