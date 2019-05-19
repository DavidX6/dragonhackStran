import sqlite3
conn = sqlite3.connect('leaderboard.db')

c = conn.cursor()

# c.execute('''
#     CREATE TABLE Project (
#         word TEXT PRIMARY KEY NOT NULL,
#         gathered REAL DEFAULT 0,
#         address TEXT NOT NULL
#     );
# ''')

# c.execute('''
#     CREATE TABLE Balance (
#         address TEXT PRIMARY KEY NOT NULL,
#         balance REAL DEFAULT 0
#     );
# ''')

c.execute('''
    CREATE TABLE Tranzaction (
        from_address TEXT NOT NULL,
        to_address TEXT NOT NULL
    );
''')

# c.execute('''
#     CREATE TABLE UserProject (
#         user_address TEXT NOT NULL,
#         project_address TEXT NOT NULL,
#         PRIMARY KEY(user_address, project_address)
#     );
# ''')
#
# result = "2MsLZKCD5ZB457EmeZ8ZeXzfsYM1fKzyfYy"
# c.execute("INSERT INTO Balance VALUES (?, ?)", (result, 5000))


# c.execute('''
#     CREATE TABLE Posting (
#         word TEXT NOT NULL,
#         documentName TEXT NOT NULL,
#         frequency INTEGER NOT NULL,
#         indexes TEXT NOT NULL,
#         PRIMARY KEY(word, documentName),
#         FOREIGN KEY (word) REFERENCES IndexWord(word)
#     );
# ''')

# Save (commit) the changes
conn.commit()
conn.close()