# Verification of the Verilog code

In this directory you will find verification related content

Every directory is named after the verilog file it depends on, each one have they dedicated Makefile.

## Dependencies - Docker

You can setup a docker with (You need Docker installed):
```
cd docker/
sudo docker build -t verificator . # This may take a whike
cd ..
# If your docker daemon is not running: $ sudo dockerd
# You should now be able to list all docker images with: sudo docker image ls

# Everytime you want to run simulations you can use (in the verif/ directory):
sudo docker run -v `pwd`:`pwd` -w `pwd` -it verificator
# You can run test by simply: cd <module to test>/ && make
# Type Ctrl-D or exit when done
```

## Dependencies - Local setup

### Debian/Ubuntu
Under linux / Debian based distribution (Like Ubuntu) you can:
```bash
./configure
```

### Others
For other OS and distribution you will need:
 - ICarus verilog (iverilog)
 - Cocotb (`sudo python3 -m pip install cocotb`)
 - Pytest (`sudo python3 -m pip install pytest`)
 - Optional: Verilator
You can then run simulations:
`cd bram_dual_port/ && make`

## Hardware requirement

There is no special hardware requirement, it should run on any machine which can run python.

## Formal verification
Notion on formal verification: <https://zipcpu.com/blog/2017/10/19/formal-intro.html>


Presentation of the toolchain: <https://yosyshq.readthedocs.io/projects/sby/en/latest/install.html#prerequisites>
