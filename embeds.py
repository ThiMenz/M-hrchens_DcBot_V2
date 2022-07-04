import discord
from datetime import datetime
import calendar
import time

help_embed_1 = discord.Embed(
  title = 'General Commands',
  description = 'Diese Commands sind allgemeinnützig und unabhängig von dem Musikbot. Wie man seinen Voicechannel anpasst erfährst du in dem Raumverwaltungschat.',
  colour = discord.Colour.blue()
)
help_embed_1.add_field(name='m!wys [Kategorie] [Schwierigkeitsstufe] [X]', value='✧ Zeigt dir die aktuellen Top [X] Runs von in der entsprechenen Kategorie auf der entsprechenen Schwierigkeitsstufe an.', inline=False)
help_embed_1.add_field(name='m!wys [Kategorie] [Schwierigkeitsstufe] [X-Y]', value='✧ Zeigt dir die aktuellen Runs von den Plätzen [X] bis [Y] in der entsprechenen Kategorie auf der entsprechenen Schwierigkeitsstufe an.', inline=False)






help_embed_2 = discord.Embed(
  title = 'Musik Commands',
  description = 'Diese Commands sind für das Starten und Steuern der Musik zuständig. Beachtet hierbei bitte, dass der Bot nicht in mehreren Channels gleichzeitig sein kann.',
  colour = discord.Colour.blue()
)
help_embed_2.add_field(name='m!play [Name / Link] / m!p [Name / Link]', value='✧ Spielt in deinem aktuellen Voicechannel die angegebene Musik ab. Falls schon etwas abgespielt wird, wird die Musik zur Queue hinzugefügt.', inline=False)
help_embed_2.add_field(name='m!skip / m!s', value='✧ Überspringt die Musik, die gerade in deinem Voicechannel läuft.', inline=False)
help_embed_2.add_field(name='m!pause / m!pa', value='✧ Pausiert die aktuelle Musik.', inline=False)
help_embed_2.add_field(name='m!resume / m!r', value='✧ Falls die Musik pausiert sein sollte, wird sie mit diesem Command wieder gestartet.', inline=False)
help_embed_2.add_field(name='m!volume [0-100] / m!v [0-100]', value='✧ Setzt die Lautstärke auf den angegebenen Prozentwert.', inline=False)
help_embed_2.add_field(name='m!replay / m!rep', value='✧ Lässt die aktuelle Musik von neu abspielen.', inline=False)
help_embed_2.add_field(name='m!loop / m!lo', value='✧ Erstellt eine Endlosschleife der aktuellen Musik.', inline=False)
help_embed_2.add_field(name='m!now / m!n', value='✧ Zeigt genauere Informationen zu der aktuellen Musik.', inline=False)
help_embed_2.add_field(name='m!queue / m!q', value='✧ Zeigt alle Musiktitel der aktuellen Queue.', inline=False)
help_embed_2.add_field(name='m!remove [Zahl] / m!re [Zahl]', value='✧ Löscht den angegebenen Musiktitel aus der aktuellen Queue.', inline=False)
help_embed_2.add_field(name='m!clear / m!c', value='✧ Löscht alle Musiktitel aus der aktuellen Queue.', inline=False)
help_embed_2.add_field(name='m!shuffle / m!sh', value='✧ Verändert mit einem Zufallsgenerator die Reihenfolge der aktuellen Queue.', inline=False)
help_embed_2.add_field(name='m!join/ m!j', value='✧ Lässt den Musik Bot zu eurem Voicechannel beitreten.', inline=False)
help_embed_2.add_field(name='m!leave / m!l', value='✧ Entfernt den Musik Bot aus eurem Voicechannel.', inline=False)
#help_embed_2.add_field(name='m!stop / m!st', value='✧ Stoppt den Musikbot.', inline=False)