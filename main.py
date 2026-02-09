from transcribe import parse_args, validate_inputs, build_output_path, transcribe_audio


def main():
    args = parse_args()

    audio_path = args.audio_path
    file_output = args.output
    model_name = args.model

    validate_inputs(audio_path)

    audio_transcript_path = build_output_path(file_output, audio_path)

    transcribe_audio(model_name, audio_path, audio_transcript_path)


if __name__ == "__main__":
    main()
