# SimpleLogin-CloudflareUpdate
A Repo to help make SimpleLogin subdomains quikcly via CloudFlare. 

# First Time Setup

1. Make a folder named ***local*** in the root of the checked out project folder.
2. Create a blank text file in ***local*** called ***cloudflare_vars*** with the following data:

  ``` 
  cloudflare_email: myname@myexampledoamin.com
  cloudflare_auth_token: my_cloudflare_api_token
  ```

3. Create a blank text file in ***local*** called ***subdomain_vars*** with the following data:

  ``` 
  simplelogin_owner_key: MY_VERIFY_KEY
  new_domain_key: MY_TARGET_SUBDOMAIN
  ```
 
4. For entire domain, create an API key in Cloudflare. Copy the values into the ./local/cloudflare_vars file:

```
cloudflare_email: mycloudflareaccount@gmail.com
cloudflare_auth_token: authorization_token_set_up_in_cloudflare
```

# Sub-domain Setup (per subdomain)

1. Go to SimpleLogin page, and type in complete subdomain:

* Ex: ***shirts.clothes.myexampledomain.com***

[![Simple Login Start Page](https://github.com/IronTooch/SimpleLogin-CloudflareUpdate/raw/main/images/SimpleLogin_Start.png)](https://github.com/IronTooch/SimpleLogin-CloudflareUpdate/raw/main/images/SimpleLogin_Start.png)


2. You will get a Verification page

[![Simple Login Verify Domain Page](https://github.com/IronTooch/SimpleLogin-CloudflareUpdate/blob/main/images/SimpleLogin_Domain_Verify.png)](https://github.com/IronTooch/SimpleLogin-CloudflareUpdate/blob/main/images/SimpleLogin_Domain_Verify.png)

* Copy the full domain (e.g. shirts.clothes.myexampledomain.com)
* Place the full domain in ***./local/subdomain_vars***
* Copy the Value from Domain Ownership Verification section
* Place the value in ***./local/subdomain_vars***

E.g.

  ``` 
  simplelogin_owner_key: si-verification=ngkwprkicxapsbacyaliguaybpxmay
  new_domain_key: shirts.clothes.myexampledomain.com
  ```

3. In VS Code, once the file edits have occured, Click "Run", then click "Run without Debugging". This will create all the records on the target domain.
4. Wait 2 minutes after running for domain to update. Then click Verify on the Verification Page in SimpleLogin.
5. Once the record is validated, then go through the rest of the SimpleLogin Domain page, and click verify on the remaining values:

[![Simple Login Verify Records Page](https://github.com/IronTooch/SimpleLogin-CloudflareUpdate/raw/main/images/SimpleLogin_Domain_Records.png)](https://github.com/IronTooch/SimpleLogin-CloudflareUpdate/raw/main/images/SimpleLogin_Domain_Records.png)

6. Once this is complete, the SimpleLogin domain is ready for use!
