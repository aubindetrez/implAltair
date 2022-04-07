#!/usr/bin/env bash
verif_path="`pwd`"
targets=(bram_dual_port  bram_single_port pu_add_cmp pu_bitwise)
for i in ${targets[*]}
do
	cd ${verif_path}/$i
	make
	make clean
	rm -rf __pycache__ results.xml
done
