#!/bin/bash

VALUES=(0x01 0x02 0x04 0x08 0x10 0x20 0x40 0x80)

for a in "${VALUES[@]}"; do
  #for b in "${VALUES[@]}"; do
    #for c in "${VALUES[@]}"; do
      a_hex=$(printf "%02x" $a)
      #b_hex=$(printf "%02x" $b)

      printf "\x10\x$a_hex\x20\x10\x01\x20" > /tmp/inputfile

      xxd /tmp/inputfile

      # Run the binary with 1 second timeout
      timeout 1s bash -c '/challenge/babyrev-level-22-1 < /tmp/inputfile'
      exitcode=$?

      echo "$payload -> exit code: $exitcode"

      if [ $exitcode -eq 255 ]; then
        echo "Found working input: $payload"
        #exit 0
      fi
    #done
  #done
done
