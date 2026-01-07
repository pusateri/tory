import sqlalchemy as sa
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class System(Base):
    __tablename__ = "systems"
    id = Column("id", Integer, primary_key=True)
    hostname = Column(String)  # DNS hostname
    created = Column(DateTime)  # UTC
    bios_vendor = Column(String)  # type 0, Vendor
    bios_version = Column(String)  # type 0, Version
    bios_release_date = Column(DateTime)  # type 0, Release Date
    bios_revision = Column(String)  # type 0, BIOS Revision

    manufacturer = Column(String)  # type 1, Manufacturer
    product_name = Column(String)  # type 1, Prodct Name

    serial_number = Column(String)  # type 2, Serial Number

    cpu_family = Column(String)  # type 4, Family
    cpu_manufacturer = Column(String)  # type 4, Manufacturer
    cpu_version = Column(String)  # type 4, Version
    cpu_max_speed = Column(String)  # type 4, Max Speed
    cpu_socket = Column(String)  # type 4, Upgrade
    cpu_core_count = Column(Integer)  # type 4, Core Count

    memory_size = Column(Integer)  # type 17, Size
    memory_max = Column(String)  # type 16, Maximum Capacity
    memory_ecc = Column(String)  # type 16, Error Correction Type
    memory_slots = Column(Integer)  # type 16, Number Of Devices
    memory_manufacturer = Column(String)  # type 17, Manufacturer
    memory_speed = Column(String)  # type 17, Speed


def sql_session():
    engine = sa.create_engine("sqlite:///tory.sqlite", echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = sa.MetaData()
    try:
        engine.connect()
    except sa.exc.DBAPIError:
        if not database_exists(engine.url):
            create_database(engine.url)

    try:
        sa.Table(
            "systems",
            metadata,
            sqlite_autoincrement=True,
            autoload_with=engine,
        )
    except sa.exc.NoSuchTableError:
        Base.metadata.create_all(engine)
    return session


"""
17 Memory Device
    Data Width: 64 bits
	Size: 4 GB or Size: No Module Installed
	Form Factor: DIMM
	Locator: DIMM_2A
	Bank Locator: BANK 0
	Type: DDR3
	Type Detail: Synchronous
	Speed: 1333 MT/s
	Manufacturer: Kingston
	Serial Number: 07042614
	Asset Tag: 9876543210
	Part Number: 9965525-033.A00LF
	Rank: 2
	Configured Memory Speed: 1333 MT/s

    os_name: FreeBSD, Linux (uname -s)
    os_version: 14.3-RELEASE-p5, Ubuntu 25.10 (lsb_release Description)
    linux_kernel_version: 6.17.0-8-generic (uname -r)
"""
