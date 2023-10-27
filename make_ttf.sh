#!/bin/bash

BeQuet=0
DoForce=0
CharMap=""
FindMap=""
FileOut=""
SvgList=()

for i in "$@"; do
  case $i in
	--help | -h)
	  echo ""
	  echo " script [options] 1.svg 2.svg ..."
	  echo ""
	  echo "  --help, -h       show this help"
	  echo "  --quet, -q       don't print the"
	  echo "  --force, -f      Force char map [default: false]"
	  echo "                   (if true, the script will continue"
	  echo "                   to add all found <symbol> to the font"
	  echo "                   after filling the user setts char map.)"
	  echo ""
	  echo "  -C=* [optional]  string char map like -C=\"ABC\"" 
	  echo "  -F=* [optional]  list of elements to be found by ID"
	  echo "                   like: -F=\"'glyph A','glyph B','glyph С'\""
	  echo "  -O=*             Write output TTF font [default: result.ttf]"
	  echo ""
	  exit
	  ;;
	--quet | -q)
	  BeQuet=1 ;;
	--force | -f)
	  DoForce=1 ;;
	-C=*)
	  CharMap="${i#*=}" ;;
	-F=*)
	  FindMap="${i#*=}" ;;
	-O=*)
	  FileOut="${i#*=}" ;;
	*.svg)
	  SvgList+=("'$i'")
	  ;;
  esac
done

Args=()
fonico_dir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
toJoin_Svg=$(IFS=','; echo "${SvgList[*]}")

if [ "$toJoin_Svg" == "" ]; then
	Args+=("['$fonico_dir/fonico.svg']")
else
	Args+=("[$toJoin_Svg]")
fi

if   [ "$FileOut" != "" ]; then
	Args+=("'$CharMap'" "[$FindMap]" "'$FileOut'")
elif [ "$FindMap" != "" ]; then
	Args+=("'$CharMap'" "[$FindMap]")
elif [ "$CharMap" != "" ]; then
	Args+=("'$CharMap'")
fi

pyver=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
npmver=""

toJoin_Args=$(IFS=','; echo "${Args[*]}")
toPrint_Args=" \033[1mSymbols2TTF_main\033[0m(
$(
	for arg in ${Args[@]}; do
		echo "    $arg,";
	done 
)\n )"

if [ "$pyver" != "" ]; then

	if [ $BeQuet == 0 ]; then
		echo -e "\n## Run Python ($pyver) script ##\n\n$toPrint_Args"
	fi

	python3 -c "
import sys; sys.path.append('$fonico_dir')
import Symbols2TTF; Symbols2TTF.fromSvgList($toJoin_Args)"

elif ["$npmver" != ""]; then

	if [ $BeQuet == 0 ]; then
		echo -e "\n/** Run Node ($npmver) script **/\n\n$toPrint_Args"
	fi

	npm update
	node Symbols2TTF.js $@
else
	echo "install Python3 or Node.js"
	exit
fi
