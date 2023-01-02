from local_constants import Utils, Cloudflare, SimpleLogin

print (SimpleLogin.OWNER_VERIFY_KEY)

email_val: str = Utils.get_yeml_key( Cloudflare.FULL_CONFIG_PATH,
                                Cloudflare.EMAIL_KEY)
new_subdomain: str = Utils.get_yeml_key( SimpleLogin.FULL_CONFIG_PATH,
                                    SimpleLogin.NEW_DOMAIN_KEY)
subdomain_verify_val: str = Utils.get_yeml_key(SimpleLogin.FULL_CONFIG_PATH,
                                          SimpleLogin.OWNER_VERIFY_KEY)


str_root_domain: str = Cloudflare.get_root_domain(new_subdomain)

# Verify Domain Ownership
domain_records = Cloudflare.get_domain_records(str_root_domain)
verify_record_exists: bool = Cloudflare.record_exists(
                          dict_records=domain_records,
                          str_record_type=Cloudflare.TXT_RECORD,
                          str_record_val=subdomain_verify_val,
                          str_recordname=new_subdomain)
print ("Verify Record Exists: " + str(verify_record_exists))

if not verify_record_exists:
    print ("Record needed")
    str_domain_comment: str = "SimpleLogin Verify Record for " + new_subdomain
    Cloudflare.write_new_record(str_domain_root=str_root_domain,
                                str_record_type=Cloudflare.TXT_RECORD,
                                str_record_val=subdomain_verify_val,
                                str_recordname=new_subdomain,
                                str_comment=str_domain_comment)

# Add MX Records
mx1_record_exists: bool = Cloudflare.record_exists(
                          dict_records=domain_records,
                          str_record_type=Cloudflare.MX_RECORD,
                          str_record_val=SimpleLogin.MX_RECORD1_VAL,
                          str_recordname=new_subdomain,
                          int_priority=SimpleLogin.MX_RECORD1_PRI)
print ("Mx1 Record Exists: " + str(mx1_record_exists))

if not mx1_record_exists:
    print ("MX1 Record needed")
    str_domain_comment: str = "SimpleLogin MX1 Record for " + new_subdomain
    Cloudflare.write_new_record(str_domain_root=str_root_domain,
                                str_record_type=Cloudflare.MX_RECORD,
                                str_record_val=SimpleLogin.MX_RECORD1_VAL,
                                str_recordname=new_subdomain,
                                str_comment=str_domain_comment,
                                int_priority=SimpleLogin.MX_RECORD1_PRI)

mx2_record_exists: bool = Cloudflare.record_exists(
                          dict_records=domain_records,
                          str_record_type=Cloudflare.MX_RECORD,
                          str_record_val=SimpleLogin.MX_RECORD2_VAL,
                          str_recordname=new_subdomain,
                          int_priority=SimpleLogin.MX_RECORD2_PRI)
print ("Mx2 Record Exists: " + str(mx2_record_exists))

if not mx2_record_exists:
    print ("MX2 Record needed")
    str_domain_comment: str = "SimpleLogin MX2 Record for " + new_subdomain
    Cloudflare.write_new_record(str_domain_root=str_root_domain,
                                str_record_type=Cloudflare.MX_RECORD,
                                str_record_val=SimpleLogin.MX_RECORD2_VAL,
                                str_recordname=new_subdomain,
                                str_comment=str_domain_comment,
                                int_priority=SimpleLogin.MX_RECORD2_PRI)

# Add SPF Record
spf_record_exists: bool = Cloudflare.record_exists(
                          dict_records=domain_records,
                          str_record_type=Cloudflare.TXT_RECORD,
                          str_record_val=SimpleLogin.SPF_RECORD_VAL,
                          str_recordname=new_subdomain)
print ("SPF Record Exists: " + str(mx2_record_exists))

if not spf_record_exists:
    print ("SPF Record needed")
    str_domain_comment: str = "SimpleLogin SPF Record for " + new_subdomain
    Cloudflare.write_new_record(str_domain_root=str_root_domain,
                                str_record_type=Cloudflare.TXT_RECORD,
                                str_record_val=SimpleLogin.SPF_RECORD_VAL,
                                str_recordname=new_subdomain,
                                str_comment=str_domain_comment)

# Add DKIM Record

str_record_name: str = SimpleLogin.DKIM_RECORD1 + new_subdomain
dkim1_record_exists: bool = Cloudflare.record_exists(
                          dict_records=domain_records,
                          str_record_type=Cloudflare.CNAME_RECORD,
                          str_record_val=SimpleLogin.DKIM_RECORD1_VAL,
                          str_recordname=str_record_name)
print ("DKIM1 Record Exists: " + str(dkim1_record_exists))

if not dkim1_record_exists:
    print ("DKIM1 Record needed")
    str_domain_comment: str = "SimpleLogin DKIM1 Record for " + new_subdomain
    Cloudflare.write_new_record(str_domain_root=str_root_domain,
                                str_record_type=Cloudflare.CNAME_RECORD,
                                str_record_val=SimpleLogin.DKIM_RECORD1_VAL,
                                str_recordname=str_record_name,
                                str_comment=str_domain_comment)


str_record_name: str = SimpleLogin.DKIM_RECORD2 + new_subdomain
dkim2_record_exists: bool = Cloudflare.record_exists(
                          dict_records=domain_records,
                          str_record_type=Cloudflare.CNAME_RECORD,
                          str_record_val=SimpleLogin.DKIM_RECORD2_VAL,
                          str_recordname=str_record_name)
print ("DKIM2 Record Exists: " + str(dkim2_record_exists))

if not dkim2_record_exists:
    print ("DKIM2 Record needed")
    str_domain_comment: str = "SimpleLogin DKIM2 Record for " + new_subdomain
    Cloudflare.write_new_record(str_domain_root=str_root_domain,
                                str_record_type=Cloudflare.CNAME_RECORD,
                                str_record_val=SimpleLogin.DKIM_RECORD2_VAL,
                                str_recordname=str_record_name,
                                str_comment=str_domain_comment)



str_record_name: str = SimpleLogin.DKIM_RECORD3 + new_subdomain
dkim3_record_exists: bool = Cloudflare.record_exists(
                          dict_records=domain_records,
                          str_record_type=Cloudflare.CNAME_RECORD,
                          str_record_val=SimpleLogin.DKIM_RECORD3_VAL,
                          str_recordname=str_record_name)
print ("DKIM3 Record Exists: " + str(dkim3_record_exists))

if not dkim3_record_exists:
    print ("DKIM3 Record needed")
    str_domain_comment: str = "SimpleLogin DKIM3 Record for " + new_subdomain
    Cloudflare.write_new_record(str_domain_root=str_root_domain,
                                str_record_type=Cloudflare.CNAME_RECORD,
                                str_record_val=SimpleLogin.DKIM_RECORD3_VAL,
                                str_recordname=str_record_name,
                                str_comment=str_domain_comment)

# Add DMARC Record

str_record_name: str = SimpleLogin.DMARC_RECORD_VAL + new_subdomain
dmarc_record_exists: bool = Cloudflare.record_exists(
                          dict_records=domain_records,
                          str_record_type=Cloudflare.TXT_RECORD,
                          str_record_val=SimpleLogin.DMARC_VAL,
                          str_recordname=str_record_name)
print ("DMARC Record Exists: " + str(dmarc_record_exists))

if not dmarc_record_exists:
    print ("DMARC Record needed")
    str_domain_comment: str = "SimpleLogin DMARC Record for " + new_subdomain
    Cloudflare.write_new_record(str_domain_root=str_root_domain,
                                str_record_type=Cloudflare.TXT_RECORD,
                                str_record_val=SimpleLogin.DMARC_VAL,
                                str_recordname=str_record_name,
                                str_comment=str_domain_comment)
