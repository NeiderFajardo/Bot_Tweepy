import tweepy
import statistics as st
from decouple import config
import os
import time

consumer_key = config('consumer_key')
consumer_secret = config('consumer_secret')
access_token = config('access_token')
access_token_secret = config('access_token_secret')

class Bot_Tweepy:

    def __init__(self, auth, api):
        self.auth = auth
        self.api = api

    def verificar_credenciales(self):
        api = self.api
        try:
            api.verify_credentials()
            return "Credenciales correctas"
        except:
            return "Las credenciales no se han validado correctamente"


    def buscar_tweets(self, hashtag):
        api = self.api
        tweets = api.search(hashtag, count=20)
        tweets_json = []
        for t in tweets:
            if t._json['entities']['hashtags'] != []:
                tweets_json.append(t)
        return tweets_json

    def dar_like(self, tweets):
        for t in tweets:
            if not t.favorited:
                try:
                    t.favorite()
                except Exception as e:
                    print("Error al dar favorito")

    def dar_retweet(self, tweets):
        for t in tweets:
            if not t.retweeted:
                try:
                    t.retweet()
                except Exception as e:
                    print("Error al dar retweet")

    def actualizar_descripcion(self, desc):
        if len(desc) <= 160:
            api = self.api
            try:
                api.update_profile(description=desc)
                print("Perfil actualizado exitosamente")
            except:
                print("No se pudo actualizar el perfil")
        else:
            print("Número de caracteres excedido")


    def seguir_seguidores(self):
        api = self.api
        for follower in tweepy.Cursor(api.followers).items():
            if not follower.following:
                print("Siguiendo al usuario ",follower.name)
                follower.follow()


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        super().__init__(api)
        self.api = api
        self.me = api.me()

        def on_status(self, tweet):
            print(f"{tweet.user.name}:{tweet.text}")

        def on_error(self, status):
            print("Error detected")

class Bot:
    def __init__(self, bot_tweepy):
        self.bot_tweepy = bot_tweepy
        #self.listener = listener


    def validarOpcion(self, opc):
        opciones_tweet = ["1","2","3"]
        opciones_perfil = ["4", "5"]
        bot = self.bot_tweepy
        tweets = []
        if opc in opciones_tweet:
            print("Escriba las palabras con la que quiere relacionar su busqueda separadas por un coma(,)")
            hashtag = input().split()
            print("¿Cuantas veces quiere realizar el proceso?\nIngrese el número de repeticiones:")
            repetir = int(input())
            print("Iniciando...\nCtrl+C Para cancelar")
            for i in range(repetir):
                for t in hashtag:
                    t = bot.buscar_tweets(hashtag)
                    tweets.extend(t)
                if opc == "1":
                    bot.dar_like(tweets)
                elif opc == "2":
                    bot.dar_retweet(tweets)
                elif opc == "3":
                    bot.dar_like(tweets)
                    bot.dar_retweet(tweets)
                time.sleep(5)
        elif opc in opciones_perfil:
            if opc == "4":
                print("Escriba la descripción:")
                desc = input()
                bot.actualizar_descripcion(desc)
            elif opc == "5":
                bot.seguir_seguidores()
        else:
            print("Por favor ingrese una opción valida")
        return "Acción terminada"

    def iniciar(self):
        opc = self.mostrar_menu()
        while opc != "0":
            self.validarOpcion(opc)
            opc = self.mostrar_menu()

    def mostrar_menu(self):
        texto_menu = "1: Dar fav\n2: Dar Retweet\n3: Fav y Retweet\n4: Acualizar Perfil\n"
        texto_menu += "5: Seguir seguidores"
        print("Prueba bot interactivo para Twitter")
        print("Por favor ingrese una opción valida")
        print(texto_menu)
        print("0: Salir")
        accion = input()
        return accion

if __name__ == '__main__':

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    bot_1 = Bot_Tweepy(auth, api)
    print(bot_1.verificar_credenciales())
    #tweepy_listener = MyStreamListener(api)
    bot = Bot(bot_1)
    bot.iniciar()


