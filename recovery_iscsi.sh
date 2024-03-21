#!/bin/bash

status=$(docker ps -a  | grep -E postgres.+Up -c  2> /dev/null)

if [ "$status" -eq "0" ] ; then
	docker ps -a  | awk '/postgre/{print "docker stop "$1}' 2> /dev/null | bash
	umount /mnt --force
	iscsiadm --mode node --logoutall=all
	umount /mnt --force
	sleep 5
	service iscsi restart
	sleep 5
	mount /dev/sda1  /mnt
	docker ps -a  | awk '/postgre/{print "docker start "$1}' 2> /dev/null | bash
fi
