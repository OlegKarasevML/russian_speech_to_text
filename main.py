###User interaction###
from pathlib import Path
import argparse

###Video to text lib###
import whisper

###Format fixing###
from pydub import AudioSegment
import codecs

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files_path',
                        default=None, help='Path to files that will be transcribed',
                        required=False, type=Path)
    parser.add_argument('-o', '--output_path',
                        help='Path to ',
                        type=Path, default=None, required=False)
    args = parser.parse_args()
    return args

def prepare_files(path_to_files: Path):
    
    files = [x for x in path_to_files.glob('*') if x.is_file()] 
    for file in files:
        if file.suffix[1:] != 'wav':
            sound = AudioSegment.from_file(file, format=file.suffix[1:])
            file_handle = sound.export(path_to_files / f'{file.stem}.wav', format='wav')
            # (path_to_files / file).unlink(missing_ok=True)
    updated_files = [x for x in path_to_files.glob('*.wav') if x.is_file()] 
    return updated_files


def main():
    args = parse_args()
    model = whisper.load_model("turbo")

    paths = prepare_files(args.files_path)
    for path in paths:
        result = model.transcribe((args.files_path / path).as_posix())
        text = result['text']
        sentences = text.split('.')
        
        with codecs.open(f"{args.output_path / path.stem}.txt", "w", "utf-8") as stream: 
            for sentence in sentences:
                stream.write(sentence + ".\n")

if __name__ == '__main__':
    main()