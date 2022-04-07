
if [ $# == 2 ]
then
	echo "Wrong number of argument"
	exit 1
fi

if [[ "$1" =~ ^[a-z][A-Za-z_0-9]*$ ]]
then
	echo "[v] \"$1\" is valid"
else
	echo "[x] \"$1\" is not a valid name"
	exit 1
fi

dir_name="$1"
#module_name="${dir_name^}"
module_name="$(tr '[:lower:]' '[:upper:]' <<< ${dir_name:0:1})${dir_name:1}"

echo "Directory's name: $dir_name"
echo "Module's name: $module_name"

main_file="src/main/scala/$dir_name/$module_name.scala"
test_file="src/test/scala/$dir_name/$module_name.scala"
f_array=()
f_array+=("$main_file")
f_array+=("$test_file")

dir_array=()
dir_array+=("src/main/scala/$dir_name")
dir_array+=("src/test/scala/$dir_name")

echo "Directories to create:"
for i in "${dir_array[@]}"
do printf "     - $i"

if [ -d $i ]; then echo " <- Already exists"
	else echo ""
fi

done

echo "Files to create:"
for i in "${f_array[@]}"
do printf "     - $i"

if [ -e $i ]; then echo " <- Already exists"
	else echo ""
fi

done

while true; do
	echo "Do you want to continue? [y/n] "
	read yn
	if [[ "$yn" == "y" ]]
		then break
	elif [[ "$yn" == "n" ]]
		then exit 0
	fi
done

echo "Creating:"
for i in "${dir_array[@]}"
do echo "     - $i"
mkdir -p $i
done
for i in "${f_array[@]}"
do echo "     - $i"
touch $i
done

# Copy template to source file
cp main.scala.template $main_file
cp test.scala.template $test_file

# Substitute %%MODULE%%
sed -i "s/%%MODULE%%/$module_name/" $main_file
sed -i "s/%%MODULE%%/$module_name/" $test_file

echo ""
echo "SUCCESS"
echo "To open all files in vim:"
printf "> vim -p"
for i in "${f_array[@]}"; do printf " $i"; done
echo ""
