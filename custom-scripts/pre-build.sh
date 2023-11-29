#!/bin/sh

cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
chmod +x $BASE_DIR/target/etc/init.d/S41network-config

cp $BASE_DIR/../custom-scripts/T1/webserver.py $BASE_DIR/target/usr/bin
chmod +x $BASE_DIR/target/usr/bin/webserver.py

cp $BASE_DIR/../custom-scripts/T3/sched_profilerQUEMU $BASE_DIR/target/usr/bin
chmod +x $BASE_DIR/target/usr/bin/sched_profilerQUEMU

cp $BASE_DIR/../custom-scripts/T1/Swebserver $BASE_DIR/target/etc/init.d
chmod +x $BASE_DIR/target/etc/init.d/Swebserver

make -C $BASE_DIR/../modules/simple_driver/

cp $BASE_DIR/../disk-test/hello $BASE_DIR/target/usr/bin
chmod +x $BASE_DIR/target/usr/bin/hello