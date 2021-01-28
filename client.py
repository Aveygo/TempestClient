
import argparse

version = 'v1.0.7'

"""
logs:

1.0.7
packaged

"""


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pool", help="Connects to a custom pool", type=str)
parser.add_argument("-o", "--port", help="Port to connect pool with", type=str)
parser.add_argument("-s", "--server", help="Tempest server IP - not recommended to change",type=str)
parser.add_argument("-n", "--name", help="Mine under a user's name", type=str)
parser.add_argument("-e", "--eula", help="Skip eula (1/0)", type=str)

args, unknown = parser.parse_known_args()

try:
    import os, time, socket, random, json, shutil, platform, requests, string, os, subprocess, _thread, sys
    from pythonping import ping
    from elevate import elevate
    from termcolor import colored

    if ('Windows' in platform.system() or 'linux' in platform.system()): elevate()

    if 'Windows' in platform.system(): os.system('cls')
    else: os.system('clear')

    print('Tempest Coin Client - Login')
    print('')

    if not ('Linux' in platform.system() or 'Windows' in platform.system()):
        print(colored('WARNING - you are not on a supported device (not linux or windows), assuming running mac which is not natively supported', 'red'))
        print('')

    if not args.name:
        name = input('Username on tempest.my.to ( case sensitive ) > ')
        response = requests.get('http://tools.glowingmines.eu/convertor/nick/' + name)
        confirm = input('Offline UUID : ' + str(json.loads(response.text)['offlinesplitteduuid']) + '? (y/n) > ')
        if not 'y' in confirm and not confirm=='':
            print('Please ask CodingCoda on discord or email dmitri.shevchenko.au@gmail.com for help signing in with UUID...')
            sys.exit()
        uuid = json.loads(response.text)['offlinesplitteduuid'].replace('-', '')
    else:
        name = args.name
        response = requests.get('http://tools.glowingmines.eu/convertor/nick/' + name)
        uuid = json.loads(response.text)['offlinesplitteduuid'].replace('-', '')
    
    print('Please wait as a connection to the server is made...')

    import socket
    import pickle

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        if args.server:
            s.connect((args.server, 8030))
        else:
            s.connect(('tempest.my.to', 8030))
    except:
        print('Cannot connect to server, possibly serving too many clients ? ...')
        sys.exit()

    data = {'headers' : {'status':'test'}, 'body':{'action':'get_account', 'uuid':uuid, 'name':name}}

    try:
        response = s.send(pickle.dumps(data) + '@'.encode('utf-8'))
        data = pickle.loads(s.recv(1024))
        wallet = data['body']['wallet_account']
        s.close()
    except Exception as e:
        print('Connection failed? ' + str(e))
        print('Server gave bad response')
        sys.exit()


    print('Connection made with server!')

    if 'Windows' in platform.system(): os.system('cls')
    else: os.system('clear')

    def eula():
        print('EULA ( of sorts ) + Info')
        print('This program is used to mine crypto on your computer to support')
        print('the tempest minecraft server (tempest.my.to).')
        print('Miners are rewarded with in game currency hourly reflecting how much')
        print('work they put into mining (subject to change - see discord).')
        print('')
        print('Any rewards that were linked to an account not on the server will go to a daily')
        print('lottery. Make sure your username is correct to prevent this.')
        print('')
        print('----- Client info -----')
        print('User : ' + str(name))
        print('UUID : ' + str(uuid))
        print('')
        print('----- Extra info -----')
        print('Wallet : ' + str(wallet))
        print('Version: ' + str(version))
        print('')
        print('ENTER to continue, ctrl + c to cancel')

        result = input('')

    if args.eula:
        if 't' in args.eula or '1' in args.eula or 'y' in args.eula:
           eula()
        else:
            pass
    else:
        eula() 

    print('Running setup...')
    
    client_info = {}

    links = {'linux':{
            'type':'.tar.gz',
            '8':'https://github.com/ethereum-mining/ethminer/releases/download/v0.18.0/ethminer-0.18.0-cuda-8-linux-x86_64.tar.gz',
            '9':'https://github.com/ethereum-mining/ethminer/releases/download/v0.18.0/ethminer-0.18.0-cuda-9-linux-x86_64.tar.gz'
        },
        'windows': {
            'type':'.zip',
            '8':'https://github.com/ethereum-mining/ethminer/releases/download/v0.18.0/ethminer-0.18.0-cuda8.0-windows-amd64.zip',
            '9':'https://github.com/ethereum-mining/ethminer/releases/download/v0.18.0/ethminer-0.18.0-cuda9.1-windows-amd64.zip',
            '10':'https://github.com/ethereum-mining/ethminer/releases/download/v0.18.0/ethminer-0.18.0-cuda10.0-windows-amd64.zip'
        }}

    version = os.popen('nvcc --version').read()

    try:
        version = int(version.split('release ')[1].split('.')[0])
    except:
        version = '9'

    client_info['nvcc'] = version

    if 'Windows' in platform.system():
        client_info['system'] = 'windows'
        os.system('cls')
    elif 'Linux' in platform.system():
        client_info['system'] = 'linux'
        os.system('clear')
    else:
        client_info['system'] = 'mac'
        os.system('clear')

    print('Loading, please wait (~2 minutes depending on internet speed)...')

    servers = ['eth-eu1.nanopool.org', 'eth-eu2.nanopool.org', 'eth-us-east1.nanopool.org', 'eth-asia1.nanopool.org', 'eth-jp1.nanopool.org', 'eth-au1.nanopool.org']
    servers_result = {}

    try:
        for i in servers: servers_result[i] = ping(i, size=40, count=10).rtt_avg_ms

        fastest_server = list(servers_result.keys())[list(servers_result.values()).index(min(servers_result.values()))]
        port = '9999'
    except:
        fastest_server = 'eth-eu1.nanopool.org'
        port = '9999'

    if args.pool:
        fastest_server = str(args.pool)
        if not args.port:
            print('Must declare port when using custom pool address')
        else:
            fastest_server = str(args.pool)

    pool = {'address': fastest_server, 'port':port, 'wallet':wallet, 'name':'tempest'}
    
    try:
        if not version in links[client_info['system']].keys():
            client_info['nvcc'] = '9'
    except:
        client_info['nvcc'] = '9'
        
    client_info['ip'] = requests.get('https://api.ipify.org').text

    def mine_coin():
        if not client_info['system'] == 'mac':
            r = requests.get(links[client_info['system']][client_info['nvcc']], allow_redirects=True)
            open('ethminer'+links[client_info['system']]['type'], 'wb').write(r.content)
            shutil.unpack_archive('ethminer'+links[client_info['system']]['type'], 'ethminer')
        
        command = '-P stratum1+tcp://' + pool['wallet'] +'@' + pool['address'] + ':' + pool['port']

        if client_info['system'] == 'windows':
            mine_proc = subprocess.Popen('"ethminer\bin\ethminer.exe" ' + command, shell = True) 
        elif client_info['system'] == 'linux': 
            mine_proc = subprocess.Popen('ethminer/bin/ethminer ' + command, shell = True)
        else:
            os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
            os.system('brew install cpp-ethereum')
            os.system('brew tap ethereum/ethereum')
            mine_proc = subprocess.Popen('ethminer ' + command, shell = True)

        while mine_proc.poll() == None:
            time.sleep(1)
        
        time.sleep(10)
    
    def information():
        information = """
        Tempest Client (or Tempest Coin) is an ethereum-based mining solution to 
        generate revenue for tempest.my.to (a minecraft server). 
        
        It was designed to be as simple as possible to use, where users mined 
        etherirum into a wallet linked to their account that is check hourly 
        and converted into in game currency. 
        
        The ethereum left over is then used as revenue (converted into real cash) for the server.

        This particular client only mines on your GPU, however you can use any other software to mine
        on your cpu as long as it goes to your wallet (see eula) if you want to be rewarded.
        Donations are also accepted when placed in your wallet.

        If ethereum is mined to a wallet linked to an account that does not exist, it instead either goes to
        a lottery or is ignored.

        """
        print(information)
        print('Press ENTER to go back')
        input('> ')

    
    logo ="""

    ████████╗███████╗███╗   ███╗██████╗ ███████╗███████╗████████╗     ██████╗ ██████╗ ██╗███╗   ██╗
    ╚══██╔══╝██╔════╝████╗ ████║██╔══██╗██╔════╝██╔════╝╚══██╔══╝    ██╔════╝██╔═══██╗██║████╗  ██║
       ██║   █████╗  ██╔████╔██║██████╔╝█████╗  ███████╗   ██║       ██║     ██║   ██║██║██╔██╗ ██║
       ██║   ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██╔══╝  ╚════██║   ██║       ██║     ██║   ██║██║██║╚██╗██║
       ██║   ███████╗██║ ╚═╝ ██║██║     ███████╗███████║   ██║       ╚██████╗╚██████╔╝██║██║ ╚████║
       ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝   ╚═╝        ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝
                                                                            By Dmitri Shevchenko                                              

    """
    while True:

        if 'Windows' in platform.system(): os.system('cls')
        else: os.system('clear')

        print(logo)
        print('Options : ')
        print('[1] Start mining coin')
        print('[2] Exit')
        print('[3] Infomation')
        print('')
        choice = input('> ')

        if choice == '1':
            mine_coin()
        if choice == '3':
            information()
        if choice == '2':
            sys.exit()

except Exception as e:
    if 'Windows' in platform.system(): os.system('cls')
    else: os.system('clear')
    print('An error has occured - please be sure to send the following error message to CodingCoda on discord or via email at dmitri.shevchenko.au@gmail.com')
    print('')
    print(str(e))
    print(client_info)
