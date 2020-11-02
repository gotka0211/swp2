import pickle
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel,
    QComboBox, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt

class ScoreDB(QWidget):
    # 생성자
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dbfilename = 'assignment6.dat'
        self.scoredb = []
        self.readScoreDB()
        self.showScoreDB()

    # 인터페이스 구현
    def initUI(self):
            ## 값 입력 행
        namelabel = QLabel('Name:')
        self.name = QLineEdit()
        agelabel = QLabel('Age:')
        self.age = QLineEdit()
        scorelabel = QLabel('Score:')
        self.score = QLineEdit()

        inputline = QHBoxLayout()
        inputline.addWidget(namelabel)
        inputline.addWidget(self.name)
        inputline.addWidget(agelabel)
        inputline.addWidget(self.age)
        inputline.addWidget(scorelabel)
        inputline.addWidget(self.score)

            ## 값 입력 행 2
        amountlabel = QLabel('Amount:')
        self.amount = QLineEdit()
        keylabel = QLabel('Key:')
        self.key = QComboBox()
        self.key.addItems(['Age','Name','Score'])

        inputline2 = QHBoxLayout()
        inputline2.addStretch(1)
        inputline2.addWidget(amountlabel)
        inputline2.addWidget(self.amount)
        inputline2.addWidget(keylabel)
        inputline2.addWidget(self.key)

            ## 명령어 버튼
        addbutton = QPushButton('Add')
        delbutton = QPushButton('Del')
        findbutton = QPushButton('Find')
        incbutton = QPushButton('Inc')
        showbutton = QPushButton('Show')

                ### 버튼연결
        addbutton.clicked.connect(self.buttonClicked)
        delbutton.clicked.connect(self.buttonClicked)
        findbutton.clicked.connect(self.buttonClicked)
        incbutton.clicked.connect(self.buttonClicked)
        showbutton.clicked.connect(self.buttonClicked)

        commandline = QHBoxLayout()
        commandline.addStretch(1)
        commandline.addWidget(addbutton)
        commandline.addWidget(delbutton)
        commandline.addWidget(findbutton)
        commandline.addWidget(incbutton)
        commandline.addWidget(showbutton)

            ## 결과창
        self.resultlabel = QLabel('Result:')
        self.result = QTextEdit()
        self.result.setReadOnly(True) #결과창에 임의로 데이터를 수정할 수 없게

        resultline = QVBoxLayout()
        resultline.addWidget(self.resultlabel)
        resultline.addWidget(self.result)

        # 레이아웃 결합
        main = QVBoxLayout()
        main.addLayout(inputline)
        main.addLayout(inputline2)
        main.addLayout(commandline)
        main.addLayout(resultline)

        self.setLayout(main)
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Assignment6_20163199')
        self.show()

    # 종료시 scoredb의 내용을 파일에 저장
    def closeEvent(self, event):
        self.writeScoreDB()

    # 실행시 데이터 파일을 읽어 scoredb 리스트에 저장
    def readScoreDB(self):
        try:
            fH = open(self.dbfilename, 'rb')
        except FileNotFoundError as e:
            self.scoredb = []
            return

        try:
            self.scoredb =  pickle.load(fH)
        except:
            pass
        else:
            pass
        fH.close()

    # write the data into person db
    def writeScoreDB(self):
        fH = open(self.dbfilename, 'wb')
        pickle.dump(self.scoredb, fH)
        fH.close()

    # Show 명령어
    def showScoreDB(self):
        self.resultlabel.setText('Result: Show list sorting by {}'.format(self.key.currentText()))
        self.result.setText('') #result 초기화
        for p in sorted(self.scoredb, key=lambda person: person[self.key.currentText()]):
            self.result.append('Age={}\tName={}\t\tScore={}'.format(p['Age'],p['Name'],p['Score']))

    # Add 명령어
    def addScoreDB(self):
        try:
            if not self.name.text()=='':
                record = {'Name': self.name.text(), 'Age': int(self.age.text()), 'Score': int(self.score.text())}
                self.scoredb += [record]
                self.showScoreDB()
                self.resultlabel.setText(
                    'Result: Add new data(Age:{}, Name:{}, Score:{})'
                        .format(self.age.text(), self.name.text(), self.score.text()))
            else: #에러처
                self.resultlabel.setText('Result: Error!')
                self.result.setText('Insufficient information!\n\'Add\' requires : Name, Age, Score')
        except: #에러처리
            self.resultlabel.setText('Result: Error!')
            if self.age.text() =='' or self.score.text()=='': # 인자를 충분히 기입하지 않았을 경우
                self.result.setText('Insufficient information!\n\'Add\' requires : Name, Age, Score')
            else: # 나이와 점수에 숫자가 아닌 수를 넣었을 경우
                self.result.setText('Invalid data type!\nAge & Score must be Integer')
        self.boxInitialize()

    # Del 명령어
    def delScoreDB(self):
        dellist = []
        for p in self.scoredb:  # del할 사람이 리스트에 있는지 판별하여
            if p['Name'] == self.name.text():
                dellist.append(p)  # 해당 이름의 사람의 수만큼 dellist가 채워집니다.
        if dellist:  # 그러면 그 수만큼 scdb에서 del 작업을 수행하여 해당이름을 가진 모든 사람의 정보를 삭제합니다.
            for p in dellist:
                self.scoredb.remove(p)
            self.showScoreDB()
            self.resultlabel.setText('Result: Del \'{}\''.format(self.name.text()))
        else:  # 에러처리
            self.resultlabel.setText('Result: Error!')
            if self.name.text() == '': #Name에 아무것도 기입하지 않았을 경우,
                self.result.setText('Nothing was written in \'Name\'! Try again ')
            else: #해당이름을 가진 사람이 scoredb에 없을경우.
                self.result.setText('\'{}\' : not in the scoreDB! Try again'.format(self.name.text()))
        self.boxInitialize()

    # Find 명령어
    def findScoreDB(self):
        self.result.setText('')
        for p in sorted(self.scoredb, key=lambda person: person[self.key.currentText()]): # 리스트를 훑으면서 해당 이름을 가진 사람의 정보를 출력합니다.
            if self.name.text() in p.values():
                self.resultlabel.setText('Result: Find {}'.format(self.name.text()))
                self.result.append('Age={}\tName={}\t\tScore={}'.format(p['Age'], p['Name'], p['Score']))
        if self.result.toPlainText() =='':  #에러처리
            self.resultlabel.setText('Result: Error!')
            if self.name.text()=='':  #Name에 아무것도 기입하지 않았을 경우,
                self.result.setText('Nothing was written in \'Name\'! Try again ')
            else: #해당이름을 가진 사람이 scoredb에 없을경우.
                self.result.setText('\'{}\' : not in the scoreDB! Try again'.format(self.name.text()))
        self.boxInitialize()

    # Inc 명령어
    def incScoreDB(self):
        exist = False
        try:
            for p in self.scoredb:
                if self.name.text() in p.values():
                    exist = True
                    p['Score'] += int(self.amount.text())
            if exist:
                self.showScoreDB()
                self.resultlabel.setText('Result: {}\'s Score was changed by {}'.format(self.name.text(),self.amount.text()))
            #에러처리
            else:  # 해당 사람이 리스트에 없는 경우
                if self.name.text() == '':  # Name에 아무것도 기입하지 않았을 경우,
                    self.result.setText('Nothing was written in \'Name\'! Try again ')
                else:  # 해당이름을 가진 사람이 scoredb에 없을경우.
                    self.result.setText('\'{}\' : not in the scoreDB! Try again'.format(self.name.text()))
        except ValueError:  # amount에 정수가 아닌 문자를 적었을 경우
            self.resultlabel.setText('Result: Error!')
            self.result.setText('#Invalid data type!\nAmount must be Integer'.format(self.name.text()))
        self.boxInitialize()

    # 입력 칸 초기화 함수
    def boxInitialize(self):
        self.name.setText('')
        self.age.setText('')
        self.score.setText('')
        self.amount.setText('')

    # 버튼을 누를 때 이벤트 처리
    def buttonClicked(self):
        sender = self.sender()
        if sender.text() == 'Add':
            self.addScoreDB()
        elif sender.text() == 'Del':
            self.delScoreDB()
        elif sender.text() == 'Find':
            self.findScoreDB()
        elif sender.text() == 'Inc':
            self.incScoreDB()
        elif sender.text() == 'Show':
            self.showScoreDB()

if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = ScoreDB()
    sys.exit(app.exec_())

