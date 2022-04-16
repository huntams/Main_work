"""
@authors: Maksim & Konstantin
"""
from threading import Thread

from db_worker import database, Composition, Membrane, Data, DataGraph
import csv
import matplotlib.pyplot as plt
import os
import openpyxl

alldata = []
emaxlist = []
csvlist = []
default_test_dir = r'D:\диплом\Test PDLC\1_Al2O3_281014 _3 d=35mn'  # D:\диплом\Test PDLC\1_Al2O3_281014 _3 d=35mn


class ThrThr(Thread):
    def __init__(self, name, thickness):
        super(ThrThr, self).__init__()
        self.name = name
        self.thickness = thickness

    def split(self, list):
        return list[::2], list[1::2]

    def run(self):
        mas = self.split(csvlist)
        if self.name == 'first':
            listslovarey(csvlist=mas[0])
        else:
            listslovarey(csvlist=mas[1])


def treewalker(plenka_dir_name):
    """
        Просматривает дирректории и ищет файлы данных
    """
    # Создание таблиц:
    database.create_tables([Composition,
                            Membrane,
                            Data,
                            DataGraph])
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


def listslovarey(csvlist=csvlist, thickness=1.0):
    """
    Словари.
    """
    # Запись информации в таблицу состава
    new_composition = Composition(name_composition=csvlist[0][0].split(os.path.sep)[-2])
    new_composition.save()
    # Запись информации в таблицу плёнки
    new_membrane = Membrane(composition=new_composition,
                            diametr=csvlist[0][0].split(os.path.sep)[-2][
                                    csvlist[0][0].split(os.path.sep)[-2].find("=") + 1:])
    new_membrane.save()
    for izmerenie in csvlist:
        if Data.select().where(Data.name == izmerenie[0].split(os.path.sep)[-1]).count() == 0:

            namedata = {}
            namedata["Edata"] = chtenieField(os.path.join(izmerenie[0], izmerenie[1][0]), thickness)
            namedata["Udata"] = chteniePhoto(os.path.join(izmerenie[0], izmerenie[1][1]), thickness)
            namedata["Emax"] = max(namedata["Edata"][1])
            namedata["Umax"] = max(namedata["Udata"][1])
            namedata["Timp_start"], namedata["Timp_stop"], namedata["dTimp"] = timpStartStop(namedata)  # [2]
            namedata["Uph_desc_step"] = descritizationSTEP(namedata["Udata"][1])
            print("work")
            namedata["Tph_On"], namedata["Tph_Off"], namedata["Uph_On"], namedata["Uph_Off"] = tphOnOff(namedata)
            if ((namedata["Umax"] - min(namedata["Udata"][1])) / namedata["Uph_desc_step"]) < 10 or namedata[
                "Tph_Off"] - namedata["Timp_stop"] <= 0:
                # Запись общей информации плёнки
                all_data = Data.create(membrane=new_membrane, dirname=izmerenie[0],
                                       name=izmerenie[0].split(os.path.sep)[-1],
                                       active=False,
                                       Emax=max(namedata["Edata"][1]),
                                       Umax=max(namedata["Udata"][1]),
                                       Uph_desc_step=descritizationSTEP(namedata["Udata"][1]),
                                       dTph_On=namedata["dTimp"],
                                       dTimp=namedata["dTimp"],
                                       dTph_Off=0,
                                       dTph_max=0,
                                       Uph_active=False,
                                       Uph_On=0,
                                       Uph_Off=0
                                       )
            else:
                # Запись общей информации плёнки
                all_data = Data.create(membrane=new_membrane, dirname=izmerenie[0],
                                       name=izmerenie[0].split(os.path.sep)[-1],
                                       active=True,
                                       Emax=max(namedata["Edata"][1]),
                                       Umax=max(namedata["Udata"][1]),
                                       Uph_desc_step=descritizationSTEP(namedata["Udata"][1]),
                                       dTph_On=namedata["Tph_On"] - namedata["Timp_start"],
                                       dTimp=namedata["dTimp"],
                                       dTph_Off=namedata["Tph_Off"] - namedata["Timp_stop"],
                                       dTph_max=namedata["Timp_stop"] - namedata["Tph_On"],
                                       Uph_active=True,
                                       Uph_On=namedata["Uph_On"],
                                       Uph_Off=namedata["Uph_Off"]
                                       )
            # Запись Edata и Udata в таблицу
            items_data = []
            switch = 1
            for index in range(0, len(namedata["Edata"][0])):
                if switch % 10 == 0:
                    items_data.append({
                        "index": all_data.dirname,
                        "Edata1": namedata["Edata"][0][index],
                        "Edata2": namedata["Edata"][1][index],
                        "Udata1": namedata["Udata"][0][index],
                        "Udata2": namedata["Udata"][1][index]
                    })
                    switch = 1
                else:
                    switch += 1
            DataGraph.insert_many(items_data).execute()
            alldata.append(namedata)


def timpStartStop(dataDict):
    """
    Нахождение точек времени начаола и конца импульса управляющего поля.

    """

    tlist = dataDict["Edata"][0]
    vlist = dataDict["Edata"][1]
    Espec = 0.5 * dataDict["Emax"]
    trigger = 0
    Tstart = 0
    Tstop = 0
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
    if len(TlistHigh) == 0 and len(UlistHigh) == 0:
        t_On = 0
        v_on = 0
    else:
        t_On = sum(TlistHigh) / len(TlistHigh)
        v_on = sum(UlistHigh) / len(UlistHigh)
    if len(TlistLow) == 0 and len(UlistLow) == 0:
        v_off = 0
        t_Off = 0
    else:
        v_off = sum(UlistLow) / len(UlistLow)
        t_Off = sum(TlistLow) / len(TlistLow)
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


def otrisovkagraf_mod():
    """
    Отрисовка графиков через использование данных
    загруженных в лист словарей

    """
    tlist1, tlist2, vlist1, vlist2 = [], [], [], []
    fig_all = plt.figure(1, tight_layout=True)
    ax_f = fig_all.subplots()
    ax_c = ax_f.twinx()
    for BD_data in Data.select():
        if BD_data.active:
            fig_one = plt.figure(2, tight_layout=True)
            fig_one.clf()
            ax_f1 = fig_one.subplots()
            ax_c1 = ax_f1.twinx()
            print("time1")
            for BD_item in DataGraph.select().where(DataGraph.index == BD_data.dirname):
                tlist1.append(BD_item.Edata1)
                vlist1.append(BD_item.Edata2)
                tlist2.append(BD_item.Udata1)
                vlist2.append(BD_item.Udata2)
            print("time2")
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
            # Отрисовка там где возможно точки включения и выключения
            if BD_data.Uph_active:
                ax_c1.plot(BD_data.dTph_On, BD_data.Uph_On, 'ob')
                ax_c1.plot(BD_data.dTph_Off, BD_data.Uph_Off, 'ob')
                ax_c.plot(BD_data.dTph_On, BD_data.Uph_On, 'ob')
                ax_c.plot(BD_data.dTph_Off, BD_data.Uph_Off, 'ob')
            print(BD_data.name)
            print(' -- ploted')
        else:
            print(BD_data.name)
            print(' -- NOT ploted')
        plt.show()

def plot_time_proc(DataClass=Data):
    """
    График времен срабатывания от поля

    """
    Emax_list = []
    dt_on_list = []
    dt_off_list = []
    dt_max_list = []
    for BD_data in DataClass.select():
        if BD_data.active:
            Emax_list.append(BD_data.Emax)
            dt_on_list.append(BD_data.dTph_On)
            dt_off_list.append(BD_data.dTph_Off)
            dt_max_list.append(BD_data.dTph_max)
    fig_time = plt.figure(3, tight_layout=True)
    plt.subplot(2, 1, 1)
    plt.plot(Emax_list, dt_on_list, 'r.-', label='t_on')
    plt.plot(Emax_list, dt_off_list, 'b.-', label='t_off')
    plt.plot(Emax_list, dt_max_list, 'g.-', label='t_work')
    plt.xlabel("Управляющее поле, В/мкм")
    plt.ylabel("Время, мс")
    plt.legend()
    plt.show()


def plot_transpare_proc(DataClass=Data):
    """
    График прозрачности от поля

    """
    Emax_list = []
    Uph_ampl_list = []
    for BD_data in DataClass.select():
        if BD_data.active:
            Emax_list.append(BD_data.Emax)
            Uph_ampl_list.append(BD_data.Umax)
    fig_time = plt.figure(3, tight_layout=True)
    plt.subplot(2, 1, 2)
    plt.plot(Emax_list, Uph_ampl_list, 'k.-', label='UphMAX')
    plt.xlabel("Управляющее поле, В/мкм")
    plt.ylabel("Прозрачность, В")
    plt.legend()
    plt.show()


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
        treewalker(aim_dir)  # r'D:\диплом\Test PDLC\1_Al2O3_281014 _3 d=35mn')
    if load_type == 0:
        print("alone mesure load ___")
        print(aim_dir)
        alone_mesure(aim_dir)
    threads = [ThrThr(name='first', thickness=thickness), ThrThr(name='second', thickness=thickness)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    csvlist.clear()


if __name__ == "__main__":
    treewalker(
        default_test_dir)  # просмотр указанной директории с заполнением списка файлив и директорий единичных измерений
    threads = [ThrThr(name='first'), ThrThr(name='second')]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    # listslovarey()  # загрузка на основе списка единичных измерений в форме словарей включая определение времён
    # otrisovkagraf_mod()  # отрисовка списка словарей единичных измерений
    plot_time_proc()
    plot_transpare_proc()
