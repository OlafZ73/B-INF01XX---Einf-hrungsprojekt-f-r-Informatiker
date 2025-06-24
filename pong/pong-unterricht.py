### Spiel Pong programmiert mit Python und Bibliotheken pygame und spiel
### Stand Dez 2017, Copyright Wilhelm Buechner Hochschule

from spiel import *

# das Hauptprogramm, Einstiegspunkt fuer den Aufruf vom Betriebssystem
def main():

    '''Konkrete Instanzen hier deklarieren'''

    ## hier Objekt ball von Klasse Ball anlegen
    ## und mit Parametern (x, y, breite, hoehe, geschwindigkeit) initialisieren
    ball = Ball(
        x=config.fenster_mitte(),
        y=config.fensterBreite // 2,
        breite=10,
        hoehe=10,
        geschwindigkeit=5,
        farbe=config.rot
        )
    
        

    ## hier Objekt spieler von Klasse Schlaeger anlegen
    ## und mit Parametern (x, y, breite, hoehe, geschwindigkeit) initialisieren
    spieler = TastaturSchlaeger(
        x=config.linker_rand(),
        y=config.schlaeger_mitte(),
        breite=config.schlaegerBreite,
        hoehe=config.schlaegerHoehe,
        geschwindigkeit=5,
        farbe=config.weiss,
        )


    ## hier Objekt für ein Hindernis erstellen
    ## und mit Parametern (x, y, breite, hoehe, geschwindigkeit) initialisieren
    hindernis = Hindernis(
        x=config.rechter_rand()/2,
        y=config.schlaeger_mitte(),
        breite=20,
        hoehe=100,
        geschwindigkeit=5,
        farbe=config.weiss,
        )


   
    
    ## hier Objekt spielfeld von Klasse Spielfeld anlegen (keine Parameter)
            
    spielfeld = Spielfeld()
    
    ## Objekt computer von Klasse AutoSchlaeger ist schon angelegt
    ## und mit Parametern (x, y, breite, hoehe, geschwindigkeit, farbe) initialisiert
    ## Objekt ball wird uebergeben, damit Computer Schlaeger dem Ball folgen kann
    computer = AutoSchlaeger(
        x=config.rechter_rand(),
        y=config.schlaeger_mitte(),
        breite=config.schlaegerBreite,
        hoehe=config.schlaegerHoehe,
        geschwindigkeit=5,
        farbe=config.weiss,
        ball=ball
    )

    ## Objekt punkte_anzeige von Klasse PunkteAnzeige ist schon angelegt
    ## und mit Parametern (punkte, x, y, schrift) initialisiert
    punkte_anzeige = PunkteAnzeige(
        punkte=0,   
        x=config.fensterBreite - 150,
        y=25,
        schrift=config.schrift()
    )
    
    ## Aufruf des Konstruktors und dann der Methode run der Klasse Spiel
    SpielErweitert(spielfeld, spieler, computer, ball, hindernis, punkte_anzeige).run()

# Aufruf der Main-Funktion
if __name__=='__main__':
    main()
