from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import urllib.request
from PyQt5.uic import loadUiType
import pafy
import humanize

import os
from os import path

ui,_=loadUiType('main.ui')
class MainApp(QMainWindow, ui):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setWindowTitle("Download Manager")
        self.setupUi(self)
        self.InitUI()
        self.Handel_Buttons()

    def InitUI(self):
        ##contain all ui changes in loading
        self.tabWidget.tabBar().setVisible(False)

    def Handel_Buttons(self):
        ##handel all buttons
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)
        self.pushButton_4.clicked.connect(self.Get_Video_Data)
        self.pushButton_5.clicked.connect(self.Download_Video)
        self.pushButton_3.clicked.connect(self.save_Browse)
        self.pushButton_7.clicked.connect(self.Playlist_Download)
        self.pushButton_6.clicked.connect(self.Playlist_Save_Browse)
        
        self.pushButton_8.clicked.connect(self.Open_Home)
        self.pushButton_9.clicked.connect(self.Open_Download)
        self.pushButton_10.clicked.connect(self.Open_Youtube)
        self.pushButton_11.clicked.connect(self.Open_Settings)
        
        self.pushButton_12.clicked.connect(self.Apply_DarkOrange_Style)
        self.pushButton_13.clicked.connect(self.Apply_DarkGray_Style)
        self.pushButton_14.clicked.connect(self.Apply_QDark_Style)
        self.pushButton_15.clicked.connect(self.Apply_QDarkBlue_Style)

    def Handel_Progress(self,blocknum,blocksize,totalsize):
        ##calculate progress
        readed_data=blocknum*blocksize
        if totalsize>0:
            download_percentage=readed_data*100/totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()


    def Handel_Browse(self):
        ##enable browsing to our os, pick location
        save_location=QFileDialog.getSaveFileName(self,caption="Save as",directory=".",filter='All Files(*.*)')
        self.lineEdit_2.setText(str(save_location[0]))

    def Download(self):
        ##downloading any file
        download_url=self.lineEdit.text()
        save_location=self.lineEdit_2.text()
        if download_url=="" or save_location=="":
            QMessageBox.warning(self,"Data Error","Please Enter a valid Url or Save location")
        else:
            try:
                urllib.request.urlretrieve(download_url,save_location,self.Handel_Progress)
            except Exception:
                QMessageBox.warning(self,"Download Error","Please Enter a valid Url or Save location")
            return
    
        ############################################
        #######Download Youtube single video########

    def save_Browse(self):
        ##save location in the line edit
        save_location=QFileDialog.getSaveFileName(self,caption="Save as",directory=".",filter='All Files(*.*)')
        self.lineEdit_4.setText(str(save_location[0]))

    def Get_Video_Data(self):
        video_url=self.lineEdit_3.text()
        if video_url=="":
            QMessageBox.warning(self,"Data Error","Provide Valid URL")
        else:
            video=pafy.new(video_url)
            # print(video.title)
            # print(video.duration)
            # print(video.author)
            # print(video.length)
            # print(video.viewcount)
            # print(video.likes)
            # print(video.dislikes)
            video_streams=video.allstreams
            for stream in video_streams:
                size =humanize.naturalsize(stream.get_filesize())
                data="{} {} {} {}".format(stream.mediatype,stream.extension,stream.quality,size)
                if str(stream.mediatype) == "normal":
                    self.comboBox.addItem(data)

    def Download_Video(self):
        video_url= self.lineEdit_3.text()
        save_location=self.lineEdit_4.text()
        if video_url=="" or save_location=="":
            QMessageBox.warning(self,"Data Error","Please provide a valide url or save location")
        else:
            video=pafy.new(video_url)
            video_stream=video.videostreams
            video_quality=self.comboBox.currentIndex()
            download=video_stream[video_quality].download(filepath=save_location,callback=self.Video_Progress)

    def Video_Progress(self,total,recieved,ratio,rate,time):
        readed_data=recieved
        if total>0:
            download_percentage=readed_data*100/total
            self.progressBar_2.setValue(download_percentage)
            remaining_time=round(time/60,2)
            self.label_5.setText(str(' {} minutes remaining'.format(remaining_time))) 
            QApplication.processEvents()
    ##########################
    #######playlist##########

    def Playlist_Download(self):
        playlist_url=self.lineEdit_5.text()
        save_location=self.lineEdit_6.text()

        if playlist_url=="" or save_location=="":
            QMessageBox.warning(self,"Data Error","Please Enter a valid url or save location")
        else:
            playlist=pafy.get_playlist(playlist_url)
            playlist_videos=playlist['items']
            self.lcdNumber_2.display(len(playlist_videos))

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))

        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))
        current_video_in_download=1
        quality=self.comboBox_2.currentIndex()


        for video in playlist_videos:
            current_video=video['pafy']
            current_video_stream=current_video.videostreams
            self.lcdNumber.display(current_video_in_download)
            download=current_video_stream[quality].download(callback=self.Playlist_Progress)
            current_video_in_download+=1
            



    def Playlist_Progress(self,total,recieved,ratio,rate,time):
        readed_data=recieved
        if total>0:
            download_percentage=readed_data*100/total
            self.progressBar_3.setValue(download_percentage)
            remaining_time=round(time/60,2)
            self.label_6.setText('{} minutes remaining'.format(remaining_time))
            QApplication.processEvents()
        
    def Playlist_Save_Browse(self):
        playlist_save_location=QFileDialog.getExistingDirectory(self,'select Download Directory')
        self.lineEdit_6.setText(playlist_save_location)

    ####################################
    #########UI Changes Methods#######
    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Youtube(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(1)

    ###################################
    #####App Themes############
    def Apply_DarkOrange_Style(self):
        style=open('themes/darkorange.css','r')
        style=style.read()
        self.setStyleSheet(style)
    
    def Apply_DarkGray_Style(self):
        style=open('themes/qdarkgray.css','r')
        style=style.read()
        self.setStyleSheet(style)
    
    def Apply_QDark_Style(self):
        style=open('themes/qdark.css','r')
        style=style.read()
        self.setStyleSheet(style)
   
    def Apply_QDarkBlue_Style(self):
        style=open('themes/darkblu.css','r')
        style=style.read()
        self.setStyleSheet(style)

def main():
    app=QApplication(sys.argv)
    window=MainApp()
    window.show()
    app.exec_()

if __name__=='__main__':
    main()