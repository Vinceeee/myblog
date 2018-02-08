#!/bin/bash

if [[ $? == 0 ]];then
mysql -uroot -p123456<<EOF
create database mydb;
create user my;
grant all PRIVILEGES on mydb.* to my identified by '123456';
EOF
fi

if [[ $? == 0 ]];then
  echo "DB config succeeded !"
fi
