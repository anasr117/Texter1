# client.py
import requests

BASE_URL = " http://127.0.0.1:5000"

def register():
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    response = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password})

    # Afficher le code de statut et le texte brut pour le débogage
    print("Statut de la réponse :", response.status_code)
    print("Contenu brut de la réponse :", response.text)

    try:
        print(response.json()["message"])
    except requests.exceptions.JSONDecodeError:
        print("Erreur : La réponse du serveur n'est pas en JSON.")

def login():
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        print("Connexion réussie !")
        return username
    else:
        print("Échec de la connexion.")
        return None
    
def send_message(user):
    recipient = input("Envoyer à : ")
    message = input("Message : ")
    response = requests.post("http://127.0.0.1:5000/send_message", json={
        "username": user,
        "recipient": recipient,
        "message": message
    })
    print("Statut de la réponse :", response.status_code)  # Affiche le code de statut HTTP
    print("Contenu brut de la réponse :", response.text)  # Affiche le contenu brut de la réponse

    try:
        print(response.json()["message"])
    except requests.exceptions.JSONDecodeError:
        print("Erreur : La réponse du serveur n'est pas en JSON.")


def get_messages(user):
    response = requests.get(f"{BASE_URL}/get_messages", params={"user": user})
    messages = response.json()
    for msg in messages:
        print(f"{msg['sender']}: {msg['message']}")

def main():
    print("Bienvenue sur Texter1 !")
    user = None
    while True:
        if not user:
            choice = input("1: Inscription, 2: Connexion, 3: Quitter\nChoisissez une option : ")
            if choice == '1':
                register()
            elif choice == '2':
                user = login()
            elif choice == '3':
                break
        else:
            action = input("1: Envoyer message, 2: Voir messages, 3: Déconnexion\nChoisissez une action : ")
            if action == '1':
                send_message(user)
            elif action == '2':
                get_messages(user)
            elif action == '3':
                user = None

if __name__ == "__main__":
    main()
