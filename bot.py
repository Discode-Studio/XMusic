import logging
import os
import traceback
from flask import Flask, request, redirect
import discord
from discord.ext import commands
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'user-read-playback-state user-modify-playback-state'

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    logging.error("Spotify client ID and secret must be set as environment variables.")
    raise ValueError("Spotify client ID and secret must be set as environment variables.")

sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                        client_secret=SPOTIFY_CLIENT_SECRET,
                        redirect_uri=SPOTIFY_REDIRECT_URI,
                        scope=SCOPE)

sp = None

intents = discord.Intents.default()
intents.message_content = True  # Ajoutez cette ligne pour activer l'intent des messages

bot = commands.Bot(command_prefix='!', intents=intents)

@app.route('/')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    global sp
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    sp = Spotify(auth=token_info['access_token'])
    return "You can now close this window."

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name}')

@bot.command()
async def play(ctx, track_uri):
    if sp:
        sp.start_playback(uris=[track_uri])
        await ctx.send(f'Playing track: {track_uri}')
    else:
        await ctx.send('Please log in to Spotify first.')

@bot.command()
async def pause(ctx):
    if sp:
        sp.pause_playback()
        await ctx.send('Playback paused')
    else:
        await ctx.send('Please log in to Spotify first.')

@bot.command()
async def resume(ctx):
    if sp:
        sp.start_playback()
        await ctx.send('Playback resumed')
    else:
        await ctx.send('Please log in to Spotify first.')

if __name__ == '__main__':
    try:
        bot.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        logging.error("An error occurred:")
        logging.error(traceback.format_exc())
