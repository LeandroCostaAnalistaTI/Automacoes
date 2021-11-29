#!/bin/bash

declare -i test=0
declare -i col=$(echo "$1" | sed 's/\./ /g' | awk '{print NF}')
tools="nmap,dirb,gobuster,enum4linux,nikto,whatweb,exploitdb,dirb" #exploitdb = searchsploit

echo

recon () {
	local host=$1
	local wordlistpath=$(locate /common.txt -n1)
	#report=$1-report.ml
	report="$host-Recon"
	mkdir $report
	# chmod 666 $report
	newline="\n(#################################################################################################################################################################)\n(#################################################################################################################################################################)\n(#################################################################################################################################################################)\n"

	# echo -e "Running Masscan..."
	# masscan -p 1-65535 $host --rate=10000 -oG masscan-$host.txt
	# chmod 666 masscan-$host.txt

	# Collecting open ports
	# ports=$(cat masscan-$host.txt | grep "Ports:" | cut -d ':' -f4 | cut -d '/' -f1| sed 's/\///g' | tr '\n' ',' | sed 's/.$//g' | sed 's/ //g')

	echo -e "\n ---> Running Nmap\n -----> nmap -sS -sC -A -Pn -p- $host -oX nmap.xml"
	# nmap -A -sC -v -Pn -p $ports $host -oX nmap.xml >> $report
	nmap -sS -sC -A -Pn -p- $host -oX nmap.xml >> $report/nmap.ml

	echo -e $newline >> $report

	echo -e "\n ---> Running Dirb\n -----> dirb http://$host $wordlistpath -S\n -----> dirb https://$host $wordlistpath -S"
	#gobuster dir -u http://$host -w $(locate directory-list-2.3-medium.txt -n1) -e -x php,html,txt,xml -t 20 -z --no-error >> $report
	dirb http://$host $wordlistpath -S >> $report/dirb.ml
	echo -e $newline >> $report/dirb.ml
	dirb https://$host $wordlistpath -S >> $report/dirb.ml

	#echo -e $newline >> $report

	echo -e "\n ---> Running Gobuster\n -----> gobuster dir -u http://$host -w $wordlistpath -e -x php,html,txt -t 20 -z --no-errorn -----> gobuster dir -u http://$host -w $wordlistpath -e -x php,html,txt -t 20 -z --no-error -k"
	#gobuster dir -u http://$host -w $(locate directory-list-2.3-medium.txt -n1) -e -x php,html,txt,xml -t 20 -z --no-error >> $report
	gobuster dir -u http://$host -w $wordlistpath -e -x php,html,txt -t 20 -z --no-error >> $report/gobuster.ml
	echo -e $newline >> $report/gobuster.ml
	gobuster dir -u https://$host -w $wordlistpath -e -x php,html,txt -t 20 -z --no-error -k >> $report/gobuster.ml

	#echo -e $newline >> $report

	echo -e "\n ---> Running Enum4linux\n -----> enum4linux $host | grep -v "unknown""
	enum4linux $host | grep -v "unknown" >> $report/enum4linux.ml

	#echo -e $newline >> $report

	echo -e "\n ---> Running Nikto\n -----> nikto -host $host"
	nikto -host $host >> $report/nikto.ml

	#echo -e $newline >> $report

	echo -e "\n ---> Running WhatWeb\n -----> whatweb --color=never --no-errors -a 3 -v $host"
	whatweb --color=never --no-errors -a 3 -v $host >> $report/whatweb.ml

	#echo -e $newline >> $report

	echo -e "\n ---> Running Searchsploit\n -----> searchsploit --nmap nmap.xml"
	searchsploit --nmap nmap.xml > aux.ml 
	cat -v aux.ml | sed 's/\^\[\[01;31m\^\[\[K//g' > aux2.ml
	cat -v aux2.ml | sed 's/\^\[\[m\^\[\[K//g' >> $report/searchsploit.ml
	
	#echo -e $newline >> $report

	#rm -f masscan-$host.txt 
	rm -f nmap.xml
	rm -f aux.ml
	rm -f aux2.ml
}

if [[ $(whoami) != 'root' || $# -ne 1 || $col -ne 3 && $col -ne 4 ]]
then
	echo -e "This script need to:\n 1) Be executed as ROOT\n 2) Receive the NETWORK or TARGET HOST as parameter\n"
	echo -e "Examples: "
	echo -e "\t Network ---> sudo ./recon.sh 10.11.1"
	echo -e "\t Host\t ---> sudo ./recon.sh 10.11.1.1"
	echo
else
	for tool in $(echo -e $tools | sed 's/,/\n/g')
	do
		if [[ $(dpkg -l $tool 2>/dev/null) = "" ]]
		then
			test=1
			echo "The tool: >>> $tool <<< need to be installed!!!"
		fi
	done
	if [[ $test -eq 1 ]]
	then
		echo -e "\nInstall the required tool(s) and re-run the script...\n\n"
	else 
		for ip in $(seq 1 255)
		do
			if [[ $col == 4 ]]
			then
				host=$1
				echo -e "\n >>>>> HOST $host SCAN STARTED <<<<<"	
				ip=255
			else
				if [[ $ip == 0 ]]
				then
					echo -e "\n >>>>> NETWORK $host.1/24 SCAN STARTED <<<<<"
				fi
				host=$1.$ip
			fi
			
			recon $host

			# Check if was passed a network or host, if it was a host it break the for loop
			if [[ $col == 4 ]]
			then
				break
			fi
		done
		echo -e "\n --- FINISHED ---"
	fi
fi
