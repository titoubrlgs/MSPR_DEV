import json
import os
import nmap
import requests
import time
import socket
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

version="1.1"

class SemaOS(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(f'SemaOS - version {version}')
        self.setWindowIcon(QIcon('./semaphorelogo.ico'))

        # Boutons
        self.scan_button = QPushButton("Scanner le réseau")
        self.speed_test_button = QPushButton("Tester le débit")
        self.export_conf_button = QPushButton("Exporter configuration")

        # Labels
        self.vm_ip_label = QLabel("Adresses IP / Nom de l'hôte :")
        self.vm_ip_data = QLabel()
        self.internet_ip_label = QLabel("IP publique / nom DNS dynamique :")
        self.internet_ip_data = QLabel()
        self.internet_status_label = QLabel("Etat de la connexion Internet :")
        self.internet_status_data = QLabel()
        self.network_devices_label = QLabel("Liste des machines détectées sur le réseau :")
        self.network_devices_table = QTableWidget()
        self.network_devices_table.setColumnCount(3)
        self.network_devices_table.setHorizontalHeaderLabels(["IP", "Nom", "Ports ouverts"])

        self.speed_test_result_label = QLabel("Résultats du dernier test de débit :")
        self.speed_test_result_data = QLabel()

        # Layouts
        self.main_layout = QVBoxLayout()

        self.vm_ip_layout = QHBoxLayout()
        self.vm_ip_layout.addWidget(self.vm_ip_label)
        self.vm_ip_layout.addWidget(self.vm_ip_data)

        self.internet_ip_layout = QHBoxLayout()
        self.internet_ip_layout.addWidget(self.internet_ip_label)
        self.internet_ip_layout.addWidget(self.internet_ip_data)

        self.internet_status_layout = QHBoxLayout()
        self.internet_status_layout.addWidget(self.internet_status_label)
        self.internet_status_layout.addWidget(self.internet_status_data)

        self.network_devices_layout = QVBoxLayout()
        self.network_devices_layout.addWidget(self.network_devices_label)
        self.network_devices_layout.addWidget(self.network_devices_table)

        self.speed_test_result_layout = QHBoxLayout()
        self.speed_test_result_layout.addWidget(self.speed_test_result_label)
        self.speed_test_result_layout.addWidget(self.speed_test_result_data)

        self.main_layout.addWidget(self.scan_button)
        self.main_layout.addWidget(self.export_conf_button)
        self.main_layout.addWidget(self.speed_test_button)
        self.main_layout.addLayout(self.vm_ip_layout)
        self.main_layout.addLayout(self.internet_ip_layout)
        self.main_layout.addLayout(self.internet_status_layout)
        self.main_layout.addLayout(self.network_devices_layout)
        self.main_layout.addLayout(self.speed_test_result_layout)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        self.export_conf_button.clicked.connect(self.exportjson)
        self.scan_button.clicked.connect(self.scan_network)
        self.speed_test_button.clicked.connect(self.speed_test)

        # Initialisation des valeurs des labels
        self.vm_ip_data.setText(socket.gethostname())
        self.internet_status_data.setText("Connexion en cours...")

        # Paramètres de test de débit
        self.test_interval = 60 # Interval de test en secondes
        self.speed_test_url = "https://example.com/speedtest" # URL du script de test de débit

        # Démarrage de la boucle de test de débit
        self.speed_test()

    def scan_network(self):
        nm = nmap.PortScanner()
        nm.scan(hosts='192.168.0.0/24', arguments='-sT')
        devices = nm.all_hosts()
        self.network_devices_table.setRowCount(len(devices))
        for i, device in enumerate(devices):
            name = socket.getfqdn(device)
            
            
            #Tentative de scan de port en listant les protocoles
            for proto in nm[device].all_protocols():
                lopenports=[]
                #la ligne du dessus me retourne des arrays vides
                lport = nm[device][proto].keys()
                for port in lport:
                    if(nm[device][proto][port]['state'] == "open" and port!=0):
                        lopenports.append(str(port))
            stringedlopenports= ', '.join(lopenports)
                     #   print(True)
            #On met les résultats quand PyQt
            
            self.network_devices_table.setItem(i, 0, QTableWidgetItem(device))
            self.network_devices_table.setItem(i, 1, QTableWidgetItem(name))
            self.network_devices_table.setItem(i, 2, QTableWidgetItem(stringedlopenports))

            return device
            
            
    def speed_test(self):
        try:
            # Test de ping
            response = requests.get("https://api.ipify.org")
            ip_address = response.text

            # Test de débit
            speed_test_result = requests.get(self.speed_test_url).text

            # Mise à jour des labels
            self.internet_ip_data.setText(ip_address)
            self.speed_test_result_data.setText(speed_test_result)
            self.internet_status_data.setText("Connexion établie")
        except:
            self.internet_status_data.setText("Connexion échouée")

        # Planification du prochain test de débit
        QTimer.singleShot(self.test_interval*1000, self.speed_test)

        return ip_address

    def exportjson(self):
        with open('data.json') as json_file:
            json_data = json.load(json_file)
            json_data['SemaOS']['Version']=version
            json_data['SemaOS']['Semabox']['PublicIP']=self.speed_test()
            json_data['SemaOS']['Scanoutput']['Hosts']['IP']=self.scan_network()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    semaos = SemaOS()
    semaos.show()
    sys.exit(app.exec_())
