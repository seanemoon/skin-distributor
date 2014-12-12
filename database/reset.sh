#!/bin/bash

if [ -z $SKIN_DIST_DATABASE ]; then
    echo No database specified, using default database.
    SKIN_DIST_DATABASE='distributor.db'
    touch $SKIN_DIST_DATABASE
fi

sqlite3 $SKIN_DIST_DATABASE < DROP.sql
sqlite3 $SKIN_DIST_DATABASE < CREATE.sql
