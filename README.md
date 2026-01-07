# Tory

An invenTORY collection script for hardware PCs and servers.

This script uses dmidecode to collect information about the motherboard, cpu, and memory of a machine and store it in a SQLlite database.

It is intended for one machine to query all other machines over SSH. Since root privileges are required to run dmidecode, it uses doas to enable privilege escalation for only the dmidecode command only for the user connecting via SSH.

The doas config file doas.conf should contain the following line for the user:

```
permit nopass your_user_name as root cmd dmidecode
```

Colleciton over SSH assumes you have public keys and authorized_users setup so that the "doas dmidecode" command can be run without any interaction.

# Building

Initial installation requirements:

    1. doas
    2. dmidecode

Running "uv run tory" for the first time will add all the dependencies to the uv virtual environment. This will build the SQLite Python wrapper which will need to find the sqlite3.h include file. For FreeBSD, you will need to set this environment variable for it to find the correct include file.
```
export CPPFLAGS=-I/usr/local/include
```

# SQLite Schema

The tory database and 'systems' table will be created automatically. The schema looks like the following:

```sql
CREATE TABLE systems (
	id INTEGER NOT NULL,
	hostname VARCHAR,
	created DATETIME,
	bios_vendor VARCHAR,
	bios_version VARCHAR,
	bios_release_date DATETIME,
	bios_revision VARCHAR,
	manufacturer VARCHAR,
	product_name VARCHAR,
	serial_number VARCHAR,
	cpu_family VARCHAR,
	cpu_manufacturer VARCHAR,
	cpu_version VARCHAR,
	cpu_max_speed VARCHAR,
	cpu_socket VARCHAR,
	cpu_core_count INTEGER,
	memory_size INTEGER,
	memory_max VARCHAR,
	memory_ecc VARCHAR,
	memory_slots INTEGER,
	memory_manufacturer VARCHAR,
	memory_speed VARCHAR,
	PRIMARY KEY (id)
);
```
# Sample data

Here is a sample row in the database showing the kind of data it collects:

```json
[
    {
        "id": 1,
        "hostname": "host1.example.com",
        "created": "2026-01-07 22:51:59.320496",
        "bios_vendor": "American Megatrends Inc.",
        "bios_version": "F4",
        "bios_release_date": "2021-03-02 00:00:00.000000",
        "bios_revision": "5.13",
        "manufacturer": "Gigabyte Technology Co., Ltd.",
        "product_name": "C246M-WU4-CF",
        "serial_number": "Default string",
        "cpu_family": "Core i7",
        "cpu_manufacturer": "Intel(R) Corporation",
        "cpu_version": "Intel(R) Core(TM) i7-9700K CPU @ 3.60GHz",
        "cpu_max_speed": "8300 MHz",
        "cpu_socket": "Socket LGA1151",
        "cpu_core_count": 8,
        "memory_size": 32,
        "memory_max": "64 GB",
        "memory_ecc": "None",
        "memory_slots": 4,
        "memory_manufacturer": "Kingston",
        "memory_speed": "2666 MT/s"
    }
]
```
