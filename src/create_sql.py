import pickle

with open('./src/mysql_keywords.pickle','rb') as stopwords:
    mysql_keys = pickle.load(stopwords)
mysql_lower = [x.lower() for x in mysql_keys]
mysql_keys.extend(mysql_lower)

def generate_sql(json_data):
    col_list = []
    extra_tables = ""
    primary_key = get_primarykey(json_data)

    for element in json_data["elements"]:
        if element["etype"] =="checkbox":
            extra_tables += get_table(element,primary_key, json_data["name"])
        if element["etype"] == "multiselectlist":
            extra_tables += get_table(element,primary_key, json_data["name"])
        if element["etype"] in ['textbox','selectlist','radiobutton']:
            col_list.append(get_col(element))

    primary_col = construct_primary(primary_key)
    if primary_col:
        col_list.append("""primary key({})""".format(primary_col))

    general_table = """
                    create table {}(
                        {}
                    );
                    """.format(json_data["name"], ",".join(col_list))
    
    boiler_plate = """drop database if exists {user};
            create database {user};
            use {user};
            drop user if exists '{user}'@'localhost';
            CREATE USER '{user}'@'localhost' IDENTIFIED BY '{}';
            GRANT ALL PRIVILEGES ON * . * TO '{user}'@'localhost';
            flush privileges;
            SET FOREIGN_KEY_CHECKS = 0;
            SET GROUP_CONCAT_MAX_LEN=32768;
            SET @tables = NULL;
            SELECT GROUP_CONCAT('`', table_name, '`') INTO @tables
                FROM information_schema.tables
                WHERE table_schema = (SELECT DATABASE());
            SELECT IFNULL(@tables,'dummy') INTO @tables;
            SET @tables = CONCAT('DROP TABLE IF EXISTS ', @tables);
            PREPARE stmt FROM @tables;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            SET FOREIGN_KEY_CHECKS = 1;
            {}
            {}""".format(json_data["mysqlPWD"], general_table, extra_tables, user = json_data["mysqlUserID"])

    with open('./{}.sql'.format(json_data["name"]), 'w') as sql_file:
        sql_file.write(boiler_plate)

    


def get_col(element):
    datatype = "varchar(256)"
    if element.get("datatype") == "integer":
        datatype = "int"

    elif element.get("maxlength"):
        datatype = "varchar({})".format(element["maxlength"])

    required = ""
    if element.get("required") == "true":
        required = "not null"

    col_name = get_sql_col_name(element)
    return "{} {} {}".format(col_name,datatype,required)

def get_sql_col_name(element):
    col_name = element.get("ename")
    col_name = col_name.replace(" ","")
    if col_name in mysql_keys:
        col_name += '___123'
    return col_name

def get_primarykey(json_data):
    primary_key = []

    for element in json_data["elements"]:
        if element.get("key") and element.get("key") == "key":
            primary_key.append(element)

    return primary_key

def construct_primary(primary_key):
    if not len(primary_key):
        return
    
    col_names = []
    for element in primary_key:
        col_names.append(get_sql_col_name(element))
    return ','.join(col_names)


def get_table(element, primary_key, main_table_name):
    # create columns using primary key
    cols_list = []
    for primary_element in primary_key:
        cols_list.append(get_col(primary_element))
    # create column for the current element
    cols_list.append(get_col(element))
    # create a primary key constraint
    col_collection = construct_primary(primary_key)
    primary_constraint = """primary key({},{})""".format(col_collection,get_sql_col_name(element))
    cols_list.append(primary_constraint)
    # create a foreign key with reference
    foreign_constraint = """foreign key ({primary}) references {}({primary})""".format(main_table_name, primary = col_collection)
    cols_list.append(foreign_constraint)

    xtra_table = """
                 create table {}_{}({});
                 """.format(get_sql_col_name(element), main_table_name, ",".join(cols_list))

    return xtra_table





    
    
