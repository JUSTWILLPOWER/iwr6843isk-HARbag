#!/bin/bash

action=(boxing wave jack jump walk squats)

for i in ${action[@]}
do
	files=`ls ${i}*`
	for file in ${files[@]}
	do
		rosbag info $file | grep -E "path|duration"
	done
done
