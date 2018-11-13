from tkinter import *
import requests
import json
from collections import namedtuple
fields = 'lutfen tutari girin',


def fetch(entries):
    for entry in entries:
        field = entry[0]
        paymentAmount = entry[1].get()
        print("%s:%s" % (field, paymentAmount))

    url = "https://sandbox-api.payosy.com/api/get_qr_sale"
    headers = {"accept": "application/json",
               "content-type": "application/json",
               "x-ibm-client-id": "b4e4932c-31c7-476e-a7c9-521104180d77",
               "x-ibm-client-secret": "yM2pL6bQ8cP1yO4fX7qF5uX2eP5pO7iP5lF1lM5qB0nF2hB3wV"}
    paymentAmount = entry[1].get()
    data = '{"totalReceiptAmount":'+ paymentAmount + '}'
    print(data)
    response = requests.post(url, headers=headers, data=data)
    x = json.loads(response.text, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    print(x.QRdata)
    left,right = x.QRdata.split("5303949",1)
    amountPart,right = right.split("800201",1)
    lenght = amountPart[2] + amountPart[3]
    left,amount = amountPart.split(lenght,1)
    print(response.text)
    print("odeme miktari:",amount)

    url = "https://sandbox-api.payosy.com/api/payment"
    headers = {"accept": "application/json",
               "content-type": "application/json",
               "x-ibm-client-id": "b4e4932c-31c7-476e-a7c9-521104180d77",
               "x-ibm-client-secret": "yM2pL6bQ8cP1yO4fX7qF5uX2eP5pO7iP5lF1lM5qB0nF2hB3wV"}

    data = '''{
                "returnCode":1000,
                "returnDesc":"success",
                "receiptMsgCustomer":"beko Campaign/n2018",
                "receiptMsgMerchant":"beko Campaign Merchant/n2018",
                "paymentInfoList":[
                    {
                        "paymentProcessorID":67,
                        "paymentActionList":[
                            {
                                "paymentType":3,
                                "amount":'''+amount+''',
                                "currencyID":949,
                                "vatRate":800
                            }
                        ]
                    }
                ],
                "QRdata":"'''+ x.QRdata+ '''"
          }'''
    print
    response = requests.post(url, headers=headers, data=data)
    print(response.text)






def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=15, text=field, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((field, ent))
    return entries


if __name__ == '__main__':
    root = Tk()
    root.title("QR Odeme Sistemi")
    ents = makeform(root, fields)

    b_show = Button(root,
                    text='QR olustur ve odeme yap',
                    command=(lambda e=ents: fetch(ents))
                    )

    b_stop = Button(root,
                    text='Uygulamayi Kapat',
                    command=root.destroy)

    b_show.pack(side=LEFT, padx=5, pady=5)
    b_stop.pack(side=LEFT, padx=5, pady=5)

    root.mainloop()