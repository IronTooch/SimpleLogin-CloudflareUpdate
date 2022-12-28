import json
import pip._vendor.requests as requests

class SimpleLogin:

    CONFIG_PATH: str = 'subdomain_vars'
    FULL_CONFIG_PATH: str = "./local/" + CONFIG_PATH

    MX_RECORD1_VAL: str = 'mx1.simplelogin.co'
    MX_RECORD1_PRI: int = 10
    MX_RECORD2_VAL: str = 'mx2.simplelogin.co'
    MX_RECORD2_PRI: int = 20
    SPF_RECORD_VAL: str = 'v=spf1 include:simplelogin.co ~all'
    DKIM_RECORD1: str = 'dkim._domainkey.'
    DKIM_RECORD1_VAL: str = 'dkim._domainkey.simplelogin.co'
    DKIM_RECORD2: str = 'dkim02._domainkey.'
    DKIM_RECORD2_VAL: str = 'dkim02._domainkey.simplelogin.co'
    DKIM_RECORD3: str = 'dkim03._domainkey.'
    DKIM_RECORD3_VAL: str = 'dkim03._domainkey.simplelogin.co'
    DMARC_RECORD_VAL: str = '_dmarc.'
    DMARC_VAL: str = 'v=DMARC1; p=quarantine; pct=100; adkim=s; aspf=s'

    OWNER_VERIFY_KEY='simplelogin_owner_key'
    NEW_DOMAIN_KEY='new_domain_key'
    ROOT_DOMAIN_KEY='root_domain_key'

class Cloudflare:

    CONFIG_PATH: str = 'cloudflare_vars'
    FULL_CONFIG_PATH: str = "./local/" + CONFIG_PATH

    API_ROOT: str = 'https://api.cloudflare.com/client/v4'
    API_ZONE_RECORDS: str = API_ROOT + '/zones'

    JSON_HEADER: str = 'application/json'
    TXT_RECORD: str = "TXT"
    MX_RECORD: str = "MX"
    CNAME_RECORD: str = "CNAME"

    EMAIL_KEY: str = 'cloudflare_email'
    AUTH_KEY: str = 'cloudflare_auth_token'

    @staticmethod
    def get_auth_header() -> dict:
        str_auth_val: str = Utils.get_yeml_key( Cloudflare.FULL_CONFIG_PATH,
                                                Cloudflare.AUTH_KEY)
        str_email_val: str = Utils.get_yeml_key(Cloudflare.FULL_CONFIG_PATH,
                                                Cloudflare.EMAIL_KEY)
        auth_header = Cloudflare.make_auth_header ( str_auth_val=str_auth_val,
                                                    str_email=str_email_val)
        return auth_header

    @staticmethod
    def make_auth_header(str_auth_val: str, str_email: str):
        return {'X-Auth-Email': str_email,
                'X-Auth-Key': str_auth_val,
                'Content-Type': Cloudflare.JSON_HEADER }

    @staticmethod
    def get_domain_id( str_domain_root: str) -> str:
        str_url_endpoint: str = (Cloudflare.API_ZONE_RECORDS
                                + '?name=' + str_domain_root)
        header: dict = Cloudflare.get_auth_header()
        req = requests.get(headers=header,url=str_url_endpoint)
        dict_json = (json.loads(req.text))['result'][0]
        str_id: str = dict_json['id']
        return str_id

    @staticmethod
    def get_domain_records( str_domain_root: str) -> dict:

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
                            bool_proxied: bool = False,
                            int_priority: int = 1) -> dict:

        str_domain_id: str = Cloudflare.get_domain_id(str_domain_root)
        header: dict = Cloudflare.get_auth_header()
        str_url_endpoint: str = (Cloudflare.API_ZONE_RECORDS
                                    + '/' + str_domain_id + '/dns_records')


        dict_data = {
                "name": str_recordname,
                "type": str_record_type,
                "content": str_record_val,
                "ttl": 1,
                "comment": str_comment,
                "proxied": bool_proxied
                }

        if str_record_type == Cloudflare.MX_RECORD:
            dict_data['priority'] = int_priority

        req = requests.post(headers=header,
                            url=str_url_endpoint,
                            json=dict_data)
        print (req)
        return req

    @staticmethod
    def get_root_domain ( str_subdomain: str) -> str:
        sections = str_subdomain.split('.')

        str_tld = sections[-1]
        str_root = sections[-2]
        str_root_domain = str_root + '.' + str_tld
        return str_root_domain


class Utils:

    # def printVariable(varName: str) -> None:
    #     int
    #     return 'Hello ' + name
    @staticmethod
    def get_yeml_key(str_filename: str, str_key: str) -> str:

        with open(str_filename, encoding="utf-8") as file:
            lst_contents = file.readlines()

        for str_line in lst_contents:
            if str_key in str_line:
                str_line = str_line.replace(str_key + ':', "")
                str_line = str_line.lstrip().rstrip()
                return str_line

        return ""
