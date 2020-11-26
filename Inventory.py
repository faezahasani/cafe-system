import os

import xlsxwriter
import openpyxl as op
from datetime import date

#Get today's date and current directory.
#Set path with today's date as document name.
today = date.today()
today_formated = today.strftime("%b-%d-%Y")
current_dir = os.getcwd()
sales_dir = current_dir + "/sales"
excel_dir = sales_dir + "/" + today_formated + ".xlsx"

#create folder for sales.
if not os.path.exists(sales_dir):
    os.makedirs(sales_dir)

#Creates workbook and worksheet
workbook = xlsxwriter.Workbook(excel_dir)
worksheet = workbook.add_worksheet("Sales")
row , orderNum = 0, 0
counter = 0
date = ""

class Inv(object):
    #class variables
    cell_header_format=None
    cell_header_format_1=None

    #Add the orders to the sales
    def add(self, order):
        global row, orderNum
        orderNum += 1

        Inv.set_format(self)

        #If sales does not exist creates file and add order, else append order
        if not os.path.exists(excel_dir):
            Inv.set_headers(self)
            orderNum = 1
            row+=1
            colText =0
            worksheet.write(row, colText, "Order #"+ str(orderNum))
            row+=1
            colText, colValue = 1, 2
            for i in order:
                for key in i:
                    if(key!='Nota' and key!='to-go'):
                        worksheet.write(row, colText, key)
                        worksheet.write(row, colValue, i[key])
                row += 1
                orderNum=+1
            workbook.close()
        else:
            wb = op.load_workbook(excel_dir)
            ws = wb.get_sheet_by_name('Sales')
            row += 1
            empty = ""
            ws.append(["Order #" + str(orderNum)])
            for i in order:
                for key in i:
                    if(key!='Nota' and key!='to-go'):
                        ws.append([empty, key, i[key]])
            wb.save(excel_dir)
            wb.close()

    #Creates the format for the excel file
    def set_format(self):
        Inv.cell_header_format = workbook.add_format()
        Inv.cell_header_format.set_bold()
        Inv.cell_header_format.set_bg_color('black')
        Inv.cell_header_format.set_font_color('white')
        Inv.cell_header_format.set_left()
        Inv.cell_header_format.set_right()
        Inv.cell_header_format.set_left_color('white')
        Inv.cell_header_format.set_right_color('white')

        Inv.cell_header_format_1 = workbook.add_format()
        Inv.cell_header_format_1.set_bold()
        Inv.cell_header_format_1.set_bg_color('black')
        Inv.cell_header_format_1.set_font_color('white')
        Inv.cell_header_format_1.set_border()
        Inv.cell_header_format_1.set_border_color('white')

        worksheet.set_column(0, 0, 15)
        worksheet.set_column(1, 1, 30)
        worksheet.set_column(2, 2, 5)
        worksheet.set_column(5, 5, 25)
        worksheet.set_column(6, 6, 10)

    #Create header for the file
    def set_headers(self):
        worksheet.write(0, 0, "Order #", Inv.cell_header_format)
        worksheet.write(0, 1, "Items", Inv.cell_header_format)
        worksheet.write(0, 2, "Cost", Inv.cell_header_format)
        worksheet.write(0, 5, "Total Number of Orders: ", Inv.cell_header_format_1)
        worksheet.write(1, 5, "Total Earnings: ", Inv.cell_header_format_1)
        worksheet.write(0, 6, "=COUNTA(A:A)-1")
        worksheet.write(1, 6, "=SUM(C:C)")