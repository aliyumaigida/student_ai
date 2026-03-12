
from memory import Memory
from agent import generate_question, evaluate_conversation
from orders import record_audio, transcribe_audio, speak
def run_agent():

    topic = input("Enter topic: ")

    memory = Memory()

    print("\nAI tutor started...\n")

    while True:

        question, end_session = generate_question(
            topic,
            memory.get_history()
        )

        if end_session == "YES":

            print("\nAI: I believe we have explored this topic sufficiently.\n")
            speak("I believe we have explored this topic sufficiently")

            results = evaluate_conversation(
                topic,
                memory.get_history()
            )

            print("Final Evaluation\n")
            speak("Final Evaluation\n")

            for k, v in results.items():
                print(f"{k}: {v}")
                speak(f"{k}: {v}")

            break

        print("\nAI:", question)

        # AI speaks the question
        speak(question)

        print("\nChoose input method:")
        print("1 - Type answer")
        print("2 - Voice answer")

        choice = input("Select option: ")

        if choice == "2":

            audio_file = record_audio()

            answer = transcribe_audio(audio_file)

        else:

            answer = input("You: ")

        memory.add(question, answer)

    print("\nSession complete.")
    speak("\nSession complete.")


if __name__ == "__main__":
    run_agent()

