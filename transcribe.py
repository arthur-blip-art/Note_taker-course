import argparse
import os
import whisper
from pathlib import Path
from platformdirs import user_data_dir
import subprocess


def parse_args():
    
    parser = argparse.ArgumentParser(
    description="Transcrit un fichier audio en texte avec le modèle Whisper"
    )
    parser.add_argument(
    "audio_path",help="Chemin vers le fichier audio à trancrire"
    )
    parser.add_argument(
    "--output",default="transcripts",
    help="Dossier dans lequel je veux que mes transcripts sont stockés"
    )
    parser.add_argument(
    "--model",default="base",
    choices=["tiny","base", "small", "medium"],
    help="Modèle whisper à utiliser (tiny, base, medium,...)")
    
    args=parser.parse_args()
    return args


def validate_inputs(audio_path):
    
    if not os.path.exists(audio_path):
        print (f"le fichier existe pas")
        raise SystemExit(1)
    if not os.path.isfile(audio_path):
        print(f"le fichier est un dossier")
        raise SystemExit(1)
    print (f"transcription en cours")
    return

def build_output_path(file_output, audio_path):

    base_dir = Path(user_data_dir("note-taker")) / file_output
    base_dir.mkdir(parents=True, exist_ok=True)

    audio_transcript_name=os.path.basename(audio_path)
    audio_transcript_name=os.path.splitext(audio_transcript_name)[0]
    audio_transcript_name=audio_transcript_name+"_transcript.txt"

    return base_dir/ audio_transcript_name


def transcribe_audio(model_name, audio_path, audio_transcript_path):

    try:
        print("Chargement du modèle")
        model=whisper.load_model(model_name, device="cpu")
        result=model.transcribe(audio_path)
        result_text=result["text"]
        print("Transcription en cours…")
        with open(audio_transcript_path, "w", encoding="UTF-8") as f:
            f.write(result_text)

    except Exception as e: 
        print(f"Impossible de transcrire ce fichier (format non supporté ou audio corrompu)")
        print(f"Détails: {e}")
        raise SystemExit(1)

    print(f"transcription réussie")
    
    subprocess.run(["open",audio_transcript_path])

    return
