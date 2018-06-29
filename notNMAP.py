##
##      Patrick Maher
##
##
##
##      Take Home Final
##
##
##
##      Did extra credit for adding list of ips and timeout value
##
##
##
##
##


import socket
import sys
import time



def name():
    print()
    print()
    print(" /$$   /$$             /$$     /$$   /$$ /$$      /$$  /$$$$$$  /$$$$$$$ ")
    print("| $$$ | $$            | $$    | $$$ | $$| $$$    /$$$ /$$__  $$| $$__  $$")
    print("| $$$$| $$  /$$$$$$  /$$$$$$  | $$$$| $$| $$$$  /$$$$| $$  \ $$| $$  \ $$")
    print("| $$ $$ $$ /$$__  $$|_  $$_/  | $$ $$ $$| $$ $$/$$ $$| $$$$$$$$| $$$$$$$/")
    print("| $$  $$$$| $$  \ $$  | $$    | $$  $$$$| $$  $$$| $$| $$__  $$| $$____/ ")
    print("| $$\  $$$| $$  | $$  | $$ /$$| $$\  $$$| $$\  $ | $$| $$  | $$| $$      ")
    print("| $$ \  $$|  $$$$$$/  |  $$$$/| $$ \  $$| $$ \/  | $$| $$  | $$| $$      ")
    print("|__/  \__/ \______/    \___/  |__/  \__/|__/     |__/|__/  |__/|__/      ")
    print()
    print()

def menu(one_selected, two_selected, three_selected):
    print()
    print("The option to run the scanner will appear after the data is entered")
    print("")
    print("Press d to view current data entered")
    print("Press 1 to enter IP(s)")
    print("Press 2 to select TCP or UDP")
    print("Press 3 to select port(s) or range of ports")
    print("Press 4 to enter a timeout value between scans")
    if one_selected == True and two_selected == True and three_selected == True:
        print("Press 5 to run the scanner")
    print("Press q to quit")
    print("")
    selection = input("Enter your selection here: ")
    if selection == '1':
        return '1'
    elif selection == '2':
        return '2'
    elif selection == '3':
        return '3'
    elif selection =='4':
        return '4'
    elif selection == '5':
        return '5'
    elif selection == 'd':
        return 'd'
    elif selection == 'q' or 'Q':
        sys.exit(0)
    else:
        print("Invalid selection please try again")
       
def main():
    name()
    ip_list = []
    protocol = ''
    ports = []
    timeout_val = 0
    
    one_selected = False
    two_selected = False
    three_selected = False

    while True:
        selection = menu(one_selected, two_selected, three_selected)
        if selection == '1':
            temp_a = ips()
            if temp_a == False:
                print("IPs not entered, please try again")
            else:
                one_selected = True
                ip_list = temp_a
        elif selection == '2':
            while protocol != 'tcp' and protocol != 'udp':
                protocol = tcp_or_udp()
            two_selected = True
        elif selection == '3':
            ports = ports_to_scan()
            three_selected = True
        elif selection =='4':
            timeout_val = timeout_value()
        elif selection == '5':
            run_scanner(ip_list, protocol, ports, timeout_val)
        elif selection =='d':
            print ("IPs [{}] ".format(ip_list) + "- Protocol[{}] ".format(protocol)+"- Ports[{}]".format(ports)+"- Time Value[{}]".format(timeout_val))
   
def timeout_value():
    selection = input("Enter the time to pause between scans in seconds: ")
    return selection

def tcp_or_udp():
    print("Press 1 if you want to scan TCP ports")
    print("Press 2 if you want to scan UDP ports")
    select = input("Enter your selection: ")
    if select == '1':
        return 'tcp'
    elif select == '2':
        return 'udp'
    else:
        print("Invalid option, try again")

def ips():
    ip_list = []
    more = True
    print("Press 1 if you want to enter the IP addresses by hand")
    print("Press 2 if you have a file of IPs that you would like to use")
    select = input("Enter your selection here: ")
    if select == '1':
        while more != False:
            temp_b= input ("Please enter the IP to scan in this format(xxx.xxx.xxx): ")
            ip_list.append(temp_b)
            cont = input("Do you have more ip addresses to enter?(y/n): ")
            if cont == 'n' or 'N':
                more = False
                return ip_list
    elif select == '2':
        try:
            file_name = input("Enter the name of you file here: ")
            infile = open(file_name, 'r')
            ip_list = infile.readlines()
            infile.close()
            print ()
            return ip_list
        except:
            return False

            
def ports_to_scan():
    port_list = []
    more = True
    print("Press 1 if you want to enter the port addresses by hand")
    print("Press 2 if you want to scan the port numbers 1 to 1024")
    print("Press 3 if you want to scan all port numbers(Really, really, really slow)")
    select = input("Enter your selection here: ")
    if select == '1':
        while more != False:
            temp_b= input ("Please enter the port number you wish to scan: (q to quit) ")
            #could insert code here to be sure you are entering port numbers
            if temp_b == 'q':
                more = False
            else:
                port_list.append(temp_b)
        return port_list
    elif select == '2':
        ctr = 1
        while ctr < 1025:
            port_list.append(ctr)
            ctr += 1
        return port_list
    elif select == '3' :
        print()
        ctr = 1
        while ctr < 65536:
            port_list.append(ctr)
            ctr += 1
        return port_list
    else:
        print("Incorrect entry, try again")

         

def run_scanner(ip_list, protocol, ports, timeout_val):  #ip and ports must be a list
    scan_protocol = protocol
    http_request = 'GET HTTP/1.1 \r\n'
    udp_request = 'Are you open?'
    outfile = open('scan_results.txt', 'a')
    open_ports = []
     
    for i in ip_list:
        for p in ports:
            if protocol == 'tcp':
                try:
                    print('Scanning TCP Port {} '.format(p)+'on {}'.format(i))
                    scan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    scan.settimeout(10) #so the scan does not get hung up waiting for a packet to return
                    scan.connect((i, int(p)))
                    scan.close()
                    open_ports.append('TCP Port '+ str(p) +' is open on '+ i)
                except:
                    pass
            else: #protocol is udp
                try:
                    #udp - will echo back whatever you send on open udp port otherwise conenction refused means closed or filtered
                    print('Scanning UDP Port {} '.format(p)+'on {}'.format(i))
                    scan = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    scan.settimeout(10)
                    scan.connect((i, int(p)))
                    scan.send(udp_request.encode())
                    comms = scan.recv(1024)
                    print('UDP Port {} '.format(p)+'is open on {}'.format(i))
                    open_ports.append('UDP Port '+ p +' is open on '+ i)
                    scan.close()
                except:
                    pass
            if timeout_val != 0:
                print('Sleeping for {} seconds'.format(timeout_val))
                time.sleep(int(timeout_val))
    print("Any results are saved to file scan_results.txt")
    print('')
    #output  results
    for i in open_ports:
        print (i)
        outfile.write(i)
    outfile.close()
    
main()





































##            if cont == 'y' or 'Y':
##                more = True
##            else:
##                more = False
