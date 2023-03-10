import random
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect("words.db")
c = conn.cursor()

# Crear tabla si no existe
c.execute('''CREATE TABLE IF NOT EXISTS words
             (english text, spanish text, meanings text, is_regular integer, simple_present_3sg text, negative_form text)''')
conn.commit()

# Función para agregar una palabra a la base de datos
def add_word():
    english = input("Ingresa la palabra en inglés: ")
    spanish = input("Ingresa la palabra en español: ")
    meanings = input("Ingresa los significados en inglés separados por comas: ")
    is_regular = input("Es la palabra regular en tiempo simple? (s/n) ")
    if is_regular.lower() == "s":
        simple_present_3sg = input("Ingresa la forma en tercera persona singular del tiempo simple: ")
    else:
        simple_present_3sg = None
    negative_form = input("Cómo se forma la forma negativa? ")
    # Insertar la palabra en la base de datos
    c.execute("INSERT INTO words VALUES (?, ?, ?, ?, ?, ?)", (english, spanish, meanings, is_regular.lower() == "s", simple_present_3sg, negative_form))
    conn.commit()
    print("La palabra ha sido agregada.")

# Función para hacer una pregunta al jugador
def ask_question():
    # Seleccionar una palabra al azar de la base de datos
    c.execute("SELECT * FROM words ORDER BY RANDOM() LIMIT 1")
    row = c.fetchone()
    english_word = row[0]
    spanish_word = row[1]
    meanings = row[2].split(",")
    is_regular = row[3]
    simple_present_3sg = row[4]
    negative_form = row[5]
    # Seleccionar un significado al azar
    meaning = random.choice(meanings)
    # Mostrar información adicional sobre la palabra
    if is_regular:
        print("Esta palabra es regular en tiempo simple.")
        print("La forma en tercera persona singular del tiempo simple es", simple_present_3sg + ".")
    else:
        print("Esta palabra es irregular en tiempo simple.")
    print("Para formar la forma negativa, se agrega", negative_form, "antes del verbo.")
    # Hacer la pregunta y esperar la respuesta del jugador
    print("¿Cuál es el significado de", english_word + "?")
    for i, option in enumerate(meanings):
        print(i + 1, option)
    answer = int(input("Selecciona una opción: "))
    # Verificar si la respuesta es correcta
    if meanings[answer - 1].strip().lower() == meaning.strip().lower():
        print("¡Correcto!")
        return True
    else:
        print("Incorrecto. La respuesta correcta es", meaning.strip() + ".")
# Función para comenzar el juego
def start_game():
    print("¡Bienvenido al juego de vocabulario!")
    while True:
        choice = input("Presiona 'a' para agregar una palabra, 'j' para jugar o 's' para salir: ")
        if choice == "a":
            add_word()
        elif choice == "j":
            score = 0
            num_questions = 0
            while True:
                if ask_question():
                    score += 1
                num_questions += 1
                choice = input("Presiona 'c' para continuar o 's' para salir: ")
                if choice == "s":
                    break
            print("Juego terminado. Puntaje:", score, "de", num_questions)
        elif choice == "s":
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

# Comenzar el juego
start_game()

# Cerrar la conexión a la base de datos
conn.close()

