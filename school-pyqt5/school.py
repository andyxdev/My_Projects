from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtWidgets import *

import sys

from PyQt5.uic import loadUiType
import mysql.connector as con

ui, _ = loadUiType('school.ui')



class MainApp(QMainWindow, ui):

	def __init__(self):

		QMainWindow.__init__(self)

		self.setupUi(self)

		self.tabWidget.setCurrentIndex(0)
		self.tabWidget.tabBar().setVisible(False)
		self.menubar.setVisible(False)
		self.b01.clicked.connect(self.login)
		self.menu11.triggered.connect(self.show_add_new_student_tab)
		self.b12.clicked.connect(self.save_student_details)

		self.menu12.triggered.connect(self.show_edit_or_delete_student_tab)
		self.cb21.currentIndexChanged.connect(self.fill_details_when_combo_box_selected)
		self.b21.clicked.connect(self.edit_student_details)
		self.b22.clicked.connect(self.delete_student_details)

		self.menu21.triggered.connect(self.show_mark_tab)
		self.b31.clicked.connect(self.save_mark_details)







	def login(self):

		un = self.tb01.text()

		pw = self.tb02.text()

		filename = QFileDialog.getOpenFileName()
		path = filename[0]
		print (path)

		if(un=="admin" and pw=="admin"):

			self.menubar.setVisible(True)

			self.tabWidget.setCurrentIndex(1)

		else:

			QMessageBox.information(self,"School Management system", "Invalid admin login details, Try again !")

			self.l01.setText("Invalid admin login details, Try again !")


		    #######  Add new student #########


	def show_add_new_student_tab(self):
		self.tabWidget.setCurrentIndex(2)
		self.fill_next_registration_number()
        	



	def fill_next_registration_number(self):
		try:
			rn = 0
			mydb = con.connect(host="localhost",user="root",password="",db="school")
			cursor = mydb.cursor()
			cursor.execute("select * from student")
			result = cursor.fetchall()
			if result:
				for stud in result:
					rn += 1
					self.tb11.setText(str(rn+1))
		except con.Error as e:
			print("Error occured in select studen reg number" + e)

	def save_student_details(self):
		try:
			mydb = con.connect(host="localhost",user="root",password="",db="school")
			cursor = mydb.cursor()
			registration_number = self.tb11.text()
			full_name = self.tb12.text()
			gender = self.cb11.currentText()
			date_of_birth = self.tb13.text()
			age = self.tb14.text()
			address = self.mtb11.toPlainText()
			phone = self.tb15.text()
			email = self.tb16.text()
			standard = self.cb12.currentText()
			qry = "insert into student (registration_number,full_name,gender,date_of_birth,age,address,phone,email,standard) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			value = (registration_number,full_name,gender,date_of_birth,age,address,phone,email,standard)
			cursor.execute(qry,value)
			mydb.commit()
			self.l11.setText("Student details saved successfully")
			QMessageBox.information(self, "School management system","Student details added successfully!")
			self.tb11.setText("")
			self.tb12.setText("")
			self.tb13.setText("")
			self.tb14.setText("")
			self.tb15.setText("")
			self.tb16.setText("")
			self.mtb11.setText("")
			self.tabWidget.setCurrentIndex(1)
		except con.Error as e:
			self.l11.setText("Error in save student form " + e)

#######  Edit / Delete student #########



	def show_edit_or_delete_student_tab(self):

		self.tabWidget.setCurrentIndex(3)

		self.fill_registration_number_in_combobox()



	def fill_registration_number_in_combobox(self):

		try:
			self.cb21.clear()
			mydb = con.connect(host="localhost",user="root",password="",db="school")
			cursor = mydb.cursor()
			cursor.execute("select * from student")
			result = cursor.fetchall()
			if result:
				for stud in result:
					self.cb21.addItem(str(stud[1]))

		except con.Error as e:
			print("Error occured in fill reg number in combo " + e)



	def fill_details_when_combo_box_selected(self):

		try:
			mydb = con.connect(host="localhost",user="root",password="",db="school")
			cursor = mydb.cursor()
			cursor.execute("select * from student where registration_number = '"+ self.cb21.currentText() +"'")
			result = cursor.fetchall()
			if result:
				for stud in result:
					self.tb21.setText(str(stud[2]))
					self.tb22.setText(str(stud[3]))
					self.tb23.setText(str(stud[4]))
					self.tb24.setText(str(stud[5]))
					self.mtb21.setText(str(stud[6]))
					self.tb25.setText(str(stud[7]))
					self.tb26.setText(str(stud[8]))
					self.tb27.setText(str(stud[9]))
		except con.Error as e:
			print("Error occured in fill defails when combo selected " + e)

	def edit_student_details(self):

		try:
			mydb = con.connect(host="localhost",user="root",password="",db="school")
			cursor = mydb.cursor()
			registration_number = self.cb21.currentText()
			full_name = self.tb21.text()
			gender = self.tb22.text()
			date_of_birth = self.tb23.text()
			age = self.tb24.text()
			address = self.mtb21.toPlainText()
			phone = self.tb25.text()
			email = self.tb26.text()
			standard = self.tb27.text()
			qry = "update student set full_name = '"+ full_name +"',gender = '"+ gender +"',date_of_birth = '"+ date_of_birth +"',age = '"+ age +"', address = '"+ address +"',phone = '"+ phone +"',email = '"+ email +"',standard = '"+ standard +"'  where registration_number = '"+ registration_number +"'"
			cursor.execute(qry)
			mydb.commit()
			self.l21.setText("Student details modified successfully")
			QMessageBox.information(self, "School management system","Student details modified successfully!")
			self.tb21.setText("")
			self.tb22.setText("")
			self.tb23.setText("")
			self.tb24.setText("")
			self.tb25.setText("")
			self.tb26.setText("")
			self.tb27.setText("")
			self.mtb21.setText("")
			self.tabWidget.setCurrentIndex(1)

		except con.Error as e:
			self.l21.setText("Error in edit student form " + e)

	def delete_student_details(self):
		m = QMessageBox.question(self,"Delete","Are you sure want to delete this students details", QMessageBox.Yes|QMessageBox.No)
		if m == QMessageBox.Yes:
			try:
				mydb = con.connect(host="localhost",user="root",password="",db="school")
				cursor = mydb.cursor()
				registration_number = self.cb21.currentText()
				qry = "delete from student where registration_number = '"+ registration_number +"'"
				cursor.execute(qry)
				mydb.commit()
				self.l21.setText("Student details delete_student_details successfully")
				QMessageBox.information(self, "School management system","Student details deleted successfully!")
				self.tabWidget.setCurrentIndex(1)
			except con.Error as e:
				self.l21.setText("Error in delete student form " + e)


    			##########  Mark Details #############



	def show_mark_tab(self):
		self.tabWidget.setCurrentIndex(4)
		self.fill_registration_number_in_combobox_for_mark_tab()

	def fill_registration_number_in_combobox_for_mark_tab(self):
		try:
			self.cb31.clear()
			self.cb32.clear()
			mydb = con.connect(host="localhost",user="root",password="",db="school")
			cursor = mydb.cursor()
			cursor.execute("select * from student")
			result = cursor.fetchall()
			if result:
				for stud in result:
					self.cb31.addItem(str(stud[1]))
					self.cb32.addItem(str(stud[1]))
		except con.Error as e:
			print("Error occured in fill reg number in combo " + e)

	def save_mark_details(self):
		try:
			mydb = con.connect(host="localhost",user="root",password="",db="school")
			cursor = mydb.cursor()
			registration_number = self.cb31.currentText()
			exam_name = self.tb31.text()
			language = self.tb32.text()
			english = self.tb33.text()
			maths = self.tb34.text()
			science = self.tb35.text()
			social = self.tb36.text()
			qry = "insert into mark (registration_number,exam_name,language,english,maths,science,social) values(%s,%s,%s,%s,%s,%s,%s)"
			value = (registration_number,exam_name,language,english,maths,science,social)
			cursor.execute(qry,value)
			mydb.commit()
			self.l31.setText("Mark details saved successfully")
			QMessageBox.information(self, "School management system","Mark details added successfully!")
			self.tb31.setText("")
			self.tb32.setText("")
			self.tb33.setText("")
			self.tb34.setText("")
			self.tb35.setText("")
			self.tb36.setText("")
			self.tabWidget.setCurrentIndex(1)
		except con.Error as e:
			self.l11.setText("Error in save mark form " + e)






def main():

	app = QApplication(sys.argv)

	window = MainApp()

	window.show()

	app.exec_()



if __name__ == '__main__':

	main()


