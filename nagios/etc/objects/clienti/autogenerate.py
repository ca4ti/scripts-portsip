#!/usr/bin/env python3
import requests
import json

json_auth = {
"username": "admin",
"password": "eCaeR495"
}

portsip = "https://ip-centrex.iptelecom.it:8887/api/tokens"

headers = {
'Content-Type': 'application/json'
}

resp = requests.post(portsip, headers=headers, json=json_auth)

if resp.status_code != 200:
	print('error: ' + str(resp.status_code))
else:
	#print('User List Loaded Successfully'+resp.text)
	auth_continue=json.loads(resp.text)
	portsip = "https://ip-centrex.iptelecom.it:8887/api/tenants"
	headers = {
	'Content-Type': 'application/json',
	'Authorization': 'Bearer '+auth_continue['access_token']
	}
	#print (headers)
	resp = requests.get(portsip,headers=headers)
	#print(str(resp.text))
	tenants=json.loads(resp.text)
	for tenant in range(len(tenants['items'])):
		#print(tenants['items'][tenant]['id'])
		#print(tenants['items'][tenant])
		domain_now = tenants['items'][tenant]
		portsip = "https://ip-centrex.iptelecom.it:8887/api/tenants/switch?id="+tenants['items'][tenant]['id']+""
		headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer '+auth_continue['access_token']
		}
		#print(portsip)
		#print(headers)
		resp = requests.post(portsip,headers=headers)
		#print(">>>switch")
		#print(str(resp.text))

		#print(tenant, tenants['items'][tenant]['domain'])
		portsip = "https://ip-centrex.iptelecom.it:8887/api/users"
		headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer '+auth_continue['access_token']
		}
		#print(portsip)
		#print(headers)
		resp = requests.get(portsip,headers=headers)
		#print(str(resp.text))
		#criar lista de usuarios
		users=json.loads(resp.text)
		if 'list_users' in locals() :
			del list_users
		list_users = []
		#print("------->>>>>>>")
		#print(range( len( users['items']) ), users['items'][0] )
		#print(len(users['items']))
		for user in range(len(users['items'])):
			#print(">>>",user)
			#print(users['items'][user]['id'])
			#print(users['items'][user]['name'])
			#print(users['items'][user])
			extension=users['items'][user]['extension_number']+"@"+domain_now['domain']
			max=len(users['items'])-1
			#print(extension)
			#print(user ,  max)
			domain=domain_now['domain']
			#print(domain)
			if 'Admin' !=  users['items'][user]['name'] :
				list_users.append(extension)
				nagios_hosts='''
define host{
        use                      server-portsip           ; Name of host template to use
                                                        ; This host definition will inherit all variables that are defined
                                                        ; in (or inherited by) the server-portsip host template definition.
        host_name               '''+extension+'''
        address                 '''+extension+'''
        }
define service{
        use                             local-service        ; Name of service template to use
        host_name                       '''+extension+'''
        service_description             OnlineOffLine
        check_command                   portsip
        }

'''
				if user > 0 :
					body_nagios=body_nagios+nagios_hosts
				else:
					body_nagios=nagios_hosts
			#print("----------------------------------------------------")
			#print(nagios_hosts)
			#print("----------------------------------------------------")
			if user == max :
				#print(body_nagios)
				#print("----------------------------------------------------")
				list_users=str(list_users)[1:][:-1].replace('\'', '')
				#print(list_users)
				nagios_hostgroup='''
define hostgroup{
        hostgroup_name  '''+domain+''' ; The name of the hostgroup
        members  	'''+list_users+'''; Comma separated list of hosts that belong to this group
        }

'''
				if  len(users['items']) > 1 :
					#print(nagios_hostgroup)
					#print("----------------------------------------------------")
					#print("===================")
					file_finale=nagios_hostgroup+body_nagios
					#print(file_finale)
					#exit(0)
					# Open text file in write+text mode
					text_file = open(domain+".cfg", "wt")

					# Write content to file
					n = text_file.write(file_finale)

					if n == len(file_finale):
						print(domain+".cfg")
					else:
						print("Failure! String not written to text file.")

					# Close file
					text_file.close()
