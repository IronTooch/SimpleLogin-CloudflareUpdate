"""Constants file to manage files

Returns:
    _type_: N/A
"""

import json
from typing import Any, Literal
from pip._vendor import requests

# import pip._vendor.requests as requests

class SimpleLogin:
    """Constants for SimpleLogin
    """
    CONFIG_PATH: str = 'subdomain_vars'
    FULL_CONFIG_PATH: str = "./local/" + CONFIG_PATH

    MX_RECORD1_VAL: Literal['mx1.simplelogin.co'] = 'mx1.simplelogin.co'
    MX_RECORD1_PRI: Literal[10] = 10
    MX_RECORD2_VAL: Literal['mx2.simplelogin.co'] = 'mx2.simplelogin.co'
    MX_RECORD2_PRI: Literal[20] = 20
    SPF_RECORD_VAL: Literal['v=spf1 include:simplelogin.co ~all'] = (
        'v=spf1 include:simplelogin.co ~all')
    DKIM_RECORD1: Literal['dkim._domainkey.'] = 'dkim._domainkey.'
    DKIM_RECORD1_VAL: Literal['dkim._domainkey.simplelogin.co'] = (
        'dkim._domainkey.simplelogin.co')
    DKIM_RECORD2: Literal['dkim02._domainkey.'] = 'dkim02._domainkey.'
    DKIM_RECORD2_VAL: Literal['dkim02._domainkey.simplelogin.co'] = (
        'dkim02._domainkey.simplelogin.co')
    DKIM_RECORD3: Literal['dkim03._domainkey.'] = 'dkim03._domainkey.'
    DKIM_RECORD3_VAL: Literal['dkim03._domainkey.simplelogin.co'] = (
        'dkim03._domainkey.simplelogin.co')
    DMARC_RECORD_VAL: Literal['_dmarc.'] = '_dmarc.'
    DMARC_VAL: Literal['v=DMARC1; p=quarantine; pct=100; adkim=s; aspf=s'] = (
        'v=DMARC1; p=quarantine; pct=100; adkim=s; aspf=s')

    OWNER_VERIFY_KEY: Literal['simplelogin_owner_key'] = 'simplelogin_owner_key'
    NEW_DOMAIN_KEY: Literal['new_domain_key'] = 'new_domain_key'
    ROOT_DOMAIN_KEY: Literal['root_domain_key'] = 'root_domain_key'

class Cloudflare:
    """CLoudflare Constants and Functions

    Returns:
        Cloudflare: Not used
    """

    CONFIG_PATH: Literal['cloudflare_vars'] = 'cloudflare_vars'
    FULL_CONFIG_PATH: str = "./local/" + CONFIG_PATH

    API_ROOT: Literal['https://api.cloudflare.com/client/v4'] = (
        'https://api.cloudflare.com/client/v4')
    API_ZONE_RECORDS: str = API_ROOT + '/zones'

    JSON_HEADER: Literal['application/json'] = 'application/json'
    TXT_RECORD: Literal['TXT'] = "TXT"
    MX_RECORD: Literal['MX'] = "MX"
    CNAME_RECORD: Literal['CNAME'] = "CNAME"

    EMAIL_KEY: Literal['cloudflare_email'] = 'cloudflare_email'
    AUTH_KEY: Literal['cloudflare_auth_token'] = 'cloudflare_auth_token'

    @staticmethod
    def get_auth_header() -> dict:
        """Creates the Authentication header based on static files

        Returns:
            dict: Authentication Header dictionary
        """
        str_auth_val: str = Utils.get_yeml_key( Cloudflare.FULL_CONFIG_PATH,
                                                Cloudflare.AUTH_KEY)
        str_email_val: str = Utils.get_yeml_key(Cloudflare.FULL_CONFIG_PATH,
                                                Cloudflare.EMAIL_KEY)
        auth_header: dict[str, str] = Cloudflare.make_auth_header (
                                                    str_auth_val=str_auth_val,
                                                    str_email=str_email_val)
        return auth_header

    @staticmethod
    def make_auth_header(str_auth_val: str, str_email: str) -> dict[str, str]:
        """Creates an Authentication header based on the values given

        Args:
            str_auth_val (str): Authentication Key for Cloudflare
            str_email (str): Authentication Email for Cloudflare

        Returns:
            dict: Dictionary of Authentication header
        """
        return {'X-Auth-Email': str_email,
                'X-Auth-Key': str_auth_val,
                'Content-Type': Cloudflare.JSON_HEADER }

    @staticmethod
    def get_domain_id( str_domain_root: str) -> str:
        """Gets the Cloudflare ID for the Domain

        Args:
            str_domain_root (str): Root Domain plus TLD

        Returns:
            str: String Representation of Domain ID
        """
        str_url_endpoint: str = (Cloudflare.API_ZONE_RECORDS
                                + '?name=' + str_domain_root)
        header: dict = Cloudflare.get_auth_header()
        req = requests.get(headers=header,url=str_url_endpoint)
        dict_json = (json.loads(req.text))['result'][0]
        str_id: str = dict_json['id']
        return str_id

    @staticmethod
    def get_domain_records( str_domain_root: str) -> dict:
        """Gets all of the records for a given domain

        Args:
            str_domain_root (str): Root domain

        Returns:
            dict: All the individual domain records
        """
        str_domain_id: str = Cloudflare.get_domain_id(str_domain_root)
        header: dict = Cloudflare.get_auth_header()
        str_url_endpoint: str = (Cloudflare.API_ZONE_RECORDS
                                    + '/' + str_domain_id + '/dns_records')
        req = requests.get(headers=header,url=str_url_endpoint)
        dict_json = (json.loads(req.text))['result']
        return dict_json

    @staticmethod
    def record_exists(  dict_records: dict,
                        str_recordname: str,
                        str_record_val: str,
                        str_record_type: str,
                        int_priority: int = 1) -> bool:
        """Checks to see if a given record already exists in the domain

        Args:
            dict_records (dict): List of all the records in the domain
            str_recordname (str): Record to search for
            str_record_val (str): Content of the Domain Record to confirm
            str_record_type (str): Type of domain record
            int_priority (int, optional): Priority for MX records. Defaults to 1

        Returns:
            bool: True if record exists in domain, else false
        """
        print ("All records count: " + str(len(dict_records)))
        # for rec in dict_records:
        #     print("Name: ", rec['name'], " ; Type: ", rec['type'], " ; Value: ", rec['content'])
        records_of_type = [ rec for rec in dict_records
                                if rec['type'] == str_record_type]
        print ("Records of Type count: " + str(len(records_of_type)))
        for rec in records_of_type:
            print("Name: ", rec['name'], " ; Type: ", rec['type'], " ; Value: ", rec['content'])
        records_of_name = [ rec for rec in records_of_type
                                if rec['name'] == str_recordname]
        print ("Records of Name count: " + str(len(records_of_name)))
        for rec in records_of_name:
            print("Name: ", rec['name'], " ; Type: ", rec['type'], " ; Value: ", rec['content'])
        records_of_value = [rec for rec in records_of_name
                                if rec['content'] == str_record_val]
        print ("Records of Value count: " + str(len(records_of_value)))
        for rec in records_of_value:
            print("Name: ", rec['name'], " ; Type: ", rec['type'], " ; Value: ", rec['content'])

        if str_record_type != Cloudflare.MX_RECORD:
            if len(records_of_value) > 0:
                return True
            else:
                return False

        records_of_priority = [ rec for rec in records_of_value
                                    if rec['priority'] == int_priority]

        if len(records_of_priority) > 0:
            return True
        else:
            return False

    @staticmethod
    def write_new_record (  str_domain_root: str,
                            str_recordname: str,
                            str_record_val: str,
                            str_record_type: str,
                            str_comment: str,
                            int_priority: int = 1):
        """Makes new DNS record

        Args:
            str_domain_root (str): Root domain to write into
            str_recordname (str): Record site to add
            str_record_val (str): Content to add
            str_record_type (str): Record type (CNAME / TXT / etc)
            str_comment (str): Comment for record
            int_priority (int, optional): Priority for MX record. Defaults to 1.

        Returns:
            _type_: Request response
        """
        str_domain_id: str = Cloudflare.get_domain_id(str_domain_root)
        header: dict = Cloudflare.get_auth_header()
        str_url_endpoint: str = (Cloudflare.API_ZONE_RECORDS
                                    + '/' + str_domain_id + '/dns_records')

        str_comment: str = str_comment[0:50]
        dict_data: dict [str, Any] = {
                "name": str_recordname,
                "type": str_record_type,
                "content": str_record_val,
                "ttl": 1,
                "comment": str_comment
                }

        if str_record_type == Cloudflare.MX_RECORD:
            dict_data['priority'] = int_priority

        if str_record_type == Cloudflare.CNAME_RECORD:
            dict_data['proxied'] = False

        req = requests.post(headers=header,
                            url=str_url_endpoint,
                            json=dict_data)

        print (req)
        return req

    @staticmethod
    def get_root_domain ( str_subdomain: str) -> str:
        """Gets Root domain from subdomain

        Args:
            str_subdomain (str): Subdomain URL

        Returns:
            str: Root domain String
        """
        sections: list[str] = str_subdomain.split('.')

        str_tld: str = sections[-1]
        str_root: str = sections[-2]
        str_root_domain: str = str_root + '.' + str_tld
        return str_root_domain


class Utils:
    """Class to houes other supporting functions and constants
    """
    # def printVariable(varName: str) -> None:
    #     int
    #     return 'Hello ' + name
    @staticmethod
    def get_yeml_key(str_filename: str, str_key: str) -> str:
        """Gets the value from a YAML key in a config file

        Args:
            str_filename (str): config file to check
            str_key (str): key file to get value from

        Returns:
            str: Value from key, "" if key not found
        """
        with open(str_filename, encoding="utf-8") as file:
            lst_contents = file.readlines()

        for str_line in lst_contents:
            if str_key in str_line:
                str_line = str_line.replace(str_key + ':', "")
                str_line = str_line.lstrip().rstrip()
                return str_line

        return ""
