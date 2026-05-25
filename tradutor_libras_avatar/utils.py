import speech_recognition as sr
from io import BytesIO

def transcrever_audio(audio_file):
    """Transcreve um arquivo de áudio usando o recognizer do SpeechRecognition.

    Mantém compatibilidade com diversos formatos tentando fallback via pydub.
    """
    r = sr.Recognizer()
    try:
        # AudioFile aceita file-like objects
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='pt-BR')
        return text
    except sr.UnknownValueError:
        return "Não consegui compreender o áudio. Por favor, tente falar mais claro."
    except sr.RequestError as e:
        return f"Erro na conexão com o serviço de transcrição: {e}"
    except Exception:
        # Tentativa de fallback usando pydub para converter formatos
        try:
            audio_file.seek(0)
            from pydub import AudioSegment
            audio_segment = AudioSegment.from_file(audio_file)
            wav_buffer = BytesIO()
            audio_segment.export(wav_buffer, format="wav")
            wav_buffer.seek(0)
            with sr.AudioFile(wav_buffer) as source:
                audio_data = r.record(source)
            return r.recognize_google(audio_data, language='pt-BR')
        except Exception as e2:
            return f"Erro no processamento do áudio: {str(e2)}"
