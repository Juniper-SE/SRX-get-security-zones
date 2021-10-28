import asyncio
import xmltodict

from scrapli_netconf.driver import AsyncNetconfDriver
from scrapli.logging import enable_basic_logging
from jinja2 import Environment, FileSystemLoader

enable_basic_logging(file=True, level="debug")
env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True)
template = env.get_template('sz.j2')

galveston = {
    "host": "192.168.105.137",
    "auth_username": "scrapli",
    "auth_password": "juniper123",
    "auth_strict_key": False,
    "transport": "asyncssh"
}

sanantonio = {
    "host": "192.168.105.146",
    "auth_username": "scrapli",
    "auth_password": "juniper123",
    "auth_strict_key": False,
    "transport": "asyncssh"
}

inventory = [galveston, sanantonio]

rpc = """
<get-zones-information>
</get-zones-information>
"""

async def gather_security_zones(device):
    conn = AsyncNetconfDriver(**device)
    await conn.open()
    result = await conn.rpc(filter_=rpc)
    await conn.close()
    return result


async def main():
    coroutines = [gather_security_zones(device) for device in inventory]
    results = await asyncio.gather(*coroutines)
    for each_result in results:
        # print(each_result.result)
        reply_as_dict = xmltodict.parse(each_result.result)
        security_zones = reply_as_dict["rpc-reply"]["zones-information"]["zones-security"]

        templated_sz = template.render(security_zones=security_zones)
        with open(f"./output/{each_result.host}.yaml", "w") as file_holder:
            file_holder.write(templated_sz)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())