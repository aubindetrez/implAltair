sudo apt install default-jdk curl make autoconf

if [ `apt-cache search ^sbt$ | wc -l` == 0 ]
then
	echo "[x] 'sbt' is not available in apt, adding the repository..."
	echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | sudo tee /etc/apt/sources.list.d/sbt.list
	echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | sudo tee /etc/apt/sources.list.d/sbt_old.list
	curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add
	sudo apt-get update
fi
sudo apt-get install sbt

# An other alternative would be to checkout verilator from github and get version v4.016
sudo apt install verilator
# Dependencies to build verilator from source
#sudo apt install default-jdk curl git make autoconf g++ flex bison

exit 0
git clone https://github.com/chipsalliance/chisel3.git
cd chisel3
sbt compile
sbt publishLocal
