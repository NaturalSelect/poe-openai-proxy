#!/bin/bash

LOG_LEVEL=${log_level}
P_B=${p_b_token}
P_LAT=${p_lat_token}

cd /root/poe-openai-proxy

if test -z ${PROXY}
then
    python3 main.py -l ${LOG_LEVEL} -b ${P_B} --lat ${P_LAT}
else
    python3 main.py -l ${LOG_LEVEL} -b ${P_B} --lat ${P_LAT} --proxy ${PROXY}
fi