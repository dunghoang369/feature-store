#!/bin/bash
./run.sh register_connector configs/postgresql-cdc.json
python create_table.py
python insert_table.py
