"""Modo consola para probar ArduinoBot."""
from chatbot import ArduinoBot


def main() -> None:
    bot = ArduinoBot()
    print("ArduinoBot listo. Escribe una falla o 'salir' para terminar.\n")

    while True:
        user_message = input("Tú: ").strip()
        if user_message.lower() in {"salir", "exit", "adios", "fin"}:
            print("ArduinoBot: Listo, éxito con tu práctica.")
            break

        result = bot.answer(user_message)
        print(f"ArduinoBot: {result['response']}")
        if result["extra"]:
            print(f"Pista extra: {result['extra']}")
        print(f"[intención={result['intent']} | confianza={result['confidence']}]\n")


if __name__ == "__main__":
    main()
