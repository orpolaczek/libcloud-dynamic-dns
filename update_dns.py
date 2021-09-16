import libcloud
from libcloud.common.types import LibcloudError
from libcloud.dns.drivers.google import GoogleDNSDriver
from libcloud.dns.types import RecordType
import requests
from config import Config


class GoogleDNSUpdater:
    dns_driver = None

    def __init__(self):
        self.create_dns_driver()

    def create_dns_driver(self):
        self.dns_driver = GoogleDNSDriver(Config.DNS_USER_ID, Config.DNS_KEY, Config.DNS_PROJECT_NAME)

    def list_zones(self):
        return self.dns_driver.list_zones()

    def format_record_name(self, name, zoneDomain):
        if "" == name:
            return zoneDomain
        return "{}.{}".format(name, zoneDomain)

    def get_record_id_for_record_name(self, zone, name):
        for record in self.dns_driver.list_records(zone):
            if record.type != RecordType.A:
                continue
            if self.format_record_name(name, zone.domain) == record.name:
                return record.id

    def create_or_update_record(self, zone=None, record_name=None, a_record_value=None, ttl_seconds=3600):
        if None in (zone, record_name, a_record_value):
            return False

        formatted_record_name = self.format_record_name(record_name, zone.domain)

        # Try locating existing record with the same name
        dns_record = None
        try:
            record_id = self.get_record_id_for_record_name(zone, record_name)
            if record_id:
                dns_record = self.dns_driver.get_record(zone.id, record_id)
        except LibcloudError as e:
            print("Error locating record: {}".format(e.message))

        # Set record data
        record_data = {
            "ttl": ttl_seconds,
            "rrdatas": [a_record_value]
        }

        # Create or update an existing record with record_data
        if not dns_record:
            return self.dns_driver.create_record(formatted_record_name, zone, RecordType.A, record_data)
        elif a_record_value in dns_record.data['rrdatas']:
            print(f"{dns_record.name} is already set to {a_record_value}. Not updating.")
            return True
        else:
            if self.dns_driver.delete_record(dns_record):
                return self.dns_driver.create_record(formatted_record_name, zone, RecordType.A, record_data)
            else:
                return False

    def update_record_ip(self, zone_name, record_name, ip, ttl_seconds):
        for zone in self.list_zones():
            if zone.domain == zone_name:
                print("Setting A record: {}.{} to point: {}".format(record_name, zone.domain, ip))
                return gdns.create_or_update_record(zone, record_name, ip, ttl_seconds)
        return False

if __name__ == '__main__':
    WHATS_MY_IP_URL = "https://api.ipify.org"
    current_ip = requests.get(WHATS_MY_IP_URL).text
    gdns = GoogleDNSUpdater()
    result = gdns.update_record_ip(Config.A_RECORD_ZONE_NAME, Config.A_RECORD_NAME,
                                   current_ip, Config.A_RECORD_TTL_SECONDS)
    print("SUCCESS" if result else "FAILURE")
