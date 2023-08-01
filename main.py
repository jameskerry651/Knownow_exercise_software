import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow
from qt_material import QtStyleTools
from PyQt5 import uic
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import Qt
import pandas as pd



class QuizApp(QMainWindow, QtStyleTools):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui\mainWindow.ui")
        self.apply_stylesheet(self.ui, 'dark_teal.xml')
        self.initUI()
        self.initSignal()
        self.choiceDataFrame = pd.read_csv("./data/choice_data.csv", encoding='utf-8')
        self.trueFalseDataFrame = pd.read_csv("./data/ture_false_data.csv", encoding='gbk')
        self.choiceLen = len(self.choiceDataFrame)  # 选择题的总数
        self.choiceSelectedIndexes = []             # 被选中过的选择题目索引
        self.tureFalseSelectedIndexes = []          # 被选中过的判断题目索引
        self.correctQesCount = 0                    # 本次做题正确数量
        self.totalQesCount = 0                      # 本次做题总数量
        self.updateNextChoiceQues()                 # 初始化第一道选择题目
        self.updateNextTrueFalseQues()              # 初始化第一道判断题目
        self.ui.statusBar().showMessage(f"本次做题总计: {self.totalQesCount}道,正确率: 0")


    def initUI(self):
        # 修改一些字体
        self.ui.quesLabel.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.AcheckBox.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.BcheckBox.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.CcheckBox.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.DcheckBox.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.EcheckBox.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.FcheckBox.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.choiceNextButton.setStyleSheet("font-size: 15pt; font-family: Microsoft YaHei;")
        self.ui.checkNextButton.setStyleSheet("font-size: 15pt; font-family: Microsoft YaHei;")
        self.ui.label.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.label_3.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.label_2.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.label_4.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.label_5.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.label_6.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.label_7.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.checkQuestionLabel.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.optionsLabel.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.answerLabel.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.questionLable.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.isTrueLabel.setStyleSheet("font-size: 15pt; font-family: Microsoft YaHei; color: green;")
        self.ui.checkLabel.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
        self.ui.isTrueLabel_2.setStyleSheet("font-size: 15pt; font-family: Microsoft YaHei; color: green;")
        self.ui.answerLabel_2.setStyleSheet("font-size: 10pt; font-family: Microsoft YaHei;")
    def initSignal(self):
        self.ui.choiceNextButton.clicked.connect(self.validateChoiceAnswer)
        self.ui.checkNextButton.clicked.connect(self.validateTrueFalseAnswer)
        self.ui.actionlight.triggered.connect(self.changeLightTheme)
        self.ui.actiondark_theme.triggered.connect(self.changeDarkTheme)

    def changeLightTheme(self):
        self.apply_stylesheet(self.ui, 'light_teal.xml')

    def changeDarkTheme(self):
        self.apply_stylesheet(self.ui, 'dark_teal.xml')

    # 随机生成一道不重复的选择题
    def genRandomChoiceQues(self):
        available_indexes = set(self.choiceDataFrame.index) - set(self.choiceSelectedIndexes)
        # 全部抽取完
        if not available_indexes:
            self.choiceSelectedIndexes = []  # 如果没有可用的索引，将choiceSelectedIndexes列表重置为空，以重新开始抽取
            available_indexes = self.choiceDataFrame.index.tolist()
        random_indexes = random.sample(available_indexes, 1)
        random_index = random_indexes[0]
        self.choiceSelectedIndexes.append(random_index)
        return self.choiceDataFrame.loc[random_index]
    def showImg(self,img_path):
        #对于有图片的题目，显示对应的图片
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(self.ui.imgLabel.size(), Qt.KeepAspectRatio)
        self.ui.imgLabel.setPixmap(pixmap)

    # 随机生成一道不重复的判断题
    def genRandomTrueFalseQues(self):
        available_indexes = set(self.trueFalseDataFrame.index) - set(self.tureFalseSelectedIndexes)
        # 全部抽取完
        if not available_indexes:
            self.tureFalseSelectedIndexes = []  # 如果没有可用的索引，将choiceSelectedIndexes列表重置为空，以重新开始抽取
            available_indexes = self.trueFalseDataFrame.index.tolist()
        random_indexes = random.sample(available_indexes, 1)
        random_index = random_indexes[0]
        self.tureFalseSelectedIndexes.append(random_index)
        return self.trueFalseDataFrame.loc[random_index]

    
    def findCommonLetters(self, str1, str2):
        # 将两个字符串转换为集合
        set1 = set(str1)
        set2 = set(str2)
        # 使用集合的交集操作找到共同的字母
        common_letters = set1.intersection(set2)
        return common_letters
    
    def updateNextTrueFalseQues(self):
         # 修改所有radionBox 选中状态为False
        self.ui.trueRadioButton.setChecked(False)
        self.ui.falseRadioButton.setChecked(False)
        
        quesSerie = self.genRandomTrueFalseQues()
        self.ui.checkLabel.setText(quesSerie.question)
        self.trueFalsequesSerie = quesSerie

    
    def updateNextChoiceQues(self):
        # 默认只有4个选项，隐藏第五和第六个选项
        self.ui.EcheckBox.setVisible(False)
        self.ui.FcheckBox.setVisible(False)
        # 修改所有checkBox 选中状态为False
        self.ui.AcheckBox.setChecked(False)
        self.ui.BcheckBox.setChecked(False)
        self.ui.CcheckBox.setChecked(False)
        self.ui.DcheckBox.setChecked(False)
        self.ui.EcheckBox.setChecked(False)
        self.ui.FcheckBox.setChecked(False)

        quesSerie = self.genRandomChoiceQues()
        self.choiceQuesSerie = quesSerie
        print(quesSerie)
        if quesSerie.isMultiChoice == 0:
            self.ui.choiceGroupBox.setTitle("单选题")
        else:
            self.ui.choiceGroupBox.setTitle("多选题")
        #更新问题
        self.ui.quesLabel.setText(quesSerie.question)
        #更新选项
        options_data = quesSerie.options.split(',')
        self.ui.AcheckBox.setText(options_data[0])
        self.ui.BcheckBox.setText(options_data[1])
        self.ui.CcheckBox.setText(options_data[2])
        if len(options_data) == 4:
            self.ui.DcheckBox.setVisible(True)
            self.ui.DcheckBox.setText(options_data[3])
        if len(options_data) == 5:
            self.ui.EcheckBox.setVisible(True)
            self.ui.EcheckBox.setText(options_data[4])
        elif len(options_data) == 6:
            self.ui.EcheckBox.setVisible(True)
            self.ui.EcheckBox.setText(options_data[4])
            self.ui.FcheckBox.setVisible(True)
            self.ui.FcheckBox.setText(options_data[5])
      

    def validateTrueFalseAnswer(self):
       

        self.totalQesCount = self.totalQesCount + 1
        answer = self.trueFalsequesSerie.answer  # 0 or 1
         
        # 异或验算答案
        if not self.ui.trueRadioButton.isChecked() ^ answer:
            self.correctQesCount = self.correctQesCount + 1
            self.ui.isTrueLabel_2.setStyleSheet("font-size: 15pt; font-family: Microsoft YaHei; color: green;")
            self.ui.isTrueLabel_2.setText("√")
        else:
            self.ui.isTrueLabel_2.setStyleSheet("font-size: 15pt; font-family: Microsoft YaHei; color: red;")
            self.ui.isTrueLabel_2.setText("x")
        # 显示答案
        if answer == 0:
            self.ui.answerLabel_2.setText("错误")
        else:
            self.ui.answerLabel_2.setText("正确")

         # 更新状态栏
        self.ui.statusBar().showMessage(f"本次做题总计: {self.totalQesCount}道,\
                                        正确率(%): {self.correctQesCount/self.totalQesCount*100:.2f}")
        # 显示问题
        self.ui.checkQuestionLabel.setText(self.trueFalsequesSerie.question)
        
        # 更新下一题
        self.updateNextTrueFalseQues()

    def validateChoiceAnswer(self):
        self.totalQesCount = self.totalQesCount + 1
        
        # 通过答案和选项求交集的方式判断是否正
        answer = self.choiceQuesSerie.answer
        checkStr = ""
        if self.ui.AcheckBox.isChecked():
            checkStr = checkStr + "A"
        if self.ui.BcheckBox.isChecked():
            checkStr = checkStr + "B"
        if self.ui.CcheckBox.isChecked():
            checkStr = checkStr + "C"
        if self.ui.DcheckBox.isChecked():
            checkStr = checkStr + "D"
        if self.ui.EcheckBox.isChecked():
            checkStr = checkStr + "E"
        if self.ui.FcheckBox.isChecked():
            checkStr = checkStr + "F"

        checkResult = self.findCommonLetters(checkStr,answer)
       
        if len(checkResult)==len(answer) and len(checkResult)==len(checkStr):
            # 回答正确
            self.correctQesCount = self.correctQesCount + 1
            self.ui.isTrueLabel.setStyleSheet("font-size: 15pt; font-family: Microsoft YaHei; color: green;")
            self.ui.isTrueLabel.setText("√")
        else: 
            self.ui.isTrueLabel.setStyleSheet("font-size: 15pt; font-family: Microsoft YaHei; color: red;")
            self.ui.isTrueLabel.setText("×")

        self.ui.answerLabel.setText(answer)
        self.ui.questionLable.setText(self.choiceQuesSerie.question)
        self.ui.optionsLabel.setText(self.choiceQuesSerie.options)
        # 更新状态栏
        self.ui.statusBar().showMessage(f"本次做题总计: {self.totalQesCount}道,\
                                        正确率(%): {self.correctQesCount/self.totalQesCount*100:.2f}")
        # 更新下一题
        self.updateNextChoiceQues()

       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_icon = QIcon("./ui/cat.png")
    app.setWindowIcon(app_icon)
    window = QuizApp()
    window.ui.show()
    sys.exit(app.exec_())
