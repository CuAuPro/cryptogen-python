import json

# ---------------------------------------------------------------------------- #
#                              Cloud request model                             #
# ---------------------------------------------------------------------------- #
class CloudCertModel:
    def __init__(self, store_folder, signing_cert_path, passcode, new_alias, validity_period, new_passcode, cloud_operator, gui):
        self.store_folder = store_folder
        self.signing_cert_path = signing_cert_path
        self.passcode = passcode
        self.new_alias = new_alias
        self.validity_period = validity_period
        self.new_passcode = new_passcode
        self.cloud_operator = cloud_operator
        self.gui = gui

    def to_json(self):
        return json.dumps({
            "store_folder": self.store_folder,
            "signing_cert_path": self.signing_cert_path,
            "passcode": self.passcode,
            "new_alias": self.new_alias,
            "validity_period": self.validity_period,
            "new_passcode": self.new_passcode,
            "cloud_operator": self.cloud_operator,
            "gui": self.gui
        }, indent=4)
        
class Client:
    def __init__(self, new_alias, validity_period, new_passcode, dns_names, ipv4_addresses, ipv6_addresses):
        self.new_alias = new_alias
        self.validity_period = validity_period
        self.new_passcode = new_passcode
        self.dns_names = dns_names
        self.ipv4_addresses = ipv4_addresses
        self.ipv6_addresses = ipv6_addresses

# ---------------------------------------------------------------------------- #
#                               Truststore model                               #
# ---------------------------------------------------------------------------- #
class TruststoreModel:
    def __init__(self, store_folder, signing_cert_path, passcode, new_alias, new_passcode, keytool_path, gui):
        self.store_folder = store_folder
        self.signing_cert_path = signing_cert_path
        self.passcode = passcode
        self.new_alias = new_alias
        self.new_passcode = new_passcode
        self.keytool_path = keytool_path
        self.gui = gui

    def to_json(self):
        return json.dumps({
            "store_folder": self.store_folder,
            "signing_cert_path": self.signing_cert_path,
            "passcode": self.passcode,
            "new_alias": self.new_alias,
            "new_passcode": self.new_passcode,
            "keytool_path": self.keytool_path,
            "gui": self.gui
        }, indent=4)

# ---------------------------------------------------------------------------- #
#                             Client request model                             #
# ---------------------------------------------------------------------------- #
class ClientsCertModel:
    def __init__(self, store_folder, signing_cert_path, passcode, clients, gui):
        self.store_folder = store_folder
        self.signing_cert_path = signing_cert_path
        self.passcode = passcode
        self.clients = clients
        self.gui = gui

    def to_json(self):
        clients_list = []
        for client in self.clients:
            clients_list.append({
                "new_alias": client.new_alias,
                "validity_period": client.validity_period,
                "new_passcode": client.new_passcode,
                "dns_names": client.dns_names,
                "ipv4_addresses": client.ipv4_addresses,
                "ipv6_addresses": client.ipv6_addresses
            })

        return json.dumps({
            "store_folder": self.store_folder,
            "signing_cert_path": self.signing_cert_path,
            "passcode": self.passcode,
            "clients": clients_list,
            "gui": self.gui
        }, indent=4)
        

# ---------------------------------------------------------------------------- #
#                           Client extract PKCS model                          #
# ---------------------------------------------------------------------------- #
class ClientExtract:
    def __init__(self, path, alias, passcode, ca, crt, key):
        self.path = path
        self.alias = alias
        self.passcode = passcode
        self.ca = ca
        self.crt = crt
        self.key = key

class ClientsExtractModel:
    def __init__(self, clients, gui):
        self.clients = clients
        self.gui = gui

    def to_json(self):
        clients_list = []
        for client in self.clients:
            clients_list.append({
                "path": client.path,
                "alias": client.alias,
                "passcode": client.passcode,
                "ca": client.ca,
                "crt": client.crt,
                "key": client.key
            })

        return json.dumps({
            "clients": clients_list,
            "gui": self.gui
        }, indent=4)
        

# ---------------------------------------------------------------------------- #
#                       Client generate MCU header model                       #
# ---------------------------------------------------------------------------- #
class ClientHeader:
    def __init__(self, path, alias):
        self.path = path
        self.alias = alias

class ClientsHeaderModel:
    def __init__(self, clients, gui):
        self.clients = clients
        self.gui = gui

    def to_json(self):
        clients_list = []
        for client in self.clients:
            clients_list.append({
                "path": client.path,
                "alias": client.alias
            })

        return json.dumps({
            "clients": clients_list,
            "gui": self.gui
        }, indent=4)

