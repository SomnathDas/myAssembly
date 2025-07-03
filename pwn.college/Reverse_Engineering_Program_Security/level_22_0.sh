#!/bin/bash

VALUES=(0x01 0x02 0x04 0x08 0x10 0x20 0x40 0x80)

VALUES_REG=(0x01 0x02 0x08 0x20 0x40)
VALUES_OP=(0x80)

for a in "${VALUES_REG[@]}"; do
  #for b in "${VALUES_REG[@]}"; do
    #for c in "${VALUES[@]}"; do
      a_raw=$(printf '\\x%02x' $a)
      #b_raw=$(printf '\\x%02x' $b)
      printf "\x69\x01\x02\x01\x00\x40\x01\x00\x40\x01\x00\x40$a_raw\x10\x01\x10\x01\x20" > /tmp/inputfile

      xxd /tmp/inputfile

      timeout 1s bash -c '/challenge/babyrev-level-22-1 < /tmp/inputfile'
      exitcode=$?

      echo "$payload -> exit code: $exitcode"

      if [ $exitcode -eq 130 ]; then
        echo "Found working input: $payload"
        #exit 0
      fi
    #done
  #done
done

