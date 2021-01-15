import sqlite3

conn = sqlite3.connect('settings.db')
c = conn.cursor()

'''
c.execute("""CREATE TABLE previous (
            nc_path text,
            as_path text,
            base text,
            tool text,
            rapid_speed integer,
            rapid_accuracy integer,
            line_speed integer,
            line_accuracy integer,
            circular_speed integer,
            circular_accuracy integer,
            options_speed bool,
            options_base bool
        )""")

conn.commit()

c.execute("""CREATE TABLE base (
            name text,
            coord text
        )""")

conn.commit()

c.execute("""CREATE TABLE tool (
            name text,
            coord text
        )""")

conn.commit()

conn.close()
'''


def insert(table, name, coord):
    with conn:
        c.execute(f"INSERT INTO {table} VALUES (:name, :coord)",
                  {'name': name, 'coord': coord})
    return None


def select(table, name, coord):
    c.execute(f"SELECT {coord} FROM {table} WHERE name=:name", {'name': name})
    return c.fetchone()[0]


def update(table, name, coord):
    c.execute(f"UPDATE {table} SET coord=:coord WHERE name=:name", {'name': name, 'coord': coord})
    return None


def remove(table, name):
    with conn:
        c.execute(f"DELETE from {table} WHERE name=:name", {'name': name})
    return None


def select_table(table):
    c.execute(f"SELECT * FROM {table}")
    return c.fetchall()[0]


def select_name(table):
    c.execute(f"SELECT name FROM {table}")
    return c.fetchall()


def update_previous(nc_path, as_path, base, tool, rapid_speed, rapid_accuracy, line_speed, line_accuracy,
                    circular_speed, circular_accuracy, options_speed, options_base):
    with conn:
        c.execute("""UPDATE previous SET
                                nc_path=:nc_path,
                                as_path=:as_path,
                                base=:base,
                                tool=:tool,
                                rapid_speed=:rapid_speed,
                                rapid_accuracy=:rapid_accuracy,
                                line_speed=:line_speed,
                                line_accuracy=:line_accuracy,
                                circular_speed=:circular_speed,
                                circular_accuracy=:circular_accuracy,
                                options_speed=:options_speed,
                                options_base=:options_base""",
                  {'nc_path': nc_path, 'as_path': as_path, 'base': base, 'tool': tool, 'rapid_speed': rapid_speed,
                   'rapid_accuracy': rapid_accuracy, 'line_speed': line_speed, 'line_accuracy': line_accuracy,
                   'circular_speed': circular_speed, 'circular_accuracy': circular_accuracy,
                   'options_speed': options_speed, 'options_base': options_base})
    return None


def insert_previous(nc_path, as_path, base, tool, rapid_speed, rapid_accuracy, line_speed, line_accuracy,
                    circular_speed, circular_accuracy, options_speed, options_base):
    with conn:
        c.execute("""INSERT INTO previous VALUES (:nc_path, :as_path, :base, :tool, :rapid_speed, :rapid_accuracy, 
                    :line_speed, :line_accuracy, :circular_speed, :circular_accuracy, :options_speed, :options_base)""",
                  {'nc_path': nc_path, 'as_path': as_path, 'base': base, 'tool': tool, 'rapid_speed': rapid_speed,
                   'rapid_accuracy': rapid_accuracy, 'line_speed': line_speed, 'line_accuracy': line_accuracy,
                   'circular_speed': circular_speed, 'circular_accuracy': circular_accuracy,
                   'options_speed': options_speed, 'options_base': options_base})
    return None


if __name__ == '__main__':
    '''insert('base', 'mojabaza1', '(0,0,0,0,0,0)')
    insert('base', 'mojabaza2', '(0,0,222,0,0,0)')
    insert('base', 'mojabaza3', '(0,0,333,0,0,0)')
    insert('base', 'mojabaza5', '(0,333,211122,2341234adsf,0,0)')
    insert('base', 'mojabaza4', '(4,4,222,4,0,0)')
    print(select('base', 'mojabaza1', 'coord')[0])
    print(select('base', 'mojabaza2', 'coord')[0])
    print(select('base', 'mojabaza3', 'coord')[0])
    print(select('base', 'mojabaza4', 'coord')[0])
    print(select('base', 'mojabaza5', 'coord')[0])
    insert('tool', 'tool1', '(4,4,212,4,0,123)')
    insert('tool', 'tool2', '(3,54,262,4,0fff)')
    print(select('tool', 'tool1', 'coord')[0])
    print(select('tool', 'tool2', 'coord')[0])
    insert_previous('a1b', 'a2c', 'a3d', 'a4e', 'afg', 'a6h', 'a7j', 'a8k', 'a9q', 'a10w', 'a11e', 'a12r')
    print(select_table('previous')[0])
    update_previous('a1b', 'a2c', 'a3d', 'a4e', 'afg', 'a6h', 'a7j', 'a8k', 'a9q', 'a10w', 'a11e', 'a12r')
    print(select_table('previous')[0])
    update_previous('a1db', 'a213c', 'a3d', 'a46e', 'afg', 'a6h', 'a7j', 'a813k', 'a9q', 'a10w', 'a11e', 'a12r')
    print(select_table('previous')[0])
    update_previous('a1b', 'a2c', 'a3d', 'a4e', 'afg', 'a6h', 'a7j', 'a8k', 'a98q', 'a1hhhhh0w', 'a11e', 'a12r')
    print(select_table('previous')[0])
    print('--------- ------------ ------------ --------')'''
    update('base', 'mojabaza1', '0')
    remove('base', 'asdf')
    update_previous('', '', '(0, 0, 0, 0, 0, 0)', '(0, 0, 0, 0, 0, 0)', '100', '100', '100', '100', '100', '100', 1, 0)
    print(select_table('tool'))
    print(select_table('base'))
    print(select_table('previous'))
    print(select('base', 'mojabaza1', 'coord'))
    print(select_name('tool'))
    print(select_name('base'))
    conn.close()
