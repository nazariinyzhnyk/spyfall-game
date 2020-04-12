import json
import smtplib
import random


def get_locations(filename='locations.json'):
    with open(filename, 'r') as f:
        locations = json.load(f)
    return [loc['title'] for loc in locations['locations']]


def get_player_mails(filename='player_mails.txt'):
    with open(filename, 'r') as f:
        mails = f.readlines()
    return [mail.replace('\n', '') for mail in mails]


def get_gmail_creds(filename='credentials.json'):
    with open(filename, 'r') as f:
        creds = json.load(f)
    return creds['email'], creds['pass']


def send_mails(user, password, mails, locations, sep='\n\t'):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user, password)

        game_location = random.choice(locations)
        spy_mail = random.choice(mails)
        mails.remove(spy_mail)

        message = 'Subject: {}\n\n{}'.format('Spyfall game role',
                                             f'Location: {game_location}. \n\nLocations:\n\t{sep.join(locations)}')
        server.sendmail(user, mails, message)

        message = 'Subject: {}\n\n{}'.format('Spyfall game role',
                                             f'Location: Spy. \n\nLocations:\n\t{sep.join(locations)}')
        server.sendmail(user, spy_mail, message)

        server.close()

    except:
        print('Something went wrong with mail server.')


if __name__ == '__main__':
    locations = get_locations()
    mails = get_player_mails()
    print('Mails in game: {}'.format(mails))
    server_mail, server_pass = get_gmail_creds()

    send_mails(server_mail, server_pass, mails, locations)
