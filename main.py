import chess
import chess.engine
import speech_recognition as sr
import pyttsx3

# STOCKFISH YOLU
STOCKFISH_PATH = r"stockfish\stockfish-windows-x86-64-avx2.exe"
# Linux örnek:
# "/usr/games/stockfish"

engine = pyttsx3.init()
engine.setProperty("rate", 170)

tahta = chess.Board()

motor = chess.engine.SimpleEngine.popen_uci(
    STOCKFISH_PATH
)

r = sr.Recognizer()

tas = {
    "knight": "N",
    "bishop": "B",
    "rook": "R",
    "queen": "Q",
    "king": "K"
}



def konus(text):
    print("BOT:", text)
    engine.say(text)
    engine.runAndWait()


def dinle():

    with sr.Microphone() as source:

        print("\nSay your move:")

        r.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        audio = r.listen(source)

    try:

        txt = r.recognize_google(
            audio,
            language="en-EN"
        )

        print("You:", txt)

        return txt.lower()

    except:

        return ""


def san_cevir(text):

    text = text.lower()

    if text in ["short castling"]:
        return "O-O"

    if text in ["long castling"]:
        return "O-O-O"

    k = text.split()

    if len(k) == 2:

        if k[0] in tas:

            return tas[k[0]] + k[1]

    return text


konus("Stockfish chess started. Let's play!")

while not tahta.is_game_over():

    print("\n")
    print(tahta)

    # OYUNCU
    hamle = dinle()

    if not hamle:
        continue

    try:

        tahta.push_san(
            san_cevir(hamle)
        )

    except:

        konus("Invalid move")
        continue

    if tahta.is_game_over():
        break

    # STOCKFISH
    sonuc = motor.play(
        tahta,
        chess.engine.Limit(
            time=0.5
        )
    )

    san = tahta.san(
        sonuc.move
    )

    tahta.push(
        sonuc.move
    )

    konus(
        "I played " + san
    )

print(
    "Result:",
    tahta.result()
)

konus(
    "Game over"
)


motor.quit()
