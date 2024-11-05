# main.py
from user_manager import register_user, login_user
from chat_manager import start_chat_session

def main():
    print("Bienvenue sur Texter1 !")
    while True:
        choix = input("1: Inscription, 2: Connexion, 3: Quitter\nChoisissez une option: ")
        if choix == '1':
            register_user()
        elif choix == '2':
            user = login_user()
            if user:
                start_chat_session(user)
        elif choix == '3':
            print("À bientôt sur Texter1 !")
            break

if __name__ == "__main__":
    main()