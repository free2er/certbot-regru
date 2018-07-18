# certbot-regru
Reg.ru DNS authenticator plugin for Certbot

An authenticator plugin for [certbot](https://certbot.eff.org/) to support [Let's Encrypt](https://letsencrypt.org/) 
DNS challenges (dns-01) for domains managed by the nameservers of [Reg.ru](https://www.reg.ru).

## Requirements
* certbot (>=0.21.1)

For older Ubuntu distributions check out this PPA: 
[ppa:certbot/certbot](https://launchpad.net/~certbot/+archive/ubuntu/certbot)

## Installation
1. First install the plugin:
   ```
   sudo pip install certbot-regru
   ```

2. Configure it with your Reg.ru Credentials:
   ```
   sudo vim /etc/letsencrypt/regru.ini
   ```

3. Make sure the file is only readable by root! Otherwise all your domains might be in danger:
   ```
   sudo chmod 0600 /etc/letsencrypt/regru.ini
   ```

## Usage
Request new certificates via a certbot invocation like this:

    sudo certbot certonly -a certbot-regru:dns -d sub.domain.tld -d *.wildcard.tld

Renewals will automatically be performed using the same authenticator and credentials by certbot.

## Command Line Options
```
 --certbot-regru:dns-propagation-seconds PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS record. 
                        (default: 120)
 --certbot-regru:dns-credentials PATH_TO_CREDENTIALS
                        Path to Reg.ru account credentials INI file 
                        (default: /etc/letsencrypt/regru.ini)

```

See also `certbot --help certbot-regru:dns` for further information.

## Removal
   ```
   sudo pip uninstall certbot-regru
   ```
