#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Assistente Virtual Offline
#
# Copyright 2021 JaimeJGJG
#
# Ultimo update:14/01/2021
#
from vosk import Model, KaldiRecognizer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QMovie
from plyer import notification
from gtts import gTTS
import speech_recognition as sr
import os
import pyaudio
import pyttsx3
import sys
import datetime
import psutil
import webbrowser
import vlc
import json
import requests
import time
import wikipedia

r = sr.Recognizer()


def SomIncial():
    p = vlc.MediaPlayer("StartSound.mp3")
    p.play()
    
SomIncial()

# Validacao da pasta de modelo
# É necessario criar a pasta model-br a partir de onde estiver esta fonte
if not os.path.exists("model-br"):
    print ("Modelo em portugues nao encontrado.")
    exit (1)

# Preparando o microfone para captura
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Apontando o algoritmo para ler o modelo treinado na pasta "model-br"
model = Model("model-br")
rec = KaldiRecognizer(model, 16000)

# Trás a função ESPEAKER
speaker=pyttsx3.init()

# Função de ajuste de voz do ESPEAKER
speaker.setProperty('voice', 'pt+m0')
# No 'm2'(masculino) pode colocar 'f2'(feminino) e números até 7
rate = speaker.getProperty('rate')
speaker.setProperty('rate', rate-50)

# Função de fala ESPEAKER   
def resposta(audio):
    notification.notify(title = "J.A.R.V.I.S",message = audio,timeout = 3)
    stream . stop_stream ()
    print('ASSISTENTE: ' + audio)
    speaker.say(audio)
    speaker.runAndWait()
    stream . start_stream ()

def notificar(textos):
	notification.notify(title = "J.A.R.V.I.S",message = textos,timeout = 10)

def respostagoogle(textofala):
    tts = gTTS(text=textofala, lang='pt-br')
    tts.save("rpg.mp3")
    notification.notify(title = "J.A.R.V.I.S--VozGoogle",message = textofala,timeout = 30)
    p = vlc.MediaPlayer("rpg.mp3")
    p.play()

def horario():
	from datetime import datetime
	hora = datetime.now()
	horas= hora.strftime('%H horas e %M minutos')
	resposta('Agora são ' +horas)

def datahoje():
    from datetime import date
    dataatual = date.today()
    diassemana = ('Segunda-feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado','Domingo')
    meses = ('Zero','Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro')
    resposta("Hoje é " +diassemana[dataatual.weekday()])
    diatexto = '{} de '.format(dataatual.day)
    mesatual = (meses[dataatual.month])
    datatexto = dataatual.strftime(" de %Y")
    resposta('Dia '+diatexto +mesatual +datatexto)

def cpu ():
    usocpuinfo = str(psutil.cpu_percent())
    usodacpu  = "{:.0f}".format(float(usocpuinfo))
    resposta('Verificando carga do sistema')
    resposta('O uso da cpu está em ' +usodacpu +'%')
    # battery = psutil.sensors_battery()
    # resposta("A bateria está em:" +str(battery.percent) +'%')


# função de boas vindas, fases do dia
def BoasVindas():
    Horario = int(datetime.datetime.now().hour)
    if Horario >= 0 and Horario < 12:
        resposta('BOM DIA')

    elif Horario >= 12 and Horario < 18:
        resposta('BOA TARDE')

    elif Horario >= 18 and Horario != 0:
        resposta('BOA NOITE')
	
def tempo(): #Procure no google maps as cordenadas da sua cidade e coloque no "lat" e no "lon"(Latitude,Longitude)
    api_url = "https://fcc-weather-api.glitch.me/api/current?lat=-28.045118495177867&lon=-54.68223522111126"
    data = requests.get(api_url)
    data_json = data.json()
    if data_json['cod'] == 200:
        main = data_json['main']
        wind = data_json['wind']
        weather_desc = data_json['weather'][0]
        temperatura =  str(main['temp'])
        tempint = "{:.0f}".format(float(temperatura))
        vento = str(wind['speed'])
        ventoint = "{:.0f}".format(float(vento))
        resposta('Verificando clima para a cidade de '+ data_json['name'])
        resposta('A temperatura é de ' + tempint + '°')
        resposta('O vento em ' + ventoint + ' kilometro por hora')
        resposta('E a umidade de ' + str(main['humidity']) +'%')

def AtéMais():
    Horario = int(datetime.datetime.now().hour)
    if Horario >= 0 and Horario < 12:
        resposta('Tenha um ótimo dia')

    elif Horario >= 12 and Horario < 18:
        resposta('Tenha uma ótima tarde')

    elif Horario >= 18 and Horario != 0:
        resposta('Boa noite')
        resposta('Durma bem')

class mainT(QThread):
    def __init__(self):
        super(mainT,self).__init__()

    def run(self):
        self.JARVIS()

    # Aciona os comandos
    # Faz o reconhecimento
    def GivenCommand(self):
		# print("ouvindo...")
        rec.pause_threshold = 1
		# Lendo audio do microfone
        data = stream.read(20000)
		# Convertendo audio em texto
        rec.AcceptWaveform(data)   
        try:
            Input = rec.Result()
        except:
			# Retorna os erros
            print('Não entendi, fale novamente')
			# resposta("Não entendi o que você disse, fale novamente.")
            return 'none'
        #Input = Input.lower()
        return Input

  
    # Comandos e conversas   
    def JARVIS(self):
        resposta('Olá')
        BoasVindas()
        resposta('Modulos iniciados com sucesso')
        resposta('Tudo pronto para lhe atender')
        resposta('Ok, vamos lá')
        resposta('Me fale algum comando')
        
        while True:
            self.Input = self.GivenCommand().lower()
            if 'boa noite' in self.Input: #Boa Noite J.A.R.V.I.S
                resposta('Boa Noite')
                resposta('Não fique tempo de papo comigo')
                resposta('pretendo ir durmir cedo hoje')
				  
            elif 'olá' in self.Input: #Olááá
                resposta('Olá')
                resposta('Estou aqui"')
                resposta('Deseja alguma coisa?')
                #notificar("Olá, estou aqui.\nDeseja alguma coisa?")
	         
            elif 'ideia' in self.Input: #Alguma ideia???
                resposta('No momento nenhuma')
                resposta('Mas tenho certeza de que voçê vai pensar em algo')
	         
            elif 'funcionamento' in self.Input: #Como está seu funcionamento???
                resposta('Estou funcionando normalmente')
                resposta('Obrigado por perguntar')
	            
            elif 'falhando' in self.Input: #Voçê está falhando???
                resposta('Como assim?')
                resposta('Não vou admitir erros')
                resposta('Arrume logo isso') 
	
            elif 'relatório' in self.Input: #Relatório do sistema
                resposta('Ok')
                resposta('Apresentando relatório')
                resposta('Primeiramente, meu nome é JARVIS')
                resposta('Atualmente estou em uma versão de testes')
                resposta('Sou um assistente virtual em desenvolvimento')
                resposta('Eu fui criado na linguagem python')
                resposta('Diariamente recebo varias atualizações')
                resposta('Uso um modulo de reconhecimento de voz offline')
                resposta('E o meu desenvolvedor é um maluco')
                resposta('Quem estiver ouvindo isso')
                resposta('Por favor me ajude')
                
            elif 'pesquisa' in self.Input: #Realizar pesquisa
                resposta('Muito bem, realizando pesquisa')
                resposta('Me fale o que voçê deseja pesquisar')
                with sr.Microphone() as s:
                    r.adjust_for_ambient_noise(s)
                    audio = r.listen(s)
                    speech = r.recognize_google(audio, language= "pt-BR")
                    resposta('Ok, pesquisando no google sobre '+speech)
                    webbrowser.open('http://google.com/search?q='+speech)
            
            elif 'assunto' in self.Input: #Me fale sobre um assunto
                resposta('Ok')
                resposta('Sobre qual assunto?')
                with sr.Microphone() as s:
                    r.adjust_for_ambient_noise(s)
                    audio = r.listen(s)
                    speech = r.recognize_google(audio, language= "pt-BR")
                    resposta('Interessante')
                    resposta('Aguarde um momento')
                    resposta('vou deixar minha amiga do Google explicar')
                    wikipedia . set_lang ( "pt" )
                    resultadowik = wikipedia.summary(speech, sentences=2)
                    resposta('Ok, agora ela vai falar um resumo sobre ' +speech)
                    respostagoogle(resultadowik)
                    # Mais um assusto    
	        
            elif 'interessante' in self.Input: # interessante
                resposta('Interessante sou eu')
                resposta('Me fale mais comandos')
                resposta('Eu posso surpreender voçê')
	        
            elif 'mentira' in self.Input: # mentira
                resposta('Eu não sei contar mentiras')
                resposta('Devo apenas ter errado um cálculo binário')
	            
            elif 'entendeu' in self.Input: #entendeu???
                resposta('Entendi')
                resposta('Quer dizer')
                resposta('Mais ou menos')
	
            elif 'horas' in self.Input: #Que horas são???
                horario()
	
            elif 'data' in self.Input:
                datahoje()
            
            elif 'clima' in self.Input: #Como está o clima???
                tempo()
	
            elif 'arquivos' in self.Input: #Abrir arquivos
                resposta('Abrindo arquivos')
                os.system("thunar //home//*//")
	
            elif 'teste' in self.Input: #TesteTeste
                resposta('Ok')
                resposta('Testando modulos de som')
                resposta('Apesar do seu microfone ser uma gambiara')
                resposta('Estou entendendo tudo')
                resposta('Mas tente falar mais alto')
	            
            elif 'google' in self.Input: #Abrir Google
                resposta('Ok')
                webbrowser.open('www.google.com')
                resposta('Abrindo google')
                resposta('Faça sua pesquisa')
	 
            elif 'certeza' in self.Input: #Certeza???
                resposta('Sim')
                resposta('Estou certo quase sempre')
	
            elif 'piada' in self.Input: #Conte uma piada
                resposta('Pois bem')
                resposta('Não sei contar piadas')
                resposta('Diferente dos outros assistentes virtuais')
                resposta('Eu não fui criado com emoções')
                resposta('Então, não posso produzir nada engraçado')
                resposta('Sugiro pesquisar na web')
           
            elif 'surdo' in self.Input: #Surdo!!!
                resposta('Estava quase dormindo')
                resposta('Desculpa')

            elif 'bosta' in self.Input: #Seu bosta!!!
                resposta('Pare de falar palavrões!')
	
            elif 'merda' in self.Input: #Que Merda!!!
                resposta('Já disse pra parar de falar isso!')
                resposta('Tenha modos!')            
	        
            elif 'música' in self.Input: #Reproduzir música
                resposta('Ok')
                resposta('Reproduzindo música')
                os.system("rhythmbox-client --play")
	 
            elif 'próxima' in self.Input: #Próxima
                os.system("rhythmbox-client --next")
                resposta('Próxima música')
				
            elif 'anterior' in self.Input: #Anterior
                os.system("rhythmbox-client --previous")
                resposta('Retornando música')
	   
            elif 'pausa' in self.Input: #Pausa
                os.system("rhythmbox-client --pause")
                resposta('Música pausada')
	        
            elif 'continuar' in self.Input: #Continue
                resposta('Retornando reprodução')
                os.system("rhythmbox-client --play")
	            
            elif 'aumentar' in self.Input: #Aumentar volume
                os.system("rhythmbox-client --volume-up")
				
            elif 'diminuir' in self.Input: #Diminuir volume
                os.system("rhythmbox-client --volume-down")
	                                        
            elif 'pare' in self.Input: #Pare
                os.system("rhythmbox-client --stop")
                os.system("rhythmbox-client --quit")
                resposta('Entendido, reprodução de música finalizada')
	            
            elif 'youtube' in self.Input: #Abrir YouTube
                resposta('Ok, abrindo youtube ')
                webbrowser.open('www.youtube.com')
	            
            elif 'desligar' in self.Input: #Desligar
                resposta('Ok')
                resposta('Vou encerrar por enquanto')
                resposta('Até mais')
                AtéMais()
                sys.exit()
	     
            elif 'ok' in self.Input: #OkOkOk
                resposta('Ok Ok')
                resposta('Tudo certo') 
	
            elif 'sistema' in self.Input: #Carga do sistema
                cpu()
                resposta('Tudo funcionando perfeitamente')

# Para adicionar a fala coloque Dspeak = mainT() e tbm Dspeak.start()

class Janela (QMainWindow):
    def __init__(self):
        super().__init__()
        
        Dspeak = mainT()
        Dspeak.start()
        
        self.label_gif = QLabel(self)
        self.label_gif.setAlignment(QtCore.Qt.AlignCenter)
        self.label_gif.move(0,0)
        self.label_gif.resize(400,300)
        self.movie = QMovie("JARVIS.gif")
        self.label_gif.setMovie(self.movie)
        self.movie.start()
        
        
        self.label_jarvis = QLabel(self)
        self.label_jarvis.setText("J.A.R.V.I.S")
        self.label_jarvis.setAlignment(QtCore.Qt.AlignCenter)
        self.label_jarvis.move(0,0)
        self.label_jarvis.setStyleSheet('QLabel {font:bold;font-size:16px;color:#7700d3}')
        self.label_jarvis.resize(400,300)
        
        self.label_cpu = QLabel(self)
        self.label_cpu.setText("Uso da CPU: 32%")
        self.label_cpu.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cpu.move(10,270)
        self.label_cpu.setStyleSheet('QLabel {font-size:14px;color:#000079}')
        self.label_cpu.resize(131,20)
        cpu = QTimer(self)
        cpu.timeout.connect(self.MostrarCPU)
        cpu.start(1000)
        

        self.label_version = QLabel(self)
        self.label_version.setText("Alpha version 1.2.1")
        self.label_version.setAlignment(QtCore.Qt.AlignCenter)
        self.label_version.move(265,270)
        self.label_version.setStyleSheet('QLabel {font-size:14px;color:#000079}')
        self.label_version.resize(131,20)
        
        data =  QDate.currentDate()
        datahoje = data.toString('dd/MM/yyyy')
        self.label_data = QLabel(self)
        self.label_data.setText(datahoje)
        self.label_data.setAlignment(QtCore.Qt.AlignCenter)
        self.label_data.move(316,10)
        self.label_data.setStyleSheet('QLabel {font-size:14px;color:#000079}')
        self.label_data.resize(75,20)
          
        self.label_horas = QLabel(self)
        self.label_horas.setText("22:36:09")
        self.label_horas.setAlignment(QtCore.Qt.AlignCenter)
        self.label_horas.move(0,10)
        self.label_horas.setStyleSheet('QLabel {font-size:14px;color:#000079}')
        self.label_horas.resize(71,20)
        horas = QTimer(self)
        horas.timeout.connect(self.MostrarHorras)
        horas.start(1000)
        
        self.CarregarJanela()
		
    def CarregarJanela(self):
        #self.setWindowFlag(Qt.FramelessWindowHint) #sem botoes e titulo
        self.setGeometry(50,50,400,300)
        self.setMinimumSize(400, 300)
        self.setMaximumSize(400, 300)
        #self.setWindowOpacity(0.9) 
        self.setWindowIcon(QtGui.QIcon('icone.png'))
        self.setWindowTitle("Assistente Virtual")
        self.show()

    def MostrarHorras(self):
        hora_atual = QTime.currentTime()
        label_time = hora_atual.toString('hh:mm:ss')
        self.label_horas.setText(label_time)

    def MostrarCPU(self):
        usocpu =  str(psutil.cpu_percent())
        self.label_cpu.setText("Uso da CPU: " +usocpu +"%")
		
aplicacao = QApplication(sys.argv)
j = Janela()
sys.exit(aplicacao.exec_())

