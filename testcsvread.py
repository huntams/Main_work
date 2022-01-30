"""
@authors: Maksim & Konstantin
"""

import csv
import matplotlib.pyplot as plt
import os
import openpyxl

alldata = []
emaxlist = []
csvlist = []
default_test_dir = r'F:\ДИПЛОМ\PDLS READER\Test PDLC\1%Al2O3_281014 _3 d=35mn'  # F:\ДИПЛОМ\Test PDLC\1%Al2O3_281014 _3 d=35mn'


def treewalker(plenka_dir_name):
    """
        Просматривает дирректории и ищет файлы данных
    """
    tree = os.walk(plenka_dir_name)  # r'C:\Users\andri\Desktop\ДИПЛОМ\Test PDLC\1%Al2O3_281014 _3 d=35mn')
    kluch = False  # нужен для отсечения первого элемента кортежа
    for i in tree:
        if kluch:
            # Выделяет список имён вложенных файлов
            files = i[2]
            # Добавляет в список измерений ['адрес_папки',['имя_канал1.CSV','имя_канал2.CSV']]
            csvlist.append([os.path.abspath(i[0]), [x for x in files if x.endswith('.CSV')]])
        else:
            kluch = True
    print(csvlist)


def alone_mesure(plenka_dir_name):
    """
    
    """
    tree = os.walk(plenka_dir_name)  # r'C:\Users\andri\Desktop\ДИПЛОМ\Test PDLC\1%Al2O3_281014 _3 d=35mn')
    kluch = True  # нужен для отсечения первого элемента кортежа
    for i in tree:
        if kluch:
            # Выделяет список имён вложенных файлов
            files = i[2]
            # Добавляет в список измерений ['адрес_папки',['имя_канал1.CSV','имя_канал2.CSV']]
            csvlist.append([os.path.abspath(i[0]), [x for x in files if x.endswith('.CSV')]])
            kluch = False
    print(csvlist)


def chtenieField(namefile, thickness=1.0):
    """
    name file - полное название .csv файла (+путь к нему)
    Функция возвращает лист со значением времени и лист со значением напряжения
    """
    tlist = []
    vlist = []
    with open(namefile) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for line in reader:
            tlist.append(float(line[3]) * 1000)
            vlist.append(float(line[4]) / thickness)
    return tlist, vlist


def chteniePhoto(namefile, thickness=30.0):
    """
    name file - полное название .csv файла (+путь к нему)
    Функция возвращает лист со значением времени и лист со значением напряжения
    """
    import numpy as np
    tlist = []
    vlist = []
    with open(namefile) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for line in reader:
            tlist.append(float(line[3]) * 1000)
            vlist.append(float(line[4]))  # *np.exp(30.0/thickness))
            # G_otk_norm = np.log(abs(float(line[4])))/thickness # определение коэффициента ослабления плёнки math.
            # vlist.append(np.exp(G_otk_norm*30.0)) #сигнал при нормальной толщине 30
    return tlist, vlist


def listslovarey(thickness=1.0):
    """
    Словари.
    """
    for izmerenie in csvlist:
        namedata = {}
        namedata["activ"] = True  # False
        namedata["dirname"] = izmerenie[0]
        namedata["name"] = izmerenie[0].split(os.path.sep)[-1]

        namedata["Edata"] = chtenieField(os.path.join(izmerenie[0], izmerenie[1][0]), thickness)
        namedata["Udata"] = chteniePhoto(os.path.join(izmerenie[0], izmerenie[1][1]), thickness)
        namedata["Emax"] = max(namedata["Edata"][1])
        namedata["Umax"] = max(namedata["Udata"][1])
        namedata["Timp_start"], namedata["Timp_stop"], namedata["dTimp"] = timpStartStop(namedata)  # [2]
        namedata["Uph_desc_step"] = descritizationSTEP(namedata["Udata"][1])
        if ((namedata["Umax"] - min(namedata["Udata"][1])) / namedata["Uph_desc_step"]) < 10:
            namedata["Uph_activ"] = False
            namedata["activ"] = False
            namedata["dTph_On"] = namedata["dTimp"]
            namedata["dTph_Off"] = 0.0
            namedata["dTph_max"] = 0.0
        else:
            namedata["Uph_activ"] = True
            namedata["Tph_On"], namedata["Tph_Off"], namedata["Uph_On"], namedata["Uph_Off"] = tphOnOff(namedata)
            namedata["dTph_On"] = namedata["Tph_On"] - namedata["Timp_start"]
            namedata["dTph_Off"] = namedata["Tph_Off"] - namedata["Timp_stop"]
            namedata["dTph_max"] = namedata["Timp_stop"] - namedata["Tph_On"]

        alldata.append(namedata)


def timpStartStop(dataDict):
    """
    Нахождение точек времени начаола и конца импульса управляющего поля.

    """

    tlist = dataDict["Edata"][0]
    vlist = dataDict["Edata"][1]
    Espec = 0.5 * dataDict["Emax"]
    trigger = 0
    for i, v in enumerate(vlist):
        if v > Espec and trigger == 0:
            Tstart = i
            trigger = 1
        if v < Espec and trigger == 1:
            Tstop = i
            trigger = 2

    return tlist[Tstart], tlist[Tstop], (tlist[Tstop] - tlist[Tstart])


def tphOnOff(dataDict):
    """
    Нахождение времён срабатывания имульса управляющего поля.

    """

    tlist = dataDict["Udata"][0]
    vlist = dataDict["Udata"][1]
    U_step = descritizationSTEP(vlist)
    Amplitude = max(vlist) - min(vlist)
    UspecLow = [0.1 * Amplitude - 1.5 * U_step, 0.1 * Amplitude + 1.5 * U_step]
    UspecHigh = [0.9 * Amplitude - 1.5 * U_step, 0.9 * Amplitude + 1.5 * U_step]

    UlistLow = []
    TlistLow = []
    UlistHigh = []
    TlistHigh = []
    for i in range(len(vlist)):
        if vlist[i] > UspecLow[0] and vlist[i] < UspecLow[1] and tlist[i] > dataDict["Timp_stop"]:
            UlistLow.append(vlist[i])
            TlistLow.append(tlist[i])
        if vlist[i] > UspecHigh[0] and vlist[i] < UspecHigh[1] and tlist[i] < dataDict["Timp_stop"]:
            UlistHigh.append(vlist[i])
            TlistHigh.append(tlist[i])
    t_On = sum(TlistHigh) / len(TlistHigh)
    t_Off = sum(TlistLow) / len(TlistLow)
    v_on = sum(UlistHigh) / len(UlistHigh)
    v_off = sum(UlistLow) / len(UlistLow)
    return t_On, t_Off, v_on, v_off


def descritizationSTEP(datalist):
    """
    Определение шага дискретизации
    """
    min_step = abs(max(datalist))
    for i in range(len(datalist) - 1):
        elem_Delta = abs(datalist[i + 1] - datalist[i])
        if elem_Delta > 0.0 and elem_Delta < min_step:
            min_step = elem_Delta
    return min_step


def otrisovkagraf_mod(dataDict_list=alldata):
    """
    Отрисовка графиков через использование данных
    загруженных в лист словарей

    """
    fig_all = plt.figure(1, tight_layout=True)
    ax_f = fig_all.subplots()
    ax_c = ax_f.twinx()
    print(dataDict_list)
    for izmer_dict in dataDict_list:
        if izmer_dict["activ"]:
            fig_one = plt.figure(2, tight_layout=True)
            fig_one.clf()
            ax_f1 = fig_one.subplots()
            ax_c1 = ax_f1.twinx()
            tlist1, vlist1 = izmer_dict["Edata"]
            tlist2, vlist2 = izmer_dict["Udata"]
            ax_f.plot(tlist1, vlist1, 'r')
            ax_f.set_xlabel("Время, мс")
            ax_f.set_ylabel("Поле, В/мкм")
            ax_c.plot(tlist2, vlist2, 'g')
            ax_c.set_ylabel("Фотоотклик, В")
            ax_f1.plot(tlist1, vlist1, 'r')
            ax_f1.set_xlabel("Время, мс")
            ax_f1.set_ylabel("Поле, В/мкм")
            ax_c1.plot(tlist2, vlist2, 'g')
            ax_c1.set_ylabel("Фотоотклик, В")
            ### Отрисовка там где возможно точки включения и выключения
            if izmer_dict["Uph_activ"]:
                ax_c1.plot(izmer_dict["Tph_On"], izmer_dict["Uph_On"], 'ob')
                ax_c1.plot(izmer_dict["Tph_Off"], izmer_dict["Uph_Off"], 'ob')
                ax_c.plot(izmer_dict["Tph_On"], izmer_dict["Uph_On"], 'ob')
                ax_c.plot(izmer_dict["Tph_Off"], izmer_dict["Uph_Off"], 'ob')

            print(izmer_dict["name"])
            print(' -- ploted')

        else:
            print(izmer_dict["name"])
            print(' -- NOT ploted')


def plot_time_proc(dataDict_list=alldata):
    """
    График времен срабатывания от поля

    """
    Emax_list = []
    dt_on_list = []
    dt_off_list = []
    dt_max_list = []
    for izmer_dict in dataDict_list:
        if izmer_dict["activ"]:
            Emax_list.append(izmer_dict["Emax"])
            dt_on_list.append(izmer_dict["dTph_On"])
            dt_off_list.append(izmer_dict["dTph_Off"])
            dt_max_list.append(izmer_dict["dTph_max"])
    fig_time = plt.figure(3, tight_layout=True)
    plt.subplot(2, 1, 1)
    plt.plot(Emax_list, dt_on_list, 'r.-', label='t_on')
    plt.plot(Emax_list, dt_off_list, 'b.-', label='t_off')
    plt.plot(Emax_list, dt_max_list, 'g.-', label='t_work')
    plt.xlabel("Управляющее поле, В/мкм")
    plt.ylabel("Время, мс")
    plt.legend()


def plot_transpare_proc(dataDict_list=alldata):
    """
    График прозрачности от поля

    """
    Emax_list = []
    Uph_ampl_list = []
    for izmer_dict in dataDict_list:
        if izmer_dict["activ"]:
            Emax_list.append(izmer_dict["Emax"])
            Uph_ampl_list.append(izmer_dict["Umax"])
    fig_time = plt.figure(3, tight_layout=True)
    plt.subplot(2, 1, 2)
    plt.plot(Emax_list, Uph_ampl_list, 'k.-', label='UphMAX')
    plt.xlabel("Управляющее поле, В/мкм")
    plt.ylabel("Прозпачность, В")
    plt.legend()


def zapisyVtablici():
    """
    
    """
    book = openpyxl.Workbook()
    sheet = book.active

    """
    запись максимального значения напряжения в xl файл (название дирректории, два значения)
    """
    for i, val in enumerate(emaxlist):
        sheet.cell(row=(i + 1), column=1).value = val[0]
        sheet.cell(row=(i + 1), column=2).value = val[1]
        sheet.cell(row=(i + 1), column=3).value = val[2]

    book.save("UmaxLIST.xlsx")
    book.close()


def fulldirload(aim_dir=default_test_dir, load_type=1, thickness=10.0):
    """
    Функция берёт дирректорию, в которой лежат данные, потом ищет в ней все csv файлы, потом отрисовывает
    """
    if load_type == 2:
        print("group of layers load ___")
        print("NOT AVAILABLE")
        # treewalker (aim_dir)
    if load_type == 1:
        print("one layer load ___")
        print(aim_dir)
        treewalker(aim_dir)  # r'G:\Download\STUDY\ДИПЛОМ\Test PDLC\1%Al2O3_281014 _3 d=35mn')
    if load_type == 0:
        print("alone mesure load ___")
        print(aim_dir)
        alone_mesure(aim_dir)

    listslovarey(thickness)
    csvlist.clear()


if __name__ == "__main__":
    treewalker(
        default_test_dir)  # просмотр указанной директории с заполнением списка файлив и директорий единичных измерений
    listslovarey()  # загрузка на основе списка единичных измерений в форме словарей включая определение времён
    otrisovkagraf_mod()  # отрисовка списка словарей единичных измерений
    plot_time_proc()
    plot_transpare_proc()
