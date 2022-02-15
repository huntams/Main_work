import peewee

database = peewee.SqliteDatabase("pdlc.db")


class BaseTable(peewee.Model):
    """
    Базовый класс для создания бд через ORM библиотеку
    """

    # В подклассе Meta указываем подключение к той или иной базе данных
    class Meta:
        database = database


# Чтобы создать таблицу в нашей БД, нам нужно создать класс
class Composition(BaseTable):
    """
    класс для созания таблицы состава плёнки
    """
    name_composition = peewee.CharField()  # от типа столбца зависит тип данных, который мы сможем в него записать


class Membrane(BaseTable):
    """
    класс для созания таблицы диаметра плёнки
    """
    composition = peewee.ForeignKeyField(Composition)
    diametr = peewee.CharField()


class Data(BaseTable):
    """
    класс для созания таблицы информации о плёнки
    """
    membrane = peewee.ForeignKeyField(Membrane)
    dirname = peewee.CharField()
    name = peewee.CharField()
    active = peewee.BooleanField()
    Emax = peewee.FloatField()
    Umax = peewee.FloatField()
    Uph_desc_step = peewee.FloatField()
    dTph_On = peewee.FloatField()
    dTph_Off = peewee.FloatField()
    dTph_max = peewee.FloatField()
    Uph_active = peewee.BooleanField()
    Uph_On = peewee.FloatField()
    Uph_Off = peewee.FloatField()


class DataGraph(BaseTable):
    data_index = peewee.ForeignKeyField(Data)
    Edata1 = peewee.FloatField()
    Edata2 = peewee.FloatField()
    Udata1 = peewee.FloatField()
    Udata2 = peewee.FloatField()


# Создание таблиц:
if __name__ == "__main__":
    database.create_tables([Composition, Membrane, Data, DataGraph])

    new_composition = Composition(name_composition="slovo")
    new_composition.save()
    new_membrane = Membrane(composition=new_composition,
                            diametr="233")
    all_data = Data.create(membrane=new_membrane.diametr, dirname="izmerenie[0]",
                           name="izmerenie[0].split(os.path.sep)[-1]", Edata=1,
                           Udata=1 + 1)
    test = []
    for item in range(100, 200):
        test.append({
            "datada": all_data,
            "Edata": item,
            "Udata": item + 1
        })
        # all = data_graph.create(datada=all_data, Edata=item, Udata=item + 1)
        # print(item)
    DataGraph.insert_many(test).execute()
    masss = []
    for data_h in DataGraph.select().where(DataGraph.Edata <= 159):
        print(data_h.Edata)
    # dddd=data.select().where(data.name=="izmerenie[0].split(os.path.sep)[-1]")
    # dddd = Data.select().where(Data.dirname == "izmerenie[0]").count()
    # print(dddd)
