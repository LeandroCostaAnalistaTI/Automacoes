#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import time, sys, os
from subprocess import PIPE, Popen
from pathlib import Path
#from db import DB


def main():
    issu()

     #conectando com o banco
    #db = DB("ec2-3-225-30-189.compute-1.amazonaws.com", "d3503a8lv953eh", "jyyfsvutdccsds", "dbff6778cdd9c5e787c459110680caf74ce277d84ece6c27590202b44f17d988")

    folder = input("Vamos criar uma pasta para salvar os arquivos, digite um nome pra ela: ")
    #cria a pasta
    os.mkdir(folder)
    # acessa a pasta
    os.chdir(folder)

    # informa o host: site.com | 127.0.0.1
    url = input("digita a url: ")

    
    varrerOsint(url)
    varrerDNS(url)
    varrerURL(url)
    varrerVulnerabilidade(url)
    varrerSSL(url)

#verifica se está com super usuário
def issu():
    if os.geteuid() != 0:
        for i in range(3):
            print("\033[93m              Este programa precisa ser executado em modo ROOT!!\n\n")
            time.sleep(0.5)
        print("\033[93m                      Exemplo: sudo python3 planoBasico.py")
        time.sleep(2)
        os.system('clear')
        sys.exit(0)
    else:
        pass

#processos | pega a saída
def cmd(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    for line in process.stdout:
        print(str(line))
        
    return process.communicate()[0]


#======== ANALISE DE VULNABILIDADES ===================
def varrerVulnerabilidade(url):
    print("Estamos no momento executando as ferramenta de subdominios... por favor, aguarde um momento!")
    cmd('subfinder -d ' + url + ' | assetfinder -subs-only ' + url + ' | httpx -silent -threads 1000 | gauplus | nuclei  -t /root/nuclei-templates/ -o resultnuclei')
    cmd('subfinder -d ' + url + ' | assetfinder -subs-only ' + url + ' | httpx -silent -threads 1000 | gauplus | jaeles scan -c 100')
    cmd('subfinder -d ' + url + ' | assetfinder -subs-only ' + url + ' | httpx -silent -threads 1000 | gauplus | dalfox pipe --mining-dict-word /root/wordlist/dalfox/params.txt |anew dalfox ')
    print("Ferramenta de subdominios executada, vamos para a próxima")
    time.sleep(2)
    
    

# =============  OSINT =================================
def varrerOsint(url):
# wafwoof
    print("Estamos no momento executando a ferramenta wafw00f... por favor, aguarde um momento!")
    cmd('wafw00f -v ' + url + ' > saidawafwoof')
    print("wafw00f executada, vamos para a próxima")
    # deixa esperar uns segundinhos só para ficar mais legal
    time.sleep(2)

    # whois
    print("Estamos no momento executando a ferramenta whois... por favor, aguarde um momento!")
    cmd('whois ' + url + ' > whois.csv ')
    print("whois executada, vamos para a próxima")
    # deixa esperar uns segundinhos só para ficar mais legal
    time.sleep(2)

    #censys
    print("Estamos no momento executando a ferramenta censys... por favor, aguarde um momento!")
    cmd('censys search ' + url + ' > censys.csv')
    cmd('censys search --index-type hosts ' + url + ' > censys.csv')
    cmd('censys search --index-type certs ' + url + ' > censys.csv')
    cmd('censys search --index-type ipv4 ' + url + ' > censys.csv')
    print("censys executada, vamos para a próxima")
    time.sleep(2)

    #nmap
    print("Estamos no momento executando a ferramenta nmap... por favor, aguarde um momento!")
    cmd('nmap -p- -v ' + url + ' -oN reconPortas')
    cmd('nmap -p- -v --script=vuln ' + url + ' -oN reconVuln')
    cmd('nmap -sC -sS -sV -v -Pn -p- ' + url + ' -oN reconNmap ')
    #cmd('nmap --script=http-methods --script-args http-methods.retest=value,http-methods.test-all=value' + url + ' -oN reconMethodos')
    #('nmap -p 21 -T5 --script ftp* ' + url + ' -oN reconFTP')
    print("nmap executada, vamos para a próxima")
    time.sleep(2)

    # METAGOOFIL
    print("Estamos no momento executando a ferramenta metagoofil... por favor, aguarde um momento!")
    cmd('metagoofil -d ' + url + ' -t pdf,doc,xls,ppt,odp,ods,docx,xlsx,pptx -l 200 -n 10 -o saidaMetagoofil')
    print("metagoofil executada, vamos para a próxima")
    time.sleep(2)
    
    #theHarvester 
    print("Estamos no momento executando a ferramenta theHarvester... por favor, aguarde um momento!")
    cmd('theHarvester -d ' + url + ' -b all > saidatheharvester')
    print("theHarvester executada, vamos para a próxima")    
    time.sleep(2) 

     # enum4linux

    cmd('enum4linux ' + url + ' > enum4.txt')
   
   # Nikto
    cmd('nikto -host ' + url + ' > nikto.txt')

    # whatweb

    cmd('whatweb ' + url + ' > whatwe.txt')

   

    # AMASS
    cmd('amass enum -d ' + url + ' > saidaamass')   


#processos | pega a saída
def cmd(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    for line in process.stdout:
        print(str(line))

    return process.communicate()[0]    

#=================ANALISE DE DNS ================================


def varrerDNS(url):

    print("Estamos no momento executando as ferramentas de DNS... por favor, aguarde um momento!")
    cmd('dnsmap ' + url + ' > saidasdnsmap')
    cmd('dig NS ' + url + ' > saidadigNS')
    cmd('dig MX ' + url + ' > saidadigTX')
    cmd('host ' + url + ' > saidaHost')
    cmd('host -t mx ' + url + ' > saidaHostMX')
    cmd('host -t ns ' + url + ' > saidaHostNS')
    cmd('dnsrecon -d ' + url + ' > saidadnsrecon')
    print("As ferramentas de DNS executadas, vamos para a próxima")
    time.sleep(2)

# =================ANALISE DE CABEÇARIO =========================

def varrerURL(url):

    #SITE :securityheaders.com 
    print("Estamos no momento executando a ferramenta curl... por favor, aguarde um momento!")
    cmd('curl -skI ' + url + ' > saidaCurlCabeçario.csv')
    print("curl executada, vamos para a próxima")
    time.sleep(2)
    

 #securityheaders 
    print("Estamos no momento executando a ferramenta securityheaders... por favor, aguarde um momento!")

    
    cmd('python3 /home/securityheaders/securityheaders.py --flatten ' + url + ' > cabecario.csv')
           
    print("securityheaders executada, vamos para a próxima")
    time.sleep(2)
    # volta para a pasta padrão
    

# ==============SCANNER DE SSL =======================================

def cmd(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    for line in process.stdout:
        print(str(line))

    return process.communicate()[0]

# CTFR
def varrerSSL(url):

    print("Estamos no momento executando a ferramenta ctfr... por favor, aguarde um momento!")
    # aqui pega a pasta atual que tu criou.
    
        # executa o programa
    cmd('python3 /home/ctfr/ctfr.py -d ' + url + ' > saidaCtfr.csv')
         
    print("ctfr executada, vamos para a próxima")
    time.sleep(2)

   

    # SSLYZE
    print("Estamos no momento executando a ferramenta sslyze... por favor, aguarde um momento!")
    cmd('sslyze ' + url + ' :443 > saidaSSL.csv')
    print("sslyze executada, vamos para a próxima")
    time.sleep(2)

# VERIFICAR DOMINIOS SEMELHANTES
    print("Estamos no momento executando a ferramenta urlcrazy... por favor, aguarde um momento!")
    

    # URLCRAZY
   
    cmd('urlcrazy -k azerty ' + url + ' > saidaurlcrazy.csv')
    
              
    print("urlcrazy executada, Fim da execução do Script")
    time.sleep(2)

    

#processos | pega a saída
def cmd(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    for line in process.stdout:
        print(str(line))

    return process.communicate()[0] 

if __name__ == '__main__':
    main()