from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QSizePolicy


def toggle_content_screen(layout, screen_name="", order=None):
    reset_layout(layout)

    if screen_name == "volumeSelection":
        create_volume_selection_screen(layout)
    elif screen_name == "insertCard":
        create_insert_card_screen(layout, order)
    elif screen_name == "processingPayment":
        create_processing_payment_screen(layout)
    elif screen_name == "tapSelection":
        create_tap_selection_screen(layout)
    elif screen_name == "dispensingWater":
        create_dispensing_water_screen(layout, order)
    elif screen_name == "dispensedShowBalance":
        pass
    elif screen_name == "paymentFailed":
        print("Payment Failed")
        pass


def reset_layout(layout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)


def create_footer_section(layout):
    font = QFont()
    font.setFamily(u"Arial")
    font.setPointSize(10)
    font.setBold(True)
    font.setWeight(75)

    l1 = QLabel()
    l2 = QLabel()
    l3 = QLabel()

    l1.setFont(font)
    l1.setStyleSheet(u"background: black;\n"
                     "color:white;")
    l1.setAlignment(Qt.AlignCenter)
    l1.setText(u"99K SOCIAL ENTERPRISE")
    l1.setMinimumHeight(54)

    l2.setFont(font)
    l2.setStyleSheet(u"background: black;\n"
                     "color:white;")
    l2.setAlignment(Qt.AlignCenter)
    l2.setText(u"SAVE WATER - SAVE LIFE")
    l1.setMinimumHeight(54)

    l3.setFont(font)
    l3.setStyleSheet(u"background: black;\n"
                     "color:white;")
    l3.setAlignment(Qt.AlignCenter)
    l3.setText(u"STATUS: ACTIVE")
    l1.setMinimumHeight(54)

    layout.addWidget(l1)
    layout.addWidget(l2)
    layout.addWidget(l3)


def create_volume_selection_screen(layout):
    font = QFont()
    font.setFamily(u"Arial")
    font.setBold(True)

    lInstruction = QLabel("lInstruction")
    lInstruction.setText("PLEASE SELECT VOLUME")
    lInstruction.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
    lInstruction.setStyleSheet("font-size:36px;color:white;")
    lInstruction.setFont(font)

    # CARD 1
    vol_1_lbl = QLabel("1 LITER")
    vol_1_lbl.setAlignment(Qt.AlignCenter)
    vol_1_lbl.setFont(font)
    vol_1_lbl.setStyleSheet("font-size:22px;color:black;background:white;border-top-left-radius:5px;border-bottom-left-radius:5px;")
    price_1_lbl = QLabel("Rs 5 /-")
    price_1_lbl.setAlignment(Qt.AlignCenter)
    price_1_lbl.setFont(font)
    price_1_lbl.setStyleSheet("font-size:22px;color:black;font-style:bold;background:white;")
    but_1_lbl = QLabel("1L")
    but_1_lbl.setAlignment(Qt.AlignCenter)
    but_1_lbl.setFont(font)
    but_1_lbl.setStyleSheet("font-size:18px;color:white;background:rgba( 58, 125, 242, 0.8 );border-top-right-radius:5px;border-bottom-right-radius:5px;border-top-left-radius:5px;border-bottom-left-radius:5px;")
    but_1_wid = QWidget()
    but_1_wid.setStyleSheet("background:white;border-top-right-radius:5px;border-bottom-right-radius:5px;")
    but_1_lay = QHBoxLayout()
    but_1_lay.addWidget(but_1_lbl)
    but_1_lay.setSpacing(0)
    but_1_lay.setContentsMargins(72, 13, 13, 13)
    but_1_wid.setLayout(but_1_lay)
    card_1_lay = QHBoxLayout()
    card_1_lay.setSpacing(0)
    card_1_lay.setContentsMargins(63, 66, 63, 66)
    card_1_lay.addWidget(vol_1_lbl)
    card_1_lay.addWidget(price_1_lbl)
    card_1_lay.addWidget(but_1_wid)
    card_1_wid = QWidget()
    card_1_wid.setLayout(card_1_lay)

    # CARD 2
    vol_2_lbl = QLabel("2 LITERS")
    vol_2_lbl.setAlignment(Qt.AlignCenter)
    vol_2_lbl.setFont(font)
    vol_2_lbl.setStyleSheet(
        "font-size:22px;color:black;background:white;border-top-left-radius:5px;border-bottom-left-radius:5px;")
    price_2_lbl = QLabel("Rs 10 /-")
    price_2_lbl.setAlignment(Qt.AlignCenter)
    price_2_lbl.setFont(font)
    price_2_lbl.setStyleSheet("font-size:22px;color:black;font-style:bold;background:white;")
    but_2_lbl = QLabel("2L")
    but_2_lbl.setAlignment(Qt.AlignCenter)
    but_2_lbl.setFont(font)
    but_2_lbl.setStyleSheet(
        "font-size:18px;color:white;background:rgba( 58, 125, 242, 0.8 );font-style:bold;border-top-right-radius:5px;border-bottom-right-radius:5px;border-top-left-radius:5px;border-bottom-left-radius:5px;")
    but_2_wid = QWidget()
    but_2_wid.setStyleSheet(
        "background:white;border-top-right-radius:5px;border-bottom-right-radius:5px;")
    but_2_lay = QHBoxLayout()
    but_2_lay.addWidget(but_2_lbl)
    but_2_lay.setSpacing(0)
    but_2_lay.setContentsMargins(72, 13, 13, 13)
    but_2_wid.setLayout(but_2_lay)
    card_2_lay = QHBoxLayout()
    card_2_lay.setSpacing(0)
    card_2_lay.setContentsMargins(63, 66, 63, 66)
    card_2_lay.addWidget(vol_2_lbl)
    card_2_lay.addWidget(price_2_lbl)
    card_2_lay.addWidget(but_2_wid)
    card_2_wid = QWidget()
    card_2_wid.setLayout(card_2_lay)

    # CARD 3
    vol_3_lbl = QLabel("5 LITERS")
    vol_3_lbl.setAlignment(Qt.AlignCenter)
    vol_3_lbl.setFont(font)
    vol_3_lbl.setStyleSheet(
        "font-size:22px;color:black;font-style:bold;background:white;border-top-left-radius:5px;border-bottom-left-radius:5px;")
    price_3_lbl = QLabel("Rs 15 /-")
    price_3_lbl.setAlignment(Qt.AlignCenter)
    price_3_lbl.setFont(font)
    price_3_lbl.setStyleSheet("font-size:22px;color:black;font-style:bold;background:white;")
    but_3_lbl = QLabel("5L")
    but_3_lbl.setAlignment(Qt.AlignCenter)
    but_3_lbl.setFont(font)
    but_3_lbl.setStyleSheet(
        "font-size:18px;color:white;background:rgba( 58, 125, 242, 0.8 );font-style:bold;border-top-right-radius:5px;border-bottom-right-radius:5px;border-top-left-radius:5px;border-bottom-left-radius:5px;")
    but_3_wid = QWidget()
    but_3_wid.setStyleSheet(
        "background:white;border-top-right-radius:5px;border-bottom-right-radius:5px;")
    but_3_lay = QHBoxLayout()
    but_3_lay.addWidget(but_3_lbl)
    but_3_lay.setSpacing(0)
    but_3_lay.setContentsMargins(72, 13, 13, 13)
    but_3_wid.setLayout(but_3_lay)
    card_3_lay = QHBoxLayout()
    card_3_lay.setSpacing(0)
    card_3_lay.setContentsMargins(63, 66, 63, 66)
    card_3_lay.addWidget(vol_3_lbl)
    card_3_lay.addWidget(price_3_lbl)
    card_3_lay.addWidget(but_3_wid)
    card_3_wid = QWidget()
    card_3_wid.setLayout(card_3_lay)

    layout.addWidget(lInstruction)
    layout.addWidget(card_1_wid)
    layout.addWidget(card_2_wid)
    layout.addWidget(card_3_wid)


def make_label_btn_card_widget(label, btn_label, btn_color):
    font = QFont()
    font.setFamily(u"Arial")
    font.setBold(True)

    lbl = QLabel(label)
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setFont(font)
    lbl.setStyleSheet(
        "font-size:22px;color:black;background:white;border-top-left-radius:5px;border-bottom-left-radius:5px;")
    but_lbl = QLabel(btn_label)
    but_lbl.setAlignment(Qt.AlignCenter)
    but_lbl.setFont(font)
    but_lbl.setStyleSheet(
        "font-size:18px;color:white;border-top-right-radius:5px;border-bottom"
        "-right-radius:5px;border-top-left-radius:5px;border-bottom-left-radius:5px;background:{};".format(btn_color))
    but_wid = QWidget()
    but_wid.setStyleSheet(
        "background:white;border-top-right-radius:5px;border-bottom-right-radius:5px;")
    but_lay = QHBoxLayout()
    but_lay.addWidget(but_lbl)
    but_lay.setSpacing(0)
    but_lay.setContentsMargins(135, 13, 13, 13)
    but_wid.setLayout(but_lay)
    card_lay = QHBoxLayout()
    card_lay.setSpacing(0)
    card_lay.setContentsMargins(63, 36, 63, 27)
    card_lay.addWidget(lbl)
    card_lay.addWidget(but_wid)
    card_wid = QWidget()
    card_wid.setLayout(card_lay)

    return card_wid


def create_insert_card_screen(layout, order):
    # print(order.get_volume(), )
    volume, amount = order.get_volume(), order.get_amount()

    font = QFont()
    font.setFamily(u"Arial")
    font.setBold(True)

    # Voume Card
    if volume == '1':
        vol_txt = f'{volume} LITER'
    else:
        vol_txt = f'{volume} LITERS'
    vol_lbl = QLabel(vol_txt)
    vol_lbl.setAlignment(Qt.AlignCenter)
    vol_lbl.setFont(font)
    vol_lbl.setStyleSheet(
        "font-size:18px;color:white;background:green;border-top-left-radius:5px;border-bottom-left-radius:5px;")
    price_txt = f'Rs {amount} /-'
    price_lbl = QLabel(price_txt)
    price_lbl.setAlignment(Qt.AlignCenter)
    price_lbl.setFont(font)
    price_lbl.setStyleSheet("font-size:18px;color:white;background:green;border-top-right-radius:5px;border-bottom-right-radius:5px;")
    card_vol_lay = QHBoxLayout()
    card_vol_lay.setSpacing(0)
    card_vol_lay.setContentsMargins(63, 66, 63, 66)
    card_vol_lay.addWidget(vol_lbl)
    card_vol_lay.addWidget(price_lbl)
    card_vol = QWidget()
    card_vol.setLayout(card_vol_lay)

    # Instruction Label
    lInstruction = QLabel("lInstruction")
    lInstruction.setText("PLEASE INSERT CARD")
    lInstruction.setFont(font)
    lInstruction.setAlignment(Qt.AlignCenter)
    lInstruction.setStyleSheet("font-size:36px;color:white;")


    # Card card
    card_lbl = QLabel("CARD")
    card_lbl.setAlignment(Qt.AlignCenter)
    card_lbl.setStyleSheet("font-size:36px;color:black;background-color:white;")

    card = QWidget()
    card_lay = QHBoxLayout()
    card_lay.addWidget(card_lbl)
    card.setContentsMargins(108, 9, 108, 9)
    card.setLayout(card_lay)

    # Cancel Card
    lbl = QLabel("CANCEL")
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setFont(font)
    lbl.setStyleSheet(
        "font-size:22px;color:black;background:white;border-top-left-radius:5px;border-bottom-left-radius:5px;")
    but_lbl = QLabel("C")
    but_lbl.setAlignment(Qt.AlignCenter)
    but_lbl.setFont(font)
    but_lbl.setStyleSheet(
        "font-size:18px;color:white;border-top-right-radius:5px;border-bottom"
        "-right-radius:5px;border-top-left-radius:5px;border-bottom-left-radius:5px;background:red;")
    but_wid = QWidget()
    but_wid.setStyleSheet(
        "background:white;border-top-right-radius:5px;border-bottom-right-radius:5px;")
    but_lay = QHBoxLayout()
    but_lay.addWidget(but_lbl)
    but_lay.setSpacing(0)
    but_lay.setContentsMargins(135, 13, 13, 13)
    but_wid.setLayout(but_lay)
    card_lay = QHBoxLayout()
    card_lay.setSpacing(0)
    card_lay.setContentsMargins(63, 66, 63, 66)
    card_lay.addWidget(lbl)
    card_lay.addWidget(but_wid)
    card_cancel = QWidget()
    card_cancel.setLayout(card_lay)



    layout.addWidget(card_vol)
    layout.addWidget(lInstruction)
    layout.addWidget(card)
    layout.addWidget(card_cancel)

# TODO: MODIFY
def create_processing_payment_screen(layout):
    lAns2 = QLabel("lAns2")
    lAns2.setText("PROCESSING PAYMENT")
    lAns2.setAlignment(Qt.AlignCenter)
    lAns2.setStyleSheet("font-size:36px;color:white;font-style:bold;border:1px solid white;")

    layout.addWidget(lAns2)


def create_tap_selection_screen(layout):
    font = QFont()
    font.setFamily(u"Arial")
    font.setBold(True)

    lInstruction = QLabel("lAns2")
    lInstruction.setText("PLEASE SELECT TAP")
    lInstruction.setFont(font)
    lInstruction.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
    lInstruction.setStyleSheet("font-size:36px;color:white;")

    blue = "rgba( 58, 125, 242, 0.8 )"
    card_tap_1 = make_label_btn_card_widget("TAP 1", "T1", blue)
    card_tap_2 = make_label_btn_card_widget("TAP 2", "T2", blue)
    card_tap_3 = make_label_btn_card_widget("TAP 3", "T3", blue)
    card_tap_4 = make_label_btn_card_widget("TAP 4", "T4", blue)
    card_cancel = make_label_btn_card_widget("CANCEL", "C", "red")

    layout.addWidget(lInstruction)
    layout.addWidget(card_tap_1)
    layout.addWidget(card_tap_2)
    layout.addWidget(card_tap_3)
    layout.addWidget(card_tap_4)
    layout.addWidget(card_cancel)


def create_dispensing_water_screen(layout, order):

    volume, tap = order.get_volume(), order.get_tap()

    font = QFont()
    font.setFamily(u"Arial")
    font.setBold(True)

    lInstruction1 = QLabel("lAns2")
    lInstruction1.setText(f"DISPENSING FROM TAP {tap}")
    lInstruction1.setAlignment(Qt.AlignCenter)
    lInstruction1.setFont(font)
    lInstruction1.setStyleSheet("font-size:36px;color:white;")

    card_lbl = QLabel(f"{volume} L")
    card_lbl.setAlignment(Qt.AlignCenter)
    card_lbl.setFont(font)
    card_lbl.setStyleSheet("font-size:36px;color:black;background-color:white;border-radius:50%;")
    card = QWidget()
    card_lay = QHBoxLayout()
    card_lay.addWidget(card_lbl)
    card_lay.setContentsMargins(153, 54, 153, 54)
    card.setLayout(card_lay)

    lAns5 = QLabel("lAns2")
    lAns5.setText(f"Thank you, {order.holder_name} !\nAvailable: Rs {order.available_balance} /-")
    lAns5.setAlignment(Qt.AlignCenter)
    lAns5.setFont(font)
    lAns5.setStyleSheet("font-size:27px;color:white;")

    layout.addWidget(lInstruction1)
    layout.addWidget(card)
    layout.addWidget(lAns5)

