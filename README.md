# Tool for generating self signed intermediate and client certificates.

This tool is primary intended to use for certificate geenration (.p12 fromat) for [Arrowhead](https://github.com/eclipse-arrowhead/core-java-spring/) platform.

Arrowhead (and its continuation, [Productive4.0](https://productive40.eu/)) is an ambitious holistic innovation project, meant to open the doors to the potentials of Digital Industry and to maintain a leadership position of the industries in Europe. The Arrowhead Framework enables the design and implementation of automation systems in application domains such as production, smart cities, e-mobility, energy, and buildings. It was created to efficiently address Industry 4.0 requirements, primarily through scalable, secure, and flexible information sharing that enables system interoperability and integration

# Table of contents
- [Acknowledgements](#acknowledgements)
- [Requirements](#requirements)
- [Intermediate (cloud) certificate generation](#cloud_generation)
- [End-entity (client) certificate generation](#client_generation)
- [Truststore generation](#truststore_generation)
    * [Truststore with Python script](#truststore_python)
    * [Truststore with KeyStore Explorer](#truststore_manual)
- [Extract PKCS12 certificate](#extract_pkcs12)

# Acknowledgements <a id='acknowledgements'></a>

This tool stems from the [AI REDGIO5.0](#https://www.airedgio5-0.eu/) project (Regions and (E)DIHs alliance for AI-at-the-Edge adoption by European Industry 5.0 Manufacturing SMEs), which has received funding from the European Union’s Horizon Europe Research and Innovation Programme under Grant Agreement No. 101092069. The tool has been developed for Slovenian regional experiment.

# Requirements <a id='requirements'></a>

```
cryptography==40.0.2
```

# Intermediate (cloud) certificate generation <a id='cloud_generation'></a>

To generate cloud certificates, you will need to use the `gen_cloud_certify.py` script with a configuration file. Before running this script, make sure you have all the dependencies installed.

To generate the certificates, follow these steps:

1. Obtain the root (`master.p12`) self-signed certificate.

2. Edit a configuration file named `config/cloud_certifi_req.json` with the following content:

```json
{
    "store_folder":         "generated_certificates/<cloud_name>/",
    "signing_cert_path":   "<path_to_master_cert>",
    "passcode":             "123456",

    "new_alias":            "<cloud_name>",
    "validity_period":      "10 years",
    "new_passcode":         "<passcode>",

    "cloud_operator":       "<cloud_operator>"
}
```

Here is what each option in the configuration file does:

 - `store_folder`: The folder where the generated certificates will be stored.

 - `signing_cert_path`: The path to the root (master) self-signed certificate.

 - `new_alias`:  The alias for the new cloud certificate.

 - `passcode`: The password for the root (master) self-signed certificate.
new_alias: The alias for the new cloud certificate.

 - `validity_period`: The validity period of the new cloud certificate (`N days/months/years`).

 - `new_passcode`: The password for the new cloud certificate.

 - `cloud_operator`: The name of the cloud operator.

3. Run the following command to generate the cloud certificates:



```bash
python gen_cloud_certify.py -p <path_to_config_file>
```
The `-p` option is optional and can be used to specify the path to the configuration file. If you do not use the `-p` option, the script will look for a file named `config/cloud_certifi_req.json`.

4. After running the command, the script will generate certificates in `store_folder`.



# End-entity (client) certificate generation <a id='client_generation'></a>

To generate client certificates, you will need to use the `gen_client_certify.py` script with a configuration file. Before running this script, make sure you have all the dependencies installed.

To generate the certificates, follow these steps:

1. Obtain the intermediate (cloud) self-signed certificate.

2. Edit a configuration file named `config/client_certifi_req.json` with the following content:

```json
{
    "store_folder":         "generated_certificates/<cloud_name>/",
    "signing_cert_path":    "generated_certificates/<cloud_name>/<new_alias_of_cloud_cert>",
    "passcode":             "<passcode_of_cloud_cert>",

    "clients": [
        {
            "new_alias":            "<client1_alias>",
            "validity_period":      "10 years",
            "new_passcode":         "<new_passcode>",
            "dns_names":            ["<SANdns1>", "<SANdns2>"],
            "ipv4_addresses":       ["<SANip1>", "<SANip2>"],
            "ipv6_addresses":       ["<SANip3>", "<SANip4>"]
        },
        {
            "new_alias":            "<client2_alias>",
            "validity_period":      "10 years",
            "new_passcode":         "<new_passcode>",
            "dns_names":            ["<SANdns1>", "<SANdns2>"],
            "ipv4_addresses":       ["<SANip1>", "<SANip2>"],
            "ipv6_addresses":       ["<SANip3>", "<SANip4>"]
        }
    ]

}
```

Here is what each option in the configuration file does:

 - `store_folder`: The folder where the generated certificates will be stored.

 - `signing_cert_path`: The path to the intermediate (cloud) certificate.

 - `passcode`: The password for the intermediate (cloud) certificate.

 - `new_alias`:  The alias for the new client certificate.

 - `validity_period`: The validity period of the new client certificate (`N days/months/years`).

 - `new_passcode`: The password for the new client certificate.

 - `dns_names`: DNS names for SAN.

 - `ipv4_addresses`: IPv4 addresses for SAN.

 - `ipv6_addresses`: IPv6 addresses for SAN.

3. Run the following command to generate the client certificates:


```bash
python gen_client_certify.py -p <path_to_config_file>
```
The `-p` option is optional and can be used to specify the path to the configuration file. If you do not use the `-p` option, the script will look for a file named `config/client_certifi_req.json`.

4. After running the command, the script will generate certificates in `store_folder`.




# Truststore generation <a id='truststore_generation'></a>

Truststore can be generated in two ways, described below.

## Truststore with Python script <a id='truststore_python'></a>
To generate cloud certificates, you will need to use the `gen_truststore.py` script with a configuration file. Before running this script, make sure you have all the dependencies installed.

`INFO`: You need to have installed `keytool` from Java.

To generate the certificates, follow these steps:

1. Edit a configuration file named `config/truststore_req.json` with the following content:

```json
{
    "store_folder":         "generated_certificates/<cloud_name>/",
    "signing_cert_path":    "generated_certificates/<cloud_name>/<new_alias_of_cloud_cert>",
    "passcode":             "<passcode_of_cloud_cert>",

    "new_alias":            "truststore",
    "new_passcode":         "<passcode>",

    "keytool_path":         "<path_to_keytool>"

}
```

Here is what each option in the configuration file does:

 - `store_folder`: The folder where the generated truststore will be stored.

 - `signing_cert_path`: The path to the intermediate (cloud) certificate.

 - `passcode`: The password for the intermediate (cloud) certificate.
new_alias: The alias for the new cloud certificate.

 - `new_alias`:  The alias for the truststore.

 - `new_passcode`: The password for the truststore.

 - `keytool_path`: Path to Java keytool.

2. Run the following command to generate the client certificates:


```bash
python gen_truststore.py -p <path_to_config_file>
```
The `-p` option is optional and can be used to specify the path to the configuration file. If you do not use the `-p` option, the script will look for a file named `config/truststore.json`.

3. After running the command, the script will generate certificates in `store_folder`.



## Truststore with KeyStore Explorer <a id='truststore_manual'></a>

You should follow [instructions](https://github.com/eclipse-arrowhead/core-java-spring/blob/master/documentation/certificates/create_trust_store.pdf).



# Extract PKCS12 certificate <a id='extract_pkcs12'></a>


This script loads a PKCS12 file (.p12) that contains a private key, a client certificate, and additional CA certificates. It then exports specified files: certificate, private key and (or) all additional CA certificates.

To generate seperate files, you will need to use the `extract_pkcs12_certs.py` script with a configuration file. Before running this script, make sure you have all the dependencies installed.

To generate the certificates, follow these steps:


1. Edit a configuration file named `config/truststore_req.json` with the following content:

```json
{
    "clients": [
        {
            "path":     "generated_certificates/<cloud_name>/",
            "alias":    "<client1_alias>",
            "passcode": "<passcode>",
            "ca":       true,
            "crt":      true,
            "key":      true

        },
        {
            "path":     "generated_certificates/<cloud_name>/",
            "alias":    "<client2_alias>",
            "passcode": "<passcode>",
            "ca":       true,
            "crt":      true,
            "key":      true

        }
    ]

}
```

Here is what each option in the configuration file does:

 - `path`: The folder where the folder of generated files will be stored.

 - `alias`:  The alias of client.

 - `passcode`: The password of the client certificate.

 - `ca`: If export additional CA certificates: true/false

 - `crt`: If export certificate: true/false

 - `key`: If export private key: true/false



2. Run the following command to generate the client certificates:


```bash
python extract_pkcs12_certs.py -p <path_to_config_file>
```
The `-p` option is optional and can be used to specify the path to the configuration file. If you do not use the `-p` option, the script will look for a file named `config/extract_pkcs12_req.json`.

3. After running the command, the script will generate certificates in `path/alias`.
