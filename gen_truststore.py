from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
import os
import json
import subprocess
import argparse
import logger
import logging
import base64

def gen_truststore(config):
 
    store_folder = config["store_folder"]
    signing_cert_path = config["signing_cert_path"]
    passcode = config["passcode"]

    new_alias = config["new_alias"]
    new_passcode = config["new_passcode"]
    
    keytool_path = config["keytool_path"]
    
    if passcode is not None:
        passcode = bytes(passcode, 'utf-8')
        
    if config["gui"]:
        p12_data = base64.b64decode(config["signing_cert_path"])
    else:
        signing_cert_path = config["signing_cert_path"]

        # Load the signing certificate and private key from the .p12 file
        with open(signing_cert_path, "rb") as f:
            p12_data = f.read()

    private_key, cert, additional_certs = load_key_and_certificates(p12_data, passcode)
    
    signing_cert_cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    # Build a certificate chain from the intermediate and root certificates
    chain = [cert]
    found_root = False
    for c in additional_certs:
        chain.append(c)
        if c.subject == c.issuer:
            found_root = True
    if found_root == False:
        raise ValueError('Could not find the root certificate in the chain')
        

    cert_data = cert.public_bytes(serialization.Encoding.PEM)                    # cloud certificate

    if not os.path.isdir(store_folder):
        os.mkdir(store_folder)

    with open(store_folder+signing_cert_cn+".crt", "wb") as f:
        f.write(cert_data)
        
    cmd = f'"{keytool_path}" \
                -keystore {store_folder+new_alias}.p12 \
                -keypass {passcode.decode()} \
                -alias {signing_cert_cn} \
                -import -file {store_folder+signing_cert_cn}.crt \
                -storepass {new_passcode}'
                
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate(input=b'yes\n')
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        description='Generate truststore.'
                        )
    parser.add_argument("-p", "--config-path", type=str, default="config/truststore_req.json",
                        help="Path to config file.")
    args = parser.parse_args()


    config_path = args.config_path
    # Open the JSON file
    with open(config_path) as f:
        # Load the JSON data
        config = json.load(f)
        
    logger.init_logger(print_to_stdout=True)
    logging.info('Start generation truststore.')
    gen_truststore(config)
    logging.info('End generation truststore.')

    
