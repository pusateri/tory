from dmidecode import DMIParse
from pssh.clients import ParallelSSHClient
from datetime import datetime
from . import db


def parse_date(date_str):
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError("No valid format found '%s'", date_str)


def read_hosts(filename):
    files = []
    with open(filename) as hosts:
        for line in hosts:
            files.append(line.strip())
    return files


def main() -> None:
    session = db.sql_session()

    hosts = read_hosts("./hosts")
    client = ParallelSSHClient(hosts)

    # TODO: make sure doas and dmidecode are installed
    output = client.run_command("doas dmidecode")
    for dmi_output in output:
        lines = list(dmi_output.stdout)
        stdout = "\n".join(lines)
        dmi = DMIParse(stdout)
        bios = dmi.get(0)[0]
        baseboard = dmi.get(2)[0]
        cpu = dmi.get(4)[0]
        memory = dmi.get(16)[0]
        devices = dmi.get(17)
        mem_manuf = set()
        mem_speed = set()
        mem_size = 0
        for device in devices:
            size = device.get("Size")
            if size != "No Module Installed":
                mem_speed.add(device["Speed"])
                mem_manuf.add(device["Manufacturer"])
                nsize = size.split(" ")
                if nsize[1] == "GB":
                    mem_size += int(nsize[0])
        release_date = parse_date(bios["Release Date"])
        system = db.System(
            hostname=dmi_output.host,
            created=datetime.utcnow(),
            bios_vendor=bios["Vendor"],
            bios_version=bios["Version"],
            bios_release_date=release_date.date(),
            bios_revision=bios["BIOS Revision"],
            manufacturer=baseboard["Manufacturer"],
            product_name=baseboard["Product Name"],
            serial_number=baseboard["Serial Number"],
            cpu_family=cpu["Family"],
            cpu_manufacturer=cpu["Manufacturer"],
            cpu_version=cpu["Version"],
            cpu_max_speed=cpu["Max Speed"],
            cpu_socket=cpu["Upgrade"],
            cpu_core_count=int(cpu["Core Count"]),
            memory_size=mem_size,
            memory_max=memory["Maximum Capacity"],
            memory_ecc=memory["Error Correction Type"],
            memory_slots=int(memory["Number Of Devices"]),
            memory_manufacturer=",".join(mem_manuf),
            memory_speed=",".join(mem_speed),
        )
        session.add(system)
    session.commit()
