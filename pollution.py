import asyncio, sys
import serial_asyncio
import serial
import logging
import time
import sqlite3
from sqlite3 import IntegrityError


FORMAT = '%(asctime)-15s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger('pi')
log.setLevel(logging.INFO)

initiate_active = bytearray([0x42, 0x4d, 0xe1, 0x0, 0x01, 0x01, 0x71])
initiate_passive = bytearray([0x42, 0x4d, 0xe1, 0x0, 0x00, 0x01, 0x70])

sleep_bytes = bytearray([0x42, 0x4d, 0xe4, 0x00, 0x00, 0x01, 0x73])
wakeup_bytes = bytearray([0x42, 0x4d, 0xe4, 0x00, 0x01, 0x01, 0x74])
db = sqlite3.connect("/home/pi/air/ppm2/air_quality.db")
cursor = db.cursor()

FRAME_SZ = 32
REFRESH_SEC = 60


class Measurement:
    def __init__(self, m_0_cf1, m2_5_cf1, m10_0_cf1, m1_0_atmo, m2_5_atmo,
                 m10_0_atmo, m0_3_ct, m0_5_ct, m1_0_ct, m2_5_ct, m5_0_ct, m10_0_ct):
        self.pm1_0_cf1 = m1_0_cf1
        self.pm2_5_cf1 = m2_5_cf1
        self.pm10_0_cf1 = m10_0_cf1
        self.pm1_0_atmo = m1_0_atmo
        self.pm2_5_atmo = m2_5_atmo
        self.pm10_0_atmo = m10_0_atmo
        self.pm0_3_ct = m0_3_ct
        self.pm0_5_ct = m0_5_ct
        self.pm1_0_ct = m1_0_ct
        self.pm2_5_ct = m2_5_ct
        self.pm5_0_ct = m5_0_ct
        self.pm10_0_ct = m10_0_ct


class Monitor(asyncio.Protocol):
    def __init__(self):
        asyncio.Protocol.__init__(self)
        self.data_ = bytearray()
        self.ct_ = 0

    def connection_made(self, transport):
        self.transport = transport
        log.info('port opened')
        transport.serial.rts = False
        transport.write(initiate_active)
        #time.sleep(10)
        #transport.write(wakeup_bytes)
        log.info('open')

    def data_received(self, data):
        log.debug('data received %d %s', len(data), repr(data))
        if data == b'\x42':
            #print("Frame ", len(self.data_))
            log.debug("frame %d %s", len(self.data_), repr(self.data_))
            if self.data_ and len(self.data_) >= FRAME_SZ:
                self.process(self.data_)
                self.data_ = bytearray()
                self.data_ += data
                #self.ct_ = self.ct_ + 1
                #if (self.ct_ >= 1):
                #self.transport.write(sleep_bytes)
                #log.info("sleeping")
                #time.sleep(REFRESH_SEC)
                #log.info("Done")
                #self.transport.write(wakeup_bytes)
                #    self.ct_ = 0
        else:
            self.data_ += data

    def process(self, data):
        log.debug("%d %s", len(data), repr(data))
        if data[0] != 0x42 or data[1] != 0x4d:
            log.warning("skipping %s %s %s", repr(data), data[0], data[1])
            return
        frame_len = (data[2] << 8) + data[3]
        data = data[4:frame_len]

        higher = data[::2]
        lower = data[1::2]
        proc_data = [(d1 << 8) + d2 for d1, d2 in zip(higher, lower)]

        ts = int(time.time())
        #print("ts: ", ts, " len(proc_data): ", len(proc_data), " proc_data: ", proc_data)
        log.debug("%d %d %s", ts % 5, len(proc_data), proc_data)

        if ts % 60 == 0:
            row = [ts]
            row += proc_data
            #print("Inserting: ", row)
            log.info("inserting %s", row)
            try:
                cursor.execute("INSERT INTO measurements2 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", row)
                db.commit()
            except IntegrityError:
                logger.warning("duplicate id, %s", row)
                db.rollback()

    def connection_lost(self, exc):
        log.info('port closed')
        sys.exit('Port closed')
        asyncio.get_event_loop().stop()


loop = asyncio.get_event_loop()
coro = serial_asyncio.create_serial_connection(loop,
                                               Monitor,
                                               '/dev/serial0',
                                               baudrate=9600)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
