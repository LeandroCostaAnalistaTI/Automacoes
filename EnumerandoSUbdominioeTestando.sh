#!/bin/bash

#Ferramentas necessarias para o funcionamento do programa subfinder, assetfinder , httpx ,xargs ,findomain,gauplus,anew,nuclei,jaeles e dalfox

echo Vamos criar uma pasta para salvar os arquivos, digite um nome pra ela:
read pasta

mkdir $pasta
cd $pasta


echo digita a url:
read url

subfinder -d $url | assetfinder -subs-only $url | httpx -silent -threads 1000 | xargs -I@ sh -c 'findomain -t @ -q | httpx -silent | anew | gauplus | anew dominios';
    cat dominios | httpx -silent | anew 200gauplus ;
    cat 200gauplus | xargs -I@ dalfox url @ | anew dalfox ;
    cat 200httpx | nuclei -t /root/nuclei-templates/ -o resultnuclei
    cat 200gauplus |jaeles scan -c 100
    








| 
