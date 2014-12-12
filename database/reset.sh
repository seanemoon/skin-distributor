#!/bin/bash

if [ -z $SKIN_DIST_DATABASE ]; then
    echo No database specified, defaulting to test database.
    SKIN_DIST_DATABASE=skintest
fi

psql $SKIN_DIST_DATABASE < DROP.sql
psql $SKIN_DIST_DATABASE < CREATE.sql
