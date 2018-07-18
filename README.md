# certbot-regru
Reg.ru DNS authenticator plugin for certbot

An authenticator plugin for [certbot](https://certbot.eff.org/) to support [Let's Encrypt](https://letsencrypt.org/) 
DNS challenges (dns-01) for domains managed by the nameservers of [Reg.ru](https://www.reg.ru).

## Requirements
* certbot (>=0.21.1)

For older Ubuntu distributions check out this PPA: 
[ppa:certbot/certbot](https://launchpad.net/~certbot/+archive/ubuntu/certbot)

## Installation
1. First install the plugin:
 * Without dependencies (if using certbot from your distribution repository):
   ```
   python3 setup.py develop --no-deps
   ```
 * With dependencies (not recommended if using certbot from your distribution repositories):
   ```
   python3 setup.py install
   ```
 * With certbot-auto (needs to be reinstalled after every certbot-auto update):
   ```
   /root/.local/share/letsencrypt/bin/pip install .
   ```

2. Configure it with your Reg.ru Credentials:
   ```
   vim /etc/letsencrypt/regru.ini
   ```

3. Make sure the file is only readable by root! Otherwise all your domains might be in danger:
   ```
   chmod 0600 /etc/letsencrypt/regru.ini
   ```

## Usage
Request new certificates via a certbot invocation like this:

    certbot certonly -a certbot-regru:dns -d sub.domain.tld -d *.wildcard.tld

Renewals will automatically be performed using the same authenticator and credentials by certbot.

## Command Line Options
```
 --certbot-regru:dns-propagation-seconds PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS record. (default: 120)
 --certbot-regru:dns-credentials PATH_TO_CREDENTIALS
                        Path to Reg.ru account credentials INI file (default: /etc/letsencrypt/regru.ini)

```

See also `certbot --help certbot-regru:dns` for further information.
