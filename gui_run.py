from nicegui import events, ui
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from utils import find_keytool_executable
from models import *
import json
import base64

from gen_cloud_cert import gen_cloud_cert
from gen_truststore import gen_truststore
from gen_client_cert import gen_client_cert
from extract_pkcs12_certs import extract_pkcs12
from gen_mcu_header_pem import gen_mcu_header_pem
from gen_mcu_header_der import gen_mcu_header_der

from cryptography import x509

class Configuration():
    
    def __init__(self):
        self.master_cert = None
        self.master_cert_passcode = ""
        
        
        self.cloud_folder_path = ""
        self.cloud_cert = None
        self.cloud_cert_passcode = ""
        
        self.cloud_req_json = None
        self.client_req_json = None
        self.truststore_json = None
        self.client_req_extract_json = None
        self.client_req_header_json = None

    
    
    
config = Configuration()
    

def cloud_gen():
    global config

    def cb_gen_cloud_cert():
        validity_period = str(cert_duration_num.value)+ " " + cert_duration_type.value
        config.cloud_folder_path = "generated_certificates/"+cloud_name.value+"."+cloud_operator.value+"/"
        cert_base64 = base64.b64encode(config.master_cert).decode('utf-8')

        model = CloudCertModel(store_folder=config.cloud_folder_path,
                               signing_cert_path=cert_base64,
                               passcode=config.master_cert_passcode,
                               new_alias=cloud_name.value,
                               validity_period=validity_period,
                               new_passcode=cloud_cert_pass.value,
                               cloud_operator=cloud_operator.value,
                               gui=True)
        req = json.loads(model.to_json())
        
        p12 = gen_cloud_cert(req)
        ui.notify(f'Cloud certificate successfully generated', color="green")
        
        if(cb_gen_truststore.value):
            keytool_path = find_keytool_executable()
            
            if keytool_path is None:
                ui.notify(f'Cannot find keytool! Use manual truststore generator', color="red")
                return
            cert_base64 = base64.b64encode(p12).decode('utf-8')

            model = TruststoreModel(store_folder=config.cloud_folder_path,
                                    signing_cert_path=cert_base64,
                                    passcode=cloud_cert_pass.value,
                                    new_alias="truststore",
                                    new_passcode=cloud_cert_pass.value,
                                    keytool_path=keytool_path,
                                    gui=True)
            req = json.loads(model.to_json())
            gen_truststore(req)
            ui.notify(f'Trustrstore successfully generated', color="green")
            
        return
            
    def cb_gen_cloud_cert_json():
        gen_cloud_cert(config.cloud_req_json)
        ui.notify(f'Cloud certificate successfully generated', color="green")
        return
    
    def cb_gen_truststore_json():
        gen_truststore(config.truststore_json)
        ui.notify(f'Truststore successfully generated', color="green")
        return
    
    def handle_upload_master_cert(e: events.UploadEventArguments):
        config.master_cert = e.content.read()
        return
    
    def handle_upload_cloud_json(e: events.UploadEventArguments):
        config.cloud_req_json = json.loads(e.content.read())
        b_gen_cloud_json.props("disable=false")
        return
    
    def handle_upload_truststore_json(e: events.UploadEventArguments):
        config.truststore_json = json.loads(e.content.read())
        b_gen_truststore_json.props("disable=false")
        return
    
    
                
    def set_master_cert_pass(e: events.UploadEventArguments):
        try:
            _ = load_key_and_certificates(config.master_cert, bytes(master_cert_pass.value, 'utf-8'))
            ui.notify(f'Password is correct!', color="green")
            config.master_cert_passcode = master_cert_pass.value
        except ValueError as ve:
            ui.notify(f'Password is wrong!', color="red")
            config.master_cert_passcode = None
            
    with ui.tabs().classes('w-full') as tabs:
        wizard_tab = ui.tab("wizard_tab", label='WIZARD')
        json_import_tab = ui.tab("json_import_tab", label='JSON IMPORT')


    with ui.tab_panels(tabs, value=wizard_tab).classes("w-full justify-center") as panelsType:
        
        with ui.tab_panel(wizard_tab):

            with ui.row().classes("w-full justify-center"):
                    
                with ui.column().classes("p-4 border rounded-lg no-wrap items-center grid-rows-1 grid-flow-row grid gap-1.5"):
                   
                    ui.label("Upload master certificate")
                
                    ui.upload(on_upload=handle_upload_master_cert, auto_upload=True).classes('max-w-full')
                    
                    with ui.row().classes("items-center w-full"):
                        master_cert_pass = ui.input(label="Password", password=True, password_toggle_button=True).classes("basis-3/5")
                        ui.button(on_click=set_master_cert_pass, icon='check').classes("basis-1/4")
                            
                         
                    cloud_name = ui.input(label="Cloud name")
                    cloud_operator = ui.input(label="Cloud operator")

                    with ui.row().classes("items-center w-full"):
                        cert_duration_num = ui.input(value=1).classes("basis-1/5")
                        cert_duration_type = ui.select(options=["years", "months", "days"], value="years").classes("basis-1/4")
                    
                    cloud_cert_pass = ui.input(label="Password", password=True, password_toggle_button=True)
                    
                    cb_gen_truststore = ui.checkbox('Generate truststore.')
            
                    b_gen_cloud = ui.button('GENERATE', on_click=cb_gen_cloud_cert)
                            
            
        with ui.tab_panel(json_import_tab):
            with ui.row().classes("w-full justify-center"):
                with ui.column().classes("no-wrap items-center grid-rows-1 grid-flow-row grid gap-1.5"):
                    with ui.row():
                        with ui.column().classes("p-4 border rounded-lg"):
                            ui.label("Upload cloud json request file")
                            ui.upload(on_upload=handle_upload_cloud_json, auto_upload=True).classes('max-w-full')
                            b_gen_cloud_json = ui.button('GENERATE CLOUD', on_click=cb_gen_cloud_cert_json).props('disable')
                        with ui.column().classes("p-4 border rounded-lg"):
                            ui.label("Upload truststore json request file")
                            ui.upload(on_upload=handle_upload_truststore_json, auto_upload=True).classes('max-w-full')
                            b_gen_truststore_json = ui.button('GENERATE TRUSTSTORE', on_click=cb_gen_truststore_json).props('disable')



def client_gen():
    global config
    
    def cb_gen_client_cert():
        
        validity_period = str(cert_duration_num.value)+ " " + cert_duration_type.value
        cert_base64 = base64.b64encode(config.cloud_cert).decode('utf-8')
        
        dns_names = []
        ipv4_addresses = []
        ipv6_addresses = []
        
        for entry in table.rows:
            if entry['type'] == 'DNS':
                dns_names.append(entry['val'])
            elif entry['type'] == 'IPv4':
                ipv4_addresses.append(entry['val'])
            elif entry['type'] == 'IPv6':
                ipv6_addresses.append(entry['val'])
                  
        client = Client(new_alias=system_name.value,
                        validity_period=validity_period,
                        new_passcode=client_cert_pass.value,
                        dns_names=dns_names,
                        ipv4_addresses=ipv4_addresses,
                        ipv6_addresses=ipv6_addresses)
        clients = [client]
        
        model = ClientsCertModel(store_folder=config.cloud_folder_path,
                                signing_cert_path=cert_base64,
                                passcode=config.cloud_cert_passcode,
                                clients=clients,
                                gui=True)
        req = json.loads(model.to_json())
        
        gen_client_cert(req)
        ui.notify(f'Client certificate successfully generated', color="green")
        
        if(cb_extract_certi.value):
            client = ClientExtract(path=config.cloud_folder_path,
                                   alias=system_name.value,
                                   passcode=client_cert_pass.value,
                                   ca=True,
                                   crt=True,
                                   key=True)
            clients = [client]
            model = ClientsExtractModel(clients,
                                        gui=True)
            req = json.loads(model.to_json())
            
            extract_pkcs12(req)
            ui.notify(f'Client certificate successfully extracted', color="green")
            
        if(cb_export_mcu_header_pem.value):
            client = ClientHeader(path=config.cloud_folder_path,
                                  alias=system_name.value)
            clients = [client]
            model = ClientsHeaderModel(clients=clients,
                                       gui=True)

            req = json.loads(model.to_json())
            
            gen_mcu_header_pem(req)
            ui.notify(f'Client certificate header PEM exported', color="green")
            
        if(cb_export_mcu_header_der.value):

            client = ClientHeader(path=config.cloud_folder_path,
                                  alias=system_name.value)
            clients = [client]
            model = ClientsHeaderModel(clients=clients,
                                       gui=True)

            req = json.loads(model.to_json())
            
            gen_mcu_header_der(req)
            ui.notify(f'Client certificate header DER exported', color="green")
                             
        return
    
    def cb_gen_client_cert_json():
        gen_client_cert(config.client_req_json)
        ui.notify(f'Client certificate(s) successfully generated', color="green")
        
        return

    def cb_gen_client_extract_json():
        extract_pkcs12(config.client_req_extract_json)
        ui.notify(f'Client certificate successfully extracted', color="green")
        
        return
     
    def cb_gen_client_header_json():
        gen_mcu_header_pem(config.client_req_header_json)
        gen_mcu_header_der(config.client_req_header_json)
        ui.notify(f'Client certificate headers exported', color="green")
        return
        
    def handle_upload_client_cert(e: events.UploadEventArguments):
        config.cloud_cert = e.content.read()
        return
    
    def handle_upload_client_json(e: events.UploadEventArguments):
        config.client_req_json = json.loads(e.content.read())
        b_gen_client_json.props("disable=false")
        return
    
    def handle_upload_client_extract_json(e: events.UploadEventArguments):
        config.client_req_extract_json = json.loads(e.content.read())
        b_client_extract_json.props("disable=false")
        return

    def handle_upload_client_header_json(e: events.UploadEventArguments):
        config.client_req_header_json = json.loads(e.content.read())
        b_gen_header_json.props("disable=false")
        return
    
    
    
    def set_client_cert_pass(e: events.UploadEventArguments):
        try:
            _, cert, _ = load_key_and_certificates(config.cloud_cert, bytes(cloud_cert_pass.value, 'utf-8'))
            ui.notify(f'Password is correct!', color="green")
            subdomain = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
            # Split the subdomain by dots
            parts = subdomain.split('.')
            extracted_parts = parts[-4:-2]
            config.cloud_folder_path = "generated_certificates/"+ '.'.join(extracted_parts)+"/"
            config.cloud_cert_passcode = cloud_cert_pass.value
        except ValueError as ve:
            ui.notify(f'Password is wrong!', color="red")
            config.cloud_cert_passcode = None
    columns = [
        {'name': "type", 'label': 'Subject Alternative Name', 'field': "type"},
        {'name': "val", 'label': '', 'field': "val"},
        {'name': "id", 'label': '', 'field': "id"}
    ]
    rows = [
        {'id':0, 'type': "IPv4", 'val': "127.0.0.1"},
        {'id':1, 'type': "DNS", 'val': "localhost"},
    ]
    rows = []
    san_type_options = ["DNS", "IPv4", "IPv6"]
    def add_row(e: events.GenericEventArguments):
        if len(table.rows) == 0:
            id_to_add = 0
        else:
            id_to_add = max(table.rows, key=lambda x: x['id'])['id']+1
        row_to_add = {'id': id_to_add, 'type': "", 'val': ""}
        table.add_rows(row_to_add)

    def remove_row(e: events.GenericEventArguments):
        table.remove_rows(e.args)
        pass

    def rename(e: events.GenericEventArguments) -> None:
        for row in table.rows:
            if row['id'] == e.args['id']:
                row['type'] = e.args['type']
                row['val'] = e.args['val']
                


    
    with ui.tabs().classes('w-full') as tabs:
        wizard_tab = ui.tab("wizard_tab", label='WIZARD')
        json_import_tab = ui.tab("json_import_tab", label='JSON IMPORT')


    with ui.tab_panels(tabs, value=wizard_tab).classes("w-full justify-center") as panelsType:
        
        with ui.tab_panel(wizard_tab):

            with ui.row().classes("w-full justify-center"):
                    
                with ui.column().classes("p-4 border rounded-lg no-wrap items-center grid-rows-1 grid-flow-row grid gap-1.5"):
                    
                        ui.label("Upload cloud certificate")
                        
                        ui.upload(on_upload=handle_upload_client_cert, auto_upload=True).classes('max-w-full')
                        
                        with ui.row().classes("items-center w-full"):
                            cloud_cert_pass = ui.input(label="Password", password=True, password_toggle_button=True).classes("basis-3/5")
                            ui.button(on_click=set_client_cert_pass, icon='check').classes("basis-1/4")
                                
                            
                         
                        system_name = ui.input(label="System name")
                        table = ui.table(columns=columns, rows=rows, row_key='id')
                        table.add_slot('body', r'''
                            <q-tr :props="props">
                                <q-td key="type" :props="props">
                                    <q-select
                                        v-model="props.row.type"
                                        :options="''' + str(san_type_options) + r'''"
                                        @update:model-value="() => $parent.$emit('rename', props.row)"
                                    />
                                </q-td>
                                
                                <q-td key="val" :props="props">
                                    <q-input
                                        v-model="props.row.val"
                                        clearable
                                        @update:model-value="() => $parent.$emit('rename', props.row)"
                                    />
                                </q-td>    
                                <q-td key="id" :props="props">               
                                    <q-btn icon="delete" color="red"
                                        v-bind="props.row.id"
                                        @click="$parent.$emit('remove_row', props.row)"
                                    />
                                </q-td>     
                                                    
                            </q-tr>
                        ''')
    

                        with ui.row().classes("justify-center"):
                            ui.button('ADD SAN', on_click=add_row)
                        table.on('rename', rename)
                        table.on('remove_row', remove_row)

                        with ui.row().classes("items-center w-full"):
                            cert_duration_num = ui.input(value=1).classes("basis-1/5")
                            cert_duration_type = ui.select(options=["years", "months", "days"], value="years").classes("basis-1/4")
                        
                        client_cert_pass = ui.input(label="Password", password=True, password_toggle_button=True)
                        
                        with ui.row().classes("w-full justify-center"):
                            cb_extract_certi = ui.checkbox('Extract pkcs12.')
                            cb_export_mcu_header_pem = ui.checkbox('Export .h PEM.')
                            cb_export_mcu_header_der = ui.checkbox('Export .h DER.')

                        b_gen_client = ui.button('GENERATE', on_click=cb_gen_client_cert)
                            
            
        with ui.tab_panel(json_import_tab):
            
            with ui.row().classes("w-full justify-center"):
                with ui.column().classes("no-wrap items-center grid-rows-1 grid-flow-row grid gap-1.5"):
                    with ui.row():
                        with ui.column().classes("p-4 border rounded-lg"):
                            ui.label("Upload client json request file")
                            ui.upload(on_upload=handle_upload_client_json, auto_upload=True).classes('max-w-full')
                            b_gen_client_json = ui.button('GENERATE CLIENT', on_click=cb_gen_client_cert_json).props("disable")

                        with ui.column().classes("p-4 border rounded-lg"):
                            ui.label("Upload client extract json request file")
                            ui.upload(on_upload=handle_upload_client_extract_json, auto_upload=True).classes('max-w-full')
                            b_client_extract_json = ui.button('EXTRACT CLIENT', on_click=cb_gen_client_extract_json).props("disable")
                            
                        with ui.column().classes("p-4 border rounded-lg"):
                            ui.label("Upload client header export json request file")
                            ui.upload(on_upload=handle_upload_client_header_json, auto_upload=True).classes('max-w-full')
                            b_gen_header_json = ui.button('EXPORT HEADER', on_click=cb_gen_client_header_json).props("disable")



def navbar():
    with ui.header().classes(replace='row items-center') as header:
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
            
    with ui.left_drawer().classes('bg-blue-100') as left_drawer:
        with ui.column().classes("w-full justify-center"):
            ui.link('Home.', home) 
            ui.link('Cloud cert.', cloud_page) 
            ui.link('Client cert.', client_page) 



@ui.page("/")
def home():
    global config

    
    navbar()

    with ui.row().classes("w-full justify-center"):
            
        with ui.column().classes("no-wrap items-center"):
            
                ui.label("Arrowhead Certificate Generation Tool").classes("p-4 border rounded-lg").style("font-size: 2rem")
                

    
    
@ui.page("/cloud")
def cloud_page():
    navbar()
    cloud_gen()
    
@ui.page("/client")
def client_page():
    navbar()
    client_gen()
            




ui.run()
