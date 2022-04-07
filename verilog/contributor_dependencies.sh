
echo "You shouldn't blindly execute a script from internet, read it first"
exit 1
# You can delete everything above this comment


apt install python3
python3 -m pip install python-dev-tools

# verilog simulators
sudo apt install iverilog verilator

# Static timing analysis
sudo apt install opensta

# Synthesis
sudo apt install yosys

# Convert systemVerilog to Verilog
# required to compile sv2v
sudo apt install haskell-platform
git clone https://github.com/zachjs/sv2v.git
cd sv2v/
sudo cp bin/sv2v /usr/bin/

# Writing testcases in python
python3 -m pip install cocotb

# Lint and format
mkdir -p ~/.bin/
cd ~/.bin/
wget https://github.com/chipsalliance/verible/releases/download/v0.0-2096-g52b8f79b/verible-v0.0-2096-g52b8f79b-Ubuntu-20.04-focal-x86_64.tar.gz
tar xvf verible-v0.0-2096-g52b8f79b-Ubuntu-20.04-focal-x86_64.tar.gz
export PATH="$PATH:~/.bin/verible-v0.0-2096-g52b8f79b/bin"
# Also add this export in your .bashrc
