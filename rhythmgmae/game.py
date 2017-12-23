# coding=utf-8
import sys
import os
import pygame

class Note:
    black = (0, 0, 0)
    white = (255, 255, 255)

    startTime = 0
    endTime = 0
    height = 0
    note_speed = 0
    notewidth = 0
    noteheight = 0
    note_count = 0
    note_name = ""
    notes = []
    note = []
    notes_ongame = []
    effects = []
    judge_effects = []
    i = 0

    good = 0
    great = 0
    perfect = 0
    score = 0
    combo = 0
    maxcombo = 0

    judgebar_y = 0
    judgebar_height = 0
    speed = 2
    musicfolder = ""
    musicname = ""
    musicsource = ""
    flag = True
    startflag = True

    def __init__(self, notefolder, notename, musicfolder, musicname, Width, Height):
        self.note_name = notename
        self.musicfolder = musicfolder
        self.musicsource = musicname
        self.musicname = musicname.split('.')[0]
        self.height = Height
        self.notewidth = (Width - 200) / 4
        self.noteheight = Height / 20
        self.judgebar_y = Height - self.noteheight
        self.note_speed = 30
        self.judgebar_height = Height / 64
        f = file(notefolder + notename)
        line = f.readline()
        while line:
            line = line.replace("\n", "")
            result = line.split(" ")
            num1 = int(result[0])
            num2 = int(result[1])
            self.note.append([num1, num2])
            line = f.readline()
            self.note_count += 1
            if not line:
                break
        f.close()
        self.perfect = 1000000 / self.note_count
        self.great = self.perfect * 0.7
        self.good = self.perfect * 0.5

        for node in self.note:
            x = (node[0] - 1) * self.notewidth
            y = 0
            onenote = [x, y, node[0], self.noteheight, node[1]]
            self.notes.append(onenote)

    def Notes_timecheck(self):
        if self.startflag:
            self.Music_play()
            self.startTime = pygame.time.get_ticks()
            self.startflag = False

        while self.flag and self.notes[self.i][4] - (330 * self.speed) < pygame.time.get_ticks() - self.startTime:
            self.notes_ongame.append(self.notes[self.i])
            self.i += 1
            if self.i == self.note_count:
                self.flag = False
                self.endTime = pygame.time.get_ticks()

    def Notes_draw(self, screen):
        for note in self.notes_ongame:
            note[1] += self.note_speed
            pygame.draw.rect(screen, self.white, (note[0], note[1], self.notewidth, note[3]))
            if note[1] >= self.judgebar_y + self.noteheight:
                self.notes_ongame.remove(note)
                if self.maxcombo < self.combo:
                    self.maxcombo = self.combo
                self.combo = 0
                self.Judge_add(4)

    def Effects_add(self, screen, x):
        alphascreen = screen.convert_alpha()
        alphascreen.fill((0, 0, 0, 0))
        pygame.draw.rect(alphascreen, (255, 255, 255, 200), ((x - 1) * self.notewidth, self.judgebar_y - 100, self.notewidth, 100))
        time = pygame.time.get_ticks()
        effect = [alphascreen, time]
        self.effects.append(effect)

    def Effects_draw(self, screen):
        for x in self.effects:
            screen.blit(x[0], (0, 0))
            if pygame.time.get_ticks() - x[1] >= 100:
                self.effects.remove(x)

    def Judge_add(self, x):
        global Text, TextRect
        Font = pygame.font.Font(None, 40)
        if x == 1:
            Text = Font.render("Perfect", True, self.white)
            TextRect = Text.get_rect()
            TextRect.center = (((self.notewidth * 4) / 2), (self.judgebar_y / 2))
        elif x == 2:
            Text = Font.render("Great", True, self.white)
            TextRect = Text.get_rect()
            TextRect.center = (((self.notewidth * 4) / 2), (self.judgebar_y / 2))
        elif x == 3:
            Text = Font.render("Good", True, self.white)
            TextRect = Text.get_rect()
            TextRect.center = (((self.notewidth * 4) / 2), (self.judgebar_y / 2))
        elif x == 4:
            Text = Font.render("Miss", True, self.white)
            TextRect = Text.get_rect()
            TextRect.center = (((self.notewidth * 4) / 2), (self.judgebar_y / 2))

        self.judge_effects = [Text, TextRect]

    def Judge_draw(self, screen):
        if len(self.judge_effects) != 0:
            screen.blit(self.judge_effects[0], self.judge_effects[1])

    def Note_hit(self, screen, x):
        self.Effects_draw(screen)
        for note in self.notes_ongame:
            if x == note[2]:
                time_click = pygame.time.get_ticks() - self.startTime - note[4]
                if 50 >= time_click >= -50:
                    self.score += self.perfect
                    self.notes_ongame.remove(note)
                    self.combo += 1
                    self.Judge_add(1)
                elif 70 >= time_click >= -70:
                    self.score += self.great
                    self.notes_ongame.remove(note)
                    self.combo += 1
                    self.Judge_add(2)
                elif 90 >= time_click >= -90:
                    self.score += self.good
                    self.notes_ongame.remove(note)
                    self.combo += 1
                    self.Judge_add(3)
                elif 160 >= time_click >= -160:
                    self.notes_ongame.remove(note)
                    if self.maxcombo < self.combo:
                        self.maxcombo = self.combo
                    self.combo = 0
                    self.Judge_add(4)

    def JudgeBar_draw(self, screen):
        pygame.draw.rect(screen, self.white, [0, self.judgebar_y, self.notewidth * 4, self.judgebar_height])
        pygame.draw.line(screen, self.white, (self.notewidth, 0), (self.notewidth, self.height))
        pygame.draw.line(screen, self.white, (self.notewidth * 2, 0), (self.notewidth * 2, self.height))
        pygame.draw.line(screen, self.white, (self.notewidth * 3, 0), (self.notewidth * 3, self.height))
        pygame.draw.line(screen, self.white, (self.notewidth * 4, 0), (self.notewidth * 4, self.height))

    def Title_draw(self, screen):
        Font = pygame.font.Font(None, 32)
        Text = Font.render("Title : " + self.musicname, True, self.white)
        screen.blit(Text, ((self.notewidth * 4) + 5, 0))

    def Score_draw(self, screen):
        Font = pygame.font.Font(None, 32)
        Text = Font.render("score : " + str(self.score), True, self.white)
        screen.blit(Text, ((self.notewidth * 4) + 5, 40))

    def Music_play(self):
        pygame.mixer.music.load(self.musicfolder + self.musicsource)
        pygame.mixer.music.play(1, 0.0)


black = (0, 0, 0)
white = (255, 255, 255)

width = 600
height = 700
case = 0
animationwidth = width / 2

musicfolder = 'music' + os.path.sep
notefolder = 'note' + os.path.sep

musiclist = ["YSR.ogg", "Aragami.ogg", "YSR.ogg"]
notelist = ["Aragami.txt", "test.txt"]
select = 0
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('rhythmgmae_v1')
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load(musicfolder + musiclist[0])
pygame.mixer.music.play(-1, 0.0)


def String_draw(string, size, x, y):
    Font = pygame.font.Font(None, size)
    Text = Font.render(string, True, black)
    TextRect = Text.get_rect()
    TextRect.center = (x, y)
    screen.blit(Text, TextRect)


while True:
    if case == 0:
        screen.fill(white)
        String_draw("Rhythmgame_v1", 70, animationwidth, height / 3)
        String_draw("Press Any Button", 30, animationwidth, height - (height / 3))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    while case == 0:
                        screen.fill(white)
                        animationwidth += width / (30 * 4)
                        String_draw("Rhythmgame_v1", 70, animationwidth, height / 3)
                        String_draw("Press Any Button", 30, animationwidth, height - (height / 3))
                        pygame.display.flip()
                        clock.tick(30)
                        if animationwidth > (width * 2):
                            case = 1
                            animationwidth = 0
        pygame.display.flip()
        clock.tick(30)

    elif case == 1:
        notecnt = len(notelist)
        select = -1

        while animationwidth < width / 2:
            screen.fill(white)
            if notecnt == 1:
                String_draw("You have " + str(1) + " song", 70, animationwidth, height / 3)
            elif notecnt == 0:
                String_draw("You don't have a song!", 70, animationwidth, height / 3)
                String_draw("Press Any key to exit.", 30, animationwidth, height - (height / 3))
            else:
                String_draw("You have " + str(1) + " songs", 70, animationwidth, height / 3)
            for i in range(0, len(notelist)):
                String_draw(str(i + 1) + ", " + notelist[i].split('.')[0], 30, animationwidth, height - (height / 3) + (i * 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            animationwidth += (width / (30 * 4))
            pygame.display.flip()
            clock.tick(30)

        screen.fill(white)
        if notecnt == 1:
            String_draw("You have " + str(1) + " song", 70, width / 2, height / 3)
        elif notecnt == 0:
            String_draw("You don't have a song!", 70, width / 2, height / 3)
            String_draw("Press Any key to exit.", 30, width / 2, height - (height / 3))
        else:
            String_draw("You have " + str(1) + " songs", 70, width / 2, height / 3)
        for i in range(0, len(notelist)):
            String_draw(str(i + 1) + ", " + notelist[i].split('.')[0], 30, width / 2, height - (height / 3) + (i*30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    select = 0
                if event.key == pygame.K_f:
                    if notecnt != 2:
                        select = notecnt - 1
                    else:
                        select = 1
                if event.key == pygame.K_j:
                    if notecnt != 3:
                        select = notecnt - 1
                    else:
                        select = 2
                if event.key == pygame.K_k:
                    if notecnt != 4:
                        select = notecnt - 1
                    else:
                        select = 3
                case = 2
        pygame.display.flip()
        clock.tick(30)

    elif case == 2:
        note_play = Note(notefolder, notelist[select], musicfolder, musiclist[select + 1], width, height)
        while note_play.flag:
            screen.fill(black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        note_play.Note_hit(screen, 1)
                        note_play.Effects_add(screen, 1)
                    if event.key == pygame.K_f:
                        note_play.Note_hit(screen, 2)
                        note_play.Effects_add(screen, 2)
                    if event.key == pygame.K_j:
                        note_play.Note_hit(screen, 3)
                        note_play.Effects_add(screen, 3)
                    if event.key == pygame.K_k:
                        note_play.Note_hit(screen, 4)
                        note_play.Effects_add(screen, 4)
            note_play.Notes_timecheck()
            note_play.Notes_draw(screen)
            note_play.JudgeBar_draw(screen)
            note_play.Effects_draw(screen)
            note_play.Title_draw(screen)
            note_play.Score_draw(screen)
            note_play.Judge_draw(screen)
            pygame.display.flip()
            clock.tick(30)
        while pygame.time.get_ticks() - note_play.endTime <= 3000:
            screen.fill(black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        note_play.Effects_add(screen, 1)
                        note_play.Note_hit(screen, 1)
                    if event.key == pygame.K_f:
                        note_play.Effects_add(screen, 2)
                        note_play.Note_hit(screen, 2)
                    if event.key == pygame.K_j:
                        note_play.Effects_add(screen, 3)
                        note_play.Note_hit(screen, 3)
                    if event.key == pygame.K_k:
                        note_play.Effects_add(screen, 4)
                        note_play.Note_hit(screen, 4)
            note_play.Notes_draw(screen)
            note_play.JudgeBar_draw(screen)
            note_play.Effects_draw(screen)
            note_play.Title_draw(screen)
            note_play.Score_draw(screen)
            note_play.Judge_draw(screen)
            pygame.display.flip()
            clock.tick(30)
        note_play = None
        case = 3
    elif case == 3:
        screen.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    case = 1
        pygame.display.flip()