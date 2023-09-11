#!/bin/sh

cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
chmod +x $BASE_DIR/target/etc/init.d/S41network-config

cp $BASE_DIR/../custom-scripts/T1/webserver.py $BASE_DIR/target/usr/bin
chmod +x $BASE_DIR/target/usr/bin/webserver.py

cp $BASE_DIR/../custom-scripts/T1/Swebserver $BASE_DIR/target/etc/init.d
chmod +x $BASE_DIR/target/etc/init.d/Swebserver