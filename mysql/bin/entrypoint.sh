#!/bin/bash

if [[ $? == 0 ]];then
mysql -uroot -p123456<<EOF
create database tangdb;
create user tang;
grant all PRIVILEGES on tangdb.* to tang identified by '123456';
EOF
fi

if [[ $? == 0 ]];then
  echo "DB config succeeded !"
fi
