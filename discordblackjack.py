import random
import time
import asyncio


class BlackJack():

    def __init__(self):
        #self.msg = self.msg.split(" ")[1]
        #self.bet2 = self.msg.split(" ")[1]
        self.colors = ["Karo", "Herz", "Pik", "Kreuz"]
        self.numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Bube", "Dame", "König", "Ass"]
        self.hand = []
        self.werte = []
        self.possibilities = []
        for x in self.colors:
            for y in self.numbers:
                self.possibilities.append(f"{x} {y}")

    def shuffle_card(self):
        choice = random.choice(self.possibilities)
        choice_splitted = choice.split(" ")
        card = f"{choice_splitted[0]} {choice_splitted[1]}"
        self.hand.append(card)
        self.possibilities.remove(str(choice))
        return card

    # print(shuffle_card().split())
    def get_wert(self,card):
        if card.split()[1] == "Bube" or card.split()[1] == "Dame" or card.split()[1] == "König":
            self.werte.append(10)
            return 10
        elif card.split()[1] == "Ass":
            if sum(self.werte) + 11 > 21:
                self.werte.append(1)
                return 1
            else:
                self.werte.append(11)
                return 11

        else:
            self.werte.append(int(card.split()[1]))
            return int(card.split()[1])

    async def play_spieler(self,wert,client):
        # print(wert)
        if wert == 21:
            await self.message.channel.send(f"Du hast die Hand {self.hand} und B L A C K J A C K")
            await self.message.channel.send("Herzlichen Glückwunsch!")
            return
        elif wert > 21:
            await self.message.channel.send(f"Du hast verloren mit der Hand {self.hand} und {wert} Punkten")
            return
        else:
            await self.message.channel.send("Willst du noch eine Karte")
            def is_correct(m):
                return m.author == self.message.author

            try:
                answer = await self.client.wait_for('message', check=is_correct, timeout=10.0)
            except asyncio.TimeoutError:
                return await self.message.channel.send(f'Sorry, so lang kann ja kein Mensch warten.')

            if answer.content == "yes":
                card = blackjack.shuffle_card()
                await self.message.channel.send(str(card))
                blackjack.get_wert(card)
                await blackjack.play_spieler(sum(self.werte),client)
            else:
                await self.message.channel.send(f"du hast die Hand {self.hand} mit {wert} Punkten")
                await self.message.channel.send('Jetzt spielt die Bank, bitte bestätigen')

                def is_correct(m):
                    return m.author == self.message.author

                try:
                    answer = await self.client.wait_for('message', check=is_correct, timeout=10.0)
                except asyncio.TimeoutError:
                    return await self.message.channel.send(f'Sorry, so lang kann ja kein Mensch warten.')

                if answer.content == "yes":
                    await self.message.channel.send("Jetzt spielt die Bank")

    async def play_bank(self,wert,spielerpunktzahl):
        # print(wert)
        time.sleep(1)
        if wert > spielerpunktzahl and wert < 21:
            time.sleep(1)
            await self.message.channel.send(f"Die Bank hat {self.hand} und {wert} Punkten und somit gewonnen")
        elif wert > 21:
            time.sleep(1)
            await self.message.channel.send(f"Die Bank hat die Hand {self.hand} und {wert} Punkten - somit verloren")
        elif wert == 21:
            time.sleep(2)
            await self.message.channel.send("B L A C K J A C K - du hast leider verloren!")
            return

        else:
            await self.message.channel.send("Die Bank nimmt noch eine Karte")
            zufall = (21 - random.randint(2, 4))
            time.sleep(1)
            if wert < zufall and wert < spielerpunktzahl:
                card = blackjack.shuffle_card()
                await self.message.channel.send(str(card))
                blackjack.get_wert(card)
                await blackjack.play_bank(sum(self.werte),spielerpunktzahl)
            else:
                await self.message.channel.send(
                    f"Du hast {spielerpunktzahl} Punkte und die Bank hat die Hand {self.hand} mit {wert} Punkten und somit gewonnen")

    async def startgame(self,msg,message,client):
        self.msg = msg
        self.message = message
        self.client = client
        card = blackjack.shuffle_card()
        blackjack.get_wert(card)
        await self.message.channel.send(f"Deine erste Karte ist {card}")
        await blackjack.play_spieler(sum(self.werte),client)
        spielerpunktzahl = sum(self.werte)
        await self.message.channel.send(f"Du hast die Punktzahl {str(spielerpunktzahl)} und die die Karten {self.hand}")
        self.werte = []
        self.hand = []
        card = blackjack.shuffle_card()
        blackjack.get_wert(card)
        await self.message.channel.send(f"Die Bank zieht {card}")
        await blackjack.play_bank(sum(self.werte),spielerpunktzahl)
        self.hand = []
        self.wert = []

blackjack = BlackJack()