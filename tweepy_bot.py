import tweepy
import statistics as st
from decouple import config
import os

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
    def __init__(self, bot_tweepy, listener):
        self.bot_tweepy = bot_tweepy
        self.listener = listener


    def validarOpcion(self, opc):
        opciones = ["1","2","3"]
        bot = self.bot_tweepy
        if opc in opciones:
            print("Escriba la palabra con la que quiere relacionar su busqueda")
            hashtag = input()
            tweets = bot.buscar_tweets(hashtag)
            if opc == "1":
                bot.dar_like(tweets)
            elif opc == "2":
                bot.dar_retweet(tweets)
            elif opc == "3":
                bot.dar_like(tweets)
                bot.dar_retweet(tweets)
        else:
            print("Por favor ingrese una opción valida")
        return "Acción terminada"

    def iniciar(self):
        opc = self.mostrar_menu()
        while opc != "0":
            self.validarOpcion(opc)
            opc = self.mostrar_menu()

    def mostrar_menu(self):
        print("Prueba bot interactivo para Twitter")
        print("Por favor ingrese una opción valida")
        print("1: Dar fav\n2: Dar Retweet\n3: Fav y Retweet\n0: Salir")
        accion = input()
        return accion

if __name__ == '__main__':

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    bot_1 = Bot_Tweepy(auth, api)
    tweepy_listener = MyStreamListener(api)
    bot = Bot(bot_1, tweepy_listener)
    bot.iniciar()


