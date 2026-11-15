#!/bin/bash


date=$(date +'%Y-%m-%d %I:%M:%S %p')
battery=$(acpi -b)

echo "$battery | $date" 
