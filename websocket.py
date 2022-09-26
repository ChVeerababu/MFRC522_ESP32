def get_connect():
    import usocket as socket

    from network import WLAN, STA_IF, AP_IF

    from binascii import unhexlify

    from time import sleep

    ap_ssid = 'AP_ESP32'

    ap_pwd = '1234567890'

    wlan_ap = None

    wlan_sta = None

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('', 80))

    server_socket.listen(1)

    print('web server listening on {}'.format(server_address))



    def replace_hex_with_ascii(string):
        
        while True:
            
            ind = string.rfind('%')
            
            if ind == -1:
                
                break
            
            string = string.replace(string[ind:ind+3], unhexlify(string[ind+1:ind+3]).decode())
            
        return string


    def list_access_points():
        
        wlan_sta = WLAN(STA_IF)
        
        wlan_sta.active(False)
        
        wlan_sta.active(True)
        
        access_points = ((ap[0].decode(), ap[4]) for ap in wlan_sta.scan() if ap[4] > 0)
        
        sleep(10)
        
        wlan_sta.active(False)
        
        return access_points
        
        
    def setup_access_point():
        
        wlan_ap = WLAN(AP_IF)
        
        wlan_ap.active(True)
        
        wlan_ap.config(essid = ap_ssid, password = ap_pwd, authmode = 3)
        
        sleep(10)
        
        return wlan_ap


    def configure_wifi_device(ssid, pwd):
        
        wlan_sta = WLAN(STA_IF)
        
        wlan_sta.active(True)
        
        wlan_sta.connect(ssid, pwd)
        
        sleep(10)
        
        return wlan_sta if wlan_sta.isconnected() else None


    def save_wifi_config(ssid, pwd):
        
        with open('wifi.conf', 'w') as f:
            
            f.write('{}:{}'.format(ssid, pwd))
        
        
    def home_page():
        
        access_points = list_access_points()
        
        aps = ['<tr> <td colspan = "2"><input type="radio" name="ssid" value="{0}" />{1}</td> </tr>'.format(ap[0], ap[0] + ' : ' + str(ap[1])) for ap in access_points]
        
        html = 	'''
                <html>
                
                <head>
                
                    <title> WiFi Configuration </title>
                    
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                
                </head>
                
                <body>
                
                    <h1 style="color: #5e9ca0; text-align: center"> WiFi Configuration </h1>
                    
                    <h4 style="color: #5e9ca0; text-align: center"> (Choose an Access Point, Enter Password and Click on submit) </h4>
                    
                    <form action="configure" method="post">
                    
                        <table style="margin-left: auto; margin-right: auto;">
                        
                        <tbody>
                        
                        {}
                        
                        <tr> <td>Password:</td> <td><input name="password" type="password" /></td> </tr>
                        
                        <tr> <td colspan = '2'><input type="submit" value="Submit" /></td> </tr>
                        
                        </tbody>
                        
                        </table>
                        
                    </form>
                
                </body>
                
                </html>
                '''.format('\n'.join(aps))
        
        return html
        
        
    def success_page(ssid, pwd, wlan):
        
        html = 	'''
                <html>
                
                <head>
                
                    <title> WiFi Configuration Successful </title>
                    
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                
                </head>
                
                <body>
                
                    <h1 style="color: #5e9ca0; text-align: center"> WiFi Configuration Successful</h1>
                    
                    <h4 style="color: #5e9ca0; text-align: center"> (ssid, password): ({}, {}) </h4>
                    
                    <h4 style="color: #5e9ca0; text-align: center"> IP Configuration: {} </h4>
                
                </body>
                
                </html>
                '''.format(ssid, pwd, wlan.ifconfig())
        
        return html
        


    print('configuring device WiFi as Access Point')

    wlan_ap = setup_access_point()

    print('Access Point (ssid, pwd) = ({}, {})'.format(ap_ssid, ap_pwd))

    while True:
            
        try:
        
            print('waiting for client to connect')
        
            client_socket, client_address = server_socket.accept()
            
            print('client connected with {}'.format(client_address))
            
            client_socket.settimeout(None)
            
            content = client_socket.recv(1024).decode()
            
            client_socket.settimeout(None)
            
            request_uri = content[:content.index('\r\n')].split()[1].strip('/')
            
            print('requested uri: {}'.format(request_uri))
            
            ind = content.rfind('\r\n\r\n')
            
            ind += 5 if ind == -1 else 4
            
            content = content[ind : ]
            
            if not request_uri: # landing page (listing access points)
            
                print('serving home page')
                
                response = home_page()
            
            elif request_uri == 'configure': # configure page (store access point configuration)
                
                print(content)
                
                sta_ssid, sta_pwd = content.strip().replace('ssid=', '').replace('password=', '').split('&')
                print(sta_ssid, sta_pwd)
                
                sta_ssid, sta_pwd = replace_hex_with_ascii(sta_ssid), replace_hex_with_ascii(sta_pwd)
                if '+' in sta_ssid:
                    sta_ssid = sta_ssid.replace('+',' ')
                print(sta_ssid, sta_pwd)
                
                wlan_sta = configure_wifi_device(sta_ssid, sta_pwd)
                
                if wlan_sta:
                    
                    save_wifi_config(sta_ssid, sta_pwd)
                    
                    print('serving success page')
                    
                    response = success_page(sta_ssid, sta_pwd, wlan_sta)
                
                else:
                    
                    # proceed once again with below case
                    
                    print('serving home page again')
                
                    response = home_page()
                
            else:
                
                continue
                
                                
            client_socket.send('HTTP/1.1 200 OK\n')
            
            client_socket.send('Content-Type: text/html\n')
            
            client_socket.send('Content-Length: {}\n'.format(len(response)))
            
            client_socket.send('Connection: close\n\n')
            
            client_socket.sendall(response)
            
            sleep(10)
            
            client_socket.close()
            
            if wlan_sta and wlan_sta.isconnected():
                
                break
            
        finally:
            
            client_socket.close()


    wlan_ap.active(False)

    wlan_sta.active(False)

    server_socket.close()



