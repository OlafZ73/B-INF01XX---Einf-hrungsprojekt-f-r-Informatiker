### Bibliothek spiel.py
### Stand Dez 2017, Copyright Wilhelm Buechner Hochschule

import pygame, sys, time

class Einstellungen(object):
    fps = 40 # Frames pro Sekunde

    # Farben
    schwarz = (0, 0, 0)
    weiss = (255, 255, 255)
    rot = (255, 0, 0)
    
    # Dimensionen
    fensterBreite = 640
    fensterHoehe = 480
    linienDicke = 10
    abstand = 2*linienDicke
    schlaegerBreite = 10
    schlaegerHoehe = 50
    schriftGroesse = 16
    ballRadius = 5 # nur fuer runden Ball notwendig
   
    def __init__(self):
        # Notwendige Initialisierung fuer pygame
        pygame.init()
        pygame.display.set_caption('Pong')
        pygame.mouse.set_visible(0)  # setze Mauszeiger unsichtbar

    def fenster_mitte(self):
        return self.fensterHoehe // 2

    def schlaeger_mitte(self):
        return self.fenster_mitte() - self.schlaegerHoehe // 2

    def linker_rand(self):
        return self.abstand

    def rechter_rand(self):
        return self.fensterBreite - self.schlaegerBreite - self.abstand

    def schrift(self):
        return pygame.font.SysFont('arial', self.schriftGroesse, bold=True)

'''Idealer Weise waere dies kein globales Objekt'''
config = Einstellungen()


class Form(pygame.sprite.Sprite):
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=config.weiss):
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe
        self.farbe = farbe
        self.geschwindigkeit = geschwindigkeit


class Rectangle(Form):
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=config.weiss):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.rect = pygame.Rect(self.x, self.y, self.breite, self.hoehe)

    def draw(self, fensterFlaeche):
        pygame.draw.rect(fensterFlaeche, self.farbe, self.rect)


class Circle(Form):
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=config.weiss):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.rect = pygame.Rect(self.x, self.y, self.breite, self.breite)
        self.radius = self.breite/2

    def draw(self, fensterFlaeche):
        pygame.draw.circle(surface=fensterFlaeche, color=self.farbe,
                           center=(self.rect.x, self.rect.y),
                           radius=self.radius)


class Willkommen():
    # Willkommensbildschirm beim Programmstart
    def __init__(self, fensterFlaeche):
        popupFenster = pygame.Rect((config.linker_rand()+80, config.linker_rand()+60),
                (config.fensterBreite*2//3, config.fensterHoehe*1//3))
        fensterFlaeche.fill(config.weiss, popupFenster)
        textZeile1='Willkommen zu Pong'
        textZeile2='Spielstart mit beliebiger Taste'
        textWidth1 , textHeight1 = config.schrift().size(textZeile1)
        textWidth2 , textHeight2 = config.schrift().size(textZeile2)
        zeile1 = config.schrift().render(textZeile1, False, config.schwarz)
        xZeile1 = (config.fensterBreite-textWidth1)//2
        yZeile1 = (config.fensterHoehe*2//3-textHeight1)//2
        zeile2 = config.schrift().render(textZeile2, False, config.schwarz)
        xZeile2 = (config.fensterBreite-textWidth2)//2
        yZeile2 = (config.fensterHoehe-config.abstand-textHeight2)//2
        fensterFlaeche.blit(zeile1, (xZeile1, yZeile1))
        fensterFlaeche.blit(zeile2, (xZeile2, yZeile2))
        
        


class Spiel():
    # Initialisierung (OOP Konstruktor)
    def __init__(self, spielfeld, spieler, computer, ball,hindernis, punkte_anzeige):
        self.punkte = 0
        self._fpsTimer = pygame.time.Clock()

        self._spielfeld = spielfeld
        self._fensterFlaeche = pygame.display.set_mode(
            (config.fensterBreite, config.fensterHoehe))
        self._spieler = spieler
        self._computer = computer
        self._ball = ball
        self._allSchlaeger = [self._spieler, self._computer] # Liste
        self._hindernis = hindernis
        self._punkteAnzeige = punkte_anzeige
        self.hindernisactive = False    
        self.boing1_sound = pygame.mixer.Sound("Sounds/boing1.mp3")
        self.boing2_sound = pygame.mixer.Sound("Sounds/boing2.mp3")
        self.loos_sound = pygame.mixer.Sound("Sounds/loos.mp3")
        pygame.mixer.music.load("Sounds/welcome.mp3")
        
  
    def run(self):
        '''
        Spielschleife - Game Loop Pattern, siehe auch:
        http://gameprogrammingpatterns.com/game-loop.html
        '''
        running = False
        pygame.mixer.music.play(0)
        # Willkommensbildschirm anzeigen, weiter mit Taste
        while running == False:
            Willkommen(self._fensterFlaeche)
            pygame.display.update()
            # Ueberpruefe ob Taste gedrueckt wurde
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.mixer.music.stop()
                    running = True
        # Spielschleife
        while running:
            self._ereignisse_behandeln()
            self._update()
            self._zeichnen()
            pygame.display.update()
            self._fpsTimer.tick(config.fps)

    def _ereignisse_behandeln(self):
        # Ereignis abfragen
        for ereignis in pygame.event.get():
            self._behandle(ereignis)

    def _behandle(self, event):
        # Ueberpruefe ob Schliessen-Symbol im Fenster gedrueckt wurde
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            return
        # Ueberpruefe ob Maus bewegt wurde
        elif event.type == pygame.MOUSEMOTION:
            self._spieler.move(event.pos)
            return
        return event

    def _update(self):
        self._bewegen()
        self._aufprall_berechnen()

    def _bewegen(self):
        self._ball.move()
        self._computer.move(self._ball)

    def _aufprall_berechnen(self):
        if self._ball.hit_schlaeger(self._computer):
            self._ball.bounce('x')
            self.boing2_sound.play()
            

        elif self._ball.hit_schlaeger(self._spieler):
            self._ball.bounce('x')
            self.punkte += 1
            # Erhöht die Ballgeschwindigkeit +1
            self._ball.increment_velocity()
            self._ball.ball_color_change()
            self.boing1_sound.play()
            
        elif self._ball.trefferComputer():
            self.punkte += 5
   
        elif self._ball.trefferSpieler():
            self.punkte = 0
            self._ball.reset_velocity()
            self._ball.ball_color_reset()
            self.loos_sound.play()

        #elif self.hindernisactive == True and self._ball.hit_hindernis(self._hindernis):
        #    self._ball.bounce('x')
        #    self.boing2_sound.play()
  
    def _zeichnen(self):
        self._spielfeld.draw(self._fensterFlaeche)
        self._ball.draw(self._fensterFlaeche)
        for schlaeger in self._allSchlaeger:
            schlaeger.draw(self._fensterFlaeche)
        self._punkteAnzeige.draw(self.punkte, self._fensterFlaeche)
        # if self.hindernisactive == True:
        # self._hindernis.draw(self._fensterFlaeche)
        # print("Zeichnen", self.hindernisactive)


class Spielfeld(object):
    def draw(self, fensterFlaeche):
        fensterFlaeche.fill(config.schwarz)
        self._umrandung(fensterFlaeche)
        self._mittellinie(fensterFlaeche)

    def _umrandung(self, fensterFlaeche):
        pygame.draw.rect(fensterFlaeche, config.weiss,
                ((0, 0), (config.fensterBreite, config.fensterHoehe)),
                config.linienDicke*2)

    def _mittellinie(self, fensterFlaeche):
        pygame.draw.line(fensterFlaeche, config.weiss,
                 (config.fensterBreite//2, 0),
                 (config.fensterBreite//2, config.fensterHoehe),
                  config.linienDicke//4)


class Ball(Circle): # Alternativer Parameter: Circle; Rectangle
    # Pfeiltasten
    LEFT = -1
    RIGHT = 1
    UP = -1
    DOWN = 1

    # Initialisierung (OOP Konstruktor)
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.richtungX = self.LEFT
        self.richtungY = self.UP
        self.startGeschwindigkeit = geschwindigkeit
        self.startFarbe = farbe
        self.inColor = 255
        self.spiel = Spiel

    # Erhöhung der Ballgeschwindigkeit bei jedem Treffer
    def increment_velocity(self):
        self.geschwindigkeit +=1

        #if self.geschwindigkeit >= 5:
            #self.spiel.hindersnisactive = True
            #print(self.spiel.hindersnisactive)

    # Rücksetzen der Ballheschwindigkeit
    def reset_velocity(self):
        self.geschwindigkeit = self.startGeschwindigkeit

        #self.spiel.hindersnisactive = False
        #print("Trigger",self.spiel.hindersnisactive)

    # Farbänderung bei Geschwindigkeitserhöhung
    def ball_color_change(self):
        if self.inColor >= 153 + 80: self.inColor -= 40
        elif self.inColor >= 153 + 40: self.inColor -= 20
        elif self.inColor >= 153 + 20: self.inColor -= 10
        elif self.inColor > 153 + 10: self.inColor -= 1
        self.farbe = (255,255,self.inColor)

    def ball_color_reset(self):
        self.farbe = self.startFarbe
        self.inColor = 255
    
    # Funktion zum Bewegen des Balls, neue Position setzen
    def move(self):
        self.rect.x += (self.richtungX * self.geschwindigkeit)
        self.rect.y += (self.richtungY * self.geschwindigkeit)

        # Pruefe Kollision mit Wand
        if self.hit_ceiling() or self.hit_floor():
            self.bounce('y')
        if self.hit_wall():
            self.bounce('x')

    # Richtungsaenderung fuer Ball
    def bounce(self, axis):
        if axis == 'x':
            self.richtungX *= -1
        elif axis == 'y':
            self.richtungY *= -1
        
    # Treffen von Ball auf Schlaeger
    def hit_schlaeger(self, schlaeger):
        return pygame.sprite.collide_rect(self, schlaeger)

    # Treffen von Ball auf Hindernis
    def hit_hindernis(self, hindernis):
        return pygame.sprite.collide_rect(self, hindernis)


    
    # Treffen von Ball auf Wand links oder rechts
    def hit_wall(self):
        return (
            (self.richtungX == -1
                and self.rect.left <= config.linienDicke*2) or
            (self.richtungX ==  1
                and self.rect.right >= config.fensterBreite - config.linienDicke)
        )

 
    # Treffen von Ball auf Decke
    def hit_ceiling(self):
        return self.richtungY == -1 and self.rect.top <= config.linienDicke*2

    # Treffen von Ball auf Boden
    def hit_floor(self):
        return (self.richtungY == 1
                and self.rect.bottom >= config.fensterHoehe - config.linienDicke)

    def trefferSpieler(self):
        return self.rect.left <= config.linienDicke*2

    def trefferComputer(self):
        return self.rect.right >= config.fensterBreite - config.linienDicke*2


class Schlaeger(Rectangle):
    # Funktion zum Zeichnen des Schlaegers
    def draw(self, fensterFlaeche):
        # Stoppt Schlaeger am unteren Spielfeldrand
        if self.rect.bottom > config.fensterHoehe - config.linienDicke:
            self.rect.bottom = config.fensterHoehe - config.linienDicke
        # Stoppt Schlaeger am oberen Spielfeldrand
        elif self.rect.top < config.linienDicke:
            self.rect.top = config.linienDicke+1 # randkorrektur

        super().draw(fensterFlaeche)

    # Funktion zum Bewegen des Schlaegers mit Maus
    def move(self, pos):
        self.rect.y = pos[1]


class AutoSchlaeger(Schlaeger):
    # Initialisierung (OOP Konstruktor)
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, ball, farbe=config.weiss):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self._ball = ball

    # Automatische Bewegung, richtet sich nach dem Ball
    def move(self, pos):
        # Wenn Ball sich vom Schlaeger wegbewegt, zentriere ihn
        if self._ball.richtungX == -1:
            self._zentrieren()
        # Wenn Ball sich auf Schlaeger zubewegt, beoachte seine Bewegung
        elif self._ball.richtungX == 1:
            self._beobachten()

    def _beobachten(self):
        if self.rect.centery < self._ball.rect.centery:
            self.rect.y += self.geschwindigkeit
        else:
            self.rect.y -= self.geschwindigkeit

    def _zentrieren(self):
        if self.rect.centery < config.fenster_mitte():
            self.rect.y += self.geschwindigkeit
        elif self.rect.centery > config.fenster_mitte():
            self.rect.y -= self.geschwindigkeit

# neue Idee für eine Erweiterung
class Hindernis(Rectangle):
    # Funktion zum Zeichnen des Schlaegers
    def draw(self, fensterFlaeche):
       super().draw(fensterFlaeche)


class PunkteAnzeige():
    # Initialisierung (OOP Konstruktor)
    def __init__(self, punkte, x, y, schrift):
        self.punkte = punkte
        self.x = x
        self.y = y
        self.schrift = schrift

    # Schreibe aktuellen Punktestand an den Bildschirm
    def draw(self, punkte, fensterFlaeche):
        self.punkte = punkte
        result_surf = self.schrift.render('Punkte: %s' %(self.punkte), True, config.weiss)
        rect = result_surf.get_rect()
        rect.topleft = (self.x, self.y)
        fensterFlaeche.blit(result_surf, rect)

class TastaturSchlaeger(Schlaeger):
    # Funktion zum Bewegen des Schlaegers mit Tastatur
    def movekey(self,pos):
        #print(self.rect.y, pos) # nur fuer debugging
        self.rect.y = self.rect.y+pos

class SpielErweitert(Spiel):
  # Erweiterung des Spiels um Tastatureingaben
  # und Tastatursteuerung des Schlaegers
  def _behandle (self, event):
    # Maus soll auch weiterhin funktionieren
    event = super()._behandle(event)

    # Wenn nichts zurueckkommt, wurde das event behandelt
    if not event:
      return
    # Ueberpruefe ob Taste gedrueckt wurde
    if event.type == pygame.KEYDOWN:
      self._reagiere_auf_tastatur(event)

  def _reagiere_auf_tastatur(self, event):
    # Bewegung um 20 Pixel pro Pfeiltaste
    if event.key == pygame.K_w:
      self._spieler.movekey(-40)
    elif event.key == pygame.K_s:
      self._spieler.movekey(+40)
    elif event.key == pygame.K_UP:
      self._spieler.movekey(-20)
    elif event.key == pygame.K_DOWN:
      self._spieler.movekey(+20)#
    # Druecken von Escape beendet Spiel
    elif event.key == pygame.K_ESCAPE :
      pygame.event.post(pygame.event.Event(pygame.QUIT))
    elif event.key == pygame.K_b:
        self._Spiel.boing_sound()
        
