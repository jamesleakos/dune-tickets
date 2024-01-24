import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def check_availability():
    url = "https://www.amctheatres.com/showtimes/all/2024-02-29/amc-metreon-16/all"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    dune_container = soup.find('h2', string='Dune: Part Two').find_parent('div', class_='ShowtimesByTheatre-film')

    if dune_container:
        imax_container = dune_container.find('h3', string='IMAX 70MM').find_parent('div', class_='Showtimes-Section')

        if imax_container:
            movie_status_element = imax_container.find('div', class_='ShowtimeButtons-status Headline--eyebrow--alt txt--uppercase txt--bold')

            if movie_status_element is not None:
                movie_status = movie_status_element.text.strip()

                if 'Available Soon' in movie_status:
                    print("Dune 2 IMAX 70MM tickets are not available yet - time: " + time.strftime("%H:%M:%S"))
                    return False
                else:
                    print("DUNE 2 IMAX 70MM TICKETS ARE AVAILABLE NOW!!!!!")
                    return True
            else:
                print("Dune 2 IMAX 70MM status is not found on the page.")
                return True
        else:
            print("Dune 2 IMAX 70MM is not listed on the page.")
            return True
    else:
        print("Dune 2 is not listed on the page.")
        return True
    
def send_text(message):
    
    to = os.getenv('PHONE_NUMBER') + '@vtext.com'

    msg = MIMEMultipart()
    msg['From'] = os.getenv('EMAIL_ADDRESS') 
    msg['To'] = to
    msg['Subject'] = message
    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(msg['From'], os.getenv('EMAIL_PASSWORD')) 
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

while True:
    if check_availability():
        send_text("Dune 2 tickets are available now.")
        break
    time.sleep(9) 

# check_availability()