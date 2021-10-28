from scrapli_netconf import NetconfDriver
import datetime

start_time = datetime.datetime.now()
print ("Current date and time : ")
print (start_time.strftime("%Y-%m-%d %H:%M:%S"))

junos_device = {
    "host": "192.168.105.137",
    "auth_username": "scrapli",
    "auth_password": "juniper123",
    "port": 22,
    "auth_strict_key": False,
    "transport": "system",
    "timeout_ops": 10,
    "timeout_transport": 10
}

rpc = """
<get-zones-information>
</get-zones-information>
"""


def main():
    conn = NetconfDriver(**junos_device)
    print("we have declared our connection object, but do not have an active SSH session yet")
    conn.open()
    
    print("we have an active SSH connection to our firewall")
    print(conn.server_capabilities)
    
    anything = conn.rpc(filter_=rpc)
    print(anything.result)
    
    conn.close()

    finish_time = datetime.datetime.now()
    print ("Current date and time : ")
    print (finish_time.strftime("%Y-%m-%d %H:%M:%S"))




if __name__ == '__main__':
    main()