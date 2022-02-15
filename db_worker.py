import peewee

database = peewee.SqliteDatabase("pdlc3.db")


class BaseTable(peewee.Model):
    # В подклассе Meta указываем подключение к той или иной базе данных
    class Meta:
        database = database


class Composition(BaseTable):
    name_composition = peewee.CharField()  # от типа столбца зависит тип данных, который мы сможем в него записать


class Membrane(BaseTable):
    composition = peewee.ForeignKeyField(Composition)
    diametr = peewee.CharField()


class Data(BaseTable):
    membrane = peewee.ForeignKeyField(Membrane)
    dirname = peewee.CharField()
    name = peewee.CharField()
    Edata = peewee.CharField()
    Udata = peewee.CharField()


class data_graph(BaseTable):
    datada = peewee.ForeignKeyField(Data)
    Edata = peewee.FloatField()
    Udata = peewee.FloatField()


# Создание таблиц:
if __name__ == "__main__":
    database.create_tables([Composition, Membrane, Data, data_graph])

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
        print(item)
    data_graph.insert_many(test).execute()
    # dddd=data.select().where(data.name=="izmerenie[0].split(os.path.sep)[-1]")
    dddd = Data.select().where(Data.dirname == "izmerenie[0]").count()
    print(dddd)
