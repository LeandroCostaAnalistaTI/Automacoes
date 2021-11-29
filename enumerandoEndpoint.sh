#!/bin/bash

#Ferramentas necessarias para o funcionamento do programa subfinder, assetfinder , httpx ,xargs ,findomain,gauplus,anew,nuclei,jaeles e dalfox
echo "ATENÇÃO!! A FERRAMENTA TEM QUE SER EXECUTADA COMO SUDO PARA FUNCIONAR"


echo Vamos criar uma pasta para salvar os arquivos, digite um nome pra ela:
read pasta

mkdir $pasta
cd $pasta


echo digita a url:
read url

subfinder -d $url | assetfinder -subs-only $url | httpx -silent -threads 1000 | xargs -I@ sh -c 'findomain -t @ -q | httpx -silent | anew | gauplus | anew dominios';
    cat dominios | httpx -silent | anew 200gauplus ;

cat 200gauplus | gf xss | httpx -silent -threads 1000 | anew xss; cat 200gauplus | gf lfi | httpx -silent -threads 1000 | anew lfi; cat 200gauplus| gf redirect | httpx -silent -threads 1000 | anew redirect; cat 200gauplus | gf rce | httpx -silent -threads 1000 | anew rce; cat 200gauplus | gf ssti | httpx -silent -threads 1000 | anew ssti; cat 200gauplus | gf sqli |  httpx -silent -threads 1000 | anew sqli; cat 200gauplus | gf idor | httpx -silent -threads 1000 | anew idor; cat 200gauplus | gf ssrf| httpx -silent -threads 1000 | anew ssrf
