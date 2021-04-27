import discord
import random
import time
import discordblackjack as dbj
import asyncio

class MyClient(discord.Client):
    # Einloggen Methode
    async def on_ready(self):
        print("Quak. ich habe mich eingeloggt")

    # Wenn Nachricht gepostet wird

    async def on_message(self, message):
        if message.author == client.user:
            return
        hello = ["hi", "hello", "hoi", "hey", "servus", "mahlzeit"]
        gast = str(message.author).split("#")
        if message.content in hello:
            await message.channel.send(f"{random.choice(hello)} {gast[0]}, alles klar?!" )
        if message.content == "$help":
            chances = 1/36*100
            await message.channel.send("GAMES \n\n"
                                       "To play Roulette type $roulette BID BET \n"
                                       "For example: $roulette black 200 \n"
                                       "Possibilities: A number between 0 and 36, red or black \n"
                                       f"Chances:\n Number = {chances}% \n Black = 50% \n Red = 50% "
                                       "\n\n\n"
                                       "To play Blackjack type $blackjack \n"
                                       "For example: $blackjack"
                                       )
        if message.content.startswith("$roulette"):
            try:
                bid = message.content.split(" ")[1]
            except IndexError:
                await message.channel.send("Missing Bid")
                return
            try:
                bet = message.content.split(" ")[2]
            except IndexError:
                await message.channel.send("Missing Bet")
                return
            #bet = message.content.split(" ")[2]
            bid_param = -3
            if bid.lower() == "black":
                bid_param = -1
            elif bid.lower() == "red":
                bid_param = -2
            else:
                try:
                    bid_param = int(bid)
                except:
                    bid_param = -3
            if bid_param == -3:
                await message.channel.send("Eingabe ungültig")
                return

            black = [15,4,2,17,6,13,11,8,10,24,33,20,31,22,29,28,35,26]
            red = [32,19,21,25,34,27,36,30,23,5,16,1,14,9,18,7,12,3]
            result = random.randint(0,36)
            if bid_param == -1:
                won = result in black
                money = int(bet) * 2
            elif bid_param == -2:
                won = result in red
                money = int(bet) * 2
            else:
                won = result == bid_param
                money = bet * 5
            if won:
                await message.channel.send(f"Die Kugel rollt!")
                time.sleep(1)
                await message.channel.send(f"...und rollt")
                time.sleep(1)
                await message.channel.send(f"..rollt um die Ecke")
                time.sleep(1)
                await message.channel.send(f"und stoppt!")
                time.sleep(1)

                if result in black:
                    await message.channel.send(f"Gewonnen! Tipp war {bid} und das Feld ist die schwarze {result} \n"
                                               f"und du hast {money}$ gewonnen")
                if result in red:
                    await message.channel.send(f"Gewonnen! Tipp war {bid} und das Feld ist die rote {result} ")
            else:
                await message.channel.send(f"Die Kugel rollt!")
                time.sleep(1)
                await message.channel.send(f"...und rollt")
                time.sleep(1)
                await message.channel.send(f"..rollt um die Ecke")
                time.sleep(1)
                await message.channel.send(f"und stoppt!")
                time.sleep(1)
                if result in black:
                    await message.channel.send(f"Leider verloren! Tipp war {bid} und das Feld ist die schwarze {result} ")
                if result in red:
                    await message.channel.send(f"Leider verloren! Tipp war {bid} und das Feld ist die rote {result} ")

            if message.content.startswith("$blackjack"):
                try:
                    bet2 = message.content.split(" ")[1]
                except IndexError:
                    await message.channel.send("Missing Bid")
                    return

                bet2 = message.content.split(" ")[1]
                colors = ["Karo", "Herz", "Pik", "Kreuz"]
                numbers = [7,8,9,10,"Bube","Dame","König","Ass"]

                color = random.choice(colors)
                number = random.choice(numbers)
                if number == "Bube" or "Dame" or "König":
                    wert = 10
                elif number == "Ass":
                    wert = 11
                else:
                    wert = int(number)

                card = f"{color} {number}"

        if message.content.startswith("$blackjack"):
            await dbj.blackjack.startgame(message.content,message, client)

        if message.content.startswith('$frage'):
            await message.channel.send('Hast du eine Frage?')

            def is_correct(m):
                return m.author == message.author

            try:
                answer = await client.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, so lang kann ja kein Mensch warten.')

            if answer.content == "yes":
                await message.channel.send('Okay, dann frage mal')
            else:
                await message.channel.send(f'okay, dann halt net')


client = MyClient()
client.run("ODM0ODY0MzAzNTYyNTU1NDcy.YIHF-A.0GtjcBWPzCgaoGrov86w0kXM6sc")


